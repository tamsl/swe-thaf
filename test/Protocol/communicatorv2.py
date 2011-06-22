# author: Chris Bovenschen
# version: 2.3

import threading
import socket
import errno
import time
import sys

class config_reader():
    # constructor
    def __init__(self):
        f = open('config.cfg')
        addresses = []
        config = f.readlines()
        # Read the config.cfg file into an array. And split the values.
        for i in range(len(config)):
            config[i] = config[i].strip()
            addresses.append(config[i].split(' '))
        self.addresses = addresses

    def connection(self, list, module):
        # Look for the address of the requested module and get its ip address
        for i in range(len(self.addresses)):
            if self.addresses[i][0] == module:
                address = self.addresses[i]
                ip = socket.gethostbyname_ex(address[1])
        # Look in the list if the connection with the requested module has
        # already been made with this module if so return that connection
        # instead of making a new connection
        for i in range(len(list)):
            # Check if the ip address of a connection in the list is the same as
            # that of the ip address of the requested module.
            if list[i][1][0] == ip[2][0]:
                return list[i][0]
        # If the connection hasn't been made yet make a connection by reading
        # what port should be used and then making a connection to the address
        # of that module using the found port number.
##        connection_attempts = 0
        while 1:
            # Try to make the connection.
            try:
                print address
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((address[1], int(address[2])))
                list.append((s, (ip[2][0], int(address[2]))))
##                if(connection_attempts > 0):
##                    time.sleep(3)
                return s
            # If it is refused try again after 10 seconds.
            except EnvironmentError as exc:
                if exc.errno == errno.ECONNREFUSED:
##                    continue
##                    connection_attempts += 1
##                    print connection_attempts
                    print 'trying again in 10 seconds\n\r'
                    time.sleep(10)
                else:
                    raise

class communication(threading.Thread):
    def __init__(self, list, running, memory, waiting_for_data, request_data):
        threading.Thread.__init__(self)
        self.list = list
        self.running = running
        # array with the received data:
        # [0]: sonar
        # [1]: odometry
        # [2]: rangescanner
        # [3]: map
        # [4]: command
        self.memory = memory
        self.waiting_for_data = waiting_for_data
        self.request_data = request_data
    # add connection to list
    def add_to_list(connection):
        self.list.append(connection)
    # main
    def run(self):
        BUFFER_SIZE = 1024
        data = ""
        data_incomplete = 0
        while self.running:
##            time.sleep(0.1)
            # if there are no connections do nothing for 0.1 second and try again
            if(len(self.list) == 0):
                time.sleep(0.1)
            # check for all connections in sequence if they give any data and if
            # they do read it
            for i in range(len(self.list)):
                while 1:
                    try:
                        data = self.list[i][0].recv(BUFFER_SIZE)
                        if data_incomplete:
                            datatemp += data
                            data_incomplete = 0
                            data = datatemp
                        if data[len(data)-1] != '#':
                            datatemp = data
                            data_incomplete = 1
                            continue
                        messagesplit = data.split("#")
                        print "data"
                        print data
                        for j in range(len(messagesplit)):
                            print "messagesplit[" + str(j) + "]"
                            print messagesplit[j]
                            datasplit = messagesplit[j].split("!")
                            print "datasplit"
                            print datasplit
                            # connection is closed if the data received is equal to
                            # nothing
                            if not data:
                                self.list.pop(i)
                            if len(datasplit) < 1:
                                continue
                            # handles messages according to our protocol
                            # handles data requests
                            if(datasplit[0] == "REQ"):
                                self.request_data.append(datasplit[1])
                                data = ""
                                datasplit = []
                            # handles commands
                            elif(datasplit[0] == "CMD"):
                                self.memory[4] = datasplit[1]
                                data = " "
                                datasplit = []
                            # handles received data
                            elif(datasplit[0] == "RCV"):
                                if(datasplit[1] == "SNR"):
                                    self.memory[0] = datasplit[2]
                                    if(self.waiting_for_data > 0):
                                        self.waiting_for_data -= 1
                                    data = ""
                                    datasplit = []
                                if(datasplit[1] == "ODO"):
                                    self.memory[1] = datasplit[2]
                                    if(self.waiting_for_data > 0):
                                        self.waiting_for_data -= 1
                                    data = ""
                                    datasplit = []
                                if(datasplit[1] == "RSC"):
                                    self.memory[2] = datasplit[2]
                                    if(self.waiting_for_data > 0):
                                        self.waiting_for_data -= 1
                                    data = ""
                                    datasplit = []
                                if(datasplit[1] == "MAP"):
                                    self.memory[3] = datasplit[2]
                                    if(self.waiting_for_data > 0):
                                        self.waiting_for_data -= 1
                                    data = ""
                                    datasplit = []
                        break
                    except(socket.error):
                        if self.running == 0:
                            break
            

class acceptor(threading.Thread):
    # constructor
    def __init__ (self, running, list, module, addresses):
        threading.Thread.__init__(self)
        self.running = running
        self.list = list
        self.module = module
        self.addresses = addresses
        # array with the received data:
        # [0]: sonar
        # [1]: odometry
        # [2]: rangescanner
        # [3]: map
        # [4]: command
        self.memory = ["","","","",""]
        self.waiting_for_data = 0
        self.request_data = []
    # main
    def run(self):
        time.sleep(5)
        # find what IP address and port this module uses to connect to the other
        # modules
        for i in range(len(self.addresses)):
            if self.addresses[i][0] == self.module:
                TCP_IP = self.addresses[i][1]
                TCP_PORT = int(self.addresses[i][2])
        BUFFER_SIZE = 1024
        # Start listening on the socket to accept connections.
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((TCP_IP, TCP_PORT))
        s.listen(0)
        s.setblocking(0)
        # Create the communication thread.
        communicationthread = communication(self.list, self.running, self.memory, self.waiting_for_data, self.request_data)
        communicationthread.setDaemon(True)
        communicationthread.start()
        # Continue till the flag is turned off and the program needs to shut
        # down
        while self.running:
            # Try to accept a connection.
            try:
                connection = s.accept()
                connection[0].setblocking(0)
                print 'voor append'
                self.list.append(connection)
                print 'na append'
            # If no noone tries to connect continue unless the flag is turned
            # off
            except(socket.error):
                if self.running == 0:
                    break
            # An error occured shut down the program by closing the connections
            # and joining the threads.
            except:
                self.running = 0
                for i in range(len(self.list)):
                    list[i][0].close()
                s.close()
                communicationthread.join()
                sys.exit()
