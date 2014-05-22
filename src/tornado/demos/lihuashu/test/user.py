#!user/bin/env python
# -*- coding: utf8 -*- 
'''
Created on Jul 11, 2012

@author: joseph
'''
from http_client import HttpClient
import urllib,urllib2,hashlib

class User():
    def __init__(self):
        self.http = HttpClient()        
        
    def login(self,loginData):
        signup_url = "http://localhost/signup/"
        xsrf = self.http.getXsrf(signup_url)
        print xsrf
        loginData['_xsrf']      = xsrf
        
        regQuery = urllib.urlencode(loginData)
        #print regQuery
        url = "http://localhost/login/"
        print url
        req = urllib2.Request(url,regQuery)
        res = urllib2.urlopen(req)
        print res.read(20)
        self.http.saveCookie()
    
    def reg(self,regData):
        signup_url = "http://localhost/signup/"
        xsrf = self.http.getXsrf(signup_url)
        print xsrf
        regData['_xsrf']      = xsrf
        regQuery = urllib.urlencode(regData)
        url = "http://localhost/signup/"
        req = urllib2.Request(url,regQuery)
        res = urllib2.urlopen(req)
        print res.read(100)
    
    def delete(self,user_key):
                
        url = "http://localhost/manager/user/delete/%s" % user_key
        res = urllib2.urlopen(url)
        print res.code

if __name__ == '__main__':
    user = User()
    regData = {}
    email = "fangtee@qq.com"
    pwd = "111111"
    regData['email']      = email
    regData['password']   = pwd
    regData['repassword'] = pwd
    regData['nickname']   = "joseph"
    user.reg(regData)
    
    loginData = {}
    loginData['email']      = email
    loginData['password']   = pwd
    loginData['next'] = ""
    
    user.login(loginData)
    
    #user_key = hashlib.md5(email).hexdigest()
    #print email
    #print user_key
    #user.delete(user_key)
    
    
    
    
