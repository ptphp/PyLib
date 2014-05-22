#!/usr/bin/env python
#-*- coding:utf-8 -*-
from poster.encode import multipart_encode#@UnresolvedImport
from poster.streaminghttp import register_openers #@UnresolvedImport
import urllib2,urllib,sys,time
import cookielib,mechanize#@UnresolvedImport
import re
DEBUG =0
reload(sys) 
sys.setdefaultencoding('utf8') #@UndefinedVariable

headers = {'User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14',
           'Accept': 'text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5',
           'Accept-Language':'zh-cn,zh;q=0.5',
           'Accept-Charset':'gb2312,utf-8;q=0.7,*;q=0.7',
           'Keep-Alive':'300',
           'Connection':'keep-alive'}

register_openers()

def select(data):
    if data['w_b'] == '8':
        postData={}
        postData['uname'] = data['sUserName']
        postData['upass'] = data['sUserPass']
        postData['typeid'] = 0
        postData['cityid'] = 1
        postData['email'] = ''
        http = httpPost58()
        res = http.login(postData)
    elif data['w_b'] == '7':
        postData={}
        postData['username']    = data['sUserName']
        postData['password'] = data['sUserPass']
        postData['next']     = ''
        postData['setcookie']     = '365'        
        print postData
        print 'ganji'
        http = httpPostGJ()
        res = http.login_m(postData)
    elif data['w_b'] == '4':
        postData={}
        postData['loginName']    = data['sUserName']
        postData['loginPasswd'] = data['sUserPass']
        postData['act']     = 'login'
        postData['history']     = ''
        
        print postData
        http = httpPostAJ()
        res = http.login_m(postData)
    elif data['w_b'] == '5':
        postData={}
        postData['user.password']    = data['sUserPass']
        postData['user.username']    = data['sUserName']
        postData['forward_url']      = 'http://www.koubei.com/'
        postData['from']             = 'http://www.koubei.com/'
        postData['redirectUrl']      = 'http://www.koubei.com/'
        postData['fromAtFlag']       = ''
        postData['hold']             = 1        
        print postData
        http = httpPostKB()
        res = http.login(postData)
    elif data['w_b'] == '6':
        postData={}
        postData['name']    = data['sUserName']
        postData['pwd']     = data['sUserPass']
        postData['method']             = 'login'      
        http = httpPostSF()
        res = http.login_m(postData)       
    else:
        res = 'loginerror'
    print res
    return res


class httpPost58():
    data = {}
    def __init__(self):
        
        self.cookie = cookielib.CookieJar()        
        httpsHandler = urllib2.HTTPHandler()        
        httpsHandler.set_http_debuglevel(DEBUG)        
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie),httpsHandler)       
        
    def login(self,loginData):        
        loginUrl = "http://post.58.com/ajax/?action=userreglogin"        
        req = urllib2.Request(loginUrl,urllib.urlencode(loginData),headers)
        r = self.opener.open(req).read()
        #print r.read()
        res = 'loginerror'
        for item in self.cookie:
            print item.name,item.value
        if r == "{result:'1', error:''}":
           res = 'ok'
        return res
        #aQQ_ajklastuser junyue_liuhua
        #print self.opener.open('http://my.anjuke.com/v2/user/broker/checked/').read()
        #open('login.txt','w').write(r.read().encode('utf-8'))
        
    def post(self):
        pass

class httpPostGJ():
    data = {}
    def __init__(self):
        
        self.cookie = cookielib.CookieJar()        
        httpsHandler = urllib2.HTTPHandler()        
        httpsHandler.set_http_debuglevel(DEBUG)        
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie),httpsHandler)       
    def login_m(self,loginData):
        self.data = loginData     
        self.brow = mechanize.Browser()
        
        httpHandler = mechanize.HTTPHandler()
        httpsHandler = mechanize.HTTPSHandler()
        
        httpHandler.set_http_debuglevel(DEBUG)
        self.cookiejar = mechanize.LWPCookieJar()
        #self.cookiejar = "Cookie    lzstat_uv=34741959842666604402|1786789; Hm_lvt_976797cb85805d626fc5642aa5244ba0=1304534271541; ASPSESSIONIDQCDRAQBB=JHCHINLAHGMAIGBIFMNANLGF; lzstat_ss=2189193215_2_1304564199_1786789; Hm_lpvt_976797cb85805d626fc5642aa5244ba0=1304535401191"
        self.opener = mechanize.OpenerFactory(mechanize.SeekableResponseOpener).build_opener(
                                        httpHandler,httpsHandler,
                                        mechanize.HTTPCookieProcessor(self.cookiejar),
                                        mechanize.HTTPRefererProcessor,
                                        mechanize.HTTPEquivProcessor,
                                        mechanize.HTTPRefreshProcessor,
                                        )
        self.opener.addheaders = [("User-Agent","Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.2.13) Gecko/20101203 Firefox/3.6.13"),
                             ("From", "")]
        #self.opener.addheaders = [(
         #                     "Referer", self.data['postUrl']
        #                      )]
        login={}
        loginUrl = "http://bj.ganji.com/user/login.php"   
        print loginUrl
        response = self.brow.open(loginUrl)
        r = self.brow.open(loginUrl,urllib.urlencode(loginData))
        html = r.read()
        res = 'loginerror'
        if html.find('login_success') !=-1:
            res = 'ok'
        return res
        
    def login(self,loginData): 
         
        loginUrl = "http://bj.ganji.com/user/login.php"        
        req = urllib2.Request(loginUrl,urllib.urlencode(loginData),headers)
        r = self.opener.open(req).read()
        print r
        res = 'loginerror'
        for item in self.cookie:
            print item.name,item.value
        
        return res
        #aQQ_ajklastuser junyue_liuhua
        #print self.opener.open('http://my.anjuke.com/v2/user/broker/checked/').read()
        #open('login.txt','w').write(r.read().encode('utf-8'))
        
    def post(self):
        pass
class httpPostAJ():
    data = {}
    def __init__(self):
        
        self.cookie = cookielib.CookieJar()        
        httpsHandler = urllib2.HTTPHandler()        
        httpsHandler.set_http_debuglevel(DEBUG)        
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie),httpsHandler)       
    def login_m(self,loginData):
        self.data = loginData     
        self.brow = mechanize.Browser()
        
        httpHandler = mechanize.HTTPHandler()
        httpsHandler = mechanize.HTTPSHandler()
        
        httpHandler.set_http_debuglevel(DEBUG)
        self.cookiejar = mechanize.LWPCookieJar()
        #self.cookiejar = "Cookie    lzstat_uv=34741959842666604402|1786789; Hm_lvt_976797cb85805d626fc5642aa5244ba0=1304534271541; ASPSESSIONIDQCDRAQBB=JHCHINLAHGMAIGBIFMNANLGF; lzstat_ss=2189193215_2_1304564199_1786789; Hm_lpvt_976797cb85805d626fc5642aa5244ba0=1304535401191"
        self.opener = mechanize.OpenerFactory(mechanize.SeekableResponseOpener).build_opener(
                                        httpHandler,httpsHandler,
                                        mechanize.HTTPCookieProcessor(self.cookiejar),
                                        mechanize.HTTPRefererProcessor,
                                        mechanize.HTTPEquivProcessor,
                                        mechanize.HTTPRefreshProcessor,
                                        )
        self.opener.addheaders = [("User-Agent","Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.2.13) Gecko/20101203 Firefox/3.6.13"),
                             ("From", "")]
        #self.opener.addheaders = [(
         #                     "Referer", self.data['postUrl']
        #                      )]
        login={}
        loginUrl = "http://agent.anjuke.com/v2/login/"   
        print loginUrl
        print urllib.urlencode(loginData)
        #response = self.opener.open(loginUrl)
        r = self.opener.open(loginUrl,urllib.urlencode(loginData))
        html = r.read()
        print self.opener.open('http://my.anjuke.com/v2/user/broker/checked/').read()
        
        res = 'loginerror'
        for item in self.cookiejar:
            print item.name,item.value
            if item.name == 'aQQ_ajkauthinfos':
                if item.value != None:
                    res = 'ok'
        return res
        
    def login(self,loginData): 
         
        loginUrl = "http://bj.ganji.com/user/login.php"        
        req = urllib2.Request(loginUrl,urllib.urlencode(loginData),headers)
        r = self.opener.open(req).read()
        print r
        res = 'loginerror'
        for item in self.cookie:
            print item.name,item.value
        
        return res
        #aQQ_ajklastuser junyue_liuhua
        #print self.opener.open('http://my.anjuke.com/v2/user/broker/checked/').read()
        #open('login.txt','w').write(r.read().encode('utf-8'))
        
    def post(self):
        pass
    
class httpPostKB():
    data = {}
    def __init__(self):
        
        self.cookie = cookielib.CookieJar()        
        httpsHandler = urllib2.HTTPHandler()        
        httpsHandler.set_http_debuglevel(DEBUG)        
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie),httpsHandler)       
    def login_m(self,loginData):
        self.data = loginData     
        self.brow = mechanize.Browser()
        
        httpHandler = mechanize.HTTPHandler()
        httpsHandler = mechanize.HTTPSHandler()
        
        httpHandler.set_http_debuglevel(DEBUG)
        self.cookiejar = mechanize.LWPCookieJar()
        #self.cookiejar = "Cookie    lzstat_uv=34741959842666604402|1786789; Hm_lvt_976797cb85805d626fc5642aa5244ba0=1304534271541; ASPSESSIONIDQCDRAQBB=JHCHINLAHGMAIGBIFMNANLGF; lzstat_ss=2189193215_2_1304564199_1786789; Hm_lpvt_976797cb85805d626fc5642aa5244ba0=1304535401191"
        self.opener = mechanize.OpenerFactory(mechanize.SeekableResponseOpener).build_opener(
                                        httpHandler,httpsHandler,
                                        mechanize.HTTPCookieProcessor(self.cookiejar),
                                        mechanize.HTTPRefererProcessor,
                                        mechanize.HTTPEquivProcessor,
                                        mechanize.HTTPRefreshProcessor,
                                        )
        self.opener.addheaders = [("User-Agent","Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.2.13) Gecko/20101203 Firefox/3.6.13"),
                             ("From", "")]
        #self.opener.addheaders = [(
         #                     "Referer", self.data['postUrl']
        #                      )]
        login={}
        loginUrl = "http://agent.anjuke.com/v2/login/"   
        print loginUrl
        print urllib.urlencode(loginData)
        #response = self.opener.open(loginUrl)
        r = self.opener.open(loginUrl,urllib.urlencode(loginData))
        html = r.read()
        print self.opener.open('http://my.anjuke.com/v2/user/broker/checked/').read()
        
        res = 'loginerror'
        for item in self.cookiejar:
            print item.name,item.value
            if item.name == 'aQQ_ajkauthinfos':
                if item.value != None:
                    res = 'ok'
        return res
        
    def login(self,loginData): 
         
        loginUrl = "http://login.koubei.com/member/login.html"        
        req = urllib2.Request(loginUrl,urllib.urlencode(loginData),headers)
        r = self.opener.open(req).read()
        res = 'loginerror'
        for item in self.cookie:
            print item.name,item.value
            if item.name == 'LogonName':
                if item.value != None:
                    res = 'ok'
        
        return res
        #aQQ_ajklastuser junyue_liuhua
        #print self.opener.open('http://my.anjuke.com/v2/user/broker/checked/').read()
        #open('login.txt','w').write(r.read().encode('utf-8'))
        
    def post(self):
        pass
class httpPostSF():
    data = {}
    def __init__(self):
        
        self.cookie = cookielib.CookieJar()        
        httpsHandler = urllib2.HTTPHandler()        
        httpsHandler.set_http_debuglevel(DEBUG)        
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie),httpsHandler)       
    def login_m(self,loginData):
        self.data = loginData     
        self.brow = mechanize.Browser()
        
        httpHandler = mechanize.HTTPHandler()
        httpsHandler = mechanize.HTTPSHandler()
        
        httpHandler.set_http_debuglevel(DEBUG)
        self.cookiejar = mechanize.LWPCookieJar()
        #self.cookiejar = "Cookie    lzstat_uv=34741959842666604402|1786789; Hm_lvt_976797cb85805d626fc5642aa5244ba0=1304534271541; ASPSESSIONIDQCDRAQBB=JHCHINLAHGMAIGBIFMNANLGF; lzstat_ss=2189193215_2_1304564199_1786789; Hm_lpvt_976797cb85805d626fc5642aa5244ba0=1304535401191"
        self.opener = mechanize.OpenerFactory(mechanize.SeekableResponseOpener).build_opener(
                                        httpHandler,httpsHandler,
                                        mechanize.HTTPCookieProcessor(self.cookiejar),
                                        mechanize.HTTPRefererProcessor,
                                        mechanize.HTTPEquivProcessor,
                                        mechanize.HTTPRefreshProcessor,
                                        )
        self.opener.addheaders = [("User-Agent","Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.2.13) Gecko/20101203 Firefox/3.6.13"),
                             ("From", "")]
        #self.opener.addheaders = [(
         #                     "Referer", self.data['postUrl']
        #                      )]
        login={}
        loginUrl = 'http://esf.soufun.com/newsecond/include/DefaultUserLoginNew.aspx?'    
        response = self.opener.open("http://esf.soufun.com/")
        r        = self.opener.open(loginUrl+urllib.urlencode(loginData))
        html = r.read()
        r1 = self.opener.open("http://agent0.soufun.com/magent/main.aspx").read()
        print r1.decode('gb2312')
        print html.decode('gb2312')
        res = 'loginerror'
        for item in self.cookiejar:
            #print item.name,item.value
            if item.name == 'new_loginname':
                if item.value != None:
                    res = 'ok'
        return res
        
    def login(self,loginData): 

        loginUrl = 'http://esf.soufun.com/newsecond/include/DefaultUserLoginNew.aspx'       
        req = urllib2.Request(loginUrl,urllib.urlencode(loginData),headers)
        r = self.opener.open(req).read()
        
        res = 'loginerror'
        for item in self.cookie:
            #print item.name,item.value
            if item.name == 'LogonName':
                if item.value != None:
                    res = 'ok'
        
        return res
        #aQQ_ajklastuser junyue_liuhua
        #print self.opener.open('http://my.anjuke.com/v2/user/broker/checked/').read()
        #open('login.txt','w').write(r.read().encode('utf-8'))
        
    def post(self):
        pass