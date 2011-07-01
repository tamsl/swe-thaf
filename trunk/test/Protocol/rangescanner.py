#!/usr/bin/env python

from communicatorv2 import *
import socket
import re

current_values = ""
list = []
running = 1
message = ""
configreader = config_reader()
accept_thread = acceptor(running, list, "RSC", configreader.addresses)
accept_thread.setDaemon(True)
accept_thread.start()
print("The acceptor thread is started.")
old_values = 20 

# Method to retrieve the list of range sensor values.
def range_module(datastring):
    if datastring == "+" or datastring == "":
        return current_values
    split = datastring.split("+")
    range_values = split[1].replace('{Range ', '')
    range_values = range_values.replace('}', '')
    datasplit = range_values.split(',')
    for i in range(len(datasplit)):
        if float(datasplit[i]) < 0:
            return current_values
    range_values = split[0] + "+" + range_values
    return range_values

while running:
    data = accept_thread.memory[2]
    string = data.split('\r\n')
    for i in range(len(string)):
        datasplit = re.findall('\{[^\}]*\}|\S+', string[i])
        if len(datasplit) > 6:
            if datasplit[2] == "{Type RangeScanner}":
                message = datasplit[1] + "+"
                message += datasplit[6]
    if message != "":
        current_values = range_module(message)
        if current_values != old_values:           
            old_values = current_values        
    message = ""
    if current_values != "":
        while len(accept_thread.request_data) != 0:
            command = "RCV!RSC!" + current_values + "#"
            configreader.connection(list, accept_thread.request_data[0]).send(
                                        command)
            print command
            print accept_thread.request_data[0]
            accept_thread.request_data.pop(0)  
