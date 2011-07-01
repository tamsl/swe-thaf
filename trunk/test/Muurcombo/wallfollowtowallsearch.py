import string
import socket
import re
import wallsearching
import time

TCP_IP = '127.0.0.1'
TCP_PORT = 2001
BUFFER_SIZE = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

# Start positions

## DEMO:
## Start in hall.
##s.send("INIT {ClassName USARBot.P2DX} {Location 6.8,-1.8,1.8} {Name R1}\r\n")
## Hall with red haired person.
##s.send("INIT {ClassName USARBot.P2DX} {Location -3.5,-2.0,1.8} {Rotation 0.0,0.0,0.0} {Name R1}\r\n")
## Hall besides room with chair.
s.send("INIT {ClassName USARBot.P2DX} {Location -3.0,2.5,1.8} {Rotation 0.0,0.0,3.155} {Name R1}\r\n")

## Start in second hall.
##s.send("INIT {ClassName USARBot.P2DX} {Location 1.5,1.5,1.8} {Name R1}\r\n") 
## Start in room with chair.
##s.send("INIT {ClassName USARBot.P2DX} {Location -5.5,-1.0,1.8} {Name R1}\r\n")
## Standard value.
##s.send("INIT {ClassName USARBot.P2DX} {Location 4.5,1.9,1.8} {Name R1}\r\n")

# Movements handler
def handle_movement(type, *args):
   handlers = {"forward":         go_drive,
               "left":            go_drive,
               "right":           go_drive,
               "reverse":         go_drive,
               "brake":           go_drive,
               "rotate_left":     go_drive,
               "rotate_right":    go_drive
              }
   return handlers[type](*args)

# Create drive instruction
def go_drive(s1, s2):
    s1 = str(s1)
    s2 = str(s2)
    string = "DRIVE {Left " + s1 + "} {Right " + s2 + "}\r\n"
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

# Method for following a wall.
def wallfollow(min_val, index_val, length):
    # Rotate to the left so you have the wall on the left or right side of the
    # robot.
    # Side 1 is the wall on right side, otherwise the wall is on the left side.
    side = 0
    if index_val < length/2:
        s.send(handle_movement("rotate_left", -1.5, 1.0))
    else:
        s.send(handle_movement("rotate_right", 1.0, -1.5))
    data_incomplete = 0
    while index_val not in range(length/5) and index_val not in range(4*length/5, length):
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
               # Laser sensor
               typeSEN2 = datasplit[2].replace('{Type ', '')
               typeSEN2 = typeSEN2.replace('}', '')    
               if typeSEN2 == "RangeScanner":
                  if len(datasplit) > 6:
                     laser_values = re.findall('([\d.]*\d+)', datasplit[6])   
                     # Find the smallest value to see if the wall is on a side.
                     min_val, index_val = min_laser_val(laser_values)
                     
    print "I am now following a wall."
    # Go forward following the wall when the left or the right side is facing
    # the wall.
    if index_val > length/2:
        side = 1
    s.send(handle_movement("forward", 1.0, 1.0))
    # Return that it is now following the wall.
    return 1, side

# Get odometry values.
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
# The wall is on the left or right side
side = 0
# Front checker
fc = 0
while 1:
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
                    length = int(len(laser_values))
                    # The threshold for finding the wall changes when it is
                    # following a wall.
                    if flag == 1:
                        level = 0.5
                    else:
                        level = 0.4

                    if index_val > length/2:
                        print "The wall is on my left side."
                    else:
                        print "The wall is on my right side."
                    for i in range((length/2) - 10, (length/2) + 10):
                        if float(laser_values[i]) <= 0.45 and fc == 0:
                            if index_val > length/2:
                                print "Adjust to the right."
                                s.send(handle_movement("right", 2.0, -1.0))
                                fc = 1
                                break
                            else:
                                print "Adjust to the left."
                                s.send(handle_movement("left", -1.0, 2.0))
                                fc = 1
                                break
                        elif float(laser_values[i]) <= 0.4 and fc == 1:
                            break
                        else :
                            fc = 0
                    if fc == 1 :
                        break
                    fc = 0
                    if min_val <= level:
                        # Check the front.
                        if min_val <= 0.30:
                            print "I am too close to the wall, I will adjust."
                            right_val, right_index_val = min_laser_val(laser_values[:len(laser_values)/2])
                            left_val, left_index_val = min_laser_val(laser_values[len(laser_values)/2:])
                            if right_val <= 0.4 and left_val <= 0.4:
                               s.send(handle_movement("forward",1.0,1.0))
                               break
                            # The most left value is 80.
                            if index_val > length/2:
                                print "Adjust to the right."
                                s.send(handle_movement("right", 1.0,-1.0))
                                break
                            else :
                                print "Adjust to the left."
                                s.send(handle_movement("left", -1.0,1.0))
                                break
                                side = 1
                        # If you get too far from the wall but the wall is still
                        # close, go towards the wall again.
                        if min_val >= 0.38 and min_val <= 0.4:
                            print "I am too far away from the wall, I will adjust."
                            if index_val > length/2:
                                print "Adjust to the right."
                                s.send(handle_movement("left", -1.0, 1.0))
                                break
                            else:
                                print "Adjust to the left."
                                s.send(handle_movement("right", 1.0, -1.0))
                                break                 
                        # Follow the wall.                        
                        flag, side = wallfollow(min_val, index_val, length)
                    else:
                        if odo_done == 1:
                            # Find a wall.
                            print "I lost the wall and will find a new one."
                            flag = wallsearching.wall_continued(side, s)
                            flag, side = wallfollow(min_val, index_val, length)
