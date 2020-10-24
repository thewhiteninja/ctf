import Image, sys

if len(sys.argv) != 3 :
	print 'Usage : LSBfilter.py <picture> <bit>\nexample : LSBfilter.py test.bmp 1 (bit position starting from the end)'
	sys.exit(2)
	
if ((sys.argv[2] != '1') and (sys.argv[2] != '2')) :
	print 'The bit position has to be 1 or 2'
	sys.exit(2)
	
LSB = int(sys.argv[2])
print "lsb : " + str(LSB)

im = Image.open(sys.argv[1])
pix = im.load()

width = im.size[0]
height = im.size[1]

if im.mode == 'RGB' :
	multi = im.split()
	Rpix = multi[0].load()

	for x in range(width):
		for y in range(height) :
		
			if ((Rpix[x,y] & LSB) / LSB) == 0 :
				Rpix[x,y] = 0
			
			if ((Rpix[x,y] & LSB) / LSB) == 1 :
				Rpix[x,y] = 255
				
	Gpix = multi[1].load()

	for t in range(width):
		for z in range(height) :
		
			if ((Gpix[t,z] & LSB) / LSB) == 0 :
				Gpix[t,z] = 0
			
			if ((Gpix[t,z] & LSB) / LSB) == 1 :
				Gpix[t,z] = 255
	
	Bpix = multi[2].load()

	for u in range(width):
		for v in range(height) :
		
			if ((Bpix[u,v] & LSB) / LSB) == 0 :
				Bpix[u,v] = 0
			
			if ((Bpix[u,v] & LSB) / LSB) == 1 :
				Bpix[u,v] = 255
				
	im = Image.merge(im.mode, multi)
	
else :
	for y in range(width):
		for x in range(height) :
		
			if ((pix[x,y] & LSB) / LSB) == 0 :
				pix[x,y] = 0
			
			if ((pix[x,y] & LSB) / LSB) == 1 :
				pix[x,y] = 255

im.save(sys.argv[1].split('.')[0]+'-LSBfiltered.bmp')

print 'Filter applied'

sys.exit(0)