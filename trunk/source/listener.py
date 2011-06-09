#!/usr/bin/env python

import socket
import re

TCP_IP = '127.0.0.1'
TCP_PORT = 2001
BUFFER_SIZE = 1024
COLOR = ['Red', 'Yellow', 'Green', 'Cyan', 'White', 'Blue', 'Purple']
TYPES = ['SonarSensor', 'SICKLMS', 'OdometrySensor']
NAMES = ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'Scanner1', 'Odometry']
OPCODE = ['RESET', 'NOP']

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send('INIT {ClassName USARBot.P2DX} {Location 4.5,1.9,1.8} {Name R1}\r\n')

##SONAR_PORT = 2101
##
##sonar = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
##sonar.connect((TCP_IP, SONAR_PORT))
##
##
##IR_PORT = 2102
##
##ir = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
##ir.connect((TCP_IP, IR_PORT))
##
##
##IMU_PORT = 2103
##
##imu = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
##imu.connect((TCP_IP, IMU_PORT))
##
##
##ODOMETRY_PORT = 2104
##
##odometry = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
##odometry.connect((TCP_IP, ODOMETRY_PORT))

def handle_movement(type, *args):
   handlers = {"forward":         go_drive,
               "left":            go_drive,
               "right":           go_drive,
               "reverse":         go_drive,
               "brake":           go_drive,
               "rotate_left":     go_drive,
               "rotate_right":    go_drive,
               "light":           go_light,
               "camera":          go_camera,
               "trace":           go_trace,
               "sonar":           go_sensor,
               "laser":           go_sensor,
               "odometry":        go_sensor
              }
   return handlers[type](*args)
    
def go_drive(s1, s2):
    s1 = str(s1)
    s2 = str(s2)
    string = "DRIVE {Left " + s1 + "} {Right " + s2 + "}\r\n"
    print string
    return string

def go_light(lights):
    if lights == 1:
       string = "DRIVE {Light true}\r\n"
    else:
       string = "DRIVE {Light false}\r\n"
    print string
    return string

def go_camera(OmniCamPillar_Link2):
    if OmniCamPillar_Link2 == 1:
       string = "SET {Type Camera} {Name OmniCamPillar_Link4} {FOV 1}\r\n"
    else:
       string = "SET {Type Camera} {Name OmniCamPillar_Link4} {FOV 1}\r\n"
    print string
    return string

def go_trace(b1, in1, COLOR):
    b1 = str(b1)
    in1 = str(in1)
    string = "Trace {On " + b1 + "} {Interval " + in1 + "} {Color " + COLOR +"}\r\n"
    print string
    return string

def go_sensor(TYPES, NAMES, OPCODE, params):
    params = str(params)
    string = "SET {Type " + TYPES + "} {Name " + NAMES + "} {Opcode " + OPCODE + "} {Params " + params + "}\r\n"
    print string
    return string

for i in range(100):
  s.send(handle_movement("camera", 1))
  s.send(handle_movement("trace", 1, 1, 'Green'))
  s.send(handle_movement("forward", 90.0, 90.0))
  s.send(handle_movement("rotate_left", -1.0, 1.0))
  s.send(handle_movement("rotate_right", 1.0, -1.0))
  s.send(handle_movement("brake", 0.0, 0.0))
  s.send(handle_movement("light", 1))
  #s.send(handle_movement("sonar", 'SonarSensor', 'F3', 'RESET', 5))
  data = s.recv(BUFFER_SIZE)
  string = data.split('\r\n')
  for i in range(len(string)):
    datasplit = re.findall('\{[^\}]*\}|\S+', string[i])
    print datasplit, "\r\n"
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
  
s.close()
