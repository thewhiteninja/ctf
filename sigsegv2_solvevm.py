import sys
import math
import codecs

rsa = [(51650810, 2009560109),
       (729078379,2103567149),      
       (1669759679,2068691993),
       (1497487137,1656909407),       
       (1559052731,1751421943)]

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a
    
def multiplicative_inverse(a, b):
    x, y = 0, 1
    lx, ly = 1, 0
    oa, ob = a, b
    while b != 0:
        q = a // b
        (a, b) = (b, a % b)
        (x, lx) = ((lx - (q * x)), x)
        (y, ly) = ((ly - (q * y)), y)
    if lx < 0:
        lx += ob
    return lx

def factor(n):
    p = int(math.sqrt(n))
    if p%2 == 0:
        p += 1
    while True:
        if n % p == 0:
            return p, int(n/p)
            break
        p -= 2
        
        
flag = ""        
for c, n in rsa:
    p, q = factor(n)
    phi = (p-1)*(q-1)
    e = 0x10001
    if gcd(e, phi) == 1:
        d = multiplicative_inverse(e, phi)
        m = pow(c, d, n)
        flag += "%08x" % m

print(codecs.decode(flag, "hex").decode())        

