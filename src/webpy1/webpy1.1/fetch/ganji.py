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
        self.baseUrl="http://%s.ganji.com"%self.citycode
        self.kind=kind
        if kind=="1":#出售
            self.urlpath="/fang5/a1u2%s/"
        elif kind=="2":#出租
            self.urlpath="/fang1/u2%s/"
        elif kind=="3":#求购
            self.urlpath="/fang4/u2f0/a1%s/"
        elif kind=="4":#求租
            self.urlpath="/fang2/u2f0/a1%s/"
            
    def __getAllNeedLinks(self):
        cond=True
        idx=0
        checkit="0"
        while  cond:
            url=self.baseUrl+self.urlpath%("f"+str(idx*32))
            #url="http://gz.ganji.com/fang2/u2f0/a1f768/"
            print url
            req=urllib2.Request(url, None, self.header)
            p=self.br.open(req).read()
            check=PyQuery(p)("ul.pageLink li a.c").text()
            if check==checkit:
                break
            else:
                checkit=check
                links=PyQuery(p)("div.list dl")
                print len(links)
                for link in links:
                    lk=self.baseUrl+PyQuery(link)(" a.list_title").attr("href")
                    if self.kind=="3" or self.kind=="4":
                        tm=PyQuery(link)("dd span.time").text()
                        if re.match('''\d{2}-\d{2}''', tm):
                            Y=int(time.strftime('%Y', time.localtime()))
                            tm="%s-%s"%(Y,tm.strip())
                            if tm<self.endtime:
                                break
                        elif "分钟" in tm:
                            pass
                        elif "小时" in tm:
                            pass
                        else:
                            break
                            
                    if lk not in self.clinks:
                        self.clinks.append(lk)
            idx=idx+1
        print len(self.clinks)
    def runme(self):
        #self.__initPageNum()
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
        
        self.xiaoqu_regex="xiaoqu : '(.*?)',"
        self.address_regex="address : '(.*?)',"
        self.house_room_regex="(\d+)室"
        self.house_hall_regex="(\d+)厅"
        self.house_toilet_regex="(\d+)卫"
        self.house_desc_regex="房屋概况</p>(.*?)</p>"
        self.house_floor_regex="<li>楼层: 第(\d+)层/总(\d+)层</li>"
        self.house_totalarea_regex="<li>面积: (\d+) ㎡</li>"
        self.house_totalarea_regex_qiu="(\d+)㎡"   
        self.house_type_regex3="<li>户型: (.*)</li>"        
        self.house_toward_regex="<li>朝向: (.*)</li>"
        self.house_type_regex="<li>类型: (.*)</li>"
        self.cityarea_regex="<li>区域:([\s\S]*?)</li>"
        self.house_age_regex="<li>房龄: (\d+) 年</li>"
        self.house_fitment_regex="<li>装修: (.*)</li>"
        self.house_support_regex="<li>配置: (.*) </li>"
        self.house_price_regex="<li>售价: <span>(.*)</span>.*</li>"
        self.house_price_regex_2="<li>租金: <span>(.*)</span>.*</li>"
        self.borough_name_regex="<li>小区:(.*)</li>"
        self.house_deposit_regex="<li>租金: (.*)</li>"
        self.house_price_regex_zu = "<li>期望租金: (.*)</li>"
        self.borough_name_regex_reg = "<li>期望小区: (.*)</li>"
        self.house_addr_regex_reg = "<li>小区地址:(.*)</li>"
        self.house_price_regex_gou  = "<li>期望售价: (.*)</li>"
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
        self.fd['city'] = self.citycode        
        self.fd['house_flag'] = 1
        self.fd['belong']=""
        request = urllib2.Request(url, None, self.header)
        response = urllib2.urlopen(request).read()
        tree = etree.HTML(response)
        soup =BeautifulSoup(response)
        
        detail_mer = soup.find('div',{'class':'detail_mer'})
        
        #非个人房源 return
        if u"个人房源"  not in str(detail_mer):return        
        
        Dname = detail_mer.find('span',{'class':'Dname'})
        if Dname:
            self.fd['owner_name'] = Dname.string
        else:
            self.fd['owner_name'] = None
            
        ganji_phone_call_class = detail_mer.find('span',{'class':'ganji_phone_call_class'})
        
        if ganji_phone_call_class:
            self.fd['owner_phone'] = ganji_phone_call_class.contents[0]
            if str(ganji_phone_call_class).find('src='):                
                self.fd['owner_phone'] = 'http://'+urlparse(url)[1]+ganji_phone_call_class.img['src']
            else:
                self.fd['owner_phone'] = None            
        else:
            self.fd['owner_phone'] = None
            
            
        #没有联系方式  return
        if not self.fd['owner_phone']:return     
        
        if re.search("<span class=\"city\"><a .*?>(.*?)</a>", response):
            cityname=re.search("<span class=\"city\"><a .*?>(.*?)</a>", response).group(1)
            self.fd['cityname'] = cityname
        else:
            return   
        
        if re.search(self.house_floor_regex, response):
            house_floor=re.search(self.house_floor_regex, response).group(1)
            house_topfloor=re.search(self.house_floor_regex, response).group(2)
            self.fd['house_floor']    = house_floor
            self.fd['house_topfloor'] = house_topfloor
        else:
            self.fd['house_floor'] = None
            self.fd['house_topfloor'] = None   
        
        if re.search(self.house_totalarea_regex, response):
            house_totalarea=re.search(self.house_totalarea_regex, response).group(1)
            self.fd['house_totalarea'] = house_totalarea
        else:
            self.fd['house_totalarea'] = None
            
        #类型 
        if re.search(self.house_type_regex, response):
            house_type=re.search(self.house_type_regex, response).group(1)
            self.fd['house_type'] = housetype(house_type)
        else:
            self.fd['house_type'] = None   
            
        if re.search(self.house_price_regex, response):
            house_price=re.search(self.house_price_regex, response).group(1)
            self.fd['house_price'] = house_price
        else:
            self.fd['house_price'] = None
    
        posttime=CSSSelector('span.pub_time')(tree)!=None and CSSSelector('span.pub_time')(tree)[0].text.strip() or None 
        if posttime:
            Y=int(time.strftime('%Y', time.localtime()))
            M=int(posttime.split(' ')[0].split('-')[0])
            D=int(posttime.split(' ')[0].split('-')[1])
            s = datetime.datetime(Y,M,D,0,0)
            posttime=int(time.mktime(s.timetuple()))
            self.fd['posttime'] =posttime 
        else:
            self.fd['posttime'] =None
            
        if re.search(self.house_room_regex, response):
            house_room=re.search(self.house_room_regex, response).group(1)
            self.fd['house_room'] = house_room
        else:
            self.fd['house_room'] = '0'
            
        if re.search(self.house_hall_regex, response):
            house_hall=re.search(self.house_hall_regex, response).group(1)
            self.fd['house_hall'] = house_hall
        else:
            self.fd['house_hall'] = '0'
        
        if re.search(self.house_toilet_regex, response):
            house_toilet=re.search(self.house_toilet_regex, response).group(1)
            self.fd['house_toilet'] = house_toilet
        else:
            self.fd['house_toilet'] = '0'

        house_title=CSSSelector("div.detail_title h1")(tree)[0] !=None and CSSSelector("div.detail_title h1")(tree)[0].text.strip() or None
        self.fd['house_title'] = house_title
        
        #描述        
        detail_box = soup.find('div',{'class':'detail_box'})
        if detail_box:
            house_desc = str(detail_box('p')[1])
            self.fd['house_desc'] = re.sub("<.*?>|\n|\r|\t|联系我时请说明是从赶集网上看到的","",house_desc)
        else:
            self.fd['house_desc'] = None

        d_i = soup.find('ul',{'class':'d_i'})
        
        #小区名
        #先处理JS
        if re.search(self.xiaoqu_regex, response):
            borough_name=re.search(self.xiaoqu_regex, response).group(1)
            self.fd['borough_name'] = borough_name
            if re.search(self.address_regex, response):
                house_addr=re.search(self.address_regex, response).group(1)
                self.fd['house_addr'] = house_addr
        else:            
            if d_i.find(text="小区: "):
                borough_box = d_i.find(text="小区: ").parent        
                borough_name = borough_box.find("a")
                if borough_name:
                    self.fd['borough_name'] = borough_name.string
                else:
                    self.fd['borough_name'] = None            
                #地址
                if borough_name and borough_name.nextSibling:
                    house_addr = borough_name.nextSibling.string
                    self.fd['house_addr'] = re.sub("\(|\)| ","",house_addr)
                else:
                    self.fd['house_addr'] = None
            else:
                if re.search(self.borough_name_regex, response):
                    borough_name=re.search(self.borough_name_regex, response).group(1)
                    self.fd['borough_name'] = re.sub("\(.*\)| ","",borough_name)
            
        #区域     
        area_box = d_i.find(text="区域: ").parent
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
        if re.search(self.house_toward_regex, response):
            house_toward=re.search(self.house_toward_regex, response).group(1)
            self.fd['house_toward'] = toward(house_toward)
        else:
            self.fd['house_toward'] = None        
            
        if re.search(self.house_fitment_regex, response):
            house_fitment=re.search(self.house_fitment_regex, response).group(1)
            self.fd['house_fitment'] = fitment(house_fitment)
        else:
            self.fd['house_fitment'] = 2
    def QiuGou(self,url):
        self.fd['city'] = self.citycode       
        self.fd['house_flag'] = 1
#        self.fd['belong']="1"
        request = urllib2.Request(url, None, self.header)
        response = urllib2.urlopen(request).read()
        tree = etree.HTML(response)
        soup =BeautifulSoup(response)
        
        detail_mer = soup.find('div',{'class':'detail_mer'})
        
        #非个人房源 return
        if u"个人房源"  not in str(detail_mer):return        
        
        Dname = detail_mer.find('span',{'class':'Dname'})
        if Dname:
            self.fd['owner_name'] = Dname.string
        else:
            self.fd['owner_name'] = None
            
        ganji_phone_call_class = detail_mer.find('span',{'class':'ganji_phone_call_class'})
        
        if ganji_phone_call_class:
            self.fd['owner_phone'] = ganji_phone_call_class.contents[0]
            if str(ganji_phone_call_class).find('src='):                
                self.fd['owner_phone'] = 'http://'+urlparse(url)[1]+ganji_phone_call_class.img['src']
            else:
                self.fd['owner_phone'] = None            
        else:
            self.fd['owner_phone'] = None
            
            
        #没有联系方式  return
        if not self.fd['owner_phone']:return     
        
        if re.search("<span class=\"city\"><a .*?>(.*?)</a>", response):
            cityname=re.search("<span class=\"city\"><a .*?>(.*?)</a>", response).group(1)
            self.fd['cityname'] = cityname
        else:
            return   
        
        self.fd['house_floor'] = 0
        self.fd['house_topfloor'] = 0 
        self.fd['house_type'] = 0
        self.fd['house_age'] = 0
        self.fd['house_toward'] = 0
        self.fd['house_fitment'] = 0

        
        if re.search(self.house_totalarea_regex_qiu, response):
            house_totalarea=re.search(self.house_totalarea_regex_qiu, response).group(1)
            self.fd['house_totalarea'] = house_totalarea
            self.fd['house_totalarea_max'] = house_totalarea
            self.fd['house_totalarea_min'] = house_totalarea
        else:
            self.fd['house_totalarea'] = 0
            self.fd['house_totalarea_max'] = 0
            self.fd['house_totalarea_min'] = 0
            
        if re.search(self.house_price_regex_gou, response):
            house_price_zu = re.search(self.house_price_regex_gou, response).group(1)
            house_price_zu = house_price_zu.replace('万','')
            if house_price_zu.find("以上") != -1:
                self.fd['house_price_max'] = 0
                self.fd['house_price_min'] = house_price_zu.replace('以上','')
            elif house_price_zu.find("以下") != -1:
                self.fd['house_price_max'] = house_price_zu.replace('以下','')
                self.fd['house_price_min'] = 0
            elif house_price_zu.find("-") != -1:
                self.fd['house_price_max'] = house_price_zu.split('-')[1]
                self.fd['house_price_min'] = house_price_zu.split('-')[0]
            else:
                self.fd['house_price_max'] = 0
                self.fd['house_price_min'] = 0
        else:
            self.fd['house_price_max'] = 0
            self.fd['house_price_min'] = 0
            
        posttime=CSSSelector('span.pub_time')(tree)!=None and CSSSelector('span.pub_time')(tree)[0].text.strip() or None 
        if posttime:
            Y=int(time.strftime('%Y', time.localtime()))
            M=int(posttime.split(' ')[0].split('-')[0])
            D=int(posttime.split(' ')[0].split('-')[1])
            s = datetime.datetime(Y,M,D,0,0)
            posttime=int(time.mktime(s.timetuple()))
            self.fd['posttime'] =posttime 
        else:
            self.fd['posttime'] =None
            
        if re.search(self.house_room_regex, response):
            house_room=re.search(self.house_room_regex, response).group(1)
            self.fd['house_room'] = house_room
        else:
            self.fd['house_room'] = '0'
            
        if re.search(self.house_hall_regex, response):
            house_hall=re.search(self.house_hall_regex, response).group(1)
            self.fd['house_hall'] = house_hall
        else:
            self.fd['house_hall'] = '0'
        
        if re.search(self.house_toilet_regex, response):
            house_toilet=re.search(self.house_toilet_regex, response).group(1)
            self.fd['house_toilet'] = house_toilet
        else:
            self.fd['house_toilet'] = '0'

        house_title=CSSSelector("div.detail_title h1")(tree)[0] !=None and CSSSelector("div.detail_title h1")(tree)[0].text.strip() or None
        self.fd['house_title'] = house_title
        
        #描述        
        detail_box = soup.find('div',{'class':'detail_box'})
        if detail_box:
            house_desc = str(detail_box('p')[1])
            self.fd['house_desc'] = re.sub("<.*?>|\n|\r|\t|联系我时请说明是从赶集网上看到的","",house_desc)
        else:
            self.fd['house_desc'] = None

        d_i = soup.find('ul',{'class':'d_i'})
        
        #小区名
        #先处理JS
        if re.search(self.xiaoqu_regex, response):
            borough_name=re.search(self.xiaoqu_regex, response).group(1)
            self.fd['borough_name'] = borough_name
            if re.search(self.address_regex, response):
                house_addr=re.search(self.address_regex, response).group(1)
                self.fd['house_addr'] = house_addr
        else:            
            if d_i.find(text="小区: "):
                borough_box = d_i.find(text="小区: ").parent        
                borough_name = borough_box.find("a")
                if borough_name:
                    self.fd['borough_name'] = borough_name.string
                else:
                    self.fd['borough_name'] = None                         
            else:
                if re.search(self.borough_name_regex_reg, response):
                    borough_name=re.search(self.borough_name_regex_reg, response).group(1)
                    self.fd['borough_name'] = borough_name
            if re.search(self.house_addr_regex_reg, response):
                house_addr=re.search(self.house_addr_regex_reg, response).group(1)
                self.fd['house_addr'] = house_addr
            else:
                self.fd['house_addr'] = ''
            
        #区域     
        area_box = d_i.find(text="区域: ").parent
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
        
    def ChuZu(self,url):
        self.fd['city'] = urlparse(url)[1].replace('.ganji.com',"")
        
        request = urllib2.Request(url, None, self.header)
        response = urllib2.urlopen(request).read()
        tree = etree.HTML(response)
        if re.search("<span class=\"city\"><a .*?>(.*?)</a>", response):
            cityname=re.search("<span class=\"city\"><a .*?>(.*?)</a>", response).group(1)
            self.fd['cityname'] = cityname
        else:
            return
        
        self.fd['house_flag'] = 2
        self.fd['house_type'] = 0
        self.fd['house_floor'] = ""
        self.fd['house_topfloor'] = "" 
        
        soup =BeautifulSoup(response)
        detail_mer = soup.find('div',{'class':'detail_mer'})
        
        #非个人房源 return
        if u"个人房源"  not in str(detail_mer):return
        
        Dname = detail_mer.find('span',{'class':'Dname'})
        if Dname:
            self.fd['owner_name'] = Dname.string
        else:
            self.fd['owner_name'] = None
            
        ganji_phone_call_class = detail_mer.find('span',{'class':'ganji_phone_call_class'})
        
        if ganji_phone_call_class:
            self.fd['owner_phone'] = ganji_phone_call_class.contents[0]
            if str(ganji_phone_call_class).find('src='):                
                self.fd['owner_phone'] = 'http://'+urlparse(url)[1]+ganji_phone_call_class.img['src']
            else:
                self.fd['owner_phone'] = None            
        else:
            self.fd['owner_phone'] = None
            
            
        #没有联系方式  return
        if not self.fd['owner_phone']:return        
        
        if re.search(self.house_totalarea_regex, response):
            house_totalarea=re.search(self.house_totalarea_regex, response).group(1)
            self.fd['house_totalarea'] = house_totalarea
        else:
            self.fd['house_totalarea'] = None
        
        if re.search(self.house_price_regex_2, response):
            house_price=re.search(self.house_price_regex_2, response).group(1)
            self.fd['house_price'] = house_price
        else:
            self.fd['house_price'] = None
    #    house_price=tree.xpath("/html/body/div[2]/div/div/ul/li/span") and tree.xpath("/html/body/div[2]/div/div/ul/li/span")[0].text.strip() or None    
    #    v['house_price'] = house_price
        
        posttime=CSSSelector('span.pub_time')(tree)!=None and CSSSelector('span.pub_time')(tree)[0].text.strip() or None 
        if posttime:
            Y=int(time.strftime('%Y', time.localtime()))
            M=int(posttime.split(' ')[0].split('-')[0])
            D=int(posttime.split(' ')[0].split('-')[1])
            s = datetime.datetime(Y,M,D,0,0)
            posttime=int(time.mktime(s.timetuple()))
            self.fd['posttime'] =posttime 
        else:
            self.fd['posttime'] =None
            
        house_title=CSSSelector("div.detail_title h1")(tree)[0] !=None and CSSSelector("div.detail_title h1")(tree)[0].text.strip() or None
        self.fd['house_title'] = house_title
        

        if re.search(self.house_room_regex, response):
            house_room=re.search(self.house_room_regex, response).group(1)
            self.fd['house_room'] = house_room
        else:
            self.fd['house_room'] = '0'
            
        if re.search(self.house_hall_regex, response):
            house_hall=re.search(self.house_hall_regex, response).group(1)
            self.fd['house_hall'] = house_hall
        else:
            self.fd['house_hall'] = '0'
        
        if re.search(self.house_toilet_regex, response):
            house_toilet=re.search(self.house_toilet_regex, response).group(1)
            self.fd['house_toilet'] = house_toilet
        else:
            self.fd['house_toilet'] = '0'

        house_title=CSSSelector("div.detail_title h1")(tree)[0] !=None and CSSSelector("div.detail_title h1")(tree)[0].text.strip() or None
        self.fd['house_title'] = house_title
        
        #描述        
        detail_box = soup.find('div',{'class':'detail_box'})
        if detail_box:
            house_desc = str(detail_box('p')[1])
            self.fd['house_desc'] = re.sub("<.*?>|\n|\r|\t|联系我时请说明是从赶集网上看到的","",house_desc)
        else:
            self.fd['house_desc'] = None

        d_i = soup.find('ul',{'class':'d_i'})        
        #小区名
        #先处理JS
        if re.search(self.xiaoqu_regex, response):
            borough_name=re.search(self.xiaoqu_regex, response).group(1)
            self.fd['borough_name'] = borough_name
            if re.search(self.address_regex, response):
                house_addr=re.search(self.address_regex, response).group(1)
                self.fd['house_addr'] = house_addr
        else:            
            if d_i.find(text="小区: "):
                borough_box = d_i.find(text="小区: ").parent        
                borough_name = borough_box.find("a")
                if borough_name:
                    self.fd['borough_name'] = borough_name.string
                else:
                    self.fd['borough_name'] = None            
                #地址
                if borough_name and borough_name.nextSibling:
                    house_addr = borough_name.nextSibling.string
                    self.fd['house_addr'] = re.sub("\(|\)| ","",house_addr)
                else:
                    self.fd['house_addr'] = None
            else:
                if re.search(self.borough_name_regex, response):
                    borough_name=re.search(self.borough_name_regex, response).group(1)
                    self.fd['borough_name'] = re.sub("\(.*\)| ","",borough_name)
            
        #区域     
        area_box = d_i.find(text="区域: ").parent
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
        if re.search(self.house_toward_regex, response):
            house_toward=re.search(self.house_toward_regex, response).group(1)
            self.fd['house_toward'] = toward(house_toward)
        else:
            self.fd['house_toward'] = None        
            
        if re.search(self.house_fitment_regex, response):
            house_fitment=re.search(self.house_fitment_regex, response).group(1)
            self.fd['house_fitment'] = fitment(house_fitment)
        else:
            self.fd['house_fitment'] = 2
            
        if re.search(self.house_deposit_regex, response):
            house_deposit=re.search(self.house_deposit_regex, response).group(1)
            self.fd['house_deposit'] = deposit(house_deposit)
        else:
            self.fd['house_deposit'] = None  
    def QiuZu(self,url):
        
        self.fd['city'] = urlparse(url)[1].replace('.ganji.com',"")        
        request = urllib2.Request(url, None, self.header)
        response = urllib2.urlopen(request).read()
        tree = etree.HTML(response)
        if re.search("<span class=\"city\"><a .*?>(.*?)</a>", response):
            cityname=re.search("<span class=\"city\"><a .*?>(.*?)</a>", response).group(1)
            self.fd['cityname'] = cityname
        else:
            return
        
        self.fd['house_flag'] = 3
        self.fd['house_type'] = 0
        self.fd['house_floor'] = ""
        self.fd['house_topfloor'] = "" 
        self.fd['house_totalarea']=0
        self.fd['house_age'] = 0
        self.fd['house_toward'] = 0
        self.fd['house_fitment'] = 0
        self.fd['house_deposit'] = 0
        self.fd['house_totalarea_max'] = 0
        self.fd['house_totalarea_min'] = 0
        self.fd['house_totalarea'] = 0
        
        soup =BeautifulSoup(response)
        detail_mer = soup.find('div',{'class':'detail_mer'})
        
        #非个人房源 return
        if u"个人房源"  not in str(detail_mer):return
        
        Dname = detail_mer.find('span',{'class':'Dname'})
        if Dname:
            self.fd['owner_name'] = Dname.string
        else:
            self.fd['owner_name'] = None
            
        ganji_phone_call_class = detail_mer.find('span',{'class':'ganji_phone_call_class'})
        
        if ganji_phone_call_class:
            self.fd['owner_phone'] = ganji_phone_call_class.contents[0]
            if str(ganji_phone_call_class).find('src='):                
                self.fd['owner_phone'] = 'http://'+urlparse(url)[1]+ganji_phone_call_class.img['src']
            else:
                self.fd['owner_phone'] = None            
        else:
            self.fd['owner_phone'] = None
            
            
        #没有联系方式  return
        if not self.fd['owner_phone']:return     
        
        if re.search(self.house_price_regex_zu, response):
            house_price_zu = re.search(self.house_price_regex_zu, response).group(1)
            house_price_zu = house_price_zu.replace('元/月','')
            if house_price_zu.find("以上") != -1:
                self.fd['house_price_max'] = 0
                self.fd['house_price_min'] = house_price_zu.replace('以上','')
            elif house_price_zu.find("以下") != -1:
                self.fd['house_price_max'] = house_price_zu.replace('以下','')
                self.fd['house_price_min'] = 0
            elif house_price_zu.find("-") != -1:
                self.fd['house_price_max'] = house_price_zu.split('-')[1]
                self.fd['house_price_min'] = house_price_zu.split('-')[0]
            else:
                self.fd['house_price_max'] = 0
                self.fd['house_price_min'] = 0
        else:
            self.fd['house_price_max'] = 0
            self.fd['house_price_min'] = 0
        
        posttime=CSSSelector('span.pub_time')(tree)!=None and CSSSelector('span.pub_time')(tree)[0].text.strip() or None 
        if posttime:
            Y=int(time.strftime('%Y', time.localtime()))
            M=int(posttime.split(' ')[0].split('-')[0])
            D=int(posttime.split(' ')[0].split('-')[1])
            s = datetime.datetime(Y,M,D,0,0)
            posttime=int(time.mktime(s.timetuple()))
            self.fd['posttime'] =posttime 
        else:
            self.fd['posttime'] =None
            
        house_title=CSSSelector("div.detail_title h1")(tree)[0] !=None and CSSSelector("div.detail_title h1")(tree)[0].text.strip() or None
        self.fd['house_title'] = house_title
        

        if re.search(self.house_room_regex, response):
            house_room=re.search(self.house_room_regex, response).group(1)
            self.fd['house_room'] = house_room
        else:
            self.fd['house_room'] = '0'
            
        if re.search(self.house_hall_regex, response):
            house_hall=re.search(self.house_hall_regex, response).group(1)
            self.fd['house_hall'] = house_hall
        else:
            self.fd['house_hall'] = '0'
        
        if re.search(self.house_toilet_regex, response):
            house_toilet=re.search(self.house_toilet_regex, response).group(1)
            self.fd['house_toilet'] = house_toilet
        else:
            self.fd['house_toilet'] = '0'

        house_title=CSSSelector("div.detail_title h1")(tree)[0] !=None and CSSSelector("div.detail_title h1")(tree)[0].text.strip() or None
        self.fd['house_title'] = house_title
        
        #描述        
        detail_box = soup.find('div',{'class':'detail_box'})
        if detail_box:
            house_desc = str(detail_box('p')[1])
            self.fd['house_desc'] = re.sub("<.*?>|\n|\r|\t|联系我时请说明是从赶集网上看到的","",house_desc)
        else:
            self.fd['house_desc'] = None

        d_i = soup.find('ul',{'class':'d_i'})        
        #小区名
        #先处理JS
        if re.search(self.xiaoqu_regex, response):
            borough_name=re.search(self.xiaoqu_regex, response).group(1)
            self.fd['borough_name'] = borough_name
            if re.search(self.address_regex, response):
                house_addr=re.search(self.address_regex, response).group(1)
                self.fd['house_addr'] = house_addr
        else:            
            if re.search(self.borough_name_regex_reg, response):
                borough_name=re.search(self.borough_name_regex_reg, response).group(1)
                self.fd['borough_name'] = borough_name
            if re.search(self.house_addr_regex_reg, response):
                house_addr=re.search(self.house_addr_regex_reg, response).group(1)
                self.fd['house_addr'] = house_addr
            else:
                self.fd['house_addr'] = ''
                
            
        #区域     
        area_box = d_i.find(text="区域: ").parent
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
   
    def extractDict(self):        
        for url in self.urls:
            if False:#checkPath(homepath,self.folder,url):
                pass
            else:
                if self.kind=="1":
                    self.ChuShou(url)
                elif self.kind=="2":
                    self.ChuZu(url)
                elif self.kind=="3":
                    self.QiuGou(url)
                else:
                    self.QiuZu(url)
                #makePath(homepath,self.folder,url)                
                #超过七天
                try:
                    if (time.time() -self.fd["posttime"]) > 7*24*36000:return
                except:pass
                self.fd["c"]="houseapi"
                self.fd["a"]="savehouse"        
                self.fd["is_checked"] = 0        
                self.fd["web_flag"]   = "gj"
                
                if not self.fd["is_checked"]:
                    for i in self.fd.items():
                        print i[0],i[1]
                print  "*"*80
                if len(self.fd)==7 or len(self.fd)==17:
                    print "#####################################"
                    continue
                #req=urllib2.Request("http://site.jjr360.com/app.php", urllib.urlencode(self.fd))
                #p=self.br.open(req).read().strip()
                #print p.decode('gbk')
                print  "*"*80
        
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
#    lc=LinkCrawl(citycode="gz",kind="4")
#    lc.runme()
#    
    
    
#    url1 = "http://su.ganji.com/fang1/11070921_417506.htm"
#    url2 = "http://su.ganji.com/fang5/11070916_233246.htm"
#    url3 = "http://su.ganji.com/fang4/11070218_4172.htm"
#    url4 = "http://su.ganji.com/fang2/11070900_21214.htm"
#    
    urls=[
          "http://gz.ganji.com/fang4/11071001_66181.htm",
          "http://gz.ganji.com/fang4/11070900_66176.htm",
          "http://gz.ganji.com/fang4/11070818_66174.htm",
          "http://gz.ganji.com/fang4/11070714_66171.htm",
          "http://gz.ganji.com/fang4/11070622_66168.htm",
          "http://gz.ganji.com/fang4/11070611_66161.htm",
          "http://gz.ganji.com/fang4/11070608_66160.htm",
          "http://gz.ganji.com/fang4/11070600_66159.htm",
          "http://gz.ganji.com/fang4/11070514_66157.htm",
          "http://gz.ganji.com/fang4/11070423_66156.htm",
          "http://gz.ganji.com/fang4/11070115_66141.htm",
          "http://gz.ganji.com/fang4/11070111_66140.htm",
          "http://gz.ganji.com/fang4/11062922_66139.htm",
          "http://gz.ganji.com/fang4/11062918_66137.htm",
          "http://gz.ganji.com/fang4/11062916_66134.htm",
          "http://gz.ganji.com/fang2/11070921_104635.htm",          
          ]
    cc=ContentCrawl(urls,citycode="gz",kind="1")
    cc.extractDict()