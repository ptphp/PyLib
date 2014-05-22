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
    isGood = 1
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
                      'webFlag':1,
                      'isPerson':1,
                      'picNum':0,
                      'followNum':0,
                      'collected':0
                      }
    def postTime(self,posttime):
        posttime = posttime.strip()
        if posttime and posttime.find('now') != -1:
                posttime = int(time.time())
        if not posttime:
            return
        
        posttime = str(posttime).replace('前','')
        #print posttime
        if posttime.find("<") != -1 or posttime.find(">") != -1:
            posttime = re.sub('<.*?>','' ,posttime)                
        if posttime.find('-') !=-1:            
            if len(posttime.split("-"))==3:                
                s = datetime.datetime(int(posttime.split('-')[0]),int(posttime.split('-')[1],),int(posttime.split('-')[2]))
            else:
                s = datetime.datetime(2011,int(posttime.split('-')[0],),int(posttime.split('-')[1]))
            posttime = int(time.mktime(s.timetuple()))
        elif posttime.find('分钟') !=-1:
            n = int(posttime.replace('分钟',''))*60
            posttime = int(time.time() - n)
        elif posttime.find('小时') !=-1:
            n = int(posttime.replace('小时',''))*60*60
            posttime = int(time.time() - n)
        else:
            posttime = int(time.time())
        return posttime
                       
    def run(self):
        self.pageNo = 1           
        while 1:
            if self.isStoped == True:
                break
            if self.pageNo:
                url = self.baseUrl(self.param['args'],self.pageNo)
                #print url
                self.__getLinks(url)
    def baseUrl(self,args,pn):
        if args['region'] != '':
            args['region'] = args['region']+"/"
        else:
            args['region'] = ''            
        if args['option']!= '':
            args['option'] = args['option']+"/"
        else:
            args['option'] = ''
            
        if self.param['flag'] == 1:
            baseUrl = 'http://%s.58.com/%sershoufang/0/%spn%d/?final=1&searchtype=3&sourcetype=5&key=%s' % (args['city'],args['region'],args['option'],pn,args['q'])       
        if self.param['flag'] == 2:
            baseUrl = 'http://%s.58.com/%szufang/0/%spn%d/?final=1&key=%s' % (args['city'],args['region'],args['option'],pn,args['q']);      
        if self.param['flag'] == 3:
            args['option'] = args['option'][:-1]
            baseUrl = 'http://%s.58.com/%sershoufang/0/%sh2/pn%d/?final=1&key=%s&searchtype=3&sourcetype=5' % (args['city'],args['region'],args['option'],pn,args['q'])     
            
        if self.param['flag'] == 4:
            baseUrl = 'http://%s.58.com/%sqiuzu/0/%spn%d/?final=1&key=%s' % (args['city'],args['region'],args['option'],pn,args['q'])
       
        return baseUrl
    def __getContent(self,url): 
        self._initTemple()
        time.sleep(self.timePerContent)
        self.infoT['url'] = url
        sHtml = self.__getResponse(self.infoT['url'])
        
        if sHtml == False: return
        sHtml = re.sub("  |\xe3\x80\x80|　|\n|\r|\t|&nbsp;|联系我时，请说是在58同城上看到的，谢谢！","",sHtml) 
        
        self.infoT['title'] = regx_data(self.house_title_regex,sHtml,"",False)
        self.infoT['posttime'] = self.postTime(regx_data(self.house_posttime_regex,sHtml,"",False))
        self.infoT['owner'] = regx_data(self.username_regex,sHtml,"个人",False)
        self.infoT['phone_pic'] = regx_data(self.house_phone_regex,sHtml,"",False)        
        
        self.infoT['pics'] = regx_datas(self.house_pics_regex,sHtml,"",False ,"tiny","big")     
        
        if self.infoT['pics'] and self.infoT['pics'].find("|") !=-1:
            self.infoT['picNum'] = len(self.infoT['pics'].split("|"))
        
        info = regx_data(self.page_info_regex,sHtml,"",False)
        self.infoT['equ'] = regx_data(self.house_equ_regex,info,"",False)
        
        info = re.sub("<script.*?script>|<em.*?>|</em>|<a .*?>|</a>|<span.*?>|</span>|<i.*?>|</i>|查看交通地图|二手房信息\d+条|房贷计算器|\(|\)","",info) 
        
        self.infoT['info'] = "%s <p>%s</p>" % (info.replace("li","p"),self.infoT['equ'])        
        self.infoT['desc'] = regx_data(self.house_desc_regex,sHtml,"",False,"<.*?>")        
        self.infoT['search'] = "%s%s%s" % (re.sub('<li>|</li>','',info),self.infoT['equ'],self.infoT['desc'])
        self.extractInfoT()
        if (time.time() - int(self.infoT['posttime']))>self.param['args']["timelimit"]:
            self.overTimeNum +=1
            
        if self.overTimeNum > 5:
            self.pageNo = 0
            self.isStoped = True
            self.overTimeNum = 0
            
    def __getLinks(self,url):
        lHtml = self.__getResponse(url)
        
        if lHtml == False:return
        
        tds = SoupStrainer("td",{"class":"t"})
        main_tds = BeautifulSoup(lHtml, parseOnlyThese=tds)        
        
        __links = []
        for tr in main_tds:
            if str(tr).find("个人") != -1:
                url = tr.a['href']
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
                print what
            else:
                if self.isGood:
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
        self.page_info_regex = "<ul class=\"info\">(.*?)</ul>"
        self.page_main_regex = "<div id=\"main\">(.*?)<div id=\"links\">"
        self.username_regex="username:'(.*?)',"
        self.house_title_regex="<h1>(.*)</h1>"        
        self.house_floor_regex="第(\d+)层"
        self.house_topfloor_regex="共(\d+)层"       

        self.house_room_regex="(\d+|一|两|二|三|四|五|六|七|八|九|十|一居|二居|三居|四居|五居)室"
        self.house_hall_regex="(\d+|一|两|二|三|四|五|六|七|八|九|十)厅"
        self.house_toilet_regex="(\d+|一|两|二|三|四|五|六|七|八|九|十)卫"
        self.house_posttime_regex="发布时间：(.*?)浏览"        
               
        self.house_age_regex="(\d+)年"        
        self.house_equ_regex = "tmp = '(.*?)'"               
            
        self.house_desc_regex = "class=\"maincon\">(.*?)</div>"        
        self.house_phone_regex = "(http://image.58.com/showphone.aspx.*?)'"        
        self.house_pics_regex = "(http://\d+.pic.58control.cn/p\d+/tiny/n_\d+.jpg)"        
              
        self.house_toward_regex = "(东|南|西|北|南北|东西|东南|东北|西北)"
        self.house_fitment_regex = "(毛坯|简单装修|中等装修|精装修|豪华装修)"
        self.house_belong_regex = "(商品房|经济适用房|公房|用权)"
        self.house_type_regex = "(平房|普通住宅|商住两用|公寓|别墅)"
        self.house_deposit_regex="(押一付三|押一付一|押二付一|半年付|年付)"
        
        self.borough_name_regex = "小区：(.*?)</p>"
        self.house_addr_regex = "地址：(.*?)</p>"
        self.house_region_regex = "区域：(.*?)</p>"
        self.house_section_regex = "地段：(.*?)</p>"
        
        
        self.house_area_regex = "(\d+)㎡" 
        self.house_area_min_regex = "(\d+)-\d+㎡" 
        
        
        if self.param['flag'] == 1 or self.param['flag'] == 3:
            u = "万"
        else:
            u = ""
        self.house_price_regex = "(\d+)%s元" % u
        self.house_price_min_regex = "(\d+)-\d+%s元" % u
        
                    
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
        #地址
        self.infoT['addr'] = regx_data(self.house_addr_regex,sHtml,"",False)        
        #区
        self.infoT['region'] = regx_data(self.house_region_regex,sHtml,"",False)  
        self.infoT['section'] = regx_data(self.house_section_regex,sHtml,"",False)
        if self.infoT['addr'] == '':
            self.infoT['addr'] = self.infoT['section']
            
    def start(self,url):
        self.__getContent(url)
q = []
if __name__=="__main__":
    url1 = 'http://sh.58.com/ershoufang/7054791740677x.shtml'
    url2 = 'http://sh.58.com/zufang/7468246420482x.shtml'
    url3 = 'http://sh.58.com/ershoufang/7607481469826x.shtml'
    url4 = 'http://sh.58.com/qiuzu/7543125341446x.shtml'
    link2 = 'http://sh.58.com/zufang/0/?selpic=2'
    link1 = 'http://sh.58.com/ershoufang/0/'
    link3 = 'http://sh.58.com/ershoufang/h2/'
    link4 = 'http://sh.58.com/qiuzu/0/'    
    data = {}
    data['flag'] = 4
    data['city'] = 1
    data['getPhone'] = 1
    cc = BaseCrawl(data,q)
    cc.start(url4)

