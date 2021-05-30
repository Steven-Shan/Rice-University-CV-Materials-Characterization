import cv2
import numpy as np
import csv
import os
print("In order to use this software, you must have ready a CSV file with its file location along with the file directory of the pictures")

#Let the user input file directory
fileInput = input("What is your file path to the images?")
desiredCSV = input("What is the file path to the CSV file where data is deposited? Include the CSV file in the file path")

#minimumSize
minimumSize = int(input("What is your image minimum size?"))

#Replace C:\Users\steven\Documents \ with /
UsableImageFilePath = fileInput.replace("\\", "/")
UsableCSVFilePath = desiredCSV.replace("\\", "/")

#os.listdir(filepath) returns an array of the name of each file
arr = os.listdir(UsableImageFilePath)

#Find only pictures in arr array by scanning everything
pictures = []
for x in range(0, len(arr)):
    if arr[x].find(".jpg") != -1 or arr[x].find(".tif") != -1:
        pictures.append(arr[x]) 

#starts CSV file
with open(UsableCSVFilePath, 'a', newline = '') as f:
        thewriter = csv.writer(f)
        thewriter.writerow(['File Title', 'Number of White Dots', 'Area of White Dots', 'Percent Picture White Dots'])
        
#loop through each file to extract the desired data
for x in range(0, len(pictures)):
    imageFile = pictures[x]
    image = cv2.imread(UsableImageFilePath + "/" + pictures[x])

    #filtering and thresholding
    blur = cv2.medianBlur(image, 5)
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray,128,255, cv2.THRESH_TOZERO)

    cnts, __ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    white_dots = []
    for c in cnts:
        area = cv2.contourArea(c)
        if area > minimumSize:
            cv2.drawContours(image, [c], -1, (36, 255, 12), 2)
            white_dots.append(c)

    #counting the area
    sumOfContours = 0
    for x in range(0, len(white_dots)):
        sumOfContours = sumOfContours + cv2.contourArea(white_dots[x])

    #calculating the size of the image and how much it takes
    height = np.size(image, 0)
    width = np.size(image, 1)

    #displaying the image
    cv2.imshow("Threshed Image", thresh)
    cv2.imshow("Image Binary", image)
    cv2.imwrite('image.png', image)
    cv2.waitKey()

    #printing stuff to the screen
    print(imageFile, end = ' ')
    print("                 ", end = ' ')
    print(len(white_dots), end = '' )
    print("                 ", end = ' ')
    print(sumOfContours, end = ' ')
    print("                 ", end = ' ')
    print (100* (sumOfContours/ (width * height)))
    amount = len(white_dots)
    percent = 100 * (sumOfContours/(width * height))

    #Reopesn and fills data to CSV
    with open(UsableCSVFilePath, 'a', newline = '') as f:
        thewriter = csv.writer(f)
        thewriter.writerow([imageFile, amount, sumOfContours, percent, "Soft Substrate"])

''''
        with open(UsableCSVFilePath, 'a', newline = '') as f:
            thewriter = csv.writer(f)
            thewriter.writerow([imageFile, cv2.contourArea(white_dots[x]), "Individual Dot", "Hard Substrate"])
'''
