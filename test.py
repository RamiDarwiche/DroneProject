import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
from cvzone.ClassificationModule import Classifier
import math
import json
import sqlite3

class HandGestures:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.detector = HandDetector(maxHands=1)
        self.classifier = Classifier("Model/keras_model.h5","Model/labels.txt")

        self.offset = 20
        self.imgSize = 300

        self.folder = "Data/Up"
        self.counter = 0

        self.labels = ["Back", "Down", "Forward", "Left", "Right", "Stop", "Up"]

        try:
            self.sqliteConnection = sqlite3.connect(r'C:\Users\darwi\test 6\Assets\gestures.db')
            self.cursor = self.sqliteConnection.cursor()
            self.count = self.cursor.execute("DELETE FROM Gestures")
            self.sqliteConnection.commit()
            print("Records deleted")
            self.cursor.close()

        except sqlite3.Error as error:
            print("Failed to delete data from sqlite table", error)
        finally:
            if self.sqliteConnection:
                self.sqliteConnection.close()
                print("The SQLite database is prepared")

    def run(self):
        while True:
            success, img = self.cap.read()
            imgOutput = img.copy()
            hands, img = self.detector.findHands(img)
            if hands:
                hand = hands[0]
                x, y, w, h = hand['bbox']

                imgCrop = img[y - self.offset:y + h + self.offset, x - self.offset:x + w + self.offset]
                imgCropShape = imgCrop.shape

                aspectRatio = h / w

                if aspectRatio > 1:
                    k = self.imgSize / h
                    wCal = math.ceil(k * w)
                    imgResize = cv2.resize(imgCrop, (wCal, self.imgSize))
                    imageResizeShape = imgResize.shape
                    wGap = math.ceil((self.imgSize - wCal) / 2)
                    imgWhite = np.ones((self.imgSize, self.imgSize, 3), np.uint8) * 255
                    imgWhite[:, wGap:wCal + wGap] = imgResize
                    prediction, index = self.classifier.getPrediction(imgWhite, draw=False)
                else:
                    k = self.imgSize / w
                    hCal = math.ceil(k * h)
                    imgResize = cv2.resize(imgCrop, (self.imgSize, hCal))
                    imageResizeShape = imgResize.shape
                    hGap = math.ceil((self.imgSize - hCal) / 2)
                    imgWhite = np.ones((self.imgSize, self.imgSize, 3), np.uint8) * 255
                    imgWhite[hGap:hCal + hGap, :] = imgResize
                    prediction, index = self.classifier.getPrediction(imgWhite, draw=False)

                with open("output.json", "w") as json_file:
                    json.dump(self.labels[index], json_file)

                try:
                    self.sqliteConnection = sqlite3.connect(r'C:\Users\darwi\test 6\Assets\gestures.db')
                    self.cursor = self.sqliteConnection.cursor()
                    self.count = self.cursor.execute("insert into Gestures (hand) values (?)", [self.labels[index]])
                    self.sqliteConnection.commit()
                    self.cursor.close()

                except sqlite3.Error as error:
                    print("Failed to insert data into sqlite table", error)
                finally:
                    if self.sqliteConnection:
                        self.sqliteConnection.close()

                cv2.putText(imgOutput, self.labels[index], (x - 26, y - 26), cv2.FONT_HERSHEY_COMPLEX, 1.7, (0, 0, 255), 2)
                cv2.rectangle(imgOutput, (x - self.offset, y - self.offset), (x + w + self.offset, y + h + self.offset), (0, 0, 255), 4)

            cv2.imshow("Image", imgOutput)
            key = cv2.waitKey(1)
            if key == 27:  # Press 'Esc' to exit the loop
                break

        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    hand_gestures = HandGestures()
    hand_gestures.run()
