import sys,math,struct

S=[[7,12,17,22],
   [5,9,14,20],
   [4,11,16,23],
   [6,10,15,21]]

O=[0,1,5,0]
M=[1,5,3,7]

T = map(lambda i: long(4294967296.0*abs(math.sin(i))), range(1,65))

A,B,C,D=struct.unpack("<IIII","\x01\x23\x45\x67\x89\xab\xcd\xef\xfe\xdc\xba\x98\x76\x54\x32\x10")

F = lambda x,y,z: x&y | (~x)&z
G = lambda x,y,z: x&z | y&(~z)
H = lambda x,y,z: x^y^z
I = lambda x,y,z: y^(x|(~z))

def K(f,a,b,c,d,xk,s,i):
    a += f(b,c,d)+xk+T[i]
    a &= (2**32-1)
    a = (a << s) | (a >> (32-s)) 
    return (a+b) & (2**32-1)

FF = lambda *args: K(F,*args)
GG = lambda *args: K(G,*args)
HH = lambda *args: K(H,*args)
II = lambda *args: K(I,*args)

Func=[FF,GG,HH,II]    

finished=0
l=0
while 1:
    if finished:
        chunk = chunk[64:]
        if len(chunk) < 64:
            break
    else:
        chunk = sys.stdin.read(64)
        l += len(chunk)
        if len(chunk) < 64:
            # Padding is always added :
            # \x80+some \x00+bitlen (on 8 bytes, little endian)
            # so that the input length is a multiple of 64 bytes.
            chunk += "\x80"
            chunk += "\x00"*( (64+56-(l+1))%64 )
            chunk += struct.pack("<II",(l*8)&(2**32-1),((l*8)>>32)&(2**32-1))
            finished = 1
    
    L=[A,B,C,D]

    for round in range(4):
        for j in range(4):
            for k in range(4):
                ofs= ((j*4+k)*M[round]+O[round]) % 16
                L[-k]=Func[round](L[-k],L[1-k],L[2-k],L[3-k],
                                  struct.unpack("<I",chunk[4*ofs:4*ofs+4])[0],
                                  S[round][k], round*16+j*4+k)
    A+=L[0]
    B+=L[1]
    C+=L[2]
    D+=L[3]


def pr(x):
    return "%02x%02x%02x%02x" % (x&0xff, (x>>8)&0xff, (x>>16)&0xff,(x>>24)&0xff)

print pr(A)+pr(B)+pr(C)+pr(D)
