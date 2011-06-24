#!/usr/bin/env python
from communicatorv2 import *
import socket
import re
import sys
import time

TCP_IP = '127.0.0.1'
TCP_PORT = 2001
BUFFER_SIZE = 1024
flag = 1
data_incomplete = 0
list = []

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
print s
s.send('INIT {ClassName USARBot.P2DX} {Location 4.5,1.9,1.8} {Name R1}\r\n')
configreader = config_reader()
print("config reader gestart")
accept_thread = acceptor(flag, list, "LIS", configreader.addresses)
accept_thread.setDaemon(True)
accept_thread.start()
#sonar module
sonar = configreader.connection(list, "SNR")
print(sonar)
#odometry module
odometry = configreader.connection(list, "ODO")
print(odometry)
#odometry module
rangescanner = configreader.connection(list, "RSC")
print(rangescanner)
print ("acceptor thread gestart")
s.send("DRIVE {Left -1.0} {Right 1.0}\r\n")

while 1:
    s.send(accept_thread.memory[4])
    try:
        data = s.recv(BUFFER_SIZE)
        if data_incomplete:
            datatemp += data
            data_incomplete = 0
            data = datatemp
        if data[len(data)-1] != '\n':
            datatemp = data
            data_incomplete = 1
            continue
        if len(list) == 0:
          continue
        message = "RCV!SNR!" + data + "#"
        sonar.send(message)
        message = "RCV!RSC!" + data + "#"
        rangescanner.send(message)
        message = "RCV!ODO!" + data + "#"
        odometry.send(message)
        data = ""
          
    except:
    
        print("er is iets fout gegaan in listener")
        flag = 0
        print(flag)
        print("flag zou 1 moeten zijn")
        acccept_thread.join()
        sys.exit()
  
s.close()
