# -*- coding: utf-8 -*-
#!/usr/bin/env python

from PySide import QtWebKit,QtNetwork,QtCore,QtGui

import json

class PtApi(QtCore.QObject):
    def __init__(self,parent = None):
        super(PtApi,self).__init__(parent)
        
    @QtCore.Slot(str)
    def text(self,msg):
        print msg
    
class NetwordAccMan(QtNetwork.QNetworkAccessManager):
    def __init__(self):   
        QtNetwork.QNetworkAccessManager.__init__(self)
        '''
        def finished (reply)
        def networkAccessibleChanged (accessible)
        def networkSessionConnected ()
        '''
        self.finished.connect(self.finish)
        self.networkAccessibleChanged.connect(self.networkAccessibleChange)
        self.networkSessionConnected.connect(self.networkSessionConnect)    
    
    def createRequest(self, operation, request, data):
        # data contains all the post data that is being added to the request
        # so you can look into it here
        #print "replay:====>",request.url().toString(),operation     
        #print request
        
        request.setAttribute(QtNetwork.QNetworkRequest.CacheLoadControlAttribute, QtNetwork.QNetworkRequest.PreferCache)
        url = request.url().toString()        
        self.replyStart(url)
        reply = QtNetwork.QNetworkAccessManager.createRequest(self, operation,request,data)      
        #if "js" in url or "gif" in url:
            #reply = QNetworkAccessManager.createRequest(self,QNetworkAccessManager.GetOperation,QNetworkRequest(QtCore.QUrl("")))  
            #reply = QNetworkAccessManager.createRequest(self, operation,request,data)        
        #else:                                           
        return reply
    
    def replyStart(self,url):
        self.emit(QtCore.SIGNAL("replyStart(QString)"),url)
        
    def replyFinish(self,url):
        self.emit(QtCore.SIGNAL("replyFinish(QString)"),url) 
    def finish(self,reply):
        fromCache = reply.attribute(QtNetwork.QNetworkRequest.SourceIsFromCacheAttribute)         
        #print("page from cache? %d" % fromCache)        
        url = reply.url().toString()
        self.replyFinish(url)
        #print reply.rawHeaderList()
        #print "*"*20
        for li in reply.request().rawHeaderList():
            pass#print li,reply.request().rawHeader(li) 
        #print "*"*10     
        for re in reply.rawHeaderPairs():
            pass#print re[0],re[1]
        pass#print reply.request()
    def networkAccessibleChange(self,accessible):
        pass#print "accessible",accessible
    def networkSessionConnect(self):
        pass#print "networkSessionConnect"
    
    
class WebPage(QtWebKit.QWebPage):
    def __init__(self):
        QtWebKit.QWebPage.__init__(self)
        self.frame = frame = self.mainFrame()
        frame.javaScriptWindowObjectCleared.connect(self.addJsObj)
        #frame.evaluateJavaScript("alert(\"hello world\")")
        #self.setContentEditable(True)
        nam = NetwordAccMan()
        self.diskCache = QtNetwork.QNetworkDiskCache(self)
        self.diskCache.setCacheDirectory("d:/Dhole/tmp/webkit")
        nam.setCache(self.diskCache)        
        self.setNetworkAccessManager(nam)
        self.linkHovered.connect(self.linkHover)
        self.statusBarMessage.connect(self.statusBarMsg)
        self.loadFinished.connect(self.loadFinish)
        self.loadStarted.connect(self.loadStart)
        self.loadProgress.connect(self.Progress)
        self.selectionChanged.connect(self.selectionChange)
        self.linkClicked.connect(self.linkClick)
        
    def addJsObj(self):
        ptApi = PtApi()
        self.frame.addToJavaScriptWindowObject('ptApi',ptApi)
    def linkClick(self,url):
        pass#print url     
    def selectionChange(self):
        pass#print self.selectedText()
    def Progress(self,progress):
        pass#print progress
    def loadStart(self):
        pass
        #print "start", self.frame.url().toString()
    def loadFinish(self):
        pass#print "finished", self.frame.url().toString()
        #print self.frame.icon()
        #print self.frame.metaData()
        #print self.networkAccessManager().cookieJar().allCookies()
        
    def statusBarMsg(self,msg):
        pass#print "status bar msg",msg
    def linkHover(self,link, title, textContent):
        pass#print link, title, textContent
    def userAgentForUrl(self, url):
        return "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.15 (KHTML, like Gecko) Chrome/24.0.1295.0 Safari/537.15"


 