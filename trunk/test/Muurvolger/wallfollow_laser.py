import string
import socket
import re

TCP_IP = '127.0.0.1'
TCP_PORT = 2001
BUFFER_SIZE = 1024
COLOR = ['Red', 'Yellow', 'Green', 'Cyan', 'White', 'Blue', 'Purple']
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send("INIT {ClassName USARBot.P2DX} {Location -3.0,4.0,1.8} {Name R1}\r\n")
# Odometry values
x = []
y = []
theta = []

# The partial movement handler contains all sorts of possible movements.
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

# Method to drive forward and backwards, make turns and rotations.
def go_drive(s1, s2):
    s1 = str(s1)
    s2 = str(s2)
    string = "DRIVE {Left " + s1 + "} {Right " + s2 + "}\r\n"
    #print string
    return string

# Method to make rotations.
def go_trace(b1, in1, COLOR):
    b1 = str(b1)
    in1 = str(in1)
    string = "Trace {On " + b1 + "} {Interval " + in1 + "} {Color " + COLOR +"}\r\n"
    #print string
    return string

# Method to convert strings to floats.
def string_to_float(laser_vals):
    float_laser_vals = []
    for i in range(len(laser_vals)):
        float_laser_vals.append(float(laser_vals[i]))
    return float_laser_vals   

# Finds the smallest value from the rangescanner sensor data and return the index
# on which this value was found.
def min_laser_val(laser_vals):
    laser_vals = string_to_float(laser_vals)
    sorted_laser_vals = sorted(laser_vals)
    index_val = laser_vals.index(sorted_laser_vals[0]) + 1 
    return sorted_laser_vals[0], index_val

# Test method for driving towards a located wall.
def wallsearch(min_val, index_val, length):
    print "dit is de min val" ,min_val
    # If the wall is on the left side of the robot, turn left.
    if index_val in range(length/4):
        s.send(handle_movement("left", -1.0, 1.0))

    # If the wall is on the right side of the robot, turn right.
    elif index_val in range(3*length/4, length):
        s.send(handle_movement("right", 1.0, -1.0))

    # Else go straight.
    else:
        s.send(handle_movement("forward", 1.0, 1.0))
    return 0

# Method for following a wall.
def wallfollow(min_val, index_val, length):
    # Rotate to the left so you have the wall on the left or right side of the
    # robot.
    s.send(handle_movement("rotate_left", -1.5, 1.0))
    while index_val not in range(length/5)and index_val not in range(5*length/5, length ):
        data = s.recv(BUFFER_SIZE)
        string = data.split('\r\n')
        laser_values = []
        for i in range(len(string)):
            datasplit = re.findall('\{[^\}]*\}|\S+', string[i])
            if len(datasplit) > 2:
               # Laser sensor
               typeSEN2 = datasplit[2].replace('{Type ', '')
               typeSEN2 = typeSEN2.replace('}', '')    
               if typeSEN2 == "RangeScanner":
                  if len(datasplit) > 7:
                     laser_values = re.findall('([\d.]*\d+)', datasplit[7])
##                     print "in wallfollow" ,laser_values, "\r\n"              
                     # Find the smallest value to see if the wall is on a side.
                     min_val, index_val = min_laser_val(laser_values)
                     
##    print "ik ga nu een muur volgen"
    # Go forward following the wall when the left or the right side is facing
    # the wall.
    s.send(handle_movement("forward", 1.0, 1.0))
    # Return that it is now following the wall.
    return 1

# Method that shows if the robot is standing still.
def odometry_module(datastring):
    senvalues = datastring[3].replace('{Pose ', '')
    senvalues = senvalues.replace('}','')
    odo_values = senvalues.split(',')
    x.append(odo_values[0])
    y.append(odo_values[1])
    theta.append(odo_values[2])
    # Take 100 x, y and theta values.
    if len(x) == 100:
##        print "\r\nx-waarde: ", x, "\r\n\r\ny-waarde: ", y, "\r\n\r\ntheta: ", theta
        # Sort odometry values.
        x.sort()
        y.sort()
        theta.sort()
        # Calculate absolute difference between smallest and biggest value.
        diff_x = abs(float(x[99]) - float(x[0]))
        diff_y = abs(float(y[99]) - float(y[0]))
        diff_theta = abs(float(theta[99]) - float(theta[0]))
##        print "\r\nsorted x: ", x, "\r\n"
##        print "kleinste x: ", x[0], "\r\ngrootste x: ", x[99], "\r\nverschil x: ", diff_x
##        print "\r\nsorted y: ", y, "\r\n"
##        print "kleinste y: ", y[0], "\r\ngrootste y: ", y[99], "\r\nverschil y: ", diff_y
##        print "\r\nsorted theta: ", theta, "\r\n"
##        print "kleinste theta: ", theta[0], "\r\ngrootste theta: ", theta[99], "\r\nverschil theta: ", diff_theta
        # I am not moving anymore if x and y not differ more than 0.2
        if diff_x < 0.2 and diff_y < 0.2:
            string = "Ik sta stil\r\n"
            print string
            return string
        # Empty odometry arrays.
        for i in range(0, len(x)):
            x.pop()
            y.pop()
            theta.pop()
    return odo_values

# Main            
flag = 0 
while 1:
    data = s.recv(BUFFER_SIZE)
    string = data.split('\r\n')
    laser_values = []
    for i in range(len(string)):
        datasplit = re.findall('\{[^\}]*\}|\S+', string[i])
        if len(datasplit) > 2:
##            print datasplit, "\r\n"
            # Odometry sensor
##            typeSEN = datasplit[1].replace('{Type ', '')
##            typeSEN = typeSEN.replace('}', '')
##            if typeSEN == "Odometry":
##                #odo_values = odometry_module(datasplit)
            # Laser sensor
            typeSEN2 = datasplit[2].replace('{Type ', '')
            typeSEN2 = typeSEN2.replace('}', '') 
            if typeSEN2 == "RangeScanner":
                if len(datasplit) > 7:
                    laser_values = re.findall('([\d.]*\d+)', datasplit[7])
                    print len(laser_values)
                    print "in main loop" , laser_values, "\r\n"              
                    min_val, index_val = min_laser_val(laser_values)
                    length = int(len(laser_values))
                    # The threshold for finding the wall changes when it is following a wall.
                    if flag == 1 :
                        level = 0.37
                    else:
                        level = 0.25

                    if min_val <= level:
##                        if min_val >= 0.4 and index_val in range(length):
##                            print "ik ga nu draaien"
##                            s.send(handle_movement("left", 1.0, -1.0))
##                        else:
                        # If you get too close to the wall, you need to turn away from it.
                        if min_val <= 0.1:
                            if index_val > length/2:
                                s.send(handle_movement("left", -1.0, 1.0))
                            else:
                                s.send(handle_movement("right", 1.0, -1.0))
                        # If you get to far from the wall but the wall is still
                        # close, go towards the wall again.
                        if min_val >= 0.28 and min_val <= 0.32:
##                            print "ik ben te ver van de muur ik ga bij sturen"
                            if index_val > length/2:
                                s.send(handle_movement("right", 1.0, -1.0))
                            else:                             
                                s.send(handle_movement("left", -1.0, 1.0))

                        # Follow the wall.
                        flag = wallfollow(min_val, index_val, len(laser_values))
                    else:
                        # Find a wall.
                        flag = wallsearch(min_val, index_val, len(laser_values))
