#!/usr/bin/env python

from communicatorv2 import *
import socket
import re

##TCP_IP = '127.0.0.1'
##TCP_PORT = 2001
##BUFFER_SIZE = 1024

##s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
##s.connect((TCP_IP, TCP_PORT))
##s.send('INIT {ClassName USARBot.P2DX} {Location 4.5,1.9,1.8} {Name R1}\r\n')
list = []
flag = 1
configreader = config_reader()
accept_thread = acceptor(flag, list, "sonar", configreader.addresses)
accept_thread.setDaemon(True)
accept_thread.start()
print("ik heb de acceptor thread gestart")

while 1:
  continue
##  try:
####    data = s.recv(BUFFER_SIZE)
##    data = ""
####    string = data.split('\r\n')
####    for i in range(len(string)):
####      datasplit = re.findall('\{[^\}]*\}|\S+', string[i])
####      if len(datasplit) > 0:
####        # Sensor message
####        if datasplit[0] == "SEN":
####          if len(datasplit) > 2:
####            typeSEN2 = datasplit[2].replace('{Type ', '')
####            typeSEN2 = typeSEN2.replace('}', '')
####            # Range sensor
####            if typeSEN2 == "Sonar":
####              print datasplit, "\r\n"
####              if len(datasplit) > 9:
####                sonar_values = []
####                for i in range(0, 8):
####                  sonar_values.append(datasplit[i + 3].replace('{Name F' + str(i+1) + ' Range ', ''))
####                  sonar_values[i] = sonar_values[i].replace('}', '')
####                print sonar_values, "\r\n"
##  except:
##    accept_thread.setflag(1)
##    print(flag)
##    print("flag zou 1 moeten zijn")
##    acccept_thread.join()
##    sys.exit()
