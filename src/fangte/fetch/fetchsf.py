# -*- coding: utf-8 -*-
import time
import datetime
import random
import cookielib
import urllib
import urllib2
from urlparse import urlparse
from config import *
from common import *
from BeautifulSoup import BeautifulSoup, SoupStrainer
import traceback
class BaseCrawl(object):
    #房源类型 1 出售 2 出租 3 求购  4 求租
    flag = None
    isStoped = False
    response = None
    header = None
    #房源信息模板
    infoT = {}
    #传入参数
    param = {}
    #全局队列
    queue = []
    pageNo = 0
    isFetched = False
    #超过时间的条数
    overTimeNum = 0
    #每次抓取内容页间隔
    timePerContent = 0.5
    isGood = True
    def __init__(self,param,que):
        self.queue = que
        self.param = param       
        self.header = header
        cj = cookielib.MozillaCookieJar()
        self.br=urllib2.build_opener(urllib2.HTTPHandler(),urllib2.HTTPCookieProcessor(cj),urllib2.HTTPRedirectHandler())
        self._initRe()
        
    def __getResponse(self,url):
        try:
            request = urllib2.Request(url, None, self.header)            
            response = urllib2.urlopen(request).read()   
            response = response.decode("gbk")#.encode("utf-8")         
        except Exception,what: 
            print traceback.format_exc() 
            return False
        else:
            
            return response

    def _initTemple(self):        
        self.infoT = {
                      'flag':self.param['flag'],#房源类型 1 出售 2 出租 3 求购  4 求租
                      'title':'',
                      'posttime':'',
                      'price':0,
                      'price_min':0,
                      'deposit':'',
                      'belong':'',
                      'room':0,
                      'hall':0,
                      'toilet':0,
                      'yt':0,
                      'area':0,
                      'area_min':0,
                      'houseType':'',
                      'fitment':'',
                      'floor':0,
                      'topfloor':0,
                      'toward':'',
                      'age':0,
                      'equ':'',
                      'city':self.param['city'],
                      'region':'',
                      'borough':'',
                      'section':'',
                      'addr':'',
                      'phone':'',
                      'phone_pic':'',
                      'owner':'',
                      'desc':'',
                      'search':'',
                      'info':'',
                      'url':'',
                      'thumb':'',
                      'webFlag':4,
                      'isPerson':1,
                      'picNum':0,
                      'followNum':0,
                      'collected':0
                      }
    def postTime(self,posttime):
        if not posttime:
            return
        
        posttime = posttime.replace('月','-').replace('日',' ')
        b = time.mktime(time.strptime(posttime,"%Y-%m-%d"))
        if b:      
            return int(b)
        else:
            return
                       
    def run(self):
        self.pageNo = 1           
        while 1:
            if self.isStoped == True:
                break
            if self.pageNo:
                url = self.baseUrl(self.param['args'],self.pageNo)
                self.__getLinks(url)
    def baseUrl(self,args,pn):
        pn = self.pageNo + 30
        if self.param['flag'] == 1:
            baseUrl = 'http://zu.sh.soufun.com/house/a21-i%d/' % pn
        if self.param['flag'] == 2:
            baseUrl = 'http://esf.sh.soufun.com/house/a21-i%d/' % pn    
        if self.param['flag'] == 3:
            pass
        if self.param['flag'] == 4:
            baseUrl = 'http://zu.sh.soufun.com/qiuzu/h316-i%d/' % pn
       
        return baseUrl
    
            
    def __getLinks(self,url):
        lHtml = self.__getResponse(url)
        h= urlparse(url)
       
        if lHtml == False:return
        
        if self.param['flag'] ==2:
            tds = SoupStrainer("div",{"class":"house"})
        elif self.param['flag'] ==4 :   
            tds = SoupStrainer("span",{"class":"li2"})
        elif self.param['flag'] ==1 : 
            tds = SoupStrainer("div",{"class":"house"})
        else:
            return
        
        
        main_tds = BeautifulSoup(lHtml, parseOnlyThese=tds)        
        __links = []
        for tr in main_tds:  
            url = tr.a['href']
            url = "%s://%s%s" % (h[0],h[1],url)
            if url not in __links:
                __links.append(url)
            del tr
            del url
        if not __links:
            self.pageNo = 0            
            return
          
        for link in __links:
            time.sleep(self.timePerContent)
            
            if self.isStoped == True:
                break
            #已抓 取
            if  checkPath("pagecash",link):
                continue
            try:
                self.__getContent(link)
            except Exception,what:
                print traceback.format_exc() 
                print what
            else:   
                if self.isGood:             
                    self.queue.append(self.infoT)
                    self.debug()
                else:
                    self.isGood = True
                self.infoT = {}
                del link
        self.pageNo +=1      
        del main_tds
        del tds
        del lHtml
                
    def _initRe(self):        
        self.house_posttime_regex="(\d{4}-\d+-\d+)" 
        self.house_title_regex=u"<h1>(.*)</h1>"  
        self.username_regex=u"联 系 人：(.*?)<"
        
        self.page_info_regex = "class=\"info\">(.*?)<div class=\"lcolumn"
        
        
        self.house_desc_regex = "class=\"beizhu\">(.*?)</div>"
        if self.param['flag'] ==1:
            self.house_pics_regex = "'bigpic':'(.*?)'" 
        else:
            self.house_pics_regex = "(http://img\d+.soufunimg.com/rent/.*?.jpg)"
        
        self.house_phone_pic_regex = "(http://img\d+.soufun.com/showphone/.*?.gif)"  
        
        
        self.page_main_regex = "<div id=\"main\">(.*?)<div id=\"links\">"
        
              
        self.house_floor_regex=u"第(\d+)层"
        self.house_topfloor_regex=u"共(\d+)层"       

        self.house_room_regex   = u"(\d+|一|两|二|三|四|五|六|七|八|九|十|一居|二居|三居|四居|五居)室"
        self.house_hall_regex   = u"(\d+|一|两|二|三|四|五|六|七|八|九|十)厅"
        self.house_toilet_regex = u"(\d+|一|两|二|三|四|五|六|七|八|九|十)卫"
        self.house_yt_regex     = u"(\d+|一|两|二|三|四|五|六|七|八|九|十)阳台"
               
               
        self.house_age_regex=u"(\d+)年"        
        self.house_equ_regex = u"房屋配套：(.*?)<"       
              
        self.house_toward_regex  = u"(东|南|西|北|南北|东西|东南|东北|西北)"
        self.house_fitment_regex = u"(豪华装修|精装修|中等装修|简单装修|毛坯)"
        self.house_belong_regex  = u"(商品房|经济适用房|公房|用权)"
        self.house_type_regex    = u"(房屋类型|平房/四合院|普通住宅|公寓|商住楼|别墅|其他)"
        self.house_deposit_regex = u"(押一付三|面议|押一付一|押一付二|押二付一|押二付三|半年付不押|年付不押|押一付半年|押一付年|押一付年|押二付年|押三付年)"
        
        self.borough_name_regex = u"楼盘名称：<br/>(.*?)<"
        self.house_addr_regex = u"址：(.*?)<"
        self.house_region_regex = "\(.*?\)</p>"
        self.house_section_regex = u"址：(.*?)<"
        
        
        self.house_area_regex = u"(\d+)平" 
        self.house_area_min_regex = u"(\d+)-\d+平" 
        
        if self.param['flag'] ==4:   
            self.house_phone_regex = u"联系电话:<.*?>(\d+)</" 
            self.house_desc_regex = u"class=\"qzbeizhu\">\s+<p>(.*?)</p" 
        elif self.param['flag'] ==3:   
            self.house_desc_regex = u"class=\"beizhu mt10\">(.*?)</p" 
            self.house_phone_regex = u"联系电话:<.*?>(\d+)</"  
            self.borough_name_regex = u"楼盘名称：<br/>(.*?)<"
            
            self.house_addr_regex = u"求购区域：(.*?)<"
            self.house_region_regex = u"求购区域:(.*?)<"
            self.house_section_regex = u"求购区域:(.*?)<"
        else:
            self.house_phone_regex = u"联系电话:<.*?>(\d+)</" 
            
            
        if self.param['flag'] == 1 or self.param['flag'] == 3:
            u = u"万"
        else:
            u = u"元"
        self.house_price_regex = "(\d+\.?\d)%s" % u
        self.house_price_min_regex = "(\d+)-\d+%s" % u
    def __getContent(self,url): 
        self._initTemple()
        time.sleep(self.timePerContent)
        self.infoT['url'] = url
        sHtml = self.__getResponse(self.infoT['url'])
        
        if sHtml == False: return
        sHtml = re.sub("\n|\r|\t|&nbsp;","",sHtml) 
        #print sHtml
        self.infoT['phone'] = regx_data(self.house_phone_regex,sHtml,"",False)  
        self.infoT['phone_pic'] = regx_data(self.house_phone_pic_regex,sHtml,"",False)  
        
        self.infoT['posttime'] = self.postTime(regx_data(self.house_posttime_regex,sHtml,"",False))
        
        
        self.infoT['title'] = re.sub(u"_上海二手房_搜房网|_上海租房网","",self.infoT['title'])
        self.infoT['pics'] = regx_datas(self.house_pics_regex,sHtml,"",False)     
        if self.infoT['pics'] and self.infoT['pics'].find("|") !=-1:
            self.infoT['picNum'] = len(self.infoT['pics'].split("|"))
        self.infoT['owner'] = regx_data(self.username_regex,sHtml,"个人",False)
        
        info = regx_data(self.page_info_regex,sHtml,"",False)
        
        if not self.infoT['owner']:
            self.isGood =  False
            return
        
        info = re.sub(u"<p.*?p>|<a.*?>|</a>|<span.*?>|</span>|<img.*?>|class=\".*?\"|style=\".*?\"|id=\".*?\"| |我要估价|房贷计算器|联系时您可以说：“您好，我从搜房网看到...”|随时随地找房子就在搜房手机客户端|发送房源到手机|　　","",info)
        info = re.sub(u"查看本价位的出售房源|楼盘详情论坛|举报为中介|如发现为中介房源，请马上举报：举报为中介|楼盘信息纠错|<div>|</div>|<dd></dd>|<dt></dt>|<dt></dt>","",info)
        
        self.infoT['title'] = regx_data(self.house_title_regex,info,"",False)        
        info = re.sub("<h1>.*?</h1>|","",info)        
        info = re.sub("<input.*?>","",info)
        info = re.sub("<iframe.*?iframe>","",info)
        info = re.sub("<script.*?script>","",info)
        info = re.sub("<Popup.*?Popup>","",info)
        info = re.sub("<table.*?table>","",info)
        info = re.sub("</td></tr></table>","",info)
        #联系时您可以说：“您好，我从搜房租房网看到...”
        info = re.sub(u"联系时您可以说：“您好，我从搜房租房网看到...”","",info)
        info = re.sub("<.*?>","<br />",info)
        info = re.sub("<br /><br />","<br />",info)
        info = re.sub("<br /><br />","<br />",info)
        info = re.sub("<br /><br />","<br />",info)
        info = re.sub(u"[地图]","",info)
        
        
        self.infoT['equ'] = regx_data(self.house_equ_regex,info,"",False)
        self.infoT['info'] = info   
        self.infoT['desc'] = regx_data(self.house_desc_regex,sHtml,"",False,"<.*?>").strip()
        self.infoT['search'] = re.sub('<.*?>| ','',("%s%s" % (info,self.infoT['desc'])))
        #print self.infoT['search']
        self.extractInfoT()
        
        
        if (time.time() - int(self.infoT['posttime']))>self.param['args']["timelimit"]:
            self.overTimeNum +=1
            
        if self.overTimeNum > 5:
            self.pageNo = 0
            self.isStoped = True
            self.overTimeNum = 0  
        del sHtml
                    
    def extractInfoT(self):
        sHtml = self.infoT['info'].replace(" ","")
        
        #价格
        self.infoT['price'] = regx_data(self.house_price_regex,sHtml,0,False)
        self.infoT['price_min'] = regx_data(self.house_price_min_regex,sHtml,0,False)        
        
        #面积
        self.infoT['area'] = regx_data(self.house_area_regex,sHtml,0,False)        
        self.infoT['area_min'] = regx_data(self.house_area_min_regex,sHtml,0,False)       
        
        #楼层
        self.infoT['floor'] = regx_data(self.house_floor_regex,sHtml,0,False)        
        #顶层
        self.infoT['topfloor']= regx_data(self.house_topfloor_regex,sHtml,0,False)               
                
        #室
        self.infoT['room'] = regx_data(self.house_room_regex,sHtml,"",False)        
        #厅
        self.infoT['hall'] = regx_data(self.house_hall_regex,sHtml,"",False)        
        #卫
        self.infoT['toilet'] = regx_data(self.house_toilet_regex,sHtml,"",False) 
        #阳台
        self.infoT['yt'] = regx_data(self.house_yt_regex,sHtml,"",False)        
        #房龄 99年
        self.infoT['age'] = regx_data(self.house_age_regex,sHtml,"",False)        
        #装修
        self.infoT['fitment'] = regx_data(self.house_fitment_regex,sHtml,"",False)        
        #朝向
        self.infoT['toward'] = regx_data(self.house_toward_regex,sHtml,"",False) 
        #类型
        self.infoT['houseType'] = regx_data(self.house_type_regex,sHtml,"",False)         
        #产权 
        self.infoT['belong'] = regx_data(self.house_belong_regex,sHtml,"",False)
        #押金 
        self.infoT['deposit'] = regx_data(self.house_deposit_regex,sHtml,"",False)

        #小区
        self.infoT['borough'] = regx_data(self.borough_name_regex,sHtml,"",False) 
        if self.infoT['borough']:
            self.infoT['borough'] = re.sub("\(.*?\)|-| ","",self.infoT['borough'])  
        #地址
        #print sHtml
        self.infoT['addr'] = regx_data(self.house_addr_regex,sHtml,"",False)        
        #区
        self.infoT['region'] = regx_data(self.house_region_regex,sHtml,"",False)  
        self.infoT['section'] = regx_data(self.house_section_regex,sHtml,"",False)
        del sHtml
        
            
    def debug(self):
        if 0:
            for i in self.infoT:
                print i,self.infoT[i]
q = []
if __name__=="__main__":
    url1 = 'http://esf.sh.soufun.com/chushou/1_119973131_-1.htm'
    url2 = 'http://zu.sh.soufun.com/chuzu/1_50246761_-1.htm'
    url3 = "http://esf.sh.soufun.com/qiugou/1_868775_-1.htm"
    url4 = "http://zu.sh.soufun.com/qiuzu/1_55127557_-1.htm"
    link2 = "http://zu.sh.soufun.com/house/a21/"
    link4 = "http://zu.sh.soufun.com/qiuzu/h316/"
    link1 = "http://esf.sh.soufun.com/house/a21/"
    
    data = {}
    data['flag'] = 4
    data['city'] = 1
    data['getPhone'] = 1
    data['name'] = "111"
    data['args'] = {
                    "timelimit":86400,"city":"sh","region":"","option":"","q":""
                    }
    
    cc = BaseCrawl(data,q)
    cc.run()


