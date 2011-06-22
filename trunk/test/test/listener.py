#!/usr/bin/env python
import socket
import re
import sys

TCP_IP = '127.0.0.1'
TCP_PORT = 2001
BUFFER_SIZE = 4096
flag = 0
list = []
datatemp = ""

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
print s
s.send('INIT {ClassName USARBot.P2DX} {Location 4.5,1.9,1.8} {Name R1}\r\n')

while 1:
    typeSEN = ""
    typeSEN2 = ""
    s.send("DRIVE {Left 1.0} {Right 1.0}")
    data = s.recv(BUFFER_SIZE)
##    print 'data'
##    print data
##    print data[len(data)-1]
    if flag:
        datatemp += data
        flag = 0
        data = datatemp
    if data[len(data)-1] != '\n':
        datatemp = data
        flag = 1
        continue

    string = data.split('\r\n')
##    if data[len(data) != '}':
##        print data
##        flag = 1
##    if flag == 1:
##        print data
##        flag = 0
    for i in range(len(string)):
        datasplit = re.findall('\{[^\}]*\}|\S+', string[i])
##        print 'datasplit'
##        print datasplit, "\r\n"
        if len(datasplit) > 0:
            # Sensor message
            if datasplit[0] == "SEN":
                typeSEN = datasplit[1].replace('{Type ', '')
                typeSEN = typeSEN.replace('}', '')
                if len(datasplit) > 2:
                    typeSEN2 = datasplit[2].replace('{Type ', '')
                    typeSEN2 = typeSEN2.replace('}', '')
##                # Range sensor
##                if typeSEN2 == "Sonar":
##                    print "doe Sonar shit\r\n"
##                if typeSEN2 == "IR":
##                    print "doe IR shit\r\n"
##                # Laser sensor
                if typeSEN2 == "RangeScanner":
##                    datareplace = data.replace('\r\n', 'hier zit een kut enter\r\n')
##                    print '\r\ndatareplace'
##                    print datareplace
                    print datasplit[6]
                    rangedata = datasplit[6].replace('{Range ', '')
                    rangedata = rangedata.replace('}', '')
                    rangedatasplit = rangedata.split(',')
                    print rangedatasplit
                    print len(rangedatasplit)
                    print "doe RangeScanner shit\r\n"
##                    if flag == 0:
##                        flag = 1
##                if typeSEN2 == "IRScanner":
##                    print "doe IRScanner shit\r\n"
##                # Odometry sensor
##                if typeSEN == "Odometry":
##                    print "doe Odometry shit\r\n"
##                # GPS sensor
##                if typeSEN == "GPS":
##                    print "doe GPS shit\r\n"
##                # INS sensor
##                if typeSEN == "INS":
##                    print "doe INS shit\r\n"
##                # Encoder sensor
##                if typeSEN == "Encoder":
##                    print "doe Encoder shit\r\n"
##                # Touch sensor
##                if typeSEN == "Touch":
##                    print "doe Touch shit\r\n"
##                # RFID sensor
##                if typeSEN == "RFIDTag":
##                    print "doe RFID shit\r\n"
##                # Victim sensor
##                if typeSEN2 == "VictSensor":
##                    print "doe VictSensor shit\r\n"
##                # Human Motion Detection
##                if typeSEN == "HumanMotion":
##                    print "doe Human Motion shit\r\n"
##                # Sound sensor
##                if typeSEN == "Sound":
##                    print "doe Sound shit\r\n"
##                print "doe SEN shit\r\n"
##            # State message
##            if datasplit[0] == "STA":
##                typeSTA = datasplit[1].replace('{Type ', '')
##                typeSTA = typeSTA.replace('}', '')
##                if typeSTA == "GroundVehicle":
##                    print "doe GroundVehicle shit\r\n"
##                if typeSTA == "LeggedRobot":
##                    print "doe LeggedRobot shit\r\n"
##                if typeSTA == "NauticVehicle":
##                    print "doe NauticVehicle shit\r\n"
##                if typeSTA == "AerialVehicle":
##                    print "doe AerialVehicle shit\r\n"
##                print "doe STA shit\r\n"
##            # Mission package message
##            if datasplit[0] == "MISSTA":
##                print "doe MISSTA shit\r\n"
##            # Geometry information
##            if datasplit[0] == "GEO":
##                typeGEO = datasplit[1].replace('{Type ', '')
##                typeGEO = typeGEO.replace('}', '')
##                if typeGEO == "GroundVehicle":
##                    print "doe GroundVehicle shit\r\n"
##                if typeGEO == "LeggedRobot":
##                    print "doe LeggedRobot shit\r\n"
##                if typeGEO == "NauticVehicle":
##                    print "doe NauticVehicle shit\r\n"
##                if typeGEO == "AerialVehicle":
##                    print "doe AerialVehicle shit\r\n"
##                if typeGEO == "MisPkg":
##                    print "doe Mission Package shit\r\n"
##                print "doe GEO shit\r\n"
##            # Configuration information
##            if datasplit[0] == "CONF":
##                typeCONF = datasplit[1].replace('{Type ', '')
##                typeCONF = typeCONF.replace('}', '')
##                if typeCONF == "GroundVehicle":
##                    print "doe GroundVehicle shit\r\n"
##                if typeCONF == "LeggedRobot":
##                    print "doe LeggedRobot shit\r\n"
##                if typeCONF == "NauticVehicle":
##                    print "doe NauticVehicle shit\r\n"
##                if typeCONF == "AerialVehicle":
##                    print "doe AerialVehicle shit\r\n"
##                if typeCONF == "MisPkg":
##                    print "doe Mission Package shit\r\n"
##                print "doe CONF shit\r\n"
##            # Response message
##            if datasplit[0] == "RES":
##                typeRES = datasplit[2].replace('{Type ', '')
##                typeRES = typeRES.replace('}', '')
##                if typeRES == "Viewports":
##                    print "doe Viewports shit\r\n"
##                if typeRES == "Camera":
##                    print "doe Camera shit\r\n"
##                print "doe RES shit\r\n"

s.close()
