import cv2
import numpy as np
def organizeWindows(frame,windows):
    (h,w,c)=frame.shape
    if w>=h:
        organizeWindowsLandscape(windows)
    else:
        organizeWindowsPortrait(windows)

def organizeWindowsPortrait(windows):
    numWindows = len(windows)
    for k in windows:
        cv2.namedWindow(k, cv2.WINDOW_NORMAL)
    height = 1080
    width = 608
    for j in range(0,numWindows):
        cv2.resizeWindow(windows[j], int(width), int(height))
        cv2.moveWindow(windows[j], int(width*j), 0)

def organizeWindowsLandscape(windows):
    Screen = (1920, 1080)
    numWindows = len(windows)
    # find optimal arangement eg 2x3 instead of 1x6
    maxFactors = [numWindows, 1]
    col = 0
    row = 0
    for k in windows:
        cv2.namedWindow(k, cv2.WINDOW_NORMAL)
    for i in range(1, numWindows):
        if numWindows % i == 0:
            if abs((numWindows / i) - i) < abs(maxFactors[0] - maxFactors[1]):
                maxFactors[0], maxFactors[1] = numWindows / i, i
    width = int(1920 / maxFactors[0])
    height = int(1080 / maxFactors[0])
    for j in range(0, numWindows):
        cv2.resizeWindow(windows[j], int(width), int(height))
        cv2.moveWindow(windows[j], int(width * col), int(height * row))
        if ((col + 1) / maxFactors[0] == 1):
            col = 0
            row = row + 1
        else:
            col = col + 1

    def reject_outliers_2(list, m=2.):
        d = np.abs(list - np.median(list))
        mdev = np.median(d)
        s = d / (mdev if mdev else 1.)
        return list[s < m]

def showWindows(windows):
    for i in windows:
        cv2.imshow(i)

def reject_outliers_2(list, m):
    d = [x-np.median(list) for x in list]
    mdev = np.median(d)
    s = d / (mdev if mdev else 1.)
    return list[s < m]

