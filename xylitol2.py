import sys, os, hashlib
from Crypto.Cipher import Blowfish
 
def hexencode(bytes):
  return ''.join("%02X" % ord(x) for x in bytes)	
 
def pad(data, size):
	return data + "\x00"*(8-(len(data)%8))
 
def modExp(a, b, m) :
    a %= m
    ret = None
    if b == 0 :
        ret = 1
    elif b%2 :
        ret = a * modExp(a,b-1,m)
    else :
        ret = modExp(a,b//2,m)
        ret *= ret     
    return ret%m
 
###############################################################################
 
def keyFor(username):
	print "Username : " + username
	print
	print "[+] Computing username data"
 
	usernameInv = username[::-1]
	print "    Inverting username        : " + usernameInv
 
	KEY = "XyLrEdCrEw2k11\x00"
	print "    Init blowfish with key    : " + KEY
	bf = Blowfish.new(KEY)
 
	data = pad(usernameInv, 8)	
	C = hashlib.md5(hexencode(bf.encrypt(data))).hexdigest().upper()
	print "    Encrypted&Hashed username : " + C
 
	print
	print "[+] Computing serial data"
 
	N = "A3A500E4E0F1B0D50C124074D0BAFAC800A4202BBFB3BCC3EC6076D0BF2961A9"
	P = "B28F156C75E602790E728CAA65212143"
	Q = "EA9E044DD28F9D33CA221460728CBCA3"
	D = "81219C81FFAB58B1D553B5BF3852C3BEB7105E6A3D012BAD6136B0DAF91E334D"
 
	print "    N : " + N
	print "    With RSATool2 : "
	print "        P : " + P
	print "        Q : " + Q
	print "        D : " + D
	print "    Calculating M = C^D % N"
 
	M = modExp(int(C, 16), int(D, 16), int(N, 16))
	M = hex(M)[2:-1].upper()
	print "        M : " + M
 
	print
	print "[+] End"
	print
	print "    Serial : " + M
 
###############################################################################
 
print 
print "============================ KeygenMe2 ============================"
print
 
if len(sys.argv)<2:
	print "Usage : " + os.path.basename(sys.argv[0]) + " username"
	print
else:
	keyFor(sys.argv[1])