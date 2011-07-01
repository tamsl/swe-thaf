# This is the test module that is specially made for the the wallfollower.
# It's simular to the original with one change: all the methods get a socket.
from communicatorv2 import *
from movementsv2 import *
import string
import socket
import re
import time

list = []
running = 1
configreader = config_reader()
accept_thread = acceptor(running, list, "WSC", configreader.addresses)
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
wallfollow = connection(running, "WFW", configreader, list)
wallfollow.setDaemon(True)
wallfollow.start()

print ("The acceptor thread is started.")
odo = 1
ran = 2
nex = 5

# Method to change all strings in an array to floats.
def string_to_float(vals):
    float_vals = []
    for i in range(len(vals)):
        float_vals.append(float(vals[i]))
    return float_vals

# Method to find the smallest value in an array of strings.
def min_laser_val(laser_vals):
    laser_vals = string_to_float(laser_vals)
    sorted_laser_vals = sorted(laser_vals)
    # index vals start from 1.
    index_val = laser_vals.index(sorted_laser_vals[0]) + 1
    return sorted_laser_vals[0], index_val

# Method to parse the odometry values.
def odometry_module(datastring):
    senvalues = datastring[3].replace('{Pose ', '')
    senvalues = senvalues.replace('}','')
    odo_values = senvalues.split(',')
    return odo_values

# When the wall has just been lost see if the wall continues on the sides.
def wall_continued(side):
    # if side is 1 then the wall is on the right otherwise it's on the left side.
    laser_values = []
    odo_values  = []
    flag = 1
    data_incomplete = 0
    values = []
    while 1:
        rangescanner.send_data("REQ!WSC#")
        accept_thread.set_wait(1)
        flag = 1
        #wait for data to arrive
        while accept_thread.get_wait() > 0 :
            if flag:
                flag = 0
            continue
        if len(values) > 0:
            if values[0] == accept_thread.memory[ran].split("+")[0]:
                continue
        values = accept_thread.memory[ran].split("+")
        laser_values  = values[1]
        min_val,index_val = min_laser_val(laser_values.split(','))

       # Here the logic of the wall is continued.
       # It is going to let you make inner turns.
       # Check if there's something nearby.
       if min_val <= 0.62 :
           # Turn towards the side where the min_val is found
           # and return to wall follow.
           if index_val > len(laser_values)/2:
                listener.send_data("CMD!" + handle_movement("right", 1.0,0.5) + "#")
                wallfollow.send_data("NEX!"+ str(1) +"#")
                return
            else :
                listener.send("CMD!" + handle_movement("left", 4.0,2.0) + "#")
                return 1
       # If the index_val is on the left side of the
       # robot
       if index_val > len(laser_values)/2 :
          #wall on the left so turn right
          if flag == 0 :                                   
              listener.send("CMD!" + handle_movement("left", 4.0,2.0) + "#")
          elif flag == 1:
              if laser_values[-1] >= 1:
                 turn_360(odo_values,s)
                 wallfollow.send("NEX!0#")
       else:
          #Wall on the right side turn right
          if flag == 0 :
             #first turn a little
              listener.send("CMD!" + handle_movement("right", 4.0,2.0) + "#")
              flag = 1
          elif flag == 1:
              # now look for a wall
              if laser_values[0] >=  1:
                  turn_360(odo_values,s)
                  wallfollow.send("NEX!0#")
       if min_val <= 0.35:
          wallfollow.send("NEX!1#")

# Method to find the smallest value by driving in circles and then saving
# the smallest value you find.
def turn_360(odo_values):
    # we always turn left while searching for a wall
    listener.send_data("CMD!" + handle_movement("rotate_left", 0.5) + "#")
    # To prevent the use of false values.
    new_odo_values = [999, 999, 999]
    temp_min_val = 10000
    temp_index_val = 0
    temp_odo_values = [999, 999, 999]
    previous_odo_values = [999, 999, 999]
    flag = 0
    rangescannervalues = []
    odometryvalues = []
    while 1:
        rangescanner.send_data("REQ!WSC#")
        odometry.send_data("REQ!WSC#")
        accept_thread.set_wait(2)
        # Wait for data to arrive
        while accept_thread.get_wait() > 0 :
            continue
        if len(rangescannervalues) > 0:
            if rangescannervalues[0] == accept_thread.memory[ran].split("+")[0]:
                continue
        if len(odometryvalues) > 0:
            if odometryvalues[0] == accept_thread.memory[odo].split("+")[0]:
                continue
        rangescannervalues = accept_thread.memory[ran].split("+")
        laser_values = rangescannervalues[1].split(',')
        odometryvalues = accept_thread.memory[odo].split('+')
        new_odo_values = odometryvalues[1].split(',')
        for i in range(len(new_odo_values)):
            new_odo_values[i] = float(new_odo_values[i])
        if new_odo_values[2] > previous_odo_values[2]:
            if flag == 2:
                listener.send_data("CMD!" + handle_movement("brake") + "#")
                turn_right_position(temp_min_val, temp_index_val,
                                    temp_odo_values)
                # Placeholder wallfollow
                return 0
            flag = 1
        if flag == 1 and new_odo_values[2] < 0:
            flag = 2
        previous_odo_values = new_odo_values
        min_val, index_val = min_laser_val(laser_values)
        # The relative thresholds
        middle = len(laser_values)/2
        threshold = len(laser_values)/40
        if index_val <= middle + threshold and index_val >= middle - threshold:
            if min_val < temp_min_val:
                temp_min_val = min_val
                temp_index_val = index_val
                temp_odo_values = new_odo_values
                                        
# Method to turn to the smallest value that was found in turn_360.
def turn_right_position(min_val, index_val, odo_values):
    # The robot always stops when the odometry is maximal.
    # We turn right when the values are smaller than PI, otherwise we turn
    # left.
    turning_right = 0
    if odo_values[2] < 0:
        listener.send_data("CMD!" + handle_movement("rotate_right", 0.5) + "#")
        turning_right = 1
    else:
        listener.send_data("CMD!" + handle_movement("rotate_left", 0.5) + "#")
    # To prevent the use of false values.
    new_odo_values = [999, 999, 999]
    previous_odo_values = [999, 999, 999]
    flag = 0
    values = []
    data_incomplete = 0
    while 1:
        odometry.send_data("REQ!WSC#")
        accept_thread.set_wait(1)
        # Wait for data to arrive
        while accept_thread.get_wait() > 0 :
            continue
        if len(values) > 0:
            if values[0] == accept_thread.memory[odo].split("+")[0]:
                continue
        values = accept_thread.memory[odo].split("+")
        new_odo_values  = values[1].split(',')
        for i in range(len(new_odo_values)):
            new_odo_values[i] = float(new_odo_values[i])
        if ((new_odo_values[2] < odo_values[2] and turning_right == 0)
            or (new_odo_values[2] > odo_values[2] and turning_right == 1
                and new_odo_values[2] < 0)):
            # When the value is found stop.
            listener.send_data("CMD!" + handle_movement("brake") + "#")
            # Drive forward.
            listener.send_data("CMD!" + handle_movement("forward",1.0) + "#")
            stop()
            return
# Method which stops the robot when it has reached the wall.
def stop():
    print 'ik ben hier ik wil stoppen'
    # To prevent false values.
    min_val = 100000000
    data_incomplete = 0
    values = []
    while 1:
        rangescanner.send_data("REQ!WSC#")
        accept_thread.set_wait(1)
        # Wait for data to arrive
        while accept_thread.get_wait() > 0 :
            continue
        if len(values) > 0:
            if values[0] == accept_thread.memory[ran].split("+")[0]:
                continue
        values = accept_thread.memory[ran].split("+")
        laser_values  = values[1]
        min_val,index_val = min_laser_val(laser_values.split(','))    
        # The threshold.
        if min_val <= 0.40:
            print "De muur gevonden"
            listener.send_data("CMD!" + handle_movement("brake") + "#")
            return

while running:
    while accept_thread.memory[nex] == "":
        continue
    side = float(accept_thread.memory[nex])
    wall_continued(side)
    accept_thread.memory[nex] = ""
odometry.close()
rangescanner.close()
listener.close()
wallfollow.close()
