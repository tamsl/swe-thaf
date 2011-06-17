import string
import socket
import re

TCP_IP = '127.0.0.1'
TCP_PORT = 2001
BUFFER_SIZE = 1024
COLOR = ['Red', 'Yellow', 'Green', 'Cyan', 'White', 'Blue', 'Purple']
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send("INIT {ClassName USARBot.P2DX} {Location 4.5,1.9,1.8} {Name R1}\r\n")

# The partial movement handler contains all sorts of possible movements.
def handle_movement(type, *args):
    handlers = {"forward":         go_drive,
                "left":            go_drive,
                "right":           go_drive,
                "reverse":         go_drive,
                "brake":           go_drive,
                "rotate_left":     go_drive,
                "rotate_right":    go_drive,
                "rotate_robot":    go_rotate,
               }
    return handlers[type](*args)

# Method to drive forward and backwards, make turns and rotations.
def go_drive(s1, s2):
    s1 = str(s1)
    s2 = str(s2)
    string = "DRIVE {Left " + s1 + "} {Right " + s2 + "}\r\n"
    print string
    return string

# Method to make rotations.
def go_rotate(s1):
    s1 = str(s1)
    string = "DRIVE {RotationalVelocity " + s1 + "}"
    print string
    return string

# Method to convert strings to floats.
def string_to_float(vals):
    float_vals = []
    for i in range(len(vals)):
        float_vals.append(float(vals[i]))
    return float_vals     

# Method to find the minimum value and its index value.
def min_sonar_val(sonar_vals):
    sonar_vals = string_to_float(sonar_vals)
    sorted_sonar_vals = sorted(sonar_vals)
    index_val = sonar_vals.index(sorted_sonar_vals[0]) + 1
    print sorted_sonar_vals[0]
    print index_val
    return sorted_sonar_vals[0], index_val

# Method to retrieve the list of odometry values.
def odometry_module(datastring):
    senvalues = datastring[3].replace('{Pose ', '')
    senvalues = senvalues.replace('}','')
    odo_values = senvalues.split(',')
    return odo_values

# Method to make a full rotation to determine the nearest wall in the robot's environment.
def turn_360(odo_values):
    x = odo_values[0]
    y = odo_values[1]
    theta = odo_values[2]
    new_odo_values = [999, 999, 999]
    temp_min_val = 10000
    temp_index_val = 0
    temp_odo_values = [999, 999, 999]
    previous_odo_values = [999, 999, 999]
    flag = 0

    s.send(handle_movement("rotate_left", -1.5, 1.0))
    while(1):
        data = s.recv(BUFFER_SIZE)
        string = data.split('\r\n')
        sonar_values = []
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
                                turn_right_position(temp_min_val, temp_index_val, temp_odo_values)
                            flag = 1
                        if flag == 1 and new_odo_values[2] <  0:
                            flag = 2
                        previous_odo_values = new_odo_values
                    if len(datasplit) > 2:
                        typeSEN2 = datasplit[2].replace('{Type ', '')
                        typeSEN2 = typeSEN2.replace('}', '')
                        # Range sensor
                        if typeSEN2 == "Sonar":
                            if len(datasplit) > 9:
                                for i in range(0, 8):
                                    sonar_values.append(datasplit[i + 3].replace('{Name F' + str(i + 1) + ' Range ', ''))
                                    sonar_values[i] = sonar_values[i].replace('}', '')
                                min_val, index_val = min_sonar_val(sonar_values)
                                # The robot is near a wall.
                                if min_val <= 0.2:
                                    s.send(handle_movement("brake", 0.0, 0.0))
                                if index_val == 5 or index_val == 4:
                                    # The latest minimum value is smaller than the old one.
                                    if min_val < temp_min_val:
                                        temp_min_val = min_val
                                        temp_index_val = index_val
                                        temp_odo_values = new_odo_values

# Method to rotate to the determined position.
def turn_right_position(min_val, index_val, odo_values):
    new_odo_values = [999, 999, 999]
    previous_odo_values = [999, 999, 999]
    flag = 0

    s.send(handle_movement("rotate_left", -1.5, 1.0))
    while(1):
        data = s.recv(BUFFER_SIZE)
        string = data.split('\r\n')
        sonar_values = []
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
                                print "The right position is found"
                                wallsearch(min_val, index_val)
                                return
                            flag = 1
                        if flag == 1 and new_odo_values[2] <  0:
                            flag = 2
                        previous_odo_values = new_odo_values

# Move to the nearest wall.
def wallsearch(min_val, index_val):
    print min_val
    if min_val <= 0.2:
        s.send(handle_movement("brake", 0.0, 0.0))
    else:
       if index_val == 1:
           print "Move to the wall on the left"
           s.send(handle_movement("rotate_left", -2.0, 2.0))
       elif index_val == 2:
           print "Move to the wall on the left"
           s.send(handle_movement("rotate_left", -1.5, 1.5))
       elif index_val == 3:
           print "Move to the wall on the left"
           s.send(handle_movement("rotate_left", -1.0, 1.0))
       elif index_val == 6:
           print "Move to the wall on the right"
           s.send(handle_movement("rotate_right", 1.0, -1.0))
       elif index_val == 7:
           print "Move to the wall on the right"
           s.send(handle_movement("rotate_right", 1.5, -1.5))
       elif index_val == 8:
           print "Move to the wall on the right"
           s.send(handle_movement("rotate_right", 2.0, -2.0))
       elif index_val == 4 or index_val == 5:
           print "Move to the wall in front"
           s.send(handle_movement("forward", 1.0, 1.0))

# Test the wallsearching for the sonar sensor.
while(1):
    data = s.recv(BUFFER_SIZE)
    string = data.split('\r\n')
    sonar_values = []
    for i in range(len(string)):
        datasplit = re.findall('\{[^\}]*\}|\S+', string[i]) 
        if len(datasplit) > 0:
            # Sensor message
            if datasplit[0] == "SEN":
                typeSEN = datasplit[1].replace('{Type ', '')
                typeSEN = typeSEN.replace('}', '')
                # Odometry sensor
                if typeSEN == "Odometry":
                    odo_values = string_to_float(odometry_module(datasplit))
                    print odo_values, "\r\n"
                    turn_360(odo_values)
