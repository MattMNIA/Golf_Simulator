from typing import Any

import cvzone
from cvzone.ColorModule import ColorFinder
from numpy import ndarray, dtype

import functions
import cv2
import numpy as np
import time
import os
from BallClass import ball
import warnings

warnings.filterwarnings('ignore')

path = os.getcwd()

video = ("Golf Ball Hit.mp4")

cap = cv2.VideoCapture(video)
fps = cap.get(cv2.CAP_PROP_FPS)
# Pull up HSV filter
showColor = False
myColorFinder = ColorFinder(showColor)
# Get size of Video
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
# Initiate Background Subtractor
backgroundsub = cv2.createBackgroundSubtractorMOG2(history = 15)
backgroundsubKNN = cv2.createBackgroundSubtractorKNN(history = 15)
GreenMin = (40,0, 0)
GreenMax = (95, 255, 255)
# read first frame
openKernel = np.ones((5,5),np.uint8)
closeKernel = np.ones((5,5),np.uint8)
diKernel = np.ones((5,5),np.uint8)
hsvVals = {'hmin': 0, 'smin': 0, 'vmin': 32, 'hmax': 179, 'smax': 55, 'vmax': 255}
points = []
frameCnt = 0
shapeMask = np.zeros((height, width), dtype="uint8")
circleThere: bool = False

while True:
    ret, frame = cap.read()

    frameCnt = frameCnt + 1
    # Create Windows
    windows = ["frame", "ballHole", 'finalFrame', 'movingFrame']
    if showColor:
        frameColor, mask = myColorFinder.update(frame, hsvVals)
        windows.append('image')
        functions.organizeWindows(frame,windows)
        cv2.imshow('image', frameColor)

    # Organize Windows
    functions.organizeWindows(frame, windows)
    # Apply Masks
    fgmask = backgroundsub.apply(frame, None, .5)
    blur = cv2.GaussianBlur(frame, (3,3), 20)
    fgmaskKNN = backgroundsubKNN.apply(frame, None, .9)
    closed = cv2.morphologyEx(fgmaskKNN, cv2.MORPH_CLOSE, closeKernel)
    opening = cv2.morphologyEx(closed, cv2.MORPH_OPEN, openKernel)
    dilated = cv2.dilate(fgmaskKNN, diKernel, iterations=1)
    mask = cv2.bitwise_or(fgmaskKNN, shapeMask)
    movingFrame = cv2.bitwise_and(frame, frame, mask = fgmaskKNN)
    finalFrame = cv2.bitwise_and(frame, frame, mask=mask)
    cv2.imshow('finalFrame', finalFrame)
    gray = cv2.cvtColor(finalFrame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('movingFrame', movingFrame)
    if circleThere:
        cv2.circle(shapeMask,(a,b), r,255,3)
        # print(golfBall.lastUpdateFrame)
    # Blur using 3 * 3 kernel.
    gray_blurred = cv2.blur(gray, (7, 7))
    # Apply Hough transform on the blurred image.
    detected_circles = cv2.HoughCircles(gray_blurred,
                                        cv2.HOUGH_GRADIENT, 1.5, 10000, param1=200,
                                        param2=35, minRadius=30, maxRadius=150)
    if circleThere:
        circleThere = golfBall.isThere
    # Draw circles that are detected.
    if detected_circles is not None:

        # Convert the circle parameters a, b and r to integers.
        detected_circles = np.uint16(np.around(detected_circles))

        for pt in detected_circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]
            if (not circleThere):
                # golfBall = ball(r, a, b, fps)
                golfBall = ball(r, a, b, 1000)

            # Draw the circumference of the circle.
            cv2.circle(frame, (a, b), r, (0, 255, 0), 2)
            # Draw a small circle (of radius 1) to show the center.
            cv2.circle(frame, (a, b), 1, (0, 0, 255), 3)
            shapeMask= np.zeros((height, width), dtype="uint8")
            cv2.circle(shapeMask, (a,b), int(r*1.2), 255, -1)

            ballHole = cv2.bitwise_or(frame, finalFrame, mask=shapeMask)
            cv2.imshow("ballHole", finalFrame)
            circleFrame = frameCnt
            if (circleThere):
                golfBall.updateBallLocation((a,b,frameCnt),r,circleFrame, frameCnt)
            circleThere = True

    else:
        cv2.imshow("ballHole", finalFrame)
        if(circleThere):
            golfBall.updateBall(frameCnt)
    # check ball attributes

    if (circleThere):
        if not (golfBall.isThere):
            golfBall.printFinalStats()
    cv2.imshow('frame',frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# for i in points:

cap.release()
cv2.destroyAllWindows()
