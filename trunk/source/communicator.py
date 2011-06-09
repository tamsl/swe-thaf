import socket
import re
import threading
import time
import sys

class listener(threading.Thread):
    def __init__(self,list, flag):
        threading.Thread.__init__(self)
        self.list = list
        self.flag = flag
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
                time.sleep(0.1)
            if self.flag == 1:
                break
            for i in range(len(self.list)):
                try:
                    data = self.list[i].recv(1024)
                except socket.error as err:
                    continue
                datasplit = data.split(" ")
                print("bericht ontvangen")
                print(data)
                print(datasplit)
                if(datasplit[0] == "REQ"):
                    self.list[i].send("bla")

class acceptor(threading.Thread):
    def __init__(self, list, flag):
        threading.Thread.__init__(self)
        self.list = list
        self.flag = flag
    def setflag(self,flag):
        print("flag is set")
        self.flag = flag
        print self.flag
    def run(self):
        TCP_IP = '127.0.0.1'
        TCP_PORT = 2044
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
                conn, address = s.accept()
                print("connection accepted")
                conn.setblocking(0)
                self.list.append(conn)
                print ("acceptor" + self.flag)
                if self.flag == 1:
                    break
            except(socket.error):
##                print("ik ga verder")
                if self.flag  == 1:
                    break
                continue
            except:
                print(self.flag)
                self.flag = 1
                print(self.flag)
                print("flag zou 1 moeten zijn2")
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

class config_reader():
    def __init__(self):
        f = open('config')
        config = f.readlines()
        for i in range(len(config)):
            config[i] = config[i].strip()
        self.config = config
            
    def connection(module):
        print("bla")
        adresses = config[i].split(' ')
        print("searching")
        for i in range(len(config)):
            if(adresses[i][0] == module):
                print("adres gevonden")
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                return adresses, s
            

                    
