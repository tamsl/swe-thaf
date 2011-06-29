from movementsv2 import *
import string
import socket
import re

TCP_IP = '127.0.0.1'
TCP_PORT = 2001
BUFFER_SIZE = 1024
COLOR = ['Red', 'Yellow', 'Green', 'Cyan', 'White', 'Blue', 'Purple']
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
#DEMO:
# 1) green shirt
##s.send("INIT {ClassName USARBot.P2DX} {Location -2.2,2.6,1.8} {Name R1}\r\n")
# 2) chair 1, green shirt
##s.send("INIT {ClassName USARBot.P2DX} {Location -4.2,-0.5,1.8} {Rotation 0.0,0.0,1.555} {Name R1}\r\n")
# 3) red hair
##s.send("INIT {ClassName USARBot.P2DX} {Location -4.2,0.0,1.8} {Name R1}\r\n")
# 4) wall
##s.send("INIT {ClassName USARBot.P2DX} {Location 1.1,0.7,1.8} {Rotation 0.0,0.0,1.555} {Name R1}\r\n")
# 5) chair 2, table
##s.send("INIT {ClassName USARBot.P2DX} {Location 1.5,-0.2,1.8} {Name R1}\r\n")
# 6) table
##s.send("INIT {ClassName USARBot.P2DX} {Location 5.0,-1.5,1.8} {Rotation 0.0,0.0,2.1} {Name R1}\r\n")
# 7) person in transparent wall
##s.send("INIT {ClassName USARBot.P2DX} {Location 5.8,1.8,1.8} {Rotation 0.0,0.0,-1.555} {Name R1}\r\n")
# 8) red hair
##s.send("INIT {ClassName USARBot.P2DX} {Location -4.2,0.0,1.8} {Name R1}\r\n")

# Odometry values
x = []
y = []
theta = []
# Robot speed
current_speed = 1
# Stop robot at this level.
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
    #print sorted_sonar_vals[0]
    #print index_val
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

# Get sensor and laser data.
def getdata():
    data = s.recv(BUFFER_SIZE)
    string = data.split('\r\n')
    sonar_values = []
    for i in range(len(string)):
        datasplit = re.findall('\{[^\}]*\}|\S+', string[i])
##        print datasplit
        if len(datasplit) > 0:
            # Sensor message
            if datasplit[0] == "SEN":
                #print datasplit, "\r\n"
                typeSEN = datasplit[1].replace('{Type ', '')
                typeSEN = typeSEN.replace('}', '')
                if typeSEN.find("Time") != -1:
                    typeSEN = datasplit[2].replace('{Type ', '')
                    typeSEN = typeSEN.replace('}', '')
                # Odometry sensor
                if typeSEN == "Odometry":
                    odo_values = odometry_module(datasplit)
                    if odo_values == "Ik sta stil\r\n":
                        return 1
                    #print odo_values, "\r\n"
                    senvalues = datasplit[3].replace('{Pose ', '')
                    senvalues = senvalues.replace('}','')               
                if len(datasplit) > 2:
                    typeSEN2 = datasplit[2].replace('{Type ', '')
                    typeSEN2 = typeSEN2.replace('}', '')                    
                    # Range sensor
                    if typeSEN2 == "Sonar":
                        #print datasplit, "\r\n"
                        if len(datasplit) > 9:
                            # Only look forward for collisions using sensor 4 and 5.
##                            sonar_values.append(datasplit[6].replace('{Name F4 Range ', ''))
##                            sonar_values.append(datasplit[7].replace('{Name F5 Range ', ''))
##                            sonar_values[0] = sonar_values[0].replace('}', '')
##                            sonar_values[1] = sonar_values[1].replace('}', '')         
##                            print "sonar 4: ", sonar_values[0], "sonar 5: ", sonar_values[1], "\r\n"
                            # Look at all sensors for collisions.
                            for i in range(0, 8):
                                sonar_values.append(datasplit[i + 3].replace('{Name F' + str(i + 1) + ' Range ', ''))
                                sonar_values[i] = sonar_values[i].replace('}', '')     
##                                if i == 5:
##                                    print sonar_values[4],sonar_values[5]
                            print sonar_values
                            min_val, index_val = min_sonar_val(sonar_values)
                            print sonar_values[3], sonar_values[4]
                            verschil = abs(float(sonar_values[3]) - float(sonar_values[4]))
                            print verschil
                            print "dit is de min val: ", min_val
                            for i in range (0,8):
                                if float(sonar_values[3]) - float(sonar_values[4]) > 1.50:
                                    print verschil
                                    print "persoon voor je neus"
                                    print "na zoveel seconden gaan we botsen: ", calc_collision(min_val)
                                    if sonar_values[0] < sonar_values[7]:
                                        s.send(handle_movement("right", 1.0, 2.0))
                                        print "RECHTS"
                                    elif sonar_values[7] < sonar_values[0]:
                                        s.send(handle_movement("left", 2.0, 1.0))
                                        print "LINKS"
                                if(float(sonar_values[i]) <= level):
    ##                                if min_val <= 0.22:
    ##                                    s.send(handle_movement("reverse"))
    ##                                print "ik ga botsen"
                                    print sonar_values[3], sonar_values[4]
##                                    print sonar_values[6], sonar_values[7], sonar_values[0]
                                    if (sonar_values[6] or sonar_values[7]) < sonar_values[0]:
                                        s.send(handle_movement("left", 2.0, 1.0))
                                        print "linksaf slaan"
                                    elif (sonar_values[0] or sonar_values[1]) < sonar_values[7]:
                                        s.send(handle_movement("right", 1.0, 2.0))
                                        print "rechtsaf slaan"
                                    if (index_val == 3 or index_val == 4) and flag == 0:
##                                        print sonar_values[4], sonar_values[5]
                                        print "persoon voor ons neus"
                                        print "na zoveel seconden gaan we botsen: ", calc_collision(min_val)
                                        if sonar_values[0] < sonar_values[7]:
                                            s.send(handle_movement("right", 1.0, 2.0))
                                            print "rechtsaf slaan"
                                        elif sonar_values[7] < sonar_values[0]:
                                            s.send(handle_movement("left", 2.0, 1.0))
                                            print "linksaf slaan"
##                                    if sonar_values[7] > level:
##                                        s.send(handle_movement("brake"))
                                    return 1
##                            if (index_val == 4 or index_val == 5) and flag == 0:
##                                print "na zoveel seconden gaan we botsen: ", calc_collision(min_val)
    return 0
 
##s.send(handle_movement("brake",2.0))
flag = 0 
while flag == 0:
    # Move forward if there is no collision.
    s.send(handle_movement("forward", 1.0))
    flag = getdata()
while 1:
    getdata()
    
##sonar_data = []
##odometry_data = []
## currentspeed moeten we ophalen.   
##current_speed = 2 
##d = 16.50
##print calc_speed()
##print calc_collision()

##handle_movement("right")
##handle_movement("left")
##handle_movement("brake")
##handle_movement("reverse")


##if calc_collision() <= 4 and front_ir <= 1.5 :
####  stuur bericht naar de movement dat de speed omlaag moet
##    current_speed /2
##    handle_movement("forward", 5.0, 5.0)
