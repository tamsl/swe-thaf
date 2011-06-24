# This is the test module that is specially made for the the wallfollower.
# It's simular to the original with one change: all the methods get a socket.
from communicatorv2 import *
from movementsv2 import *
import string
import socket
import re
import time

BUFFER_SIZE = 1024
current_vlaues = ""
list = []
running = 1
configreader = config_reader()
accept_thread = acceptor(running, list, "WSC", configreader.addresses)
accept_thread.setDaemon(True)
accept_thread.start()
odometry = configreader.connection(list, "ODO")
rangescanner = configreader.connection(list, "RSC")
listener = configreader.connection(list, "LIS")
wallfollow = configreader.connection(list, "WFW")
print ("acceptor thread gestart")
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
##    print sorted_laser_vals[0]
##    print index_val
    return sorted_laser_vals[0], index_val

# Method to parse the odometry values.
def odometry_module(datastring):
    senvalues = datastring[3].replace('{Pose ', '')
    senvalues = senvalues.replace('}','')
    odo_values = senvalues.split(',')
    return odo_values

# When the wall has just been lost see if the wall continues on the sides.

def wall_continued(side,s):
    # if side is 1 then the wall is on the right otherwise it's on the left side.
    laser_values = []
    odo_values  = []
    flag = 0
    data_incomplete = 0
    while 1:
       rangescanner.send("REQ!WSC#")
       accept_thread.waiting_for_data += 1
       #wait for data to arrive
       while accept_thread.waiting_for_data > 0 :
           continue
              
       laser_values  = accept_thread.memory[ran]
       min_val,index_val = min_laser_val(laser_values.split(','))

       # here is the logic of the wall continued
       # is going to let you make inner turns
       # Check if there's something nearby
       if min_val <= 0.62 :
           # turn towards the side where the min val is found
           # and return to wall follow
           if index_val > len(laser_values)/2:
                print"ik stuur bij naar rechts in cont"
                s.send(handle_movement("right", 4.0,2.0))
                return 1
           else :
                print"ik stuur bij naar links in cont"
                s.send(handle_movement("left", 4.0,2.0))
                return 1
       # if the index val is on the left side of the
       # robot
       if index_val > len(laser_values)/2 :
          #wall on the left so turn right
          print "waarde aan de linkerkant",laser_values[-1]
          if flag >= 0 :                                   
              s.send(handle_movement("left", 4.0,2.0))
          if flag >= 1 and min_val >= 1.2:
              if laser_values[-1] >= 1:
                 turn_360(odo_values,s)
                 wallfollow.send("NEX!0#")
          else:
              s.send(handle_movement("right", 4.0,2.0))
       else:
          #Wall on the right side turn right
          print "waarde aan de rechterkant" , laser_values[0]
          if flag >= 0 :
             #first turn a little
              s.send(handle_movement("right", 4.0,2.0))
              flag = 1
          if flag >= 1:
              # now look for a wall
              if laser_values[0] >=  1 and min_val >= 1.2:
                  turn_360(odo_values,s)
                  wallfollow.send("NEX!0#")
          else:
              s.send(handle_movement("right", 2.0,4.0))
       if min_val <= 0.35:
          wallfollow.send("NEX!1#")

# Method to find the smallest value by driving in circles and then saving
# the smallest value you find.
def turn_360(odo_values, s):
##    print odo_values
##    x = odo_values[0]
##    y = odo_values[1]
##    theta = odo_values[2]
    # we always turn left while searching for a wall
    
    s.send(handle_movement("rotate_left", 1.5))
    # To prevent the use of false values.
    new_odo_values = [999, 999, 999]
    temp_min_val = 10000
    temp_index_val = 0
    temp_odo_values = [999, 999, 999]
    previous_odo_values = [999, 999, 999]
    flag = 0
    while 1:
        rangescanner.send("REQ!WSC#")
        odometry.send("REQ!WSC#")
        accept_thread.waiting_for_data += 2
        #wait for data to arrive
        while accept_thread.waiting_for_data > 0 :
            continue
        laser_values  = accept_thread.memory[ran].split(',')
        new_odo_values  = accept_thread.memory[odo].split(',')
        if new_odo_values[2] > previous_odo_values[2]:
            if flag == 2:
                s.send(handle_movement("brake"))
                print "De kleinste min value gevonden"
                turn_right_position(temp_min_val, temp_index_val, temp_odo_values, s)
                #placeholder wallfollow
                return 0
            flag = 1
        if flag == 1 and new_odo_values[2] < 0:
            flag = 2
        previous_odo_values = new_odo_values
        min_val, index_val = min_laser_val(laser_values)
        print  "360", min_val
        # the relative thresholds
        middle = len(laser_values)/2
        threshold = len(laser_values)/40
        if index_val <= middle + threshold and index_val >= middle - threshold:
            if min_val < temp_min_val:
                print min_val
                print index_val
                print 'minimum waarde'
                print 'draaiing', new_odo_values[2]
                temp_min_val = min_val
                temp_index_val = index_val
                temp_odo_values = new_odo_values
                                        
# Method to turn to the smallest value that was found in turn_360.
def turn_right_position(min_val, index_val, odo_values, s):
    # The robot always stops when the odometry is maximal.
    # We turn right when the values are smaller than PI, otherwise we turn
    # left.
    print "turning to the right position"
    turning_right = 0
    if odo_values[2] < 0:
        s.send(handle_movement("rotate_right", 1.5))
        turning_right = 1
    else:
        s.send(handle_movement("rotate_left", 1.5))
    # To prevent the use of false values.
    new_odo_values = [999, 999, 999]
    previous_odo_values = [999, 999, 999]
    flag = 0
    data_incomplete = 0
    print "ik ga nu naar de goede waarde draaien"
    while 1:
        odometry.send("REQ!WSC#")
        accept_thread.waiting_for_data += 1
        #wait for data to arrive
        while accept_thread.waiting_for_data > 0 :
            continue
        new_odo_values  = accept_thread.memory[odo].split(',')
        print 'new_odo_values', new_odo_values
        print 'odo_values', odo_values
        print 'turning right', turning_right
        if ((new_odo_values[2] < odo_values[2] and turning_right == 0)
            or (new_odo_values[2] > odo_values[2] and turning_right == 1
                and new_odo_values[2] < 0)):
            # When the value is found stop.
            s.send(handle_movement("brake"))
            print "De juiste positie gevonden"
            # Drive forward.
            s.send(handle_movement("forward",1.0))
            stop(s)
##                            print "turn to the right position", index_val
            return
# Method which stops the robot when it has reached the wall.
def stop(s):
    print 'ik ben hier ik wil stoppen'
    # To prevent false values.
    min_val = 100000000
    data_incomplete = 0
    while 1:
        rangescanner.send("REQ!WSC#")
        accept_thread.waiting_for_data += 1
        #wait for data to arrive
        while accept_thread.waiting_for_data > 0 :
            continue
        laser_values  = accept_thread.memory[ran].split(',')
        min_val, index_val = min_laser_val(laser_values)
        print "in stop" ,min_val
##        print "minval in wallsearch ", min_val
                
        # The threshold.
        if min_val <= 0.40:
            print "De muur gevonden"
            s.send(handle_movement("brake"))
            return
