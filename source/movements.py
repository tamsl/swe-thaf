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
               "rotate_right":    go_drive
              }
   return handlers[type](*args)
    
def go_drive(s1, s2):
    s1 = str(s1)
    s2 = str(s2)
    string = "DRIVE {Left " + s1 + "} {Right " + s2 + "}\r\n"
    print string
    return string

while 1:
   s.send(handle_movement("forward", 90.0, 90.0))
   s.send(handle_movement("rotate_left", -1.0, 1.0))
   s.send(handle_movement("rotate_right", 1.0, -1.0))
   s.send(handle_movement("brake", 0.0, 0.0))

s.close()
    
               
