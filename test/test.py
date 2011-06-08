#!/usr/bin/env python

import socket
import re

location = [["Sonar", "127.0.0.1", 2101]]
location.append(["IR", "127.0.0.1", 2102])

print location[0][0]
f = open('config')
config = f.readlines()
for i in range(len(config)):
    config[i] = config[i].strip()
print config
