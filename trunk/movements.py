import string
import socket

TCP_IP = '127.0.0.1'
TCP_PORT = 2002
BUFFER_SIZE = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send("INIT {ClassName USARBot.P2DX} {Location 4.5,1.9,1.8} {Name R1}\r\n")


def handle_movement(type, *args):
   handlers = {"forward":         go_move,
               "left":            go_move,
               "right":           go_move,
               "reverse":         go_move,
               "brake":           go_move,
               "rotate_left":     go_move,
               "rotate_right":    go_move
              }
   return handlers[type](*args)
    
def go_move(s1, s2):
    s1 = str(s1)
    s2 = str(s2)
    string = "DRIVE {Left " + s1 + "} {Right " + s2 + "}\r\n"
    print string
    return string

#if __name__ == "__main__":
while 1:
   s.send(handle_movement("forward", 1.0, 1.0))
   s.send(handle_movement("rotate_left", -1.0, 1.0))
   s.send(handle_movement("rotate_right", 1.0, -1.0))
   s.send(handle_movement("brake", 0.0, 0.0))

s.close()
    
               
