#coding=UTF-8
'''
Created on 2011-7-6

@author: Administrator
'''
from urlparse import urlparse
import cookielib
import urllib2,urllib
from pyquery.pyquery import PyQuery
import re
import time
import datetime
import urllib2
from lxml import etree
import datetime
import time
from urlparse import urlparse
import re
from lxml.cssselect import CSSSelector
import mimetypes
import cookielib
import simplejson as js
import random
from config import housetype, checkPath, makePath,fitment,toward,deposit
import threading
from BeautifulSoup import BeautifulSoup
homepath="d:\\home\\spider\\"
class LinkCrawl(object):
    def __init__(self,citycode="",kind=""):
        cj = cookielib.MozillaCookieJar()
        self.br=urllib2.build_opener(urllib2.HTTPHandler(),urllib2.HTTPCookieProcessor(cj),urllib2.HTTPRedirectHandler())
        self.header={
            "User-Agent":'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB6.6; .NET CLR 3.5.30729)',
        }
        self.endtime=str(datetime.date.today() -datetime.timedelta(days=7))  
        self.clinks=[]
        self.pn=[]
        self.citycode=citycode
        self.baseUrl="http://%s.58.com"%self.citycode
        self.kind=kind
        if kind=="1":#1出售
            self.urlpath="/ershoufang/h1/pn%s/"
        elif kind=="2":#出租
            self.urlpath="/zufang/0/pn%s/"
        elif kind=="3":#求购
            self.urlpath="/ershoufang/h2/pn%s/"
        elif kind=="4":#求租
            self.urlpath="/qiuzu/0/pn%s/"
    
    def __getAllNeedLinks(self):
        cond=True
        idx=0
        checkit="0"
        while  cond:
            url=self.baseUrl+self.urlpath%(str(idx+1))
            print url
            req=urllib2.Request(url, None, self.header)
            p=self.br.open(req).read()
            check=PyQuery(p)("div.pager strong span").text()
            if check==checkit:
                break
            else:
                checkit=check
                if self.kind=="1" or self.kind=="3":
                    links=PyQuery(p)("table.tbimg td.t")
                elif self.kind=="2" or self.kind=="4":
                    links=PyQuery(p)("table.tblist tr")
                print len(links)
                for link in links:
                    if self.kind=="1" or self.kind=="3":
                        if re.search(ur'''更新时间：(.*)''',PyQuery(link).text()):
                            tm=re.search(ur'''更新时间：(.*)''',PyQuery(link).text()).group(1)
                    elif self.kind=="2"or self.kind=="4":
                        tm=PyQuery(link)("td.tc").eq(2).text()
                    if u"今天" in tm:
                        pass
                    elif u"小时" in tm:
                        pass
                    elif u"分钟" in tm:
                        pass
                    else:
                        Y=int(time.strftime('%Y', time.localtime()))
                        ttt="%s-%s"%(Y,tm)
                        if ttt<self.endtime:
                            break
                    lk=PyQuery(link)("a.t").attr("href")
                    if lk not in self.clinks:
                        self.clinks.append(lk)
            idx=idx+1
        print len(self.clinks)
    def runme(self):
#        self.__initPageNum()
        self.__getAllNeedLinks()
        print len(self.clinks)
        return self.clinks
    
class ContentCrawl(object):
    def __init__(self,links,citycode,kind):
        cj = cookielib.MozillaCookieJar()
        self.br=urllib2.build_opener(urllib2.HTTPHandler(),urllib2.HTTPCookieProcessor(cj),urllib2.HTTPRedirectHandler())
        self.pdb={}
        self.header={
            "User-Agent":'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB6.6; .NET CLR 3.5.30729)',
        }
        self.urls=links
        self.kind=kind
        self.fd={}
        self.citycode=citycode
        
        if kind=="1":
            self.folder="sell\\"
        if kind=="2":
            self.folder="rent\\"
        if kind=="3":
            self.folder="buy\\"
        else:
            self.folder="req\\"
        #js resgx
        
        self.agencyname_regex="agencyname:'(.*)',"
        self.username_regex="username:'(.*?)',"
        self.house_room_regex="(\d+)室"
        self.house_hall_regex="(\d+)厅"
        self.house_toilet_regex="(\d+)卫"
        self.borough_name_regex="<li><i>小区：</i>(.*?)</li>"
        self.borough_name1_regex="<li><i>小区：</i>(.*?)</a>"
        self.house_addr_regex="<li><i>地段：</i>(.*?)</li>"
        self.house_floor_regex="第(\d+)层"
        self.house_topfloor_regex="共(\d+)层"
        self.house_price_regex=""
        self.belong_regex="<li><i>产权：</i>(.*)</li>"
        self.house_age_regex="(\d+)年"
        self.house_totalarea_regex="(\d+)㎡"
        self.house_totalarea_req_regex="(\d+)-(\d+)㎡"
        self.house_title_regex="<h1>(.*)</h1>"
        
    def __addText(self,tag, no_tail=False):
        text = []
        if tag.text:
            text.append(tag.text)
        for child in tag.getchildren():
            text.append(self.__addText(child))
        if not no_tail and tag.tail:
            text.append(tag.tail)
        return "".join(text)
    def getText(self,html):
        text=[]
        for tag in html:
            text.append(self.__addText(tag, no_tail=True))
        return ' '.join([t.strip() for t in text if t.strip()])
    def ChuShou(self,url):
        self.fd['house_flag'] = 1        
        request = urllib2.Request(url, None, self.header)
        response = urllib2.urlopen(request).read()
        tree = etree.HTML(response)
        soup =BeautifulSoup(response)
        
        detail_mer = soup.find('ul',{'class':'info'})
        detail_mer_str =str(detail_mer).replace(" ", "")
        #非个人房源 return
        #print re.search(self.agencyname_regex, response).group(1)
        if re.search(self.agencyname_regex, response):
            agencyname=re.search(self.agencyname_regex, response).group(1)
            if agencyname != '个人房源':return            
        else:
            return 
        
        if re.search(self.username_regex, response):
            username=re.search(self.username_regex, response).group(1)
            self.fd['owner_name'] = username
        else:             
            self.fd['owner_name'] = None

        owner_phone = soup('img')
        self.fd['owner_phone'] = ''
        for phone in owner_phone:
            if phone['src'].find('http://image.58.com/showphone.aspx') != -1:
                self.fd['owner_phone'] = phone['src']
            
        #没有联系方式  return
        if not self.fd['owner_phone']:return 
        
        if soup.find('div',{"class":'other'}):
            posttime = soup.find('div',{"class":'other'}).contents[0]                            
            posttime = re.sub('\n|\r| |\t','',posttime)
            posttime = posttime.replace('发布时间：','').replace('　浏览','')
        else:
            posttime = ''
                            
        if not posttime:
            return                            
        elif posttime.find('-') !=-1:
            s = datetime.datetime(int(posttime.split('-')[0]),int(posttime.split('-')[1],),int(posttime.split('-')[2]))
            posttime = int(time.mktime(s.timetuple()))
        elif posttime.find('分钟') !=-1:
            n = int(posttime.replace('分钟前',''))*60
            posttime = int(time.time() - n)
        elif posttime.find('小时') !=-1:
            n = int(posttime.replace('小时前',''))*60*60
            posttime = int(time.time() - n)
        self.fd['posttime'] = posttime
                            
        if (time.time() - self.fd['posttime']) > 3600*24*7: 
            return
            print "++++++++++++++++"                 
        print time.strftime('%Y %m %d', time.localtime(self.fd['posttime']))    
        
        if re.search(self.house_floor_regex, detail_mer_str):
            house_floor=re.search(self.house_floor_regex, detail_mer_str).group(1)
            self.fd['house_floor']  = house_floor
        else:
            self.fd['house_floor'] = None
            
        if re.search(self.house_topfloor_regex, detail_mer_str):
            house_topfloor=re.search(self.house_topfloor_regex, detail_mer_str).group(1)
            self.fd['house_topfloor'] = house_topfloor
        else:
            self.fd['house_topfloor'] = None   
        
        if re.search(self.house_totalarea_regex, detail_mer_str):
            house_totalarea=re.search(self.house_totalarea_regex, detail_mer_str).group(1)
            self.fd['house_totalarea'] = house_totalarea
        else:
            self.fd['house_totalarea'] = None
            
        #类型 
        self.fd['house_type'] = housetype(detail_mer_str) 
            
        self.fd['house_price'] = detail_mer.em.string  
            
        if re.search(self.house_room_regex, detail_mer_str):
            house_room=re.search(self.house_room_regex, detail_mer_str).group(1)
            self.fd['house_room'] = house_room
        else:
            self.fd['house_room'] = '0'
            
        if re.search(self.house_hall_regex, detail_mer_str):
            house_hall=re.search(self.house_hall_regex, detail_mer_str).group(1)
            self.fd['house_hall'] = house_hall
        else:
            self.fd['house_hall'] = '0'
        
        if re.search(self.house_toilet_regex, detail_mer_str):
            house_toilet=re.search(self.house_toilet_regex, detail_mer_str).group(1)
            self.fd['house_toilet'] = house_toilet
        else:
            self.fd['house_toilet'] = '0'
        
        if re.search(self.house_title_regex, response):
            house_title=re.search(self.house_title_regex, response).group(1)
            self.fd['house_title'] = house_title
        else:
            self.fd['house_title'] = ''
        
        #描述        
        detail_box = soup.find('div',{'class':'maincon'})
        if detail_box:
            house_desc = str(detail_box)
            self.fd['house_desc'] = re.sub("<.*?>|\n|\r|\t|联系我时，请说是在58同城上看到的，谢谢！","",house_desc)
        else:
            self.fd['house_desc'] = None

        #小区名
        if re.search(self.borough_name_regex, detail_mer_str):
            borough_name=re.search(self.borough_name_regex, detail_mer_str).group(1)
            self.fd['borough_name'] = re.sub("\(.*\)|<.*?>","",borough_name)
            
        else:
            self.fd['borough_name'] = ''
        
        #区域     
        try:
            area_box = detail_mer.find(text="区域：").parent.parent
            area_a = area_box('a')
            if area_a and len(area_a)>1:
                self.fd['cityarea'] = area_a[0].string
                self.fd['section'] = area_a[1].string
            elif area_a and len(area_a)==1:
                self.fd['cityarea'] = area_a[0].string
                self.fd['section'] = None
            else:
                self.fd['cityarea'] = None
                self.fd['section'] = None
        except:
            self.fd['cityarea'] = None
            self.fd['section'] = None
            
        
        if re.search(self.house_age_regex, response):
            house_age=re.search(self.house_age_regex, response).group(1)
            self.fd['house_age'] = house_age
        else:
            self.fd['house_age'] = None
            
        #朝向
        self.fd['house_toward'] = toward(detail_mer_str)    
        self.fd['house_fitment'] = fitment(detail_mer_str)
        
    def QiuGou(self,url):
        self.fd['city'] = ''        
        self.fd['house_flag'] = 3
        request = urllib2.Request(url, None, self.header)
        response = urllib2.urlopen(request).read()
        tree = etree.HTML(response)
        soup =BeautifulSoup(response)
        
        detail_mer = soup.find('ul',{'class':'info'})
        detail_mer_str =str(detail_mer).replace(" ", "")
        #非个人房源 return
        #print re.search(self.agencyname_regex, response).group(1)
        if re.search(self.agencyname_regex, response):
            agencyname=re.search(self.agencyname_regex, response).group(1)
            if agencyname != '个人房源':return            
        else:
            return 
        
        if re.search(self.username_regex, response):
            username=re.search(self.username_regex, response).group(1)
            self.fd['owner_name'] = username
        else:             
            self.fd['owner_name'] = None

        owner_phone = soup('img')
        self.fd['owner_phone'] = ''
        for phone in owner_phone:
            if phone['src'].find('http://image.58.com/showphone.aspx') != -1:
                self.fd['owner_phone'] = phone['src']
            
        #没有联系方式  return
        if not self.fd['owner_phone']:return
        
        if soup.find('div',{"class":'other'}):
            posttime = soup.find('div',{"class":'other'}).contents[0]                            
            posttime = re.sub('\n|\r| |\t','',posttime)
            posttime = posttime.replace('发布时间：','').replace('　浏览','')
        else:
            posttime = ''
                            
        if not posttime:
            return                            
        elif posttime.find('-') !=-1:
            s = datetime.datetime(int(posttime.split('-')[0]),int(posttime.split('-')[1],),int(posttime.split('-')[2]))
            posttime = int(time.mktime(s.timetuple()))
        elif posttime.find('分钟') !=-1:
            n = int(posttime.replace('分钟前',''))*60
            posttime = int(time.time() - n)
        elif posttime.find('小时') !=-1:
            n = int(posttime.replace('小时前',''))*60*60
            posttime = int(time.time() - n)
        self.fd['posttime'] = posttime
                            
        if (time.time() - self.fd['posttime']) > 3600*24*7: 
            return
            print "++++++++++++++++"                 
        print time.strftime('%Y %m %d', time.localtime(self.fd['posttime']))    
        
        self.fd['house_floor'] = 0
        self.fd['house_topfloor'] = 0 
        
        if re.search(self.house_totalarea_req_regex, detail_mer_str):
            house_totalarea_min=re.search(self.house_totalarea_req_regex, detail_mer_str).group(1)
            house_totalarea_max=re.search(self.house_totalarea_req_regex, detail_mer_str).group(2)
            self.fd['house_totalarea'] = house_totalarea_min
            self.fd['house_totalarea_max'] = house_totalarea_max
            self.fd['house_totalarea_min'] = house_totalarea_min
        else:
            if re.search(self.house_totalarea_regex, detail_mer_str):
                house_totalarea=re.search(self.house_totalarea_regex, detail_mer_str).group(1)
                self.fd['house_totalarea'] = house_totalarea
                self.fd['house_totalarea_max'] = house_totalarea
                self.fd['house_totalarea_min'] = house_totalarea
            else:                
                self.fd['house_totalarea'] = 0
                self.fd['house_totalarea_max'] = 0
                self.fd['house_totalarea_min'] = 0
            
        #类型 
        self.fd['house_type'] = housetype(detail_mer_str)
           
        house_price = detail_mer.em.string
        if house_price.find('-'):
            self.fd['house_price_max'] = int(house_price.split('-')[0])
            self.fd['house_price_min'] = int(house_price.split('-')[1])
            self.fd['house_price'] = int(house_price.split('-')[0])
        else:
            self.fd['house_price_min']  = int(house_price)
            self.fd['house_price_min'] = int(house_price)
            self.fd['house_price'] = int(house_price)        
            
        if re.search(self.house_room_regex, detail_mer_str):
            house_room=re.search(self.house_room_regex, detail_mer_str).group(1)
            self.fd['house_room'] = house_room
            self.fd['house_room1'] = house_room
        else:
            self.fd['house_room'] = '0'
            self.fd['house_room1'] = '0'
            
        self.fd['house_hall'] = '0'
        self.fd['house_toilet'] = '0'
        self.fd['house_toilet'] = '0'
        
        if re.search(self.house_title_regex, response):
            house_title=re.search(self.house_title_regex, response).group(1)
            self.fd['house_title'] = house_title
        else:
            self.fd['house_title'] = ''
        
        #描述        
        detail_box = soup.find('div',{'class':'maincon'})
        if detail_box:
            house_desc = str(detail_box)
            self.fd['house_desc'] = re.sub("<.*?>|\n|\r|\t|联系我时，请说是在58同城上看到的，谢谢！","",house_desc)
        else:
            self.fd['house_desc'] = None

        #小区名
        if re.search(self.house_addr_regex, detail_mer_str):
            house_addr = re.search(self.house_addr_regex, detail_mer_str).group(1)
            self.fd['house_addr'] = house_addr
            self.fd['borough_name'] = house_addr
            
        else:
            self.fd['house_addr'] = ''
            self.fd['borough_name'] = ''   
        
        #区域     
        #print detail_mer
        area_box = detail_mer.find(text="地段：").parent.parent
        area_a = area_box('a')
        if area_a and len(area_a)>1:
            self.fd['cityarea'] = area_a[0].string
            self.fd['section'] = area_a[1].string
        elif area_a and len(area_a)==1:
            self.fd['cityarea'] = area_a[0].string
            self.fd['section'] = None
        else:
            self.fd['cityarea'] = None
            self.fd['section'] = None
        
        self.fd['house_age'] = 0
            
        #朝向
        self.fd['house_toward'] = 0
        self.fd['house_fitment'] = 0
                    
    def ChuZu(self,url):
        self.fd['house_flag'] = 2
        request = urllib2.Request(url, None, self.header)
        response = urllib2.urlopen(request).read()
        tree = etree.HTML(response)  
        soup =BeautifulSoup(response)
        detail_mer = soup.find('ul',{'class':'info'})
        detail_mer_str =re.sub("\n|\t\r| ","",str(detail_mer))
        #print detail_mer_str
        #非个人房源 return
        #print re.search(self.agencyname_regex, response).group(1)
        if re.search(self.agencyname_regex, response):
            agencyname=re.search(self.agencyname_regex, response).group(1)
            if agencyname != '个人房源':return            
        else:
            return
                
        if re.search(self.username_regex, response):
            username=re.search(self.username_regex, response).group(1)
            self.fd['owner_name'] = username
        else:             
            self.fd['owner_name'] = None

        owner_phone = soup('img')
        self.fd['owner_phone'] = ''
        for phone in owner_phone:
            if phone['src'].find('http://image.58.com/showphone.aspx') != -1:
                self.fd['owner_phone'] = phone['src']
            
        #没有联系方式  return
        if not self.fd['owner_phone']:return 
        
        if soup.find('div',{"class":'other'}):
            posttime = soup.find('div',{"class":'other'}).contents[0]                            
            posttime = re.sub('\n|\r| |\t','',posttime)
            posttime = posttime.replace('发布时间：','').replace('　浏览','')
        else:
            posttime = ''
                            
        if not posttime:
            return                            
        elif posttime.find('-') !=-1:
            s = datetime.datetime(int(posttime.split('-')[0]),int(posttime.split('-')[1],),int(posttime.split('-')[2]))
            posttime = int(time.mktime(s.timetuple()))
        elif posttime.find('分钟') !=-1:
            n = int(posttime.replace('分钟前',''))*60
            posttime = int(time.time() - n)
        elif posttime.find('小时') !=-1:
            n = int(posttime.replace('小时前',''))*60*60
            posttime = int(time.time() - n)
        self.fd['posttime'] = posttime
                            
        if (time.time() - self.fd['posttime']) > 3600*24*7: 
            return
            print "++++++++++++++++"                 
        print time.strftime('%Y %m %d', time.localtime(self.fd['posttime']))    
        
        if re.search(self.house_floor_regex, detail_mer_str):
            house_floor=re.search(self.house_floor_regex, detail_mer_str).group(1)
            self.fd['house_floor']  = house_floor
        else:
            self.fd['house_floor'] = None
            
        if re.search(self.house_topfloor_regex, detail_mer_str):
            house_topfloor=re.search(self.house_topfloor_regex, detail_mer_str).group(1)
            self.fd['house_topfloor'] = house_topfloor
        else:
            self.fd['house_topfloor'] = None   
        
        if re.search(self.house_totalarea_regex, detail_mer_str):
            house_totalarea=re.search(self.house_totalarea_regex, detail_mer_str).group(1)
            self.fd['house_totalarea'] = house_totalarea
        else:
            self.fd['house_totalarea'] = None
            
        #类型 
        self.fd['house_type'] = housetype(detail_mer_str) 
            
        self.fd['house_price'] = detail_mer.em.string  
            
        if re.search(self.house_room_regex, detail_mer_str):
            house_room=re.search(self.house_room_regex, detail_mer_str).group(1)
            self.fd['house_room'] = house_room
        else:
            self.fd['house_room'] = '0'
            
        if re.search(self.house_hall_regex, detail_mer_str):
            house_hall=re.search(self.house_hall_regex, detail_mer_str).group(1)
            self.fd['house_hall'] = house_hall
        else:
            self.fd['house_hall'] = '0'
        
        if re.search(self.house_toilet_regex, detail_mer_str):
            house_toilet=re.search(self.house_toilet_regex, detail_mer_str).group(1)
            self.fd['house_toilet'] = house_toilet
        else:
            self.fd['house_toilet'] = '0'
        
        if re.search(self.house_title_regex, response):
            house_title=re.search(self.house_title_regex, response).group(1)
            self.fd['house_title'] = house_title
        else:
            self.fd['house_title'] = ''
        
        #描述        
        detail_box = soup.find('div',{'class':'maincon'})
        if detail_box:
            house_desc = str(detail_box)
            self.fd['house_desc'] = re.sub("<.*?>|\n|\r|\t|联系我时，请说是在58同城上看到的，谢谢！","",house_desc)
        else:
            self.fd['house_desc'] = None

        #小区名
        if re.search(self.borough_name_regex, detail_mer_str):
            borough_name=re.search(self.borough_name_regex, detail_mer_str).group(1)
            self.fd['borough_name'] = re.sub("\(.*\)|<.*?>","",borough_name)
        else:
            self.fd['borough_name'] = ''
        
        #区域     
        area_box = detail_mer.find(text="区域：").parent.parent
        area_a = area_box('a')
        if area_a and len(area_a)>1:
            self.fd['cityarea'] = area_a[0].string
            self.fd['section'] = area_a[1].string
        elif area_a and len(area_a)==1:
            self.fd['cityarea'] = area_a[0].string
            self.fd['section'] = None
        else:
            self.fd['cityarea'] = None
            self.fd['section'] = None
        
        if re.search(self.house_age_regex, response):
            house_age=re.search(self.house_age_regex, response).group(1)
            self.fd['house_age'] = house_age
        else:
            self.fd['house_age'] = None
            
        #朝向
        self.fd['house_toward'] = toward(detail_mer_str)    
        self.fd['house_fitment'] = fitment(detail_mer_str)        
        self.fd['house_deposit'] = deposit(detail_mer_str)
        
    def QiuZu(self,url):
        self.fd['house_flag'] = 3
        self.fd['house_floor'] = 0
        self.fd['house_topfloor'] = 0        
        self.fd['house_age'] = 0
        self.fd['house_toward'] = 0
        self.fd['house_fitment'] = 0
        self.fd['house_deposit'] = 0
        self.fd['house_totalarea_max'] = 0
        self.fd['house_totalarea_min'] = 0
        self.fd['house_totalarea'] = 0
        request = urllib2.Request(url, None, self.header)
        response = urllib2.urlopen(request).read()
        tree = etree.HTML(response)        
        soup =BeautifulSoup(response)
        
        
        detail_mer = soup.find('ul',{'class':'info'})
        detail_mer_str =str(detail_mer).replace(" ", "")
        #非个人房源 return
        #print re.search(self.agencyname_regex, response).group(1)
        if re.search(self.agencyname_regex, response):
            agencyname=re.search(self.agencyname_regex, response).group(1)
            if agencyname == '经纪人':return            
        else:
            return 
        
        if re.search(self.username_regex, response):
            username=re.search(self.username_regex, response).group(1)
            self.fd['owner_name'] = username
        else:             
            self.fd['owner_name'] = None

        owner_phone = soup('img')
        self.fd['owner_phone'] = ''
        for phone in owner_phone:
            if phone['src'].find('http://image.58.com/showphone.aspx') != -1:
                self.fd['owner_phone'] = phone['src']
            
        #没有联系方式  return
        if not self.fd['owner_phone']:return
        
        if soup.find('div',{"class":'other'}):
            posttime = soup.find('div',{"class":'other'}).contents[0]                            
            posttime = re.sub('\n|\r| |\t','',posttime.replace("&nbsp;", "　"))
            posttime = posttime.replace('发布时间：','').replace('　浏览','')
        else:
            posttime = ''
        print posttime                     
        if not posttime:
            return                             
        elif posttime.find('-') !=-1:
            s = datetime.datetime(int(posttime.split('-')[0]),int(posttime.split('-')[1],),int(posttime.split('-')[2]))
            posttime = int(time.mktime(s.timetuple()))
        elif posttime.find('分钟') !=-1:
            n = int(posttime.replace('分钟前',''))*60
            posttime = int(time.time() - n)
        elif posttime.find('小时') !=-1:
            n = int(posttime.replace('小时前',''))*60*60
            posttime = int(time.time() - n)
        self.fd['posttime'] = posttime
                            
        if (time.time() - self.fd['posttime']) > 3600*24*7: 
            return
            print "++++++++++++++++"                 
        print time.strftime('%Y %m %d', time.localtime(self.fd['posttime']))    
        
        self.fd['house_floor'] = 0
        self.fd['house_topfloor'] = 0 
        
        if re.search(self.house_totalarea_req_regex, detail_mer_str):
            house_totalarea_min=re.search(self.house_totalarea_req_regex, detail_mer_str).group(1)
            house_totalarea_max=re.search(self.house_totalarea_req_regex, detail_mer_str).group(2)
            self.fd['house_totalarea'] = house_totalarea_min
            self.fd['house_totalarea_max'] = house_totalarea_max
            self.fd['house_totalarea_min'] = house_totalarea_min
        else:
            if re.search(self.house_totalarea_regex, detail_mer_str):
                house_totalarea=re.search(self.house_totalarea_regex, detail_mer_str).group(1)
                self.fd['house_totalarea'] = house_totalarea
                self.fd['house_totalarea_max'] = house_totalarea
                self.fd['house_totalarea_min'] = house_totalarea
            else:                
                self.fd['house_totalarea'] = 0
                self.fd['house_totalarea_max'] = 0
                self.fd['house_totalarea_min'] = 0
            
        #类型 
        self.fd['house_type'] = housetype(detail_mer_str)
        
        house_price = detail_mer.em.string
        if house_price:
            house_price = house_price.replace('元','')
            if house_price.find("以上") != -1:
                self.fd['house_price_max'] = 0
                self.fd['house_price_min'] = house_price.replace('以上','')
                self.fd['house_price'] = house_price.replace('以上','')
            elif house_price.find("以下") != -1:
                self.fd['house_price_max'] = house_price.replace('以下','')
                self.fd['house_price_min'] = 0
                self.fd['house_price'] = house_price.replace('以下','')
            elif house_price.find("-") != -1:
                self.fd['house_price_max'] = house_price.split('-')[1]
                self.fd['house_price_min'] = house_price.split('-')[0]
                self.fd['house_price'] = house_price.split('-')[0]
            else:
                self.fd['house_price_max'] = 0
                self.fd['house_price_min'] = 0
                self.fd['house_price'] = 0
        else:
            self.fd['house_price_max'] = 0
            self.fd['house_price_min'] = 0
            self.fd['house_price'] = 0

        if re.search(self.house_room_regex, detail_mer_str):
            house_room=re.search(self.house_room_regex, detail_mer_str).group(1)
            self.fd['house_room'] = house_room
            self.fd['house_room1'] = house_room
        else:
            self.fd['house_room'] = '0'
            self.fd['house_room1'] = '0'
            
        self.fd['house_hall'] = '0'
        self.fd['house_toilet'] = '0'
        self.fd['house_toilet'] = '0'
        
        if re.search(self.house_title_regex, response):
            house_title=re.search(self.house_title_regex, response).group(1)
            self.fd['house_title'] = house_title
        else:
            self.fd['house_title'] = ''
        
        #描述        
        detail_box = soup.find('div',{'class':'maincon'})
        if detail_box:
            house_desc = str(detail_box)
            self.fd['house_desc'] = re.sub("<.*?>|\n|\r|\t|联系我时，请说是在58同城上看到的，谢谢！","",house_desc)
        else:
            self.fd['house_desc'] = None

        #小区名
        if re.search(self.house_addr_regex, detail_mer_str):
            house_addr = re.search(self.house_addr_regex, detail_mer_str).group(1)
            self.fd['house_addr'] = house_addr
            self.fd['borough_name'] = house_addr
            
        else:
            self.fd['house_addr'] = ''
            self.fd['borough_name'] = ''   
        
        #区域     
        #print detail_mer
        area_box = detail_mer.find(text="地段：").parent.parent
        area_a = area_box('a')
        if area_a and len(area_a)>1:
            self.fd['cityarea'] = area_a[0].string
            self.fd['section'] = area_a[1].string
        elif area_a and len(area_a)==1:
            self.fd['cityarea'] = area_a[0].string
            self.fd['section'] = None
        else:
            self.fd['cityarea'] = None
            self.fd['section'] = None
        
        self.fd['house_age'] = 0
            
        #朝向
        self.fd['house_toward'] = 0
        self.fd['house_fitment'] = 0
        
   
    def extractDict(self):    
        for url in self.urls:
            if checkPath(homepath,self.folder,url):
                pass
            else:
                self.fd["posttime"] = 0
                if self.kind=="1":
                    self.ChuShou(url)
                elif self.kind=="2":
                    self.ChuZu(url)
                elif self.kind=="3":
                    self.QiuGou(url)
                else:
                    self.QiuZu(url)
                self.fd['city'] = urlparse(url)[1].replace('.58.com',"") 
                #makePath(homepath,self.folder,url)                
                #超过七天
                if (time.time() -self.fd["posttime"]) > 7*24*36000:return
                self.fd["c"]="houseapi"
                self.fd["a"]="savehouse"        
                self.fd["is_checked"] = 0        
                self.fd["web_flag"]   = "58"
                
                if not self.fd["is_checked"]:
                    for i in self.fd.items():
                        print i[0],i[1]
                        
                # req=urllib2.Request("http://site.jjr360.com/app.php", urllib.urlencode(self.fd))
                #p=self.br.open(req).read().strip()
                #print p.decode('gbk')
        
class fetchData(threading.Thread): 
    def __init__(self,d):
        threading.Thread.__init__(self)
        self.d=d
    def run(self):
        lc=LinkCrawl(self.d["citycode"],self.d["kind"])
        clinks=lc.runme()
        cc=ContentCrawl(clinks,self.d["citycode"],self.d["kind"])
        cc.extractDict()
        
if __name__=="__main__":    
    lc=LinkCrawl(citycode="liaoyang",kind="3")
    lc.runme()
    
#    url1 = "http://su.58.com/ershoufang/6432469244037x.shtml"
#    url2 = "http://su.58.com/zufang/6433540736258x.shtml"
#    url3 = "http://su.58.com/ershoufang/6383611408516x.shtml"
#    url4 = "http://su.58.com/qiuzu/6268009935368x.shtml"
#    
#    cc=ContentCrawl(["http://liaoyang.58.com/ershoufang/6433334900867x.shtml"],citycode="su",kind="1")
#    cc.extractDict()