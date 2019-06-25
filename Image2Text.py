"""A simple script to extract text from a scanned Image. """
""" **Image with tabular data is not supported ** """

from PIL import Image
import cv2
import argparse
import os
import pytesseract

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image to be OCR'd")
ap.add_argument("-p", "--preprocess", type=str, default="thresh", help="type of preprocessing to be done")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)


if args["preprocess"] == "thresh":
    gray = cv2.threshold(gray,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

elif args["preprocess"] == "blur":
    gray = cv2.medianBlur(gray,3)

filename = 'filename.jpg'
cv2.imwrite(filename,gray)
text = pytesseract.image_to_string(Image.open(filename))
os.remove(filename)

ImageText = open("ImageText.txt","w")
ImageText.write(text)
ImageText.close()
