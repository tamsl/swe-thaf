def handle_movement(type, *args):
   handlers = {"forward":         go_drive,
               "left":            go_left,
               "right":           go_right ,
               "reverse":         go_reverse,
               "brake":           go_brake,
##               "rotate_left":     go_drive,
##               "rotate_right":    go_drive,
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
    print string
    return string

def go_reverse():
   string = "DRIVE {Left -1.0} {Right -1.0}\r\n"
   print string
   return string

def go_left():
   string = "DRIVE {Left -2.0} {Right 2.0}\r\n"
   print string
   return string

def go_right():
   string = "DRIVE {Left 2.0} {Right -2.0}\r\n"
   print string
   return string

def go_brake():
   string = "DRIVE {Left 0.0} {Right 0.0}\r\n"
   print string
   return string

def go_light(lights):
    if lights == 1:
       string = "DRIVE {Light true}\r\n"
    else:
       string = "DRIVE {Light false}\r\n"
    print string
    return string

def go_camera(CameraPanTilt_Link2):
    if CameraPanTilt_Link2 == 1:
       string = "SET {Type Camera} {Name CameraPanTilt_Link2} {FOV 1}\r\n"
    else:
       string = "SET {Type Camera} {Name CameraPanTilt_Link2} {FOV 1}\r\n"
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

def go_tag(OPCODE_RFID):
    string = "SET {Type RFIDReleaser} {Name Gun} {Opcode " + OPCODE_RFID + "}\r\n"
    print string
    return string

def go_rfid(OPCODE_RFID, RFIDTagID, MemoryContent):
    MemoryContent = str(MemoryContent)
    string = " "
    for i in range(len(RFIDTagID)):  
        if OPCODE_RFID == 'Write': 
            string = "SET {Type RFID} {Name RFID} {Opcode " + OPCODE_RFID + "} {Params " + RFIDTagID[i] + MemoryContent + "}\r\n"  
        elif OPCODE_RFID == 'Read':
            string = "SET {Type RFID} {Name RFID} {Opcode " + OPCODE_RFID + "} {Params " + RFIDTagID[i] + "}\r\n"
    print string
    return string  

               
