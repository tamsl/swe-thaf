from movementsv2 import *
import string
import socket
import re

TCP_IP = '127.0.0.1'
TCP_PORT = 2001
BUFFER_SIZE = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

#DEMO:
# Person in transparent wall.
s.send("INIT {ClassName USARBot.P2DX} {Location 5.8,1.8,1.8} {Rotation 0.0,0.0,-1.555} {Name R1}\r\n")
# Green shirt. 
##s.send("INIT {ClassName USARBot.P2DX} {Location -2.2,2.6,1.8} {Name R1}\r\n")
# Table.
##s.send("INIT {ClassName USARBot.P2DX} {Location 5.0,-1.5,1.8} {Rotation 0.0,0.0,2.1} {Name R1}\r\n")

# Odometry values.
x = []
y = []
theta = []
# Robot speed.
current_speed = 1
# Minimal distance between object and robot.
level = .315

# Calculate robot speed.
def calc_speed():
    v = (current_speed*0.1650)/2
    return v

# Calculate time to collision.
def calc_collision(value):
    c_t = value /calc_speed()
    return c_t

# Convert sonar values to floats.
def string_to_float(sonar_vals):
    float_sonar_vals = []
    for i in range(len(sonar_vals)):
        float_sonar_vals.append(float(sonar_vals[i]))
    return float_sonar_vals     

# Calculate smallest sonar value and the index of it.
def min_sonar_val(sonar_vals):
    sonar_vals = string_to_float(sonar_vals)
    sorted_sonar_vals = sorted(sonar_vals)
    index_val = sonar_vals.index(sorted_sonar_vals[0]) + 1
    return sorted_sonar_vals[0], index_val

# Determine whether the robot is moving or not.
def odometry_module(datastring):
    senvalues = datastring[3].replace('{Pose ', '')
    senvalues = senvalues.replace('}','')
    odo_values = senvalues.split(',')
    x.append(odo_values[0])
    y.append(odo_values[1])
    theta.append(odo_values[2])
    # Take 100 x, y and theta values.
    if len(x) == 100:
        # Sort odometry values.
        x.sort()
        y.sort()
        theta.sort()
        # Calculate absolute difference between smallest and biggest value.
        diff_x = abs(float(x[99]) - float(x[0]))
        diff_y = abs(float(y[99]) - float(y[0]))
        diff_theta = abs(float(theta[99]) - float(theta[0]))
        # I am not moving anymore if x and y not differ more than 0.2.
        if diff_x < 0.2 and diff_y < 0.2:
            string = "I'm standing still\r\n"
            print string
            return string
        # Empty odometry arrays.
        for i in range(0, len(x)):
            x.pop()
            y.pop()
            theta.pop()
    return odo_values

# Get sensor and laser data.
def getdata():
    data = s.recv(BUFFER_SIZE)
    string = data.split('\r\n')
    sonar_values = []
    for i in range(len(string)):
        datasplit = re.findall('\{[^\}]*\}|\S+', string[i])
        if len(datasplit) > 0:
            # Sensor message.
            if datasplit[0] == "SEN":
                typeSEN = datasplit[1].replace('{Type ', '')
                typeSEN = typeSEN.replace('}', '')
                if typeSEN.find("Time") != -1:
                    typeSEN = datasplit[2].replace('{Type ', '')
                    typeSEN = typeSEN.replace('}', '')
                # Odometry sensor.
                if typeSEN == "Odometry":
                    odo_values = odometry_module(datasplit)
                    if odo_values == "I'm standing still\r\n":
                        return 1
                    senvalues = datasplit[3].replace('{Pose ', '')
                    senvalues = senvalues.replace('}','')               
                if len(datasplit) > 2:
                    typeSEN2 = datasplit[2].replace('{Type ', '')
                    typeSEN2 = typeSEN2.replace('}', '')                    
                    # Range sensor.
                    if typeSEN2 == "Sonar":
                        if len(datasplit) > 9:
                            # Look at all sensors for collisions.
                            for i in range(0, 8):
                                sonar_values.append(datasplit[i + 3].replace('{Name F' + str(i + 1) + ' Range ', ''))
                                sonar_values[i] = sonar_values[i].replace('}', '')     
                            print sonar_values
                            min_val, index_val = min_sonar_val(sonar_values)
                            for i in range (0,8):
                                # Person in front if difference is greater than 1.50.
                                if abs(float(sonar_values[3]) - float(sonar_values[4])) > 1.50:
                                    print "Seconds before collision: ", calc_collision(min_val)
                                    # Check for leftside or rightside wall.
                                    if sonar_values[0] < sonar_values[7]:
                                        s.send(handle_movement("right", 1.0, 2.0))
                                    elif sonar_values[7] < sonar_values[0]:
                                        s.send(handle_movement("left", 2.0, 1.0))
                                # Sonar values small, expecting collision.        
                                if(float(sonar_values[i]) <= level):
                                    # Check for leftside or rightside wall.
                                    if (sonar_values[6] or sonar_values[7]) < sonar_values[0]:
                                        s.send(handle_movement("left", 2.0, 1.0))
                                    elif (sonar_values[0] or sonar_values[1]) < sonar_values[7]:
                                        s.send(handle_movement("right", 1.0, 2.0))
                                    # Object in front
                                    if (index_val == 3 or index_val == 4) and flag == 0:
                                        print "Seconds before collision: ", calc_collision(min_val)
                                        # Check for leftside or rightside wall.
                                        if sonar_values[0] < sonar_values[7]:
                                            s.send(handle_movement("right", 1.0, 2.0))
                                        elif sonar_values[7] < sonar_values[0]:
                                            s.send(handle_movement("left", 2.0, 1.0))
                                    return 1
    return 0

# Test the collision avoider module.
flag = 0 
while flag == 0:
    # Move forward if there is no collision.
    s.send(handle_movement("forward", 1.0))
    flag = getdata()
while 1:
    getdata()
