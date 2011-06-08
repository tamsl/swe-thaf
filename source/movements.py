import string
import socket

TCP_IP = '127.0.0.1'
TCP_PORT = 2002
BUFFER_SIZE = 1024
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
               "mission":          go_mission,
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

def go_mission(f1, i1, f2, i2):
    i1 = str(i1)
    f1 = str(f1)
    f2 = str(f2)
    i2 = str(i2)
    string = "MISPGK {Name OmniCamPillar} {Link" + i1 + "} {Value" + f1 + "} {Link" + i2 + "} {Value" + f2 + "}\r\n"
    print string
    return string

while 1:
   s.send(handle_movement("camera", 1))
   s.send(handle_movement("mission", 3, 3, 5, 5))
   #s.send(handle_movement("forward", 90.0, 90.0))
   #s.send(handle_movement("rotate_left", -1.0, 1.0))
   s.send(handle_movement("rotate_right", 1.0, -1.0))
   #s.send(handle_movement("brake", 0.0, 0.0))
   #s.send(handle_movement("light", 1))

s.close()
    
               
