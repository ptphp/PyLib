#!/usr/bin/env python
# -*- coding: utf-8 -*-
#http://www.randomnude.com/
import urllib,urllib2,time,sys,os,re,hashlib
from BeautifulSoup import BeautifulSoup
from urlparse import urlparse

page = []
    

# html代码截取函数
def rects(html,regx,cls=''):
    if not html or html == None or len(html)==0 : return ;
    # 正则表达式截取
    if regx[:1]==chr(40) and regx[-1:]==chr(41) :
        reHTML = re.search(regx,html,re.I)
        if reHTML == None : return 
        reHTML = reHTML.group()
        intRegx = re.search(regx,reHTML,re.I)
        R = reHTML[intRegx]
    # 字符串截取
    else :        
        # 取得字符串的位置
        pattern =re.compile(regx.lower())
        intRegx=pattern.findall(html.lower()) 
        # 如果搜索不到开始字符串，则直接返回空
        if not intRegx : return 
        R = intRegx
    # 清理内容
    if cls:
        RC = []
        for item in R:
            RC.append(re.sub(item,cls))            
        return RC
    else:
        return R


def getURL(url = 'http://www.randomnude.com'):
    req =urllib2.Request(url)
    r =urllib2.urlopen(req).read()
    soup = BeautifulSoup(r)
    for url in soup("a"):
        if str(url).find("http://www.randomnude.com") !=-1:
            href = url['href']
            if href not in page:
                page.append(href)
                getCom(href)
    
def getCom(url = 'http://www.randomnude.com/2011/07/07/random-nude-image-part-15-173/#respond'):
    req =urllib2.Request(url)
    r =urllib2.urlopen(req).read()
    soup = BeautifulSoup(r)
    imgs = soup("img")
    for img in imgs:
        if img['src'].find('/uploads/20') !=-1:
            src = img['src']
            hash = hashlib.md5(src).hexdigest().upper()+".jpg"
            print src
            downjpg(src,'d:\\pic\\'+hash+".jpg")
def downjpg(url,filename):
    try:
        urllib.urlretrieve(url,filename)
    except Exception,what:
        #print what
        return False
    else:
        return True 

if __name__ == "__main__":
    while 1:
        u =getURL()
        for h in u:
            try:            
                getURL(h)
            except:
                pass