#!/usr/bin/env python
# -*- coding: utf-8 -*-
from database import *
import urllib,urllib2,json,re,time
from BeautifulSoup import BeautifulSoup
import MySQLdb
from urlparse import urlparse
import Queue, threading, sys
from threading import Thread

citycode = "sh"
conn  = MySQLdb.Connect(host="localhost",user="dbuser",passwd="201108",db="house",charset="utf8")
cr = conn.cursor()
Q = []
class Worker(Thread):
    worker_count = 0
    timeout = 1
    def __init__( self, workQueue, resultQueue, **kwds):
        Thread.__init__( self, **kwds )
        self.id = Worker.worker_count
        Worker.worker_count += 1
        self.setDaemon( True )
        self.workQueue = workQueue
        self.resultQueue = resultQueue
        self.start( )

    def run( self ):
        ''' the get-some-work, do-some-work main loop of worker threads '''
        while True:
            try:
                callable, args, kwds = self.workQueue.get(timeout=Worker.timeout)
                res = callable(*args, **kwds)
                #print "worker[%2d]: %s" % (self.id, str(res) )
                self.resultQueue.put( res )
                #time.sleep(Worker.sleep)
            except Queue.Empty:
                break
            except :
                #print 'worker[%2d]' % self.id, sys.exc_info()[:2]
                raise
                
class WorkerManager:
    def __init__( self, num_of_workers=10, timeout = 2):
        self.workQueue = Queue.Queue()
        self.resultQueue = Queue.Queue()
        self.workers = []
        self.timeout = timeout
        self._recruitThreads( num_of_workers )

    def _recruitThreads( self, num_of_workers ):
        for i in range( num_of_workers ):
            worker = Worker( self.workQueue, self.resultQueue )
            self.workers.append(worker)

    def wait_for_complete( self):
        # ...then, wait for each of them to terminate:
        while len(self.workers):
            worker = self.workers.pop()
            worker.join( )
            if worker.isAlive() and not self.workQueue.empty():
                self.workers.append( worker )
        print "All jobs are are completed."

    def add_job( self, callable, *args, **kwds ):
        self.workQueue.put( (callable, args, kwds) )

    def get_result( self, *args, **kwds ):
        return self.resultQueue.get( *args, **kwds )


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
    res = urllib2.urlopen(url).read()
    res = re.sub("\n|\r|\t","",res)
    soup = BeautifulSoup(res)
    h =  urlparse(url)
    info = {}
    info["name"] = soup.h2.string
    info["url"] = url
    print url
    info["letter"] = h[2].replace("/xiaoqu/","")[:-1]
    info["addr"] = ''
    if re.search("小区地址:</td><td>(.*?)</td>",res):
        info["addr"] = re.search("小区地址:</td><td>(.*?)</td>",res).group(1)
    area = ""
    if re.search("所属区域:</td><td class=\"table_wd300\">(.*?)</td>",res):
        area = re.search("所属区域:</td><td class=\"table_wd300\">(.*?)</td>",res).group(1)
    if area:
        soup_area = BeautifulSoup(area)
        l = soup_area("a")
        if len(l) >1:
            info['region'] = l[0].string
            info['section'] = l[1].string
        else:
            info['region'] = l[0].string
            info['section'] = ''
    del soup
    del res
    del area
    del soup_area
    del h
    del url
    del l
    if info not in Q:
        Q.append(info)
    del info
         

def test_job(url, sleep = 0.001 ):
    try:
        getBorgoughContent(url)
    except:
        pass
        #print '[%4d]' % id, sys.exc_info()[:2]
    return  id
def getBoroughUrl(url):
    import socket
    socket.setdefaulttimeout(10)
    
    res = urllib2.urlopen(url).read()
    soup = BeautifulSoup(res)
    a = soup.findAll("a",{"class":"list_title"})
    h = urlparse(url)
    wm = WorkerManager(30)
    for i in a:
        bUrl = "%s://%s%s" % (h[0],h[1],i['href'])
        wm.add_job( test_job, bUrl,0.001)
    wm.wait_for_complete()
   
    for row in Q:
        try:
            sql ="insert into borough_gj(name,letter,addr,region,section,url) values('%s','%s','%s','%s','%s','%s')" % (row['name'],row['letter'],row['addr'],row['region'],row['section'],row['url'])
            cr.execute(sql)
            conn.commit()
            Q.remove(row)
        except:
            pass
    
def getBorough():
    for i in range(629):
        p = 30*i
        url = "http://%s.ganji.com/xiaoqu/f%d/" % (citycode,p)
        getBoroughUrl(url)
        
    


if __name__ == "__main__":
    #getBorough("sh")
    #getBorgoughContent("http://sh.ganji.com/xiaoqu/laoximenxinyuan/")
    getBorough()
    
        