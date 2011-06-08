import string
import socket

TCP_IP = '127.0.0.1'
TCP_PORT = 2002
BUFFER_SIZE = 1024
COLOR = ['Red', 'Yellow', 'Green', 'Cyan', 'White', 'Blue', 'Purple']
TYPES = ['SonarSensor', 'SICKLMS', 'OdometrySensor']
NAMES = ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'Scanner1', 'Odometry']
OPCODE = ['RESET', 'NOP']
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send("INIT {ClassName USARBot.P2DX} {Location 4.5,1.9,1.8} {Name R1}\r\n")

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
   
while 1:
   s.send(handle_movement("camera", 1))
   s.send(handle_movement("trace", 1, 1, 'Green'))
   s.send(handle_movement("forward", 90.0, 90.0))
   s.send(handle_movement("rotate_left", -1.0, 1.0))
   s.send(handle_movement("rotate_right", 1.0, -1.0))
   s.send(handle_movement("brake", 0.0, 0.0))
   s.send(handle_movement("light", 1))
   s.send(handle_movement("sonar", 'SonarSensor', 'F3', 'RESET', 5))

s.close()
    
               
