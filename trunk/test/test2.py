import socket
import re
import threading
import time
import sys

class listener(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        print ("ikben binnen")
        while 1:
            time.sleep(0.1)
            data = ""
            if(len(list) == 0):
                time.sleep(0.1)
            if flag == 1:
                break
            for i in range(len(list)):
                try:
                    data=list[i].recv(1024)
                except socket.error as err:
                    continue
                datasplit = data.split(" ")
                print("bericht ontvangen")
                print(data)
                print(datasplit)
                if(datasplit[0] == "REQ"):
                    list[i].send("bla")

class acceptor(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        flag = 0
        TCP_IP = '127.0.0.1'
        TCP_PORT = 2038
        BUFFER_SIZE = 1024
        # Server test.
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((TCP_IP, TCP_PORT))
        s.listen(0)
        list = []
        thread1 = listener()
        thread1.start()
        print("socketmade")

        while 1:
            try:
                conn, address = s.accept()
                print("connection accepted")
                conn.setblocking(0)
                list.append(conn)
            except:
                flag = 1
                thread1.join()
                for i in range(list.size):
                    list[i].close()
                s.close()
                sys.exit()
                
            
        ##    conn.send("bla")
        ##    print("done send")
        ##    data = conn.recv(BUFFER_SIZE)
        ##    print data

        print("ik ga de thread sluiten")
        thread1.join()

        conn.close()

        s.close()


                    
