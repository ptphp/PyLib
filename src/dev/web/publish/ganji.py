#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: Joseph
@email:liseor@gmail.com
Created on 2012-6-10
'''
import cookielib
import urllib2
import mimetypes
import os
import re
import urllib
import traceback 
import json
import time, datetime
import random

header = {
            "User-Agent":'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB6.6; .NET CLR 3.5.30729)',
        }
def regx_data(regx, html, default, d=False, clean=False, rep=''):
    #print regx
    if re.search(regx, html):        
        data = re.search(regx, html).group(1)
        if clean:
            print rep
            data = re.sub(clean, rep, data)
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
    def __init__(self, type, note):
        self.type = type
        self.note = note
    def __str__(self):
        return str("%s|%s" % (self.type, self.note))

class browser():
    def __init__(self, param):
        cj = cookielib.MozillaCookieJar("c:\\gj.txt")
        cj.load("c:\\gj.txt")
        self.br = urllib2.build_opener(urllib2.HTTPHandler(), urllib2.HTTPCookieProcessor(cj), urllib2.HTTPRedirectHandler())
        self.cj = cj
        self.pdb = {}
        self.header = header
        self.param = param
        self.returnStr = ""
        
        #self.subdict={
    def saveCookie(self):
        self.cj.save(ignore_discard=True, ignore_expires=True)
        
    def goLogin(self):
        self.loginUrl = "http://%s.ganji.com/user/login.php" % self.param['citycode']
        req = urllib2.Request(self.loginUrl , None, self.header)
        self.br.open(req)
        loginData = urllib.urlencode(self.param['login'])
        req = urllib2.Request(self.loginUrl , loginData, self.header)
        res = self.br.open(req).read()
        if "login_success.php" in res:
            self.returnStr = "登陆成功"
            print self.returnStr
            self.saveCookie()
            
        else:
            raise Exception("loginError|登陆失败")
        
    def goRegPage(self):
        self.regUrl = "http://%s.ganji.com/user/register.php" % self.param['citycode']
        self.checkUserNameUrl = "http://%s.ganji.com/user/ajax/checkUserName.php" % self.param['citycode']
        self.checkCodeUrl = "http://%s.ganji.com/ajax/check_code_v5.php" % self.param['citycode']
        
        req = urllib2.Request(self.regUrl , None, self.header)
        res = self.br.open(req)
        self.goCheckUserName()
        if """<label for="yzm">验证码：</label>""" in res:
            self.goCheckCode()
        #self.saveCookie()
    def goCheckUserName(self):
        post = {}
        post['username'] = self.param['reg']['username']
        req = urllib2.Request(self.checkUserNameUrl , urllib.urlencode(post), self.header)
        res = self.br.open(req).read()
        code = regx_data("({.*?})", res, '')
        j = json.loads(code)
        #regx_data()
        if j['error'] == 1:
            print self.param['reg']['username']
            username = raw_input(j['message'])
            self.param['reg']['username'] = username
            self.goCheckUserName()
    def goCheckCode(self):
        self.CodeUrl = "http://sh.ganji.com/common/checkcode.php?nocache=%d" % int(time.time())
        req = urllib2.Request(self.CodeUrl , None, self.header)
        r = self.br.open(req).read()
        open("c:\\gj.jpg", "wb").write(r)
        post = {}
        code = raw_input("输入验证码：")
        post['checkcode'] = code.strip()
        req = urllib2.Request(self.checkCodeUrl , urllib.urlencode(post), self.header)
        res = self.br.open(req).read()
        r_code = regx_data("({.*?})", res, '')
        j = json.loads(r_code)
        #regx_data()
        print j
        if j['error'] == 1:
            self.goCheckCode()
        else:
            self.param['reg']['checkcode'] = code.strip()
        
    def goReg(self):
        regData = urllib.urlencode(self.param['reg'])
        print regData
        req = urllib2.Request(self.regUrl, regData, self.header)
        pp = self.br.open(req).read()
        error = ""
        if '/user/register_success.php' in pp:
            print "成功"
        if error != "":
            raise Exception("regError|%s" % error)
    
    def debugPostData(self):
        if DEBUG:
            for i in self.subdict:
                print i, self.subdict[i]
    def Login(self):
        self.goLogin()
    def Publish(self):
        try:
            self.Login()
        except Exception, e:
            print traceback.format_exc() 
            self.returnStr = str(e) 
    def uploadImages(self, ifiles):
        ###########################################
        fields = [
                ('MAX_FILE_SIZE', '5242880')
                ]
        self.imagesdata = []
        for ifile in ifiles:
            imgdata = file(ifile, "rb")
            files = [
                   ('file', imgdata.name, imgdata.read())
                   ]
            content_type, upload_data = self.uploadfile(fields, files)
            
            uploadheader = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 5.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
                    'Content-Type': content_type,
                    'Content-Length': str(len(upload_data))
                    }
            request = urllib2.Request("http://image.ganji.com/upload.php", upload_data, uploadheader)
            js = self.br.open(request).read()
            #print js
            #json.dumps()
            jsondict = json.loads(js)
            if jsondict["error"] == 0:
                imgid = "tmp%s" % ("%s" % time.time()).replace(".", "%s" % random.randint(0, 9))
                imgsdict = {}
                imgdict = {}
                imgdict["image"] = jsondict["info"][0]["url"]
                imgdict["thumb_image"] = jsondict["info"][0]["thumbUrl"]
                imgdict["row_id"] = ""
                imgdict["is_new"] = True
                imgdict["id"] = imgid
                imgsdict[imgid] = imgdict
                self.imagesdata.append(imgsdict)  
    def getUsername(self):
        req = urllib2.Request("http://sh.ganji.com/vip/", None, self.header)
        
        rr = self.br.open(req).read()
        print regx_data("<a href=\"/vip/\">(.*?)</a>", rr, "no")
    def publish(self, type, ifiles):
        types = {
               "zufang":"http://sh.ganji.com/common/pub.php?category=housing&type=1",
               "chushou":"http://sh.ganji.com/common/pub.php?category=housing&type=5",
               }   
        pay_type = {
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
        
        response = self.br.open(request).read()
        self.saveCookie()
        self.imagesdata = []
        self.uploadImages(ifiles)      
                
        ####################################################
        self.imagesdata.append({})
        publishdoct_rent = {
                     "title":"文慧明圆插件租",
                     "xiaoqu":"徐汇馨苑",
                     "district_id":"1,徐汇",
                     "street_id":"24,上海南站",
                     "xiaoqu_address":"南宁路501弄",
                     "agent":"0",
                     "rent_mode":"1", #1 整租,2合租
                     "huxing_shi":"1",
                     "huxing_ting":"1",
                     "huxing_wei":"1",
                     "area":"30",
                     "price":"500",
                     "pay_type_int":"1",
                     "description":"慧明圆插件出租文慧明圆插件插件出租",
                     "phone":"13425478568",
                     "person":"周先生",
                     "images":json.dumps(self.imagesdata) == "[{}]" and  "" or json.dumps(self.imagesdata) ,
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
        publishdoct_sell = {
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
                     "images":json.dumps(self.imagesdata) == "[{}]" and  "" or json.dumps(self.imagesdata) ,
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
        publishheader = {
               "User-Agent":"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB6.6; .NET CLR 3.5.30729)",
               "Referer":types[type],
               'Content-Type': content_type,
               'Content-Length': str(len(params))
               }
        request = urllib2.Request("http://sh.ganji.com/common/pub.php?category=housing&type=5", params, publishheader)
        res = self.br.open(request).read()
        if "发布成功啦！" in res:
            url = regx_data("您的帖子“<a href=\"(.*?)\">", res, "")
            print url
        else:
            print "error"
    def uploadfile(self, fields, files):
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
    def getSID(self):
        Y = int(time.strftime('%Y', time.localtime()))
        M = int(time.strftime('%m', time.localtime()))
        D = int(time.strftime('%d', time.localtime()))
        s = datetime.datetime(Y, M, D, 0, 0, 0)
        sidtime = int(time.mktime(s.timetuple()))
        sidtime = int(time.time() - sidtime) * 1000 * 1000 + random.randint(1000, 9999)
        return str(sidtime)
    def getGanji_uuid(self):
        k = int("%s" % ("%s" % time.time()).replace(".", "%s" % random.randint(0, 9)))
        m = random.randint(10000000, 99999999)
        lp = "%s%s" % (k, random.randint(1, 9))
        o = len(lp)
        print o
        p = [];
        while o > 0:
            o = o - 1
            p.append(lp[o:o + 1])
        n = "".join(p)
        return "%s%s" % ((int(n) + m) , m)
        
def Reg(p):
    try:
        br = browser(p)
        br.goRegPage()        
        br.goReg()
        #return sts  
    except Exception, e:
        print traceback.format_exc() 
        return str(e)      
def Login(p):
    try:
        br = browser(p)
        br.goLogin() 
        #return sts  
    except Exception, e:
        print traceback.format_exc() 
        return str(e)        

def Publish(p):
    try:
        br = browser(p)
        br.goLogin()
        br.getUsername()
        br.publish("chushou", ["c:\\111.jpg"]) 
    except Exception, e:
        print traceback.format_exc() 
        return str(e) 
"""      
        sid = cookielib.Cookie(version=0, name='_gl_tracker', value=self.getSID(), port=None, port_specified=False, domain='ganji.com', domain_specified=False, domain_initial_dot=False, path='/', path_specified=True, secure=False, expires=None, discard=True, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False)
        self.cj.set_cookie(sid)
        citydomain = cookielib.Cookie(version=0, name='citydomain', value="anshan", port=None, port_specified=False, domain='ganji.com', domain_specified=False, domain_initial_dot=False, path='/', path_specified=True, secure=False, expires=None, discard=True, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False)
        self.cj.set_cookie(citydomain)
        ganji_uuid = cookielib.Cookie(version=0, name='ganji_uuid', value=self.getGanji_uuid(), port=None, port_specified=False, domain='ganji.com', domain_specified=False, domain_initial_dot=False, path='/', path_specified=True, secure=False, expires=None, discard=True, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False)
        self.cj.set_cookie(ganji_uuid)
        ganji_uuid_bak2 = cookielib.Cookie(version=0, name='ganji_uuid_bak2', value="2", port=None, port_specified=False, domain='ganji.com', domain_specified=False, domain_initial_dot=False, path='/', path_specified=True, secure=False, expires=None, discard=True, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False)
        self.cj.set_cookie(ganji_uuid_bak2)
        
        request = urllib2.Request("http://anshan.ganji.com/common/pub.php?category=housing&type=3",params , publishheader)
        br = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj),urllib2.HTTPRedirectHandler())
    #    request.add_data(params)
        response=br.open(request).read()
        print response
"""
"""

注册网址：    http://sh.ganji.com/user/register.php
username   4-20个字符（汉字、字母、数字、下划线
password   6-12个字符
password2  重复密码
email      ''
checkcode  ''


http://sh.ganji.com/user/ajax/checkUserName.php
username=""
{"error":1,"message":"\u6b64\u7528\u6237\u540d\u5df2\u88ab\u6ce8\u518c\uff0c\u8bf7\u53e6\u6362\u4e00\u4e2a\u3002"}

#http://sh.ganji.com/common/checkcode.php?nocache=1319860137     
#<label for="yzm">验证码：</label>
http://sh.ganji.com/ajax/check_code_v5.php
checkcode=""
{"error":1,"message":"\u9a8c\u8bc1\u7801\u4e0d\u6b63\u786e\u3002"}


login

source=passport&username=jjj223456us1&password=112233&expireDays=365&setcookie=365&next=
"""

if __name__ == "__main__":
    reg = {
       "username":"jjj22us1",
       "password":"112233",
       "password2":"112233",
       "next":"http%3A%2F%2Fsh.ganji.com%2F",
       "second":"",
       "email":"",
       "checkcode":"",
       "affirm":"on"
    }
    login = {
       "source":"passport",
       "username":"housemain",
       "password":"112233",
       "expireDays":"365",
       "setcookie":"365",
       "next":""
    }
    p = {}
    p['reg'] = reg
    p['login'] = login
    p['publish'] = ""
    p['citycode'] = "sh"
    DEBUG = 1
    Publish(p)
    #Reg(p)
    #Login(p)
    
    
