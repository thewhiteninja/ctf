import asn1

#######################################################################
        
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

#######################################################################    
        
p = 398075086424064937397125500550386491199064362342526708406385189575946388957261768583317
q = 472772146107435302536223071973048224632914695302097116459853171130520711256363590397527
e = 0x1001

n= p*q
d = modInverse(e, (p-1)*(q-1))        
exp1 = d%(p-1)
exp2 = d%(q-1)
coeff = modInverse(q, p)
              
                          
enc = asn1.Encoder(file='private.der', encoding='DER')
seq = asn1.Sequence()
seq.append(n)
seq.append(e)
seq.append(d)
seq.append(p)
seq.append(q)
seq.append(exp1)
seq.append(exp2)
seq.append(coeff)
enc.dump(seq)