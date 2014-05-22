#coding=UTF-8
'''
Created on 2011-7-5

@author: Administrator
'''
import cookielib
import urllib2
from pyquery.pyquery import PyQuery
import re
from config import housetype, checkPath, makePath,citynameDict_sf, isDEV,\
    getDefaultVal
import datetime
import time
import threading
from BeautifulSoup import BeautifulSoup
from jjrlog import LinkLog
from jjrlog import msglogger
from common import postHost,printRsult
import gc
from urlparse import urlparse
gc.enable()
homepath="F:\\home\\spider\\"
getheader={
            "User-Agent": "Mozilla/5.0 (Windows NT 5.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
            }
class LinkCrawl(object):
    def __init__(self,citycode="",kind="",upc="5",st="3"):
        cj = cookielib.MozillaCookieJar()
        self.br=urllib2.build_opener(urllib2.HTTPHandler(),urllib2.HTTPCookieProcessor(cj),urllib2.HTTPRedirectHandler())
        self.header={
            "User-Agent":'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB6.6; .NET CLR 3.5.30729)',
        }
        self.clinks=[]
        self.pn=[]
        self.citycode=citycode
        self.kind=kind
        self.st=st
        if kind=="3":#1求购
            self.urlpath="http://esf.%s.soufun.com/qiugou/i3%s/"
            self.baseurl="http://esf.%s.soufun.com"%self.citycode
            self.folder="buy\\"
        elif kind=="4":#2求租
            self.urlpath="http://rent.%s.soufun.com/qiuzu/i3%s/"
            self.baseurl="http://rent.%s.soufun.com"%self.citycode
            self.folder="req\\"
        elif kind=="2":#出租
            self.urlpath="http://rent.%s.soufun.com/house/a21-i%s/"
            self.baseurl="http://rent.%s.soufun.com"%self.citycode
            self.folder="rent\\"
        elif kind=="1":#出售
            self.urlpath="http://esf.%s.soufun.com/house/a21-i%s/"
            self.baseurl="http://esf.%s.soufun.com"%self.citycode
            self.folder="sell\\"
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
                tm=tm and tm.replace("个人","") or ""
                link=self.baseurl+PyQuery(li)("p.housetitle a").attr("href")
            else: 
                tm=PyQuery(li)("span.li5").text()
                link=self.baseurl+PyQuery(li)("span.li2 a").attr("href")
            if self.kind=="4": 
                if PyQuery(li)("span.li1").text()=="合租 ":
                    continue
#            tm=PyQuery(li)("span.li5").text()
#            link=self.baseurl+PyQuery(li)("span.li2 a").attr("href")
            #link=self.baseurl+PyQuery(li)("span.li2 a").attr("href")
#            print link
            if u"天" in tm:
                s=tm.find(u"天")
                tm=tm[:s]
                if int(tm)<2:
                    links.append(link)
                else:
                    break
            elif u"小时" in tm:
                links.append(link)
            elif u"分钟" in tm:
                links.append(link)
            else:
                continue
            if not checkPath(homepath,self.folder,link):
                LinkLog.info("%s|%s"%(self.kind,link))
                try:
                    getContent(link,self.citycode,self.kind)
                except Exception,e:print "soufun getContent  Exception %s %s %s %s" %(e,link,self.kind,self.citycode)
            time.sleep(int(self.st))
#            fetch_quere.put({"mod":"soufang","link":link,"citycode":self.citycode,"kind":self.kind})
#        self.clinks.extend(links)
       
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
        try:
            p=self.br.open(req).read()
        except:
            raise
        p=unicode(p.decode("GB18030").encode("UTF-8"))
        if self.kind=="1":
            pg=PyQuery(p)("li#list_98").text()
        else:
            pg=PyQuery(p)("li#rentid_67").text()
#        pg=PyQuery(p)("li#rentid_67").text()
        if pg and re.search('''1/(\d+) ''', pg):
            pn=int(re.search('''1/(\d+) ''', pg).group(1))
#        print pn
        r=self.__getPageAllLink(p)
        if not r:
            return
        self.pn=range(2,int(pn)+1)
    def __getAllNeedLinks(self):
        for i in self.pn:
            if self.kind=="2" or self.kind=="1":
                i="3%s"%i
            url=self.urlpath%(self.citycode,i)
#            print url
            req=urllib2.Request(url, None, self.header)
            p=self.br.open(req).read()
            p=unicode(p.decode("GB18030").encode("UTF-8"))
            r=self.__getPageAllLink(p)
            if not r:
                break
    def runme(self):
        self.__initPageNum()
        self.__getAllNeedLinks()
#        print len(self.clinks)
#        return self.clinks
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
        elif kind=="2":
            self.folder="rent\\"
        elif kind=="3":
            self.folder="buy\\"
        else:
            self.folder="req\\"
        
        self.posttime_regx         = '''\((.*?)前更新'''
        self.owner_name_regx       = '''<dd>联 系 人：(.*?)</dd>'''
        self.owner_phone_regx      = '''<span class="telno0">(\d+)</span>'''
        self.owner_phone1_regx      = '''<span class="telno">(.*) <span class="telzhuan">转</span>(.*)</span><br>'''
        
        self.cityarea_regx         = '''\( <a .*>(.*)</a>  <a .*>.*</a> \)'''
        self.borough_section_regx  = '''\( <a .*>.*</a>  <a .*>(.*)</a> \)'''
        self.house_addr_regx       = '''地　　址：</span><a .*">(.*)</a>'''
        self.house_addr1_regx      = '''地　　址：</span>[\s]+<a .*>(.*)&nbsp;<span'''
        
        self.house_price_regx_rent      = '''租　　金：<span class="red20b">(\d+)</span>'''
        self.house_price_regx_sell      = '''总　　价：<span .*>(.*)</span>'''
        self.house_price_regx_buy      = '''<li class="right">不超过<span class="red20b">(\d+)<'''
        
        self.house_price_regx_req       = '''<li class="right">不超过<span class="red20b">(\d+)</span>元/月'''
        self.house_totalarea_regx_req   = '''不小于(\d+)平米'''
        self.house_totalarea_regx_rent  = '''<dd>出租面积：(.*)平方米</dd>'''
        self.house_totalarea_regx_sell  = '''建筑面积：<span .*>(.*)</span>'''  
        self.house_totalarea_regx_buy   = '''期望面积：</span>不小于(\d+)平米'''  
              
        
        self.house_room_regx       = '''(\d)室'''
        self.house_room1_regx      = '''(.{3})居'''
        self.house_hall_regx       = '''(\d)厅'''
        self.house_toilet_regx     = '''(\d)卫'''
        
        self.house_room_regx_sell       = '''(.{3})室'''
        self.house_hall_regx_sell       = '''(.{3})厅'''
        self.house_toilet_regx_sell     = '''(.{3})卫'''
        
        self.house_floor_regx      = '''第(\d+)层'''
        self.house_topfloor_regx   = '''共(\d+)层'''
        
        self.house_age_regx        = '''建筑年代：</span>(.*)年</dd>'''
        
        self.belong_regx           = '''产权性质：</span>(.*)</dd>''' 
        
        self.paytype_regx          = '''支付方式：(.*)</dd>'''
        self.house_toward_regx     = '''朝　　向：</span>(.*)</dd>'''
        self.house_type_regx       = '''物业类型：</span>(.*)</dd>'''
        self.house_fitment_regx    = '''装　　修：</span>(.*)</dd>'''
        self.house_support_regx    = '''房屋配套：</span><span .*>(.*)</span>''' 
        self.house_support1_regx   = '''房屋配套：</span>(.*)</dt>''' 
        
        
        self.house_desc_regx       = '''<div class="beizhu" .*><p>(.*?)</p>'''
        self.house_desc_regx_req   = '''<div class="qzbeizhu">(.*?)</p>'''
        
        
        
        
        self.house_posttime_regex="([\d]{4}-[\d]{1,2}-[\d]{1,2} [\d]{1,2}:[\d]{1,2}:[\d]{1,2})"
        
        
    def require(self,url): 
        hc= urlparse(url)[1].replace('.soufun.com',"").replace('zu.',"")  
        hc2=citynameDict_sf.get(hc)
        if hc2:
            self.fd['house_city']=hc2
        else:
            self.fd['house_city']=hc       
        cookiestore=cookielib.MozillaCookieJar()
        request = urllib2.Request(url,None , getheader)
        br = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiestore),urllib2.HTTPRedirectHandler())
        response=br.open(request).read()
        response=response and response.decode("GB18030").encode("UTF-8").replace('''<meta http-equiv="Content-Type" content="text/html; charset=gb2312" />''',"") or ""       
        soup = BeautifulSoup(response)
        
        
        
        
#        if self.parseHtml(self.house_posttime_regex, response):
#                   
#            posttime  = self.parseHtml(self.house_posttime_regex, response)
#            posttime = re.sub('<.*?>','',posttime)
#            self.fd['posttime1'] =posttime
#            if posttime.find('天') != -1:
#                self.fd['posttime'] =int(posttime.replace('天',''))*3600*24
#            elif posttime.find('小时') != -1:
#                self.fd['posttime'] =int(posttime.replace('小时',''))*3600
#            elif posttime.find('分钟') != -1:
#                self.fd['posttime'] =int(posttime.replace('分钟',''))*60
#            elif posttime.find('秒') != -1:
#                self.fd['posttime'] =int(posttime.replace('秒',''))
#            else:
#                self.fd['posttime'] = 0
#                
#        else:
#            self.fd["is_ok"] = False
#            return

        if self.parseHtml(self.house_posttime_regex, response):
            try:
                pt  = self.parseHtml(self.house_posttime_regex, response)
                t = time.strptime(pt, "%Y-%m-%d %H:%M:%S")
                s = datetime.datetime(int(t[0]),int(t[1]),int(t[2]),int(t[3]),int(t[4]),int(t[5]))
                posttime = int(time.mktime(s.timetuple()))
                self.fd['house_posttime']=str(posttime)
            except:
                s=time.localtime(time.time())
                self.fd['house_posttime'] =str(int(time.mktime(s)))
        else:
            s=time.localtime(time.time())
            self.fd['house_posttime'] =str(int(time.mktime(s)))
            
            
            
            
        ss=PyQuery(unicode(response,"UTF-8"))("dl.house dd")
        for sp in ss:
            spt=PyQuery(sp).text()
            if "面 积：" in spt:
                try:
                    area=self.parseHtml("([\d]+)", spt)
                except:
                    area=0
                if "不小于" in spt:
                    self.fd["house_area"]=area
                elif "不大于" in spt:
                    self.fd["house_area_max"]=area
                else:
                    self.fd["house_area"]=area
                break
        uls=PyQuery(unicode(response,"UTF-8"))("div.price ul")
        for ul in uls:
            ult=PyQuery(ul).text()
            if "期望租金：" in ult:
                try:
                    price=self.parseHtml("([\d]+)", ult)
                except:
                    price=0
                if "不超过" in ult:
                    self.fd["house_price_max"]=price
                elif "不低于" in ult:
                    self.fd["house_price"]=price
                else:
                    self.fd["house_price"]=price
                break
        
        info_class = soup.find('div',{'class':'info'})
        if info_class==None:
            self.fd['house_title']=None
            return 
        info_class_str = str(info_class)
        self.fd["house_title"]  = info_class.h1.span.contents[0].strip() if info_class.h1.span else ""
        tel = info_class.find('span',{'class':'tel'})
        if tel and tel.font:             
             self.fd["owner_phone"] = tel.font.contents[0]             
             if tel.font.nextSibling:
                 self.fd["owner_name"] = tel.font.nextSibling.strip()
             else:
                 self.fd["owner_name"] = ''
        else:
            self.fd['is_ok'] = False
            raise
         
        if info_class.ul and info_class.ul.table and info_class.ul.table.td:
            house_area = info_class.ul.table.td.contents[0].replace('[','')
            self.fd["house_addr"]=house_area            
            if house_area.find(' ') != -1:
                house_area = house_area.split(' ')
                self.fd["borough_name"] =house_area[1]
                self.fd["cityarea"]=house_area[0]
                self.fd["borough_section"]=house_area[1]                
            else:
                self.fd["borough_name"] =house_area
                self.fd["cityarea"]= ''
                self.fd["borough_section"]=''
        else:
            self.fd["borough_name"] =''
            self.fd["cityarea"]= ''
            self.fd["borough_section"]=''
            self.fd["house_addr"]=''
            
        house_class = soup.find('dl',{'class':'house'})
        house_class_str = str(house_class)
        
##        self.fd["house_price"]  = self.parseHtml(self.house_price_regx_req, response) if self.parseHtml(self.house_price_regx_req, response) else "0"
#        self.fd["house_price_min"]  ="0"
#        self.fd["house_price_max"]  =self.fd["house_price"]
        
        self.fd["house_totalarea"] = self.parseHtml(self.house_totalarea_regx_req, response) if self.parseHtml(self.house_totalarea_regx_req, response) else "0"
        self.fd["house_totalarea_max"] = self.fd["house_totalarea"]
        self.fd["house_totalarea_min"] = "0"
        
        self.fd["house_room"]   = self.houserhtnum(self.parseHtml(self.house_room1_regx, response)) if self.parseHtml(self.house_room1_regx, response) else "1"
        self.fd["house_hall"]    = "0"
        self.fd["house_toilet"]  = "0"
        
        self.fd["house_floor"]   = "0"
        self.fd["house_topfloor"]= "0"     
        self.fd["house_age"]     = "0"        
        
        house_support = self.parseHtml(self.house_support1_regx, response) if self.parseHtml(self.house_support1_regx, response) else "0" 
        house_support = house_support.replace('、',',')
        
        self.fd["house_deposit"] = "0"
        self.fd["paytype"]       = "0"
        self.fd["house_toward"]  = "0"
        self.fd["house_type"]    = "1"
        self.fd["house_fitment"] = "0"
        self.fd["house_support"] = '0'
        self.fd["house_support1"]= '0'#self.getsupport(house_support)
        
        qzbeizhu_class = soup.find('div',{'class':'qzbeizhu'})
        if qzbeizhu_class and qzbeizhu_class.p:
            self.fd["house_desc"] = soup.find('div',{'class':'qzbeizhu'}).p.contents[0].strip()
            self.fd["house_desc"] = re.sub("<.*?>|\n|\t|\r","",self.fd["house_desc"])
        else:
            self.fd["house_desc"] = ""

    def buy(self,url):
        hc= urlparse(url)[1].replace('.soufun.com',"").replace('esf.',"")  
        hc2=citynameDict_sf.get(hc)
        if hc2:
            self.fd['house_city']=hc2
        else:
            self.fd['house_city']=hc
        cookiestore=cookielib.MozillaCookieJar()
        request = urllib2.Request(url,None , getheader)
        br = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiestore),urllib2.HTTPRedirectHandler())
        response=br.open(request).read()
        response=response and response.decode("GB18030").encode("UTF-8").replace('''<meta http-equiv="Content-Type" content="text/html; charset=gb2312" />''',"") or ""
           
        soup = BeautifulSoup(response)
        
#        if self.parseHtml(self.posttime_regx, response):            
#            posttime  = self.parseHtml(self.posttime_regx, response)
#            self.fd['posttime1'] =posttime
#            if posttime.find('天') != -1:
#                self.fd['posttime'] =int(posttime.replace('天',''))*24*3600
#            elif posttime.find('小时') != -1:
#                self.fd['posttime'] =int(posttime.replace('小时',''))*3600
#            elif posttime.find('分钟') != -1:
#                self.fd['posttime'] =int(posttime.replace('分钟',''))*60
#            elif posttime.find('秒') != -1:
#                self.fd['posttime'] =int(posttime.replace('秒',''))
#            else:
#                self.fd['posttime'] = int(time.time())
#        else:
#            self.fd["is_ok"] = False
#            return
        if self.parseHtml(self.house_posttime_regex, response):
            try:
                pt  = self.parseHtml(self.house_posttime_regex, response)
                t = time.strptime(pt, "%Y-%m-%d %H:%M:%S")
                s = datetime.datetime(int(t[0]),int(t[1]),int(t[2]),int(t[3]),int(t[4]),int(t[5]))
                posttime = int(time.mktime(s.timetuple()))
                self.fd['house_posttime']=str(posttime)
            except:
                s=time.localtime(time.time())
                self.fd['house_posttime'] =str(int(time.mktime(s)))
        else:
            s=time.localtime(time.time())
            self.fd['house_posttime'] =str(int(time.mktime(s)))
        ss=PyQuery(unicode(response,"UTF-8"))("dl.house dd")
        for sp in ss:
            spt=PyQuery(sp).text()
            if "期望面积：" in spt:
                try:
                    area=self.parseHtml("([\d]+)", spt)
                except:
                    area=0
                if "不小于" in spt:
                    self.fd["house_area"]=area
                elif "不大于" in spt:
                    self.fd["house_area_max"]=area
                else:
                    self.fd["house_area"]=area
                break     
            
            
            
            
            
            
            
            
            
            
            
            
            
        
        info_class = soup.find('div',{'class':'info'})
        info_class_str = str(info_class)
        self.fd["house_title"]  = info_class.h1.span.contents[0].strip() if info_class.h1.span else ""
        tel = info_class.find('span',{'class':'tel'})
        if tel and tel.font:             
             self.fd["owner_phone"] = tel.font.contents[0]             
             if tel.font.nextSibling:
                 self.fd["owner_name"] = tel.font.nextSibling.strip()
             else:
                 self.fd["owner_name"] = ''
        else:
            self.fd['is_ok'] = False
            raise
         
        if info_class.ul and info_class.ul.table and info_class.ul.table.td:
            house_area = info_class.ul.table.td.contents[0].replace('[','')
            self.fd["house_addr"]=house_area            
            if house_area.find(' ') != -1:
                house_area = house_area.split(' ')
                self.fd["borough_name"] =house_area[1]
                self.fd["cityarea"]=house_area[0]
                self.fd["borough_section"]=house_area[1]                
            else:
                self.fd["borough_name"] =house_area
                self.fd["cityarea"]= ''
                self.fd["borough_section"]=''
        else:
            self.fd["borough_name"] =''
            self.fd["cityarea"]= ''
            self.fd["borough_section"]=''
            self.fd["house_addr"]=''
            
        house_class = soup.find('dl',{'class':'house'})
        house_class_str = str(house_class)
        
        self.fd["house_price"]  = self.parseHtml(self.house_price_regx_buy, response) if self.parseHtml(self.house_price_regx_buy, response) else "0"
        self.fd["house_price_min"]  ="0"
        self.fd["house_price_max"]  =self.fd["house_price"]
        
        self.fd["house_totalarea"] = self.parseHtml(self.house_totalarea_regx_buy, response) if self.parseHtml(self.house_totalarea_regx_buy, response) else "0"
        self.fd["house_totalarea_max"] = "0"
        self.fd["house_totalarea_min"] = self.fd["house_totalarea"]
        
           
        self.fd["house_room"]   = self.houserhtnum(self.parseHtml(self.house_room_regx_sell, info_class_str)) if self.parseHtml(self.house_room_regx_sell, info_class_str) else "0"
        self.fd["house_hall"]   = self.houserhtnum(self.parseHtml(self.house_hall_regx_sell, info_class_str)) if self.parseHtml(self.house_hall_regx_sell, info_class_str) else "0"
        self.fd["house_toilet"] = self.houserhtnum(self.parseHtml(self.house_toilet_regx_sell, info_class_str)) if self.parseHtml(self.house_toilet_regx_sell, info_class_str) else "0"
        
        self.fd["house_floor"] = "0"
        self.fd["house_topfloor"] = "0"
        self.fd["house_age"] = "0"
        self.fd["belong"] = "0"

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

        self.fd["house_deposit"] = "0"
        self.fd["house_toward"]  = "0"
        self.fd["house_type"]    = "0"
        self.fd["house_fitment"] = "0"
        self.fd["house_support"] = "0"
        
        beizhu_class = soup.find('p',{'class':'beizhu mt10'})
        if beizhu_class:
            self.fd["house_desc"] = str(beizhu_class).strip()            
            self.fd["house_desc"] = re.sub("<.*?>|\n|\t|\r","",self.fd["house_desc"])
            self.fd["house_desc"] = self.fd["house_desc"].replace('&nbsp;','')
        else:
            self.fd["house_desc"] = ""
     
     
    def sell(self,url):
        hc= urlparse(url)[1].replace('.soufun.com',"").replace('esf.',"")  
        hc2=citynameDict_sf.get(hc)
        if hc2:
            self.fd['house_city']=hc2
        else:
            self.fd['house_city']=hc
        cookiestore=cookielib.MozillaCookieJar()
        request = urllib2.Request(url,None , getheader)
        br = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiestore),urllib2.HTTPRedirectHandler())
        page=br.open(request).read()
        response=page and page.decode("GB18030").encode("UTF-8").replace('''<meta http-equiv="Content-Type" content="text/html; charset=gb2312" />''',"") or ""
        soup = BeautifulSoup(response)
        
#        if self.parseHtml(self.posttime_regx, response):            
#            posttime  = self.parseHtml(self.posttime_regx, response)
#            self.fd['posttime1'] =posttime
#            if posttime.find('天') != -1:
#                self.fd['posttime'] =int(posttime.replace('天',''))*24*3600
#            elif posttime.find('小时') != -1:
#                self.fd['posttime'] =int(posttime.replace('小时',''))*3600
#            elif posttime.find('分钟') != -1:
#                self.fd['posttime'] =int(posttime.replace('分钟',''))*60
#            elif posttime.find('秒') != -1:
#                self.fd['posttime'] =int(posttime.replace('秒',''))
#            else:
#                self.fd['posttime'] = 0
#        else:
#            self.fd["is_ok"] = False
#            return
        if self.parseHtml(self.house_posttime_regex, response):
            try:
                pt  = self.parseHtml(self.house_posttime_regex, response)
                t = time.strptime(pt, "%Y-%m-%d %H:%M:%S")
                s = datetime.datetime(int(t[0]),int(t[1]),int(t[2]),int(t[3]),int(t[4]),int(t[5]))
                posttime = int(time.mktime(s.timetuple()))
                self.fd['house_posttime']=str(posttime)
            except:
                s=time.localtime(time.time())
                self.fd['house_posttime'] =str(int(time.mktime(s)))
        else:
            s=time.localtime(time.time())
            self.fd['house_posttime'] =str(int(time.mktime(s)))
                
        
        info_class = soup.find('div',{'class':'info'})
        info_class_str = str(info_class)
        tel = info_class.find('span',{'class':'tel'})
        if tel and tel.span:
            self.fd["owner_phone"] = tel.span.contents[0]
        else:
            self.fd["owner_phone"]=""
            self.fd["is_ok"] = False
            raise
        
        self.fd["house_title"]  = info_class.h1.span.contents[0].strip() if info_class.h1.span else ""
        self.fd["owner_name"]  = self.parseHtml(self.owner_name_regx, response) if self.parseHtml(self.owner_name_regx, response) else ""
        
        #if self.parseHtml(self.owner_phone_regx, response):
            #self.fd["owner_phone"]  = self.parseHtml(self.owner_phone_regx, response)        
        #else:            
            #if re.search(self.owner_phone1_regx, response):
                #owner_phone=re.search(self.owner_phone1_regx, response)
                #self.fd["owner_phone"]=owner_phone.group(1)+"-"+owner_phone.group(2)
            #else:
                #self.fd["owner_phone"]=""
                #self.fd["is_ok"] = False
                #return
        
        house_class = soup.find('dl',{'class':'house'})
        house_class_str = str(house_class)
        if house_class:
            house_class_str = str(house_class)
            self.fd["borough_name"] = house_class.strong.contents[0] if house_class.strong else ''            
            self.fd["cityarea"]= self.parseHtml(self.cityarea_regx, response) if self.parseHtml(self.cityarea_regx, response) else ""
            self.fd["borough_section"]= self.parseHtml(self.borough_section_regx, response) if self.parseHtml(self.borough_section_regx, response) else ""
        else:
            self.fd["borough_name"] =''
            self.fd["cityarea"]=""
            self.fd["borough_section"]=""
        
        if self.parseHtml(self.house_addr_regx, response):
            self.fd["house_addr"]= self.parseHtml(self.house_addr_regx, response)
        else: 
            self.fd["house_addr"]= self.parseHtml(self.house_addr1_regx, response) if self.parseHtml(self.house_addr1_regx, response) else "" 
        
        self.fd["house_price"]  = self.parseHtml(self.house_price_regx_sell, response) if self.parseHtml(self.house_price_regx_sell, response) else "0"
        
        self.fd["house_totalarea"] = self.parseHtml(self.house_totalarea_regx_sell, response) if self.parseHtml(self.house_totalarea_regx_sell, response) else "0"
        
        self.fd["house_room"]   = self.houserhtnum(self.parseHtml(self.house_room_regx_sell, info_class_str)) if self.parseHtml(self.house_room_regx_sell, info_class_str) else "0"
        self.fd["house_hall"]   = self.houserhtnum(self.parseHtml(self.house_hall_regx_sell, info_class_str)) if self.parseHtml(self.house_hall_regx_sell, info_class_str) else "0"
        self.fd["house_toilet"] = self.houserhtnum(self.parseHtml(self.house_toilet_regx_sell, info_class_str)) if self.parseHtml(self.house_toilet_regx_sell, info_class_str) else "0"
        
        self.fd["house_floor"] = self.parseHtml(self.house_floor_regx, response) if self.parseHtml(self.house_floor_regx, response) else "0"
        self.fd["house_topfloor"] = self.parseHtml(self.house_topfloor_regx, response) if self.parseHtml(self.house_topfloor_regx, response) else "0"
        self.fd["house_age"] = self.parseHtml(self.house_age_regx, response) if self.parseHtml(self.house_age_regx, response) else "0"
        self.fd["belong"] = self.getbelong(self.parseHtml(self.belong_regx, response)) if self.parseHtml(self.belong_regx, response) else "0"
        
        
        house_toward  = self.parseHtml(self.house_toward_regx, response) if self.parseHtml(self.house_toward_regx, response) else "0"
        house_type    = self.parseHtml(self.house_type_regx, response) if self.parseHtml(self.house_type_regx, response) else "0"
        house_fitment = self.parseHtml(self.house_fitment_regx, response) if self.parseHtml(self.house_fitment_regx, response) else "0"
        house_support = self.parseHtml(self.house_support_regx, response) if self.parseHtml(self.house_support_regx, response) else "0" 
        
        self.fd["house_deposit"] = "0"
        self.fd["house_toward"]  = self.getforward(house_toward)
        self.fd["house_type"]    = self.gethousetype(house_type)
        self.fd["house_fitment"] = self.getfitment(house_fitment)
        self.fd["house_support"] = self.getsupport(house_support)
        
        beizhu_class = soup.find('div',{'class':'beizhu'})
        if beizhu_class and beizhu_class.div:
            self.fd["house_desc"] = str(beizhu_class.div).strip()            
            self.fd["house_desc"] = re.sub("<.*?>|\n|\t|\r","",self.fd["house_desc"])
            self.fd["house_desc"] = self.fd["house_desc"].replace('&nbsp;','')
        else:
            self.fd["house_desc"] = ""
    def parseHtml(self,regx,response):
        if re.search(regx, response):
            return re.search(regx, response).group(1)
        else:
            return None
    def rent(self,url):
        hc= urlparse(url)[1].replace('.soufun.com',"").replace('zu.',"")  
        hc2=citynameDict_sf.get(hc)
        if hc2:
            self.fd['house_city']=hc2
        else:
            self.fd['house_city']=hc
        cookiestore=cookielib.MozillaCookieJar()
        request = urllib2.Request(url,None , getheader)
        br = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiestore),urllib2.HTTPRedirectHandler())
        response=br.open(request).read()
        response=response and response.decode("GB18030").encode("UTF-8").replace('''<meta http-equiv="Content-Type" content="text/html; charset=gb2312" />''',"") or ""   
        soup = BeautifulSoup(response)
        
#        if self.parseHtml(self.posttime_regx, response):            
#            posttime  = self.parseHtml(self.posttime_regx, response)
#            self.fd['posttime1'] =posttime
#            if posttime.find('天') != -1:
#                self.fd['posttime'] =int(posttime.replace('天',''))*24*3600
#            elif posttime.find('小时') != -1:
#                self.fd['posttime'] =int(posttime.replace('小时',''))*3600
#            elif posttime.find('分钟') != -1:
#                self.fd['posttime'] =int(posttime.replace('分钟',''))*60
#            elif posttime.find('秒') != -1:
#                self.fd['posttime'] =int(posttime.replace('秒',''))
#            else:
#                self.fd['posttime'] = 0
#        else:
#            self.fd["is_ok"] = False
#            return

        if self.parseHtml(self.house_posttime_regex, response):
            try:
                pt  = self.parseHtml(self.house_posttime_regex, response)
                t = time.strptime(pt, "%Y-%m-%d %H:%M:%S")
                s = datetime.datetime(int(t[0]),int(t[1]),int(t[2]),int(t[3]),int(t[4]),int(t[5]))
                posttime = int(time.mktime(s.timetuple()))
                self.fd['house_posttime']=str(posttime)
            except:
                s=time.localtime(time.time())
                self.fd['house_posttime'] =str(int(time.mktime(s)))
        else:
            s=time.localtime(time.time())
            self.fd['house_posttime'] =str(int(time.mktime(s)))

        info_class = soup.find('div',{'class':'info'})
        info_class_str = str(info_class)
        
        self.fd["house_title"]  = info_class.h1.span.contents[0].strip() if info_class.h1.span else ""
        self.fd["owner_name"]  = self.parseHtml(self.owner_name_regx, response) if self.parseHtml(self.owner_name_regx, response) else ""
        
        
#        if self.parseHtml(self.owner_phone_regx, response):
#            self.fd["owner_phone"]  = self.parseHtml(self.owner_phone_regx, response)        
#        else:            
#            if re.search(self.owner_phone1_regx, response):
#                owner_phone=re.search(self.owner_phone1_regx, response)
#                self.fd["owner_phone"]=owner_phone.group(1)+"-"+owner_phone.group(2)
#            else:
#                self.fd["owner_phone"]=""
#                self.fd["is_ok"] = False
#                return
        tel=PyQuery(response)("span.telgr img").eq(0)
        self.fd["owner_phone_pic"]=PyQuery(tel).attr("src")
        
        
        
        house_class = soup.find('dl',{'class':'house'})
        house_class_str = str(house_class)
        if house_class:
            house_class_str = str(house_class)
            self.fd["borough_name"] = house_class.strong.contents[0] if house_class.strong else ''            
            self.fd["cityarea"]= self.parseHtml(self.cityarea_regx, response) if self.parseHtml(self.cityarea_regx, response) else ""
            self.fd["borough_section"]= self.parseHtml(self.borough_section_regx, response) if self.parseHtml(self.borough_section_regx, response) else ""
        else:
            self.fd["borough_name"] =''
            self.fd["cityarea"]=""
            self.fd["borough_section"]=""
        
        if self.parseHtml(self.house_addr_regx, response):
            self.fd["house_addr"]= self.parseHtml(self.house_addr_regx, response)
        else: 
            self.fd["house_addr"]= self.parseHtml(self.house_addr1_regx, response) if self.parseHtml(self.house_addr1_regx, response) else "" 
        
        self.fd["house_price"]  = self.parseHtml(self.house_price_regx_rent, info_class_str) if self.parseHtml(self.house_price_regx_rent, info_class_str) else "0"
        self.fd["house_totalarea"] = self.parseHtml(self.house_totalarea_regx_rent, info_class_str) if self.parseHtml(self.house_totalarea_regx_rent, info_class_str) else "0"
        
        self.fd["house_room"]   = self.parseHtml(self.house_room_regx, info_class_str) if self.parseHtml(self.house_room_regx, info_class_str) else "0"
        self.fd["house_hall"]   = self.parseHtml(self.house_hall_regx, info_class_str) if self.parseHtml(self.house_hall_regx, info_class_str) else "0"
        self.fd["house_toilet"] = self.parseHtml(self.house_toilet_regx, info_class_str) if self.parseHtml(self.house_toilet_regx, info_class_str) else "0"
        
        self.fd["house_floor"] = self.parseHtml(self.house_floor_regx, response) if self.parseHtml(self.house_floor_regx, response) else "0"
        self.fd["house_topfloor"] = self.parseHtml(self.house_topfloor_regx, response) if self.parseHtml(self.house_topfloor_regx, response) else "0"
        
        self.fd["house_age"] = self.parseHtml(self.house_age_regx, response) if self.parseHtml(self.house_age_regx, response) else "0"
        
        paytype       = self.parseHtml(self.paytype_regx, info_class_str) if self.parseHtml(self.paytype_regx, info_class_str) else "5"            
        house_toward  = self.parseHtml(self.house_toward_regx, response) if self.parseHtml(self.house_toward_regx, response) else "0"
        house_type    = self.parseHtml(self.house_type_regx, response) if self.parseHtml(self.house_type_regx, response) else "0"
        house_fitment = self.parseHtml(self.house_fitment_regx, response) if self.parseHtml(self.house_fitment_regx, response) else "0"
        house_support = self.parseHtml(self.house_support_regx, response) if self.parseHtml(self.house_support_regx, response) else "0" 
        
        
        
        self.fd["house_deposit"]=self.getpaytype(paytype)
        self.fd["house_toward"]  = self.getforward(house_toward)
        self.fd["house_type"]    = self.gethousetype(house_type)
        self.fd["house_fitment"] = self.getfitment(house_fitment)
        self.fd["house_support"] = self.getsupport(house_support)
            
        self.fd["house_desc"] = self.parseHtml(self.house_desc_regx, response) if self.parseHtml(self.house_desc_regx, response) else ""
        
        self.fd["house_desc"] = re.sub("<.*?>|\n|\t|\r","",self.fd["house_desc"])
         
            
         
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
            
        return ",".join([ support.get(s) and support.get(s) or "" for s in ss])
        
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
        return num.get(str) and num.get(str) or "0"
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
        if checkPath(homepath,self.folder,self.urls):
            return None
        else:
            self.fd["citycode"] = self.citycode
            self.fd["cityname"] = citynameDict_sf[self.citycode]
            self.fd["c"]="houseapi"
            self.fd["a"]="savehouse"        
            self.fd["is_checked"] = 1     
            self.fd["web_flag"]   = "sf"
            self.fd["is_ok"] = True
            #print self.urls
            try:
                if self.kind=="3":                    
                    self.buy(self.urls)
                    self.fd["house_flag"] = 3
                elif self.kind=="4":
                    self.require(self.urls)
                    self.fd["house_flag"] = 4
                elif self.kind=="2":                    
                    self.rent(self.urls)
                    self.fd["house_flag"] = 2
                elif self.kind=="1":
                    self.sell(self.urls)
                    self.fd["house_flag"] = 1
                #makePath(homepath,self.folder,self.urls)
                
                    
            except Exception,e:
                print "%s 链接采集异常   %s"%(self.urls,e)
                self.fd['house_title']=None
                msglogger.info("%s 链接采集异常"%self.urls)
            if isDEV:
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
                
            if not self.fd["is_ok"]:
                return
            if not self.fd["is_checked"]:
                printRsult(self.fd,self.kind) 
            self.fd['house_posttime'] = int(time.time()) - int(self.fd['house_posttime'])
            #print "%s %s %s %s"%(self.citycode, self.kind ,time.strftime("%Y-%m-%d %H:%M:%S",self.fd['posttime']), self.urls)
            return self.fd
            
        
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

def getLinks(d):
    lc=LinkCrawl(d["citycode"],d["kind"],d["st1"])
    while True:
        lc.runme()
        del gc.garbage[:]
        time.sleep(int(d["st2"]))
def getContent(clinks,citycode,kind):
    cc=ContentCrawl(clinks,citycode,kind)
    fd=cc.extractDict()
    res=""
    try:
        res=postHost(fd)
    except Exception,e:
        print clinks
        res=e
    msglogger.info("%s|%s|%s"%(clinks,res,""))
    return fd

  
if __name__=="__main__":
    
#    lc=LinkCrawl(citycode="wuxi",kind="4")
#    lc.runme()
    
    #cc=ContentCrawl("http://esf.wuxi.soufun.com/chushou/1_119888237_-1.htm#p=1",citycode="wuxi",kind="1")
    #cc=ContentCrawl("http://rent.wuxi.soufun.com/chuzu/1_49544277_-1.htm",citycode="wuxi",kind="2")
#    cc=ContentCrawl("http://esf.wuxi.soufun.com/chushou/1_119893906_-1.htm",citycode="wuxi",kind="1")
    cc=ContentCrawl("http://rent.suzhou.soufun.com/chuzu/1_49811782_-1.htm",citycode="suzhou",kind="2")
    cc.extractDict()
    #http://rent.suzhou.soufun.com/chuzu/1_49811782_-1.htm 2 suzhou
    
    
    
    
#    lf=file("link.log")
#    for link in lf.readlines():
#        cc=ContentCrawl(link,citycode="suzhou",kind="3")
#        cc.extractDict()
        
        
#    getDict({"citycode":"suzhou","kind":"1",})
