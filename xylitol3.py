import sys, os, hashlib, random	
 
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
 
def coprime(a,b):
	return egcd(a,b)[2] == 1 
 
def egcd(a,b):
    u, u1 = 1, 0
    v, v1 = 0, 1
    while b:
        q = a // b
        u, u1 = u1, u - q * u1
        v, v1 = v1, v - q * v1
        a, b = b, a - q * b
    return u, v, a

def modInv(e,n):
    return egcd(e,n)[0]%n 
	
###############################################################################
 
def keyFor(username):
	hash = hashlib.md5(username[::-1]).hexdigest().upper()
 
	P = int("FB1813805D8526E3", 16)
	G = int("A308247C9C2D410E", 16)
	X = int("D6B02EF1B81DE89", 16)
	M = int(hash, 16) % P
	
	while True:
		K = random.randint(1, P-2)
		if coprime(K, P-1):
			break

	# Part1
	R = modExp(G, K, P)
	
	# Part2	
	S = (M-X*R)*modInv(K, P-1) % (P-1)
	 
	print "Login : ", username
	print "Pass  : ", hex(R)[2:-1].upper() + hex(S)[2:-1].upper()
 
###############################################################################
 
if len(sys.argv)<2:
	print "Usage : " + os.path.basename(sys.argv[0]) + " username"
	print
else:
	keyFor(sys.argv[1])
