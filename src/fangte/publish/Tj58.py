#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cookielib
import urllib2
import mimetypes
import os
import re
import urllib
import traceback 
import json
import time,datetime
import random
header = {
            "User-Agent":'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB6.6; .NET CLR 3.5.30729)',
        }
def regx_data(regx,html,default,d= False,clean=False,rep=''):
    #print regx
    if re.search(regx, html):        
        data = re.search(regx, html).group(1)
        if clean:
            print rep
            data = re.sub(clean,rep,data)
        if d:
            print regx
            print data
        return data
    else:
        if d:
            print regx
            print "没有"
        return default
class MyException(Exception):
    def __init__(self, type,note):
        self.type = type
        self.note=note
    def __str__(self):
        return str("%s|%s"%(self.type,self.note))

class browser():
    def __init__(self,param):
        self.cityid = "2"
        cj = cookielib.MozillaCookieJar("c:\\58.txt")
        #cj.load("c:\\58.txt")
        self.br=urllib2.build_opener(urllib2.HTTPHandler(),urllib2.HTTPCookieProcessor(cj),urllib2.HTTPRedirectHandler())
        #add_header('Referer', 'http://www.python.org/')
        self.cj = cj
        self.pdb={}
        self.header=header
        self.param=param
        self.returnStr = ""
        
        #self.subdict={
    def saveCookie(self):
        self.cj.save(ignore_discard=True, ignore_expires=True)
        
    def goLogin(self):
        
        self.uname = self.param['login']['username']
        self.upass = self.param['login']['password']
        self.email = ""
        params="uname=%s&upass=%s&email=%s&typeid=0&cityid=%s"%(self.uname,self.upass,self.email,self.cityid)
        req=urllib2.Request("http://post.58.com/ajax/?action=userreglogin", params, self.header)
        res=self.br.open(req).read()
        
        #error=""
        #if re.search('''{result:'0', error:'(.*)'}''', pp):
            #error=re.search('''{result:'0', error:'(.*)'}''', pp).group(1)
        #if error !="":
            #raise Exception("loginerror|%s"%error)
        #res =  self.br.open(req).read()
        #if "login_success.php" in res:
            #self.returnStr =  "登陆成功"
            #print self.returnStr
            #self.saveCookie()
        
        
        
        
    def goRegPage(self):
        self.regUrl = "http://passport.58.com/reg/?city=%s" % self.param['citycode']
        self.regSubmitUrl = "http://passport.58.com/submit"
        
        self.checkCodeUrl = "http://%s.ganji.com/ajax/check_code_v5.php" % self.param['citycode']
        self.regSaveUrl = "http://passport.58.com/save"
        
        
        req=urllib2.Request(self.regUrl , None, self.header)
        res = self.br.open(req)
        req=urllib2.Request(self.regSubmitUrl , None, self.header)
        req.add_header('Referer', self.regUrl)
        res = self.br.open(req)
        self.goCheckUserName()
        self.goCheckEmail()
        #self.saveCookie()
    def goCheckUserName(self):
        self.checkUserNameUrl = "http://passport.58.com/ajax/checknickname?id=%d&nickname=%s" % (random.randint(1000, 9999),self.param['reg']['username'])
        req=urllib2.Request(self.checkUserNameUrl ,None, self.header)
        req.add_header('Referer', self.regUrl)
        res = self.br.open(req).read()
        if int(res.strip()) != 1:
            print "用户名有误"
        else:
            print "用户名成功"
    def goCheckEmail(self):
        self.checkEmailUrl = "http://passport.58.com/ajax/checkemail?id=%d&email=%s" % (random.randint(1000, 9999),self.param['reg']['email'])
        req=urllib2.Request(self.checkEmailUrl ,None, self.header)
        req.add_header('Referer', self.regUrl)
        res = self.br.open(req).read()
        if int(res.strip()) != 1:
            print "emain有误"
        else:
            print "邮箱验证成功"
        #code = regx_data("({.*?})",res,'')
        #j = json.loads(code)
        #regx_data()
        #if j['error'] == 1:
            #print self.param['reg']['username']
            #username  = raw_input(j['message'])
            #self.param['reg']['username'] =  username
            #self.goCheckUserName()
    def goCheckCode(self):
        self.CodeUrl = "http://sh.ganji.com/common/checkcode.php?nocache=%d" % int(time.time())
        req=urllib2.Request(self.CodeUrl , None, self.header)
        r = self.br.open(req).read()
        open("c:\\gj.jpg","wb").write(r)
        post={}
        code = raw_input("输入验证码：")
        post['checkcode'] = code.strip()
        req=urllib2.Request(self.checkCodeUrl , urllib.urlencode(post), self.header)
        res = self.br.open(req).read()
        r_code = regx_data("({.*?})",res,'')
        j = json.loads(r_code)
        #regx_data()
        print j
        if j['error'] == 1:
            self.goCheckCode()
        else:
            self.param['reg']['checkcode'] = code.strip()
        
    def goReg(self):
        #nickName=housemain&txtemail=112233pb%40afdsd.com&password=112233&cpassword=112233&checkbox=on
        regDict={
                 "nickName":self.param['reg']['username'],
                 "txtemail":self.param['reg']['email'],
                 "password":self.param['reg']['password'],
                 "cpassword":self.param['reg']['password'],
                 "checkbox":"on"
                 }
        regData = urllib.urlencode(regDict)
        print regData
        req=urllib2.Request(self.regSaveUrl, regData, self.header)
        req.add_header('Referer', self.regUrl)
        req.add_header('Origin', ":http://passport.58.com")
        pp=self.br.open(req).read()
        error=""
        if 'regok?regok=1' in pp:
            print "成功"
        if error !="":
            raise Exception("regError|%s"%error)
    
    def debugPostData(self):
        if DEBUG:
            for i in self.subdict:
                print i,self.subdict[i]
    def Login(self):
        self.goLogin()
    
    def uploadImages(self,ifiles):
        ###########################################
        fields=[
                ('MAX_FILE_SIZE','5242880')
                ]
        self.imagesdata = []
        for ifile in ifiles:
            imgdata= file(ifile,"rb")
            files=[
                   ('file',imgdata.name,imgdata.read())
                   ]
            content_type, upload_data = self.uploadfile(fields, files)
            
            uploadheader={
                    "User-Agent": "Mozilla/5.0 (Windows NT 5.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
                    'Content-Type': content_type,
                    'Content-Length': str(len(upload_data))
                    }
            request = urllib2.Request("http://image.ganji.com/upload.php", upload_data, uploadheader)
            js=self.br.open(request).read()
            #print js
            #json.dumps()
            jsondict=json.loads(js)
            if jsondict["error"]==0:
                imgid="tmp%s"%("%s"%time.time()).replace(".","%s"%random.randint(0,9))
                imgsdict={}
                imgdict={}
                imgdict["image"]=jsondict["info"][0]["url"]
                imgdict["thumb_image"]=jsondict["info"][0]["thumbUrl"]
                imgdict["row_id"]=""
                imgdict["is_new"]=True
                imgdict["id"]=imgid
                imgsdict[imgid]=imgdict
                self.imagesdata.append(imgsdict)  
    def getUsername(self):
        req=urllib2.Request("http://my.58.com/", None, self.header)
        
        rr =  self.br.open(req).read()
        if "审核中的信息" in rr:
            print "登陆中"
        else:
            print "没有登陆"
    def publish(self,type,ifiles):
        types={
               "zufang":"http://sh.ganji.com/common/pub.php?category=housing&type=1",
               "chushou":"http://sh.ganji.com/common/pub.php?category=housing&type=5",
               }   
        pay_type={
                    "1":"押一付三",
                    "2":"面议",
                    "3":"押一付一",
                    "4":"押一付二",
                    "5":"押二付一",
                    "9":"押二付三",
                    "6":"半年付不押",
                    "7":"年付不押",
                    "8":"押一付半年",
                  }
        #self.getUsername()
        request = urllib2.Request(types[type], None, self.header)
        #self.cj.add_cookie_header(request)
        
        response=self.br.open(request).read()
        self.saveCookie()
        self.imagesdata=[]
        self.uploadImages(ifiles)      
                
        ####################################################
        self.imagesdata.append({})
        publishdoct_rent={
                     "title":"文慧明圆插件租",
                     "xiaoqu":"徐汇馨苑",
                     "district_id":"1,徐汇",
                     "street_id":"24,上海南站",
                     "xiaoqu_address":"南宁路501弄",
                     "agent":"0",
                     "rent_mode":"1",#1 整租,2合租
                     "huxing_shi":"1",
                     "huxing_ting":"1",
                     "huxing_wei":"1",
                     "area":"30",
                     "price":"500",
                     "pay_type_int":"1",
                     "description":"慧明圆插件出租文慧明圆插件插件出租",
                     "phone":"13425478568",
                     "person":"周先生",
                     "images":json.dumps(self.imagesdata)=="[{}]" and  "" or json.dumps(self.imagesdata) ,
                     "latlng":"31.15331,121.429495",
                     "password":"111111",
                     "act":"submit",
                     "major_category":"1",
                     "pinyin":"xuhuixinyuan",
                     "share_type_list":"1",
                     "share_mode":"",
                     "house_type":"",
                     "ceng":"2",
                     "ceng_total":"3",
                     }
        publishdoct_sell={
                     "title":"新盘11月5号开盘,低价出售单价只要1.5万元",
                     "xiaoqu":"广海花园",
                     "district_id":"0,闵行",
                     "street_id":"4,七宝",
                     "xiaoqu_address":"七莘路2315弄",
                     "agent":"1",
                     "huxing_shi":"3",
                     "huxing_ting":"2",
                     "huxing_wei":"1",
                     "area":"30",
                     "price":"76",
                     "description":"单价只要1.5万元一平米，135万可以买两房一厅一卫",
                     "phone":"13425478568",
                     "person":"周先生",
                     "images":json.dumps(self.imagesdata)=="[{}]" and  "" or json.dumps(self.imagesdata) ,
                     "latlng":"31.15331,121.429495",
                     "password":"111111",
                     "act":"submit",
                     "major_category":"5",
                     "pinyin":"xuhuixinyuan",
                     "ceng":"2",
                     "ceng_total":"3",
                     "chaoxiang":"2",
                     "fang_xing":"3",
                     "zhuangxiu":"3",
                     "niandai":"2009",
                     }
        content_type, params = self.uploadfile(publishdoct_sell.items(), [])
        #print params
        publishheader={
               "User-Agent":"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB6.6; .NET CLR 3.5.30729)",
               "Referer":types[type],
               'Content-Type': content_type,
               'Content-Length': str(len(params))
               }
        request = urllib2.Request("http://sh.ganji.com/common/pub.php?category=housing&type=5",params, publishheader)
        res = self.br.open(request).read()
        if "发布成功啦！" in res:
            url = regx_data("您的帖子“<a href=\"(.*?)\">",res,"")
            print url
        else:
            print "error"
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
    def goUploadPics(self):
        for pic  in self.images[0:8]:
            self.processUploadPics(pic)
        self.subdict["Pic"]="%s"%"|".join(self.PicL)
        self.subdict["PicPos"]="1"
    def getCityarea_id(self,caid):
        return "1411"
    def getBorough_section(self,bs):
        return "5910"
    def processUploadPics(self):
        #print self.br.handlers[6].cookiejar
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
        imgdata= file("c:\\111.jpg","rb")
        files=[
               ('fileUploadInput',os.path.basename("c:\\111.jpg"),imgdata.read())
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
            print re.search(r'''finish\(\d, '(.*)', \d\);''', page).group(1)
            self.PicL.append(re.search(r'''finish\(\d, '(.*)', \d\);''', page).group(1))
    def goPublishPage(self):
        req=urllib2.Request("http://post.58.com/%s/"%self.cityid, None, self.header)
        self.br.open(req)
        req=urllib2.Request("http://track.58.com/referrer2.js", None, self.header)
        self.br.open(req)
        #print self.br._ua_handlers['_cookies'].cookiejar
    def goSubmit(self):
        postQuery = urllib.urlencode(self.subdict)
        if self.isSell:
            catcode = 'ershoufang'
            req=urllib2.Request("http://post.58.com/%s/12/s5/submit"%self.cityid, postQuery, self.header)
        else:
            catcode = 'zufang'
            req=urllib2.Request("http://post.58.com/%s/8/s5/submit"%self.cityid, postQuery, self.header)
        try:
            page=self.br.open(req).read()
            print page
        except Exception,e:
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
    def porcessGetParams(self):
        self.uname = self.param["login"]["usename"]
        self.title=self.param["publish"]["title"]
        
        self.localArea=self.param["publish"]["region"]
        self.localDiduan=self.param["publish"]["section"]
        
        self.gobalsokey_p1=""#"普通住宅"
        self.ObjectType=self.param["publish"]["houseType"]
            
        self.toward=self.param["publish"]["house_toward"]
        self.fukuanfangshi=self.param["publish"]["deposit"]
        
            
            
        self.MinPrice=self.param["publish"]["price"]
        self.area=self.param["publish"]["area"]
        self.jushishuru=self.param["publish"]["room"]
        self.huxingshi=self.param["publish"]["room"]
        self.zonglouceng=self.param["publish"]["topfloor"]
        self.huxingting=self.param["publish"]["hall"]
        self.huxingwei=self.param["publish"]["toilet"]
        self.Floor=self.param["publish"]["flloor"]
        
        self.content=self.param["publish"]["desc"]
        self.fitType=self.param["publish"]["fitment"]
        
        self.gobalsokey_p2=""#fitment
        
        self.xiaoqu=self.param["publish"]["borough"]
        self.mobile=self.param["publish"]["phone"]
        self.contact=self.param["publish"]["owner"]
        
        for pic in self.param["publish"]["pics"].split("|"):
            if pic=="":
                continue
            self.images.append(pic)

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
                
        if self.param["publish"]["flag"] =="1":
            self.isSell=True
            del self.subdict["HireType"]
            self.subdict["type"]="0"
            self.subdict["chanquan"]=self.param["publish"]["belong"]
            self.subdict["diduan"]="[|#|@]"
            self.subdict["diduan2"]="[|#|@]"
            self.subdict["BuildingEra"]=self.param["publish"]["house_age"]
            
            self.subdict["xiaoqu_view"]=self.xiaoqu
            self.subdict["hiddenTextBoxJoinValue"]="%s:%s:%s"%(self.xiaoqu,self.contact,self.uname)
            self.subdict["gobalsokey"]="%s|%s|%s居室,%s居,%s室|%s层,%s楼|%s|%s平米|%s|%s"%(self.title,self.xiaoqu,self.jushishuru,self.jushishuru,self.jushishuru,self.Floor,self.Floor,self.MinPrice,self.area,self.gobalsokey_p1,self.gobalsokey_p2)
        #print  self.subdict       
def Reg(p):
    try:
        br=browser(p)
        br.goRegPage()        
        br.goReg()
        #return sts  
    except Exception,e:
        print traceback.format_exc() 
        return str(e)      
def Login(p):
    try:
        br=browser(p)
        br.goLogin() 
        #return sts  
    except Exception,e:
        print traceback.format_exc() 
        return str(e)        

def Publish(p):
    try:
        br=browser(p)
        br.goLogin()
        br.getUsername()
        br.goPublishPage()
        br.goSubmit()
    except Exception,e:
        print traceback.format_exc() 
        return str(e) 

if __name__=="__main__":
    reg={
       "username":"housemian33",
       "password":"112233",
       "password2":"112233",
       "next":"http%3A%2F%2Fsh.ganji.com%2F",
       "second":"",
       "email":"567tyui@qq.com",
       "checkcode":"",
       "affirm":"on"
    }
    login={
       "source":"passport",
       "username":"housemain",
       "password":"112233",
       "expireDays":"365",
       "setcookie":"365",
       "next":""
    }
    p={}
    p['reg'] = reg
    p['login'] = login
    p['publish'] = ""
    p['citycode'] = "sh"
    DEBUG = 1
    #Reg(p)
    #Login(p)
    Publish(p)
    
    