import string
import socket
import re

TCP_IP = '127.0.0.1'
TCP_PORT = 2002
BUFFER_SIZE = 1024
COLOR = ['Red', 'Yellow', 'Green', 'Cyan', 'White', 'Blue', 'Purple']
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
#s.send("INIT {ClassName USARBot.P2DX} {Location 4.5,1.9,1.8} {Name R1}\r\n")
s.send("INIT {ClassName USARBot.P2DX} {Location 4.3,1.1,1.8} {Name R1}\r\n")

def handle_movement(type, *args):
   handlers = {"forward":         go_drive,
               "left":            go_drive,
               "right":           go_drive,
               "reverse":         go_drive,
               "brake":           go_drive,
               "rotate_left":     go_drive,
               "rotate_right":    go_drive,
               "trace":           go_trace,
               "rotate_robot":    go_rotate,
              }
   return handlers[type](*args)

def go_drive(s1, s2):
    s1 = str(s1)
    s2 = str(s2)
    string = "DRIVE {Left " + s1 + "} {Right " + s2 + "}\r\n"
    print string
    return string

def go_trace(b1, in1, COLOR):
    b1 = str(b1)
    in1 = str(in1)
    string = "Trace {On " + b1 + "} {Interval " + in1 + "} {Color " + COLOR +"}\r\n"
    print string
    return string

def go_rotate(s1):
    s1 = str(s1)
    string = "DRIVE {RotationalVelocity " + s1 + "}"
    print string
    return string

def string_to_float(sonar_vals):
    float_sonar_vals = []
    for i in range(len(sonar_vals)):
        float_sonar_vals.append(float(sonar_vals[i]))
    return float_sonar_vals     

def min_sonar_val(sonar_vals):
    sonar_vals = string_to_float(sonar_vals)
    sorted_sonar_vals = sorted(sonar_vals)
    index_val = sonar_vals.index(sorted_sonar_vals[0]) + 1
    print sorted_sonar_vals[0]
    print index_val
    return sorted_sonar_vals[0], index_val
   
def wallsearch(min_val, index_val):
    print "Roteer 360 graden"
    x = s.send(handle_movement("rotate_robot", 0.05))
    while(x):
    #if min_val <= 0.20 and (index_val == 4 or index_val == 5):
    #    s.send(handle_movement("brake", 0, 0)) 
    #else:
        for index_val in range(1,9):
            if min_val:
                if index_val == 1:
                    print "Richting een muur links"
                    s.send(handle_movement("rotate_left", -2.0, 2.0))
                    break
                elif index_val == 2:
                    print "Richting een muur links"
                    s.send(handle_movement("rotate_left", -1.5, 1.5))
                    break
                elif index_val == 3:
                    print "Richting een muur links"
                    s.send(handle_movement("rotate_left", -1.0, 1.0))
                    break
                elif index_val == 6:
                    print "Richting een muur rechts"
                    s.send(handle_movement("rotate_right", 1.0, -1.0))
                    break
                elif index_val == 7:
                    print "Richting een muur rechts"
                    s.send(handle_movement("rotate_right", 1.5, -1.5))
                    break
                elif index_val == 8:
                    print "Richting een muur rechts"
                    s.send(handle_movement("rotate_right", 2.0, -2.0))
                    break
                elif index_val == 4 or index_val == 5:
                    print "Richting een muur rechtdoor"
                    s.send(handle_movement("forward", 1.0, 1.0))
                    break

while(1):
    data = s.recv(BUFFER_SIZE)
    string = data.split('\r\n')
    sonar_values = []
    for i in range(len(string)):
        datasplit = re.findall('\{[^\}]*\}|\S+', string[i])
        if len(datasplit) > 0:
            # Sensor message
            if datasplit[0] == "SEN":
                if len(datasplit) > 2:
                    typeSEN2 = datasplit[2].replace('{Type ', '')
                    typeSEN2 = typeSEN2.replace('}', '')
                    # Range sensor
                    if typeSEN2 == "Sonar":
                        print datasplit, "\r\n"
                        if len(datasplit) > 9:
                            for i in range(0, 8):
                                sonar_values.append(datasplit[i + 3].replace('{Name F' + str(i + 1) + ' Range ', ''))
                                sonar_values[i] = sonar_values[i].replace('}', '')
                            print sonar_values, "\r\n"
                            min_val, index_val = min_sonar_val(sonar_values)
                            wallsearch(min_val, index_val)

      
     #sonar_vals = [4.001, 4.243, 5.000, 2.865, 3.852, 2.534, 1.948, 3.28]

      



