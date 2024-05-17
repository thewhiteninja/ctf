import urllib
import urllib2
import time

minscore = 600000

levelUrl = 'http://flashgame.azurewebsites.net/Level.aspx'	
submitUrl = 'http://flashgame.azurewebsites.net/Submit.aspx'

headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0',
			'Cookies' : 'WAWebSiteSID:74f7c4f0805d4f3984689cbe011c45d5; ARRAffinity:59f2c0d75626615e506c113bef6955ffdd5da3a09f1af84d5c6a9eab389ec27d',
			'Host' : 'flashgame.azurewebsites.net',
			'Referer' : 'http://flashgame.azurewebsites.net/EliTheZombie.swf'}

			
def nextLevel(score, level):
	values = {'ID' : 'IPSTMESMWN',
          'Score' : score,
          'Level' : level}
	data = urllib.urlencode(values)
	req = urllib2.Request(levelUrl, data, headers)
	response = urllib2.urlopen(req)
	print response.read()
	print "Level %d sent with score %d"%(level,score)

def submitFinal(score, level):
	values = {'ID' : 'IPSTMESMWN',
          'Score' : score,
          'MaxLevel' : level+1,
		  'Code':  str((((-42-score)&0xffffffff) ^ 3735928559) & 0xffffffff),
		  'Name': 'Tes'}
	data = urllib.urlencode(values)
	req = urllib2.Request(submitUrl, data, headers)
	response = urllib2.urlopen(req)
	response.read()
	print "Final Level %d sent with score %d"%(score,level)

def getScoreboard():
	req = urllib2.Request("http://flashgame.azurewebsites.net/Scores.aspx?ID=IPSTMESMWN")
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0')
	req.add_header('Cookies', 'WAWebSiteSID:74f7c4f0805d4f3984689cbe011c45d5; ARRAffinity:59f2c0d75626615e506c113bef6955ffdd5da3a09f1af84d5c6a9eab389ec27d')
	req.add_header('Host', 'flashgame.azurewebsites.net')
	req.add_header('Referer', 'http://flashgame.azurewebsites.net/EliTheZombie.swf')
	resp = urllib2.urlopen(req)
	print resp.read()	

def run():
	s=0
	humans = 6
	nextLevel(s, 1)
	while s < minscore:
		s += humans * 100
		humans += 1
		nextLevel(s, humans-5)
		time.sleep(2)
	submitFinal(s, humans-5)

run()	
getScoreboard()
