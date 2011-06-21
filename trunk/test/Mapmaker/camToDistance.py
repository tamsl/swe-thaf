# camToDistance.py
# This file holds code to convert pixel locations into distances from the camera.
# Author: Max Korbel
# This file is part of the HMC PixelLaser research project.
# Advisor: Zach Dodds

import math
from Tkinter import *
import time
from datetime import datetime
import re
import cv
import os
import shutil
import operator
import Segmenter as seg

import Map

from numpy import *
from numpy.linalg import lstsq

# The calibration file
# Its organized by:
# MAXX  MAXY    HORIZON
# ACTUALDISTANCE    PIXELX  PIXELY
# ACTUALDISTANCE    PIXELX  PIXELY
# ACTUALDI...


################################################
# We left off at 1582 for the halls building... #
#################################################

STANDARDMAXX = 640
STANDARDMAXY = 480

CALIBFILE = 'distpixcalib2.txt'
CALIBOUTFILE = 'distpixendcalibration.txt'
DPSLAMOUT = 'dpslamout.log'
PICTURESFOLDER = '../Pictures/'
ODOMLOGFILE = 'odometrylog.txt'
PICLOGFILE = 'PictureTimes.txt'
PICODOMFILE = 'PicOdom.txt'
LASERMAPSFILESTART = '../LaserMaps Playground/'

# the maximum distance away something could be (in inches)
# this variable stops some random distances from being really far away
MAXDISTANCE = 400

# the span of the camera angle in degrees
CAMERASPAN = 58 # This could be off a little bit...

# the number of lasers for output expected by DP-SLAM
NUMLASERS = 181


def getOdomForPics(odomLog, picLog):
    '''
    Returns the odometry for the given pictures
    This method linearly extrapolates odometry based on time
    odomLog is a list of lists, each containing a datetime and odoometry:
        it looks like:
        [
            [datetime1, x, y, thr]
            ...
        ]
    pic log is a list of lists, each has the string picName and datetime
        it looks like:
        [
            [picName, datetime1]
            ...
        ]
    this method returns a list of of pic names with corresponding odometry
        it looks like:
        [
            [picName, x, y, thr]
            ...
        ]
    '''
    outList = []
    for pic in picLog:
        lastOdom = odomLog[0]
        picOdom = []
        for odom in odomLog:
            if lastOdom[0] < pic[1] and pic[1] <= odom[0]:
                deltaLast = pic[1] - lastOdom[0]
                deltaCur = odom[0] - pic[1]
                
                # assume the entries in odometry are less than 60 sec appart
                diffLast = float(deltaLast.microseconds) +\
                           float(deltaLast.seconds)*10.0**6
                diffCur = float(deltaCur.microseconds) +\
                          float(deltaCur.seconds)*10.0**6

                # kinda the percentage of the way till the next odometry point
                ratio = diffLast/(diffCur + diffLast)
                opRatio = 1.0-ratio

                #print diffCur, ratio
                

                # just do a weighted average
                picOdom = [\
                    pic[0],\
                    ratio*odom[1] + opRatio*lastOdom[1],\
                    ratio*odom[2] + opRatio*lastOdom[2],\
                    ratio*odom[3] + opRatio*lastOdom[3]]
                break
            else:
                lastOdom = odom
        if picOdom == []:
            print "Warning: not enough odometry info found for " + pic[0]
            picOdom = [pic[0], lastOdom[1], lastOdom[2], lastOdom[3]]
                
        # append the odometry (or empty if we found none)
        outList.append(picOdom)
    return outList

def getOdomForPicsFromFolder(folder):
    '''
    takes in a folder in the default pictures directory and returns odometry
    for the pictures
    this method uses getOdomForPics and all of its formats
    '''
    picLogFile = open(PICTURESFOLDER + folder + '/' + PICLOGFILE)
    odomLogFile = open(PICTURESFOLDER + folder + '/' + ODOMLOGFILE)

    odomLog = []
    picLog = []

    for line in picLogFile:
        lineArray = line.split('\t')
        lineArray[1] = lineArray[1].strip()
        t = re.split(r"[\r\n\s\.:-]+",lineArray[1])
        # append a zero in case there are no microseconds
        t.append(0)
        dt = datetime(int(t[0]), int(t[1]), int(t[2]),
                      int(t[3]), int(t[4]), int(t[5]), int(t[6]))
        pic = [lineArray[0],\
               dt]
        picLog.append(pic)
    for line in odomLogFile:
        lineArray = line.split('\t')
        lineArray[0] = lineArray[0].strip()
        t = re.split(r"[\r\n\s\.:-]+",lineArray[0])
        dt = datetime(int(t[0]), int(t[1]), int(t[2]),
                      int(t[3]), int(t[4]), int(t[5]), int(t[6]))
        odom = [dt, 
                float(lineArray[1]),
                float(lineArray[2]),
                float(lineArray[3].strip())]
        odomLog.append(odom)
        
    picLogFile.close()
    odomLogFile.close()

    #print odomLog
    #print picLog

    return getOdomForPics(odomLog, picLog)

def writePicOdomToFile(folder="20100621T100418"):
    '''
    Calls getOdomForPicsFromFolder and saves output to PICODOMFILE
    '''
    print "Extrapolating..."
    info = getOdomForPicsFromFolder(folder)
    pofile = open(PICTURESFOLDER + folder + '/' + PICODOMFILE, 'w')
    for a in info:
        for b in a:
            pofile.write(str(b) + '\t')
        pofile.write('\n')
    print "Done! Wrote to " + PICTURESFOLDER + folder + '/' + PICODOMFILE

    
def testWrite(folder="20100617T104520"):
    standardFileStart = PICTURESFOLDER + folder +'/000'
    data = []
    i = 3
    while i <= 6:
        x = 0
        pointset = []
        extra = "0"
        if i >= 10:
            extra = ""
        name = standardFileStart + extra + str(i) + ".txt"
        f = open(name)
        for line in f:
            pointset.append([x, int(line)])
            x += 1
        data.append([pointset, [(i-3)*200.0/1000.0,0.0,0.0]])
        print "Done reading in:\t" + name
        i += 1
    print "Converting..."
    dpslamData(data)
    print "DONE"

def labelImage(folder, image, linePoints):
    '''
    Will create the necessary txt file for a given image (y vals, one per line)
    folder is a string containing the folder that has the images
    image is a string name of the image
        ******(NO .png included!! eg: '00004')******
    linePoints is an array of points, this method will linearly extrapolate the
        points inbetween given points. it looks like:
        [ [x, y] [x, y] ...]
        the list should be sorted by increasing x
    '''
    standardFileStart = PICTURESFOLDER + folder +'/'
    f = open(standardFileStart + '/' + image + '.txt', 'w')
    i = 0
    while i <= linePoints[len(linePoints)-1][0]:
        lastPoint = linePoints[0]
        for point in linePoints:
            if lastPoint[0] < i and i <= point[0]:
                lastDiff = float(i - lastPoint[0])
                currDiff = float(point[0] - i)

                # kinda like the percentage of the way to currPoint
                ratio = lastDiff / (lastDiff + currDiff)
                opRatio = 1-ratio

                # weighted average
                iy = lastPoint[1]*opRatio + point[1]*ratio

                # write to the file
                f.write(str(int(iy)) + '\n')
                
                break
            else:
                lastPoint = point
        i += 1
    f.close()


def runFull():
    '''
    Just runs dpslamDataFromFolder() with no arguments
    '''
    dpslamDataFromFolder()



def dpslamDataFromFolder(folder="20100706T154750",
                         reCalcPicOdom=True, reSegmentLabel=True):
    '''
    Will create a dpslam output file given a folder with proper files within
    Requires PICLOGFILE, ODOMLOGFILE, (or PICODOMFILE)
    and text files for each image that give the pixels of the obstacle line
    (just a bunch of y's one0.0
 per line)
    set reSegmentLabel=True to create these text files
    '''
    
    if reCalcPicOdom:
        print "Recalculating PICODOMFILE..."
        writePicOdomToFile(folder)
    standardFileStart = PICTURESFOLDER + folder + '/'
    pofile = open(standardFileStart + PICODOMFILE)
    
    if reSegmentLabel:
        print "Will resegment and label images..."


    print "Creating data array..."
    
    data = []
    for line in pofile:
        splitLine = line.split()
        if len(splitLine) == 0:
            print "Not enough information in PICODOMFILE. " +\
                  "Check if pictures were taken after the last odometry reading."
        else:
            im = cv.LoadImage(standardFileStart + '/' + splitLine[0] + '.png')
            if im[0,0] != (0.0, 0.0, 0.0):
                pointset = []
                if reSegmentLabel:
                    print "Segmenting " + str(splitLine[0])
                    segPoints = seg.segment(im)
                    print "Segmented points:  ", segPoints
                    labelImage(folder, splitLine[0], segPoints)
                pxFile = standardFileStart + '/' + splitLine[0] + '.txt'
                pxPath = open(pxFile)

                x = 0
                for l in pxPath:
                    pointset.append([x, int(l)])
                    x += 1

                # I have no clue what happened here but it still works....
                data.append([pointset,
                             [splitLine[1],
                              splitLine[2],
                              splitLine[3]]])
            else:
                print "All black image detected! Skipping " + str(splitLine[0])

    print "Done."
    print "dpslamming..."
    dpslamData(data, standardFileStart)
    print "Done!"
    

def dpslamData(data, outFolder=""):
    '''
    Creates an entire dpslam formatted output file
    data is formatted as follows:
    [
        [                              <-- this is a single time step
            [x1, y1], [x2, y2], ... ], <-- this is a set of points
            [x, y, theta]              <-- this is the odometry
        ],
        [
            [x1, y1], [x2, y2], ... ],
            [x, y, theta]
        ]....
    ]0.0


    DPSLAM output file format:
    
    ODOMETRY <x> <y> <theta>
    The first argument denotes this as a reading from the robot's odometer. 
    <x> and <y> are the robot's current position from some arbitrary 
    starting point. These measures are in meters. <theta> is robot's 
    current facing angle, in radians.

    LASER <number> <values>...
    <number> is the number of laser readings that were observed.  
    Those actual laser measurements are the values that follow, in meters.
    The values are evenly spaced throughout the span of the camera

    Theres a good example of this file format in dpslamout.log
    Basically it looks like:
        Odometry 0.2 0.0 0.0
        Laser 181 1.13315686528 1.13755059359 1.14751869748 ....
        Odometry 0.6 0.0 0.0
        Laser 181 0.823853288756 0.829595445674 0.83142457855 ....
        ....

    The NUMLASERS variable can vary as we experiment with SLAM
        
    '''
    # erase the old file
    f = open(outFolder + '/' + DPSLAMOUT, 'w')
    f.close()

    # now write the new one
    for timestep in data:
        dpslamPoint(timestep[0], timestep[1], outFolder)
    

def dpslamPoint(points, odometry, outFolder=""):
    '''
    Writes a line to the dpslam formatted output file
    points is an array of points [x, y] at the floor of an obstacle
    odometry is [x, y, theta] from the roomba [mm, mm, rad]
    this method ADDS A LINE, does not erase the old data
    '''
    numLasers = NUMLASERS
    rX = float(odometry[0])/1000.0
    rY = float(odometry[1])/1000.0
    rThr = math.degrees(float(odometry[2]))
    #f = open(outFolder + '/' + DPSLAMOUT, 'a')
    #f.write("Odometry " + str(rX) + " " +\
    #        str(rY) + " " + str(rThr) + "\n")
    laserString = "Laser " + str(numLasers)
    i = 0.0
    while i < numLasers:
        point = points[ int(math.floor(i*(float(len(points)))/float(numLasers))) ]
        D = (1.0/1000.0) * toMillimeters( convertPixToD(point[0],point[1]) )
        laserString += " " +str( D )
        i += 1.0
    #f.write(laserString + "\n")
    #f.close()
    return laserString


def testDrawDists(i=3, folder = "20100617T104520"):
    standardFileStart = PICTURESFOLDER + folder +'/000'
    x = 0
    pointset = []
    extra = "0"
    if i >= 10:
        extra = ""
    name = standardFileStart + extra + str(i) + ".txt"
    f = open(name)
    for line in f:
        pointset.append([x, int(line)])
        x += 1
    print "Done reading in points. Drawing..."
    drawDists(pointset)

def getPointsFromFile(inFile):
    '''
    Returns a list of points from the files of the form 00001.txt (for example)
    The output looks like [ [0, y1], [1, y2], ...] ]
    '''
    x = 0
    pointset = []
    f = open(inFile)
    for line in f:
        pointset.append([x, int(line)])
        x += 1
    return pointset

def drawPointsInFile(inFile, canvas=None, canvasSize=540, loc=[0,0]):
    '''
    Draws the points in a file
    canvasSize is the size of the canvas (or part of canvas) to draw on
    pass it a canvas if you want it to draw on a certain canvas,
        otherwise it will make its own
    loc is the location on the canvas you want to draw on in [x,y] format
    '''
    drawDists(getPointsFromFile(inFile), canvas, canvasSize, loc)

def drawDists(points, canvas=None, canvasSize=540, loc=[0,0]):
    '''
    Draws lines representing the distances to all the points.
    points is an array of points [x, y] at the floor of an obstacle
    Should look like an overhead map of the place...
    '''


    # array of processed points in the form [D, theta]
    processedPoints = []
    maxD = 1
    i = 0
    for point in points:
        D = convertPixToD(point[0],point[1])
        if D > maxD:
            maxD = D
        processedPoints.append([\
            D,\
            angleFromStraightForDrawing(\
                point[0],point[1],STANDARDMAXX,STANDARDMAXY)])
        i += 1
    
    # now to scale all the points to fit on the canvas
    scalingFactor = 0.9*float(canvasSize)/maxD
    for point in processedPoints:
        point[0] = scalingFactor * point[0]

    # now draw stuff

    if canvas == None:
        canvas = Canvas(root, width=canvasSize, height=canvasSize, bg='white')
        root = Tk()
        root.title('Distance map')
        for point in processedPoints:
            x = canvasSize/2 -\
                point[0]*math.sin(point[1])
            y = canvasSize - point[0]*math.cos(point[1])
            canvas.create_line( canvasSize/2, \
                                canvasSize, \
                                x, \
                                y)
        canvas.pack(expand=YES, fill=BOTH)
        root.mainloop()
        
    else:
        for point in processedPoints:
            x = canvasSize/2 -\
                point[0]*math.sin(point[1])
            y = canvasSize - point[0]*math.cos(point[1])
            canvas.create_line( loc[0]+canvasSize/2, \
                                loc[1]+canvasSize, \
                                loc[0]+x, \
                                loc[1]+y)
            canvas.create_text(loc[0], loc[1]+30,
                               text="Max distance shown: " +\
                               "%4.2f"%maxD + " inches.")
            


def probabilityAtPointInMap(scan, pos, inMap, drawIt=False):
    '''
    Gives a probability that the scan was taken at the given pos in the map
    The map is read in from LASERMAPSFILE
    pos is [x, y, thd]
    scan looks like [ [r, thd], [r, thd],... ]
    '''

    # use slope variable
    useSlope = False
    
    scale = inMap.scale
    
    maxThd = scan[len(scan)-1][1]
    minThd = scan[0][1]

    if drawIt:
        drawLaserMap(pos[0]*scale, pos[1]*scale, scan, pos[2])
        
    # there will be one distance per degree in this scan
    adjustedScan = []
    thd = int(minThd)
    while thd <= maxThd:
        x = len(scan)-1.0
        lastScan = scan[0]
        while x >= 0:
            thisScan = scan[int(x)]

            thisThd = thisScan[1]
            lastThd = lastScan[1]

            if thisThd < thd:
                lastDiff = thd - lastThd
                thisDiff = thisThd - thd

                ratio = lastDiff/(lastDiff + thisDiff)
                opRatio = 1.0 - ratio

                adjustedScan.append([ thisScan[0]*ratio + lastScan[0]*opRatio,
                                      thd + pos[2]])
                break
            else:
                lastScan = thisScan
            x -= 1
        thd += 1

    # now we have something kinda like -29 degrees to 29 degrees (for example)
    # plus the position theta
    # now we want to compare to the map we took
    # lets load up the map from the file

##    relevantLaserMap = []
##    # convert back to centimeters again
##    try:
##        f = open(LASERMAPSFILESTART + 'lm_' +\
##                 str(int(pos[0]*scale+.5)) + '_' +\
##                 str(int(pos[1]*scale+.5)) + '.txt')
##    except:
##        # if the file doesnt exist (WHICH IS BAD) look for something close
##        print "MISSING A FILE FOR " + str(pos[0]) + ", " + str(pos[1]) + "!!!!"
##        f = open(LASERMAPSFILESTART + 'lm_' +\
##                 str(int(pos[0]*scale-.5)) + '_' +\
##                 str(int(pos[1]*scale-.5)) + '.txt')
##    line = f.readline().strip('[').strip('\n').strip(']')
##    splitLine = line.split(', ')
##    relevantLaserMap = splitLine
##    f.close()

    ''' OLD CODE, READS ONE FILE instead of thousands
    for line in f:
        line = line.strip('[').strip('\n').strip(']')
        splitLine = line.split(', ')
        if pos[0] == int(splitLine[0]) and pos[1] == int(splitLine[1]):
            relevantLaserMap = splitLine
    f.close()
    '''

    
    relevantLaserMap = inMap.getLaserMap(int(pos[0]*scale+.5),
                                         int(pos[1]*scale+.5),
                                         LASERMAPSFILESTART,
                                         loadToMemory=False)
    
    
    # right now use a fairly simple abs difference algorithm

    # a list of differences and their percent errors to take the best of them
    diffList = []

    if useSlope:
        # a list of differences in slope between points and their percent errors
        # to take the best of them
        slopeDiffList = []
        # Interval between which you look at the slope. Avoid too small intervals
        slopeInterval = 5
        oldScanDist = None
        oldMapDist = None
    
    maxPercentError = 2.0
    maxSlopePercentError = 2.5
    
    #Keep track of which number scan is being compared (need every
    scanNum = 0
    # relevantLaserMap goes from 0 to 359 degrees
    for scanLine in adjustedScan:
        scanDist = float(scanLine[0])
        mapDist = float(relevantLaserMap[2 + int(validDegrees(scanLine[1]))])
        if mapDist > Map.inchesToMeters(MAXDISTANCE):
            mapDist = Map.inchesToMeters(MAXDISTANCE)
        #absDifference = abs(scanDist - mapDist)
        absDifference = math.sqrt(abs(scanDist**2 - mapDist**2))
        if mapDist <= 0.0:
            percentError = maxPercentError
        else:
            percentError = absDifference / mapDist
        diffList.append([absDifference, percentError])

        if useSlope:
            # Slope
            if scanNum == 0:
                oldScanDist = scanDist
                oldMapDist = mapDist
            elif scanNum%slopeInterval == 0:
                scanSlope = scanDist - oldScanDist
                mapSlope = mapDist - oldMapDist
                #print "mapDist:", mapDist, "oldMapDist", oldMapDist
                #print scanSlope, "vs", mapSlope
                absSlopeDifference = abs(scanSlope - mapSlope)
                if mapSlope == 0 and scanSlope != 0:
                    percentSlopeError = maxSlopePercentError
                elif mapSlope == 0 and scanSlope == 0:
                    percentSlopeError = 0.0
                else:
                    percentSlopeError = absSlopeDifference / abs(mapSlope)
                slopeDiffList.append([absSlopeDifference, percentSlopeError])
                oldScanDist = scanDist
                oldMapDist = mapDist
            scanNum += 1
    # take just the best of the data (distance and slope)
    BESTPERCENTAGE = .95
    #uncomment this if BESTPERCENTAGE != 1.0
    diffList = sorted(diffList,
                      key=operator.itemgetter(1),
                      reverse=True) 
    bestDiffsList = diffList[:int(BESTPERCENTAGE*len(diffList))]
    if useSlope:
        slopeDiffList = sorted(slopeDiffList,
                               key=operator.itemgetter(1),
                               reverse=True) 
        bestSlopeDiffList = slopeDiffList[:int(BESTPERCENTAGE*len(diffList))]
    
    # find the average percent error
    sumOfErrors = 0.0
    for pair in bestDiffsList:
        sumOfErrors += pair[1]
        
    if useSlope:
        sumOfSlopeErrors = 0.0
        for pair in bestSlopeDiffList:
            sumOfSlopeErrors += pair[1]

    avgError = sumOfErrors / len(bestDiffsList)
    if avgError > maxPercentError:
        avgError = maxPercentError

    avgError /= maxPercentError

    if useSlope:
        avgSlopeError = sumOfSlopeErrors / len(bestSlopeDiffList)

        if avgSlopeError > maxSlopePercentError:
            avgSlopeError = maxSlopePercentError

        avgSlopeError /= maxSlopePercentError
        print "AvgSlopeError", avgSlopeError

    # avgError will be 0.0 if they all  match up perfectly
    # and 1.0 if they are all at least 100% error
    # so 1 - avgError should give something that looks like probability
    if useSlope:
        probability = ( (1.0 - avgError) + (1.0 - avgSlopeError) )/ 2.0
    else:
        probability = 1.0 - avgError
    #print "Prob: ", probability
    return probability


def validDegrees(degrees):
    if(degrees >= 360):
        return validDegrees(degrees - 360)
    elif(degrees < 0):
        return validDegrees(degrees + 360)
    return int(degrees)
    
    

def buildLaserMaps(inMap):
    '''
    Will create a 360 degree laser scan at all positions in the given map.
    Will save it to a file
    inMap is a Map object
    This method is VERY SLOW.  You do NOT want to do this often.
    '''

    #mapSize = int(math.sqrt(float(len(inMap))))

    XRES = 1.0/inMap.scale
    YRES = 1.0/inMap.scale

    print XRES, YRES

    # a list of lists, looks like:
    # [ [x, y, laserAtDeg1, laserAtDeg2, laserAtDeg3,...], ...]
    #laserMaps=[]


    # gettin ready to save files
    #shutil.rmtree(LASERMAPSFILESTART)
    #os.mkdir(LASERMAPSFILESTART)

    x = 1581.0/inMap.scale
    while x < len(inMap.mapArray)/inMap.scale:
        y = 0.0
        while y < len(inMap.mapArray[0])/inMap.scale:
            thd = 0
            laserMap = [x,y]
            while thd < 360:
                thr = math.radians(thd)
                #print thd
                laserMap.append(
                    distToWall(inMap,
                               [laserMap[0],
                                laserMap[1],
                                thr]))
            
                thd += 1
            #print laserMap
            #laserMaps.append(laserMap)

            # save to the correct file
            # convert back to pixels
            saveLoc = LASERMAPSFILESTART + 'lm_' +\
                      str(int(laserMap[0]*inMap.scale+.5)) + '_' +\
                      str(int(laserMap[1]*inMap.scale+.5)) + '.txt'
            f = open(saveLoc, 'w')
            if y == 0:
                print "Wrote " + saveLoc
            f.write(str(laserMap))
            f.close()
            
            #print "Done with (" + str(x) + ", " + str(y) + ")"
            y += YRES
            #y = round(y, 2)
        #print "Done with row " + str(x)
        x += XRES
        #x = round(x, 2)

    
    # print laserMaps
    # print "Saving to files..." 
    # this will print each line into a separate file for efficiency later
    # files look like LASERMAPSFILESTART/lm_x_y.txt

    
    
##    x = 0
##    for laserMap in laserMaps:
##        # convert back to pixels
##        saveLoc = LASERMAPSFILESTART + 'lm_' +\
##                  str(int(round(laserMap[0],2)*inMap.scale+.5)) + '_' +\
##                  str(int(round(laserMap[1],2)*inMap.scale+.5)) + '.txt'
##        f = open(saveLoc, 'w')
##        if x%1000 == 0:
##            print "Wrote " + saveLoc
##        f.write(str(laserMap))
##        f.close()
##        x += 1
    
    #return laserMaps


def drawLaserMap(x, y, scan=None, scanAngle=None):
    '''
    x, y lm file
    put a scan in to compare it to the laser map
        scan looks like [ [r, thd], [r, thd],... ]
    '''

    drawSize = 1000
    
    relevantLaserMap = []
    # convert back to centimeters again
    f = open(LASERMAPSFILESTART + 'lm_' +\
             str(int(x)) + '_' + str(int(y)) + '.txt')
    line = f.readline().strip('[').strip('\n').strip(']')
    splitLine = line.split(', ')
    relevantLaserMap = splitLine
    f.close()


    root = Tk()
    canvas = Canvas(root, width=drawSize, height=drawSize, bg='white')
    root.title('Laser map')

    i = 2
    while i < len(relevantLaserMap):
        laserDist = int(100*float(relevantLaserMap[i]))
        #print laserDist
        finalX = laserDist*math.cos(math.radians(i-2)) + drawSize/2
        finalY = laserDist*math.sin(-math.radians(i-2)) + drawSize/2
        canvas.create_line(drawSize/2,
                           drawSize/2,
                           finalX,
                           finalY)
        i += 1

    if scan != None:
        for ray in scan:
            laserDist = int(100*float(ray[0]))
            angle = math.radians(ray[1] + scanAngle)
            finalX = laserDist*math.cos(angle) + drawSize/2
            finalY = laserDist*math.sin(-angle) + drawSize/2
            canvas.create_line(drawSize/2,
                               drawSize/2,
                               finalX,
                               finalY,
                               fill="blue")
            
                           
    canvas.pack(expand=YES, fill=BOTH)
    root.mainloop()
    

def distToWall(inMap, pos):
    '''
    A helper method for buildLaserMaps.
    Finds the distance to a wall in the map from a point at an angle
    pos is [x, y, thr]
    1 px is 1 cm
    '''
    c = math.cos(pos[2])
    s = -math.sin(pos[2]) # negative to account for y increasing downwards

    DRES = min(.005, max(abs(c)/inMap.scale, abs(s)/inMap.scale))

    d = 0.0
    #print len(inMap)    
    counter = 0
    while True:
        x = pos[0] + d*c
        y = pos[1] + d*s
        if y*inMap.scale >= len(inMap.mapArray[0]) or x*inMap.scale >= len(inMap.mapArray):
            return d
        #0 is black (wall)
        if inMap.mapArray[int(x*inMap.scale)][int(y*inMap.scale)] <= 65500/2+5:
            return d
        if d >= Map.inchesToMeters(MAXDISTANCE):
            return d
        d += DRES
        counter += 1
        #print d
        
    

        
def toMillimeters(inches):
  '''
  Converts an inch measurement to millimeters.
  '''
  return 25.4 * inches
    
def convertPixToD(x, y, reCalibrate=False):
    '''
    Takes a point on an image and returns a distance
    Must be pixel location from a calibrated image
    Location must be on the floor
    Pixel location must be below the horizon
    returns the distance
    '''
    if(reCalibrate):
        calibrateCamera()

    # Get best fit data from the file
    f = open(CALIBOUTFILE)
    # the third line has stuff we want
    f.readline()
    f.readline()
    lineThreeSplit = f.readline().split()
    m = float(lineThreeSplit[1])
    b = float(lineThreeSplit[2])
    maxx = float(lineThreeSplit[3])
    maxy = float(lineThreeSplit[4])
    horizon = float(lineThreeSplit[5])

    if(y <= horizon):
        return -1
    
    # Now for some MATH! YAY!
    # Dstraight is the straight distance to the given y
    # print m, y, horizon, b
    Dstraight = m/(float(y)-horizon)+b
    # d is the distance to the point
    d = Dstraight/math.cos(angleFromStraight(x, y, maxx, maxy))
    if d > MAXDISTANCE:
        return MAXDISTANCE
    return d


def calibrateCamera():
    '''
    Reads a calibration file and calibrates the program to be able to convert
    pixels into distances.
    '''
    # read in from the calibration file
    reading = readCalibFile()
    calibArray = reading[0]
    maxx = reading[1]
    maxy = reading[2]
    horizon = reading[3]

    # so if a point is straight ahead, the equation
    #      D = c/(y-y0) - k
    # gives the distance as a function of difference between the y
    # location and the horizon line.  let dy = y-y0 for now.
    # since we know the angle from straight ahead, we can manipulate the data
    # to give more useful calibration info (aka [straight distance, y-value]

    # the straight distance can be found with some trig...

    # simple array of the form [ [Distance, y],[Dist...,...]... ]
    straightArray = []

    # linFitArray is ready for a linear fit so of the form [ [1/(y-y0), D]...]
    linFitArray = []

    
    i = 0
    Dvals = []
    yvals = []
    while i < len(calibArray):
        d0 = calibArray[i][0]
        x = calibArray[i][1]
        y = calibArray[i][2]
        # some trig to get the straight distance
        D = d0*math.cos(angleFromStraight(x, y, maxx, maxy))
        straightArray.append([])
        linFitArray.append([])
        Dvals.append(D)
        yvals.append(y)
        straightArray[i] = [D, y]
        linFitArray[i] = [ 1.0/(y-horizon), D]
        i += 1
    #print straightArray
    #print "Distances: ", Dvals, "\n"
    #print "Y vals: ", yvals, "\n"

    fit = bestLinearFit(linFitArray)
    fittext = "Best fit: D(x) = " + str(fit[0]) + \
              "/(x - " + str(horizon) + ") + " + str(fit[1])
    print "Distance as a function of the height y:"
    print fittext
    
    # save the calibration to a file
    outfile = open(CALIBOUTFILE, 'w')
    outfile.write("# " + str(fittext) + "\r\n")
    outfile.write("# m\tb\tmaxx\tmaxy\thorizon\r\n")
    outfile.write("# " + str(fit[0]) + "\t" + str(fit[1]) + "\t"\
                  + "\t" + str(maxx) + "\t" + str(maxy) + "\t" +\
                  str(horizon) + "\r\n")
    outfile.write("######Straightened Data#######\r\n")
    outfile.write("# y\tD\r\n")
    for point in straightArray:
        outfile.write(str(point[1]) + "\t" + str(point[0]) + "\r\n")
    outfile.close()
    
    


def angleFromStraight(x, y, maxx, maxy, alwaysPos = True):
    '''
    Calculates the absolute value of the angle from straight ahead
    the point (x, y) is in the picture using the maxx and maxy vars
    returns an angle in radians
    '''
    
    # there is an additional amount of pixels that we must take the angle
    # from, so this code calculates the aditional pixels first
    aX = maxx/2
    aTheta = (CAMERASPAN/2)*math.pi/180
    aY = aX/math.tan(aTheta)

    middlex = maxx/2
    if alwaysPos:
        sx = math.fabs(x - middlex)
    else:
        sx = middlex - x
    sy = maxy - y
    theta = math.atan( sx / (sy + aY) )
    
    return theta

def angleFromStraightForDrawing(x, y, maxx, maxy):
    '''
    Calculates the absolute value of the angle from straight ahead
    the point (x, y) is in the picture using the maxx and maxy vars
    returns an angle in radians
    there is no sy in this one, thats the difference
    also, theres no alwaysPos
    '''
    
    # there is an additional amount of pixels that we must take the angle
    # from, so this code calculates the aditional pixels first
    aX = maxx/2
    aTheta = (CAMERASPAN/2)*math.pi/180
    aY = aX/math.tan(aTheta)

    middlex = maxx/2
    sx = middlex - x
    theta = math.atan( sx / aY )
    return theta

def bestLinearFit(data):
    '''
    data is a list of length 2 lists, each pair is an x, y coordinate.
    output is a length 2 list with m=slope and b=intercept [m,b]
    '''
    #an algorithm to find the least squares regression slope
    i = 0
    # first find the average dist and average reading
    sum_x = 0.0
    sum_y = 0.0
    while i < len(data):
      sum_x += float(data[i][0])
      sum_y += float(data[i][1])
      i += 1
    avg_x = float(sum_x / float(len(data)))
    avg_y = float(sum_y / float(len(data)))
    # m = sum( (xi - xbar)(yi - ybar) ) / sum( (xi - xbar)^2 )
    i = 0
    top_sum = 0.0
    bottom_sum = 0.0
    while i < len(data):
      top_sum += (data[i][0] - avg_x)*(data[i][1] - avg_y)
      bottom_sum += (data[i][0] - avg_x)*(data[i][0] - avg_x)
      i += 1
    #print top_sum
    #print bottom_sum
    #print data
    m = top_sum / bottom_sum
    # b = avg_y - m*avg_x
    b = avg_y - m*avg_x
    return [m, b]

def readCalibFile():
    '''
    Reads the calibration file into an array (DIST, X, Y)
    returns an array containing [the array, maxx, maxy, horizon]
    '''
    f = open(CALIBFILE)
    firstline = f.readline().split()
    #print firstline
    maxx = float(firstline[0])
    maxy = float(firstline[1])
    horizon = float(firstline[2])
    #print maxx, maxy
    calibArray = []
    lineNum = 0
    for line in f:
        calibArray.append([])
        splitLine = line.split()
        calibArray[lineNum] = [float(splitLine[0]),
                               float(splitLine[1]),
                               float(splitLine[2])]
        lineNum += 1
    return [calibArray, maxx, maxy, horizon]
