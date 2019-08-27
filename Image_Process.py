"""This script will convert pdf pages to images.
The images will undergo some processing to improve its quality.
Following processing techniques are implemented:

1: Binarizing Image
2: Scaling Image
3: De-skewing Image
4: Denoising Image via erosion - dilation method
5: Eroding Image
6: Dilating Image
7: Denoising Image (Non local means denoising)"""

import pdf2image
import argparse
import os
import math
import shutil
import cv2
import numpy as np
from PIL import Image


class ImageProcessing:

    def __init__(self, input_file):
        self.input_file = input_file

    def pdf_to_image(self, input_directory):
        """ This method takes an 'PDF' file as input, convert each page of
        file to an image and saves them to a directory.
        Returns a list of image files"""

        image_file_names = []
        image_files = pdf2image.convert_from_path(self.input_file, 300)
        count = 0
        for files in image_files:
            filename = "/Images"+str(count)+".jpg"
            files.save(input_directory+filename, "jpeg")
            image_file_names.append(filename)
            count = count + 1

        return image_file_names

    def binarize_image(self, image_filepath):
        """This method converts a 3 channel (colored) image to a single channel
        (gray)image and performs simple thresholding using OTSU binarization.
        Returns thresholded image"""

        image_open = cv2.imread(image_filepath)
        gray_image = cv2.cvtColor(image_open, cv2.COLOR_BGR2GRAY)
        _, thresholded_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        return thresholded_image

    def scaling_image(self, image_filepath):
        """This method rescales the image to be saved at a particular DPI.
        Standard DPI 300 is set for each image.
        Returns a rescaled image."""
        image_open = Image.open(image_filepath)
        height, width = image_open.size
        factor = min(1, float(1024 / height))
        size = int(factor * height), int(factor * width)
        image_resized = image_open.resize(size, Image.ANTIALIAS)
        return image_resized

    def rotate_image(self, image_filepath):
        """This function method rotates the image to straighten it.
        Returns the correct rotated image"""

        image_open = cv2.imread(image_filepath)
        img_edges = cv2.Canny(image_open, 100, 100, apertureSize=3)
        lines = cv2.HoughLinesP(img_edges, 1, math.pi / 180.0, 100, minLineLength=100, maxLineGap=5)
        angles = []
        for x1, y1, x2, y2 in lines[0]:
            angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
            angles.append(angle)
        angle = np.median(angles)
        if angle < -45:
            angle = -(90 + angle)
        (height, width) = image_open.shape[:2]
        center = (width // 2, height // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated_image = cv2.warpAffine(image_open, M, (width, height), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        return rotated_image

    def remove_noise_image(self, image_filepath):
        """This method removes noise from the image.
        It invokes erosion and then dilation for noise removal.
        Return de-noised image"""

        eroded_image = self.erosion_image(image_filepath)
        cv2.imwrite(image_filepath, eroded_image)
        print("Image eroded ...")
        dilated_image = self.dilation_image(image_filepath)
        return dilated_image

    def erosion_image(self, image_filepath):
        """This method erodes the image.
        Returns eroded image."""

        image_open = cv2.imread(image_filepath)
        kernel = np.ones((3, 3), np.uint8)
        erosion = cv2.erode(image_open, kernel, iterations=1)
        return erosion

    def dilation_image(self, image_filepath):
        """This method dilates the image.
        Returns dilated image."""

        image_open = cv2.imread(image_filepath)
        kernel = np.ones((3, 3), np.uint8)
        dilation = cv2.dilate(image_open, kernel, iterations=1)
        return dilation

    def denoising_image(self, image_filepath, noise_param=10, template_window=7, search_window=21):
        """This method tends to remove noise from the image.
        It uses Non-Local Means Denoising algorithm.
        Returns denoised image."""

        image_open = cv2.imread(image_filepath)
        dst = cv2.fastNlMeansDenoisingColored(image_open, None, noise_param, noise_param, template_window, search_window)
        return dst


# Definition for Command Line Argument
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--file", required=True)
args = vars(ap.parse_args())
# Object creation for class
pdf_file_image = ImageProcessing(args["file"])
# Creating directories for storing image files
input_directory = os.getcwd() + "/Input_Image_Files"
temp_directory = os.getcwd() + "/Temp_Files"
access_rights = 0o755
try:
    os.mkdir(input_directory, access_rights)
    os.mkdir(temp_directory, access_rights)
except Exception:
    """If directories are present. Delete them and recreate to store new files"""
    print("Refreshing the directories for storing images......")
    shutil.rmtree(os.getcwd()+"/Input_Image_Files")
    shutil.rmtree(os.getcwd()+"/Temp_Files")
    os.mkdir(input_directory, access_rights)
    os.mkdir(temp_directory, access_rights)
# Convert PDF to Images
image_files = pdf_file_image.pdf_to_image(input_directory)

"""For testing purpose"""
# For graying and thresholding
print("Graying & Thresholding in progress..")
count = 0
for image in image_files:
    image_filename = input_directory + image
    gray_image = pdf_file_image.binarize_image(image_filename)
    cv2.imwrite(temp_directory+"/Gray"+str(count)+".jpg", gray_image)
    count = count + 1
# For scaling the images to standard dpi
print("Scaling to standard DPI in progress..")
count = 0
for image in os.listdir(temp_directory):
    image_filename = temp_directory + "/Gray"+str(count)+".jpg"
    rescaled_image = pdf_file_image.scaling_image(image_filename)
    rescaled_image.save(temp_directory+"/Gray"+str(count)+".jpg", dpi=(300, 300))
    count = count + 1
# For Rotating the images
print("Rotation (if any) in progress..")
count = 0
for image in os.listdir(temp_directory):
    image_filename = temp_directory + "/Gray"+str(count)+".jpg"
    rotated_image = pdf_file_image.rotate_image(image_filename)
    cv2.imwrite(temp_directory+"/Gray"+str(count)+".jpg", rotated_image)
    count = count + 1
# For Noise removal of images using Non-Local Means Denoising algorithm.
print("Noise Removal using Non-Local Means Denoising algorithm in progress..")
count = 0
for image in os.listdir(temp_directory):
    image_filename = temp_directory + "/Gray"+str(count)+".jpg"
    denoised_image = pdf_file_image.denoising_image(image_filename)
    cv2.imwrite(temp_directory+"/Gray"+str(count)+".jpg", denoised_image)
    count = count + 1
# For eroding image.
print("Eroding image in progress..")
count = 0
for image in os.listdir(temp_directory):
    image_filename = temp_directory + "/Gray"+str(count)+".jpg"
    denoised_image = pdf_file_image.erosion_image(image_filename)
    cv2.imwrite(temp_directory+"/Gray"+str(count)+".jpg", denoised_image)
    count = count + 1
# For Dilating image.
print("Dilating image in progress..")
count = 0
for image in os.listdir(temp_directory):
    image_filename = temp_directory + "/Gray"+str(count)+".jpg"
    denoised_image = pdf_file_image.dilation_image(image_filename)
    cv2.imwrite(temp_directory+"/Gray"+str(count)+".jpg", denoised_image)
    count = count + 1
# For Noise removal of images using erosion - dilation process.
print("Noise Removal using erosion - dilation process in progress..")
count = 0
for image in os.listdir(temp_directory):
    image_filename = temp_directory + "/Gray"+str(count)+".jpg"
    denoised_image = pdf_file_image.remove_noise_image(image_filename)
    cv2.imwrite(temp_directory+"/Gray"+str(count)+".jpg", denoised_image)
    count = count + 1
