# This is the test module that is specially made for the the wallfollower.
# It's simular to the original with one change: all the methods get a socket
# We use relative tresholds, because the range scanneer doesn't always give
# the same amount of values.
import string
import socket
import re

BUFFER_SIZE = 1024

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
##    print string
    return string

def go_trace(b1, in1, COLOR):
    b1 = str(b1)
    in1 = str(in1)
    string = "Trace {On " + b1 + "} {Interval " + in1 + "} {Color " + COLOR +"}\r\n"
##    print string
    return string

def go_rotate(s1):
    s1 = str(s1)
    string = "DRIVE {RotationalVelocity " + s1 + "}"
##    print string
    return string

# Method to change all string in an array to a float.
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
    #print sorted_laser_vals[0]
    #print index_val
    return sorted_laser_vals[0], index_val

# Method to parse the odometry values.
def odometry_module(datastring):
    senvalues = datastring[3].replace('{Pose ', '')
    senvalues = senvalues.replace('}','')
    odo_values = senvalues.split(',')
    return odo_values

# Method to find the smallest value by driving in circles and then saving
# the smallest value you find.
def turn_360(odo_values, s):
    print odo_values
    x = odo_values[0]
    y = odo_values[1]
    theta = odo_values[2]
    # we always trun left while searching for a wall
    s.send(handle_movement("rotate_left", -1.5, 1.0))
    # to prevent the use of false values.
    new_odo_values = [999, 999, 999]
    temp_min_val = 10000
    temp_index_val = 0
    temp_odo_values = [999, 999, 999]
    previous_odo_values = [999, 999, 999]
    flag = 0
    while(1):
        data = s.recv(BUFFER_SIZE)
        string = data.split('\r\n')
        sonar_values = []
        #print temp_odo_values
        for i in range(len(string)):
            datasplit = re.findall('\{[^\}]*\}|\S+', string[i])
            if len(datasplit) > 0:
                # Sensor message
                if datasplit[0] == "SEN":
                    #print datasplit, "\r\n"
                    typeSEN = datasplit[1].replace('{Type ', '')
                    typeSEN = typeSEN.replace('}', '')
                    # Odometry sensor
                    if typeSEN == "Odometry":
                        #print datasplit
                        new_odo_values = string_to_float(odometry_module(datasplit))
                        #print new_odo_values, "\r\n"
                        if new_odo_values[2] > previous_odo_values[2]:
                            if flag == 2:
                                s.send(handle_movement("brake", 0.0, 0.0))
                                print "De kleinste min value gevonden"
                                turn_right_position(temp_min_val, temp_index_val, temp_odo_values, s)
                                return 1#placeholder wallfollow
                            flag = 1
                        if flag == 1 and new_odo_values[2] <  0:
                            flag = 2
                        previous_odo_values = new_odo_values
                    if len(datasplit) > 2:
                        typeSEN2 = datasplit[2].replace('{Type ', '')
                        typeSEN2 = typeSEN2.replace('}', '')
                        # Range sensor
                        if typeSEN2 == "RangeScanner":
                            #print datasplit, "\r\n"
                            if len(datasplit) > 7:
                                # puts all RangeScanner values in an array.
                                laser_values = re.findall('([\d.]*\d+)', datasplit[7])
                                #print laser_values
                                #print len(laser_values)
                                min_val, index_val = min_laser_val(laser_values)
                                print min_val
                                # the relative thresholds
                                middle = len(laser_values)/2
                                treshold = len(laser_values)/20
                                if index_val <= middle+treshold and index_val >= middle -treshold:
                                    if min_val < temp_min_val:
##                                        print min_val
##                                        print index_val
##                                        print 'minimum waarde'
                                        temp_min_val = min_val
                                        temp_index_val = index_val
                                        temp_odo_values = new_odo_values
# Method to trun to the smallest value that was found in turn_360.
def turn_right_position(min_val, index_val, odo_values, s):
    # The robot always stops when the odometry is maximal.
    # we turn right when the values are smaller than PI otherwise we turn
    # left.
    if odo_values[2] < 0:
        s.send(handle_movement("rotate_right", 1.0, -1.5))
    else:
        s.send(handle_movement("rotate_left", -1.5, 1.0))
    # To prevent the use of false values.
    new_odo_values = [999, 999, 999]
    previous_odo_values = [999, 999, 999]
    flag = 0
    print "ik ga nu naar de goede waarde draaien"
    while(1):
        data = s.recv(BUFFER_SIZE)
        string = data.split('\r\n')
        sonar_values = []
        for i in range(len(string)):
            datasplit = re.findall('\{[^\}]*\}|\S+', string[i])
            if len(datasplit) > 0:
                # Sensor message
                if datasplit[0] == "SEN":
                    #print datasplit, "\r\n"
                    typeSEN = datasplit[1].replace('{Type ', '')
                    typeSEN = typeSEN.replace('}', '')
                    # Odometry sensor
                    if typeSEN == "Odometry":
                        #print datasplit
                        new_odo_values = string_to_float(odometry_module(datasplit))
                        if(new_odo_values[2] < odo_values[2]):
                            # When the value is found stop.
                            s.send(handle_movement("brake", 0.0, 0.0))
                            print "De juiste positie gevonden"
                            # Drive forward.
                            s.send(handle_movement("forward", 1.0, 1.0))
                            stop(s)
                            print " turn to the right position",index_val
                            return
# Method which stops the robot when it has reached the wall.
def stop(s):
    print 'ik ben hier ik wil stoppen'
    # to prevent false values.
    min_val =  100000000
    while 1:
        data = s.recv(BUFFER_SIZE)
        string = data.split('\r\n')
        laser_values = []
        for i in range(len(string)):
            datasplit = re.findall('\{[^\}]*\}|\S+', string[i])
            if len(datasplit) > 0:
                if datasplit[0] == "SEN":
                    #print datasplit, "\r\n"
                    if len(datasplit) > 2:
                        typeSEN = datasplit[2].replace('{Type ', '')
                        typeSEN = typeSEN.replace('}', '')
                        # RangeScannner values
                        if typeSEN == "RangeScanner":
                            #print datasplit, "\r\n"
                            if len(datasplit) > 7:
                                laser_values = re.findall('([\d.]*\d+)', datasplit[7])
##                                print laser_values
                                min_val, index_val = min_laser_val(laser_values)
        print "minval in wallseatch ",min_val
        # The treshold.
        if min_val <= 0.3:
            print "De muur gevonden"
            s.send(handle_movement("brake", 0.0, 0.0))
            break
