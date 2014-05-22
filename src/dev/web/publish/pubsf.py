#!/usr/bin/env python
# -*- coding: utf-8 -*-
from database import *
import urllib,urllib2,json,re,time
from BeautifulSoup import BeautifulSoup
import MySQLdb
from urlparse import urlparse
import threading
import random
import time
from Queue import Queue
import traceback 
citycode = "sh"
conn  = MySQLdb.Connect(host="localhost",user="dbuser",passwd="201108",db="house",charset="utf8")
cr = conn.cursor()
Q = []



#===============================================================================
# 赶集押金
#===============================================================================
def depositDict():
    dHtml = """    
    <select name="pay_type_int" id="pay_type_int">
        <option value="1">押一付三</option>
        <option value="2">面议</option>
        <option value="3">押一付一</option>
        <option value="4">押一付二</option>
        <option value="5">押二付一</option>
        <option value="9">押二付三</option>
        <option value="6">半年付不押</option>
        <option value="7">年付不押</option>
        <option value="8">押一付半年</option>
        <option value="10">押一付年</option>
        <option value="11">押二付年</option>
        <option value="12">押三付年</option>
    </select>
    """
    soup = BeautifulSoup(dHtml)
    options =  soup("option")
    for row in options:
        pass#print '"%s":"%s",' % (row['value'],row.string)
    option_deposit = {
                    "1":"押一付三",
                    "2":"面议",
                    "3":"押一付一",
                    "4":"押一付二",
                    "5":"押二付一",
                    "9":"押二付三",
                    "6":"半年付不押",
                    "7":"年付不押",
                    "8":"押一付半年",
                    "10":"押一付年",
                    "11":"押二付年",
                    "12":"押三付年"
                      }
    

def towardDict():
    tHtml = """
    <select name="chaoxiang" id="chaoxiang" autocomplete="off">
        <option value="1">东</option>
        <option value="2">南</option>
        <option value="3">西</option>
        <option value="4">北</option>
        <option value="5">东西</option>
        <option value="6">南北</option>
        <option value="7">东南</option>
        <option value="8">东北</option>
        <option value="9">西南</option>
        <option value="10">西北</option>
    </select>
    """
    soup = BeautifulSoup(tHtml)
    options =  soup("option")
    for row in options:
        pass#print '"%s":"%s",' % (row['value'],row.string)
    option_toward = {
                    "1":"东",
                    "2":"南",
                    "3":"西",
                    "4":"北",
                    "5":"东西",
                    "6":"南北",
                    "7":"东南",
                    "8":"东北",
                    "9":"西南",
                    "10":"西北"
                     }
    print option_toward
def housTypeDict():
    tHtml = """
    <select name="fang_xing" id="fang_xing" autocomplete="off">
        <option value="2">平房/四合院</option>
        <option value="3">普通住宅</option>
        <option value="4">公寓</option>
        <option value="5">商住楼</option>
        <option value="7">别墅</option>
        <option value="8">其他</option>
    </select>
    """
    soup = BeautifulSoup(tHtml)
    options =  soup("option")
    for row in options:
        print '"%s":"%s",' % (row['value'],row.string)
    option_housType = {
                    "2":"平房/四合院",
                    "3":"普通住宅",
                    "4":"公寓",
                    "5":"商住楼",
                    "7":"别墅",
                    "8":"其他",
                     }
def ftimentDict():
    fHtml = """
    <select name="zhuangxiu" id="zhuangxiu" autocomplete="off">
        <option value="0">装修情况</option>
        <option value="1">豪华装修</option>
        <option value="2">精装修</option>
        <option value="3">中等装修</option>
        <option value="4">简单装修</option>
        <option value="5">毛坯</option>
    </select>
    """
    soup = BeautifulSoup(fHtml)
    options =  soup("option")
    for row in options:
        print '"%s":"%s",' % (row['value'],row.string)
    option_fitment = {
                "1":"豪华装修",
                "2":"精装修",
                "3":"中等装修",
                "4":"简单装修",
                "5":"毛坯",
                     }
def cityArea(city):
    sql = """
    DROP TABLE IF EXISTS `region_gj`;
    CREATE TABLE IF NOT EXISTS `region_gj` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `regionname` varchar(25) NOT NULL,
      `regioncode` varchar(25) NULL,
      `regionvalue` int(11) NULL,
      `city` int(11) NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;
    
    DROP TABLE IF EXISTS `section_gj`;
    CREATE TABLE IF NOT EXISTS `section_gj` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `sectionname` varchar(25) NOT NULL,
      `sectioncode` varchar(25) NULL,
      `sectionvalue` int(11) NULL,
      `region` int(11) NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;
    
    DROP TABLE IF EXISTS `borough_gj`;
    CREATE TABLE IF NOT EXISTS `borough_gj` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `name` varchar(80) NOT NULL,
      `letter` varchar(80) NOT NULL,
      `addr` varchar(180) NULL,
      `region` varchar(50) NULL,
      `section` varchar(50) NULL,
      `region_id` int(11) NULL,
      `section_id` int(11) NULL,
      `url` varchar(250) NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;
    """
    pubUrl = "http://%s.ganji.com/common/pub.php?category=housing&type=5" % city
    streetUrl = "http://%s.ganji.com/ajax/streetOptions.php" % city
    #domain=sh&district_id=2&street_id=-1&with_all_option=1
    
    req = urllib2.Request(pubUrl)
    res = urllib2.urlopen(req).read()
    soup = BeautifulSoup(res)
    select = soup("select",{"name":"district_id"})
    soup = BeautifulSoup(str(select))
    options = soup("option")
    for row in options:
        if row['value']:
            t = row['value'].split(",")
            sql = """insert into region_gj values(null,'%s',null,%d,1);""" % (t[1],int(t[0]))            
            #cr.execute(sql)
    #conn.commit()
    sql = "select id,regionvalue from region_gj"
    cr.execute(sql)
    r = cr.fetchall()
    for jj in r:
        postData = {}
        postData['domain'] = "sh"
        postData['district_id'] = jj[1]   
        postData['street_id'] = "-1"
        postData['with_all_option'] = "1"
        queryData = urllib.urlencode(postData)
        #print postData
        req = urllib2.Request(streetUrl)
        res = urllib2.urlopen(req,queryData).read()   
        j = json.loads(res)  
        for h in j:
            print h[0],h[1]
            if h[0] >= 0:
                sql = """insert into section_gj values(null,'%s',null,%d,%d);""" % (h[1],int(h[0]),jj[0])   
                print sql  
                cr.execute(sql)
        conn.commit()
       
def getBorgoughContent(url):
    info = {}
    info["url"] = url
    url = url.replace("view","round")
    res = urllib2.urlopen(url).read()
    res = re.sub("\n|\r|\t|  ","",res)
    soup = BeautifulSoup(res)
    h =  urlparse(url)
    
    info["name"] = soup.h4.string    
    print url
    info["letter"] = ''
    info["addr"] = soup.h4.nextSibling.string.replace("地址：","")
    
    area = ""
    if re.search("bread_crumb\">(.*?)</div>",res):
        area = re.search("bread_crumb\">(.*?)</div>",res).group(1)
    area = re.sub("<.*?>","",area).replace("首页 &gt;小区房价 &gt;","")
    tt = area.split("&gt")
    info['region'] = tt[0]
    info['section'] = tt[1]
    
    del soup
    del res
    del area
    del url
    if info not in Q:
        Q.append(info)
    del info
         

def test_job(url, sleep = 0.001 ):
    try:
        getBorgoughContent(url)
    except:
        print traceback.format_exc() 
        pass
    return  url
def getBoroughUrl(url):
    import socket
    socket.setdefaulttimeout(10)
    res = urllib2.urlopen(url).read()
    soup = BeautifulSoup(res)
    a = soup.findAll("div",{"class":"pic"})
    workerArr = []
    j = 0
    for i in a:
        bUrl = i.a['href']
        workerArr.append(Producer(bUrl))
        time.sleep(random.randrange(10)/10.0)
        workerArr[j].start()
        j = j+1
def getBorough():
    cc = Consumer()
    cc.start()
    for i in range(878):
        url = "http://esf.%s.soufun.com/housing/__0_0_0_0_%d/" % (citycode,i)
        getBoroughUrl(url)
        
class Producer(threading.Thread):
    def __init__(self,url):
        threading.Thread.__init__(self)
        self.url = url

    def run(self):
        getBorgoughContent(self.url)

class Consumer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)


    def run(self):
        while 1:
            time.sleep(0.1)
            if Q:
                row = Q.pop()
                try:
                    sql ="insert into borough_sf(name,letter,addr,region,section,url) values('%s','%s','%s','%s','%s','%s')" % (row['name'],row['letter'],row['addr'],row['region'],row['section'],row['url'])
                    cr.execute(sql)
                    conn.commit()
                except:
                    print traceback.format_exc() 
                    pass
       
if __name__ == "__main__":
    #getBorough("sh")
    getBorgoughContent("http://shanghai.anjuke.com/community/view/3642")
    #getBorough()
    
    
    
        