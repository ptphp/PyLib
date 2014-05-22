#!user/bin/env python
# -*- coding: utf8 -*- 
'''
Created on Jul 11, 2012

@author: joseph
'''
import urllib,urllib2
from http_client import HttpClient
import urllib,urllib2,hashlib,mimetypes

def uploadfile(fields, files):
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




class Pin():
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
        signup_url = "http://localhost/uploader/file/"
        xsrf = self.http.getXsrf(signup_url)
        print xsrf
        
        bData['_xsrf']       = xsrf
        
        bQuery = urllib.urlencode(bData)
        url = "http://localhost/ajax/addboard/"
        req = urllib2.Request(url,bQuery)
        res = urllib2.urlopen(req)
        print res.read()
        
    def uploadFile(self):        
        signup_url = "http://localhost/uploader/file/"
        xsrf = self.http.getXsrf(signup_url)
        print xsrf        
        
        fields=[
            ('_xsrf',xsrf)
            ]
        
        ifile = "/home/sites/lihuashu.com/test/1.gif"
        
        imgdata= file(ifile,"rb")
        files=[
                ('ifile',imgdata.name,imgdata.read())
            ]
        
        content_type, upload_data = uploadfile(fields, files)
                
        uploadheader={
                        'Content-Type': content_type,
                        'Content-Length': str(len(upload_data))
                        }
        request = urllib2.Request("http://localhost/upload/", upload_data, uploadheader)
        res = urllib2.urlopen(request)
        print res.read(100)
        print self.http.cookieJar
        for c in self.http.cookieJar:
            if c.name == '_xsrf':
                self._xsrf = c.value
                print c.value
            if c.name == 'pic_url':
                self.pic_url = c.value
                print c.value
            if c.name == 'thumb_url':
                self.thumb_url = c.value
                print c.value
            if c.name == 'board':
                self.board = c.value
                print c.value
        
    def addPin(self):        
        print self._xsrf
        
        url = 'http://localhost/service/form/'
        pData = {}
        pData['board']       = self.board
        pData['thumb_url']   = self.thumb_url
        pData['pic_url']     = self.pic_url
        pData['content']     = 'content'
        pData['_xsrf']       = self._xsrf
        
        req = urllib2.Request(url, urllib.urlencode(pData))
        r = urllib2.urlopen(req)
        
        #print r.read(100)
        
        
#http://localhost/uploader/file/

if __name__ == '__main__':
    email = "fangtee@qq.com"
    pwd   = "111111"
    p = Pin()
    loginData = {}
    loginData['email']      = email
    loginData['password']   = pwd
    loginData['next'] = ""
    p.login(loginData)
    
    p.uploadFile() 
    #p.addPin()
    