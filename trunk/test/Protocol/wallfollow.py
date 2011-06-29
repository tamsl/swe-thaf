import string
from communicatorv2 import *
from movementsv2 import *
import socket
import re
##import wallsearching
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
odometry = connection(running, "ODO", configreader, list)
odometry.setDaemon(True)
odometry.start()
rangescanner = connection(running, "RSC", configreader, list)
rangescanner.setDaemon(True)
rangescanner.start()
listener = connection(running, "LIS", configreader, list)
listener.setDaemon(True)
listener.start()
wallsearch = connection(running, "WSC", configreader, list)
wallsearch.setDaemon(True)
wallsearch.start()
##odometry = configreader.connection(list, "ODO")
##rangescanner = configreader.connection(list, "RSC")
##listener = configreader.connection(list, "LIS")
##wallsearch = configreader.connection(list, "WSC")
print ("acceptor thread gestart")
odo = 1
ran = 2
nex = 5


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

# Method for following a wall.
def wallfollow(min_val, index_val, length):
    # Rotate to the left so you have the wall on the left or right side of the
    # robot.
    # side 1 is wall on right side otherwise the wall is on the left side
    print "in wall follow"
    side = 0
    values = []
##    if index_val < length/2:
##        listener.send("CMD!" + handle_movement("left", 1.0,-1.0) + "#")
##    else:
##        listener.send("CMD!" + handle_movement("right", 1.0,-1.0) + "#")
##    while index_val not in range(length/5) and index_val not in range(4*length/5, length):
##        print "in while loop"
##        rangescanner.send("REQ!WFW#")
##        accept_thread.set_wait(1)
##        while accept_thread.get_wait() > 0 :
##            continue
##        if accept_thread.memory[ran] == "":
##            continue
##        if len(values) > 0:
##            if values[0] == accept_thread.memory[ran].split("+")[0]:
##                continue
##        values = accept_thread.memory[ran].split("+")
##        laser_values  = values[1].split(',')
##        accept_thread.memory[ran] = ""
##        length = len(laser_values)
##        min_val,index_val = min_laser_val(laser_values)
    # Go forward following the wall when the left or the right side is facing
    # the wall.
    if index_val > length/2:
        side = 1
    print "ik ga rechtdoor"
    listener.send_data("CMD!" + handle_movement("forward", 1.0) + "#")
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
values = []
counter = 0
old_v = ""
while running:
    #request data
    print "ik begin"
    rangescanner.send_data("REQ!WFW#")
##    print "te vroeg?"
    accept_thread.set_wait(1)
##    print "ik ga wachten"
    #wait for data to arrive
    while accept_thread.get_wait() > 0 :
        if old_v != accept_thread.memory[ran]:
            print accept_thread.memory[ran]
        old_v = accept_thread.memory[ran]
##        if counter > 30000:
##            break
##            print "ik ben aan het wachten"
##        else:
##            break
##        counter += 1
##        print accept_thread.get_wait()
        continue
##    if counter > 30000:
##        print "motherfucker"
##        continue
##    counter = 0
    if accept_thread.memory[ran] == "":
        print "data is leeg"
        continue
    if len(values) > 0:
        if values[0] == accept_thread.memory[ran].split("+")[0]:
            print "data is hetzelfde"
            continue
##    print "ik ben awesome"
##    print accept_thread.memory[ran]
    
    print("data binnen")
    values = accept_thread.memory[ran].split("+")
    laser_values  = values[1].split(',')
    accept_thread.memory[ran] = ""
    length = len(laser_values)
    min_val,index_val = min_laser_val(laser_values)
    if flag == 1:
        level = 0.5
    else:
        level = 0.4

##    print "min val: ", min_val
##    print "index val: ", index_val
##    if index_val > length/2:
##        print "links"
##    else:
##        print "rechts"
##    print "dit is fc",fc
    #front checker.
    for i in range((length/2)-10,(length/2)+10):
##                        print "front checker",laser_values[i]
        if float(laser_values[i]) <= 0.45 and fc == 0:
            print "in front checker"
            fc = 1
            if index_val > length/2:
##                print "ik stuur bij naar rechts"
                listener.send_data("CMD!" + handle_movement("rotate_right", 0.3) + "#")
                side = 0
##                print "klaar met sturen"
                break
            else:
##                print "ik stuur bij naar links"
                listener.send_data("CMD!" + handle_movement("rotate_left", 0.3) + "#")
                side = 1
##                print "klaar met sturen"
                break
        elif float(laser_values[i]) <= 0.4 and fc == 1:
            break
        else :
            fc = 0
    if fc == 1 :
        continue
    fc = 0
##    print "ik ben binnen de level."
    if min_val <= level:
        # If you get too close to the wall, you need to turn
        # away from it.
        # checks the front
        if min_val <= 0.30:
            print "ik ben te dicht bij de muur k moet bij sturen"
            # the most left value is 181
            if index_val > length/2:
                print"ik stuur bij naar rechts"
                listener.send_data("CMD!" + handle_movement("rotate_right", 0.3) + "#")
                side = 1
##                print "klaar met sturen"
                continue
            else :
                print"ik stuur bij naar links"
                listener.send_data("CMD!" + handle_movement("rotate_left", 0.3) + "#")
##                print "klaar met sturen"
                side = 0
                continue
                
        # If you get too far from the wall but the wall is still
        # close, go towards the wall again.
        if min_val >= 0.38 and min_val <= 0.43:
            print "ik ben te ver van de muur ik ga bij sturen"
            if index_val > length/2:
                print"ik stuur bij naar links"
                listener.send_data("CMD!" + handle_movement("rotate_left", 0.3) + "#")
##                print "klaar met sturen"
                side = 0
                continue
            else:
                print"ik stuur bij naar rechts"
                listener.send_data("CMD!" + handle_movement("rotate_right", 0.3) + "#")
                side = 1
##                print "klaar met sturen"
                continue
        
        # Follow the wall.
        
        flag, side = wallfollow(min_val, index_val, length)
    else:
        # Find a wall.
        print "ik ben de muur kwijt"
        wallsearch.send_data("NEX!" + str(side) + "#")
        while accept_thread.memory[nex] == "":
            continue
        accept_thread.memory[nex] = ""
        flag, side = wallfollow(min_val, index_val, length)
odometry.close()
rangescanner.close()
listener.close()
wallsearch.close()
