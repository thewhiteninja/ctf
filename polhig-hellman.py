import gmpy2
import math
import ecc
import struct

def bits_to_int(bits):
    return int.from_bytes(bits, 'big')


def int_to_bits(n):
    l = gmpy2.mpz(n).bit_length()
    if l%8 == 0:
        l = int(l/8)
    else:
        l = int(l/8) + 1

    return n.to_bytes(l, 'big')


def point_to_bits(p):
    if p.isInf():
        return struct.pack('!H', 0)

    x = int_to_bits(p.x)
    y = int_to_bits(p.y)

    msg  = struct.pack('!H', len(x)) + x
    msg += struct.pack('!H', len(y)) + y

    return msg


def bits_to_point(p):
    (x_size,) = struct.unpack('!H', p[:2])
    if x_size == 0:
        return ecc.PointInf()

    x = bits_to_int(p[2:x_size+2])
    y = bits_to_int(p[x_size+4:])

    return ecc.Point(x, y)


def xgcd(b, n):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while n != 0:
        q, b, n = b // n, n, b % n
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return  b, x0, y0

def decompose_order(n):
    factors = []

    i = 2
    while i <= n and n != 1:
        if n % i == 0:
            factors.append([i, 0])
        while n % i == 0:
            factors[-1][1] += 1
            n //= i
        i += 1

    return factors


def baby_step_giant_step(curve, G, H, order):

    m = int(math.ceil(gmpy2.sqrt(order)))
    L = {}


    # Baby steps
    for j in range(0, m):
        P_tmp = curve.mul(j, G)
        L[str(P_tmp)] = j

    mG = curve.mul(m, G)

    # Giant steps
    for i in range(0, m):
        P_tmp = curve.mul(i, mG)
        if not P_tmp.isInf():
            P_tmp = ecc.Point(P_tmp.x, (-P_tmp.y) % curve.p)

        P = curve.add(H, P_tmp)

        index = str(P)

        if index in L:
            return (L[index] + i*m) % curve.p

    return None

# Solve the equation : G^x = H (mod curve.p)
def pohlig_hellman(curve, G, H):
    N = curve.p-1
    factors = decompose_order(N)
    x = 0


    for i in range(len(factors)):
        ni = factors[i][0]**(factors[i][1])
        tmp = N//ni
        G_prime = curve.mul(tmp, G)
        H_prime = curve.mul(tmp, H)

        order = ni

        # Now, use the Baby Step Giant Step algorithm to solve :
        # H_prime = x_prime*G_prime
        x_prime = baby_step_giant_step(curve, G_prime, H_prime, order)
        while x_prime == None:
            order *= 2
            x_prime = baby_step_giant_step(curve, G_prime, H_prime, order)

        print("BSGS found a solution in O(sqrt(%d))" % order)

        # Use the CRT to solve the equation x_prime = x (mod ni)
        (gcd, x0, x1) = xgcd(ni, tmp)

        x += x_prime*x1*tmp

    return x % N

# (A, B, N)

A = 0
B = 0
N = 0

X = 0
Y = 0

curve = ecc.Curve(A, B, N)
G = ecc.Point(X, Y)

sent = [0x00, 0x30, 0x00, 0x16, 0x0d, 0x6c, 0x24, 0xb0, 
        0x5a, 0xf7, 0xff, 0x4f, 0xa6, 0x28, 0xeb, 0xce, 
        0xfd, 0x43, 0xdd, 0xad, 0x1a, 0x57, 0xac, 0xb9, 
        0xa4, 0x65, 0x00, 0x16, 0x0a, 0x00, 0x63, 0x5f, 
        0x98, 0x88, 0x1c, 0x47, 0x07, 0x50, 0x48, 0x3e, 
        0xa0, 0x59, 0x77, 0xc1, 0x93, 0x28, 0x9a, 0xeb, 
        0x50, 0x64]

H = bits_to_point("".join(map(chr, sent)).encode())

x = pohlig_hellman(curve, G, H)
print("x = %s" % x)