#coding=UTF-8
'''
Created on 2011-7-4

@author: Administrator
'''
import cookielib
import urllib2
from pyquery.pyquery import PyQuery
import re
import time
import datetime
from config import housetype
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
        self.baseUrl="http://%s.sofang.com"%self.citycode
        if kind=="1":
            self.urlpath="ershoufang"
        else:
            self.urlpath="zufang"
    def __initPageNum(self):
        initurl="%s/%s/&act=personal&options="%(self.baseUrl,self.urlpath)
        req=urllib2.Request(initurl, None, self.header)
        p=self.br.open(req).read()
        pg=PyQuery(p)("div#houses div.fl")
        if re.search('''(\d+)''',pg.text()):
            pg=re.search('''(\d+)''',pg.text()).group(1)
        r=self.__getPageAllLink(p)
        if not r:
            return
            
        self.pn= [i for i in range(int(pg)+1)][2:]
        print ""
    def __getPageAllLink(self,p):
        items=PyQuery(p)("li.item")   
        links=[] 
        for item in items:
            t=PyQuery(item)("div.summary p.time").text()
            if re.search('''(\d{2}\-\d{2})''',t):
                tm="%s-%s"%(time.strftime('%Y', time.localtime()),re.search('''(\d{2}\-\d{2})''',t).group(1))
                if time.strptime(tm, "%Y-%m-%d")>time.strptime(self.endtime, "%Y-%m-%d"):
                    links.append(self.baseUrl+PyQuery(item)("div.summary h3 a").attr("href"))
                    
            elif re.search('''(\d{2}\:\d{2})''',t):
                links.append(self.baseUrl+PyQuery(item)("div.summary h3 a").attr("href"))
        self.clinks.extend(links)
        if self.urlpath=="ershoufang" and len(links)!=10:
            return False
        elif self.urlpath=="zufang" and len(links)!=20:
            return False
        else:
            return True
    def extractDict(self):
        for link in self.clinks:
            req=urllib2.Request(link, None, self.header)
            page=self.br.open(req)
            
    def __getAllNeedLinks(self):
        for i in self.pn:
            url="%s/%s/&act=personal&page=%s"%(self.baseUrl,self.urlpath,i,)
            req=urllib2.Request(url, None, self.header)
            p=self.br.open(req).read()
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
        self.citycode=citycode
        self.housetypes=["平房","普通住宅","商住两用","公寓","别墅"]
        self.fd={}
        self.ht_r='''物业类型：</span>(.*)</li>'''
        self.ad_r='''地　　址：</span>(.*)</li>'''
        self.ca_r='''<iframe src="/ditu\.php\?city=&country=([\u4e00-\u9fa5]+)&'''
        self.fm_r='''装　　修：</span>(.*)</li>'''
        self.bl_r='''产权性质：</span>(.*)</li>'''
        self.hp_r='''<em>(.*)</em>万元'''
        self.hta_r='''建筑面积：</span><em>(.*)</em> 平米</li>'''
        self.hrht_r='''户　　型：</span>(.*)</li>'''
        self.hf_r='''楼　　层：</span>第(.*)层\(共(.*)层\)</li>'''
        self.ha_r='''建筑年代：</span>(\d+)年</li>'''
        self.hs_r='''配套设施：</span>(.*)</li>'''
        self.nm_r='''名　　称：</span>(.*)</li>'''
        self.hd_r='''<div class="bd" style="font-size:13px;">\n(.*)\n</div>\n'''
    def extractDict(self):
        self.fd["citycode"]=self.citycode
        for url in self.urls:
            req=urllib2.Request(url, None, self.header)
            page=self.br.open(req).read()
            if re.search(self.ht_r, page):
                if "商铺"==re.search(self.ht_r, page).group(1):
                    continue
                else:
                    ht=housetype(re.search(self.ht_r, page).group(1))
                    self.fd["house_type"]=ht
                    #lambda a: a and self.fd["borough_section"]=a.group(1) or self.fd["borough_section"]=""
                    self.fd["borough_section"]=re.search(self.ad_r, page)!=None and re.search(self.ad_r, page).group(1) or ""
                    self.fd["cityarea"]=re.search(self.ca_r, page)!=None and re.search(self.ca_r, page).group(1) or ""
                    self.fd["house_fitment"]=re.search(self.fm_r, page)!=None and re.search(self.fm_r, page).group(1) or ""
                    self.fd["house_kind"]=self.kind
                    self.fd["belong"]=re.search(self.bl_r, page)!=None and re.search(self.bl_r, page).group(1) or ""
                    self.fd["house_price"]=re.search(self.hp_r, page)!=None and re.search(self.hp_r, page).group(1) or ""
                    self.fd["house_totalarea"]=re.search(self.hta_r, page)!=None and re.search(self.hta_r, page).group(1) or ""
                    house_type=re.search(self.hrht_r, page)!=None and re.search(self.hrht_r, page).group(1) or ""
                    blank=0
                    if house_type.find("室")!= -1:
                        self.fd["house_room"]=house_type[blank:house_type.find("室")]
                        blank=house_type.find("室")+3
                    else:
                        self.fd["house_room"]=""
                    if house_type.find("厅")!=-1:
                        self.fd["house_hall"]=house_type[blank:house_type.find("厅")]
                        blank=house_type.find("厅")+3
                    else:
                        self.fd["house_hall"]=""
                    if house_type.find("卫")!=-1:
                        self.fd["house_toilet"]=house_type[blank:house_type.find("卫")]
                    else:
                        self.fd["house_toilet"]=""
                    self.fd["house_floor"]=re.search(self.hf_r, page)!=None and re.search(self.hf_r, page).group(1) or ""
                    self.fd["house_topfloor"]=re.search(self.hf_r, page)!=None and re.search(self.hf_r, page).group(2) or ""
                    self.fd["house_age"]=re.search(self.ha_r, page)!=None and re.search(self.ha_r, page).group(1) or ""
                    self.fd["house_sup"]=re.search(self.hs_r, page)!=None and re.search(self.hs_r, page).group(1) or ""
                    self.fd["house_desc"]=re.search(self.hd_r, page)!=None and re.search(self.hd_r, page).group(1) or ""
                    self.fd["borough_name"]=re.search(self.nm_r, page)!=None and re.search(self.nm_r, page).group(1) or ""
                    
            for ddd in  self.fd.items():
                print ddd[0],ddd[1]
        
            print "="*60
    
def getDict(d):
    lc=LinkCrawl(d["citycode"],d["kind"])
    clinks=lc.runme()
    cc=ContentCrawl(clinks,d["citycode"],d["kind"])
    cc.extractDict()
if __name__=="__main__":
    lc=LinkCrawl("su","2")
    lc.runme()
    
    cc=ContentCrawl(["http://su.sofang.com/zufang-1021844.htm"],"su",1)
    cc.extractDict()
        
    