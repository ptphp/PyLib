import os
import re
import urlparse
import urllib2

root_dir = 'D:\Dhole\PtProject\Core\Application\static\game110\images'

def saveUrlToLocal(url):
	#print urlparse.urlparse(url)
	u = urlparse.urlparse(url)
	#print u.path.replace("/td/site","")
	svae_path  = root_dir + u.path.replace("/td/site","")
	#print svae_path
	makeDir(os.path.dirname(svae_path))
	#print svae_path
	res = urllib2.urlopen(url)
	#print res.read()
	saveFile(svae_path,res.read())


def reUrls(content):
	res = re.findall("url\((.*?)\)",content)
	return res

def makeDir(path):
    if os.path.isdir(path) == False:
        makeDir(os.path.dirname(path))
        return os.mkdir(path)    
    return True

def getFileContent(name):
	f = open(name,"r")
	return f.read()
def saveFile(name,content):
	f = open(name,"w")
	f.write(content)

def main():
	filename = 'D:\Dhole\PtProject\Core\Application\static\game110\css\qq_global.css'
	content = getFileContent(filename)
	urls = reUrls(content)
	#print urls
	for url in urls:		
		#saveUrlToLocal(url)
		print url
	#saveFile(filename,content)

if __name__ == '__main__':
	main()