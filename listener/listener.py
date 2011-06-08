#!/usr/bin/env python

import socket
import re

TCP_IP = '127.0.0.1'
TCP_PORT = 2001
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send('INIT {ClassName USARBot.P2DX} {Location 4.5,1.9,1.8} {Name R1}\r\n')

while 1:
  s.send('DRIVE {Left 1.0}\r\n')
  data = s.recv(BUFFER_SIZE)
  string = data.split('\r\n')
  for i in range(len(string)):
    datasplit = re.findall('\{[^\}]*\}|\S+', string[i])
    print datasplit
    if len(datasplit) > 0:
      if datasplit[0] == "SEN":
        typeSEN = datasplit[1].replace('{Type ', '')
        typeSEN = typeSEN.replace('}', '')
        print typeSEN
        #Range Sensor
        if typeSEN == "Sonar":
          print "doe Sonar shit\r\n"
        if typeSEN == "IR":
          print "doe IR shit\r\n"
        #Laser Sensor
        if typeSEN == "RangeScanner":
          print "doe RangeScanner shit\r\n"
        if typeSEN == "IRScanner":
          print "doe IRScanner shit\r\n"
        #Odometry sensor
        if typeSEN == "Odometry":
          print "doe Odometry shit\r\n"
        #GPS Sensor
        if typeSEN == "GPS":
          print "doe GPS shit\r\n"
        #INS Sensor
        if typeSEN == "INS":
          print "doe INS shit\r\n"
        #Encoder Sensor
        if typeSEN == "Encoder":
          print "doe Encoder shit\r\n"
        #Touch Sensor
        if typeSEN == "Touch":
          print "doe Touch shit\r\n"
        #RFID Sensor
        if typeSEN == "RFIDTag":
          print "doe RFID shit\r\n"
        #Victim Sensor
        if typeSEN == "VictSensor":
          print "doe Victim shit\r\n"
        #Human Motion Detection
        if typeSEN == "HumanMotion":
          print "doe Human Motion shit\r\n"
        #Sound Sensor
        if typeSEN == "Sound":
          print "doe Sound shit\r\n"
        print "doe SEN shit\r\n"
      if datasplit[0] == "STA":
        typeSTA = datasplit[1].replace('{Type ', '')
        typeSTA = typeSTA.replace('}', '')
        if typeSTA == "GroundVehicle":
          print "doe GroundVehicle shit\r\n"
        if typeSTA == "LeggedRobot":
          print "doe LeggedRobot shit\r\n"
        if typeSTA == "NauticVehicle":
          print "doe NauticVehicle shit\r\n"
        if typeSTA == "AerialVehicle":
          print "doe AerialVehicle shit\r\n"
        print "doe STA shit\r\n"
      if datasplit[0] == "MISSTA":
        print "doe MISSTA shit\r\n"
      if datasplit[0] == "GEO":
        print "doe GEO shit\r\n"
      if datasplit[0] == "CONF":
        print "doe CONF shit\r\n"
      if datasplit[0] == "RES":
        print "doe RES shit\r\n"
  
s.close()
