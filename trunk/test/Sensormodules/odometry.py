#!/usr/bin/env python

import socket
import re

TCP_IP = '127.0.0.1'
TCP_PORT = 2001
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send('INIT {ClassName USARBot.P2DX} {Location 4.5,1.9,1.8} {Name R1}\r\n')

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

# Test the odometry module.
for i in range(100):
    s.send("DRIVE {Left 1.0}\r\n")
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
          
s.close()


