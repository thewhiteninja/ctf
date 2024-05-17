import socket
import time
import sys


def typecheck(f):
    """
    Taken from "Python 3 - Das umfassende Handbuch"
    """
    def decorated(*args, **kws):
        for i, name in enumerate(f.__code__.co_varnames):
            argtype = f.__annotations__.get(name)

            # Only check if annotation exists and it is as a type
            if isinstance(argtype, type):
                # First len(args) are positional...
                if i < len(args):
                    if not isinstance(args[i], argtype):
                        raise TypeError("Positional argument {0} has type {1} but expected was type {2}.".format(i, type(args[i]), argtype))
                # ...after that check keywords
                elif name in kws:
                    if not isinstance(kws[name], argtype):
                        raise TypeError("Keyword argument '{0}' has type {1} but expected was type {2}.".format(name, type(kws[name]), argtype))

        res = f(*args, **kws)
        restype = f.__annotations__.get('return')

        # Check return type
        if isinstance(restype, type):
            if not isinstance(res, restype):
                raise TypeError("Return value has type {0} but expected was type {1}.".format(type(res), restype))

        return res

    return decorated

@typecheck
def os2ip(octets: bytes) -> int:
    """
    Octet-String-to-Integer primitive
    PKCS #1 Version 1.5 (RFC2313)
    """
    return int.from_bytes(octets, 'big')


@typecheck
def i2osp(i: int, k: int) -> bytes:
    """
    Integer-to-Octet-String primitive
    PKCS #1 Version 1.5 (RFC2313)
    """
    return i.to_bytes(k, byteorder='big')
    

class Oracle:
    """
    Bleichebacher's oracle implementing methods available to eve.
    """

    @typecheck
    def __init__(self, msg, n):
        """
        Setup keys, secret message and encryption/decryption schemes.
        """
        self.s = socket.socket()
        self.s.connect(("localhost", 51027))
        self._pkcsmsg = msg
        self._n = n

    @typecheck
    def get_n(self) -> int:
        """
        Returns the public RSA modulus.
        """
        return self._n 

    @typecheck
    def get_e(self) -> int:
        """
        Returns the public RSA exponent.
        """
        return 65537

    @typecheck
    def get_k(self) -> int:
        """
        Returns the length of the RSA modulus in bytes.
        """
        return 256

    @typecheck
    def eavesdrop(self) -> bytes:
        return self._pkcsmsg

    @typecheck
    def decrypt(self, ciphertext: bytes) -> bool:
        self.s.send(ciphertext)
        resp = self.s.recv(1024).decode("utf-8")
        print(resp)
        ok = resp.find("decryption : ok") != -1
        print(ok)
        sys.exit(0)
        return ok
        

@typecheck
def extended_gcd(aa: int, bb: int) -> tuple:
    """
    http://rosettacode.org/wiki/Modular_inverse#Python
    """
    lastremainder, remainder = abs(aa), abs(bb)
    x, lastx, y, lasty = 0, 1, 1, 0
    while remainder:
        lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
        x, lastx = lastx - quotient * x, x
        y, lasty = lasty - quotient * y, y
    return lastremainder, lastx * (-1 if aa < 0 else 1), lasty * (-1 if bb < 0 else 1)


@typecheck
def modinv(a: int, m: int) -> int:
    """
    http://rosettacode.org/wiki/Modular_inverse#Python
    """
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise ValueError
    return x % m


@typecheck
def interval(a: int, b: int) -> range:
    return range(a, b + 1)


@typecheck
def ceildiv(a: int, b: int) -> int:
    """
    http://stackoverflow.com/a/17511341
    """
    return -(-a // b)


@typecheck
def floordiv(a: int, b: int) -> int:
    """
    http://stackoverflow.com/a/17511341
    """
    return a // b


@typecheck
def bleichenbacher(oracle: Oracle):
    """
    Bleichenbacher's attack

    Good ideas taken from:
        http://secgroup.dais.unive.it/wp-content/uploads/2012/11/Practical-Padding-Oracle-Attacks-on-RSA.html
    """

    k, n, e = oracle.get_k(), oracle.get_n(), oracle.get_e()

    B = pow(2, 8 * (k - 2))
    B2 = 2 * B
    B3 = B2 + B

    @typecheck
    def pkcs_conformant(c_param: int, s_param: int) -> bool:
        """
        Helper-Function to check for PKCS conformance.
        """
        pkcs_conformant.counter += 1
        return oracle.decrypt(i2osp(c_param * pow(s_param, e, n) % n, k))

    pkcs_conformant.counter = 0

    cipher = os2ip(oracle.eavesdrop())

    assert(pkcs_conformant(cipher, 1))

    c_0 = cipher
    set_m_old = {(B2, B3 - 1)}
    i = 1

    s_old = 0
    while True:
        if i == 1:
            s_new = ceildiv(n, B3)
            while not pkcs_conformant(c_0, s_new):
                s_new += 1

        elif i > 1 and len(set_m_old) >= 2:
            s_new = s_old + 1
            while not pkcs_conformant(c_0, s_new):
                s_new += 1

        elif len(set_m_old) == 1:
            a, b = next(iter(set_m_old))
            found = False
            r = ceildiv(2 * (b * s_old - B2), n)
            while not found:
                for s in interval(ceildiv(B2 + r*n, b), floordiv(B3 - 1 + r*n, a)):
                    if pkcs_conformant(c_0, s):
                        found = True
                        s_new = s
                        break
                r += 1

        set_m_new = set()
        for a, b in set_m_old:
            r_min = ceildiv(a * s_new - B3 + 1, n)
            r_max = floordiv(b * s_new - B2, n)
            for r in interval(r_min, r_max):
                new_lb = max(a, ceildiv(B2 + r*n, s_new))
                new_ub = min(b, floordiv(B3 - 1 + r*n, s_new))
                if new_lb <= new_ub:  # intersection must be non-empty
                    set_m_new |= {(new_lb, new_ub)}

        print("Calculated new intervals set_m_new = {} in Step 3".format(set_m_new))

        if len(set_m_new) == 1:
            a, b = next(iter(set_m_new))
            if a == b:
                print("Calculated:     ", i2osp(a, k))
                print("Calculated int: ", a)
                print("Success after {} calls to the oracle.".format(pkcs_conformant.counter))
                return a

        i += 1
        s_old = s_new
        set_m_old = set_m_new

if __name__ == "__main__":
    encmsg = bytes.fromhex("AB4BEEE8FE53773EBDF5BFF1A4C5364558CA986BA74BAD44ECC106694BEC44CD25681FAE106C81C7195231B4A2F6CA1E1E7853C6BBA2A18E4A9B8FDDD262ED27325F6F56045CE8593A2BD10AFFC8F42B16E43E4655EC328F4F34C8EE0269FC4F00B02B37FC7296A9B2E78D25E2D5777D83A1510B97F9F44896CAAB14078E6300740B3A25D2098D8042F5C6953BE70108A88040E48109F05E7E2923A481475293C5AD68F540754EA6CAB139BC803A91890383D2D1AF33D2C6216F4C68D0D0895B5E5B7B627AE36FBABEDB67ADC742FF911909D65E8B9B07D805F24B2ABD336F28C412A433F0FE2F19F066DFA8833AB2A2CCB9764D0CF1D754082D0BE770230EF6")
    n = 27080861298319437815633310784006984833173283797779738907042118088413153195707172513724176382473810715102224034126973994622466306866468122718802449959709278753937064444655427776112428351591669264429699595580580682860394129412716224924713453836152005549566739739327593727104054391375814744426313793812092409489252917611935017231260553012797538583712710235336204768620209756636770180548721989739061091202408219263645950843040364734418328274561224671650912686748424893806291933165596129266096299469428824579295155527725313354681726959327676864265430653342063686059366213088539663746331243027420156930356600056209003641403
    
    oracle = Oracle(encmsg, n)
    bleichenbacher(oracle), oracle.get_k()
