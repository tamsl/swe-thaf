#!/usr/bin/env python

import socket
import re

location = [["Sonar", "127.0.0.1", 2101]]
location.append(["IR", "127.0.0.1", 2102])

def TCP_socket(module):

    f = open('config')
    config = f.readlines()
    for i in range(len(config)):
        config[i] = config[i].strip()
        adresses = config[i].split(' ')
        if(adresses[0] == module):
            print adresses
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((adresses[1], int(adresses[2])))
            return s
    print config

print location[0][0]
s = TCP_socket("routeplanner")
s.send('INIT {ClassName USARBot.P2DX} {Location 4.5,1.9,1.8} {Name R1}\r\n')

while 1:
    s.send('DRIVE {Left 1.0} {Right 1.0}\r\n')
