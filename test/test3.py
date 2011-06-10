import socket

TCP_IP = '127.0.0.1'
TCP_PORT = 2001
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
print s
print socket.gethostbyname_ex("u012908.science.uva.nl")

test = [[3]]
test.append(["kippenbot"])
test[0].append("testing")
test[1].append("testing2")

print(test)

TCP_PORT = 5010

test2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
test2.bind((TCP_IP, TCP_PORT))
test2.listen(1)

connection = test2.accept()
print 'Connection address:', connection[1][0]
kip = socket.gethostbyname_ex("localhost")
print connection
print connection[1]
print 'this is it', (connection[0], (kip[2][0], TCP_PORT))
print kip
print kip[2][0]
if connection[1][0] == kip[2][0]:
    print("great success")
else:
    print 'not so great success'
print connection[0]
while 1:
    data = connection[0].recv(BUFFER_SIZE)
    if not data: break
    print "received data:", data
    connection[0].send(data) # echo
connection[0].close()
