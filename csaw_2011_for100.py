import os, sys, itertools, hashlib, Image

DIR = "cutyoface"

def fact(x):
     if x < 2:
         return 1
     else:
         return x * fact(x-1)

def md5(filePath):
    fh = open(filePath, 'rb')
    m = hashlib.md5()
    while True:
        data = fh.read(8192)
        if not data:
            break
        m.update(data)
    return m.hexdigest()

print "CSAW - Forensics 100"
print 

files = os.listdir(DIR)

print str(len(files)) + " files in " + DIR + os.sep
print 

firstFile = "316551"
files.remove(firstFile)

print "Testing " + str(fact(len(files))) + " permutations ..."

for p in itertools.permutations(files):
	s = firstFile
	for file in p:
		s += file
	if hashlib.md5(s).hexdigest() == "72b968afe153d2fd1fab46eddcfb5093":
		print "Correct image found !"
		break

	