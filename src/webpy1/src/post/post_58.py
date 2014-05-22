#!/usr/bin/env python
#-*- coding:utf-8 -*-
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2,urllib,sys,time
import cookielib,mechanize
import re
DEBUG =0
reload(sys) 
sys.setdefaultencoding('utf8') #@UndefinedVariable

register_openers()

headers = {'User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14',
           'Accept': 'text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5',
           'Accept-Language':'zh-cn,zh;q=0.5',
           'Accept-Charset':'gb2312,utf-8;q=0.7,*;q=0.7',
           'Keep-Alive':'300',
           'Connection':'keep-alive'}

#datagen11, headers = multipart_encode({"fileUploadInput": open("/home/myapp/Screenshot-1.jpg","rb"),"backFunction": "$.c.Uploader.finish"})

class httpPost():
    data = {}
    def __init__(self):
        
        self.cookie = cookielib.CookieJar()        
        httpsHandler = urllib2.HTTPHandler()        
        httpsHandler.set_http_debuglevel(DEBUG)        
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie),httpsHandler)        
        
        
    def login1(self):
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
        login['method'] = self.data['method']
        login['name'] = self.data['name']
        login['pwd'] = self.data['pwd']
        loginUrl = self.data['loginUrl']+'?'+urllib.urlencode(login)
        print loginUrl
        response = mechanize.urlopen("http://esf.soufun.com/")
        response = mechanize.urlopen(loginUrl)
        print response.read().decode('gb2312')
        
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
    
#postData = {}
#postData['loginUrl'] = 'http://agent.anjuke.com/v2/login/'
#postData['act'] = 'login'
#postData['loginName'] = 'junyue_liuhua'
#postData['loginPasswd'] = 'lh_131415'
#http = httpPost(postData)
#http.login()
