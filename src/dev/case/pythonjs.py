#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2011-7-27

@author: dholer
'''
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
import PyQt4.QtNetwork
import sys,urllib2


app,browser=None,None

class BrowserScreen(QWebView): 
    '''主窗口'''
    def __init__(self): 
        QWebView.__init__(self) 
        self.resize(800, 600) 
        self.show() 
        self.setHtml(open('pythonjs_test.html').read())
        self.load(QUrl(r'http://www.sohu.com'))
    
    def showMessage(self, msg): 
        print msg


class PythonJS(QObject): 
    '''供JS调用'''
    __pyqtSignals__ = ( "contentChanged(const QString &)" ) 
    
    @pyqtSlot("")
    def close(self):
        sys.exit()
    
    @pyqtSlot("") 
    def openMap(self): 
        return 11
    
if __name__== '__main__' :
    app = QApplication(sys.argv) 
    browser = BrowserScreen() 
    #供js调用的python对象
    pjs = PythonJS() 
    #绑定通信对象
    browser.page().mainFrame().addToJavaScriptWindowObject( "python" , pjs) 
    QObject.connect(pjs , SIGNAL( "contentChanged(const QString &)" ), browser.showMessage) 
    sys.exit(app.exec_())
