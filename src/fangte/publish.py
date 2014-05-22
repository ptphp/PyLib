# -*- coding: utf-8 -*-import re
import sys,re
import PyQt4
from PyQt4 import QtCore, QtGui
from PyQt4 import uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from PyQt4.QtNetwork import *

formclass, baseclass = uic.loadUiType("WebWindow.ui")
class WebBrowser(baseclass,formclass): 
    def __init__(self):
        baseclass.__init__(self)        
        self.setupUi(self)
 
class IEWinApp:
    def __init__(self):
        self.REGEXPS = \
        {
            'cookie':re.compile(r'(?P<cookie_name>\S*?)\s*=\s*(?P<cookie_value>\S*?);', re.I | re.DOTALL)
        }
        cookie_input = "acookie=a; bcookie=b; ccookie=c;"
        self.current = "http://www.fangtee.com/Broker/"
        cookiebase = QNetworkCookie("","")
        self.cookies = cookiebase.parseCookies("")
        
        for cookiename,cookievalue in self.REGEXPS['cookie'].findall(cookie_input):
            cookie_tmp = QNetworkCookie(QByteArray(cookiename),QByteArray(cookievalue))
            self.cookies.append(cookie_tmp)
        
        self.cookiejar = QNetworkCookieJar()
        #self.cookiejar.setCookiesFromUrl(self.cookies, QUrl(self.current))
        self.network_manager = QNetworkAccessManager()
        self.network_manager.setCookieJar(self.cookiejar)
        
        
        
        
        QtCore.QObject.connect(self.network_manager,SIGNAL("finished(QNetworkReply*)"),self.replyFinished)
        #Send the request:
        
        
        
        self.window = WebBrowser()
        self.page = IEWinPage()
        
        agent = "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)1"
        self.page.setUserAgent(agent)
        self.page.setNetworkAccessManager(self.network_manager)   
        #self.postData()     
        self.frame = self.page.mainFrame()
        self.window.webView.setPage(self.page)
        self.frame.load(QUrl(self.current))
        self.window.show()
    def postData(self):
        self.req = QNetworkRequest()
        self.req.setUrl(QUrl(self.current))
        #Configure the parameters for the post request:
        postData = QByteArray()
        postData.append("Login=log_name&")
        #postData.append("test=log_name&")
        postData.append("Password=some_pass")
        self.network_manager.post(self.req, postData)
        
        
    def replyFinished(self,reply):
        print reply.readAll()
        
class IEWinPage(QWebPage):
    def __init__(self):
        QWebPage.__init__(self)
        self.useragent = "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)"
    
    def setUserAgent(self, agent):
        self.useragent = agent
 
    def userAgentForUrl(self, url):
        return QString(QByteArray(self.useragent))
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = IEWinApp()
    sys.exit(app.exec_())