from socket import *
from ast import literal_eval as make_tuple

#####################################################################

HOST = '93.191.13.142'
PORT = 7777

#####################################################################

def remove_key(sbox, k):
    for i2, c in enumerate(k):
        for i in xrange(len(sbox)):
            sbox[i] = (sbox[i] - 1) % 128
        sbox[i2], sbox[ord(c)] = sbox[ord(c)], sbox[i2]
        
def findSize(sbox):
	return sbox[-1] + 1

def getKeyedSaltedSbox(sbox):
	client = socket(AF_INET, SOCK_DGRAM)
	for c in range(1, 128):
		client.sendto("A" + chr(c), (HOST, PORT))
		data = client.recvfrom(1024)
		sbox.append(int(data[0], 16))
	client.close()		
	for i in range(128):
		if i not in sbox:
			sbox.insert(0, i)
			break;

def cleanSbox(sbox, size):
	for i in range(len(sbox)):
		sbox[i] = (sbox[i]-size)%128
	for i in range(size):
		while sbox[i]<17:
			sbox[i] = sbox[sbox[i]]
		
			
#####################################################################

print
print "######"
print "## hackyou - crypto300 - UDP Hardcore"
print "######"

sbox = []

print "\n[+] Retrieving keyed and salted sbox"
getKeyedSaltedSbox(sbox)
print "KSsbox:", sbox

print "\n[+] Removing key"
remove_key(sbox, "A")
print "Ssbox:", sbox 

print "\n[+] Finding flag size ...",
keySize = findSize(sbox)
print keySize

print "\n[+] Cleaning sbox"
cleanSbox(sbox, keySize)
print "sbox:", sbox

print "\nFlag is : %s (%s)" % (''.join(map(chr, sbox[:keySize])), sbox[:keySize])
	