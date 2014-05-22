#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cookielib
import urllib2
import mimetypes
import os
import re
import urllib
import traceback 

header = {
            "User-Agent":'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB6.6; .NET CLR 3.5.30729)',
        }
class MyException(Exception):
    def __init__(self, type,note):
        self.type = type
        self.note=note
    def __str__(self):
        return str("%s|%s"%(self.type,self.note))

class browser():
    def __init__(self,ppms):
        cj = cookielib.MozillaCookieJar("c:\\58.txt")
        self.br=urllib2.build_opener(urllib2.HTTPHandler(),urllib2.HTTPCookieProcessor(cj),urllib2.HTTPRedirectHandler())
        self.cj = cj
        self.pdb={}
        self.header=header
        self.ppms=ppms
        self.picRoot=""#"/home/wwwroot/jjr360v1.1/site.jjr.com/upfile/"
        self.gobalsokey_p1=""
        self.gobalsokey_p2=""
        self.isSell=False
        #======================================
        self.city="3"
        self.images=[]
        self.uname=""
        self.upass=""
        self.email=""
        self.contact="李新佳"
        self.PicL=[]
        self.localArea="1411"
        self.localDiduan="5910"
        self.ObjectType="3"
        self.toward=""
        self.fitType="2"
        self.fukuanfangshi="1"
        self.title="闸北新立小区花园整间出租"
        self.xiaoqu="闸北新立小区花园整间出租"
        self.content="<SPAN id=comp-paste-div-700>闸北新立小区花园整间出租<SPAN id=comp-paste-div-700>闸北新立小区花园整间出租</SPAN></SPAN>"
        self.MinPrice="面议"
        self.area="43"
        self.jushishuru="1"
        self.huxingting="1"
        self.huxingwei="1"
        self.Floor="2"
        self.zonglouceng="33"
        self.mobile=""
        self.citycode=self.ppms["citycode"]
        #self.subdict={
    def saveCookie(self):
        self.cj.save(ignore_discard=True, ignore_expires=True)
    def goPublishPage(self):
        req=urllib2.Request("http://post.58.com/%s/"%self.city, None, self.header)
        self.br.open(req)
        req=urllib2.Request("http://track.58.com/referrer2.js", None, self.header)
        self.br.open(req)
        #self.saveCookie()
    def goUploadPics(self):
        for pic  in self.images[0:8]:
            self.processUploadPics(pic)
        self.subdict["Pic"]="%s"%"|".join(self.PicL)
        self.subdict["PicPos"]="1"
    def goLogin(self):
        params="uname=%s&upass=%s&email=%s&typeid=0&cityid=%s"%(self.uname,self.upass,self.email,self.city)
        req=urllib2.Request("http://post.58.com/ajax/?action=userreglogin", params, self.header)
        pp=self.br.open(req).read()
        error=""
        if re.search('''{result:'0', error:'(.*)'}''', pp):
            error=re.search('''{result:'0', error:'(.*)'}''', pp).group(1)
        if error !="":
            raise Exception("loginerror|%s"%error)
    def makePostData(self,dict):
        params = urllib.urlencode(dict)
        return  params;
    def debugPostData(self):
        if DEBUG:
            for i in self.subdict:
                print i,self.subdict[i]
    def goSubmit(self):
        fp=self.makePostData(self.subdict)
        self.debugPostData()
        if self.isSell:
            catcode = 'ershoufang'
            req=urllib2.Request("http://post.58.com/%s/12/s5/submit"%self.city, fp, self.header)
        else:
            catcode = 'zufang'
            req=urllib2.Request("http://post.58.com/%s/8/s5/submit"%self.city, fp, self.header)
        
        try:
            page=self.br.open(req).read()
        except Exception,e:
            print traceback.format_exc()
            return "%s|%s"%("puterror",e)
        
        note=""
        #print page
        if '''<script>parent.window.location.href='http://my.58.com/InfoPressSuccess/?infoid='''in page:
            if re.search('''<script>parent.window.location.href='(.*)'</script></form>''', page):
                note=re.search('''infoid=(.*)&cityinfo''', page).group(1)
                note="http://"+self.citycode+".58.com/"+catcode+"/"+note+"x.shtml"
                return "success|%s"%(note,)
        else:
            
            if re.search('''parent\.\$\.c\.Error\.showError\('(.*)'\);''', page):
                note=re.search('''parent\.\$\.c\.Error\.showError\('(.*)'\);''', page).group(1)
                pos=note.find("<")
                note=note[:pos]
                return "incomplete|%s"%(note,)
             
            elif "errorInfo.S_Message" in page:
                if re.search(''''msg':\['(.*)'\],''', page):
                    note=re.search(''''msg':\['(.*)'\],''', page).group(1)
                    if "<span class=currentMaxValue>" in note:
                        return "maxhouse|您的该账号今日可发房源数已满"
                    else:
                        return "samehouse|%s"%(note,)
                                    
    def uploadfile(self,fields, files):
        BOUNDARY = '----------267402204411258'
        CRLF = '\r\n'
        L = []
        for (key, value) in fields:
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="%s"' % key)
            L.append('')
            L.append(value)
        for (key, filename, value) in files:
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
            L.append('Content-Type: %s' % mimetypes.guess_type(filename)[0] or 'application/octet-stream')
            L.append('')
            L.append(value)
        L.append('--' + BOUNDARY + '--')
        L.append('')
        body = CRLF.join(L)
        content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
        return content_type, body
    def porcessGetParams(self):
        self.uname=self.ppms["username"]
        self.upass=self.ppms["passwd"]
        self.title=self.ppms["house_title"]
        self.city=self.ppms["city"]
        self.localArea=self.ppms["cityarea_id"]
        self.localDiduan=self.ppms["borough_section"]
        house_type={"2":"平房","3":"普通住宅","4":"公寓","5":"别墅","6":"其他","7":"商住两用"}
        if self.ppms["house_type"] in house_type.keys():
            self.gobalsokey_p1=house_type[self.ppms["house_type"]]
            self.ObjectType=self.ppms["house_type"]
        else:
            self.gobalsokey_p1="普通住宅"
            self.ObjectType=self.ppms["house_type"]
        self.toward=self.ppms["house_toward"]
        house_deposit=["0","1","3","8","6","7",]
        if self.ppms["house_deposit"]not in house_deposit:
            self.fukuanfangshi="1"
        else:
            self.fukuanfangshi=self.ppms["house_deposit"]
            
            
        self.MinPrice=self.ppms["house_price"]
        self.area=self.ppms["house_totalarea"]
        self.jushishuru=self.ppms["house_room"]
        self.huxingshi=self.ppms["house_room"]
        self.zonglouceng=self.ppms["house_topfloor"]
        self.huxingting=self.ppms["house_hall"]
        self.huxingwei=self.ppms["house_toilet"]
        self.Floor=self.ppms["house_floor"]
        self.content=self.ppms["house_desc"]
        house_fitment={"1":"毛坯","2":"简单装修","3":"中等装修","4":"精装修","5":"豪华装修",}
        if not self.ppms["house_fitment"] in house_fitment.keys():
            self.fitType="2"
        else:
            self.fitType=self.ppms["house_fitment"]
        self.gobalsokey_p2=house_fitment[self.ppms["house_fitment"]]
        
        
        self.xiaoqu=self.ppms["borough_name"]
        self.mobile=self.ppms["mobile"]
        self.contact=self.ppms["contact"]
        for pic1 in self.ppms["house_drawing"].split("|"):
            if pic1=="":
                continue
            self.images.append(pic1)
        for pic1 in self.ppms["house_thumb"]:
            if pic1=="":
                continue
            self.images.append(pic1)
        for pic1 in self.ppms["house_xqpic"]:
            if pic1=="":
                continue
            self.images.append(pic1)

        self.subdict={
             "area":self.area,
             "backFunction":"$.c.Uploader.finish",
             "busdistance":"",
             "Content":urllib.unquote(self.content),
             "daxue":"",
             "distancetime":"",
             "ditiexian":"",
             "ditiezhan":"",
             "dizhi":"",
             "fileUploadInput":"filename="" Content-Type: application/octet-stream",
             "FitType":self.fitType,
             "Floor":self.Floor,
             "fukuanfangshi":self.fukuanfangshi,
             "gobalsokey":"%s居室,%s居,%s室|%s层,%s楼|%s|%s"%(self.jushishuru,self.jushishuru,self.jushishuru,self.Floor,self.Floor,self.gobalsokey_p1,self.gobalsokey_p2),
             "goblianxiren":"%s"%self.contact,
             "gongjiaoxian":"",
             "gongjiaozhan":"",
             "hiddenTextBoxJoinValue":"%s:%s:%s:%s"%(self.xiaoqu,"",self.MinPrice=="" and "面议" or self.MinPrice,self.contact),
             "HireType":"2",
             "HouseAllocation":"6",
             "HouseAllocation":"8",
             "huxingshi":self.huxingshi,
             "huxingting":self.huxingting,
             "huxingwei":self.huxingwei,
             "jushishuru":self.jushishuru,
             "localArea":"%s"%self.localArea,
             "localDiduan":"%s"%self.localDiduan,
             "MinPrice":self.MinPrice,
             "ObjectType":self.ObjectType,
             "Phone":self.mobile,
             "PicDesc":"",
             "PicPos":"0",
             "postRegLogin":"0",
             "radioHasAccount":"1",
             "stationdistance":"",
             "Title":self.title,
             "Toward":self.toward,
             "xianluzhoubian":"",
             "xiaoqu":self.xiaoqu,
             "zonglouceng":self.zonglouceng,
             "IsBiz":"1"
             }    
                
        if self.ppms["house_kind"] =="1":
            self.isSell=True
            del self.subdict["HireType"]
            self.subdict["type"]="0"
            self.subdict["chanquan"]=self.ppms["belong"]
            self.subdict["diduan"]="[|#|@]"
            self.subdict["diduan2"]="[|#|@]"
            self.subdict["BuildingEra"]=self.ppms["house_age"]
            
            self.subdict["xiaoqu_view"]=self.xiaoqu
            self.subdict["hiddenTextBoxJoinValue"]="%s:%s:%s"%(self.xiaoqu,self.contact,self.uname)
            self.subdict["gobalsokey"]="%s|%s|%s居室,%s居,%s室|%s层,%s楼|%s|%s平米|%s|%s"%(self.title,self.xiaoqu,self.jushishuru,self.jushishuru,self.jushishuru,self.Floor,self.Floor,self.MinPrice,self.area,self.gobalsokey_p1,self.gobalsokey_p2)
        #print  self.subdict       
                
                
    def getCityarea_id(self,caid):
        return "1411"
    def getBorough_section(self,bs):
        return "5910"
    def processUploadPics(self,pic):
        #self.br.handlers[6].cookiejar
        publishdict={
                 "area":"",
                 "backFunction":"$.c.Uploader.finish",
                 "busdistance":"",
                 "Content":"例如对求租者的要求，房间情况，附近环境，周边配套信息…",
                 "daxue":"",
                 "distancetime":"",
                 "ditiexian":"",
                 "ditiezhan":"",
                 "dizhi":"",
                 "FitType":"2",
                 "Floor":"",
                 "fukuanfangshi":"1",
                 "goblianxiren":"",
                 "gongjiaoxian":"",
                 "gongjiaozhan":"",
                 "HireType":"2",
                 "HouseAllocation":"6",
                 "HouseAllocation":"8",
                 "huxingshi":"",
                 "huxingting":"",
                 "huxingwei":"",
                 "jushishuru":"",
                 "localArea":"",
                 "localDiduan":"",
                 "MinPrice":"面议",
                 "ObjectType":"3",
                 "Phone":"",
                 "Pic":"",
                 "PicDesc":"",
                 "PicPos":"1",
                 "postRegLogin":"1",
                 "stationdistance":"",
                 "Title":"",
                 "Toward":"",
                 "xianluzhoubian":"",
                 "xiaoqu":"",
                 "zonglouceng":"",
                 
                 }
        imgdata= file(self.picRoot+pic,"rb")
        files=[
               ('fileUploadInput',os.path.basename(pic),imgdata.read())
               ]
        content_type, upload_data = self.uploadfile(publishdict.items(), files)
        uploadheader={
                "User-Agent": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB6.6; .NET CLR 3.5.30729)",
                'Content-Type': content_type,
                'Content-Length': str(len(upload_data))
                }
        req = urllib2.Request("http://post.58.com/upload", upload_data, uploadheader)
        page=self.br.open(req).read()
        if re.search(r'''finish\(\d, '(.*)', \d\);''', page):
            self.PicL.append(re.search(r'''finish\(\d, '(.*)', \d\);''', page).group(1))
            
            
def Publish(p):
    try:
        br=browser(p)
        br.porcessGetParams()
        br.goPublishPage()
        br.goUploadPics()
        br.goLogin()
        sts=br.goSubmit()  
        return sts  
    except Exception,e:
        print traceback.format_exc() 
        return str(e)
        
if __name__=="__main__":
    p={
    "house_kind":"2",
    "username":"liseor8855",
    "passwd":"200898",
    "webid":"8",
    "broker_id":"1111",
    "citycode":"suzhou",
    "house_title":"领公寓 媲美酒店",
    "city":"2",
    "cityarea_id":"1411",
    "borough_section":"5910",
    "house_type":"3",
    "house_toward":"1",
    "house_fitment":"2",    
    "house_deposit":"1",
    "belong":"1",
    "house_price":"500",
    "house_totalarea":"120",
    "house_room":"3",
    "house_hall":"2",
    "house_toilet":"1",
    "house_topfloor":"6",
    "house_floor":"2",
    "house_age":"10",
    "house_desc":'''<SPAN id=comp-paste-div-700><font color='red'>领公领公寓 媲美酒店寓 媲美酒店</font></SPAN>''',
    "borough_id":"10",
    "borough_name":"市区高档品质小区",
    "house_drawing":"d:/111.jpg|d:/111.jpg",
    "house_thumb":"",
    "house_xqpic":"",
    #========================
    "mobile":"13855698654",
    "contact":"苏大生",
    
   }
    DEBUG = 1
    print Publish(p)
    #br=browser(p)
    #br.porcessGetParams()
    #br.goPublishPage()
#    br.goUploadPics()
    #br.goLogin()