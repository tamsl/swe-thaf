#!/usr/bin/env python
#!/usr/bin/env python

from communicatorv2 import *
import socket
import re

current_values = ""
old_values = "-"
list = []
running = 1
message = ""
configreader = config_reader()
accept_thread = acceptor(running, list, "SNR", configreader.addresses)
accept_thread.setDaemon(True)
accept_thread.start()

# Method to retrieve the list of sonar values
def sonar_module(datastring):
    if datastring == "" or datastring == "+":
        return current_values
    split = datastring.split('+')
    datasplit = re.findall('\{[^\}]*\}|\S+', split[1])
    sonar_values = []
    values = split[0] + "+"
    for i in range(len(datasplit)):
        sonar_values.append(datasplit[i].replace('{Name F' + str(i+1)
                                            + ' Range ', ''))
        sonar_values[i] = sonar_values[i].replace('}', '')
        if float(sonar_values[i]) < 0:
            return current_values
        values += sonar_values[i] + ','
    values = values.rstrip(',')
    return values

while running:
    data = accept_thread.memory[0]
    string = data.split('\r\n')
    for i in range(len(string)):
        datasplit = re.findall('\{[^\}]*\}|\S+', string[i])
        if len(datasplit) > 10:
            if datasplit[2] == "{Type Sonar}":
                message = ""
                message = datasplit[1] + "+"
                for i in range(3, len(datasplit)):
                    message += str(datasplit[i])
    current_values = sonar_module(message)
    if current_values != old_values:
        old_values = current_values
    if current_values != "":
        while len(accept_thread.request_data) != 0:
            command = "RCV!SNR!" + str(current_values) + "#"
            configreader.connection(list, accept_thread.request_data[0]).send(
                                        command)
            accept_thread.request_data.pop(0)
