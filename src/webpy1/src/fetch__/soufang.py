#coding=UTF-8
'''
Created on 2011-7-5

@author: Administrator
'''
import cookielib
import urllib2
from pyquery.pyquery import PyQuery
import re
from config import housetype, checkPath, makePath
import datetime
import time
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
        self.clinks=[]
        self.pn=[]
        self.citycode=citycode
        self.kind=kind
        
        if kind=="3":#1求购
            self.urlpath="http://esf.%s.soufun.com/qiugou/i3%s/"
            self.baseurl="http://esf.%s.soufun.com"%self.citycode
        elif kind=="4":#2求租
            self.urlpath="http://rent.%s.soufun.com/qiuzu/i3%s/"
            self.baseurl="http://rent.%s.soufun.com"%self.citycode
        elif kind=="2":#出租
            self.urlpath="http://rent.%s.soufun.com/house/a21-i%s/"
            self.baseurl="http://rent.%s.soufun.com"%self.citycode
        elif kind=="1":#出售
            self.urlpath="http://esf.%s.soufun.com/house/a21-i%s/"
            self.baseurl="http://esf.%s.soufun.com"%self.citycode
    def __getPageAllLink(self,p):
        
#        if self.kind=="1":
#            lis=PyQuery(p)("div.qiuzu li")
#        elif self.kind=="2":
#            lis=PyQuery(p)("div.qiuzu li")
        if self.kind=="1" or self.kind=="2":
            lis=PyQuery(p)("div.house")
        else:
            lis=PyQuery(p)("div.qiuzu li")
        links=[]
        for li in lis:
#            if self.kind=="3":
#                tm=PyQuery(li)("p.time span").eq(1).text()
#                link=self.baseurl+PyQuery(li)("p.housetitle a").attr("href")
            if self.kind=="2" or self.kind=="1":
                tm=PyQuery(li)("p.time").text()
                tm=tm.replace("个人","")
                link=self.baseurl+PyQuery(li)("p.housetitle a").attr("href")
            else: 
                tm=PyQuery(li)("span.li5").text()
                link=self.baseurl+PyQuery(li)("span.li2 a").attr("href")
            if self.kind=="4": 
                if PyQuery(li)("span.li1").text()=="合租 ":
                    continue
#            tm=PyQuery(li)("span.li5").text()
#            link=self.baseurl+PyQuery(li)("span.li2 a").attr("href")
            print tm
            #link=self.baseurl+PyQuery(li)("span.li2 a").attr("href")
            if u"天" in tm:
                s=tm.find(u"天")
                tm=tm[:s]
                if int(tm)<8:
                    links.append(link)
            elif u"小时" in tm:
                links.append(link)
            elif u"分钟" in tm:
                links.append(link)
        self.clinks.extend(links)
       
        if self.kind=="1" or self.kind=="2":
            if len(links)!=30:
                return False
            else:
                return True
        else:
            if len(links)!=35:
                return False
            else:
                return True
    def __initPageNum(self):
        initurl=(self.urlpath%(self.citycode,"1"))[:-4]
        req=urllib2.Request(initurl, None, self.header)
        p=self.br.open(req).read()
        p=unicode(p.decode("GBK").encode("UTF-8"))
        if self.kind=="1":
            pg=PyQuery(p)("li#list_98").text()
        else:
            pg=PyQuery(p)("li#rentid_67").text()
#        pg=PyQuery(p)("li#rentid_67").text()
        if re.search('''1/(\d+) ''', pg):
            pn=int(re.search('''1/(\d+) ''', pg).group(1))
        print pn
        r=self.__getPageAllLink(p)
        if not r:
            return
        self.pn=range(2,int(pn)+1)
    def __getAllNeedLinks(self):
        for i in self.pn:
            if self.kind=="2" or self.kind=="1":
                i="3%s"%i
            url=self.urlpath%(self.citycode,i)
            req=urllib2.Request(url, None, self.header)
            p=self.br.open(req).read()
            p=unicode(p.decode("GBK").encode("UTF-8"))
            r=self.__getPageAllLink(p)
            if not r:
                break
    def runme(self):
        self.__initPageNum()
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
            self.folder="qiugou"
        else:
            self.folder="qiuzu"
        self.house_type_regx = "<dd><span class=\"gray9\">物业类型：</span>(.*)</dd>"
    def QiuZu(self,url):
        getheader={
               "User-Agent": "Mozilla/5.0 (Windows NT 5.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
               }
        request = urllib2.Request(url,None , getheader)
        response=self.br.open(request).read()
        response=response.decode("GBK").encode("UTF-8")
    #    print response
        if re.search('''搜房网</a> &gt; <a .* target="_blank">(.*)租房</a>''', response):
            self.fd["cityname"]=re.search('''搜房网</a> &gt; <a .* target="_blank">(.*)租房</a>''', response).group(1)
        else:
            self.fd["cityname"]=""
            
        if re.search(ur'''<tr><td>([\u4e00-\u9fa5]+) ([\u4e00-\u9fa5]+)\[''', unicode(response,"UTF-8")):
            area=re.search(ur'''<tr><td>([\u4e00-\u9fa5]+) ([\u4e00-\u9fa5]+)\[''', unicode(response,"UTF-8"))
            self.fd["cityarea"]=area.group(1)
            self.fd["borough_name"]=area.group(2)
        else:
            self.fd["cityarea"]=""
            self.fd["borough_name"]=""
            
        if re.search('''期望租金：</li>[\s]+<li class="right">(.*)<span class="red20b">(.*)</span>''', response):
            house_price=re.search('''期望租金：</li>[\s]+<li class="right">(.*)<span class="red20b">(.*)</span>''', response)
            if house_price.group(1)=="不超过":
                self.fd['house_price_max']=house_price.group(2) 
                self.fd['house_price_min']=0
            else:
                self.fd['house_price_max']=0
                self.fd['house_price_min']=house_price.group(2)
        else:
            self.fd['house_price_max']=0
            self.fd['house_price_min']=0
            
#        if re.search('''户　　型：</span>(.*)</dd>''', response):
#            house_room=re.search('''户　　型：</span>(.*)</dd>''', response)
#            self.fd["house_room"]=house_room.group(1)
#        else:
#            self.fd["house_room"]="" 
        if re.search("(.{3})室",response):
            if "居"!=re.search("(.{3})室",response).group(1):
                self.fd['house_room'] = self.houserhtnum(re.search("(.{3})室",response).group(1))
            else:
                if re.search("(.{3})居",response):
                    self.fd['house_room'] = self.houserhtnum(re.search("(.{3})居",response).group(1))
                else:
                    self.fd['house_room'] = ""
        else:
            self.fd['house_room'] = ""
            
        if re.search("(.{3})厅",response):
            self.fd['house_hall'] = self.houserhtnum(re.search("(.{3})厅",response).group(1))
        else:
            self.fd['house_hall'] = ""
            
        if re.search("(.{3})卫",response):
            self.fd['house_toilet'] = self.houserhtnum(re.search("(.{3})卫",response).group(1))
        else:
            self.fd['house_toilet'] = ""
        if re.search('''面　　积：</span>(.*)</dd>''', response):
            house_area=re.search('''面　　积：</span>(.*)</dd>''', response)
            self.fd["house_area"]=house_area.group(1)
        else:
            self.fd["house_area"]=""
        if re.search('''租赁方式：</span>(.*)</dd>''', response):
            rent_type=re.search('''租赁方式：</span>(.*)</dd>''', response)
            self.fd["rent_type"]=self.getrent_type(rent_type.group(1))
        else:
            self.fd["rent_type"]=""   
            
        if re.search('''房屋配套：</span>(.*)</dt>''', response):
            house_support=re.search('''房屋配套：</span>(.*)</dt>''', response)
            self.fd["house_support"]=self.getsupport(house_support.group(1))
        else:
            self.fd["house_support"]=""   
            
        if re.search('''<div class="qzbeizhu">([\s\S]*?)</div>''', response):
            house_desc=re.search('''<div class="qzbeizhu">([\s\S]*?)</div>''', response)
            self.fd["house_desc"]=house_desc.group(1).replace("<br />","").replace("联系时请提醒我您是在搜房租房网看到的，谢谢！","").replace("<p>","").replace("</p>","").strip()
        else:
            self.fd["house_desc"]=""  
            
            
        if re.search('''发布时间：(.*)\(''', response):
            posttime=re.search('''发布时间：(.*)\(''', response).group(1)
            dd=posttime.split(" ")[0]
            tt=posttime.split(" ")[1]
            Y=int(dd.split("-")[0])
            M=int(dd.split("-")[1])
            D=int(dd.split("-")[2])
            H=int(tt.split(":")[0])
            min=int(tt.split(":")[1])
            sd=int(tt.split(":")[2])
            s = datetime.datetime(Y,M,D,H,min,sd)
            posttime=int(time.mktime(s.timetuple()))
            self.fd['posttime'] =posttime 
        else:
            self.fd["posttime"]=""   
            
        if re.search('''联系电话:<font class="font20">(.*)</font>[\s]+(.*)[\s]+</span>''', response):
            owner=re.search('''联系电话:<font class="font20">(.*)</font>[\s]+(.*)[\s]+</span>''', response)
            self.fd["owner_phone"]=owner.group(1)
            self.fd["owner_name"]=owner.group(2)
        else:
            self.fd["owner_phone"]=""
            self.fd["owner_name"]=""
        
        if re.search('''<div class="title">[\s]+ <h1>[\s]+<span>[\s]+(.*)[\s]+</span>[\s]+</h1>''', response):
            house_title=re.search('''<div class="title">[\s]+ <h1>[\s]+<span>[\s]+(.*)[\s]+</span>[\s]+</h1>''', response)
            self.fd["house_title"]=house_title.group(1)
        else:
            self.fd["house_title"]=""

    def QiuGou(self,url):
        getheader={
               "User-Agent": "Mozilla/5.0 (Windows NT 5.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
               }
        cookiestore=cookielib.MozillaCookieJar()
        request = urllib2.Request(url,None , getheader)
        br = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiestore),urllib2.HTTPRedirectHandler())
        response=br.open(request).read()
        response=response.decode("GBK").encode("UTF-8")
        #print response
        if re.search('''搜房网</a> &gt; <a .* target="_blank">(.*)二手房</a>''', response):
            self.fd["cityname"]=re.search('''搜房网</a> &gt; <a .* target="_blank">(.*)二手房</a>''', response).group(1)
        else:
            self.fd["cityname"]=""
        if re.search('''发布时间：(.*)\(''', response):
            posttime=re.search('''发布时间：(.*)\(''', response).group(1)
            dd=posttime.split(" ")[0]
            tt=posttime.split(" ")[1]
            Y=int(dd.split("-")[0])
            M=int(dd.split("-")[1])
            D=int(dd.split("-")[2])
            H=int(tt.split(":")[0])
            min=int(tt.split(":")[1])
            sd=int(tt.split(":")[2])
            s = datetime.datetime(Y,M,D,H,min,sd)
            posttime=int(time.mktime(s.timetuple()))
            self.fd['posttime'] =posttime 
        else:
            self.fd["posttime"]="" 
        if re.search('''联系电话:<font class="font20">(.*)</font>[\s]+(.*)[\s]+</span>''', response):
            owner=re.search('''联系电话:<font class="font20">(.*)</font>[\s]+(.*)[\s]+</span>''', response)
            self.fd["owner_phone"]=owner.group(1)
            self.fd["owner_name"]=owner.group(2)
        else:
            self.fd["owner_phone"]=""
            self.fd["owner_name"]=""
        if re.search('''期望总价：</li>[\s]+<li class="right">(.*)<span class="red20b">(.*)</span>''', response):
            house_price=re.search('''期望总价：</li>[\s]+<li class="right">(.*)<span class="red20b">(.*)</span>''', response)
            if house_price.group(1)=="不超过":
                self.fd['house_price_max']=house_price.group(2) 
                self.fd['house_price_min']=0
            else:
                self.fd['house_price_max']=0
                self.fd['house_price_min']=house_price.group(2)
        else:
            self.fd['house_price_max']=0
            self.fd['house_price_min']=0
        
        if re.search("(.{3})室",response):
            self.fd['house_room'] = self.houserhtnum(re.search("(.{3})室",response).group(1))
        else:
            if re.search("(.{3})居",response):
                self.fd['house_room'] = self.houserhtnum(re.search("(.{3})室",response).group(1))
            else:
                self.fd['house_room'] = ""
            
        if re.search("(.{3})厅",response):
            self.fd['house_hall'] = self.houserhtnum(re.search("(.{3})厅",response).group(1))
        else:
            self.fd['house_hall'] = ""
            
        if re.search("(.{3})卫",response):
            self.fd['house_toilet'] = self.houserhtnum(re.search("(.{3})卫",response).group(1))
        else:
            self.fd['house_toilet'] = ""
#        if re.search('''期望户型：</span>(.*)</dd>''', response):
#            house_room=re.search('''期望户型：</span>(.*)</dd>''', response)
#        else:
#            self.fd["house_room"]="" 
            
        if re.search(ur'''<tr><td>([\u4e00-\u9fa5]+[\s]*[\u4e00-\u9fa5]+)*\[''', unicode(response,"UTF-8")):
            area=re.search(ur'''<tr><td>([\u4e00-\u9fa5]+[\s]*[\u4e00-\u9fa5]+)*\[''', unicode(response,"UTF-8"))
            if " " in area.group(1):
                self.fd["cityarea"]=area.group(1).split(" ")[0]
                #self.fd["borough_section"]=area.group(1).split(" ")[0]
                self.fd["borough_name"]=area.group(1).split(" ")[1]
            else:
                self.fd["cityarea"]=area.group(1)
                #self.fd["borough_section"]=area.group(1)
                self.fd["borough_name"]=area.group(1)
        else:
            self.fd["cityarea"]=""
            #self.fd["borough_section"]="" 
            self.fd["borough_name"]=""
        if re.search('''<p class="beizhu mt10">([\s\S]*?)</p>''', response):
            house_desc=re.search('''<p class="beizhu mt10">([\s\S]*?)</p>''', response)
            self.fd["house_desc"]=house_desc.group(1).replace("联系时您可以说：“您好，我从搜房网看到...”","")
        else:
            self.fd["house_desc"]=""     
           
        if re.search('''<div class="title">[\s]+ <h1>[\s]+<span>[\s]+(.*)[\s]+</span>[\s]+</h1>''', response):
            house_title=re.search('''<div class="title">[\s]+ <h1>[\s]+<span>[\s]+(.*)[\s]+</span>[\s]+</h1>''', response)
            self.fd["house_title"]=house_title.group(1)
        else:
            self.fd["house_title"]=""    
            
#        self.fd['info_type'] = '' 
        if re.search('''期望面积：</span>(.*)</dd>''', response):
            house_area=re.search('''期望面积：</span>(.*)</dd>''', response)
            if "不小于" in house_area.group(1):
                house_area=re.search('''(\d+)''', house_area.group(1))
                self.fd["house_totalarea_min"]=house_area.group(1)
                self.fd["house_totalarea_max"]=""
            else:
                house_area=re.search('''(\d+)''', house_area)
                self.fd["house_totalarea_min"]=""
                self.fd["house_totalarea_max"]=house_area.group(1)
        else:
            self.fd["house_totalarea_min"]=""
            self.fd["house_totalarea_max"]=""
            
        if re.search(ur'''期望楼层：</span>([\u4e00-\u9fa5]+)[\s]*</dd>''', unicode(response,"UTF-8")):
            house_floor=re.search(ur'''期望楼层：</span>([\u4e00-\u9fa5]+)[\s]*</dd>''', unicode(response,"UTF-8"))
            self.fd["house_floor"]=self.qiugouhousefloor(house_floor.group(1))
        else:
            self.fd["house_floor"]=""     
        if re.search('''配套设施：</span>(.*)</dt>''', response):
            house_support=re.search('''配套设施：</span>(.*)</dt>''', response)
            self.fd["house_support"]=self.getsupport(house_support.group(1))
        else:
            self.fd["house_support"]=""                   
          
        if re.search(ur'''期望朝向：</span>([\u4e00-\u9fa5]+)[\s]*</dd>''',  unicode(response,"UTF-8")):
            house_toward=re.search(ur'''期望朝向：</span>([\u4e00-\u9fa5]+)[\s]*</dd>''',  unicode(response,"UTF-8"))
            self.fd["house_toward"]=self.qiugouhousetoward(house_toward.group(1))
        else:
            self.fd["house_toward"]=""  
        if re.search('''期望房龄：</span>(.*)年.*</dd>''', response):
            house_age=re.search('''期望房龄：</span>(.*)年.*</dd>''', response)
            self.fd["house_age"]=self.gethouseage(house_age.group(1))
        else:
            self.fd["house_age"]=""
    def ChuShou(self,url):
        getheader={
               "User-Agent": "Mozilla/5.0 (Windows NT 5.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
               }
        cookiestore=cookielib.MozillaCookieJar()
        request = urllib2.Request(url,None , getheader)
        br = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiestore),urllib2.HTTPRedirectHandler())
        response=br.open(request).read()
        response=response.decode("GBK").encode("UTF-8")
        #print response
        esfsuzhouxq=PyQuery(response)("a#esfsuzhouxq_01")
        self.fd["cityname"]=esfsuzhouxq.text().replace("二手房","")
        
        if re.search('''<h1><span  >(.*)</span> </h1>''', response):
            house_title=re.search('''<h1><span  >(.*)</span> </h1>''', response).group(1)
            self.fd["house_title"]=house_title
        else:
            self.fd["house_title"]=""
        if re.search('''总　　价：<span .*>(.*)</span>''', response):
            house_price=re.search('''总　　价：<span .*>(.*)</span>''', response).group(1)
            self.fd["house_price"]=house_price
        else:
            self.fd["house_price"]=""
            
        if re.search('''建筑面积：<span .*>(.*)</span>''', response):
            house_totalarea=re.search('''建筑面积：<span .*>(.*)</span>''', response).group(1)
            self.fd["house_totalarea"]=house_totalarea
        else:
            self.fd["house_totalarea"]=""
            
        if re.search('''<span class="font20">(.*)</span></span''', response):
            owner_phone=re.search('''<span class="font20">(.*)</span></span''', response).group(1)
            self.fd["owner_phone"]=owner_phone
        else:
            self.fd["owner_phone"]=""
        if re.search('''<strong style="font-size:14px;">(.*)</strong>''', response):
            borough_name=re.search('''<strong style="font-size:14px;">(.*)</strong>''', response).group(1)
            self.fd["borough_name"]=borough_name
        else:
            self.fd["borough_name"]=""
        if re.search('''\( <a .*>(.*)</a>  <a .*>(.*)</a> \)''', response):
            borough_section1=re.search('''\( <a .*>(.*)</a>  <a .*>(.*)</a> \)''', response).group(1)
            borough_section2=re.search('''\( <a .*>(.*)</a>  <a .*>(.*)</a> \)''', response).group(2)
            self.fd["cityarea"]=borough_section1
            self.fd["borough_section"]=borough_section2
        else:
            self.fd["cityarea"]=""
            self.fd["borough_section"]=""
        if re.search('''地　　址：</span><a .*>(.*)</a>''', response):
            house_addr=re.search('''地　　址：</span><a .*>(.*)</a>''', response).group(1)
            self.fd["house_addr"]=house_addr
        else:
            if re.search('''地　　址：</span>(.*)</dt>''', response):
                house_addr=re.search('''地　　址：</span>(.*)</dt>''', response).group(1)
                self.fd["house_addr"]=house_addr
            else:
                self.fd["house_addr"]=""
            
        if re.search("(.{3})室",response):
            self.fd['house_room'] = self.houserhtnum(re.search("(.{3})室",response).group(1))
        else:
            self.fd['house_room'] = ""
            
        if re.search("(.{3})厅",response):
            self.fd['house_hall'] = self.houserhtnum(re.search("(.{3})厅",response).group(1))
        else:
            self.fd['house_hall'] = ""
            
        if re.search("(.{3})卫",response):
            self.fd['house_toilet'] = self.houserhtnum(re.search("(.{3})卫",response).group(1))
        else:
            self.fd['house_toilet'] = ""
        if re.search('''朝　　向：</span>(.*)</dd>''', response):
            house_toward=re.search('''朝　　向：</span>(.*)</dd>''', response).group(1)
            self.fd["house_toward"]=self.getforward(house_toward)
        else:
            self.fd["house_toward"]=""
        if re.search('''建筑年代：</span>(.*)年</dd>''', response):
            house_age=re.search('''建筑年代：</span>(.*)年</dd>''', response).group(1)
            self.fd["house_age"]=house_age
        else:
            self.fd["house_age"]=""
            
        if re.search('''户　　型：</span>(.*)</dt>''', response):
            house_type=re.search('''户　　型：</span>(.*)</dt>''', response).group(1)
            self.fd["house_type"]=house_type
        else:
            self.fd["house_type"]=""    
                        
        if re.search('''楼　　层：</span>第(\d+)层\(共(\d+)层\)</dd>''', response):
            house_f1=re.search('''楼　　层：</span>第(\d+)层\(共(\d+)层\)</dd>''', response).group(1)
            house_f2=re.search('''楼　　层：</span>第(\d+)层\(共(\d+)层\)</dd>''', response).group(2)
            self.fd["house_floor"]=house_f1
            self.fd["house_topfloor"]=house_f2
            
            
        else:
            self.fd["house_floor"]=""
            self.fd["house_topfloor"]=""  
            
        if re.search('''装　　修：</span>(.*)</dd>''', response):
            house_fitment=re.search('''装　　修：</span>(.*)</dd>''', response).group(1)
            self.fd["house_fitment"]=self.getfitment(house_fitment)
        else:
            self.fd["house_fitment"]=""

        if re.search('''产权性质：</span>(.*)</dd>''', response):
            belong=re.search('''产权性质：</span>(.*)</dd>''', response).group(1)
            self.fd["belong"]=self.getbelong(belong)
        else:
            self.fd["belong"]=""
                
        if re.search('''<div class="beizhu">(.*)</div>''', response):
            beizhu=re.search('''<div class="beizhu">(.*)</div>''', response).group(1)
            self.fd["house_desc"]=PyQuery(beizhu).text().encode('raw_unicode_escape') 
         
       
        if re.search('''发布时间：(.*)</p>''', response):
            posttime=re.search('''发布时间：(.*)</p>''', response).group(1)
            posttime=re.sub(r"\(.*\)", "", posttime)
            dd=posttime.split(" ")[0]
            tt=posttime.split(" ")[1]
            Y=int(dd.split("-")[0])
            M=int(dd.split("-")[1])
            D=int(dd.split("-")[2])
            H=int(tt.split(":")[0])
            min=int(tt.split(":")[1])
            sd=int(tt.split(":")[2])
            s = datetime.datetime(Y,M,D,H,min,sd)
            posttime=int(time.mktime(s.timetuple()))
            self.fd['posttime'] =posttime 
        else:
            self.fd["posttime"]=""                 
        
        if re.search('''联 系 人：(.*)</dd>''', response):
            owner_name=re.search('''联 系 人：(.*)</dd>''', response).group(1)
            self.fd["owner_name"]=re.sub('<.*>','',owner_name)
        else:
            self.fd["owner_name"]="" 
            
        #房屋类型
        if re.search(self.house_type_regx, response):
            house_type=re.search(self.house_type_regx, response).group(1)
            self.fd["house_type"]=self.gethousetype(house_type)
        else:
            self.fd["house_type"]=""    
        
            
    
    def ChuZhu(self,url):
        getheader={
               "User-Agent": "Mozilla/5.0 (Windows NT 5.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
               }
        cookiestore=cookielib.MozillaCookieJar()
        request = urllib2.Request(url,None , getheader)
        br = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiestore),urllib2.HTTPRedirectHandler())
        response=br.open(request).read()
        response=response.decode("GBK").encode("UTF-8")
    #    print response
        if re.search('''搜房网</a> &gt; <a .* target="_blank">(.*)租房</a>''', response):
            self.fd["cityname"]=re.search('''搜房网</a> &gt; <a .* target="_blank">(.*)租房</a>''', response).group(1)
        else:
            self.fd["cityname"]=""
            
        if re.search('''租　　金：<span class="red20b">(\d+)</span>''', response):
            house_price=re.search('''租　　金：<span class="red20b">(\d+)</span>''', response).group(1)
            self.fd["house_price"]=house_price
        else:
            self.fd["house_price"]=""
 
        if re.search('''户　　型：<span class="tel14 blod">(.*)</span>''', response):
            house_type=re.search('''户　　型：<span class="tel14 blod">(.*)</span>''', response).group(1)
            try:
                house_type=house_type.strip()
            except:
                pass
            blank=house_type.rfind(" ")
            if house_type.find("室")!= -1:
                house_room=house_type[blank+1:house_type.find("室")]
                blank=house_type.find("室")+3
            else:
                house_room=None
            if house_type.find("厅")!=-1:
                house_hall=house_type[blank:house_type.find("厅")]
                blank=house_type.find("厅")+3
            else:
                house_hall=None
            if house_type.find("卫")!=-1:
                house_toilet=house_type[blank:house_type.find("卫")]
            else:
                house_toilet=None
                
            self.fd['house_room'] = house_room
            self.fd['house_hall'] = house_hall
            self.fd['house_toilet'] = house_toilet
        else:
            self.fd['house_room'] = None
            self.fd['house_hall'] = None
            self.fd['house_toilet'] = None
        
        
        
        
        if re.search('''<dd>出租面积：(.*)平方米</dd>''', response):
            house_totalarea=re.search('''<dd>出租面积：(.*)平方米</dd>''', response).group(1)
            self.fd["house_totalarea"]=house_totalarea
        else:
            self.fd["house_totalarea"]=""
            
        if re.search('''支付方式：(.*)</dd> ''', response):
            house_paytype=re.search('''支付方式：(.*)</dd> ''', response).group(1)
            self.fd["paytype"]=self.getpaytype(house_paytype) 
        else:
            self.fd["paytype"]=""
        
        if re.search('''<dd>租赁方式：(.*)</dd>''', response):
            house_type=re.search('''<dd>租赁方式：(.*)</dd>''', response).group(1)
            self.fd["rent_type"]=self.getrent_type(house_type)
        else:
            self.fd["rent_type"]=""
            
        if re.search('''<strong style="font-size:14px;">(.*)</strong>''', response):
            borough_name=re.search('''<strong style="font-size:14px;">(.*)</strong>''', response).group(1)
            self.fd["borough_name"]=borough_name
        else:
            self.fd["borough_name"]=""
        #    
        if re.search('''\( <a .* target="_blank">(.*)</a>  <a .* target="_blank">(.*)</a> \) ''', response):
            borough_section1=re.search('''\( <a .* target="_blank">(.*)</a>  <a .* target="_blank">(.*)</a> \) ''', response).group(1)
            borough_section2=re.search('''\( <a .* target="_blank">(.*)</a>  <a .* target="_blank">(.*)</a> \) ''', response).group(2)
            self.fd["cityarea"]=borough_section1
            self.fd["borough_section"]=borough_section2
        else:
            self.fd["cityarea"]=""
            self.fd["borough_section"]=""
            
            
        if re.search('''地　　址：</span><a .*">(.*)</a>''', response):
            house_addr=re.search('''地　　址：</span><a .*">(.*)</a>''', response).group(1)
            self.fd["house_addr"]=house_addr
        else:
            if re.search('''地　　址：</span>[\s]+<a .*>(.*)&nbsp;<span ''', response):
                house_addr=re.search('''地　　址：</span>[\s]+<a .*>(.*)&nbsp;<span ''', response).group(1)
                self.fd["house_addr"]=house_addr
            else:
                self.fd["house_addr"]=""
        
        
        #
        if re.search('''楼　　层：</span>第(\d+)层\(共(\d+)层\)</dd>''', response):
            house_f1=re.search('''楼　　层：</span>第(\d+)层\(共(\d+)层\)</dd>''', response).group(1)
            house_f2=re.search('''楼　　层：</span>第(\d+)层\(共(\d+)层\)</dd>''', response).group(2)
            self.fd["house_floor"]=house_f1
            self.fd["house_topfloor"]=house_f2
            
            
        else:
            self.fd["house_floor"]=""
            self.fd["house_topfloor"]=""
            
            
        if re.search('''朝　　向：</span>(.*)</dd>''', response):
            house_toward=re.search('''朝　　向：</span>(.*)</dd>''', response).group(1)
            self.fd["house_toward"]=self.getforward(house_toward)
        else:
            self.fd["house_toward"]=""
        
        
        if re.search('''物业类型：</span>(.*)</dd>''', response):
            house_type=re.search('''物业类型：</span>(.*)</dd>''', response).group(1)
            self.fd["house_type"]=self.gethousetype(house_type)
        else:
            self.fd["house_type"]=""
            
        if re.search('''装　　修：</span>(.*)</dd>''', response):
            house_fitment=re.search('''装　　修：</span>(.*)</dd>''', response).group(1)
            self.fd["house_fitment"]=self.getfitment(house_fitment)
        else:
            self.fd["house_fitment"]=""
            
        if re.search('''房屋配套：</span><span .*>(.*)</span>''', response):
            house_support=re.search('''房屋配套：</span><span .*>(.*)</span>''', response).group(1)
            self.fd["house_support"]=self.getsupport(house_support)
        else:
            self.fd["house_support"]=""
            
            
        if re.search('''<div class="beizhu" .*><p>([\s\S]*?)</div>''', response):
            house_desc=re.search('''<div class="beizhu" .*><p>([\s\S]*?)</div>''', response).group(1)
            self.fd["house_desc"]=house_desc.replace("<p>","").replace("</p>","")
        else:
            self.fd["house_desc"]=""
            
        if re.search('''<dd>联 系 人：(.*?)</dd>''', response):
            owner_name=re.search('''<dd>联 系 人：(.*?)</dd>''', response).group(1)
            self.fd["owner_name"]=owner_name.strip()
        else:
            self.fd["owner_name"]="" 
            
        if re.search('''发布时间：(.*)</p>''', response):
            posttime=re.search('''发布时间：(.*)</p>''', response).group(1)
            posttime=re.sub(r"\(.*\)", "", posttime)
            dd=posttime.split(" ")[0]
            tt=posttime.split(" ")[1]
            Y=int(dd.split("-")[0])
            M=int(dd.split("-")[1])
            D=int(dd.split("-")[2])
            H=int(tt.split(":")[0])
            min=int(tt.split(":")[1])
            sd=int(tt.split(":")[2])
            s = datetime.datetime(Y,M,D,H,min,sd)
            posttime=int(time.mktime(s.timetuple()))
            self.fd['posttime'] =posttime 
        else:
            self.fd["posttime"]=""      
            
        if re.search('''<h1><span>(.*)</span></h1>''', response):
            house_title=re.search('''<h1><span>(.*)</span></h1>''', response).group(1)
            self.fd["house_title"]=house_title.strip()
        else:
            self.fd["house_title"]="" 
            
        if re.search('''<span class="telno0">(\d+)</span>''', response):
            owner_phone1=re.search('''<span class="telno0">(\d+)</span>''', response).group(1)
            self.fd["owner_phone"]=owner_phone1
        else:
            
            if re.search('''<span class="telno">(.*) <span class="telzhuan">转</span>(.*)</span><br>''', response):
                owner_phone1=re.search('''<span class="telno">(.*) <span class="telzhuan">转</span>(.*)</span><br>''', response)
                self.fd["owner_phone"]=owner_phone1.group(1)+"转"+owner_phone1.group(2)
            else:
                self.fd["owner_phone"]=""
         
    def getfitment(self,str):
        fitment={
                 "毛坯":"1",
                 "简单装修":"2",
                 "中等装修":"3",
                 "精装修":"4",
                 "豪华装修":"5",
                 }
        return fitment.get(str) and fitment.get(str) or "3"
    def getforward(self,str):
        forward={
                 "南北通透":"1",
                 "东西向":"2",
                 "朝南":"3",
                 "朝比":"4",
                 "朝东":"5",
                 "朝西":"6",
                 "不限":"0",
                 }
        return forward.get(str) and forward.get(str) or "0"
    def getsupport(self,str):
        support={
                 "煤气/天然气":"1",
                 "暖气":"2",
                 "车位/车库":"3",
                 "电梯":"4",
                 "储藏室/地下室":"5",
                 "花园/小院":"6",
                 "露台":"7",
                 "阁楼":"8",
                 
                 "宽带":"1",
                 "空调":"2",
                 "冰箱":"3",
                 "洗衣机":"4",
                 "热水器":"5",
                 "厨具":"6",
                 "床":"7",
                 "家具":"8",
                 "有线电视":"9",
                 "微波炉":"10",
                 "煤气/天然气":"11",
                 "暖气":"12",
                 "车位":"13",
                 "电梯":"14",
                 "露台/花园":"15",
                 "储藏室/地下室":"16",
                 "电话":"17",
                 }
        ss=str.split(",")
            
        return [ support.get(s) and support.get(s) or "" for s in ss]
        
    def gethousetype(self ,str):
        housetype={
                  "普通住宅":"1",
                  "住宅":"1",
                 "酒店式公寓":"2",
                 "商住楼":"3",
                 "拆迁安置房":"4",
                 "老新村":"5",
                  }
        return  housetype.get(str) and  housetype.get(str) or""
    def gethousestruct(self):
        housestruct={
                  "平层":"1",
                 "复式":"2",
                 "跃层":"3",
                 "错层":"4",
                 "开间":"5",
                  }
    def gethouseother(self):
        houseother={
                    "拎包入住":"1",
                    "家电齐全":"2",
                    "可上网":"3",
                    "可做饭":"4",
                    "可洗澡":"5",
                    "空调房":"6",
                    "可看电视":"7",
                    "有暖气":"8",
                    "有车位":"9",
                    }
        
    def getrent_type(self,str):
        rent_type={
                  "整租":"1",
                  "合租":"2",
                  "合租单间":"3",
                  "合租床位":"4",
                  }
        return rent_type.get(str) and rent_type.get(str)or "1"
    def getpaytype(self,str):
        paytype={
                 "月付":"1",
                 "季付":"2",
                 "半年付":"3",
                 "年付":"4",
                 "面议":"5",
                 }
        return paytype.get(str) and paytype.get(str) or "5" 
    def getbelong(self,str):
        belong={
                "个人产权":"1",
                "使用权":"2",
                }
        return belong.get(str) and  belong.get(str) or "1" 
    def gethouseage(self,str):
        age={
             "2":"1",
             "2-5":"2",
             "5-10":"3",
             "10":"4",
             }
        return age.get(str) and age.get(str) or "2"
    def houserhtnum(self,str):
        num={
             "一":"1",
             "二":"2",
             "两":"2",
             "三":"3",
             "四":"4",
             "五":"5",
             "六":"6",
             "七":"7",
             "八":"8",
             "九":"9",
             }
        return num.get(str) and num.get(str) or ""
    def qiugouhousefloor(self,str):
        floor={
               "不限":"0",
               "底层":"1",
               "中低层":"2",
               "高层":"3",
               "顶层":"4",
               "地下室":"5",
               }
        return floor.get(str) or floor.get(str) or "0" 
    def qiugouhousetoward(self,str):
        twd={
               "不限":"0",
               "南北":"1",
               "东西":"2",
               "东南":"3",
               "东北":"4",
               "西南":"5",
               "西北":"6",
               "东":"7",
               "西":"8",
               "南":"9",
               "北":"10",
               }
        return twd.get(str) or twd.get(str) or "0" 
    def extractDict(self):
        self.fd["citycode"]=self.citycode
        for url in self.urls:
            if False:#checkPath(homepath,self.folder,url):
                continue
            else:
                if self.kind=="3":
                    self.QiuGou(url)
                elif self.kind=="4":
                    self.QiuZu(url)
                elif self.kind=="2":
                    self.ChuZhu(url)
                elif self.kind=="1":
                    self.ChuShou(url)
#                makePath(homepath,self.folder,url)
            #do anything
            for i in self.fd.items():
                print i[0],i[1]
            
        
def getDict(d):
    lc=LinkCrawl(d["citycode"],d["kind"])
    clinks=lc.runme()
    cc=ContentCrawl(clinks,d["citycode"],d["kind"])
    cc.extractDict()
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
#    lc=LinkCrawl(citycode="suzhou",kind="1")
#    lc.runme()

    cc=ContentCrawl(["http://esf.suzhou.soufun.com/chushou/3_12818861.htm"],citycode="suzhou",kind="1")
    cc.extractDict()
#    getDict({"citycode":"suzhou","kind":"1",})