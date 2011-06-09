#!/usr/bin/env python

import socket
import re

TCP_IP = '127.0.0.1'
TCP_PORT = 2001
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send('INIT {ClassName USARBot.P2DX} {Location 4.5,1.9,1.8} {Name R1}\r\n')

for i in range(100):
  s.send("DRIVE {Left 1.0} {Right 1.0}")
  data = s.recv(BUFFER_SIZE)
  string = data.split('\r\n')
  for i in range(len(string)):
    datasplit = re.findall('\{[^\}]*\}|\S+', string[i])
    if len(datasplit) > 0:
      # Sensor message
      if datasplit[0] == "SEN":
        if len(datasplit) > 2:
          typeSEN2 = datasplit[2].replace('{Type ', '')
          typeSEN2 = typeSEN2.replace('}', '')
        if len(datasplit) > 9:
          typeSEN3 = datasplit[3].replace('{Name F1 Range ', '')
          typeSEN3 = typeSEN3.replace('}', '')
          typeSEN4 = datasplit[4].replace('{Name F2 Range ', '')
          typeSEN4 = typeSEN4.replace('}', '')
          typeSEN5 = datasplit[5].replace('{Name F3 Range ', '')
          typeSEN5 = typeSEN5.replace('}', '')          
          typeSEN6 = datasplit[6].replace('{Name F4 Range ', '')
          typeSEN6 = typeSEN6.replace('}', '')
          typeSEN7 = datasplit[7].replace('{Name F5 Range ', '')
          typeSEN7 = typeSEN7.replace('}', '')
          typeSEN8 = datasplit[8].replace('{Name F6 Range ', '')
          typeSEN8 = typeSEN8.replace('}', '')          
          typeSEN9 = datasplit[9].replace('{Name F7 Range ', '')
          typeSEN9 = typeSEN9.replace('}', '')
          typeSEN10 = datasplit[10].replace('{Name F8 Range ', '')
          typeSEN10 = typeSEN10.replace('}', '')
        # Range sensor
        if typeSEN2 == "Sonar":
          print datasplit, "\r\n"
          print typeSEN2, typeSEN3, typeSEN4, typeSEN5, typeSEN6, typeSEN7, typeSEN8, typeSEN9, typeSEN10, "\r\n"

s.close()
