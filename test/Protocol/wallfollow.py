import string
from communicatorv2 import *
import socket
import re
import wallsearching
import time


##COLOR = ['Red', 'Yellow', 'Green', 'Cyan', 'White', 'Blue', 'Purple']

BUFFER_SIZE = 1024
current_vlaues = ""
list = []
running = 1
configreader = config_reader()
accept_thread = acceptor(running, list, "WFW", configreader.addresses)
accept_thread.setDaemon(True)
accept_thread.start()
odometry = configreader.connection(list, "ODO")
rangescanner = configreader.connection(list, "RSC")
listener = configreader.connection(list, "LIS")
wallsearch = configreader.connection(list, "WSC")
print ("acceptor thread gestart")
odo = 1
ran = 2
nex = 5

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
    string = ("Trace {On " + b1 + "} {Interval " + in1 + "}" +
              "{Color " + COLOR +"}\r\n")
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
        rangescanner.send("REQ!WFW#")
##        odometry.send("REQ!WFW#")
        accept_thread.waiting_for_data += 1
        while accept_thread.waiting_for_data > 0 :
            continue
##        odometry_value = accept_thread.memory[odo]
        laser_values  = accept_thread.memory[ran]
        min_val,index_val = min_laser_val(laser_values)
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
fc = 0
laser_values = []
while 1:
    data = s.recv(BUFFER_SIZE)
    #request data
    rangescanner.send("REQ!WFW#")
    accept_thread.waiting_for_data += 1
    #wait for data to arrive
    while accept_thread.waiting_for_data > 0 :
        continue
           
    laser_values  = accept_thread.memory[ran]

    if flag == 1:
        level = 0.5
    else:
        level = 0.4

    print "min val: ", min_val
    print "index val: ", index_val
    if index_val > length/2:
        print "links"
    else:
        print "rechts"
    print "dit is fc",fc
    for i in range((length/2)-10,(length/2)+10):
##                        print "front checker",laser_values[i]
        if float(laser_values[i]) <= 0.45 and fc == 0:
            print "in front checker"
            fc = 1
            if index_val > length/2:
                print"ik stuur bij naar rechts"
                s.send(handle_movement("right", 2.0, -1.0))
                side = 1 
                break
            else:
                print"ik stuur bij naar link"
                s.send(handle_movement("left", -1.0, 2.0))
                side =1
                break
        elif float(laser_values[i]) <= 0.4 and fc == 1:
            break
        else :
            fc = 0
    if fc == 1 :
        break
    fc = 0
    if min_val <= level:
        # If you get too close to the wall, you need to turn
        # away from it.
        #checks the front
        if min_val <= 0.30:
            print "ik ben te dicht bij de muur k moet bij sturen"
            # the most left value is 181
            if index_val > length/2:
                print"ik stuur bij naar rechts"
                s.send(handle_movement("right", 1.0,-1.0))
                side = 0
                break
            else :
                print"ik stuur bij naar links"
                s.send(handle_movement("left", -1.0,1.0))
                break
                side = 1
        # If you get too far from the wall but the wall is still
        # close, go towards the wall again.
        if min_val >= 0.38 and min_val <= 0.4:
            print "ik ben te ver van de muur ik ga bij sturen"
            if index_val > length/2:
                print"ik stuur bij naar rechts"
                s.send(handle_movement("left", -1.0, 1.0))
                side = 0
                break
            else:
                print"ik stuur bij naar links"
                s.send(handle_movement("right", 1.0, -1.0))
                side = 1
                break
        
        # Follow the wall.
        
        flag, side = wallfollow(min_val, index_val, length)
    else:
        if odo_done == 1:

            # Find a wall.
            print "ik ben de muur kwijt"
            wallsearch.send("NEX!"+ side +"#")
            while len(accept_thread.memory[nex]) == "":
                continue
            flag, side = wallfollow(min_val, index_val, length)
