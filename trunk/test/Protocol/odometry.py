#!/usr/bin/env python

from communicatorv2 import *
import socket
import re

##TCP_IP = '127.0.0.1'
##TCP_PORT = 2001
##BUFFER_SIZE = 1024
##
##s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
##s.connect((TCP_IP, TCP_PORT))
##s.send('INIT {ClassName USARBot.P2DX} {Location 4.5,1.9,1.8} {Name R1}\r\n')
current_values = ""
list = []
running = 1
configreader = config_reader()
accept_thread = acceptor(running, list, "ODO", configreader.addresses)
accept_thread.setDaemon(True)
accept_thread.start()
print("ik heb de acceptor thread gestart")

# Method to retrieve the list of odometry values.
def odometry_module(datastring):
    odo_values = ""
    odo_values = datastring.replace('{Pose ', '')
    odo_values = odo_values.replace('}', '')
    values = odo_values.split(',')
##    print len(values)
    if len(values) > 2:
        if (float(values[2]) > 3.15) or (float(values[2]) < -3.15):
            return
    current_values = datastring

while 1:
    odometry_module(accept_thread.memory[1])
##    print list
##    print 'current_values', current_values
    while len(accept_thread.request_data) != 0:
        config_reader.connection(list,
                                 accept_thread.request_data[0]).send(
                                     current_values)
        accept_thread.request_data.pop(0)

### Test the odometry module.
##for i in range(100):
##    s.send("DRIVE {Left 1.0}\r\n")
##    data = s.recv(BUFFER_SIZE)
##    string = data.split('\r\n')
##    for i in range(len(string)):
##        datasplit = re.findall('\{[^\}]*\}|\S+', string[i])
##        if len(datasplit) > 0:
##            # Sensor message.
##            if datasplit[0] == "SEN":
##                typeSEN = datasplit[1].replace('{Type ', '')
##                typeSEN = typeSEN.replace('}', '')
##                # Odometry sensor.
##                if typeSEN == "Odometry":
##                    odo_values = odometry_module(datasplit)
          
s.close()


