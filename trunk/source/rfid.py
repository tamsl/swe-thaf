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
OPCODE_RFID = ['Release', 'Read', 'Write']
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send("INIT {ClassName USARBot.P2DX} {Location 1.5,2.0,1.8} {Name R1}\r\n")

def rfid_module(datastring):
  id_values = []
  for i in range(len(datastring)):
    id_values.append(0)
    datastring[i] = datastring[i].replace('{ID ', '')
    id_values[i] = datastring[i].replace('}','')
  for i in range(4):
    id_values.pop(0)
#  print id_values
  return id_values

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
               "odometry":        go_sensor,
               "rfid-tag":        go_tag,
               "rfid":            go_rfid,
              }
   return handlers[type](*args)
    
def go_drive(s1, s2):
    s1 = str(s1)
    s2 = str(s2)
    string = "DRIVE {Left " + s1 + "} {Right " + s2 + "}\r\n"
   # print string
    return string

def go_light(lights):
    if lights == 1:
       string = "DRIVE {Light true}\r\n"
    else:
       string = "DRIVE {Light false}\r\n"
  #  print string
    return string

def go_camera(CameraPanTilt_Link2):
    if CameraPanTilt_Link2 == 1:
       string = "SET {Type Camera} {Name CameraPanTilt_Link2} {FOV 1}\r\n"
    else:
       string = "SET {Type Camera} {Name CameraPanTilt_Link2} {FOV 1}\r\n"
#    print string
    return string

def go_trace(b1, in1, COLOR):
    b1 = str(b1)
    in1 = str(in1)
    string = "Trace {On " + b1 + "} {Interval " + in1 + "} {Color " + COLOR +"}\r\n"
#    print string
    return string

def go_sensor(TYPES, NAMES, OPCODE, params):
    params = str(params)
    string = "SET {Type " + TYPES + "} {Name " + NAMES + "} {Opcode " + OPCODE + "} {Params " + params + "}\r\n"
#    print string
    return string

def go_tag(OPCODE_RFID):
    string = "SET {Type RFIDReleaser} {Name Gun} {Opcode " + OPCODE_RFID + "}\r\n"
#    print string
    return string

def go_rfid(OPCODE_RFID, RFIDTagID, MemoryContent):
    MemoryContent = str(MemoryContent)
    string = " "
    for i in range(len(RFIDTagID)):  
        if OPCODE_RFID == 'Write': 
            string = "SET {Type RFID} {Name RFID} {Opcode " + OPCODE_RFID + "} {Params " + RFIDTagID[i] + MemoryContent + "}\r\n"  
        elif OPCODE_RFID == 'Read':
            string = "SET {Type RFID} {Name RFID} {Opcode " + OPCODE_RFID + "} {Params " + RFIDTagID[i] + "}\r\n"
#    print string
    return string  

while 1:
  #s.send("DRIVE {Left 1.0}\r\n")
  data = s.recv(BUFFER_SIZE)
  string = data.split('\r\n')
  id_value = []
  for i in range(len(string)):
    datasplit = re.findall('\{[^\}]*\}|\S+', string[i])
#    print datasplit
    if len(datasplit) > 0:
      # Sensor message
      if datasplit[0] == "SEN":
        typeSEN = datasplit[2].replace('{Type ', '')
        typeSEN = typeSEN.replace('}', '')
        # RFID sensor
        if typeSEN == "RFID":
          print datasplit
          id_value = rfid_module(datasplit)
          
  s.send(handle_movement("camera", 1))
  s.send(handle_movement("rfid-tag", 'Release'))
  s.send(handle_movement("trace", 1, 1, 'White'))
  s.send(handle_movement("forward", 5.0, 5.0))
  #s.send(handle_movement("rotate_left", 1.0, -1.0))
  #s.send(handle_movement("rotate_right", -1.0, 1.0))
  #s.send(handle_movement("brake", 0.0, 0.0))
  s.send(handle_movement("light", 1))
  s.send(handle_movement("sonar", 'SonarSensor', 'F3', 'RESET', 5))
  s.send(handle_movement("rfid", 'Write', id_value, 0))

s.close()
