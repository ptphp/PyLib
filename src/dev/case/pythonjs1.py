#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2011-7-27

@author: dholer
'''
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from PyQt4.QtWebKit import QWebView
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import *

class BrowserScreen(QWebView):
    def __init__(self):
        QWebView.__init__(self)
        self.createTrayIcon()
        self.resize(400, 200)
        
        self.setHtml("""
           <script>
               function message() 
               {
                   return "jsClicked!"; 
                }
           </script>
           <h1>QtWebKit + Python sample program</h1>
           <input type="button" value="Click JavaScript!"
                  onClick="alert('[javascript] ' + message())"/>
           <input type="button" value="Click int!"
                  onClick="alert('[python] ' +
                                        python.message(5))"/>
           <input type="button" value="Click string!"
                  onClick="alert('[python] ' +
                                        python.message1('55','1f'))"/>
           <br />
        """)
        self.show()
        self.trayIcon.show()

    def createTrayIcon(self):
        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setIcon(QIcon("d:/111.jpg"))

    def showMessage(self, msg):
        self.trayIcon.showMessage("This is Python1",msg,QSystemTrayIcon.MessageIcon(0), 15 * 1000)

class PythonJS(QObject):
    __pyqtSignals__ = ("contentChanged(const QString &)")
    @pyqtSlot("QString")
    def alert(self, msg):
        self.emit(SIGNAL('contentChanged(const QString &)'), msg)

    @pyqtSlot("int", result="QString")
    def message(self,m):
        print m*10
        return str(m*10)

    @pyqtSlot("QString","QString", result="QString")
    def message1(self,m,n):
        m= int(m)*5
        print n,m
        return str(n)

if __name__=='__main__':
    import sys
    app = QApplication(sys.argv)
    browser = BrowserScreen()
    pjs = PythonJS()
    browser.page().mainFrame().addToJavaScriptWindowObject("python", pjs)
    QObject.connect(pjs, SIGNAL("contentChanged(const QString &)"),browser.showMessage)
    sys.exit(app.exec_())