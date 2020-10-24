import sys
import os


def usage():
	print 'Usage: playfair.py dictionary.txt'
	sys.exit(0)
	
def isOnTheSameLine(c, t):
	return t.index(c[0])/5==t.index(c[1])/5
	
def isOnTheSameColumn(c, t):
	return t.index(c[0])%5 == t.index(c[1])%5
	
def decodeLine(c, t):
	il = t.index(c[0])/5
	li = t[il*5:il*5+5]
	i1 = li.index(c[0])-1 % 5
	i2 = li.index(c[1])-1 % 5
	return li[i1]+li[i2] 

def decodeCol(c, t):
	ic = t.index(c[0])%5
	col = []
	for i in range(5):
		col.append(t[i*5 + ic])
	i1 = col.index(c[0])-1 % 5
	i2 = col.index(c[1])-1 % 5
	return col[i1]+col[i2] 

def decodeRect(c, t):
	il1 = t.index(c[0])/5
	ic1 = t.index(c[0])%5
	il2 = t.index(c[1])/5
	ic2 = t.index(c[1])%5
	l1 = t[il1*5:il1*5+5]
	l2 = t[il2*5:il2*5+5]
	return l1[ic2]+l2[ic1] 

def tryThisKey(k, data):
	t = []
	for i in range(len(k)):
		if not (k[i] in t) and not(k[i]=='W'):
			t.append(k[i])
	while len(t)<25:
		for c in range(65, 91):
			if not(chr(c) in t) and not(chr(c)=='W'):
				t.append(chr(c))
				break
				
	plaintext = ''
	for i in range(0, len(data), 2):
		cipher = data[i:i+2]
		if isOnTheSameLine(cipher, t):
			plaintext += decodeLine(cipher, t)
		elif isOnTheSameColumn(cipher, t):
			plaintext += decodeCol(cipher, t)
		else:
			plaintext += decodeRect(cipher, t)

	if plaintext.find("PASS")!=-1:
		print "I found a key ! It's " + k + ""
		print "So, the plaintext is " + plaintext
		sys.exit(0)
		
################################################################################
	
data = ""

	
if len(sys.argv)<=1:
	usage()
	
try:
	fs = open(sys.argv[1], 'r')
	while 1:
		key = fs.readline().strip().upper()
		if key == '':
			break
		if len(key)==6:
			tryThisKey(key, data)
except IOError :
	print "Where is that file \""+os.path.basename(sys.argv[1])+"\"??"
	sys.exit(0)

print "Humm ... I tried all the key and ... sorry :("
		