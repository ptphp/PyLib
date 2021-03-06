#coding=UTF-8
'''
Created on 2011-7-6

@author: Administrator
'''
from urlparse import urlparse
import cookielib

from pyquery.pyquery import PyQuery #@UnresolvedImport
import re

import datetime #@UnusedImport
import urllib2
from lxml import etree #@UnresolvedImport



from lxml.cssselect import CSSSelector #@UnresolvedImport

import simplejson as js #@UnusedImport @UnresolvedImport

from config import housetype, checkPath, makePath,fitment,toward,deposit, isDEV,\
    citynameDict_sf, getDefaultVal
import threading
from BeautifulSoup import BeautifulSoup #@UnresolvedImport
import time
import gc
from jjrlog import msglogger, LinkLog
from common import postHost
homepath="F:\\home\\spider\\"
gc.enable()
class LinkCrawl(object):
    def __init__(self,citycode="",kind="",upc="5",st="3"):
        cj = cookielib.MozillaCookieJar()
        self.br=urllib2.build_opener(urllib2.HTTPHandler(),urllib2.HTTPCookieProcessor(cj),urllib2.HTTPRedirectHandler())
        self.header={
            "User-Agent":'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB6.6; .NET CLR 3.5.30729)',
        }
        self.upc=upc
        self.endtime=str(datetime.date.today() -datetime.timedelta(days=1))  
        self.clinks=[]
        self.pn=[]
        self.citycode=citycode
        self.baseUrl="http://%s.ganji.com"%self.citycode
        self.kind=kind
        if kind=="1":#出售
            self.urlpath="/fang5/a1u2%s/"
            self.folder="sell\\"
        elif kind=="2":#出租
            self.urlpath="/fang1/u2%s/"
            self.folder="rent\\"
        elif kind=="3":#求购
            self.urlpath="/fang4/u2f0/a1%s/"
            self.folder="buy\\"
        elif kind=="4":#求租
            self.urlpath="/fang2/u2f0/a1%s/"
            self.folder="req\\"
            
            
    def __getAllNeedLinks(self):
        cond=True
        idx=0
        checkit="0"
        while  cond:
            url=self.baseUrl+self.urlpath%("f"+str(idx*32))
            #url="http://gz.ganji.com/fang2/u2f0/a1f768/"
#            print url
            try:
                req=urllib2.Request(url, None, self.header)
                p=self.br.open(req).read()
            except:
                continue
            else:
                check=PyQuery(p)("ul.pageLink li a.c").text()
                if check==None or check==checkit:
                    cond=False
                    break
                else:
                    checkit=check
                    links=PyQuery(p)("div.list dl")
                    p=None
#                    print len(links)
                    for link in links:
                        lk=self.baseUrl+PyQuery(link)(" a.list_title").attr("href")
#                        print lk
                        if self.kind=="3" or self.kind=="4":
                            tm=PyQuery(link)("dd span.time").text()
                            if re.match('''\d{2}-\d{2}''', tm):
                                Y=int(time.strftime('%Y', time.localtime()))
                                tm="%s-%s"%(Y,tm.strip())
                                if tm<self.endtime:
                                    cond=False
                                    break
                            elif "分钟" in tm:
                                pass
                            elif "小时" in tm:
                                pass
                            else:
                                cond=False
                                break
                        if not checkPath(homepath,self.folder,lk):
                            LinkLog.info("%s|%s"%(self.kind,lk))
                            try:
                                getContent(lk,self.citycode,self.kind,self.upc)
                            except Exception,e:print "ganji getContent Exception %s"%e
#                            fetch_quere.put({"mod":"ganji","link":lk,"citycode":self.citycode,"kind":self.kind})        
#                        if lk not in self.clinks:
#                            self.clinks.append(lk)
                idx=idx+1
#        print len(self.clinks)
    def runme(self):
        #self.__initPageNum()
        self.__getAllNeedLinks()
    
class ContentCrawl(object):
    def __init__(self,links,citycode,kind,upc):
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
        self.upc=upc
        
        if kind=="1":
            self.folder="sell\\"
        elif kind=="2":
            self.folder="rent\\"
        elif kind=="3":
            self.folder="buy\\"
        else:
            self.folder="req\\"
        #js resgx
        
        self.xiaoqu_regex="xiaoqu : '(.*?)',"
        self.address_regex="address : '(.*?)',"
        self.house_room_regex="(\d+)室"
        self.house_hall_regex="(\d+)厅"
        self.house_toilet_regex="(\d+)卫"
        self.house_veranda_regex="(\d+)阳台"
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
    def mayGetIt(self,page):
        try:
            href=PyQuery(page)("a.userHistory").attr("href")
            if href==None:
                return False
            href="http://%s.ganji.com%s"%(self.citycode,href)
            resp = urllib2.urlopen(urllib2.Request(href, None, self.header)).read()
            trs=PyQuery(resp)("table.tel_list tr")
        except:
            return True
#        print "user list-------->%s| %s"%((len(trs)-1),self.urls)
        if len(trs)-1>int(self.upc):
            return True
        else:
            return False
    def sell(self,url):
        request = urllib2.Request(url, None, self.header)
        response = urllib2.urlopen(request).read()
        if self.mayGetIt(response):
            self.fd={}
            raise 
        tree = etree.HTML(response)
        soup =BeautifulSoup(response)
        
        self.fd['house_flag'] = 1
        self.fd['house_belong']=0
        self.fd['owner_phone']=''
        self.fd['house_area_max']=0
        self.fd['house_price_max']=''
        
        detail_mer = soup.find('div',{'class':'detail_mer'})        
        #非个人房源 return
        if u"个人房源"  not in str(detail_mer):raise        
        
        Dname = detail_mer.find('span',{'class':'Dname'})
        if Dname:
            self.fd['owner_name'] = str(Dname.string)
        else:
            self.fd['owner_name'] = None
            
        ganji_phone_call_class = detail_mer.find('span',{'class':'ganji_phone_call_class'})
        
        if ganji_phone_call_class:
            self.fd['owner_phone_pic'] = ganji_phone_call_class.contents[0]
            if str(ganji_phone_call_class).find('src='):                
                self.fd['owner_phone_pic'] = 'http://'+urlparse(url)[1]+ganji_phone_call_class.img['src']
            else:
                self.fd['owner_phone_pic'] = None            
        else:
            self.fd['owner_phone_pic'] = None            
            
        #没有联系方式  return
        if not self.fd['owner_phone_pic']:raise     
        
        if re.search("<span class=\"city\"><a .*?>(.*?)</a>", response):
            cityname=re.search("<span class=\"city\"><a .*?>(.*?)</a>", response).group(1)
            self.fd['cityname'] = cityname
        else:
            raise   
        
        if re.search(self.house_floor_regex, response):
            house_floor=re.search(self.house_floor_regex, response).group(1)
            house_topfloor=re.search(self.house_floor_regex, response).group(2)
            self.fd['house_floor']    = int(house_floor)
            self.fd['house_topfloor'] = int(house_topfloor)
        else:
            self.fd['house_floor'] = 0
            self.fd['house_topfloor'] = 0   
        
        if re.search(self.house_totalarea_regex, response):
            house_totalarea=re.search(self.house_totalarea_regex, response).group(1)
            self.fd['house_area'] = int(house_totalarea)
        else:
            self.fd['house_area'] = 0
            
        #类型 
        if re.search(self.house_type_regex, response):
            house_type=re.search(self.house_type_regex, response).group(1)
            self.fd['house_type'] = housetype(house_type)
        else:
            self.fd['house_type'] = 6   
            
        if re.search(self.house_price_regex, response):
            house_price=re.search(self.house_price_regex, response).group(1)
            if house_price=="面议":
                house_price=0
            self.fd['house_price'] = int(house_price)
        else:
            self.fd['house_price'] = 0
    
        #posttime=CSSSelector('span.pub_time')(tree)!=None and CSSSelector('span.pub_time')(tree)[0].text.strip() or None 
        #if posttime:
            #Y=int(time.strftime('%Y', time.localtime()))
            #M=int(posttime.split(' ')[0].split('-')[0])
            #D=int(posttime.split(' ')[0].split('-')[1])
            #s = datetime.datetime(Y,M,D,0,0)
            #posttime=int(time.mktime(s.timetuple()))
            #self.fd['house_posttime'] =posttime 
        #else:
            #self.fd['house_posttime'] =None
            
        if re.search(self.house_room_regex, response):
            house_room=re.search(self.house_room_regex, response).group(1)
            self.fd['house_room'] = int(house_room)
        else:
            self.fd['house_room'] = 0
            
        if re.search(self.house_hall_regex, response):
            house_hall=re.search(self.house_hall_regex, response).group(1)
            self.fd['house_hall'] = int(house_hall)
        else:
            self.fd['house_hall'] = 0
        
        if re.search(self.house_toilet_regex, response):
            house_toilet=re.search(self.house_toilet_regex, response).group(1)
            self.fd['house_toilet'] = int(house_toilet)
        else:
            self.fd['house_toilet'] = 0
            
        if re.search(self.house_veranda_regex, response):
            house_veranda=re.search(self.house_veranda_regex, response).group(1)
            self.fd['house_veranda'] = int(house_veranda)
        else:
            self.fd['house_veranda'] = 0    
        

        house_title=CSSSelector("div.detail_title h1")(tree)[0] !=None and CSSSelector("div.detail_title h1")(tree)[0].text.strip() or None
        self.fd['house_title'] = house_title.replace("(求购)","").replace("(求租)","").replace("(出售)","")
        
        #描述        
        detail_box = soup.find('div',{'class':'detail_box'})
        if detail_box:
            house_desc = str(detail_box('p')[1])
            self.fd['house_desc'] = re.sub("<.*?>|\n|\r|\t|联系我时请说明是从赶集网上看到的","",house_desc)
        else:
            self.fd['house_desc'] = ""

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
                    self.fd['borough_name'] = str(borough_name.string)
                else:
                    self.fd['borough_name'] = None            
                #地址
                if borough_name and borough_name.nextSibling:
                    house_addr = borough_name.nextSibling.string
                    self.fd['house_addr'] = re.sub("\(|\)| ","",house_addr)
                else:
                    self.fd['house_addr'] = ""
            else:
                if re.search(self.borough_name_regex, response):
                    borough_name=re.search(self.borough_name_regex, response).group(1)
                    self.fd['borough_name'] = re.sub("\(.*\)| ","",borough_name)
            
        #区域     
        area_box = d_i.find(text="区域: ").parent
        area_a = area_box('a')
        if area_a and len(area_a)>1:
            self.fd['house_region'] = str(area_a[0].string)
            self.fd['house_section'] = str(area_a[1].string)
        elif area_a and len(area_a)==1:
            self.fd['house_region'] = str(area_a[0].string)
            self.fd['house_section'] = ""
        else:
            self.fd['house_region'] = ""
            self.fd['house_section'] = ""
        
        if re.search(self.house_age_regex, response):
            house_age=re.search(self.house_age_regex, response).group(1)
            Y=int(time.strftime('%Y', time.localtime()))
            house_age=Y-int(house_age)
            self.fd['house_age'] = house_age
        else:
            self.fd['house_age'] = 0
            
        #朝向
        if re.search(self.house_toward_regex, response):
            house_toward=re.search(self.house_toward_regex, response).group(1)
            self.fd['house_toward'] = toward(house_toward)
        else:
            self.fd['house_toward'] = 0        
            
        if re.search(self.house_fitment_regex, response):
            house_fitment=re.search(self.house_fitment_regex, response).group(1)
            self.fd['house_fitment'] = fitment(house_fitment)
        else:
            self.fd['house_fitment'] = 2
        request = None
        response = None
        soup=None
        tree=None
        del tree
        del request
        del response
        del soup 
    def buy(self,url):
        self.fd['house_city'] = self.citycode       
        self.fd['house_flag'] = 3
#        self.fd['belong']="1"
        request = urllib2.Request(url, None, self.header)
        response = urllib2.urlopen(request).read()
        if self.mayGetIt(response):
            self.fd={}
            raise
        tree = etree.HTML(response)
        soup =BeautifulSoup(response)
        
        detail_mer = soup.find('div',{'class':'detail_mer'})
        
        #非个人房源 return
        if u"个人房源"  not in str(detail_mer):raise        
        
        Dname = detail_mer.find('span',{'class':'Dname'})
        if Dname:
            self.fd['owner_name'] = str(Dname.string)
        else:
            self.fd['owner_name'] = ""
            
        ganji_phone_call_class = detail_mer.find('span',{'class':'ganji_phone_call_class'})
        
        if ganji_phone_call_class:
            self.fd['owner_phone_pic'] = ganji_phone_call_class.contents[0]
            if str(ganji_phone_call_class).find('src='):                
                self.fd['owner_phone_pic'] = 'http://'+urlparse(url)[1]+ganji_phone_call_class.img['src']
            else:
                self.fd['owner_phone_pic'] = ""            
        else:
            self.fd['owner_phone_pic'] = ""
            
            
        #没有联系方式  return
        if not self.fd['owner_phone_pic']:raise     
        
        if re.search("<span class=\"city\"><a .*?>(.*?)</a>", response):
            cityname=re.search("<span class=\"city\"><a .*?>(.*?)</a>", response).group(1)
            self.fd['cityname'] = cityname
        else:
            raise
        
        self.fd['house_floor'] = 0
        self.fd['house_topfloor'] = 0 
        self.fd['house_type'] = 6
        self.fd['house_age'] = 0
        self.fd['house_toward'] = 0
        self.fd['house_fitment'] = 0

        
        if re.search(self.house_totalarea_regex_qiu, response):
            house_totalarea=re.search(self.house_totalarea_regex_qiu, response).group(1)
            self.fd['house_area_max'] = int(house_totalarea)
            self.fd['house_area'] = int(house_totalarea)
        else:
            self.fd['house_area'] = 0
            self.fd['house_area_max'] = 0
            
        if re.search(self.house_price_regex_gou, response):
            house_price_zu = re.search(self.house_price_regex_gou, response).group(1)
            house_price_zu = house_price_zu.replace('万','')
            if house_price_zu.find("以上") != -1:
                self.fd['house_price_max'] = 0
                self.fd['house_price'] = int(house_price_zu.replace('以上',''))
            elif house_price_zu.find("以下") != -1:
                self.fd['house_price_max'] = int(house_price_zu.replace('以下',''))
                self.fd['house_price'] = 0
            elif house_price_zu.find("-") != -1:
                self.fd['house_price_max'] = int(house_price_zu.split('-')[1])
                self.fd['house_price'] = int(house_price_zu.split('-')[0])
            else:
                self.fd['house_price_max'] = 0
                self.fd['house_price'] = 0
        else:
            self.fd['house_price_max'] = 0
            self.fd['house_price'] = 0
            
        posttime=CSSSelector('span.pub_time')(tree)!=None and CSSSelector('span.pub_time')(tree)[0].text.strip() or None 
        if posttime:
            Y=int(time.strftime('%Y', time.localtime()))
            M=int(posttime.split(' ')[0].split('-')[0])
            D=int(posttime.split(' ')[0].split('-')[1])
            H=int(time.strftime('%H',time.localtime(time.time())))
            Min=int(time.strftime('%M',time.localtime(time.time())))
            s = datetime.datetime(Y,M,D,H,Min)
            posttime=str(int(time.mktime(s.timetuple())))
            self.fd['house_posttime'] =posttime 
        else:
            s=time.localtime(time.time())
            self.fd['house_posttime'] =str(int(time.mktime(s)))
            
        if re.search(self.house_room_regex, response):
            house_room=re.search(self.house_room_regex, response).group(1)
            self.fd['house_room'] = int(house_room)
        else:
            self.fd['house_room'] = 0
            
        if re.search(self.house_hall_regex, response):
            house_hall=re.search(self.house_hall_regex, response).group(1)
            self.fd['house_hall'] = int(house_hall)
        else:
            self.fd['house_hall'] = 0
        
        if re.search(self.house_toilet_regex, response):
            house_toilet=re.search(self.house_toilet_regex, response).group(1)
            self.fd['house_toilet'] = int(house_toilet)
        else:
            self.fd['house_toilet'] = 0
    
        if re.search(self.house_veranda_regex, response):
            house_veranda=re.search(self.house_veranda_regex, response).group(1)
            self.fd['house_veranda'] = int(house_veranda)
        else:
            self.fd['house_veranda'] = 0 

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
            self.fd['house_region'] = str(area_a[0].string)
            self.fd['house_section'] = str(area_a[1].string)
        elif area_a and len(area_a)==1:
            self.fd['house_region'] = str(area_a[0].string)
            self.fd['house_section'] = ""
        else:
            self.fd['house_region'] = ""
            self.fd['house_section'] = ""
        request = None
        response = None
        soup=None
        tree=None
        del tree
        del request
        del response
        del soup
    def rent(self,url):
#        self.fd['house_city'] = urlparse(url)[1].replace('.ganji.com',"")
        hc= urlparse(url)[1].replace('.ganji.com',"") 
        hc2=citynameDict_sf.get(hc)
        if hc2:
            self.fd['house_city']=hc2
        else:
            self.fd['house_city']=hc
        request = urllib2.Request(url, None, self.header)
        response = urllib2.urlopen(request).read()
        if self.mayGetIt(response):
            self.fd={}
            raise
        tree = etree.HTML(response)
        if re.search("<span class=\"city\"><a .*?>(.*?)</a>", response):
            cityname=re.search("<span class=\"city\"><a .*?>(.*?)</a>", response).group(1)
            self.fd['cityname'] = cityname
        else:
            raise
        
        self.fd['house_flag'] = 2
        self.fd['house_type'] = 6
        self.fd['house_floor'] = 0
        self.fd['house_topfloor'] = 0 
        
        soup =BeautifulSoup(response)
        detail_mer = soup.find('div',{'class':'detail_mer'})
        
        #非个人房源 return
        if u"个人房源"  not in str(detail_mer):raise
        
        Dname = detail_mer.find('span',{'class':'Dname'})
        if Dname:
            self.fd['owner_name'] = str(Dname.string)
        else:
            self.fd['owner_name'] = ""
            
        ganji_phone_call_class = detail_mer.find('span',{'class':'ganji_phone_call_class'})
        
        if ganji_phone_call_class:
            self.fd['owner_phone_pic'] = ganji_phone_call_class.contents[0]
            if str(ganji_phone_call_class).find('src='):                
                self.fd['owner_phone_pic'] = 'http://'+urlparse(url)[1]+ganji_phone_call_class.img['src']
            else:
                self.fd['owner_phone_pic'] = None            
        else:
            self.fd['owner_phone_pic'] = None
            
            
        #没有联系方式  return
        if not self.fd['owner_phone_pic']:raise        
        
        if re.search(self.house_totalarea_regex, response):
            house_totalarea=re.search(self.house_totalarea_regex, response).group(1)
            self.fd['house_area'] = house_totalarea
        else:
            self.fd['house_area'] = None
        
        if re.search(self.house_price_regex_2, response):
            house_price=re.search(self.house_price_regex_2, response).group(1)
            if house_price=="面议":
                house_price=0
            self.fd['house_price'] = int(house_price)
        else:
            self.fd['house_price'] = 0
    #    house_price=tree.xpath("/html/body/div[2]/div/div/ul/li/span") and tree.xpath("/html/body/div[2]/div/div/ul/li/span")[0].text.strip() or None    
    #    v['house_price'] = house_price
        
        posttime=CSSSelector('span.pub_time')(tree)!=None and CSSSelector('span.pub_time')(tree)[0].text.strip() or None 
        if posttime:
            Y=int(time.strftime('%Y', time.localtime()))
            M=int(posttime.split(' ')[0].split('-')[0])
            D=int(posttime.split(' ')[0].split('-')[1])
            H=int(time.strftime('%H',time.localtime(time.time())))
            Min=int(time.strftime('%M',time.localtime(time.time())))
            s = datetime.datetime(Y,M,D,H,Min)
            posttime=str(int(time.mktime(s.timetuple())))
            self.fd['house_posttime'] =posttime 
        else:
            s=time.localtime(time.time())
            self.fd['house_posttime'] =str(int(time.mktime(s)))
            
        house_title=CSSSelector("div.detail_title h1")(tree)[0] !=None and CSSSelector("div.detail_title h1")(tree)[0].text.strip() or None
        self.fd['house_title'] = house_title.replace("(求购)","").replace("(求租)","").replace("(出售)","")
        

        if re.search(self.house_room_regex, response):
            house_room=re.search(self.house_room_regex, response).group(1)
            self.fd['house_room'] = house_room
        else:
            self.fd['house_room'] = 0
            
        if re.search(self.house_hall_regex, response):
            house_hall=re.search(self.house_hall_regex, response).group(1)
            self.fd['house_hall'] = house_hall
        else:
            self.fd['house_hall'] = 0
        
        if re.search(self.house_toilet_regex, response):
            house_toilet=re.search(self.house_toilet_regex, response).group(1)
            self.fd['house_toilet'] = house_toilet
        else:
            self.fd['house_toilet'] = 0
            
        if re.search(self.house_veranda_regex, response):
            house_veranda=re.search(self.house_veranda_regex, response).group(1)
            self.fd['house_veranda'] = house_veranda
        else:
            self.fd['house_veranda'] = 0
            
            
        if re.search(self.house_floor_regex, response):
            house_floor=re.search(self.house_floor_regex, response).group(1)
            house_topfloor=re.search(self.house_floor_regex, response).group(2)
            self.fd['house_floor']    = int(house_floor)
            self.fd['house_topfloor'] = int(house_topfloor)
        else:
            self.fd['house_floor'] = 0
            self.fd['house_topfloor'] = 0
          
            
        house_title=CSSSelector("div.detail_title h1")(tree)[0] !=None and CSSSelector("div.detail_title h1")(tree)[0].text.strip() or None
        self.fd['house_title'] = house_title.replace("(求购)","").replace("(求租)","").replace("(出售)","")
        
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
            self.fd['house_region'] = str(area_a[0].string)
            self.fd['house_section'] = str(area_a[1].string)
        elif area_a and len(area_a)==1:
            self.fd['house_region'] = str(area_a[0].string)
            self.fd['house_section'] = ""
        else:
            self.fd['house_region'] = ""
            self.fd['house_section'] = ""
        
        if re.search(self.house_age_regex, response):
            house_age=re.search(self.house_age_regex, response).group(1)
            Y=int(time.strftime('%Y', time.localtime()))
            house_age=Y-int(house_age)
            self.fd['house_age'] = house_age
        else:
            self.fd['house_age'] = 0
            
        #朝向
        if re.search(self.house_toward_regex, response):
            house_toward=re.search(self.house_toward_regex, response).group(1)
            self.fd['house_toward'] = toward(house_toward)
        else:
            self.fd['house_toward'] = 0        
            
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
        request = None
        response = None
        soup=None
        tree=None
        del tree
        del request
        del response
        del soup  
    def require(self,url):
        hc= urlparse(url)[1].replace('.ganji.com',"") 
        hc2=citynameDict_sf.get(hc)
        if hc2:
            self.fd['house_city']=hc2
        else:
            self.fd['house_city']=hc
        request = urllib2.Request(url, None, self.header)
        response = urllib2.urlopen(request).read()
        if self.mayGetIt(response):
            self.fd={}
            raise
        tree = etree.HTML(response)
        if re.search("<span class=\"city\"><a .*?>(.*?)</a>", response):
            cityname=re.search("<span class=\"city\"><a .*?>(.*?)</a>", response).group(1)
            self.fd['cityname'] = cityname
        else:
            raise
        
        self.fd['house_flag'] = 4
        self.fd['house_type'] = 6
        self.fd['house_floor'] = 0
        self.fd['house_topfloor'] = 0 
        self.fd['house_area']=0
        self.fd['house_age'] = 0
        self.fd['house_toward'] = 0
        self.fd['house_fitment'] = 0
        self.fd['house_deposit'] = 0
#        self.fd['house_totalarea_max'] = 0
#        self.fd['house_totalarea_min'] = 0
        
        soup =BeautifulSoup(response)
        detail_mer = soup.find('div',{'class':'detail_mer'})
        
        #非个人房源 return
        if u"个人房源"  not in str(detail_mer):raise
        
        Dname = detail_mer.find('span',{'class':'Dname'})
        if Dname:
            self.fd['owner_name'] = Dname.string
        else:
            self.fd['owner_name'] = None
            
        ganji_phone_call_class = detail_mer.find('span',{'class':'ganji_phone_call_class'})
        
        if ganji_phone_call_class:
            self.fd['owner_phone_pic'] = ganji_phone_call_class.contents[0]
            if str(ganji_phone_call_class).find('src='):                
                self.fd['owner_phone_pic'] = 'http://'+urlparse(url)[1]+ganji_phone_call_class.img['src']
            else:
                self.fd['owner_phone_pic'] = None            
        else:
            self.fd['owner_phone_pic'] = None
            
            
        #没有联系方式  return
        if not self.fd['owner_phone_pic']:raise     
        
        if re.search(self.house_price_regex_zu, response):
            house_price_zu = re.search(self.house_price_regex_zu, response).group(1)
            house_price_zu = house_price_zu.replace('元/月','')
            if house_price_zu.find("以上") != -1:
                self.fd['house_price_max'] = 0
                self.fd['house_price'] = int(house_price_zu.replace('以上',''))
            elif house_price_zu.find("以下") != -1:
                self.fd['house_price_max'] = int(house_price_zu.replace('以下',''))
                self.fd['house_price'] = 0
            elif house_price_zu.find("-") != -1:
                self.fd['house_price_max'] = int(house_price_zu.split('-')[1])
                self.fd['house_price'] = int(house_price_zu.split('-')[0])
            else:
                self.fd['house_price_max'] = 0
                self.fd['house_price'] = 0
        else:
            self.fd['house_price_max'] = 0
            self.fd['house_price'] = 0
        
        posttime=CSSSelector('span.pub_time')(tree)!=None and CSSSelector('span.pub_time')(tree)[0].text.strip() or None 
        if posttime:
            Y=int(time.strftime('%Y', time.localtime()))
            M=int(posttime.split(' ')[0].split('-')[0])
            D=int(posttime.split(' ')[0].split('-')[1])
            H=int(time.strftime('%H',time.localtime(time.time())))
            Min=int(time.strftime('%M',time.localtime(time.time())))
            s = datetime.datetime(Y,M,D,H,Min)
            posttime=str(int(time.mktime(s.timetuple())))
            self.fd['house_posttime'] =posttime 
        else:
            s=time.localtime(time.time())
            self.fd['house_posttime'] =str(int(time.mktime(s)))
            
        house_title=CSSSelector("div.detail_title h1")(tree)[0] !=None and CSSSelector("div.detail_title h1")(tree)[0].text.strip() or None
        self.fd['house_title'] = house_title.replace("(求购)","").replace("(求租)","").replace("(出售)","")
        

        if re.search(self.house_room_regex, response):
            house_room=re.search(self.house_room_regex, response).group(1)
            self.fd['house_room'] = int(house_room)
        else:
            self.fd['house_room'] = 0
            
        if re.search(self.house_hall_regex, response):
            house_hall=re.search(self.house_hall_regex, response).group(1)
            self.fd['house_hall'] = int(house_hall)
        else:
            self.fd['house_hall'] = 0
        
        if re.search(self.house_toilet_regex, response):
            house_toilet=re.search(self.house_toilet_regex, response).group(1)
            self.fd['house_toilet'] = int(house_toilet)
        else:
            self.fd['house_toilet'] = 0

        if re.search(self.house_veranda_regex, response):
            house_veranda=re.search(self.house_veranda_regex, response).group(1)
            self.fd['house_veranda'] = int(house_veranda)
        else:
            self.fd['house_veranda'] = 0

        house_title=CSSSelector("div.detail_title h1")(tree)[0] !=None and CSSSelector("div.detail_title h1")(tree)[0].text.strip() or None
        self.fd['house_title'] = house_title.replace("(求购)","").replace("(求租)","").replace("(出售)","")
        
        #描述        
        detail_box = soup.find('div',{'class':'detail_box'})
        if detail_box:
            house_desc = str(detail_box('p')[1])
            self.fd['house_desc'] = re.sub("<.*?>|\n|\r|\t|联系我时请说明是从赶集网上看到的","",house_desc)
        else:
            self.fd['house_desc'] = ""

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
            self.fd['house_region'] = str(area_a[0].string)
            self.fd['house_section'] = str(area_a[1].string)
        elif area_a and len(area_a)==1:
            self.fd['house_region'] = str(area_a[0].string)
            self.fd['house_section'] = ""
        else:
            self.fd['house_region'] = ""
            self.fd['house_section'] = ""
        request = None
        response = None
        soup=None
        tree=None
        del tree
        del request
        del response
        del soup
    def extractDict(self):        
        if checkPath(homepath,self.folder,self.urls):
            pass
        else:
            try:
                if self.kind=="1":
                    self.sell(self.urls)
                elif self.kind=="2":
                    self.rent(self.urls)
                elif self.kind=="3":
                    self.buy(self.urls)
                else:
                    self.require(self.urls)
                makePath(homepath,self.folder,self.urls)                
                #超过七天
                
#                if (time.time() -self.fd["posttime"]) > 7*24*36000:return
            except Exception,e:
                self.fd['house_title']=None
                msglogger.info("%s 链接采集异常"%self.urls)
#                print "%s||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||"%self.urls
            if isDEV:
#                self.fd.update(getDefaultVal(4))
                dfv=getDefaultVal(self.kind)
                for item in dfv.items() :
#                    print item[0],item[1]
                    if item[0] not in  self.fd:
                        self.fd[item[0]]=dfv.get(item[0])
                for item in dfv.items() :
                    print item[0],self.fd[item[0]],type(self.fd[item[0]])
                    
                return
            else:
                dfv=getDefaultVal(self.kind)
                for item in dfv.items() :
#                    print item[0],item[1]
                    if item[0] not in  self.fd:
                        self.fd[item[0]]=dfv.get(item[0])
            self.fd["is_checked"] = 1        
            self.fd["web_flag"]   = "gj"
            #print "%s %s %s %s %s"%(("%s.soufun.com"% self.citycode),self.citycode, self.kind ,time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())), self.urls)
            return self.fd
        
            if not self.fd["is_checked"]:
                for i in self.fd.items():
                    print i[0],i[1]
            print  "*"*80
#            if len(self.fd)==7 or len(self.fd)==17:
#                print "#####################################"
#                continue
#            req=urllib2.Request("http://site.jjr360.com/app.php", urllib.urlencode(self.fd))
#            p=self.br.open(req).read().strip()
#            print p.decode('gbk')
#            print  "*"*80
        
class fetchData(threading.Thread): 
    def __init__(self,d):
        threading.Thread.__init__(self)
        self.d=d
    def run(self):
        lc=LinkCrawl(self.d["citycode"],self.d["kind"])
        clinks=lc.runme()
        cc=ContentCrawl(clinks,self.d["citycode"],self.d["kind"])
        cc.extractDict()

class getLinksThread(threading.Thread):
    def __init__(self,d):
        threading.Thread.__init__(self)
        self.d=d
    def run(self):
        gc.enable()
        lc=LinkCrawl(self.d["citycode"],self.d["kind"])
        lc.runme()
        del gc.garbage[:]
def getLinks(d):
    lc=LinkCrawl(d["citycode"],d["kind"],d["st1"])
    while True:
        lc.runme()
        del gc.garbage[:]
        time.sleep(int(d["st2"]))
def getContent(clinks,citycode,kind,upc):
#    return
    cc=ContentCrawl(clinks,citycode,kind,upc)
    fd=cc.extractDict()
    res=""
    try:
        res=postHost(fd)
    except Exception,e:
        res=e
    print res
    msglogger.info("%s|%s|%s"%(clinks,res,fd))
    del gc.garbage[:]

        
if __name__=="__main__":    
#    lc=LinkCrawl(citycode="su",kind="1")
#    lc.runme()#    
    #url1 = "http://su.ganji.com/fang5/11071015_233901.htm"
    #url2 = "http://su.ganji.com/fang1/11071017_418972.htm"
    #url3 = "http://su.ganji.com/fang4/11062413_4152.htm"
    #url4 = "http://su.ganji.com/fang2/11070900_21214.htm"

#    cc=ContentCrawl("http://su.ganji.com/fang2/11071417_21820.htm",citycode="su",kind="4",upc=0)
    cc=ContentCrawl("http://su.ganji.com/fang5/tuiguang-4269169.htm",citycode="su",kind="1",upc=0)
    cc.extractDict()
#    while 1:
#        for i in range(1,5):
#            k = "%s" % str(i)
#            try:
#                lc=LinkCrawl(citycode="su",kind=k)
#                clinks=lc.runme()
#                cc=ContentCrawl(clinks,citycode="su",kind=k)
#                cc.extractDict()
#            except:
#                pass
            
