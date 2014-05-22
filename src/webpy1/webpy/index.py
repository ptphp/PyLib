#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
import urllib2,urllib
web.config.debug = False
from post import postSite
from post import publish58
from fetch import threadControl
urls = (
        '/check_account', 'check_account',
        '/post_data', 'post_data',
        '/post_data_t', 'post_data_t',
        '/fetch_data', 'fetch_data',
        "/.*", "hello"
        )
app = web.application(urls, globals())

class hello:
    def GET(self):
        return 'good luck!'
class check_account1:
    def GET(self):
        return 'check_account11'
def postDecode(post):
    result={}
    for i in post.split("&"):
        i=i.split("=",1)
        if len(i)==2:
            result[urllib.unquote(i[0])]=urllib.unquote(i[1])
    return result

class check_account:
    def POST(self):
        data = web.data()
        print data
        postData = postDecode(data)  
        try:            
            res = postSite.select(postData)            
        except:
            res = 'codeerror' 
            pass
        return res
    
class post_data:
    def POST(self):
        data = web.data()
        postData = postDecode(data)
        if int(postData['webid']) ==8:
            result = publish58.Publish(postData) 
            
        print result               
        return result
class fetch_data:
    def POST(self):
        
        data = web.data()
        postData = postDecode(data)
        if postData['command']=="run":
            ct=threadControl.CThread("su",'1')
            ct.setDaemon(True)
            ct.start()
        print result               
        return result
    
class test:
    def POST(self,data):        
        res = postSite.select(7)
        print data
        return res
if __name__ == "__main__":
    #web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)
    app.run()