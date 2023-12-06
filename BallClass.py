import math
import numpy as np
import functions


def reject_outliers_2(list, m):
    d = [x-np.median(list) for x in list]
    mdev = np.median(d)
    s = d / (mdev if mdev else 1.)
    return list[s < m]


class ball:
    lastUpdateFrame: object

    def __init__(self,rad, cenx, ceny, camfps):
        self.radius = [rad]
        frame = 0
        self.xstart = cenx
        self.ystart = ceny
        self.location = [(cenx, ceny, frame)]
        self.xlocation = self.location[len(self.location)-1][0]
        self.ylocation = self.location[len(self.location)-1][1]
        # creates list of locations

        self.radiusList = [rad]
        # condition to check if ball is moving
        self.struck = False
        self.frame_struck = -1
        self.speed = 0
        # easier to find index where ball starts moving
        self.index_struck = -1
        self.isThere = True
        self.lastUpdateFrame = 0
        self.camfps = camfps
    def updateBallLocation(self, loc, r, framewithCircle,f):
        self.location.append(loc)
        self.radius.append(r)
        self.lastUpdateFrame = framewithCircle
        self.isBallMoving()
        self.isBallThere(f)

    def updateBall(self, f):
        self.isBallMoving()
        self.isBallThere(f)


    def isBallMoving(self):
        if(len(self.location)>2):
            if(abs(float(self.location[len(self.location)-2][0])-float(self.location[len(self.location)-1][0]))>10 or abs(float(self.location[len(self.location)-2][1])-float(self.location[len(self.location)-1][1]))>10) and not self.struck:
                    self.struck = True
                    print('struck')
                    self.frame_struck = self.lastUpdateFrame-1
                    self.index_struck = len(self.location)



    def getBallSpeed(self):
        xinc = []
        yinc = []
        for i in range(self.index_struck, len(self.location)-1):
            xinc.append((float(self.location[i+1][0]-self.location[i][0]))/(self.location[i+1][2]-self.location[i][2]))
            yinc.append((float(self.location[i][1]-self.location[i+1][1]))/(self.location[i+1][2]-self.location[i][2]))

        # does not account for outliers
        if(len(xinc)>0 and len(yinc)>0):
            avgxinc = sum(xinc)/len(xinc)
            avgyinc = sum(yinc)/len(yinc)
            self.speed = math.sqrt(pow(avgxinc,2)+pow(avgyinc,2))
        else:
            self.speed = 0

    def isBallThere(self, frameCnt):
        if self.struck:
            if frameCnt-10>self.lastUpdateFrame:
                self.isThere=False
    def printFinalStats(self):
        self.getBallSpeed()
        i = 0
        radsum = 0
        for r in range(self.index_struck, len(self.location)-1):
            radsum = radsum + self.radius[r]
            i = i +1
        avgrad = radsum/i
        # radius of a golf ball = 0.84 inches
        ppi = 0.84 / avgrad
        # 30 frames in one second
        # 1/30 = seconds in a frame
        # 1 inch/second = 0.0568182 miles/hour
        print('the ball moved an average of ' + str(self.speed*ppi*self.camfps*0.0568182) + ' miles per hour, and had an average radius of ')







    def ballGone(self):
        del self

