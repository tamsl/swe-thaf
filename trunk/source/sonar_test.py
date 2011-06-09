#!/usr/bin/env python

import re

f = open('sonar_test.txt')
data = f.read()

string = data.split('\r\n')
for i in range(len(string)):
  datasplit = re.findall('\{[^\}]*\}|\S+', string[i])
  if len(datasplit) > 0:
    # Sensor message
    if datasplit[0] == "SEN":
      if len(datasplit) > 2:
        typeSEN2 = datasplit[2].replace('{Type ', '')
        typeSEN2 = typeSEN2.replace('}', '')
        # Range sensor
        if typeSEN2 == "Sonar":
          print datasplit, "\r\n"
          if len(datasplit) > 9:
            sonar_values = []
            for i in range(0, 8):
              sonar_values.append(datasplit[i + 3].replace('{Name F' + str(i+1) + ' Range ', ''))
              sonar_values[i] = sonar_values[i].replace('}', '')
            print sonar_values, "\r\n"
