import string
from communicatorv2 import *
from movementsv2 import *
import socket
import re
import time

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
    side = 0
    values = []
    # Go forward following the wall when the left or the right side is facing
    # the wall.
    if index_val > length/2:
        side = 1
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
while running:
    #request data
    rangescanner.send_data("REQ!WFW#")
    accept_thread.set_wait(1)
    #wait for data to arrive
    while accept_thread.get_wait() > 0 :
        continue
    if accept_thread.memory[ran] == "":
        continue
    if len(values) > 0:
        if values[0] == accept_thread.memory[ran].split("+")[0]:
            continue
    values = accept_thread.memory[ran].split("+")
    laser_values  = values[1].split(',')
    accept_thread.memory[ran] = ""
    length = len(laser_values)
    min_val,index_val = min_laser_val(laser_values)
    if flag == 1:
        level = 0.5
    else:
        level = 0.4

    #front checker.
    for i in range((length/2)-10,(length/2)+10):
        if float(laser_values[i]) <= 0.45 and fc == 0:
            fc = 1
            if index_val > length/2:
                listener.send_data("CMD!" + handle_movement("rotate_right", 0.3) + "#")
                side = 0
                break
            else:
                listener.send_data("CMD!" + handle_movement("rotate_left", 0.3) + "#")
                side = 1
                break
        elif float(laser_values[i]) <= 0.4 and fc == 1:
            break
        else :
            fc = 0
    if fc == 1 :
        continue
    fc = 0
    if min_val <= level:
        # If you get too close to the wall, you need to turn
        # away from it.
        # Checks the front.
        if min_val <= 0.30:
            # the most left value is 181
            if index_val > length/2:
                listener.send_data("CMD!" + handle_movement("rotate_right", 0.3) + "#")
                side = 1
                continue
            else :
                listener.send_data("CMD!" + handle_movement("rotate_left", 0.3) + "#")
                side = 0
                continue
                
        # If you get too far from the wall but the wall is still
        # close, go towards the wall again.
        if min_val >= 0.38 and min_val <= 0.43:
            if index_val > length/2:
                listener.send_data("CMD!" + handle_movement("rotate_left", 0.3) + "#")
                side = 0
                continue
            else:
                listener.send_data("CMD!" + handle_movement("rotate_right", 0.3) + "#")
                side = 1
                continue
        
        # Follow the wall.
        
        flag, side = wallfollow(min_val, index_val, length)
    else:
        # Find a wall.
        wallsearch.send_data("NEX!" + str(side) + "#")
        while accept_thread.memory[nex] == "":
            continue
        accept_thread.memory[nex] = ""
        flag, side = wallfollow(min_val, index_val, length)
