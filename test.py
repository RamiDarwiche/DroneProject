import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
from cvzone.ClassificationModule import Classifier
import math
import json
import time
import sqlite3

class HandGestures:
    cap = cv2.VideoCapture(0)
    detector = HandDetector(maxHands=1)
    classifier = Classifier("Model/keras_model.h5","Model/labels.txt")

    offset = 20
    imgSize = 300

    folder = "Data/Up"
    counter = 0

    labels = ["Back", "Down", "Forward", "Left", "Right", "Stop", "Up"]

    try:
        sqliteConnection = sqlite3.connect(r'C:\Users\darwi\test 6\Assets\gestures.db')
        cursor = sqliteConnection.cursor()
        count = cursor.execute("DELETE FROM Gestures")
        sqliteConnection.commit()
        print("Records deleted")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to delete data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite database is prepared")

    while True:
        success, img = cap.read()
        imgOutput = img.copy()
        hands, img = detector.findHands(img)
        if hands:
            hand = hands[0]
            x,y,w,h = hand['bbox']

            imgWhite = np.ones((imgSize,imgSize,3),np.uint8)*255
            imgCrop = img[y-offset:y + h+offset,x-offset:x + w+offset]

            imgCropShape = imgCrop.shape


            aspectRatio = h/w

            if aspectRatio >1:
                k = imgSize/h
                wCal = math.ceil(k*w)
                imgResize = cv2.resize(imgCrop, (wCal,imgSize))
                imageResizeShape = imgResize.shape
                wGap = math.ceil((imgSize -wCal)/2)
                imgWhite[:,wGap:wCal+wGap] = imgResize
                prediction, index = classifier.getPrediction(imgWhite, draw=False)
                #print(prediction,index)
                with open("output.json", "w") as json_file:
                    output = json.dump(labels[index], json_file)
                    #print("updated")
                    json_file.close()
                #print(labels[index])
                try:
                    sqliteConnection = sqlite3.connect(r'C:\Users\darwi\test 6\Assets\gestures.db')
                    cursor = sqliteConnection.cursor()
                    #print("Successfully Connected to SQLite")

                    count = cursor.execute("insert into Gestures (hand) values (?)", [labels[index]])
                    sqliteConnection.commit()
                    #print("Record inserted successfully into Sqlite Gestures table ", cursor.rowcount)
                    cursor.close()

                except sqlite3.Error as error:
                    print("Failed to insert data into sqlite table", error)
                finally:
                    if sqliteConnection:
                        sqliteConnection.close()
                        #print("The SQLite connection is closed")

            else:
                k = imgSize/w
                hCal = math.ceil(k*h)
                imgResize = cv2.resize(imgCrop, (imgSize,hCal))
                imageResizeShape = imgResize.shape
                hGap = math.ceil((imgSize -hCal)/2)
                imgWhite[hGap:hCal+hGap, :] = imgResize
                prediction, index = classifier.getPrediction(imgWhite, draw=False)

            #cv2.rectangle(imgOutput, (x - offset, y - offset-50), (x-offset+250, y - offset-50+50), (255, 255, 255), cv2.FILLED)
            cv2.putText(imgOutput, labels[index],(x-26,y-26), cv2.FONT_HERSHEY_COMPLEX,1.7,(0,0,255),2)
            cv2.rectangle(imgOutput,(x-offset,y-offset),(x+w+offset,y+h+offset),(0,0,255), 4)


            #cv2.imshow("ImageCrop", imgCrop)
            #cv2.imshow("ImageWhite", imgWhite)

        cv2.imshow("Image",imgOutput)
        key = cv2.waitKey(1)
