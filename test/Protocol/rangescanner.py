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
message = ""
configreader = config_reader()
accept_thread = acceptor(running, list, "RSC", configreader.addresses)
accept_thread.setDaemon(True)
accept_thread.start()
##wallsearch = configreader.connection(list, "WSC")
##wallfollow = configreader.connection(list, "WFW")
print("ik heb de acceptor thread gestart")
old_values = 20 

# Method to retrieve the list of range sensor values.
def range_module(datastring):
    if datastring == "+" or datastring == "":
        return current_values
##    print datastring
    split = datastring.split("+")
    range_values = split[1].replace('{Range ', '')
    range_values = range_values.replace('}', '')
    datasplit = range_values.split(',')
    for i in range(len(datasplit)):
        if float(datasplit[i]) < 0:
##            print 'foute data'
            return current_values
##    print 'receiving monkey data'
    range_values = split[0] + "+" + range_values
    return range_values
##    print current_values

while 1:
    data = accept_thread.memory[2]
    string = data.split('\r\n')
    for i in range(len(string)):
        datasplit = re.findall('\{[^\}]*\}|\S+', string[i])
##        if len(datasplit) != 0:
##            print datasplit
##        if len(datasplit) > 2:
##            print datasplit
        if len(datasplit) > 6:
##            typeSEN = datasplit[2].replace('{Type ', '')
##            typeSEN = typeSEN.replace('}', '')
##            print typeSEN
            if datasplit[2] == "{Type RangeScanner}":
##                print datasplit[6]
                message = datasplit[1] + "+"
                message += datasplit[6]
##                print message
    if message != "":
        current_values = range_module(message)
        if current_values != old_values:           
##            print current_values
            old_values = current_values        
    message = ""
##    print list
##    print 'current_values', current_values
##    if current_values != "":
##        command = "RCV!RSC!" + str(current_values) + "#"
##        wallfollow.send(command)
##        wallsearch.send(command)
    if current_values != "":
        while len(accept_thread.request_data) != 0:
            command = "RCV!RSC!" + current_values + "#"
            configreader.connection(list, accept_thread.request_data[0]).send(
                                        command)
            accept_thread.request_data.pop(0)

### Test the range sensor module.
##for i in range(100):
##    s.send("DRIVE {Left 1.0} {Right 1.0}")
##    data = s.recv(BUFFER_SIZE)
##    string = data.split('\r\n')
##    for i in range(len(string)):
##        datasplit = re.findall('\{[^\}]*\}|\S+', string[i])
##        if len(datasplit) > 0:
##            # Sensor message
##            if datasplit[0] == "SEN":
##                if len(datasplit) > 2:
##                    typeSEN = datasplit[2].replace('{Type ', '')
##                    typeSEN = typeSEN.replace('}', '')
##                    # Range sensor
##                    if typeSEN == "RangeScanner":
##                        laser_values = range_module(datasplit)    

s.close()
