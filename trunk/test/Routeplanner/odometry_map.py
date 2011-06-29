#!/usr/bin/env python

import socket
import re
import math
from movementsv2 import *

TCP_IP = '127.0.0.1'
TCP_PORT = 2002
BUFFER_SIZE = 1024
posX = 0
posY = 1
theta = 2
TS_MAP_SIZE=1000 #2048   # number of pixels
TS_MAP_SCALE=50 #0.1     # scales the pixels appropriately

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send('INIT {ClassName USARBot.P2DX} {Location 4.5,3.8,1.8} {Rotation 0.0,0.0,0.0} {Name R1}\r\n')

xs = 500
ys = 500
xf = 505
yf = 505
alpha = 0
beta = 0
alphabeta = 0

# Method to retrieve the list of odometry values.
def odometry_module(datastring):
    print datastring, "\r\n"
    senvalues = datastring[3].replace('{Pose ', '')
    senvalues = senvalues.replace('}','')
    odo_values = senvalues.split(',')
    
    # Test for validity
    test = []
    for i in range(len(odo_values)):
        test.append(re.findall('([\d.]*\d+)', odo_values[i]))
    if len(test) == 3:
        print "BINGO"
    else:
        print "FAIL"    
    print odo_values, "\r\n"
    return odo_values

def adjust(xs, ys, alpha):
    dx = xf - xs
    if dx == 0 and  alpha > 0:
        return  90,alpha + 90
    elif dx == 0 and alpha < 0:
        return  -90,alpha + -90
    dy = yf - ys
    if dx == 0  and dy == 0:
        print "IK BEN ERRR"        
    print "dx ", dx,"dy ", dy
    #beta = math.atan(dy / dx)
    beta = math.atan2(dy, dx)
    return beta, alpha + beta

dx = xs - xf
dy = ys - yf
alpha = math.atan(dy / dx)
s.send(handle_movement("right", 2.0, 1.0))
# Test the odometry module.
while 1:
    data = s.recv(BUFFER_SIZE)
    string = data.split('\r\n')
    for i in range(len(string)):
        datasplit = re.findall('\{[^\}]*\}|\S+', string[i])
        if len(datasplit) > 0:
            # Sensor message.
            if datasplit[0] == "SEN":
                typeSEN = datasplit[1].replace('{Type ', '')
                typeSEN = typeSEN.replace('}', '')
                # Odometry sensor.
                if typeSEN == "Odometry":
                    odo_values = odometry_module(datasplit)

                    pos = [float(x) for x in odo_values]
                    pos[posY]=pos[posY]/2
                    pos[posX]=pos[posX]/2
                    pos[theta]=math.degrees(pos[theta])

                    pos[posY] = pos[posY]+(TS_MAP_SIZE/(2.0*TS_MAP_SCALE))
                    pos[posX] = pos[posX]+(TS_MAP_SIZE/(2.0*TS_MAP_SCALE))
                    pos[posX] = int(pos[posX]*TS_MAP_SCALE+0.5)
                    pos[posY] = int(pos[posY]*TS_MAP_SCALE+0.5)
                    print "Pos", pos
                    new_value = pos
                    beta, alphabeta = adjust(new_value[0], new_value[1], alpha)
                    if pos[2]+alphabeta < 0:
                        s.send(handle_movement("right", 2.0, 1.0))
                    else:
                        s.send(handle_movement("left", 2.0, 1.0))
                        

    print math.degrees(alphabeta)
                    
          
s.close()
