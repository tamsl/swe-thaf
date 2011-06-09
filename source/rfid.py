#!/usr/bin/env python

import socket
import re

TCP_IP = '127.0.0.1'
TCP_PORT = 2002
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send('INIT {ClassName USARBot.P2DX} {Location 4.5,1.9,1.8} {Name R1}\r\n')

def rfid_module(datastring):
  id_values = []
  for i in range(len(datastring)):
    id_values.append(0)
    datastring[i] = datastring[i].replace('{ID ', '')
    id_values[i] = datastring[i].replace('}','')
  for i in range(4):
    id_values.pop(0)
  print id_values
  return id_values

for i in range(10000):
  s.send("DRIVE {Left 1.0}\r\n")
  data = s.recv(BUFFER_SIZE)
  string = data.split('\r\n')
  for i in range(len(string)):
    datasplit = re.findall('\{[^\}]*\}|\S+', string[i])
    if len(datasplit) > 0:
      # Sensor message
      if datasplit[0] == "SEN":
        typeSEN = datasplit[2].replace('{Type ', '')
        typeSEN = typeSEN.replace('}', '')
        # RFID sensor
        if typeSEN == "RFID":
          id_value = rfid_module(datasplit)
          
s.close()
