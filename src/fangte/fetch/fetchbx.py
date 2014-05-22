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
import base64
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
    isGood = True
    timePerContent = 0.5
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
                      'webFlag':3,
                      'isPerson':1,
                      'picNum':0,
                      'followNum':0,
                      'collected':0
                      }
    def postTime(self,posttime):
        if not posttime:
            return
        posttime = "2011-%s" % posttime
        posttime = posttime.replace('月','-').replace('日',' ')
        b = time.mktime(time.strptime(posttime,"%Y-%m-%d %H:%M"))
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
           
        if self.param['flag'] == 1:
            baseUrl = 'http://shanghai.baixing.com/ershoufang/?page=%d&发布人=个人' % self.pageNo       
        if self.param['flag'] == 2:
            baseUrl = 'http://shanghai.baixing.com/zhengzu/?page=%d&发布人=个人' % self.pageNo    
        if self.param['flag'] == 3:
            pass
        if self.param['flag'] == 4:
            pass
        return baseUrl
    
            
    def __getLinks(self,url):
        lHtml = self.__getResponse(url)
        h = urlparse(url)
        if lHtml == False:return
        tds = SoupStrainer("td",{"class":"title"})
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
        self.house_posttime_regex="发布时间：(.*?)</li>" 
        self.house_title_regex="<h1>(.*)</h1>"  
        self.username_regex="(个人)"
        
        self.page_info_regex = "<article>(.*?)</article>"
        
        
        self.house_desc_regex = ""
        
        self.house_pics_regex = "(http://img\d+.baixing.net/m/.*?.jpg)" 
        self.house_phone_regex = "(http://static.baixing.net/pages/mobile.php.*?.jpg)"  
        
        
        self.page_main_regex = "<div id=\"main\">(.*?)<div id=\"links\">"
        
              
        self.house_floor_regex="(\d+)/\d+层"
        self.house_topfloor_regex="(\d+)层"       

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
        
        
        self.house_area_regex = "(\d+)平米" 
        self.house_area_min_regex = "(\d+)-\d+平米" 
        
        
        if self.param['flag'] == 1 or self.param['flag'] == 3:
            u = "万"
        else:
            u = "元"
        self.house_price_regex = "(\d+\.?\d)%s" % u
        self.house_price_min_regex = "(\d+)-\d+%s" % u
    def __getContent(self,url): 
        self._initTemple()
        time.sleep(self.timePerContent)
        self.infoT['url'] = url
        sHtml = self.__getResponse(self.infoT['url'])
        
        if sHtml == False: return
        sHtml = re.sub("  |\xe3\x80\x80|　|\n|\r|\t|&nbsp;|联系我时，请说是在58同城上看到的，谢谢！|该小区租房约\d条","",sHtml) 
        self.infoT['phone_pic'] = regx_data(self.house_phone_regex,sHtml,"",False)  
        if not self.infoT['phone_pic']:
            self.isGood =  False
            return 
        self.infoT['posttime'] = self.postTime(regx_data(self.house_posttime_regex,sHtml,"",False))
        
        self.infoT['title'] = regx_data(self.house_title_regex,sHtml,"",False)
        self.infoT['title'] = re.sub("<span.*?span>","",self.infoT['title'])
              
        
        self.infoT['pics'] = regx_datas(self.house_pics_regex,sHtml,"",False)
        if self.infoT['pics']:
            self.infoT['pics'] = self.infoT['pics'][:-1].replace("_sm","")
            self.encodePics();           
        if self.infoT['pics'] and self.infoT['pics'].find("|") !=-1:
            self.infoT['picNum'] = len(self.infoT['pics'].split("|"))
        
        info = regx_data(self.page_info_regex,sHtml,"",False)
        
        self.infoT['owner'] = regx_data(self.username_regex,info,"个人",False)
        if not self.infoT['owner']:
            self.isGood =  False
            return
        #self.infoT['equ'] = regx_data(self.house_equ_regex,info,"",False)
        
        info = re.sub("<strong>|</strong>|<a .*?>|</a>|<span.*?>|\.\.\.|</span>|<label.*?>|</label>|次查看| id=\".*?\"| class=\"blank10\"","",info)
        #print info
        self.infoT['info'] = info.replace("<div></div>","<br>")   
        #self.infoT['desc'] = 'regx_data(self.house_desc_regex,sHtml,"",False,"<.*?>")  '      
        self.infoT['search'] = re.sub('<.*?>','',info)
        self.extractInfoT()
        return
        
        if (time.time() - int(self.infoT['posttime']))>self.param['args']["timelimit"]:
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
        self.infoT['addr'] = regx_data(self.house_addr_regex,sHtml,"",False)        
        #区
        self.infoT['region'] = regx_data(self.house_region_regex,sHtml,"",False)  
        self.infoT['section'] = regx_data(self.house_section_regex,sHtml,"",False)
        if self.infoT['addr'] == '':
            if self.infoT['section']:
                self.infoT['addr'] = self.infoT['section']
            else:
                self.infoT['addr'] = self.infoT['borough']
                
        if 0:
            for row in self.infoT:
                print row,self.infoT[row]
    def encodePics(self):
        tmp = self.infoT['pics'].split("|")
        res = ""
        for i in tmp:
            r = self.__getResponse(i)
            time.sleep(0.1)
            code = base64en(r)
            b64code = "data:image/gif;base64,%s" % code
            res += b64code+"|"
        self.infoT['pics'] =  res[:-1]
        del tmp
        del res

    def debug(self):
        if 0:
            for i in self.infoT:
                print i,self.infoT[i]
q = []
if __name__=="__main__":
    url1 = 'http://shanghai.baixing.com/ershoufang/a134467983.html'
    url2 = 'http://shanghai.baixing.com/zhengzu/a125191478.html'
    url3 = "http://sh.ganji.com/fang4/11102411_221100.htm"
    url4 = "http://sh.ganji.com/fang2/11102423_434670.htm"
    link2 = "http://shanghai.baixing.com/zhengzu/?page=2&%E5%8F%91%E5%B8%83%E4%BA%BA=%E4%B8%AA%E4%BA%BA"
    link1 = "http://shanghai.baixing.com/ershoufang/?%E5%8F%91%E5%B8%83%E4%BA%BA=%E4%B8%AA%E4%BA%BA"
    data = {}
    data['flag'] = 2
    data['city'] = 1
    data['getPhone'] = 1
    data['name'] = "111"
    data['args'] = {
                    "timelimit":86400,"city":"sh","region":"","option":"","q":""
                    }
    
    cc = BaseCrawl(data,q)
    cc.run()

