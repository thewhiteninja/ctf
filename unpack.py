
offset = 0x08448050

#.text
blockStart = 0x08789610
blockLen = 0x7d5b
blockChecksum = "45C940E247DE83513AB32C98".decode("hex")

def decrypt(d, k):
    return [(((ord(d[i])^ord(k[i%len(k)])) & 0xff) +86)& 0xff for i in range(len(d))]
    
def checksum(d):
    c = []
    for i in range(12):
        c += [0]
        for i in range(i, len(d), 12):
            c[-1] = (d[i]^c[-1]) & 0xff
    return c

password = []
for k in range(256):
    blockData = data[blockStart-offset:blockStart-offset+blockLen]
    blockData = decrypt(blockData, chr(k))
    check = checksum(blockData)
    print "".join(map(chr, check)).encode("hex")
    
            
print password
print map(chr, password)





