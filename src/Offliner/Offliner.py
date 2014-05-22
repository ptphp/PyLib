#!/usr/bin/env python
# -*- coding: utf-8 -*-
#:offliner.py

from BeautifulSoup import BeautifulSoup
import urllib,urllib2
from urlparse import urlparse
import os,re,time

def getPath(url):
    path = urlparse(url).path
    _path = "fanli%s" % path
    makeDir(os.path.dirname(_path))
    return _path

def makeDir(path):
    path = os.path.join(os.getcwd(),path) 
    if os.path.isdir(path) == False:
        makeDir(os.path.dirname(path))        
        return os.mkdir(path)    
    return True

def putContent(path,content,f = False):
    if os.path.isfile(path) and f == False:
        pass
    else:                
        f = open(path,'w')
        f.write(content)
        f.close()
def processImg(imgurl):
    path = getPath(imgurl)
    if os.path.isfile(path) == False:
        urllib.urlretrieve(imgurl, path)
    return path
    
                
url = 'http://51fanli.com/index.html'    
res = urllib2.urlopen(url).read()
soup = BeautifulSoup(res)
html = soup.prettify()
#print soup.prettify()
jsFiles =  soup.findAll('script',src=True)
#print jsFiles
replaceList = []
for js in jsFiles:
    jsurl = js['src']
    path = getPath(jsurl)
    putContent(path,urllib2.urlopen(jsurl).read())
    replaceList.append({jsurl:path})
    
cssFiles = soup('link',href=True)
for css in cssFiles:
    #print css['href']
    if "css" in css['href']:
        cssurl = css['href']
        path = getPath(cssurl)
        putContent(path,urllib2.urlopen(cssurl).read())
        replaceList.append({cssurl:path})        

        cssContent = urllib2.urlopen(cssurl).read()        
        p = re.compile("url\((.*?)\)")
        imgUrl = re.findall(p,cssContent)
        for img in imgUrl:
            o = urlparse(cssurl)
            img_url = "%s://%s%s" % (o.scheme,o.netloc,img.strip("\""))
            print img_url            
            processImg(img_url)

#imgFiles =  soup.findAll('img',src=True)
#for img in imgFiles:
#    img_url = img['src'].encode('utf-8')
#    path = processImg(img['src'])
    #replaceList.append({img['src']:path})

print replaceList
for r in replaceList:
    for i in r:
        key = i;
        value = r[i]
        
    html = html.replace(key,value)
putContent(getPath(url),html,True)
        