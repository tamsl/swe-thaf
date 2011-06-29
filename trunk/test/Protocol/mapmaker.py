import CoreSLAM
import socket
import string
import re
import math
from communicatorv2 import *
##
##TCP_IP = '127.0.0.1'
##TCP_PORT = 2001
##BUFFER_SIZE = 4096
##COLOR = ['Red', 'Yellow', 'Green', 'Cyan', 'White', 'Blue', 'Purple']
##s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
##s.connect((TCP_IP, TCP_PORT))
##s.send("INIT {ClassName USARBot.P2DX} {Location 2.5,1.9,1.8} {Name R1}\r\n")
####s.send("INIT {ClassName USARBot.P2DX} {Location -6.0,3.5,1.8} {Name R1}\r\n")
##print("robot gemaakt")

list = []
running = 1
configreader = config_reader()
accept_thread = acceptor(running, list, "MAP", configreader.addresses)
accept_thread.setDaemon(True)
accept_thread.start()
odometry = connection(running, "ODO", configreader, list)
odometry.setDaemon(True)
odometry.start()
rangescanner = connection(running, "RSC", configreader, list)
rangescanner.setDaemon(True)
rangescanner.start()

print "connected"
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

odo = 1
ran = 2

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


        
Map= CoreSLAM.ts_map_init()

scans = []
pos = []
sonar_values = []
draw = 0
data_incomplete = 0
SCALE = 2
odometryvalues = []
rangescannervalues = []

while 1:
    print "ik ga data opvragen"
    rangescanner.send_data("REQ!MAP#")
    odometry.send_data("REQ!MAP#")
    accept_thread.set_wait(2)
    #wait for data to arrive
    while accept_thread.get_wait() > 0 :
        continue
    print "klaar met data ophalen"
    if len(rangescannervalues) > 0:
        if rangescannervalues[0] == accept_thread.memory[ran].split("+")[0]:
            continue
    if len(odometryvalues) > 0:
        if odometryvalues[0] == accept_thread.memory[odo].split("+")[0]:
            continue
    rangescannervalues = accept_thread.memory[ran].split("+")
    laser_values = rangescannervalues[1].split(',')
    odometryvalues = accept_thread.memory[odo].split('+')
    odo_values = odometryvalues[1].split(',')
    min_vals, index_val = min_laser_val(laser_values)
    scans = [float(y)/SCALE for y in laser_values]
    pos = [float(x) for x in odo_values]
    pos[posY]=pos[posY]/SCALE
    pos[posX]=pos[posX]/SCALE
    pos[theta]=math.degrees(pos[theta])
    pos[posY]=pos[posY]+(TS_MAP_SIZE/(2.0*TS_MAP_SCALE))
    pos[posX]=pos[posX]+(TS_MAP_SIZE/(2.0*TS_MAP_SCALE))
##    print pos,scans
    CoreSLAM.makeMap(scans, pos, len(scans), Map)
    draw += 1
    if draw == 10:
        print " ik ga tekenen"
        CoreSLAM.drawMap(Map)
        print " ik ben klaar met tekenen"
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

