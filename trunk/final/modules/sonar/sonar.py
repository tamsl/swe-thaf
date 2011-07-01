#!/usr/bin/env python

import socket
import re

# Standard way to connect to your local server.
TCP_IP = '127.0.0.1'
TCP_PORT = 2001
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
# Start position: wall near transparent wall.
s.send('INIT {ClassName USARBot.P2DX} {Location 4.5,1.9,1.8} {Name R1}\r\n')

# Method to retrieve the list of sonar values
def sensor_module(datastring):
    if len(datasplit) > 9:
        sonar_values = []
        for i in range(0, 8):
            sonar_values.append(datasplit[i + 3].replace('{Name F' + str(i+1) + ' Range ', ''))
            sonar_values[i] = sonar_values[i].replace('}', '')
        # Test for validity.
        test = []
        for i in range(len(sonar_values)):
            test.append(re.findall('([\d.]*\d+)', sonar_values[i]))
        if len(test) == 8:
            print "Correct values."
        else:
            print "Incorrect values."

    print sonar_values, "\r\n"

# Test the sensor module.
for i in range(100):
    s.send("DRIVE {Left 1.0}\r\n")
    data = s.recv(BUFFER_SIZE)
    string = data.split('\r\n')
    for i in range(len(string)):
        datasplit = re.findall('\{[^\}]*\}|\S+', string[i])
        if len(datasplit) > 0:
            # Sensor message.
            if datasplit[0] == "SEN":
                if len(datasplit) > 2:
                    typeSEN2 = datasplit[2].replace('{Type ', '')
                    typeSEN2 = typeSEN2.replace('}', '')
		    # Sonar sensor.
                    if typeSEN2 == "Sonar":
		        sonar_values = sensor_module(datasplit)    

s.close()
