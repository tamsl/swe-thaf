import string
import socket

COLOR       = ['Red', 'Yellow', 'Green', 'Cyan', 'White', 'Blue', 'Purple']
TYPES       = ['SonarSensor', 'SICKL-MS', 'OdometrySensor']
NAMES       = ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'Scanner1', 'Odometry']
OPCODE      = ['RESET', 'NOP']
OPCODE_RFID = ['Release', 'Read', 'Write']

# The movement handler contains all sorts of possible movements
def handle_movement(type, *args):
    handlers = {"forward":         go_drive,
                "left":            go_drive,
                "right":           go_drive,
                "reverse":         go_drive,
                "brake":           go_drive,
                "rotate_left":     go_drive,
                "rotate_right":    go_drive,
                "rotate_robot":    go_rotate,
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

# Method to drive forward and backwards, make turns and rotations
def go_drive(s1, s2):
    s1 = str(s1)
    s2 = str(s2)
    string = "DRIVE {Left " + s1 + "} {Right " + s2 + "}\r\n"
    print string
    return string

# Method to make rotations
def go_rotate(s1):
    s1 = str(s1)
    string = "DRIVE {RotationalVelocity " + s1 + "}"
    print string
    return string

# Method to turn on and turn off the light
def go_light(lights):
    if lights == 1:
       string = "DRIVE {Light true}\r\n"
    else:
       string = "DRIVE {Light false}\r\n"
    print string
    return string
   
# Method to set the camera
def go_camera(CameraPanTilt_Link2):
    if CameraPanTilt_Link2 == 1:
       string = "SET {Type Camera} {Name CameraPanTilt_Link2} {FOV 1}\r\n"
    else:
       string = "SET {Type Camera} {Name CameraPanTilt_Link2} {FOV 1}\r\n"
    print string
    return string

# Method to leave dots used for tracing
def go_trace(b1, in1, COLOR):
    b1 = str(b1)
    in1 = str(in1)
    string = "Trace {On " + b1 + "} {Interval " + in1 + "} {Color " + COLOR +"}\r\n"
    print string
    return string

# Method to control the sensor
def go_sensor(TYPES, NAMES, OPCODE, params):
    params = str(params)
    string = "SET {Type " + TYPES + "} {Name " + NAMES + "} {Opcode " + OPCODE + "} {Params " + params + "}\r\n"
    print string
    return string

# Method to drop a tag
def go_tag(OPCODE_RFID):
    string = "SET {Type RFIDReleaser} {Name Gun} {Opcode " + OPCODE_RFID + "}\r\n"
    print string
    return string

# Method to read, write and erase RFID tags
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
