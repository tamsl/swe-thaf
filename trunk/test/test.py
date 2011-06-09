#!/usr/bin/env python

import socket

class config_reader():

    def connection(module):
        adresses = config[i].split(' ')
        if(adresses[0] == module):
            print adresses
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((adresses[1], int(adresses[2])))
            return s
    
    f = open('config')
    config = f.readlines()
    for i in range(len(config)):
        config[i] = config[i].strip()
