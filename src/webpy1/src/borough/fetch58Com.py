#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbmysql import * 
from dbsqli import * 
from parseBody import *
import urllib, urllib2, time, sys, os,socket,re,hashlib
from BeautifulSoup import BeautifulSoup
from urlparse import urlparse
from time import localtime,strftime

timeout =10
drawpath ="D:\\myapp\\project\\wwwroot\\jjr\\upfile\\borough\\drawing\\"
compath ="D:\\myapp\\project\\wwwroot\\jjr\\upfile\\borough\\picture\\"
xiaoqupath ="D:\\home\\spider\\xiaoqu\\"
headers = {'User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14',
           'Accept': 'text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5',
           'Accept-Language':'zh-cn,zh;q=0.5',
           'Accept-Charset':'gb2312,utf-8;q=0.7,*;q=0.7',
           'Keep-Alive':'300',
           'Connection':'keep-alive'}
def collectOne(url,headers):
    req = urllib2.Request(url)
    try:
        socket.setdefaulttimeout(timeout)
        response = urllib2.urlopen(req)
        r = response.read()
        if r:
            return r
        else:
            return False  
    except Exception , what:
        print '[collect error]',url#,req
        return False

mysql = MySQL()
sql ='''
    CREATE TABLE IF NOT EXISTS [borough](
      [id] INTEGER PRIMARY KEY,
      [title] TEXT,
      [city] TEXT,
      [url] TEXT,
      UNIQUE([url]));
            '''
dbname = 'db/ks_58_com.db'
sqli = Sqli(dbname)
sqli.query(sql)
#===============================================================================
# 采集58小区
#===============================================================================
def getLink():
    for i in range(1,60):
        url = "http://su.58.com/xiaoqu/szkunshan/pn%d/" % i        
        print url
        fetchComUrl(url)

def fetchComUrl(url):
    #print url
    r = urllib2.urlopen(url).read()
    soup = BeautifulSoup(r)    
    list = soup.find('div',{'class':"lists"})    
    a = soup('a',{'class':"t"})
    for url in a:
        print url['href'],url.string
        sqli.query("insert into borough values(null,'%s','%s','%s')" % (url.string,'ks',url['href']))

def fetchComCon(url = "http://su.58.com/xiaoqu/szkunshan/sijihuacheng/"):
    
    print url
    #r = spiderIO.collectOne(pagedata, headers)
    #br.set_debug_http(True)
    hosts = urlparse(url)
    citycode ='ks'
    
    if not os.path.isdir(compath+citycode+"\\") :
        os.makedirs(compath+citycode+"\\")
    if not os.path.isdir(drawpath+citycode+"\\") :
        os.makedirs(drawpath+citycode+"\\")
        
    url_jieshao = url+'jieshao/'
    url_map     = url+'map/'
    url_pic     = url+'shijing/'
    url_drawn    = url+'huxing/'
    #r = br.open(pagedata['url']+'jieshao/')
    html = collectOne(url+'jieshao/', headers)
    #print pagedata['url']+'jieshao/'
    #r = br.open('file:///home/myapp/workspace/house/src/main/58.html')
    soup = BeautifulSoup(html)
    v = {}
    v['citycode'] = citycode
    v['detail_url'] = url
    details = soup('table')    
    v['detail'] = re.sub('<img.*?>|style=".*?"| width=".*?"|<a.*?>|</a>|\n|\t|  |class=".*?"','',str(details[0])) 
    v['title'] = rect(v['detail'], '名称：</td><td>(.*?)</td>')
    cityname = rect(html, '<a href="/xiaoqu/">(.*?)小区</a>')
    if rect(v['detail'], '别名：</td><td>(.*?)</td>'):        
        v['othername'] = rect(v['detail'], '别名：</td><td>(.*?)</td>').replace('无','')
    else:
        v['othername'] = ''
    v['wuye'] = rect(v['detail'], '物业公司：</td><td>(.*?)</td>')
    v['kaifa'] = rect(v['detail'], '开发商：</td><td>(.*?)</td>')
    v['wuyefei'] = rect(v['detail'], '物业费：</td><td>(.*?)元/')
    v['green'] = rect(v['detail'], '绿化率：</td><td>(.*?)%')
    
    if rect(v['detail'], '容积率：</td><td>(.*?)</td>'):
        v['rongji'] = rect(v['detail'], '容积率：</td><td>(.*?)</td>').replace('&nbsp;','')
    else:
        v['rongji'] = ''
    subinfolist =  soup.find('div',{'class':'subinfolist'})
    b = subinfolist("b")
    v['avg'] =  str(b[0].string)
    if b[1]['class'] == 'icon_up':
        v['percent_change'] =  str(b[1].string)
    else:
        v['percent_change'] =  "-"+str(b[1].string)    
    if v['percent_change']:
        v['percent_change'] = re.sub(' |%','',v['percent_change'])
    addr = rect(v['detail'], '地址：</td><td>(.*?)</td>')
    if addr:
        addr = addr.replace('…','')
    
    area = rect(v['detail'], '板块：</td><td>(.*?)</td>')
    area =re.sub(' |&nbsp;','',area)
    if rect(v['detail'], '建筑年代：</td><td>(.*?)</td>'):
        v['startyear'] = rect(v['detail'], '建筑年代：</td><td>(.*?)</td>').replace('暂无资料','')
    else:
        v['startyear'] = ''    
    
    if area and area.find('-') !=-1:
        v['area'] =  area.split('-')[0]
        if v['area']  ==cityname:
            v['area'] =area.split('-')[1]
            v['block'] = ''
        else:        
            v['block'] = area.split('-')[1]
    else:
         v['area'] = ''
         v['block'] = ''
    
    v['addr'] = addr
    
    peitao = str(details[2])
    if peitao:
        v['peitao'] = re.sub('  |<a.*?>|</a>|\r|\n|\t|class=".*?"','',peitao)
    else:
        v['peitao'] = ''
    train = str(details[1])
    v['train'] = re.sub('  |<a.*?>|</a>|\r|\n|\t|查看地图|class=".*?"','',train)
    about = str(soup.find('p', {'class':'p_info'}))
    if about:
        about = re.sub('  |\||\r|\n|\t|class=".*?"','',about)
        v['about'] = about.replace('div','p')
    else:
        v['about'] = ''
    map_r = collectOne(url_map, headers)
    if map_r:        
        px =rect(map_r, "lat = '(.*?)'")
        py =rect(map_r, "lon = '(.*?)'")
        v['x'] = px
        v['y'] = py
    else:
        v['x'] = ''
        v['y'] = ''
    draw_r = collectOne(url_drawn, headers)
    pic_r = collectOne(url_pic, headers)
    soup_d =BeautifulSoup(draw_r)
    soup_p =BeautifulSoup(pic_r)
    drawImg = []
    comImg = []     
    if int(soup_d.find(text=u"户型图").nextSibling.b.string) >0:
        piclist_con = soup_d.find('div',{"id":"piclist_con"})
        imgs = rects(str(piclist_con), 'src="(.*?)"')
        for img in imgs:
            drawImg.append(img)
        v['drawImg'] = downImg(drawImg,drawpath+"\\"+citycode+"\\")
        #v['drawImg'] = downImg(drawImg,"/home/myapp/workspace/wwwroot/jjr/upfile/borough/drawing/suzhou/")
    else:
        v['drawImg'] = ''
    if int(soup_p.find(text=u"实景图").nextSibling.b.string) >0:
        piclist_con1 = soup_p.find('div',{"id":"piclist_con"})
        imgs1 = rects(str(piclist_con1), 'src="(.*?)"')
        for img1 in imgs1:
            comImg.append(img1)
        print compath+"\\"+citycode+"\\"
        v['comImg'] = downImg(comImg,compath+'\\'+citycode+"\\")
        #v['comImg'] = downImg(comImg,"/home/myapp/workspace/wwwroot/jjr/upfile/borough/picture/suzhou/")
    else:
        v['comImg'] =''
    #/home/myapp/workspace/wwwroot/jjr/upfile/borough/drawing/
    
    return v
def downImg(img,fr):
    if not img:
        return ''
    else:
        imgT =''
        n = len(img)
        for i in range(0,n):
            if i < 5:
                name                  = hashlib.md5(img[i]).hexdigest().lower()
                dowmimg               = {}
                dowmimg['TrueUrl']    = img[i]
                dowmimg['SaveFile']   = name+os.path.splitext(img[i])[-1]
                if downjpg(dowmimg['TrueUrl'],fr + dowmimg['SaveFile']):
                    imgT += dowmimg['SaveFile']+','   
    return imgT
def downjpg(url,filename):
    try:          
        urllib.urlretrieve(url,filename)
    except Exception,what:
        #print what
        return False
    else:
        print filename
        if os.path.getsize(filename)>8000:
            return True
        else:
            return False
def loopComUrl():
    pass
    sqli.query("select * from borough")
    res = sqli.show()
    for row in res:
        try:    
            r =fetchComCon(row['url'])
            post = urllib.urlencode(r)
            posturl = "http://ks.jjr360.com/api3.php"
            print posturl
            print "---------------------------------------------------------"
            back = urllib2.urlopen(posturl, post)
            print back.read()
        except:
            pass
        
        
if __name__ == "__main__":
    #url = "http://su.58.com/xiaoqu/szkunshan/pn57/"
    #fetchComUrl(url)
    #getLink()
    loopComUrl()
    
