import sys, urllib, urllib2
from PIL import Image
from pytesser import *

def cleanImg(imgfile, cleanfile):
	img = Image.open(imgfile)
	left, top, width, height = 163, 29, 582, 35
	box = (left, top, left+width, top+height)
	clean = img.crop(box)
	clean.save(cleanfile, "png")
	return cleanfile
	
def factorize(n):
	p = urllib.urlopen("http://wims.unice.fr/wims/wims.cgi?session=popup&wims_window=500x200&module=tool%2Falgebra%2Ffactor.fr&precision=12&calc=factor&formula=" + str(n))
	c = p.read()
	p.close()
	return c[c.rfind("&times;</font>")+14:c.find('<p>', c.rfind("&times;</font>"))].strip()
	
def ocr(imgFile):
	img = Image.open(imgFile)
	return image_to_string(img)
	
def getFile(url, name):
	p = urllib.urlopen(url)
	content = p.read()
	p.close()
	f = open(name, "wb")
	f.write(content)
	f.close()
	return name
	
def sendRep(n, trueans):
	values = {'captchatype' : 'refactor',
			  'trueanswer' : trueans,
			  'answer' : str(n),
			  'submit ' : 'Submit '}

	data = urllib.urlencode(values)
	req = urllib2.Request("http://misteryou.ru/ppc300/", data)
	handle = urllib2.urlopen(req)
	return handle.read()
	
def extractData(pageFile):
	f = open(pageFile, "r")
	c = f.read()
	captcha = c[c.find('src=\'')+6:c.find('.png')+4]
	trueans = c[c.find('value=\'', c.find("trueanswer"))+7:c.find('\' />', c.find("trueanswer"))]
	f.close()
	return (captcha, trueans)
	
getFile("http://misteryou.ru/ppc300/", "page.html")
(imagepath, trueans) = extractData("page.html")
print (imagepath, trueans)
getFile("http://misteryou.ru/" + imagepath, "captcha.png")
cleanImg("captcha.png", "clean.png")
n = int(ocr("clean.png").replace(" ", "").replace("l", "1").strip(), 10)
print "n = ", n
rep = factorize(n)
print "    factor : ", rep
print sendRep(rep, trueans)
