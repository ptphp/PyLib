#!user/bin/env python
# -*- coding: utf8 -*- 
'''
Created on Jul 16, 2012

@author: joseph
'''
import urllib2
import cookielib

class HttpClient():
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.cookieFile  = "cookie.txt"
        
        self.cookieJar   = cookielib.MozillaCookieJar(self.cookieFile)
        
        try:
            self.cookieJar.load(ignore_discard = None, ignore_expires= None)
        except Exception as what:
            print what
            self.cookieJar.save(ignore_discard = None, ignore_expires= None)
        
        httpHandler = urllib2.HTTPHandler(debuglevel =1)
        cookieHandler = urllib2.HTTPCookieProcessor(self.cookieJar)
        
        opener = urllib2.build_opener(httpHandler,cookieHandler)
        urllib2.install_opener(opener)
        
    def saveCookie(self):        
        print self.cookieJar    
        for c in self.cookieJar:
            print "%s is : %s" % (c.name,c.value)    
        self.cookieJar.save(ignore_discard = None, ignore_expires= None)
        
        return self.cookieJar
    def getXsrf(self,url):
        urllib2.urlopen(url)
        cookie = self.saveCookie()
        xsrf = ''
        for c in cookie:
            if c.name == '_xsrf':
                _xsrf = c.value
        return _xsrf
        
        