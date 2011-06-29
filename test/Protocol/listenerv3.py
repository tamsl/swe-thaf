#!/usr/bin/env python
from communicatorv2 import *
import socket
import re
import sys
import time

TCP_IP = '127.0.0.1'
TCP_PORT = 2001
BUFFER_SIZE = 1024
running = 1
data_incomplete = 0
list = []

configreader = config_reader()
print("config reader gestart")
accept_thread = acceptor(running, list, "LIS", configreader.addresses)
accept_thread.setDaemon(True)
accept_thread.start()
#sonar module
sonar = connection(running, "SNR", configreader, list)
sonar.setDaemon(True)
sonar.start()
##sonar = configreader.connection(list, "SNR")
#odometry module
odometry = connection(running, "ODO", configreader, list)
odometry.setDaemon(True)
odometry.start()
##odometry = configreader.connection(list, "ODO")
#rangescanner module
rangescanner = connection(running, "RSC", configreader, list)
rangescanner.setDaemon(True)
rangescanner.start()
##rangescanner = configreader.connection(list, "RSC")
print ("acceptor thread gestart")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.setblocking(0)
##print s
##s.send("INIT {ClassName USARBot.P2DX} {Location 1.5,1.5,1.8} {Name R1}\r\n")
s.send("INIT {ClassName USARBot.P2DX} {Location 1.8,3.8,1.8} {Name R1}\r\n")
s.send("DRIVE {Left -1.0} {Right 1.0}\r\n")

while running:
    try:
        if accept_thread.memory[4] != "":
            print accept_thread.memory[4]
            s.send(accept_thread.memory[4])
            accept_thread.memory[4] = ""
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
        sonar.send_data(message)
        message = "RCV!RSC!" + data + "#"
        rangescanner.send_data(message)
        message = "RCV!ODO!" + data + "#"
        odometry.send_data(message)
        data = ""
    except(socket.error):
        continue    
    except:
        print("er is iets fout gegaan in listener")
        flag = 0
        print(running)
        print("running zou 1 moeten zijn")
##        acccept_thread.join()
        s.close()
        sonar.join()
        odometry.join()
        rangescanner.join()
        sys.exit()
  
s.close()
sonar.close()
odometry.close()
rangescanner.close()
