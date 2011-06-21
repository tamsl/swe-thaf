# CoreSLAM.py
# This file takes in scan data in log file and uses CoreSLAM to generate map
# Author: Kenny Lei
# This file is part of the HMC PixelLaser research project.
# Advisor: Zach Dodds

import math
##from bmp import *
##import camToDistance
import operator
import random
##from PIL import Image

TS_SCAN_SIZE=181 #8192
TS_MAP_SIZE=1000 #2048   # number of pixels
TS_MAP_SCALE=50 #0.1     # scales the pixels appropriately

TS_DISTANCE_NO_DETECTION=5 #4000
TS_NO_OBSTACLE=65500
TS_OBSTACLE=0
TS_HOLE_WIDTH=600

MAP_OUTPUT_NAME="Map.bmp"
LOG_INPUT_NAME="volledig.txt"

#Check camToDistance.py for updated camera angle in degrees
CAMERASPAN = 180.0

scanX = 0
scanY = 1
scanValue = 2

scanR=0
scanTheta=1

posX=0
posY=1
theta=2 # in degrees
posTheta=2 # in degrees (since some places accidently use posTheta instead of theta)

def ImageToMapArray():
    im = Image.open("halls.jpg")
    Map = list(im.getdata())
    print Map
    
def ts_map_init():
    initval=(TS_OBSTACLE+TS_NO_OBSTACLE)/2
    Map = [initval]*(TS_MAP_SIZE * TS_MAP_SIZE)
    return Map
    
def ts_distance_scan_to_map(scan, Map, pos):
    nb_points=0
    #value=2, nb_points=3
    c=math.cos(math.radians(pos[theta]))
    s=math.sin(math.radians(pos[theta]))
    dist=0.0
    #Translate and rotate scan to robot position
    #and compute the distance

    scan_len = len(scan[scanX])
    #print "scan_len is", scan_len
    
    for i in range(0,scan_len):
        if(scan[scanValue][i] != TS_NO_OBSTACLE):
            x=(int)((pos[posX]+c*scan[scanX][i]-s*scan[scanY][i])*TS_MAP_SCALE+0.5)
            y=(int)((pos[posX]+s*scan[scanX][i]+c*scan[scanY][i])*TS_MAP_SCALE+0.5)
            # if in bounds
            #print "x,y are", x, y
            if(x>=0 and x<TS_MAP_SIZE and y>=0 and y<TS_MAP_SIZE):
                dist+=Map[y*TS_MAP_SIZE+x]
                nb_points+=1
    # if there are any points, then give the per-point value
    if nb_points>0:
        dist/=nb_points
    else:
        dist=2000000000
    return (int)(dist)

def ts_map_update(scan, Map, pos, quality, hole_width):
    c=math.cos(math.radians(pos[theta]))
    s=math.sin(math.radians(pos[theta]))
    x1=(int)(pos[posX]*TS_MAP_SCALE+0.5)
    y1=(int)(pos[posY]*TS_MAP_SCALE+0.5)
    #Translate and rotate scan to robot position
    scan_len = len(scan[scanX])
    for i in range(0,scan_len):
        x2p=c*scan[scanX][i]-s*scan[scanY][i]
        y2p=s*scan[scanX][i]+c*scan[scanY][i]
        xp=(int)(math.floor((pos[posX]+x2p)*TS_MAP_SCALE+0.5))
        yp=(int)(math.floor((pos[posY]+y2p)*TS_MAP_SCALE+0.5))
        dist=math.sqrt(x2p*x2p+y2p*y2p)
##        print 'dist is', dist,
        add=hole_width/2.0/dist
        x2p*=TS_MAP_SCALE*(1+add)
        y2p*=TS_MAP_SCALE*(1+add)
        x2=(int)(pos[posX]*TS_MAP_SCALE+x2p+0.5)
        y2=(int)(pos[posY]*TS_MAP_SCALE+y2p+0.5)
        if(scan[scanValue][i]==TS_NO_OBSTACLE):
            q=quality/4
            value=TS_OBSTACLE
        else:
            q=quality
            value=TS_OBSTACLE



##        print "x1,y1", x1, y1,
##        print "xp,yp", xp, yp,
##        print "x2,y2", x2, y2,
##        print

        
        Map=ts_map_laser_ray(Map, x1, y1, x2, y2, xp, yp, value, q)
    return Map


        
def ts_map_laser_ray(Map, x1, y1, x2, y2, xp, yp, value, alpha):
    """ adds one laser ray to the map! """
    
    if(x1<0 or x1>=TS_MAP_SIZE or y1<0 or y1>=TS_MAP_SIZE):
        return #Robot is out of the Map

    # Clipping for portions out of bounds
    x2c = x2
    y2c = y2
    if(x2c<0):
        if(x2c==x1): return
        y2c+=(y2c-y1)*(-x2c)/(x2c-x1)
        x2c=0
    if(x2c>=TS_MAP_SIZE):
        if(x1==x2c): return
        y2c+=(y2c-y1)*(TS_MAP_SIZE-1-x2c)/(x2c-x1)
        x2c=TS_MAP_SIZE - 1
    if(y2c<0):
        if(y1==y2c): return
        x2c+=(x1-x2c)*(-y2c)/(y1-y2c)
        y2c=0
    if(y2c>=TS_MAP_SIZE):
        if(y1==y2c): return
        x2c+=(x1-x2c)*(TS_MAP_SIZE-1-y2c)/(y1-y2c)
        y2c=TS_MAP_SIZE-1

    # Bresenham algorithm
    dx=abs(x2-x1);     dy=abs(y2-y1)
    dxc=abs(x2c-x1);   dyc=abs(y2c-y1)
    
    if(x2>x1):
        incptrx = 1
    else:
        incptrx = -1
        
    if(y2>y1):
        incptry = TS_MAP_SIZE
    else:
        incptry = -TS_MAP_SIZE
        
    if(value>TS_NO_OBSTACLE): 
        sincv = 1  # if there is an obstacle
    else:
        sincv = -1 # if there is NO obstacle

    derrorv = 0.0  # placeholder for the following:
    
    if(dx>dy):
        # traverse by steps of x
        derrorv = abs(xp-x2)
    else:
        # swap x and y values so that we
        # traverse by steps of x
        dx, dy = dy, dx
        dxc, dyc = dyc, dxc
        incptrx, incptry = incptry, incptrx
        derrorv=abs(yp-y2)

    # now, we are traversing in steps of x
    error=2*dyc-dxc
    horiz=2*dyc
    diago=2*(dyc-dxc)
    errorv=derrorv/2
    # if value == TS_NO_OBSTACLE, then incv = 0
    # if value == TS_OBSTACLE, then incv = -65500/derrorv
    incv=(value-TS_NO_OBSTACLE)/derrorv
    # if value == TS_NO_OBSTACLE, then incerrorv = 0
    # if value == TS_OBSTACLE, then incerrorv = 65500
    incerrorv=value-TS_NO_OBSTACLE-derrorv*incv

    # location of the origin in the Map
    ptr = y1*TS_MAP_SIZE+x1
    pixval=TS_NO_OBSTACLE
    
    x=0
    while(x<=dxc):
        if(x>dx-2*derrorv):
            if (x <= dx - derrorv):
                pixval += incv
                errorv += incerrorv
                if (errorv > derrorv):
                    pixval+=sincv
                    errorv-=incerrorv
            else:
                pixval -= incv
                errorv -= incerrorv
                if(errorv<0):
                    pixval-=sincv
                    errorv+=derrorv
                    
        #Integration into the map
        Map[ptr] = ((256-alpha)*Map[ptr] + alpha*pixval)/256
        if(error>0):
            ptr += incptry
            error += diago
        else:
            error += horiz           
        x+=1
        ptr+=incptrx
        
    return Map

def drawMap(Map, mapName = MAP_OUTPUT_NAME):
    cell_side = 1
##    image=BitMap(TS_MAP_SIZE*cell_side, TS_MAP_SIZE*cell_side)
##    im = Image.new('RGB', [TS_MAP_SIZE*cell_side, TS_MAP_SIZE*cell_side])
##    pix = im.load()
    fn = open("ronddraaien.ppm","w")
    fn.write("P3")
    fn.write("\n")
    fn.write(str(TS_MAP_SIZE)+"\t"+str(TS_MAP_SIZE))
    fn.write("\n")
    fn.write("255\n")
    for row in range((TS_MAP_SIZE*cell_side)):
        rowFlip=TS_MAP_SIZE*cell_side-row-1 #row
        for col in range((TS_MAP_SIZE*cell_side)):
            pixVal=Map[rowFlip/cell_side*TS_MAP_SIZE+col/cell_side]
            pixVal=int(pixVal*255.0/TS_NO_OBSTACLE)
            #pixColor=Color(pixVal,pixVal,pixVal)
            fn.write(str(pixVal)+"\t")
            fn.write(str(pixVal)+"\t")
            fn.write(str(pixVal)+"\t")
##            pix[col, row] = (pixVal, pixVal, pixVal)
            #image.setPenColor(pixColor)
            #image.plotPoint(col, row)
    #image.saveFile(mapName)
    fn.flush()
    fn.close()
##    im.save(mapName)
##    print 'Map File Saved as', mapName

def drawCroppedMap(Map, mapRowLength, mapColLength):
    cell_side = 1
    image=BitMap(mapRowLength*cell_side, mapColLength*cell_side)
    for row in range((mapColLength*cell_side)):
        rowFlip=row #TS_MAP_SIZE*cell_side-row-1
        for col in range((mapRowLength*cell_side)):
            pixVal=Map[rowFlip/cell_side*TS_MAP_SIZE+col/cell_side]
            pixVal=pixVal*255.0/TS_NO_OBSTACLE
            pixColor=Color(pixVal,pixVal,pixVal)
            image.setPenColor(pixColor)
            image.plotPoint(col, row)
    image.saveFile(MAP_OUTPUT_NAME)
    print 'Map File Saved as', MAP_OUTPUT_NAME

def rescaleMap(Map, newScale):
    '''
    Rescale Map with new scale.  Map size remains the same.
    '''
    initval=(TS_OBSTACLE+TS_NO_OBSTACLE)/2
    newMap = [initval]*(TS_MAP_SIZE * TS_MAP_SIZE)

    newScale = int(newScale)
    global TS_MAP_SCALE
    
    scaleDifference = float(newScale)/float(TS_MAP_SCALE)
    for row in range(TS_MAP_SIZE):
        for col in range(TS_MAP_SIZE):
            newMap[int(row*scaleDifference)*TS_MAP_SIZE+
                   int(col*scaleDifference)-
                   int((TS_MAP_SCALE-newScale)/2)*TS_MAP_SIZE-
                   int((TS_MAP_SCALE-newScale)/2)]\
                   = Map[row*TS_MAP_SIZE+col]

    TS_MAP_SCALE = newScale
    return newMap

def mapParser(filename):
    """
    handle the log files..
    """
    
    data=open(filename, 'r')
    Map=ts_map_init()
    print 'Start Parsing...'
    while True:
        odometry=data.readline()
        if(odometry==''):
            print 'Finished Parsing'
            print 'Starting drawMap...'
            drawMap(Map)
            #cropToMap(Map)
            return
        odometry=odometry.strip()
        pos=odometry.split()
        pos=pos[1:4]
        pos=[float(x) for x in pos]

        #Temporary convert from meters to centimeters and radians to degrees
        #Future output logs will have this fixed
        pos[posY]=pos[posY]/3
        pos[posX]=pos[posX]/3
        pos[theta]=math.degrees(pos[theta])

        
        pos[posY]=pos[posY]+(TS_MAP_SIZE/(2.0*TS_MAP_SCALE))
        pos[posX]=pos[posX]+(TS_MAP_SIZE/(2.0*TS_MAP_SCALE))        
        
        laser=data.readline()
        laser=laser.strip()
        scans=laser.split()
        NUMLASERS=int(scans[1])
        scans=scans[2:]
        scans=[float(y)/3 for y in scans]
        #print NUMLASERS, pos

        makeMap(scans, pos, NUMLASERS, Map)

def cropToMap(Map):
    '''
    Crops out portions of map that is left blank and focuses picture to used portions of the map.
    Removes need to change and adjust TS_MAP_SIZE and center adjustment all the time
    '''
    initval = (TS_OBSTACLE+TS_NO_OBSTACLE)/2

    #Find top region of cropped map
    setTop = False
    topRow = 0
    while topRow < TS_MAP_SIZE and setTop==False:
        topCol = 0
        while topCol < TS_MAP_SIZE and setTop==False:
            if(Map[topRow*TS_MAP_SIZE+topCol])!=initval:
                mapTop = topRow
                setTop = True
            topCol += 1
        topRow += 1
    print "Found Top Crop", mapTop
    #Find bottom region of cropped map
    setBottom = False
    bottomRow = TS_MAP_SIZE-1
    while bottomRow >= 0 and setBottom==False:
        bottomCol = 0
        while bottomCol < TS_MAP_SIZE and setBottom==False:
            if(Map[bottomRow*TS_MAP_SIZE+bottomCol])!=initval:
                mapBottom = bottomRow
                setBottom = True
            bottomCol += 1
        bottomRow -= 1
    print "Found Bottom Crop", mapBottom
    #Find left region of cropped map
    setLeft = False
    leftCol = 0
    while leftCol < TS_MAP_SIZE and setLeft==False:
        leftRow = 0
        while leftRow < TS_MAP_SIZE and setLeft==False:
            if(Map[leftRow*TS_MAP_SIZE+leftCol])!=initval:
                mapLeft = leftCol
                setLeft = True
            leftRow += 1
        leftCol += 1
    print "Found Left Crop", mapLeft
    #Find right region of cropped map
    setRight = False
    while rightCol >= 0 and setRight==False:
        rightRow = 0
        while rightRow < TS_MAP_SIZE and setRight==False:
            if(Map[rightRow*TS_MAP_SIZE+rightCol])!=initval:
               mapRight = rightCol
               setRight = True
            rightRow += 1
        rightCol -= 1
    print "Found Right Crop", mapRight
    
    #Take only portions within boundaries in Map list
    mapRowLength=mapRight-mapLeft
    mapColLength=mapBottom-mapTop
    croppedMap=[0]*(mapRowLength*mapColLength)
    for i in range(0, mapColLength):
        for j in range(0, mapRowLength):
            croppedMap[i*mapRowLength+j] = Map[mapTop*TS_MAP_SIZE+mapLeft+i*mapRowLength+j]

    #Draw cropped map
    print "Drawing cropped map..."
    drawCroppedMap(croppedMap, mapRowLength, mapColLength)
        
def makeMap(scans, pos, NUMLASERS, Map):

    # set scan to correct format...
    scan=[[0]*NUMLASERS, [0]*NUMLASERS, [0]*NUMLASERS]
    angle_interval = CAMERASPAN/float(NUMLASERS-1)
    for i in range(0, NUMLASERS):
        angle_for_this_ray = CAMERASPAN/2.0 - i*angle_interval
        angle = math.radians(angle_for_this_ray)
        length = scans[i]
        scan[scanX][i] = math.cos(angle)*length
        scan[scanY][i] = math.sin(angle)*length
        scan[scanValue][i] = TS_OBSTACLE
        
    #quality = magnitude of changing Map values
    #hole_width = how spread out the detected area is (confidence of where the obstacle is)
    Map = ts_map_update(scan, Map, pos, 50, .25)
    return Map

def makeHandDrawnMap():
    MAP_SIZE=200

    # the playground
    Map = [(TS_NO_OBSTACLE+TS_OBSTACLE)/2]*(MAP_SIZE*MAP_SIZE)
    for a in range(0, 86):
        Map[a]=TS_OBSTACLE
    for b in range(0, 166):
        Map[b*MAP_SIZE]=TS_OBSTACLE
    for c in range(36, 127):
        Map[195*MAP_SIZE+c]=TS_OBSTACLE
    dist = math.sqrt(36.0*36.0+30.0*30.0)
    xInterval = 36.0/dist
    yInterval = 30.0/dist
    yInterval /= xInterval
    for d in range(0, 37):
        Map[int(d*yInterval+165)*MAP_SIZE+d]=TS_OBSTACLE
    dist = math.sqrt(110.0*110.0+131.0*131.0)
    xInterval = 110.0/dist
    yInterval = 131.0/dist
    xInterval /= yInterval
    for e in range(0, 132):
        Map[e*MAP_SIZE+int(e*xInterval)+85]=TS_OBSTACLE
    dist = math.sqrt(69.0*69.0+64.0*64.0)
    xInterval = -69.0/dist
    yInterval = 64.0/dist
    yInterval /= xInterval
    for f in range(0, 69):
        Map[(int(f*-yInterval+131))*MAP_SIZE+195-f]=TS_OBSTACLE

##    # the square
##    for a in range(0, MAP_SIZE):
##        Map[a]=TS_OBSTACLE
##        Map[a+MAP_SIZE*(MAP_SIZE-1)]=TS_OBSTACLE
##        Map[a*MAP_SIZE]=TS_OBSTACLE
##        Map[a*MAP_SIZE+MAP_SIZE-1]=TS_OBSTACLE

    for i in range(0, MAP_SIZE):
        start=-1
        end=-1
        x=0
        while(x < MAP_SIZE and start == -1):
            if Map[i*MAP_SIZE+x]==0:
                start=x
                #In case wall is two pixels long
                x+=1
            x += 1
        while(x < MAP_SIZE and end == -1):
            if Map[i*MAP_SIZE+x]==0:
                end=x
            x += 1
        if (start != -1 and end != -1):
            for j in range(start+1, end):
                #Make sure not changing walls to empty space
                if Map[i*MAP_SIZE+j] != TS_OBSTACLE:
                    Map[i*MAP_SIZE+j]=TS_NO_OBSTACLE           
    #(Map)
    return Map


def createHandDrawnMap():
    data=open(MAP_POINTS_INPUT, 'r')
    line=data.readline()
    line=line.strip()
    line=line.split()
       
def createTestPos(Map, scale):
    initialProb=0
    posList=[]
    YRES = 25
    XRES = 25
    THDRES = 30
    for y in range(0, TS_MAP_SIZE, YRES):
        for x in range(0, TS_MAP_SIZE, XRES):
            if Map[y*TS_MAP_SIZE+x]==TS_NO_OBSTACLE:
                for angle in range(0, 361, THDRES):# used to be -180 to 181
                    posList.append([x/scale, y/scale, angle, initialProb])
    return posList
##    for i in posList:
##        Map[i[posY]*TS_MAP_SIZE+i[posX]]=TS_OBSTACLE
##    drawMap(Map)

def createRandomTestPos(Map, scale, points):
    initialProb=0
    posList = []
    counter = 0
    while counter<points:
        x = random.random()*2
        y = random.random()*2
        #print x, y
        theta = random.random()*360
        if Map[int(y*scale)*TS_MAP_SIZE+int(x*scale)] == TS_NO_OBSTACLE:
            posList.append([x, y, theta, initialProb])
            counter += 1
    return posList

def localizationParser(folder):
    scale=100.0
    randomizing=False
    odometryCorrection = False
    numRandomPoints = 200
    Map=makeHandDrawnMap()
    if randomizing == True:
        posList=createRandomTestPos(Map, scale, numRandomPoints)
    else:
        posList=createTestPos(Map, scale)
    
    #posList=[[70,70,120,0]]
    posListOriginal=[[b for b in a] for a in posList]
    data=open("../Pictures/"+folder+"/"+LOG_INPUT_NAME, 'r')

    print "posList created!"

    #Call method that will precompute rays around 360 degrees at every position in posList
    #(Passing in Map and posList)
    camToDistance.buildLaserMaps(Map, scale)

    posChange =[0,0,0]
    odometry=data.readline()
    odometry=odometry.strip()
    posNew=odometry.split()
    posNew=posNew[1:4]
    posNew=[float(x) for x in posNew]
    
    #Temporary convert from meters to centimeters and radians to degrees
    #Future output logs will have this fixed
    #posNew[posY]=posNew[posY]/scale
    #posNew[posX]=posNew[posX]/scale
    #pos[theta]=math.degrees(pos[theta])

    timesCallProb=1
    while True:
        bestProb=0
        #add posChange to posList
        for z in posList:
            if z[3] != -1:
                z[posX] += posChange[posX]
                z[posY] += posChange[posY]
                z[posTheta] += posChange[posTheta]
            # CHANGE THIS LATER, GETS RID OF OoB POSs... KILLS BAD ODOMETRY DEAD, NO CORRECTION
            if z[0]<0 or z[0]>=2 or z[1]<0 or z[1]>=2:
                z[0] = -1
                z[1] = -1
                z[2] = -1
                z[3] = -1
                #print "-1 detected"
            if z[3]>bestProb:
                bestProb = z[3]

        if randomizing == True:
            for z in posList:
                if z[3] == -1 or z[0] == -1 or z[1] == -1:
                    #Rerandomizing points that were below threshold and had low probability
                    temp = createRandomTestPos(Map, scale, 1)[0]
                    z[0] = temp[0]
                    z[1] = temp[1]
                    z[2] = temp[2]
                    z[3] = temp[3]

        #Scale remaining pos probabilities between 0 and 1
##        if bestProb !=0:
##            for c in posList:
##                c[3] = c[3]/bestProb
                     
        laser=data.readline()
        laser=laser.strip()
        scans=laser.split()
        NUMLASERS=int(scans[1])
        scans=scans[2:]
        scans=[float(y) for y in scans]

        scan=[]#[[0.0, 0.0]*NUMLASERS]
        angle_interval = CAMERASPAN/float(NUMLASERS-1)
        #Take only 1/3 of NUMLASERS since probability method has accuracy to the degree anyways
        #Speed up by 3 times hopefully
        for i in range(0, NUMLASERS, int(NUMLASERS/CAMERASPAN)):
            angle_for_this_ray = -CAMERASPAN/2.0 + i*angle_interval
            angle = math.radians(angle_for_this_ray)
            length = scans[i]
##            scan[scanX][i] = math.cos(angle)*length
##            scan[scanY][i] = math.sin(angle)*length
##            scan[scanValue][i] = TS_OBSTACLE
            #scan[i][scanR]= length
            #scan[i][scanTheta]=angle_for_this_ray # in degrees
            scan.append([length, angle_for_this_ray])
            #send r and theta (angle and length variables)
            
            #Call ts_distance_to_map here for each pos in posList
        t=0
        print "Starting " + str(timesCallProb)
        for j in posList:
            #if statement to call only ones that does not have probability -1(already taken out)
            if t%100 == 0:
                print "Checking probability ", t, " of ", len(posList)
            t+=1
            if j[3] == 0:
                j[3] = camToDistance.probabilityAtPointInMap(scan, j)
            elif j[3] != -1:
                
                if odometryCorrection:
                    bestPosAndProb = monteCarloRandomization(scan, j, scale)
                    j[0] = bestPosAndProb[0][0]
                    j[1] = bestPosAndProb[0][1]
                    j[2] = bestPosAndProb[0][2]
                    if bestPosAndProb[1] != -1:
                        j[3] = (j[3] + bestPosAndProb[1])/2
                else:
                    # average the two
                    j[3] = (j[3] + camToDistance.probabilityAtPointInMap(scan, j))/2
##            if j[3] != -1 and timesCallProb > 1:
##                #reflect changes to probability, change later
##                bestPosAndProb = monteCarloRandomization(scan, j, scale)
##                j[0] = bestPosAndProb[0][0]
##                j[1] = bestPosAndProb[0][1]
##                j[2] = bestPosAndProb[0][2]
##                if bestPosAndProb[1] != -1:
##                    j[3] = ((j[3]*(timesCallProb-1) + bestPosAndProb[1])/timesCallProb)
##                #print j
##            elif j[3] != -1:
##                j[3] = (j[3]*(timesCallProb-1)+camToDistance.probabilityAtPointInMap(scan, j))/timesCallProb
        timesCallProb +=1
        
        bestListForScanOutput = posList #bestProbPerPos(posList)
        imageNumber = ""
        for i in range(0, 5-len(str(timesCallProb-1))):
            imageNumber += "0"
        imageNumber += str(timesCallProb-1)
        scanOutput = open("../Pictures/"+folder+"/"+imageNumber+".log", 'w')
        for a in bestListForScanOutput:
            scanOutput.write(str(a)+"\n")
        scanOutput.close()
        
        posOld = posNew
        
        odometry=data.readline()
        #if statement to leave loop when done looping through log file
        if(odometry==''):
            data.close()
            print 'Finished Monte-Carlo Search'
            print 'Start drawing most-likely location'
            #Create for loop to find highest probability location (lower values better)
            bestIndex=0
            bestProbability=0
            for w in range(0, len(posList)):
                if posList[w][3] != -1 and  posList[w][3] > bestProbability:
                    bestIndex = w
                    bestProbability = posList[w][3]

##            for i in range(0, len(posList)):
##                posListOriginal[i][3]=posList[i][3]
            print bestProbability
            #print posListOriginal[bestIndex]
            #bestPosList=posListOriginal[bestIndex]
            bestPosList=posList[bestIndex]
            Map[int(bestPosList[posY]*scale)*TS_MAP_SIZE+int(bestPosList[posX]*scale)]=TS_OBSTACLE
            drawMap(Map)

            # prints the highest probabilities
            print sorted(posList, key=operator.itemgetter(3), reverse=True)[:len(posList)/20]
            
            #Create map with points of likelihood
            return bestProbPerPos(posList)
        odometry=odometry.strip()
        posNew=odometry.split()
        posNew=posNew[1:4]
        posNew=[float(x) for x in posNew]
        
        #Temporary convert from meters to centimeters and radians to degrees
        #Future output logs will have this fixed
        #posNew[posY]=posNew[posY]/scale
        #posNew[posX]=posNew[posX]/scale
        #pos[theta]=math.degrees(pos[theta])

        #Update posChange for next set of odometry (all three are lists of length 3)
        for x in range(0,3):
            posChange[x] = posNew[x]-posOld[x]

        THRESHOLD = .75
        #Loop to remove some of the pos in posList that have low probability
        for y in range(0, len(posList)):
            if posList[y][3] <= THRESHOLD:
                posList[y] = [-1, -1, -1, -1]

def bestProbPerPos(posList):
    bestPosList = [posList[0]]
    for item in posList:
        itemAlreadyExists = False
        for bestItem in bestPosList:
            if bestItem[0] == item[0] and bestItem[1] == item[1]:
                itemAlreadyExists = True
                if bestItem[3] < item[3]:
                    bestItem[3] = item[3]
                    replacedAProb = True
        if not itemAlreadyExists:
            bestPosList.append(item)
    #print bestPosList
    return bestPosList


def monteCarloRandomization(scan, pos, scale):
    NEARRANGE = 20
    INCREMENT=10
    nearbyPos = []
##    #Used to take in posChange as parameter
##    distance = math.sqrt(posChange[posX]*posChange[posX] + posChange[posY]*posChange[posY])
##    unitX = posChange[posX]/distance
##    unitY = posChange[posY]/distance
    #Create list of close nearby points
    for i in range(-NEARRANGE, NEARRANGE, INCREMENT):
        for j in range(-NEARRANGE, NEARRANGE, INCREMENT):
            for k in range(-NEARRANGE, NEARRANGE, INCREMENT):
                #print [pos[posX]+i/scale, pos[posY]+j/scale, pos[posTheta]+k]
                #print i/scale, j/scale
                nearbyPos.append([pos[posX]+i/scale, pos[posY]+j/scale, pos[posTheta]+k])

    #Find best probability out of all of them
    bestProb = -1
    bestIndex = -1
    for l in range(0, len(nearbyPos)):
        if nearbyPos[l][0]>0 and nearbyPos[l][0]<TS_MAP_SIZE/scale and nearbyPos[l][1]>0 and nearbyPos[l][1]<TS_MAP_SIZE/scale:
            thisProb = camToDistance.probabilityAtPointInMap(scan, nearbyPos[l])
            if thisProb > bestProb:
                bestProb = thisProb
                bestIndex = l

    if bestIndex != -1:
        return [nearbyPos[bestIndex], bestProb]

    else:
        return [[-1,-1,-1], -1]
    
def getMCFile(folder, imageNumber):
    data = open("../Pictures/"+folder+"/"+imageNumber+".log")
    output = []
    for line in data:
        splitLine = line[1:-1].split(', ')
        outSplit = []
        for item in splitLine:
            outSplit.append(float(item.strip(']')))
        output.append(outSplit)
    return output

if False:

    mapParser(LOG_INPUT_NAME)


    if False:
        Map=ts_map_init()
        NUMLASERS = 4
        pos = [ 5.0, 5.0, 0.0 ]
        scans = [ 1.0, 2.0, 1.0, 0.5 ]
        makeMap(scans, pos, NUMLASERS, Map)
        drawMap(Map)
        
    

if False:
    Map = ts_map_init() # 8x8
    print "Map is"
    for row in range(8):
        print Map[0+row*8:8+row*8]

    
    x1, y1 = 0, 0
    x2, y2 = 0, 6
    xp, yp = 0, 4
    value = TS_OBSTACLE
    alpha = 50
    
    ts_map_laser_ray(Map, x1, y1, x2, y2, xp, yp, value, alpha)

    
    print "Map is"
    for row in range(8):
        print Map[0+row*8:8+row*8]

    drawMap(Map)

    """
    Map[2] = 0
    #Map[2*TS_MAP_SIZE+4] = 0
    scan = [0,0,0]
    scan[scanX] = [2]
    scan[scanY]=[0]
    scan[scanValue]=[TS_OBSTACLE]*1
    pos=[2,2,45]
    #pos=[0,0,0]
    d = ts_distance_scan_to_map(scan,Map,pos)
    print d

    hole_width =6
    ts_map_update(scan, Map, pos, 10.0, hole_width)
    """
