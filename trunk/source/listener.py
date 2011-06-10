#!/usr/bin/env python
from communicator import *
import socket
import re
import sys

TCP_IP = '127.0.0.1'
TCP_PORT = 2001
BUFFER_SIZE = 1024
flag = 0
list = []

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
print s
s.send('INIT {ClassName USARBot.P2DX} {Location 4.5,1.9,1.8} {Name R1}\r\n')
configreader = config_reader()
print("config reader gestart")
#sonar module
sonar = configreader.connection(list, "sonar")
print(sonar)
print("miauw miauw miauw")
accept_thread = acceptor(list, flag, "listener", configreader.addresses)
accept_thread.start()
print ("acceptor thread gestart")

while 1:
  try:
##    s.send("DRIVE {Left 1.0} {Right 1.0}")
    data = s.recv(BUFFER_SIZE)
    print data
    if len(list) == 0:
      continue
    string = data.split('\r\n')
##    print("in de while loop")
    for i in range(len(string)):
      datasplit = re.findall('\{[^\}]*\}|\S+', string[i])
##      print datasplit, "\r\n"
      if len(datasplit) > 0:
        # Sensor message
        if datasplit[0] == "SEN":
          typeSEN = datasplit[1].replace('{Type ', '')
          typeSEN = typeSEN.replace('}', '')
          if len(datasplit) > 2:
            typeSEN2 = datasplit[2].replace('{Type ', '')
            typeSEN2 = typeSEN2.replace('}', '')
          # Range sensor
          if typeSEN2 == "Sonar":
            print("bla123")
            sonar.send("REQ ")
            print "doe Sonar shit\r\n"
          if typeSEN2 == "IR":
            print "doe IR shit\r\n"
          # Laser sensor
          if typeSEN2 == "RangeScanner":
            print "doe RangeScanner shit\r\n"
          if typeSEN2 == "IRScanner":
            print "doe IRScanner shit\r\n"
          # Odometry sensor
          if typeSEN == "Odometry":
            print "doe Odometry shit\r\n"
          # GPS sensor
          if typeSEN == "GPS":
            print "doe GPS shit\r\n"
          # INS sensor
          if typeSEN == "INS":
            print "doe INS shit\r\n"
          # Encoder sensor
          if typeSEN == "Encoder":
            print "doe Encoder shit\r\n"
          # Touch sensor
          if typeSEN == "Touch":
            print "doe Touch shit\r\n"
          # RFID sensor
          if typeSEN == "RFIDTag":
            print "doe RFID shit\r\n"
          # Victim sensor
          if typeSEN2 == "VictSensor":
            print "doe VictSensor shit\r\n"
          # Human Motion Detection
          if typeSEN == "HumanMotion":
            print "doe Human Motion shit\r\n"
          # Sound sensor
          if typeSEN == "Sound":
            print "doe Sound shit\r\n"
          print "doe SEN shit\r\n"
        # State message
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
        # Mission package message
        if datasplit[0] == "MISSTA":
          print "doe MISSTA shit\r\n"
        # Geometry information
        if datasplit[0] == "GEO":
          typeGEO = datasplit[1].replace('{Type ', '')
          typeGEO = typeGEO.replace('}', '')
          if typeGEO == "GroundVehicle":
            print "doe GroundVehicle shit\r\n"
          if typeGEO == "LeggedRobot":
            print "doe LeggedRobot shit\r\n"
          if typeGEO == "NauticVehicle":
            print "doe NauticVehicle shit\r\n"
          if typeGEO == "AerialVehicle":
            print "doe AerialVehicle shit\r\n"
          if typeGEO == "MisPkg":
            print "doe Mission Package shit\r\n"
          print "doe GEO shit\r\n"
        # Configuration information
        if datasplit[0] == "CONF":
          typeCONF = datasplit[1].replace('{Type ', '')
          typeCONF = typeCONF.replace('}', '')
          if typeCONF == "GroundVehicle":
            print "doe GroundVehicle shit\r\n"
          if typeCONF == "LeggedRobot":
            print "doe LeggedRobot shit\r\n"
          if typeCONF == "NauticVehicle":
            print "doe NauticVehicle shit\r\n"
          if typeCONF == "AerialVehicle":
            print "doe AerialVehicle shit\r\n"
          if typeCONF == "MisPkg":
            print "doe Mission Package shit\r\n"
          print "doe CONF shit\r\n"
        # Response message
        if datasplit[0] == "RES":
          typeRES = datasplit[2].replace('{Type ', '')
          typeRES = typeRES.replace('}', '')
          if typeRES == "Viewports":
            print "doe Viewports shit\r\n"
          if typeRES == "Camera":
            print "doe Camera shit\r\n"
          print "doe RES shit\r\n"
          
  except:
    print("er is iets fout gegaan in listener")
    accept_thread.setflag(1)
    print(flag)
    print("flag zou 1 moeten zijn")
    acccept_thread.join()
    sys.exit()
  
s.close()
