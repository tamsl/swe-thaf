import socket
import re
import threading
import time
import sys
import errno

class listener(threading.Thread):
    def __init__(self,list, flag):
        threading.Thread.__init__(self)
        self.list = list
        self.flag = flag
    def add_to_list(connection):
        self.list.append(connection)
    def setflag(self,flag):
        self.flag = flag
        
    def run(self):
##        print list
##        list = ""
        print ("ik ben binnen")
##        print list
        while 1:
            time.sleep(0.1)
            data = ""
##            print("wat wat in de butt")
##            print(self.list)
##            print(self.flag)
            if(len(self.list) == 0):
                print("ik ben leeg")
                time.sleep(0.1)
##            if self.flag == 1:
##                print("omg flag is 1")
##                break
            for i in range(len(self.list)):
                try:
                    print("lijst niet meer leeg")
                    data = self.list[i][0].recv(1024)
                    print("data ontvangen")
                    datasplit = data.split(" ")
                    print("bericht ontvangen")
                    print(data)
                    print(datasplit)
                    if not data:
                        self.list.pop(i)
                    if(datasplit[0] == "REQ"):
                        self.list[i][0].send("bla")
                        datasplit[0] = ''
                except (socket.error):
                    if self.flag  == 1:
                        print ("blaat")
                        break
                    continue
        


class acceptor(threading.Thread):
    def __init__(self, list, flag, module, addresses):
        threading.Thread.__init__(self)
        self.list = list
        self.flag = flag
        self.module = module
        self.addresses = addresses
    def setflag(self,flag):
        print("flag is set")
        self.flag = flag
        print self.flag
    def run(self):
        for i in range(len(self.addresses)):        
            if(self.addresses[i][0] == self.module):
                TCP_IP = self.addresses[i][1]
        TCP_PORT = 2000
        BUFFER_SIZE = 1024
        # Server test.
        print("ik ga nu socket aanmaken")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((TCP_IP, TCP_PORT))
        s.listen(0)
        s.setblocking(0)
        thread1 = listener(self.list, self.flag)
        thread1.start()
        print("socketmade")
        print(self.list)
        while 1:
            try:
                connection = s. accept()
                print("connection accepted")
                print(connection)
                connection[0].setblocking(0)
                print("gaat hij hier dood")
                self.list.append(connection)
                thread1.add_to_list(connection)
                print ("acceptor" + self.flag)
                if self.flag == 1:
                    break
            except(socket.error):
                if self.flag  == 1:
                    print ("blaat")
                    break
                continue
            except:
                print(self.flag)
                self.flag = 1
                print(self.flag)
                print("flag zou 1 moeten zijn")
                break
                thread1.join()
                for i in range(self.list.size):
                    list[i].close()
                s.close()
                sys.exit()
                
            
        ##    conn.send("bla")
        ##    print("done send")
        ##    data = conn.recv(BUFFER_SIZE)
        ##    print data
        thread1.setflag(1)
        print("ik ga de thread sluiten")
        thread1.join()
        s.close()
        sys.exit()

class config_reader():
    def __init__(self):
        f = open('config')
        addresses = []
        config = f.readlines()
        for i in range(len(config)):
            config[i] = config[i].strip()
            addresses.append(config[i].split(' '))
        self.addresses = addresses
            
    def connection(self, list, module):
        print("bla")
        for i in range(len(list)):
            for i in range(len(self.addresses)):
                address = socket.gethostbyname_ex(self.addresses[i][1])
                if list[i][1][0] == address[2][0]:
                    return list[i][0]
        for i in range(len(self.addresses)):
            print("searching")
            print(self.addresses[i])       
            if(self.addresses[i][0] == module):
                while 1:
                    try:
                        print("adres gevonden")
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.connect((self.addresses[i][1], int(self.addresses[i][2])))
                        address = socket.gethostbyname_ex(self.addresses[i][1])
                        list.append((s, (address[2][0], int(self.addresses[i][2]))))
                        return s
                    except EnvironmentError as exc:
                        if exc.errno == errno.ECONNREFUSED:
                            print 'trying again in 10 seconds\n\r'
                            time.sleep(10)
                        else:
                            raise
                    else:
                        break

