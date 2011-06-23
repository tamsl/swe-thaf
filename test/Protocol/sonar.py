#!/usr/bin/env python
# This module is one of the reflex modules. This one checks the sonar values.

from communicatorv2 import *
import socket
import re

# Standard way to connect to your local server.
##TCP_IP = '127.0.0.1'
##TCP_PORT = 2001
##BUFFER_SIZE = 1024

current_values = ""
list = []
running = 1
configreader = config_reader()
accept_thread = acceptor(running, list, "SNR", configreader.addresses)
accept_thread.setDaemon(True)
accept_thread.start()
print("ik heb de acceptor thread gestart")
##s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
##s.connect((TCP_IP, TCP_PORT))
##s.send('INIT {ClassName USARBot.P2DX} {Location 4.5,1.9,1.8} {Name R1}\r\n')

# Method to retrieve the list of sonar values
def sonar_module(datastring):
##    print datastring, "\r\n"
    datasplit = re.findall('\{[^\}]*\}|\S+', datastring)
    sonar_values = []
    values = ""
    for i in range(len(datasplit)):
        sonar_values.append(datasplit[i].replace('{Name F' + str(i+1)
                                            + ' Range ', ''))
        sonar_values[i] = sonar_values[i].replace('}', '')
        if float(sonar_values[i]) < 0:
            return
        values += sonar_values[i] + ','
    values = values.rstrip(',')
    current_values = values

while 1:
    sonar_module(accept_thread.memory[0])
##    print list
##    print 'current_values', current_values
    while len(accept_thread.request_data) != 0:
        message = "RCV!SNR!" + str(current_values) + "#"
        config_reader.connection(list,
                                 accept_thread.request_data[0]).send(
                                     message)
        accept_thread.request_data.pop(0)
            
### Test the sensor module.
##for i in range(100):
##    s.send("DRIVE {Left 1.0}\r\n")
##    data = s.recv(BUFFER_SIZE)
##    string = data.split('\r\n')
##    for i in range(len(string)):
##        datasplit = re.findall('\{[^\}]*\}|\S+', string[i])
##        if len(datasplit) > 0:
##            # Sensor message
##            if datasplit[0] == "SEN":
##                if len(datasplit) > 2:
##                    typeSEN2 = datasplit[2].replace('{Type ', '')
##                    typeSEN2 = typeSEN2.replace('}', '')
##		    # Sonar sensor
##                    if typeSEN2 == "Sonar":
##		        sonar_values = sensor_module(datasplit)    

s.close()


