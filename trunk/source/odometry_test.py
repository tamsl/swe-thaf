#!/usr/bin/env python

import re

f = open('odometry_test.txt')
data = f.read()
string = data.split('\r\n')

def odometry_module(datastring):
  print datastring, "\r\n"
  senvalues = datastring[3].replace('{Pose ', '')
  senvalues = senvalues.replace('}','')
  odo_values = senvalues.split(',')
  print odo_values, "\r\n"
  return odo_values

for i in range(len(string)):
  datasplit = re.findall('\{[^\}]*\}|\S+', string[i])
  if len(datasplit) > 0:
    # Sensor message
    if datasplit[0] == "SEN":
      typeSEN = datasplit[1].replace('{Type ', '')
      typeSEN = typeSEN.replace('}', '')
      # Odometry sensor
      if typeSEN == "Odometry":
        odo_values = odometry_module(datasplit)
