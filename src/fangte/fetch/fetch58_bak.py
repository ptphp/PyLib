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
from BeautifulSoup import BeautifulSoup

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
    def __init__(self,param,que):
        self.queue = que
        self.param = param       
        self.header = header
        cj = cookielib.MozillaCookieJar()
        self.br=urllib2.build_opener(urllib2.HTTPHandler(),urllib2.HTTPCookieProcessor(cj),urllib2.HTTPRedirectHandler())
        self.endtime=str(datetime.date.today() -datetime.timedelta(days=7)) 
                
        self._initRe()
    def getContent(self):
        
        if self.__cInit__(self.infoT['url']) :
            
            self.response = re.sub(" |\n|\r|\t|　|&nbsp;|联系我时，请说是在58同城上看到的，谢谢！","",self.response) 
            self.response = re.sub("rlist\d\">.*?</ul>","",self.response)
            try:
                if self.param['flag'] == 1:
                    self.sell();               
                if self.param['flag'] == 2:
                    self.rent(); 
                if self.param['flag'] == 3:
                    self.buy(); 
                if self.param['flag'] == 4:
                    self.req();
            except Exception,what:
                print what            
                
        if (time.time() - int(self.infoT['posttime']))>self.param['args']["timelimit"]:
            self.overTimeNum +=1
            
        if self.overTimeNum > 5:
            self.pageNo = 0
            self.isStoped = True
            self.overTimeNum = 0
                
    def getPhoneself(self):
        if self.__cInit__(self.infoT['url']) :       
            sHtml = self.response
            self.infoT['phone'] = regx_data(self.house_phone_regex,sHtml,"",False)
         
              
    def __getLinks(self,url):
        if not self.__cInit__(url):
            return        
        self.response = re.sub("\n|\r|\t|　|&nbsp;","",self.response) 
        page_main = regx_data(self.page_main_regex,self.response,"",0)
        self.page_main_trs_regex = "<tr logr=\".*?\">(.*?)</tr>"
        page_main_trs = regx_lists(self.page_main_trs_regex,page_main,"",0)
        if page_main_trs and len(page_main_trs)>0:
            for tr in page_main_trs:
                if self.isStoped:
                    self.pageNo = 0
                    break
                self._initTemple(self.param['flag'],self.param['city'])
                try:
                    if self.param['flag'] == 1:
                        self.__parseSellTrs(tr)               
                    if self.param['flag'] == 2:
                        self.__parseRentTrs(tr)
                    if self.param['flag'] == 3:
                        self.__parseBuyTrs(tr)
                    if self.param['flag'] == 4:
                        self.__parseReqTrs(tr)    
                except Exception,what:
                    print what
                else: 
                    if not self.isFetched:           
                        self.queue.append(self.infoT)
                        self.isFetched = False
                time.sleep(0.1)
                self.infoT = {}
            self.pageNo +=1
        else:
            self.pageNo = 0

    def __parseBuyTrs(self,tr):
        soup = BeautifulSoup(tr)        
        at = soup.find('a',{'class':'t'})
        #标题
        if at:
            self.infoT['title'] = at.string            
            #链接        
            self.infoT['url'] = at['href']
            if  checkPath("pagecash",self.infoT['url']):
                self.isFetched = True                
                return
        
        else:            
            return

        #图片
        img = soup.find('td',{'class':'img'})
        if img:
            if img.img['src'].find("noimg") == -1:
                self.infoT['thumb'] = img.img['src']
                
        #信息
        t = soup.find('td',{'class':'t'})

        self.infoT['belong'] = regx_data(self.house_belong_dict_regex,str(t),"",False) 
        self.infoT['houseType'] = regx_data(self.house_type_regex,str(t),"",False)
        self.infoT['posttime'] = self.postTime(regx_data("更新时间：(.*?)<",str(t),"",False))
       
        #self.infoT['room'] = regx_data(self.house_room_regex,str(soup),"",False) 
        #if self.infoT['room']:
            #self.infoT['room'] = re.sub("一|二|三|四|五|六|七|八|九|十","1|2|3|4|5|6|7|8|9|10",self.infoT['room'])
        self.infoT['hall'] = regx_data(self.house_hall_regex,str(soup),"",False) 
        self.infoT['toilet'] = regx_data(self.house_toilet_regex,str(soup),"",False) 
        
        agencyname = regx_data("(个人)",str(t),"",False) 
        if agencyname:
            self.infoT['isPerson'] = 1
        else:
            self.infoT['isPerson'] = 0
        
        #价格
        num = soup('td',{'class':'tc'})
        if num and len(num) > 1:  
            if str(num[0]).find("面议") == -1:
                price  = num[0].b.string  
                if price.find('-') == -1:
                    self.infoT['price'] = price
                else:
                    self.infoT['price'] = price.split("-")[0]
                    self.infoT['price_max'] = price.split("-")[1]
                del price  
            area = num[1].b.string      
            if area.find('-') == -1:
                self.infoT['area'] = area
            else:
                self.infoT['area'] = area.split("-")[0]
                self.infoT['area_max'] = area.split("-")[1]
            del area
            
        self.infoT['search']= re.sub("<.*?>","",str(soup))
        del soup
        del t
        del img
        del at
        del num
        del agencyname
        self.getContent()
        
    def __parseReqTrs(self,tr):
        soup = BeautifulSoup(tr)
        at = soup.find('a',{'class':'t'})
        #标题
        if at:
            self.infoT['title'] = at.string            
            #链接        
            self.infoT['url'] = at['href']
            if  checkPath("pagecash",self.infoT['url']):
                self.isFetched = True
                return
        else:
            
            return

        agencyname = regx_data("(个人)",str(soup),"",False) 
        if agencyname:
            self.infoT['isPerson'] = 1
        else:
            self.infoT['isPerson'] = 0
        
        #价格
        if soup.find('b',{'class':'pri'}):            
            self.infoT['price'] = soup.find('b',{'class':'pri'}).string
            if self.infoT['price']:
                if self.infoT['price'].find('-') != -1:
                    self.infoT['price_max'] = self.infoT['price'].split("-")[1]
                    self.infoT['price'] = self.infoT['price'].split("-")[0]
        
        self.infoT['room'] = soup("td")[2].string
        
        #时间
        tds = soup("td")[3]
        if tds:
            self.infoT['posttime']= self.postTime(tds.string)
            #rint tds.string
        self.infoT['search']= re.sub("<.*?>","",str(soup))
        del soup
        del at
        del agencyname
        del tds    
        self.getContent()  
        
    def __parseSellTrs(self,tr):
        
        soup = BeautifulSoup(tr)        
        at = soup.find('a',{'class':'t'})
        #标题
        if at:
            self.infoT['title'] = at.string            
            #链接        
            self.infoT['url'] = at['href']
            if  checkPath("pagecash",self.infoT['url']):
                self.isFetched = True
                return
        else:
            
            return

        #图片
        img = soup.find('td',{'class':'img'})
        if img:
            if img.img['src'].find("noimg") == -1:
                self.infoT['thumb'] = img.img['src']
                
        #信息
        t = soup.find('td',{'class':'t'})

        self.infoT['topfloor'] = regx_data(self.house_topfloor_regex,str(t),"",False) 
        self.infoT['floor'] = regx_data(self.house_floor_regex,str(t),"",False) 
        self.infoT['belong'] = regx_data(self.house_belong_dict_regex,str(t),"",False) 
        self.infoT['houseType'] = regx_data(self.house_type_regex,str(t),"",False)
        self.infoT['toward'] = regx_data(self.house_toward_regex,str(t),"",False)
        self.infoT['age'] = regx_data("(\d+)年",str(t),"",False)
        self.infoT['posttime'] = self.postTime(regx_data("更新时间：(.*?)<",str(t),"",False))
                 
        #self.infoT['room'] = regx_data(self.house_room_regex,str(soup),"",False) 
        #if self.infoT['room']:
            #self.infoT['room'] = re.sub("一|二|三|四|五|六|七|八|九|十","1|2|3|4|5|6|7|8|9|10",self.infoT['room'])
        self.infoT['hall'] = regx_data(self.house_hall_regex,str(soup),"",False) 
        self.infoT['toilet'] = regx_data(self.house_toilet_regex,str(soup),"",False) 
        
        agencyname = regx_data("(个人)",str(t),"",False) 
        if agencyname:
            self.infoT['isPerson'] = 1
        else:
            self.infoT['isPerson'] = 0

        #价格
        num = soup('td',{'class':'tc'})
        if num and len(num) > 1:  
            if str(num[0]).find("面议") == -1:     
                self.infoT['price'] = num[0].b.string
          
            self.infoT['area'] = num[1].b.string
  
            
        self.infoT['search']= re.sub("<.*?>","",str(soup))
        del soup
        del t
        del img
        del at
        del agencyname
        self.getContent()
        
    def __parseRentTrs(self,tr):
        soup = BeautifulSoup(tr)
        at = soup.find('a',{'class':'t'})
        #标题
        if at:
            self.infoT['title'] = at.string            
            #链接        
            self.infoT['url'] = at['href']
            if  checkPath("pagecash",self.infoT['url']):
                self.isFetched = True
                return
        else:
            
            return

        #图片
        img = soup.find('td',{'class':'img'})
        if img:
            if img.img['src'].find("noimg") == -1:
                self.infoT['thumb'] = img.img['src']
                
        #信息
        t = soup.find('td',{'class':'t'})
    
        self.infoT['topfloor'] = regx_data(self.house_topfloor_regex,str(t),"",False) 
        self.infoT['floor'] = regx_data(self.house_floor_regex,str(t),"",False) 
        self.infoT['area'] = regx_data(self.house_totalarea_regex,str(t),"",False) 
        self.infoT['fitment'] = regx_data(self.house_fitment_regex,str(t),"",False) 
        
        self.infoT['room'] = regx_data(self.house_room_regex,str(soup),"",False) 
        self.infoT['hall'] = regx_data(self.house_hall_regex,str(soup),"",False) 
        self.infoT['toilet'] = regx_data(self.house_toilet_regex,str(soup),"",False) 
        self.infoT['equ'] = regx_data("配置：(.*?)<",str(soup),"",False) 
        
        agencyname = regx_data("(个人)",str(t),"",False) 
        if agencyname:
            self.infoT['isPerson'] = 1
        else:
            self.infoT['isPerson'] = 0
        
        #价格
        if soup.find('b',{'class':'pri'}):
            
            self.infoT['price'] = soup.find('b',{'class':'pri'}).string

        #时间
        tds = soup("td")[4]
        if tds:
            self.infoT['posttime']= self.postTime(tds.string)
            #rint tds.string
        self.infoT['search']= re.sub("<.*?>","",str(soup))
        del soup
        del t
        del img
        del at
        del agencyname
        del tds
        self.getContent()
    def __cInit__(self,url):
        try:
            request = urllib2.Request(url, None, self.header)        
            self.response = urllib2.urlopen(request).read()
        except Exception,what: 
            return False
        else:
            return True
           
        
    def req(self):        
        sHtml = self.response
        self.response = None
        #个人  OR 经纪人
        #agencyname = regx_data(self.agencyname_regex,sHtml,"个人房源",False)
        #if not agencyname:
            #agencyname = '个人房源'
        #联系人
        
        self.infoT['owner'] = regx_data(self.username_regex,sHtml,"个人",False)                   
        #价格
        if not self.infoT['price']:
            self.infoT['price'] = regx_data(self.house_price_regex,sHtml,0,False)   
        #500以下
        if not self.infoT['price'] :
            self.infoT['price'] = regx_data(self.house_price1_regex,sHtml,0,False)   
        #以上 
        if not self.infoT['price'] :
            self.infoT['price'] = regx_data(self.house_price2_regex,sHtml,0,False)
        #标题
        if not self.infoT['title']:
            self.infoT['title'] = regx_data(self.house_title_regex,sHtml,"",False)        
        #发布时间
        if not self.infoT['posttime']:
            self.infoT['posttime'] = self.postTime(regx_data(self.house_posttime_regex,sHtml,"",False))       
        #house_posttime = postTime(house_posttime,1)        
        #室
        if not self.infoT['room']:
            self.infoT['room'] = regx_data(self.house_room_regex,sHtml,"",False) 
         #区
        
        self.infoT['region'] = regx_data(self.house_region_regex,sHtml,"",False)        
        #地段
        #print self.house_section_regex
        self.infoT['section'] = regx_data(self.house_section_regex,sHtml,"",False)    
        #详细
        self.infoT['desc'] = regx_data(self.house_desc_regex,sHtml,"",False ,"<.*?>")
        #电话
        if self.param['getPhone']:
            self.infoT['phone'] = regx_data(self.house_phone_regex,sHtml,"",False)        
    def rent(self):
        sHtml = self.response
        self.response = None
        #个人  OR 经纪人
        #agencyname = regx_data(self.agencyname_regex,sHtml,"",False) 
        #联系人
        self.infoT['owner'] = regx_data(self.username_regex,sHtml,"个人",False)        
        #楼层
        if not self.infoT['floor']:
            self.infoT['floor'] = regx_data(self.house_floor_regex,sHtml,"",False)        
        #顶层
        if not self.infoT['topfloor']:
            self.infoT['topfloor'] = regx_data(self.house_topfloor_regex,sHtml,"",False)        
        #面积
        if not self.infoT['area']:
            self.infoT['area'] = regx_data(self.house_totalarea_regex,sHtml,"",False)        
        #价格
        if not self.infoT['price']:
            self.infoT['price'] = regx_data(self.house_price_regex,sHtml,0,False)        
        #标题
        if not self.infoT['title']:
            self.infoT['title'] = regx_data(self.house_title_regex,sHtml,"",False)        
        #发布时间
        if not self.infoT['posttime']:
            self.infoT['posttime'] = self.postTime(regx_data(self.house_posttime_regex,sHtml,"",False) )      
        #house_posttime = postTime(house_posttime,1)        
        #室
        if not self.infoT['room']:
            self.infoT['room'] = regx_data(self.house_room_regex,sHtml,"",False)        
        #厅
        if not self.infoT['hall']:
            self.infoT['hall'] = regx_data(self.house_hall_regex,sHtml,"",False)        
        #卫
        if not self.infoT['toilet']:
            self.infoT['toilet'] = regx_data(self.house_toilet_regex,sHtml,"",False)        
        #押金
        if not self.infoT['deposit']:
            self.infoT['deposit'] = regx_data(self.house_deposit_regex,sHtml,"",False)        
             
        #小区
        self.infoT['borough'] = regx_data(self.borough_name_regex,sHtml,"",False)        
        #地址
        self.infoT['addr'] = regx_data(self.house_addr_regex,sHtml,"",False)        
        #区
        self.infoT['region'] = regx_data(self.house_region_regex,sHtml,"",False)        
        #地段
        self.infoT['section'] = regx_data(self.house_section_regex,sHtml,"",False)        
        #详细
        self.infoT['desc'] = regx_data(self.house_desc_regex,sHtml,"",False ,"<.*?>")        
              
        #图片
        self.infoT['pics'] = regx_datas(self.house_pics_regex,sHtml,"",False ,"tiny","big")    
        _t = regx_data(self.house_toward_t_regex,sHtml,"",False) 
        #装修
        if not self.infoT['fitment']:
            self.infoT['fitment'] = regx_data(self.house_fitment_regex,_t,"",False)        
        #朝向
        if not self.infoT['toward']:
            self.infoT['toward'] = regx_data(self.house_toward_regex,_t,"",False)        
        #类型
        if not self.infoT['houseType']:
            self.infoT['houseType'] = regx_data(self.house_type_regex,_t,"",False) 
        #电话
        if self.param['getPhone']:
            self.infoT['phone'] = regx_data(self.house_phone_regex,sHtml,"",False)  

        
    def buy(self):
        sHtml = self.response
        self.response = None
        #个人  OR 经纪人
        #agencyname = regx_data(self.agencyname_regex,sHtml,"",False) 
        #联系人
        if not self.infoT['owner']:
            self.infoT['owner']= regx_data(self.username_regex,sHtml,"个人",False)              
        #面积
        if not self.infoT['area']:
            self.infoT['area'] = regx_data(self.house_totalarea_regex,sHtml,"",False)        
        #价格
        if not self.infoT['price']:
            self.infoT['price']= regx_data(self.house_price_regex,sHtml,0,False)        
        #标题
        if not self.infoT['title']:
            self.infoT['title'] = regx_data(self.house_title_regex,sHtml,"",False)        
        #发布时间
        if not self.infoT['posttime']:
            self.infoT['posttime'] = self.postTime(regx_data(self.house_posttime_regex,sHtml,"",False) )      
        #house_posttime = postTime(house_posttime,1)        
        #室
        if not self.infoT['room']:
            self.infoT['room'] = regx_data(self.house_room_regex,sHtml,"",False) 
        #地址
        self.infoT['addr'] = regx_data(self.house_addr_regex,sHtml,"",False)              
        #详细
        self.infoT['desc'] = regx_data(self.house_desc_regex,sHtml,"",False ,"<.*?>")
        
        #图片
        self.infoT['pics'] = regx_datas(self.house_pics_regex,sHtml,"",False ,"tiny","big")    
        #电话
        if self.param['getPhone']:
            self.infoT['phone'] = regx_data(self.house_phone_regex,sHtml,"",False)  

    def sell(self):
        sHtml = self.response
        self.response = None
        #个人  OR 经纪人
        #agencyname = regx_data(self.agencyname_regex,sHtml,"",False) 
        #联系人
        self.infoT['owner'] = regx_data(self.username_regex,sHtml,"个人",False)        
        #楼层
        if not self.infoT['floor']:
            self.infoT['floor'] = regx_data(self.house_floor_regex,sHtml,"",False)        
        #顶层
        if not self.infoT['topfloor']:
            self.infoT['topfloor']= regx_data(self.house_topfloor_regex,sHtml,"",False)        
        #面积
        if not self.infoT['area']:
            self.infoT['area'] = regx_data(self.house_totalarea_regex,sHtml,"",False)        
        #价格
        if not self.infoT['price']:
            self.infoT['price'] = regx_data(self.house_price_regex,sHtml,0,False)        
        #标题
        if not self.infoT['title']:
            self.infoT['title'] = regx_data(self.house_title_regex,sHtml,"",False)        
        #发布时间
        if not self.infoT['posttime']:
            self.infoT['posttime'] = self.postTime(regx_data(self.house_posttime_regex,sHtml,"",False) )      
        #house_posttime = postTime(house_posttime,1)        
        #室
        if not self.infoT['room']:
            self.infoT['room'] = regx_data(self.house_room_regex,sHtml,"",False)        
        #厅
        if not self.infoT['hall']:
            self.infoT['hall'] = regx_data(self.house_hall_regex,sHtml,"",False)        
        #卫
        if not self.infoT['toilet']:
            self.infoT['toilet'] = regx_data(self.house_toilet_regex,sHtml,"",False)        
        #产权 
        if not self.infoT['belong']: 
            self.infoT['belong'] = regx_data(self.house_belong_regex,sHtml,"",False)        
        #房龄 99年
        self.infoT['age'] = regx_data(self.house_age_regex,sHtml,"",False)        
        #小区
        self.infoT['borough'] = regx_data(self.borough_name_regex,sHtml,"",False)        
        #地址
        self.infoT['addr'] = regx_data(self.house_addr_regex,sHtml,"",False)        
        #区
        self.infoT['region'] = regx_data(self.house_region_regex,sHtml,"",False)        
        #地段
        self.infoT['section'] = regx_data(self.house_section_regex,sHtml,"",False)        
        #详细
        self.infoT['desc'] = regx_data(self.house_desc_regex,sHtml,"",False ,"<.*?>")        
               
        #图片
        self.infoT['pics'] = regx_datas(self.house_pics_regex,sHtml,"",False ,"tiny","big")    
        _t = regx_data(self.house_toward_t_regex,sHtml,"",False) 
        #装修
        if not self.infoT['fitment']:
            self.infoT['fitment'] = regx_data(self.house_fitment_regex,_t,"",False)        
        #朝向
        if not self.infoT['toward']:
            self.infoT['toward'] = regx_data(self.house_toward_regex,_t,"",False) 
        #类型
        if not self.infoT['houseType']:
            self.infoT['houseType'] = regx_data(self.house_type_regex,_t,"",False) 
        #电话
        if self.param['getPhone']:
            self.infoT['phone'] = regx_data(self.house_phone_regex,sHtml,"",False)  

    def _initRe(self):
        self.page_main_regex = "<div id=\"main\">(.*?)<div id=\"links\"> "
        self.agencyname_regex="agencyname:'(.*?)',"
        self.username_regex="username:'(.*?)',"
        self.house_title_regex="<h1>(.*)</h1>"        
        self.house_floor_regex="第(\d+)层"
        self.house_topfloor_regex="共(\d+)层"       

        self.house_room_regex="(\d+|一|二|三|四|五|六|七|八|九|十)室"
        self.house_hall_regex="(\d+)厅"
        self.house_toilet_regex="(\d+)卫"
        self.house_posttime_regex="发布时间：(.*?)浏览"        
               
        self.house_age_regex="(\d+)年"        
        
               
        self.house_region_regex = "locallist.*?listname.*?name:'(.*?)'"        
        self.house_section_regex = "<li><i>区域：</i><a.*?<a.*?>(.*?)</a></li>"        
        self.house_desc_regex = "class=\"maincon\">(.*?)</div>"        
        self.house_phone_regex = "(http://image.58.com/showphone.aspx.*?)'"        
        self.house_pics_regex = "(http://\d+.pic.58control.cn/p\d+/tiny/n_\d+.jpg)"        
              
        self.house_toward_regex = "(东|南|西|北|南北|东西|东南|东北|西北)"
        self.house_fitment_regex = "(毛坯|简单装修|中等装修|精装修|豪华装修)"
        self.house_belong_dict_regex = "(商品房|经济适用房|公房|用权)"
        self.house_type_regex = "(平房|普通住宅|商住两用|公寓|别墅)"
        
        self.borough_name_regex = "<li><i>小区：</i><.*?>(.*?)<.*?></li>"
        self.borough_name1_regex = "<li><i>小区：</i>(.*?)</li>"
        

        if self.param['flag'] ==1:
            self.house_addr_regex = "address\">(.*?)<" 
            self.house_totalarea_regex="(\d+)㎡"
            self.house_belong_regex="<li><i>产权：</i>(.*?)</li>" 
            self.house_price_regex="(\d+)万元"   
            self.house_toward_t_regex = "房龄：</i>(.*?)<"  

        elif self.param['flag'] ==2:            
            self.house_totalarea_regex="(\d+)㎡"
            self.house_price_regex="(\d+)元/月"
            self.house_equ_regex="vartmp='(.*?)';"
            self.house_deposit_regex="(押一付三|押一付一|押二付一|半年付|年付)"
            self.house_toward_t_regex = "基本情况：</i>(.*?)<"  
            self.house_addr_regex = "address\">(.*?)<" 
        
            
        elif self.param['flag'] ==3:
            self.house_belong_regex="<li><i>产权：</i>(.*?)</li>" 
            self.house_totalarea_regex="(\d+-\d+)㎡" 
            self.house_addr_regex="<li><i>地段：</i>(.*?)</li>"
            self.house_price_regex="(\d+-\d+)万元"
        elif self.param['flag'] ==4:
            self.house_price_regex="(\d+-\d+)元"
            self.house_price1_regex="(\d+)元以下"
            self.house_price2_regex="(\d+)元以上"
            self.house_room_regex="(一|两|三|四)居室"
    def _initTemple(self,flag,city):
        
        self.infoT = {
                      'flag':flag,#房源类型 1 出售 2 出租 3 求购  4 求租
                      'title':'',
                      'posttime':'',
                      'price':0,
                      'price_max':0,
                      'deposit':'',
                      'belong':'',
                      'room':0,
                      'hall':0,
                      'toilet':0,
                      'yt':0,
                      'area':0,
                      'area_max':0,
                      'houseType':'',
                      'fitment':'',
                      'floor':0,
                      'topfloor':0,
                      'toward':'',
                      'age':1,
                      'equ':'',
                      'city':city,
                      'region':'',
                      'borough':'',
                      'section':'',
                      'addr':'',
                      'phone':'',
                      'owner':'',
                      'desc':'',
                      'search':'',
                      'url':'',
                      'thumb':'',
                      'webFlag':1,
                      'isPerson':1,
                      }
    def postTime(self,posttime):    
        if posttime and posttime.find('now') != -1:
                posttime = int(time.time())
        if not posttime:
            return
        posttime = str(posttime).replace('前','')
        #print posttime
        if posttime.find("<") != -1 or posttime.find(">") != -1:
            posttime = re.sub('<.*?>','' ,pottime)                
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
                            
        if (time.time() - self.fd['posttime']) > 3600*24*7: 
            return
            print "++++++++++++++++"                 
        print time.strftime('%Y %m %d', time.localtime(self.fd['posttime']))     
    def run(self):
        self.pageNo = 1           
        while 1:
            if self.isStoped == True:
                break
            if self.pageNo:
                url = self.baseUrl(self.param['args'],self.pageNo)
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
        
q = []
if __name__=="__main__":    
    url1 = 'http://sh.58.com/ershoufang/7489033818376x.shtml'
    url2 = 'http://sh.58.com/zufang/7468246420482x.shtml'
    url3 = 'http://sh.58.com/ershoufang/7544211350792x.shtml'
    url4 = 'http://sh.58.com/qiuzu/7543125341446x.shtml'
    link2 = 'http://sh.58.com/zufang/0/?selpic=2'
    link1 = 'http://sh.58.com/ershoufang/'
    link3 = 'http://sh.58.com/ershoufang/h2/'
    link4 = 'http://sh.58.com/qiuzu/0/'
    data = {}
    data['flag'] = 1
    data['city'] = 1
    data['getPhone'] = 1
    cc = BaseCrawl(data,q)
    cc.run()

