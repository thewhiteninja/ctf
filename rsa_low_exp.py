import gmpy2

n = 1
e = 0x10001
d = 1


def isqrt(n):
    d = len(str(n))
    x = '3'
    d = d / 2
    while d > 0:
        d = d - 1
        x = x + '1'
    x = int(x)
    prev = 0
    while x != prev:
        prev = x
        q = n / x
        x = (x + q) / 2

    return x
    
def rfact(n, e, d):    
    """ because e*d is congruent to 1 mod phi(n), e*d is very close to
      being a multiple of phi, and phi is very close to n for an RSA
      modulus - so the whole number quotient (e*d)/n is 1 less than
      this factor """
    k = 1 + (e * d) / n
    phi = (e * d - 1) / k
    """ if n=p*q, then phi(n) = (p-1)*(q-1) = p*q + 1 - (p+q); but p*q=n,
      so phi(n) = n + 1 - (p+q); set 'sum' to p+q """
    sum = n + 1 - phi
    """ we now know the product of p and q (n) and their sum (sum).  we
      solve for p and q using the quadratic formula.  set 'delta' to
      the radical in the numerator of the formula """
    delta = isqrt(sum**2 - 4*n)
    p = (sum + delta) / 2
    q = (sum - delta) / 2
    if p*q != n:
        print '!Failed:  modulus not factored correctly!'
    return [p, q]   
    
def egcd(a,b):
    u, u1 = 1, 0
    v, v1 = 0, 1
    while b:
        q = a // b
        u, u1 = u1, u - q * u1
        v, v1 = v1, v - q * v1
        a, b = b, a - q * b
    return u, v, a

# 1/e % n
def modInverse(e,n):
    return egcd(e,n)[0]%n    
    

(p,q) = rfact(n, e, d)    

print "p", hex(p)
print "q", hex(q)
print "expo1", hex(d % (p-1))
print "expo2", hex(d % (q-1))
print "coeff", hex(modInverse(q, p))


orig = int(open("secret").read().encode("hex"), 16) 
c = orig
while True:
    m = gmpy2.cbrt(c)
    if pow(int(m), 3, n) == orig:
        print "pwned"
        out=""
        for k in xrange(212,-1,-1):
            blah=27**k
            val=int(m/blah)
            m = m - val*blah
            if val==0:
                out+=" "
            else:
                out+=chr(0x60+val)
            print out[::-1]        
        break
    c += n