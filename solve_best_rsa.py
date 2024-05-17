import gmpy2
import binascii
import sys


def factorize(N):
    tmp = N
    
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]
    factors = []
    for p in primes:
        if tmp == 1:
            break
        cnt = gmpy2.mpz(0)
        while tmp % p == 0:
            tmp /= p
            cnt += 1
        if cnt > 0:
            factors.append([gmpy2.mpq(p), cnt])
    if tmp != 1:
        return None
    return factors
    
def find_phi(N):
    factors = factorize(N)
    if factors is None:
        return None
    phi = gmpy2.mpq(N)
    for f in factors:
        phi = phi * (1 - 1 / f[0])
    return phi

def solve():
    N_str = "11111111111"
    C_str = "11111111111"
    
    N = gmpy2.mpz(N_str)
    c = gmpy2.mpz(C_str)
    e = gmpy2.mpz('65537')
    
    phi = gmpy2.mpz(find_phi(N))
    if phi is None:
        print 'Failed to factorize N'
        return None
        
    print 'N factorized.'
    d = gmpy2.invert(e, phi)
    print 'd found. Decrypting message ...'
    
    m = gmpy2.powmod(c, d, N)   
    return binascii.unhexlify(gmpy2.digits(m, 16))
    
def main():
    gmpy2.get_context().precision=1000
    argv = sys.argv
    argc = len(argv)
    if argc < 2:
        print 'Usage: solve_best_rsa.py <result>'
        return
    result = solve()
    if result is None:
        print 'Failed!'
        return
    try:
        f = open(argv[1], 'wb')
        f.write(result)
        f.close()
        print 'Success!'
    except IOError:
        print 'Failed to save result to file'
    
if __name__ == "__main__":
    main()
