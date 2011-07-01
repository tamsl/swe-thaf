# This is the test module that is specially made for the the wallfollower.
# It's simular to the original with one change: all the methods get a socket.
import string
import socket
import re
import time

BUFFER_SIZE = 1024

# Movements handler
def handle_movement(type, *args):
   handlers = {"forward":         go_drive,
               "left":            go_drive,
               "right":           go_drive,
               "reverse":         go_drive,
               "brake":           go_drive,
               "rotate_left":     go_drive,
               "rotate_right":    go_drive,
               "rotate_robot":    go_rotate
              }
   return handlers[type](*args)

# Create drive instruction.
def go_drive(s1, s2):
    s1 = str(s1)
    s2 = str(s2)
    string = "DRIVE {Left " + s1 + "} {Right " + s2 + "}\r\n"
    return string

# Create rotate instruction.
def go_rotate(s1):
    s1 = str(s1)
    string = "DRIVE {RotationalVelocity " + s1 + "}"
    return string

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
    # Index_val starts at 1.
    index_val = laser_vals.index(sorted_laser_vals[0]) + 1
    return sorted_laser_vals[0], index_val

# Method to parse the odometry values.
def odometry_module(datastring):
    senvalues = datastring[3].replace('{Pose ', '')
    senvalues = senvalues.replace('}','')
    odo_values = senvalues.split(',')
    return odo_values

# When the wall is lost, check if the wall continues on the sides.
def wall_continued(side,s):
    # If side is 1 then the wall is on the right side, otherwise its on the left side.
    laser_values = []
    odo_values  = []
    flag = 0
    data_incomplete = 0
    while 1:
        # Makes sure the data is complete.
        data = s.recv(BUFFER_SIZE)
        if data_incomplete:
            datatemp += data
            data_incomplete = 0
            data = datatemp
        if data[len(data)-1] != '\n':
            datatemp = data
            data_incomplete = 1
            continue
        
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
                    odo_done = 1
                # Laser sensor
                typeSEN2 = datasplit[2].replace('{Type ', '')
                typeSEN2 = typeSEN2.replace('}', '')
                if typeSEN2 == "RangeScanner":
                    if len(datasplit) > 6:
                        laser_values = re.findall('([\d.]*\d+)', datasplit[6])
                        min_val, index_val = min_laser_val(laser_values)
                        # Check if there is a wall nearby.54
                        if min_val <= 0.62 :
                            # turn towards the side where the min val is found
                            # and return to wall follow
                            if index_val > len(laser_values)/2:
                                 print "Adjust to the right."
                                 s.send(handle_movement("right", 4.0,-2.0))
                                 return 1
                            else :
                                 print "Adjust to the left."
                                 s.send(handle_movement("left", -2.0,4.0))
                                 return 1
                        # If there's data
                        # They turn faster here to makes sure you wont be
                        # stuck in the same place.
                        if len(laser_values) != 0:
                            if index_val > len(laser_values)/2 :
                               # The wall is on the left side, turn right.
                               if flag == 0 :
                                   s.send("DRIVE {LEFT 2.0} {RIGHT -1.0}\r\n")
                                   flag = 1
                               if flag == 1: 
                                   if laser_values[-1] >=  1.5:
                                      turn_360(odo_values,s)
                                      return 0
                               else:
                                   s.send(handle_movement("right", 4.0,-2.0))
                            else:
                               # The wall on the right side, turn left.
                               if flag == 0 :
                                  # First turn a little.
                                   s.send(handle_movement("right", 4.0,-2.0))
                                   flag = 1
                               if flag >= 1:
                                   # When all fails look for a wall by turning
                                   # around.
                                   if laser_values[0] >= 1.5:
                                       turn_360(odo_values, s)
                                       return 0
                               else:
                                   s.send(handle_movement("right", -2.0,4.0))
                            if min_val <= 0.35:
                               return 1

# Method to find the smallest value by driving in circles and then saving
# the smallest value you find.
def turn_360(odo_values, s):
    # Always turn left while searching for a wall.
    s.send(handle_movement("forward", 10.0, 10.0))
    s.send(handle_movement("rotate_left", -1.5, 1.0))
    # To prevent the use of false values.
    new_odo_values = [999, 999, 999]
    temp_min_val = 10000
    temp_index_val = 0
    temp_odo_values = [999, 999, 999]
    previous_odo_values = [999, 999, 999]
    flag = 0
    data_incomplete = 0
    while 1:
        # makes sure the data is complete.
        data = s.recv(BUFFER_SIZE)
        if data_incomplete:
            datatemp += data
            data_incomplete = 0
            data = datatemp
        if data[len(data)-1] != '\n':
            datatemp = data
            data_incomplete = 1
            continue
        string = data.split('\r\n')
        for i in range(len(string)):
            datasplit = re.findall('\{[^\}]*\}|\S+', string[i])
            if len(datasplit) > 0:
                # Sensor message
                if datasplit[0] == "SEN":
                    typeSEN = datasplit[1].replace('{Type ', '')
                    typeSEN = typeSEN.replace('}', '')
                    # Odometry sensor
                    if typeSEN == "Odometry":
                        new_odo_values = string_to_float(odometry_module(datasplit))
                        if new_odo_values[2] > previous_odo_values[2]:
                            if flag == 2:
                                s.send(handle_movement("brake", 0.0, 0.0))
                                turn_right_position(temp_min_val, temp_index_val, temp_odo_values, s)
                                # Placeholder for wallfollow.
                                return 0
                            flag = 1
                        if flag == 1 and new_odo_values[2] < 0:
                            flag = 2
                        previous_odo_values = new_odo_values
                    if len(datasplit) > 2:
                        typeSEN2 = datasplit[2].replace('{Type ', '')
                        typeSEN2 = typeSEN2.replace('}', '')
                        # Range sensor
                        if typeSEN2 == "RangeScanner":
                            if len(datasplit) > 6:
                                # Put all RangeScanner values in an array.
                                laser_values = re.findall('([\d.]*\d+)', datasplit[6])
                                min_val, index_val = min_laser_val(laser_values)
                                # The relative thresholds.
                                middle = len(laser_values)/2
                                threshold = len(laser_values)/40
                                if index_val <= middle + threshold and index_val >= middle - threshold:
                                    if min_val < temp_min_val:
                                        temp_min_val = min_val
                                        temp_index_val = index_val
                                        temp_odo_values = new_odo_values
                                        
# Method to trun to the smallest value that was found in turn_360.
def turn_right_position(min_val, index_val, odo_values, s):
    # The robot always stops when the odometry is maximal.
    # We turn right when the values are smaller than PI, otherwise we turn
    # left.
    print "Turn to the right position."
    turning_right = 0
    if odo_values[2] < 0:
        s.send(handle_movement("rotate_right", 1.0, -1.5))
        turning_right = 1
    else:
        s.send(handle_movement("rotate_left", -1.5, 1.0))
    # To prevent the use of false values.
    new_odo_values = [999, 999, 999]
    previous_odo_values = [999, 999, 999]
    flag = 0
    data_incomplete = 0
    print "I will now turn to the right value."
    while 1:
        # makes sure the data is complete
        data = s.recv(BUFFER_SIZE)
        if data_incomplete:
            datatemp += data
            data_incomplete = 0
            data = datatemp
        if data[len(data)-1] != '\n':
            datatemp = data
            data_incomplete = 1
            continue
        string = data.split('\r\n')
        for i in range(len(string)):
            datasplit = re.findall('\{[^\}]*\}|\S+', string[i])
            if len(datasplit) > 0:
                # Sensor message
                if datasplit[0] == "SEN":
                    typeSEN = datasplit[1].replace('{Type ', '')
                    typeSEN = typeSEN.replace('}', '')
                    # Odometry sensor
                    if typeSEN == "Odometry":
                        new_odo_values = string_to_float(odometry_module(datasplit))
                        if ((new_odo_values[2] < odo_values[2] and turning_right == 0)
                            or (new_odo_values[2] > odo_values[2] and turning_right == 1
                                and new_odo_values[2] < 0)):
                            # Stop when the value is found.
                            s.send(handle_movement("brake", 0.0, 0.0))
                            print "The right position is found."
                            # Drive forward.
                            s.send(handle_movement("forward", 1.0, 1.0))
                            stop(s)
                            print "Turn to the right position."
                            return

# Method which stops the robot when it has reached the wall.
def stop(s):
    # To prevent false values.
    min_val = 100000000
    data_incomplete = 0
    while 1:
        # makes sure the data is complete. 
        data = s.recv(BUFFER_SIZE)
        if data_incomplete:
            datatemp += data
            data_incomplete = 0
            data = datatemp
        if data[len(data)-1] != '\n':
            datatemp = data
            data_incomplete = 1
            continue
        string = data.split('\r\n')
        laser_values = []
        for i in range(len(string)):
            datasplit = re.findall('\{[^\}]*\}|\S+', string[i])
            if len(datasplit) > 0:
                if datasplit[0] == "SEN":
                    typeSEN = datasplit[1].replace
                    # Odometry sensor
                    if typeSEN == "Odometry":
                        new_odo_values = string_to_float(odometry_module(datasplit))
                    if len(datasplit) > 2:
                        typeSEN = datasplit[2].replace('{Type ', '')
                        typeSEN = typeSEN.replace('}', '')
                        # RangeScannner values
                        if typeSEN == "RangeScanner":
                            if len(datasplit) > 6:
                                laser_values = re.findall('([\d.]*\d+)', datasplit[6])
                                min_val, index_val = min_laser_val(laser_values)
                                # The threshold.
                                if min_val <= 0.40:
                                    print "The wall is found."
                                    s.send(handle_movement("brake", 0.0, 0.0))
                                    return
