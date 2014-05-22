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

year = '2011'

class BaseCrawl(object):
    #房源类型 1 出售 2 出租 3 求购  4 求租
    house_flag = None
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
    isGood = True
    timePerContent = 0.5
    
    #测试采集
    isTest = False
    Lists = []
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
        except Exception,what:
            print traceback.format_exc() 
            return False
        else:
            
            return response

    def _initTemple(self):        
        self.infoT = {
                      'house_flag':self.param['house_flag'],#房源类型 1 出售 2 出租 3 求购  4 求租
                      'title':'',
                      'uptime':'',
                      'price':0,
                      'price_min':0,
                      'deposit':0,
                      'belong':0,
                      'room':0,
                      'hall':0,
                      'toilet':0,
                      'yt':0,
                      'area':0,
                      'area_min':0,
                      'house_type':0,
                      'fitment':0,
                      'floor':0,
                      'topfloor':0,
                      'toward':0,
                      'age':0,
                      'equ':0,
                      'borough_name':'',
                      'city':self.param['city'],                      
                      'region':0,
                      'section':0,
                      'address':'',
                      'owner_phone':'',
                      'owner_phone_pic':'',
                      'owner_name':'',
                      'house_desc':'',
                      'search':'',
                      'info':'',
                      'url':'',
                      'thumb':'',
                      'web_flag':2,
                      'house_src':0,
                      'pic_num':0,
                      'pics':'',
                      }
    def postTime(self,posttime):
        if not posttime:
            return
        b = time.mktime(time.strptime(posttime,"%Y-%m-%d %H:%M"))
        if b:             
            return int(b)
        else:
            return
                       
    def run(self):
        #print self.param
        self.pageNo = 1           
        while 1:
            if self.isStoped == True:
                break
            if self.pageNo:
                url = self.baseUrl(self.param['args'],self.pageNo)
                self.__getLinks(url)
                
    def baseUrl(self,args,pn):
        pn = (self.pageNo+1)*32            
        if self.param['house_flag'] == 1:
            baseUrl = 'http://sh.ganji.com/fang5/a1f%d/' % pn
        if self.param['house_flag'] == 2:
            baseUrl = 'http://sh.ganji.com/fang1/f%d/' % pn      
        if self.param['house_flag'] == 3:
            args['option'] = args['option'][:-1]
            baseUrl = 'http://sh.ganji.com/fang4/f%d/' % pn
        if self.param['house_flag'] == 4:
            baseUrl = 'http://sh.ganji.com/fang2/a1f%d/' % pn
       
        return baseUrl
    
            
    def __getLinks(self,url):
        h = urlparse(url)
        lHtml = self.__getResponse(url)
        print url
        if lHtml == False:return
        tds = SoupStrainer("a",{"class":"list_title"})
        main_tds = BeautifulSoup(lHtml, parseOnlyThese=tds)        
        
        __links = []
        
        for tr in main_tds:            
            url = tr['href']           
            url = "%s://%s%s" % (h[0],h[1],url)
            #print url
            if url not in __links:
                __links.append(url)
            #测试
            print tr.string
            if self.isTest:
                row = {}
                row['title'] = tr.string
                row['url'] = url
                self.Lists.append(row)
            del tr
            del url
        if self.isTest:
            return
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
                #print "gj:%s" % link
                self.__getContent(link)
            except Exception,what:
                print  traceback.format_exc() 
            else:   
                if self.isGood:
                    self.debug()       
                    self.queue.append(self.infoT)
                else:
                    self.isGood = True
                self.infoT = {}
                del link
                
        self.pageNo +=1      
        del main_tds
        del tds
        del lHtml
                
    def _initRe(self):        
        self.house_posttime_regex="<span class=\"pub_time\">(.*?)</span>" 
        self.house_title_regex="<h1>(.*)</h1>"  
        self.username_regex="<span class=\"Dname\">(.*?)</span>"
        
        self.page_info_regex = "<ul class=\"d_i\">(.*?)</ul>"
        
        
        self.house_desc_regex = "<p class=\"text\">(.*?)</p>"
        
        self.house_pics_regex = "(http://image.ganjistatic\d+.com/.*?.jpg)" 
        self.house_phone_regex = "(/tel/.*?\.png)"  
        
        
        self.page_main_regex = "<div id=\"main\">(.*?)<div id=\"links\">"
        
              
        self.house_floor_regex="第(\d+)层"
        self.house_topfloor_regex="总(\d+)层"       

        self.house_room_regex="(\d+|一|两|二|三|四|五|六|七|八|九|十|一居|二居|三居|四居|五居)室"
        self.house_hall_regex="(\d+|一|两|二|三|四|五|六|七|八|九|十)厅"
        self.house_toilet_regex="(\d+|一|两|二|三|四|五|六|七|八|九|十)卫"
               
               
        self.house_age_regex="(\d+)年"        
        self.house_equ_regex = "tmp = '(.*?)'"       
              
        self.house_toward_regex = "(东|南|西|北|南北|东西|东南|东北|西北)"
        self.house_fitment_regex = "(豪华装修|精装修|中等装修|简单装修|毛坯)"
        self.house_belong_regex = "(商品房|经济适用房|公房|用权)"
        self.house_type_regex = "(房屋类型|平房/四合院|普通住宅|公寓|商住楼|别墅|其他)"
        self.house_deposit_regex="(押一付三|面议|押一付一|押一付二|押二付一|押二付三|半年付不押|年付不押|押一付半年|押一付年|押一付年|押二付年|押三付年)"
        
        self.borough_name_regex = "小区:(.*?)</p>"
        self.house_addr_regex = "小区:.*?\((.*?)\)"
        self.house_region_regex = "区域:(.*?)</p>"
        self.house_section_regex = "小区地址：(.*?)</p>"
        
        
        self.house_area_regex = "(\d+)㎡" 
        self.house_area_min_regex = "(\d+)-\d+㎡" 
        
        if self.param['house_flag'] == 1 or self.param['house_flag'] == 3:
            u = "万"
        else:
            u = "元"
        self.house_price_regex = "(\d+\.?\d)%s" % u
        self.house_price_min_regex = "(\d+)-\d+%s" % u
    def __getContent(self,url): 
        #print url
        h = urlparse(url)
        self._initTemple()
        time.sleep(self.timePerContent)
        self.infoT['url'] = url
        sHtml = self.__getResponse(self.infoT['url'])
        #print sHtml
        if sHtml == False: return
        
        sHtml = re.sub("  |\xe3\x80\x80|　|\n|\r|\t|&nbsp;|联系我时，请说是在58同城上看到的，谢谢！|该小区租房约\d条","",sHtml) 
        
        self.infoT['owner_phone_pic'] = regx_data(self.house_phone_regex,sHtml,"",False)
        if not self.infoT['owner_phone_pic']:
            self.isGood =  False
            return 
        else:
            self.infoT['owner_phone_pic'] = "%s://%s%s" % (h[0],h[1],self.infoT['owner_phone_pic'])
        posttime= regx_data(self.house_posttime_regex,sHtml,"",False)
        self.infoT['uptime']  = "%s-%s" % (year,posttime)
        
        self.infoT['title'] = regx_data(self.house_title_regex,sHtml,"",False)
        self.infoT['title'] = re.sub("<span.*?span>","",self.infoT['title'])
        self.infoT['owner_name'] = regx_data(self.username_regex,sHtml,"个人",False)              
        print self.infoT['title']
        
        
        detail_img = regx_data("detail_img(.*?)</ul>",sHtml,"",False)
        if detail_img:            
            self.infoT['pics'] = regx_datas1(self.house_pics_regex,detail_img,"",False)     
            if self.infoT['pics']:
                self.infoT['pic_num'] = len(self.infoT['pics'])
                self.infoT['thumb'] = self.infoT['pics'][0]     
            
        info = regx_data(self.page_info_regex,sHtml,"",False)
        #self.infoT['equ'] = regx_data(self.house_equ_regex,info,"",False)
        
        info = re.sub("<a .*?>|</a>|<span.*?>|</span>|<i.*?>|</i>|查看交通地图|该小区二手房约\d+条|房贷计算器","",info)
       
        self.infoT['info'] = info.replace("li","p").replace(" ","")    
        self.infoT['house_desc'] = regx_data(self.house_desc_regex,sHtml,"",False,"<.*?>")
        self.infoT['search'] = "%s%s" % (re.sub('<li>|</li>','',info),self.infoT['house_desc'])
        self.extractInfoT()
        
        
        if (time.time() - int(self.postTime(self.infoT['uptime'])))>self.param['args']["timelimit"]:
            self.overTimeNum +=1
            
        if self.overTimeNum > 5:
            self.pageNo = 0
            self.isStoped = True
            self.overTimeNum = 0   
                    
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
        #房龄 99年
        self.infoT['age'] = regx_data(self.house_age_regex,sHtml,"",False)        
        #装修
        self.infoT['fitment'] = regx_data(self.house_fitment_regex,sHtml,"",False)        
        #朝向
        self.infoT['toward'] = regx_data(self.house_toward_regex,sHtml,"",False) 
        #类型
        self.infoT['house_type'] = regx_data(self.house_type_regex,sHtml,"",False)         
        #产权 
        self.infoT['belong'] = regx_data(self.house_belong_regex,sHtml,"",False)
        #押金 
        self.infoT['deposit'] = regx_data(self.house_deposit_regex,sHtml,"",False)

        #小区
        self.infoT['borough_name'] = regx_data(self.borough_name_regex,sHtml,"",False) 
        if self.infoT['borough_name']:
            self.infoT['borough_name'] = re.sub("\(.*?\)|-| ","",self.infoT['borough_name'])  
        #地址
        self.infoT['addr'] = regx_data(self.house_addr_regex,sHtml,"",False)        
        #区
        self.infoT['region'] = regx_data(self.house_region_regex,sHtml,"",False)  
        if self.infoT['region'] and self.infoT['region'].find("-") != -1:
            self.infoT["section"] = self.infoT['region'].split("-")[1]
            self.infoT["region"] = self.infoT['region'].split("-")[0]
        self.debug()
        #self.infoT['section'] = regx_data(self.house_section_regex,sHtml,"",False)
        if self.infoT['address'] == '':
            if self.infoT['section']:
                self.infoT['address'] = self.infoT['address']
            else:
                self.infoT['address'] = self.infoT['borough_name']
    def fetchContent(self):
        self.__getContent(self.param['url'])
    def fetchList(self):
        self.__getLinks(self.param['url'])
        
    def debug(self):
        if 1:
            for i in self.infoT:
                print i,self.infoT[i]
q = []
if __name__=="__main__":
    
    url1 = 'http://sh.ganji.com/fang5/11120800_1324402.htm'
    url2 = 'http://sh.ganji.com/fang1/11122512_5282580.htm'
    url3 = "http://sh.ganji.com/fang4/11102411_221100.htm"
    url4 = "http://sh.ganji.com/fang2/11102423_434670.htm"
    link2 = "http://sh.ganji.com/fang1/minhang/h1p1f32/"
    link1 = "http://sh.ganji.com/fang5/a1/"
    link4 = "http://sh.ganji.com/fang2/f32/"
    link3 = "http://sh.ganji.com/fang4/a1/"
    data = {}
    data['house_flag'] = 2
    data['city'] = 1
    data['url'] = url2
    data['getPhone'] = 1
    data['name'] = "ganji"
    data['args'] = {
                    "timelimit":86400,"city":"1","region":"","option":"","q":""
                    }
    
    cc = BaseCrawl(data,q)
    #cc.run()
    cc.fetchContent()
    cc.debug()
    #cc.isTest =True
    #cc.fetchList()
    #print cc.Lists
    #cc.run()

