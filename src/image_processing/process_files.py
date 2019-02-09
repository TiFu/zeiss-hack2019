FOLDER = "/home/tino/smt_image_data/SmtImageData/"
from image_processing import ImageProcessing
import cv2
import os
import numpy as np

filesForId = {}
imageProcessor = ImageProcessing()

print("Loading files")
for file in os.listdir(FOLDER):
    id = file.split("_")[0]
    if id not in filesForId:
        filesForId[id] = []
    filesForId[id].append(file)

print("Done loading files.")

print("Processing files")

outputFile = open("./displacements.csv", "w")

with outputFile:
    ids = len(filesForId)
    for id in filesForId:
        files = filesForId[id]
        if len(files) != 4:
            print("WHAT?")
        files.sort()
        print(files)
        beforeLeft = cv2.imread(FOLDER + files[0])
        beforeRight = cv2.imread(FOLDER + files[1])
        afterLeft = cv2.imread(FOLDER + files[2])
        afterRight = cv2.imread(FOLDER + files[3])
        try:
            displLeft, displRight, _, _, qualityScore = imageProcessor.determineDisplacement(beforeLeft, beforeRight, afterLeft, afterRight)
            print("Quality Score: " + str(qualityScore))
        except:
            continue
        
        outputFile.write(str(id) + "," + str(displLeft[0]) + "," + str(displLeft[1][0]) + "," + str(displLeft[1][1]) + "," + str(displRight[0]) + "," + str(displRight[1][0]) + "," + str(displRight[1][1]) + "," + str(qualityScore) + "\n")
        outputFile.flush()
        print(displLeft)
        print(displRight)