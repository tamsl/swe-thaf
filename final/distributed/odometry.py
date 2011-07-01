#!/usr/bin/env python

from communicatorv2 import *
import socket
import re

current_values = ""
list = []
running = 1
message = ""
configreader = config_reader()
accept_thread = acceptor(running, list, "ODO", configreader.addresses)
accept_thread.setDaemon(True)
accept_thread.start()
old_values = 20

# Method to retrieve the list of odometry values.
def odometry_module(datastring):
    if datastring == "+" or datastring == "":
        return current_values
    datasplit = datastring.split('+')
    odo_values = ""
    odo_values = datasplit[1].replace('{Pose ', '')
    odo_values = odo_values.replace('}', '')
    check = odo_values.split(',')
    if len(check) > 2:
        if (float(check[2]) > 3.15) or (float(check[2]) < -3.15):
            return current_values
    else:
        return current_values
    odo_values = datasplit[0] + "+" + odo_values
    return odo_values

flag = 1
while running:
    data = accept_thread.memory[1]
    string = data.split('\r\n')
    for i in range(len(string)):
        datasplit = re.findall('\{[^\}]*\}|\S+', string[i])
        if len(datasplit) > 3:
            if datasplit[2] == "{Type Odometry}":
                message = ""
                message = datasplit[1] + "+"
                message += datasplit[4]
    if message != "":
        current_values = odometry_module(message)
        if current_values != old_values:
            old_values = current_values
    if current_values != "":
        while len(accept_thread.request_data) != 0:
            command = "RCV!ODO!" + str(current_values) + "#"
            configreader.connection(list, accept_thread.request_data[0]).send(
                                         command)
            accept_thread.request_data.pop(0)
