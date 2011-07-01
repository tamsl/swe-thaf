import CoreSLAM
import socket
import string
import re
import math

TCP_IP = '127.0.0.1'
TCP_PORT = 2002
BUFFER_SIZE = 4096
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send("INIT {ClassName USARBot.P2DX} {Location 2.5,1.9,1.8} {Name R1}\r\n")

x = []
y = []
theta = []
posX=0
posY=1
theta=2 # in degrees
# 8192
TS_SCAN_SIZE = 181
# 2048, number of pixels.
TS_MAP_SIZE = 1000
# 0.1, scales the pixels appropriately.
TS_MAP_SCALE = 50
# 4000
TS_DISTANCE_NO_DETECTION=5
TS_NO_OBSTACLE=65500
TS_OBSTACLE=0
TS_HOLE_WIDTH=600
CAMERASPAN = 180.0

def string_to_float(sonar_vals):
    float_sonar_vals = []
    for i in range(len(sonar_vals)):
        float_sonar_vals.append(float(sonar_vals[i]))
    return float_sonar_vals     

def min_sonar_val(sonar_vals):
    sonar_vals = string_to_float(sonar_vals)
    sorted_sonar_vals = sorted(sonar_vals)
    index_val = sonar_vals.index(sorted_sonar_vals[0]) + 1
    return sorted_sonar_vals[0], index_val

def min_laser_val(laser_vals):
    laser_vals = string_to_float(laser_vals)
    sorted_laser_vals = sorted(laser_vals)
    index_val = laser_vals.index(sorted_laser_vals[0]) + 1 
    return sorted_laser_vals[0], index_val


# Make the map.
Map = CoreSLAM.ts_map_init()
scans = []
pos = []
sonar_values = []
draw = 0
data_incomplete = 0
SCALE = 2
while 1:
    s.send("DRIVE {LEFT -1.0} {RIGHT 1.0}\r\n")
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
            # Sensor message.
            if datasplit[0] == "SEN":
                typeSEN = datasplit[1].replace('{Type ', '')
                typeSEN = typeSEN.replace('}', '')
                if len(datasplit) > 2:
                    typeSEN2 = datasplit[2].replace('{Type ', '')
                    typeSEN2 = typeSEN2.replace('}', '')
                if typeSEN2 == "RangeScanner":
                    # datasplit[6] contains data.
                    if len(datasplit) >= 6:
                        laser_values = re.findall('([\d.]*\d+)', datasplit[6])
                        min_vals, index_val = min_laser_val(laser_values)
                        print laser_values
                        if min <= 0.2 :
                            if index_val < len(laser_values) / 2:
                                s.send("DRIVE {LEFT -1.0} {RIGHT 1.0}\r\n")
                            else:
                                s.send("DRIVE {LEFT 1.0} {RIGHT -1.0}\r\n")
                        scans = [float(y) / SCALE for y in laser_values]
                        print scans
                if typeSEN == "Odometry":
                    senvalues = datasplit[3].replace('{Pose ', '')
                    senvalues = senvalues.replace('}','')
                    odo_values = senvalues.split(',')
                    pos = [float(x) for x in odo_values]
                    # Make the map twice as small.
                    pos[posY] = pos[posY] / SCALE
                    pos[posX] = pos[posX] / SCALE
                    pos[theta] = math.degrees(pos[theta])
                    # The map starts in the middle.
                    pos[posY] = pos[posY] + (TS_MAP_SIZE / (2.0 * TS_MAP_SCALE))
                    pos[posX] = pos[posX] + (TS_MAP_SIZE / (2.0 * TS_MAP_SCALE))

    if len(scans)!= 0 and len(pos)!= 0:
        print "Making map"
        CoreSLAM.makeMap(scans, pos, len(scans), Map)
        draw += 1
        if draw == 100:
            print "Drawing"
            CoreSLAM.drawMap(Map)
            draw = 0
        # Clean the values
        scans = []
        pos = []
