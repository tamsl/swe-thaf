import string
import socket
import re

TCP_IP = '127.0.0.1'
TCP_PORT = 2001
BUFFER_SIZE = 1024
COLOR = ['Red', 'Yellow', 'Green', 'Cyan', 'White', 'Blue', 'Purple']
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
#s.send("INIT {ClassName USARBot.P2DX} {Location 4.5,1.9,1.8} {Name R1}\r\n")
s.send("INIT {ClassName USARBot.P2DX} {Location 2.0,2.0,1.8} {Name R1}\r\n")
x = []
y = []
theta = []

def handle_movement(type, *args):
   handlers = {"forward":         go_drive,
               "left":            go_drive,
               "right":           go_drive,
               "reverse":         go_drive,
               "brake":           go_drive,
               "rotate_left":     go_drive,
               "rotate_right":    go_drive,
               "trace":           go_trace,
              }
   return handlers[type](*args)

def go_drive(s1, s2):
    s1 = str(s1)
    s2 = str(s2)
    string = "DRIVE {Left " + s1 + "} {Right " + s2 + "}\r\n"
    #print string
    return string

def go_trace(b1, in1, COLOR):
    b1 = str(b1)
    in1 = str(in1)
    string = "Trace {On " + b1 + "} {Interval " + in1 + "} {Color " + COLOR +"}\r\n"
    #print string
    return string

def string_to_float(laser_vals):
    float_laser_vals = []
    for i in range(len(laser_vals)):
        float_laser_vals.append(float(laser_vals[i]))
    return float_laser_vals   

def min_laser_val(laser_vals):
##    print laser_vals
##    print len(laser_vals)
    laser_vals = string_to_float(laser_vals)
    sorted_laser_vals = sorted(laser_vals)
    index_val = laser_vals.index(sorted_laser_vals[0]) + 1 
##    print sorted_laser_vals, "\r\n"
##    print "binnen minlaser" ,index_val
    return sorted_laser_vals[0], index_val

def wallsearch(min_val, index_val, length):
    print "dit is de min val" ,min_val
    if min_val <= 0.25 and min_val != 0.0:
        wallfollow(min_val, index_val, length)
##        print "ben uit wallsearch"
    else:
##        print index_val
        if index_val in range(length/4):
##            print "Richting een muur links"
            s.send(handle_movement("left", -1.0, 1.0))
        elif index_val in range(3*length/4, length):
##            print "Richting een muur rechts"
            s.send(handle_movement("right", 1.0, -1.0))
        else:
            #odometry_module()
##            print "Richting een muur rechtdoor"
            s.send(handle_movement("forward", 1.0, 1.0))

def wallfollow(min_val, index_val, length):
    #print "Roteer 90 graden naar links"
    s.send(handle_movement("rotate_left", -1.5, 1.0))
    print index_val
    while index_val not in range(3*length/4, length):
        data = s.recv(BUFFER_SIZE)
        string = data.split('\r\n')
        laser_values = []
        for i in range(len(string)):
            datasplit = re.findall('\{[^\}]*\}|\S+', string[i])
            if len(datasplit) > 2:
                #print datasplit, "\r\n"
                typeSEN = datasplit[1].replace('{Type ', '')
                typeSEN = typeSEN.replace('}', '')
                typeSEN2 = datasplit[2].replace('{Type ', '')
                typeSEN2 = typeSEN2.replace('}', '')            
                # Odometry sensor
                #if typeSEN == "Odometry":
                    #odometry_module(datasplit)
                    # Laser sensor
                if typeSEN2 == "RangeScanner":
                    if len(datasplit) > 7:
                        laser_values = re.findall('([\d.]*\d+)', datasplit[7])
                        print "in wallfollow" ,laser_values, "\r\n"              
                        for i in range(0, len(laser_values)):
                            min_val, index_val = min_laser_val(laser_values)
    print (3*length/4)                        
    if index_val in range(3*length/4, length):
        h = int(length/2)
##        print index_val
        print "ik ben binnen"
        if index_val in range((h/2)-(h/5), (h/2)+(h/5)):
            #print "Roteer 90 graden naar links"
            print "ik ga een muur zoeken" 
            s.send(handle_movement("rotate_left", -1.5, 1.0))
        #print "Volg rechtermuur"
        print "ik ga nu een muur volgen"
        s.send(handle_movement("forward", 1.0, 1.0))
    wallsearch(min_val, index_val, length)

def odometry_module(datastring):
    senvalues = datastring[3].replace('{Pose ', '')
    senvalues = senvalues.replace('}','')
    odo_values = senvalues.split(',')
    x.append(odo_values[0])
    y.append(odo_values[1])
    theta.append(odo_values[2])
    if len(x) == 200:
        #print "\r\nx-waarde: ", x, "\r\n\r\ny-waarde: ", y, "\r\n\r\ntheta: ", theta
        x.sort()
        y.sort()
        theta.sort()
        #print "\r\nsorted x: ", x, "\r\n"
        diff_x = abs(float(x[99]) - float(x[0]))
        #print "kleinste x: ", x[0], "\r\ngrootste x: ", x[99], "\r\nverschil x: ", diff_x
        #print "\r\nsorted y: ", y, "\r\n"
        diff_y = abs(float(y[99]) - float(y[0]))
        #print "kleinste y: ", y[0], "\r\ngrootste y: ", y[99], "\r\nverschil y: ", diff_y
        #print "\r\nsorted theta: ", theta, "\r\n"
        diff_theta = abs(float(theta[99]) - float(theta[0]))
        #print "kleinste theta: ", theta[0], "\r\ngrootste theta: ", theta[99], "\r\nverschil theta: ", diff_theta
        if diff_x < 0.2 and diff_y < 0.2:
           string = "Ik sta stil\r\n"
           return string
        for i in range(0, len(x)):
            x.pop()
            y.pop()
            theta.pop()

while 1:
    data = s.recv(BUFFER_SIZE)
    string = data.split('\r\n')
    laser_values = []
    for i in range(len(string)):
        datasplit = re.findall('\{[^\}]*\}|\S+', string[i])
        if len(datasplit) > 2:
            #print datasplit, "\r\n"
            typeSEN = datasplit[1].replace('{Type ', '')
            typeSEN = typeSEN.replace('}', '')
            typeSEN2 = datasplit[2].replace('{Type ', '')
            typeSEN2 = typeSEN2.replace('}', '')            
            # Odometry sensor
            #if typeSEN == "Odometry":
                #odometry_module(datasplit)
                # Laser sensor
            if typeSEN2 == "RangeScanner":
                if len(datasplit) > 7:
                    laser_values = re.findall('([\d.]*\d+)', datasplit[7])
##                    print len(laser_values)
##                    print "in main loop" , laser_values, "\r\n"              
                    for i in range(len(laser_values)):
                        min_val, index_val = min_laser_val(laser_values)
                        wallsearch(min_val, index_val, len(laser_values))
