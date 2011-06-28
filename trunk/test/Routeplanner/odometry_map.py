#!/usr/bin/env python

import socket
import re
import math

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
s.send('INIT {ClassName USARBot.P2DX} {Location 4.5,1.9,1.8} {Name R1}\r\n')

xs = 500
ys = 500
xf = 510
yf = 530
alpha = 0
beta = 0

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

dx = xf - xs
dy = yf - ys
alpha = math.atan(dy / dx)
new_value = []

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
                    dx = xf - new_value[0]
                    dy = yf - new_value[1]
                    beta = math.atan(dy / dx)

    print math.degrees(alpha + beta)
                    
          
s.close()
