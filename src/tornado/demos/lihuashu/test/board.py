#!user/bin/env python
# -*- coding: utf8 -*- 
'''
Created on Jul 11, 2012

@author: joseph
'''
import urllib,urllib2
from http_client import HttpClient
import urllib,urllib2,hashlib

class Board():
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
        
    def new(self,bData):        
        signup_url = "http://localhost/"
        xsrf = self.http.getXsrf(signup_url)
        print xsrf               
        bData['_xsrf']       = xsrf
        
        bQuery = urllib.urlencode(bData)
        url = "http://localhost/ajax/addboard/"
        req = urllib2.Request(url,bQuery)
        res = urllib2.urlopen(req)
        print res.read()
    def newBoard(self,bData):        
        signup_url = "http://localhost/"
        xsrf = self.http.getXsrf(signup_url)
        print xsrf               
        bData['_xsrf']       = xsrf
        
        bQuery = urllib.urlencode(bData)
        url = "http://localhost/manager/board/new/"
        req = urllib2.Request(url,bQuery)
        res = urllib2.urlopen(req)
        print res.read()
 
        
def login(b):
    email = "fangtee@qq.com"
    pwd   = "111111"
    loginData = {}
    loginData['email']      = email
    loginData['password']   = pwd
    loginData['next'] = ""
    b.login(loginData)
def newBoard(b):
    bData = {}
    bData['title']       = "flowers11"
    bData['category']    = "d63560f2d18711e19b68000c291fd5c0" 
    bData['user']        = "51e09ca8d18811e196ee000c291fd5c0"     
    b.newBoard(bData)    

if __name__ == '__main__':    
    b = Board()
    login(b)
    newBoard(b)
    