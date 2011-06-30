import CoreSLAM
import socket
import string
import re
import math

TCP_IP = '127.0.0.1'
TCP_PORT = 2002
BUFFER_SIZE = 4096
COLOR = ['Red', 'Yellow', 'Green', 'Cyan', 'White', 'Blue', 'Purple']
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send("INIT {ClassName USARBot.P2DX} {Location 2.5,1.9,1.8} {Name R1}\r\n")
##s.send("INIT {ClassName USARBot.P2DX} {Location -6.0,3.5,1.8} {Name R1}\r\n")
print("robot gemaakt")
x = []
y = []
theta = []
posX=0
posY=1
theta=2 # in degrees
posTheta=2 # in degrees (since some places accidently use posTheta instead of theta)

TS_SCAN_SIZE=181 #8192
TS_MAP_SIZE=1000 #2048   # number of pixels
TS_MAP_SCALE=50 #0.1     # scales the pixels appropriately

TS_DISTANCE_NO_DETECTION=5 #4000
TS_NO_OBSTACLE=65500
TS_OBSTACLE=0
TS_HOLE_WIDTH=600

#Check camToDistance.py for updated camera angle in degrees
CAMERASPAN = 180.0


def string_to_float(sonar_vals):
    float_sonar_vals = []
    for i in range(len(sonar_vals)):
        float_sonar_vals.append(float(sonar_vals[i]))
    return float_sonar_vals     

def min_sonar_val(sonar_vals):
    sonar_vals = string_to_float(sonar_vals)
    sorted_sonar_vals = sorted(sonar_vals)
    index_val = sonar_vals.index(sorted_sonar_vals[0]) + 1
    #print sorted_sonar_vals[0]
    #print index_val
    return sorted_sonar_vals[0], index_val

def min_laser_val(laser_vals):
    laser_vals = string_to_float(laser_vals)
    sorted_laser_vals = sorted(laser_vals)
    index_val = laser_vals.index(sorted_laser_vals[0]) + 1 
    return sorted_laser_vals[0], index_val


        
Map = CoreSLAM.ts_map_init()
scans = []
pos = []
sonar_values = []
draw = 0
data_incomplete = 0
SCALE = 2
while 1:
    s.send("DRIVE {LEFT -1.0} {RIGHT 1.0}\r\n")
    data = s.recv(BUFFER_SIZE)
##    print data
    if data_incomplete:
        datatemp += data
        data_incomplete = 0
        data = datatemp
    if data[len(data)-1] != '\n':
        datatemp = data
        data_incomplete = 1
        continue
    string = data.split('\r\n')
##    print string
    for i in range(len(string)):
        datasplit = re.findall('\{[^\}]*\}|\S+', string[i])
        if len(datasplit) > 0:
            # Sensor message
            if datasplit[0] == "SEN":
                typeSEN = datasplit[1].replace('{Type ', '')
                typeSEN = typeSEN.replace('}', '')
                if len(datasplit) > 2:
                    typeSEN2 = datasplit[2].replace('{Type ', '')
                    typeSEN2 = typeSEN2.replace('}', '')
                if typeSEN2 == "RangeScanner":
                    #datasplit[6] bevat data
                    if len(datasplit) >= 6:
                        laser_values = re.findall('([\d.]*\d+)', datasplit[6])
                        min_vals, index_val = min_laser_val(laser_values)
                        print laser_values
                        if min <= 0.2 :
                            if index_val < len(laser_values)/2:
                                s.send("DRIVE {LEFT -1.0} {RIGHT 1.0}\r\n")
                            else:
                                s.send("DRIVE {LEFT 1.0} {RIGHT -1.0}\r\n")
                        scans = [float(y)/SCALE for y in laser_values]
                        print scans
                if typeSEN == "Odometry":
                    #geen ide
                    senvalues = datasplit[3].replace('{Pose ', '')
                    senvalues = senvalues.replace('}','')
                    odo_values = senvalues.split(',')
    ##                    print odo_values
                    pos = [float(x) for x in odo_values]
                    print pos
                    pos[posY]=pos[posY]/SCALE
                    pos[posX]=pos[posX]/SCALE
                    pos[theta]=math.degrees(pos[theta])

                    pos[posY]=pos[posY]+(TS_MAP_SIZE/(2.0*TS_MAP_SCALE))
                    pos[posX]=pos[posX]+(TS_MAP_SIZE/(2.0*TS_MAP_SCALE))
                    print pos
                



##    print scans
##    print pos
##    print len(scans)
##    print len(pos)
    if len(scans)!=0 and len(pos)!=0:
        print scans
        print pos
        print "ik ga nu map maken"        
        CoreSLAM.makeMap(scans, pos, len(scans), Map)
        draw += 1
        if draw == 50:
            print " ik ga tekenen"
            CoreSLAM.drawMap(Map)
            draw = 0
        
        scans = []
        pos = []
        
##    if(odometry==''):
##        print 'Finished Parsing'
##        print 'Starting drawMap...'
##        drawMap(Map)
##        #cropToMap(Map)
##        return
##    odometry=odometry.strip()
##    pos=odometry.split()
##    pos=pos[1:4]
##    pos=[float(x) for x in pos]
##
##    #Temporary convert from meters to centimeters and radians to degrees
##    #Future output logs will have this fixed
##    pos[posY]=pos[posY]/3
##    pos[posX]=pos[posX]/3
##    pos[theta]=math.degrees(pos[theta])
##
##    
##    pos[posY]=pos[posY]+(TS_MAP_SIZE/(2.0*TS_MAP_SCALE))
##    pos[posX]=pos[posX]+(TS_MAP_SIZE/(2.0*TS_MAP_SCALE))        
##    
##    laser=data.readline()
##    laser=laser.strip()
##    scans=laser.split()
##    NUMLASERS=int(scans[1])
##    scans=scans[2:]
##    scans=[float(y)/3 for y in scans]
##    #print NUMLASERS, pos
##
##    makeMap(scans, pos, NUMLASERS, Map)

