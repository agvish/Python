"""Triangle Problem. Divide each of side of the triangle into n terms and store those co-ordinates.
Now check how may isosceles triangle can be formed with those new co-ordinates"""


import math


# function to calculate Euclidean Distance between 2 points
def calculate_euclidean_distance(x1, y1, x2, y2):
    dist = math.sqrt(math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2))
    return dist


# function to calculate area of 3 points and check if they are collinear
def calculate_area(x1, y1, x2, y2, x3, y3):
    return math.fabs(0.5 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)))


def triangle_operation(originalCoord, n):
    tempCoord1 = originalCoord.copy()                       # Copies Coordinates of Original Triangle to a Temporary List
    coord = []                                              # List to store Coordinates
    newCoord = []                                           # List to store new Coordinates after dividing each side
    tempCoord2 = []                                         # Temporary List to hold coordinates of Isosceles Triangle
    isoscelesCord = []                                      # List to store coordinates of a single Isosceles Triangle
    result = []                                             # List to store coordinates of all Isosceles Triangle

    # Loop to generate new coordinates for each side
    for i in range(0, 3):
        if i == 0:
            x1 = originalCoord[0][0]
            y1 = originalCoord[0][1]
            x2 = originalCoord[1][0]
            y2 = originalCoord[1][1]
        elif i == 1:
            x1 = originalCoord[1][0]
            y1 = originalCoord[1][1]
            x2 = originalCoord[2][0]
            y2 = originalCoord[2][1]
        else:
            x1 = originalCoord[2][0]
            y1 = originalCoord[2][1]
            x2 = originalCoord[0][0]
            y2 = originalCoord[0][1]
        for j in range(1, n):
            k = float(j/n)
            coord.append(int(x1 + k * (x2 - x1)))
            coord.append(int(y1 + k * (y2 - y1)))
            tempCoord1.append(coord)
            newCoord.append(coord)
            coord = []

    #Loop to generate coordinates of Isosceles Triangle
    """x1, x2, x3, y1, y2, y3 are used to hold abscissa and ordinates of coordinates has been generated previously"""
    for i in range(0, 3):
        x1 = originalCoord[i][0]
        y1 = originalCoord[i][1]
        j = i + 1
        while j < (len(tempCoord1) - 1):
            x2 = tempCoord1[j][0]
            y2 = tempCoord1[j][1]
            k = j + 1
            while k < len(tempCoord1):
                x3 = tempCoord1[k][0]
                y3 = tempCoord1[k][1]
                area = calculate_area(x1, y2, y1, y2, x3, y3)
                # If coordinates are collinear then next coordinate is chosen
                if area == 0:
                    k = k + 1
                    continue

                # Calculating the distance of each side
                side1_distance = calculate_euclidean_distance(x1, y1, x2, y2)
                side2_distance = calculate_euclidean_distance(x2, y2, x3, y3)
                side3_distance = calculate_euclidean_distance(x3, y3, x1, y1)
                coord = []
                if (side1_distance == side2_distance) or (side2_distance == side3_distance) or (side1_distance == side3_distance):
                    coord.append(x1)
                    coord.append(y1)
                    tempCoord2.append(coord)
                    coord = []
                    coord.append(x2)
                    coord.append(y2)
                    tempCoord2.append(coord)
                    coord = []
                    coord.append(x3)
                    coord.append(y3)
                    tempCoord2.append(coord)
                    coord = []

                # Removing the duplicate coordinate if any
                for cord in tempCoord2:
                    if cord not in isoscelesCord:
                        isoscelesCord.append(cord)
                tempCoord2 = []
                k = k + 1

            #Storing the resultant coordinates
            if len(isoscelesCord) > 0:
                result.append(isoscelesCord)
                isoscelesCord = []
            j = j + 1

    # Result Display
    print("\nOriginal Coordinates : ", originalCoord)
    print("New Coordinates after divison : ",newCoord)
    print("Resultant Coordinates of Isosceles Triangle :\n",result)


coord = []                                 # Stores coordinates
triangleCoord = []                         # Stores coordinates of triangle
for i in range(1,4):
    try:
        x = int(input("Enter the abscissa value of coordinate {0}: ".format(i)))
        y = int(input("Enter the ordinate value of coordinate {0}: ".format(i)))
    except ValueError:
        print("Not an integer.Try Again!!")
        exit()
    coord.append(x)
    coord.append(y)
    triangleCoord.append(coord)
    coord = []

try:
    n = int(input("Enter the value in which each side is to be decided: "))
except ValueError:
    print("Not an integer. Try Again!!")

# Function call to check the coordinates of isosceles triangle
triangle_operation(triangleCoord, n)
