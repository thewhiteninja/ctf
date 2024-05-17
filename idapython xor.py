from idaapi import patch_byte, get_byte

def decrypt(start, end, key):
    iKey = 0
    for i in xrange(start, end):
        patch_byte(i, get_byte(i) ^ ord(key[iKey % len(key)]))
        iKey += 1

        
