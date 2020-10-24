import math
import time

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
    
def egcd(a,b):
    u, u1 = 1, 0
    v, v1 = 0, 1
    while b:
        q = a // b
        u, u1 = u1, u - q * u1
        v, v1 = v1, v - q * v1
        a, b = b, a - q * b
    return u, v, a

def modInverse(e,n):
    return egcd(e,n)[0]%n

def baby(base, res, modulus):
    m = int(math.sqrt(modulus) + 1)
    h = {}
    basePow = 1
    for i in range(m):
        h[str(basePow)] = i
        basePow = (basePow * base) % modulus
    basetotheminv = modInverse(modExp(base, m, modulus), modulus)
    y = res
    for i in range(m):
        target = h.get(str(y), None)
        if target != None:
            return (i*m)+target
        else:
            y = y*basetotheminv % modulus
    return None    
        
g = 33785
p = 41513
A = 1761

print("a=%x" % baby(g, A, p))
