#!user/bin/env python
# -*- coding: utf8 -*- 
'''
Created on Jul 11, 2012

@author: joseph
'''
from http_client import HttpClient

import urllib,urllib2,hashlib

class Cat():
    def __init__(self):
        self.http = HttpClient()        
        
    def add(self,catData):
        cat_url = "http://localhost/manager/cat/new/"
        xsrf = self.http.getXsrf(cat_url)
        print xsrf
        catData['_xsrf']      = xsrf
        
        catQuery = urllib.urlencode(catData)
        #print regQuery
        req = urllib2.Request(cat_url,catQuery)
        res = urllib2.urlopen(req)
        
        print res.read(20)
        self.http.saveCookie()      
        
    def delete(self,user_key):
                
        url = "http://localhost/manager/user/delete/%s" % user_key
        res = urllib2.urlopen(url)
        print res.code

if __name__ == '__main__':
    cat = Cat()
    catData = {}
    catData['name'] = "home"
    catData['urlname'] = "home"
    catData['title'] = "home"
    catData['description'] = "home"
    catData['group'] = 1
    catData['order'] = 1
    
    cat.add(catData)    
    