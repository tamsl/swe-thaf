import string
import socket
import re
import wallsearching

TCP_IP = '127.0.0.1'
TCP_PORT = 2001
BUFFER_SIZE = 1024
COLOR = ['Red', 'Yellow', 'Green', 'Cyan', 'White', 'Blue', 'Purple']
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

# Convert the list of strings to floats.
def string_to_float(laser_vals):
    float_laser_vals = []
    for i in range(len(laser_vals)):
        float_laser_vals.append(float(laser_vals[i]))
    return float_laser_vals   

# Find the smallest value from the rangescanner sensor data and returns the
# index on which this value was found.
def min_laser_val(laser_vals):
    laser_vals = string_to_float(laser_vals)
    sorted_laser_vals = sorted(laser_vals)
    index_val = laser_vals.index(sorted_laser_vals[0])
    return sorted_laser_vals[0], index_val

### Test method for driving towards a located wall.
##def wallsearch(min_val, index_val, length):
####    print "dit is de min val" , min_val
##    # If the wall is on the left side of the robot, turn left.
##    if index_val in range(length/4):
##        s.send(handle_movement("left", -1.0, 1.0))
##
##    # If the wall is on the right side of the robot, turn right.  
##    elif index_val in range(3*length/4, length):
##        s.send(handle_movement("right", 1.0, -1.0))
##
##    # Else go straight
##    else:
##        s.send(handle_movement("forward", 1.0, 1.0))
##    return 0

# Method for following a wall.
def wallfollow(min_val, index_val, length):
    # Rotate to the left so you have the wall on the left or right side of the
    # robot.
    # side 1 is wall on right side otherwise the wall is on the left side
    side = 0
    if index_val < length/2:
        s.send(handle_movement("rotate_left", -1.5, 1.0))
    else:
        s.send(handle_movement("rotate_right", 1.0, -1.5))
    data_incomplete = 0
    while index_val not in range(length/5) and index_val not in range(4*length/5, length):
        data = s.recv(BUFFER_SIZE)
        if data[len(data)-1] != '\n':
            datatemp = data
            data_incomplete = 1
            continue
        if data_incomplete:
            datatemp += data
            data_incomplete = 0
            data = datatemp
        string = data.split('\r\n')
        laser_values = []
        for i in range(len(string)):
            datasplit = re.findall('\{[^\}]*\}|\S+', string[i])
            if len(datasplit) > 2:
               # Laser sensor
               typeSEN2 = datasplit[2].replace('{Type ', '')
               typeSEN2 = typeSEN2.replace('}', '')    
               if typeSEN2 == "RangeScanner":
                  if len(datasplit) > 6:
                     laser_values = re.findall('([\d.]*\d+)', datasplit[6])
##                     print "in wallfollow" ,laser_values, "\r\n"              
                     # Find the smallest value to see if the wall is on a side.
                     min_val, index_val = min_laser_val(laser_values)
                     
##    print "ik ga nu een muur volgen"
    # Go forward following the wall when the left or the right side is facing
    # the wall.
    if index_val > length/2:
        side = 1
    s.send(handle_movement("forward", 1.0, 1.0))
    # Return that it is now following the wall.
    return 1 , side
   
def odometry_module(datastring):
    senvalues = datastring[3].replace('{Pose ', '')
    senvalues = senvalues.replace('}','')
    odo_values = senvalues.split(',')
    return odo_values

# Main            
flag = 0
odo_done = 0
odo_values = []
data_incomplete = 0
side = 0
while 1:
    data = s.recv(BUFFER_SIZE)
    if data[len(data)-1] != '\n':
        datatemp = data
        data_incomplete = 1
        continue
    if data_incomplete:
        datatemp += data
        data_incomplete = 0
        data = datatemp
    string = data.split('\r\n')
    laser_values = []
    for i in range(len(string)):
        datasplit = re.findall('\{[^\}]*\}|\S+', string[i])
        if len(datasplit) > 2:
            # Odometry sensor
            typeSEN = datasplit[1].replace('{Type ', '')
            typeSEN = typeSEN.replace('}', '')
            if typeSEN == "Odometry":
                odo_values = odometry_module(datasplit)
##                odometry_string = "Odometry " + str(odo_values[0]) + " " + str(odo_values[1]) + " " + str(odo_values[2])
##                print odometry_string
                odo_done = 1
            # Laser sensor
            typeSEN2 = datasplit[2].replace('{Type ', '')
            typeSEN2 = typeSEN2.replace('}', '') 
            if typeSEN2 == "RangeScanner":
                if len(datasplit) > 6:
                    laser_values = re.findall('([\d.]*\d+)', datasplit[6])
##                    print len(laser_values)
##                    print "in main loop" , laser_values, "\r\n"
##                    laser_string = "Laser " + str(len(laser_values)) + " "
##                    for i in range(len(laser_values)):
##                       laser_string += laser_values[i] + " "
####                    print laser_string
                    min_val, index_val = min_laser_val(laser_values)
                    length = int(len(laser_values))
                    # The threshold for finding the wall changes when it is
                    # following a wall.
                    if flag == 1:
                        level = 0.38
                    else:
                        level = 0.3

                    print "min val: ", min_val
                    print "index val: ", index_val
                    if min_val <= level:
##                        if min_val >= 0.4 and index_val in range(length):
##                            print "ik ga nu draaien"
##                            s.send(handle_movement("left", 1.0, -1.0))
##                        else:
                        # If you get too close to the wall, you need to turn
                        # away from it.
                        if min_val <= 0.26:
                            print "ik ben te dicht bij de muur k moet bij sturen"
                            if index_val > length/2:
                                s.send(handle_movement("left", -1.0, 1.0))
                                side = 0
                            else:
                                s.send(handle_movement("right", 1.0, -1.0))
                                side = 1
                        # If you get too far from the wall but the wall is still
                        # close, go towards the wall again.
                        if min_val >= 0.30 and min_val <= 0.37:
                            print "ik ben te ver van de muur ik ga bij sturen"
                            if index_val > length/2:
                                s.send(handle_movement("right", -1.0, 1.0))
                            else:                             
                                s.send(handle_movement("left", 1.0, -1.0))
                        for i in range((length/2) - 10, (length/2) + 10):
                            print "front checker", laser_values[i]
                            if (laser_values[i] <= 0.4):
                                print "muur ahoi" 
                                if side:
                                    s.send(handle_movement("left", 1.0, -1.0))
                                else:
                                    s.send(handle_movement("right", -1.0, 1.0))
                        # Follow the wall.
                        flag, side = wallfollow(min_val, index_val, length)
                    else:
##                        print 'zoeken1'
##                        print odo_done
                        if odo_done == 1:
##                            print 'zoeken'
##                            print odo_values
                            # Find a wall.
                            flag = wallsearching.wall_continued(side, s)
