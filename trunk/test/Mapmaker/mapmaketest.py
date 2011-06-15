import CoreSLAM
import socket
import string
import re

TCP_IP = '127.0.0.1'
TCP_PORT = 2001
BUFFER_SIZE = 1024
COLOR = ['Red', 'Yellow', 'Green', 'Cyan', 'White', 'Blue', 'Purple']
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
#s.send("INIT {ClassName USARBot.P2DX} {Location 4.5,1.9,1.8} {Name R1}\r\n")
s.send("INIT {ClassName USARBot.P2DX} {Location 2.0,1.8,1.8} {Name R1}\r\n")
print("robot gemaakt")
x = []
y = []
theta = []
def string_to_float(sonar_vals):
    float_sonar_vals = []
    for i in range(len(sonar_vals)):
        float_sonar_vals.append(float(sonar_vals[i]))
    return float_sonar_vals     

def min_sonar_val(sonar_vals):
    sonar_vals = string_to_float(sonar_vals)
    sorted_sonar_vals = sorted(sonar_vals)
    index_val = sonar_vals.index(sorted_sonar_vals[0]) + 1
    #print sorted_sonar_vals[0]
    #print index_val
    return sorted_sonar_vals[0], index_val

def odometry_module(datastring):
    senvalues = datastring[3].replace('{Pose ', '')
    senvalues = senvalues.replace('}','')
    odo_values = senvalues.split(',')
    x.append(odo_values[0])
    y.append(odo_values[1])
    theta.append(odo_values[2])
    if len(x) == 100:
        print "\r\nx-waarde: ", x, "\r\n\r\ny-waarde: ", y, "\r\n\r\ntheta: ", theta
        x.sort()
        y.sort()
        theta.sort()
        print "\r\nsorted x: ", x, "\r\n"
        diff_x = abs(float(x[99]) - float(x[0]))
        print "kleinste x: ", x[0], "\r\ngrootste x: ", x[99], "\r\nverschil x: ", diff_x
        print "\r\nsorted y: ", y, "\r\n"
        diff_y = abs(float(y[99]) - float(y[0]))
        print "kleinste y: ", y[0], "\r\ngrootste y: ", y[99], "\r\nverschil y: ", diff_y
        print "\r\nsorted theta: ", theta, "\r\n"
        diff_theta = abs(float(theta[99]) - float(theta[0]))
        print "kleinste theta: ", theta[0], "\r\ngrootste theta: ", theta[99], "\r\nverschil theta: ", diff_theta
        for i in range(0, len(x)):
            x.pop()
            y.pop()
            theta.pop()
    return odo_values

def datahalen():
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
                print typeSEN
                if typeSEN == "Odometry":
                    #odo_values = odometry_module(datasplit)
                    #print odo_values, "\r\n"
                    senvalues = datasplit[3].replace('{Pose ', '')
                    senvalues = senvalues.replace('}','')
                    odo_values = senvalues.split(',')
                    print odo_values
                if typeSEN == "RangeScanner":
                    laser_values = re.findall('([\d.]*\d+)', datasplit[7])
                    
                if len(datasplit) > 2:
                    typeSEN2 = datasplit[2].replace('{Type ', '')
                    typeSEN2 = typeSEN2.replace('}', '')
                    # Range sensor
                    if typeSEN2 == "Sonar":
                        #print datasplit, "\r\n"
                        if len(datasplit) > 9:
                            for i in range(0, 8):
                                sonar_values.append(datasplit[i + 3].replace('{Name F' + str(i + 1) + ' Range ', ''))
                                sonar_values[i] = sonar_values[i].replace('}', '')
                                #print sonar_values, "\r\n"
                                min_val, index_val = min_sonar_val(sonar_values)
##Map = CoreSLAM.ts_map_init()
while 1:
    datahalen()
