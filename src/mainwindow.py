#!/usr/bin/env python
# -*- coding=utf-8 -*-
import sys
import os
import threading
import hashlib
import ConfigParser
import simplejson as json
import subprocess
from PySide import QtGui,QtCore,QtWebKit
from PySide.QtCore import Qt
from ui.titleBar import TitleBar
from ui.webview import MyWebView

from app.utils.service import ClientApi
from app.utils.config import Config
from app.utils.fileIO import File
from app.utils.sqlitedb import SqliteDB
from app.utils.common import getPidByPort,killPidByPort
from app.utils.common import urldecode
from app.utils.path import Path

import re
        
        
class MainWindow(QtGui.QMainWindow):
    config = Config()  
    path   = Path()
    f      = File()
    db     = SqliteDB()

    def __init__(self):
        super(MainWindow,self).__init__()        
        self.startServer()
        self.setPhpApp()
        self.setPtMetaData()
        self.setPtWidget()
        
        self.loadUrl(self.config.ptUrl,self.webview)    
        self.addPtSignals()
        self.addTray()
        self.thread = threading.currentThread()
        self.workers = {}
    
    def startServer(self):
        php = os.path.join(self.config.dir['ptproject'],self.config.path['phpserver'])
        port = int(self.config.setting['port'])
        host = self.config.setting['host']
        public = os.path.join(self.config.dir['ptproject'],self.config.dir['public'])
        ini_file = os.path.join(self.config.dir['ptproject'],self.config.path['phpserver_ini'])
        router_file = os.path.join(self.config.dir['ptproject'],self.config.path['phpserver_router'])
        
        #如果 port 已启用 先KILL
        if getPidByPort(port):
            #print "port has runnint"
            killPidByPort(port)
            
        hostPort = "%s:%d" % (host,port)
        self.config.ptUrl = url = "http://" +hostPort
        cmd ="%s -S %s -c %s -t %s %s" % (php,hostPort,ini_file,public,router_file)        
        subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        
    def setPhpApp(self):
        #设置 Asserts/index.php
        indexContent = self.f.get(os.path.join(self.config.dir['ptproject'],
                                               self.config.dir['ptphp'],
                                               'Asserts','tpl','index_core.php'))
        
        #print indexContent
        path_ptphp_lib = os.path.join(self.config.dir['ptproject'],self.config.dir['ptphp'])
        indexContent = indexContent.replace('#PATH_PTPHP_LIB#',path_ptphp_lib)        
        self.f.set(os.path.join(self.config.dir['ptproject'],self.config.dir['public'],'index.php'),indexContent)
        
    def setPtMetaData(self):
        self.icon = QtGui.QIcon()
        icon_path = os.path.join(self.config.dir['ptgui'],'res','title.png')
        #icon_path = "res/title.png"
        self.icon.addPixmap(QtGui.QPixmap(icon_path),QtGui.QIcon.Normal,QtGui.QIcon.Off)
        self.setWindowIcon(self.icon)
        self.setWindowTitle(self.config.wintitle)
        
        self.setMinimumSize(400,240)
        self.setGeometry(10, 30, 800, 500)
        # 设置窗口标记（无边框|任务栏右键菜单）
        self.setMouseTracking(True)
        #self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowSystemMenuHint)
        #self.showMaximized()
  
    def setPtWidget(self):
        stacker = self.stacker = QtGui.QStackedWidget(self)
        self.widget = QtGui.QWidget()
        m_titleBar = self.m_titleBar= TitleBar(self);
        m_titleBar.setMinimumHeight(20)
        m_titleBar.setMaximumHeight(20)
        layout = QtGui.QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)   
        #layout.addWidget(m_titleBar)  
        layout.addWidget(stacker)  
        
        self.widget.setLayout(layout)        
        #self.setCentralWidget(stacker)   
        self.setCentralWidget(self.widget) 
        self.webview  = MyWebView(stacker)
        
        self.webview.setFont(QtGui.QFont('YaHei.Consolas.1.12.ttf', 12))
        print self.webview.font()
        stacker.addWidget(self.webview)    
        #layout.addWidget(self.webview.inspect)        
        self.mainframe =  self.webview.page().mainFrame()
        self.debugview  = MyWebView(stacker)
        stacker.addWidget(self.debugview)
        self.stacker.setCurrentIndex(0)

    def addTray(self):
        self.isWindow()
        self.trayIcon = QtGui.QSystemTrayIcon(self)
        self.trayIcon.setIcon(self.icon)
        self.trayIcon.show()
        self.trayIcon.activated.connect(self.trayClick)
        self.trayIcon.setToolTip(u"PtProject 开发工具\nv 1.0 ")
        self.trayMenu()
        
    def addPtSignals(self):        
        #self.webview.page().linkHovered.connect(self.onLinkHovered)
        QtCore.QObject.connect(self.webview,QtCore.SIGNAL("urlChanged (const QUrl&)"), self.urlChanged)
        self.mainframe.javaScriptWindowObjectCleared.connect(self.populateJavaScriptWindowObject)
    
   
    def urlChanged(self,url):
        self.url =url.toString()
        print self.url
        js = "var in_ptproject = 1;"            
        self.mainframe.evaluateJavaScript(js)

    def callback(self,msg):
        #print msg
        #print type(msg)
        msg = msg.replace('"','\\"')
        js ='ptApi.setCallbackParam("%s");' % msg       
        self.mainframe.evaluateJavaScript(js)
    def populateJavaScriptWindowObject(self):
        self.clientApi = ClientApi()
        self.mainframe.addToJavaScriptWindowObject('clientApi', self.clientApi)       
        self.connect(self.clientApi,QtCore.SIGNAL("callback(QString)"), self.callback)
        self.connect(self.clientApi,QtCore.SIGNAL("callbackMainWindow(QString)"), self.callbackMainWindow)
        
    def loadUrl(self,url,webview):      
        self.currenturl = QtCore.QUrl(url)        
        webview.setUrl(self.currenturl)           
    
    def callbackMainWindow(self,data):
        #print data
        _data = json.loads(data)        
        method = getattr(self, _data['_function'])
        method(_data['_args'])

    def opentUrl(self,args):
        url = args['url']
        if "http://" not in url:
            url = "http://" + url
        #cmd = "python Browser.py %s" % url
        cmd = r"%s %s" % (self.browser,url)
        subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)  
    
    #def closeEvent(self, *args, **kwargs):  
    def closeEvent(self, event):
        #claer thread      
        for w in self.workers:
            self.workers[w].terminate()
        for w in self.workers:
            self.workers[w].wait()
            
        self.clientApi = None
        os.popen("Taskkill /f /t /im php.exe")        
        #reply = QtGui.QMessageBox.question(self, 'Message',
        #            "Are you sure to quit?", QtGui.QMessageBox.Yes | 
        #            QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        
        #if self.trayIcon.isVisible():
        #    self.showMessage(u"提示信息",u"最小化")
        #    self.hide()
        #    event.ignore()
                
        #if reply == QtGui.QMessageBox.Yes:
        
        #    event.accept()
        #else:
        #    event.ignore()
        event.accept()
        #return QtGui.QMainWindow.closeEvent(self, *args, **kwargs)
    def trayClick(self,reason):
        if reason==QtGui.QSystemTrayIcon.DoubleClick: #双击
            self.showNormal()
        elif reason==QtGui.QSystemTrayIcon.MiddleClick: #中击
            self.showMessage(u"提示信息",u"中击")
        else:
            pass

    def showMessage(self,title,content,icon=QtGui.QSystemTrayIcon.Information):        
        self.trayIcon.showMessage(title,content,icon)

    def trayMenu(self):
        self.minimizeAction = QtGui.QAction(u"最小化", self,triggered=self.hide)
        self.maximizeAction = QtGui.QAction(u"最大化",self,triggered=self.showMaximized)
        self.restoreAction = QtGui.QAction(u"还原", self,triggered=self.showNormal)
        self.quitAction = QtGui.QAction(u"直接退出", self,triggered=QtGui.qApp.quit)
        self.trayIconMenu = QtGui.QMenu(self)
        self.trayIconMenu.addAction(self.minimizeAction)
        self.trayIconMenu.addAction(self.maximizeAction)
        self.trayIconMenu.addAction(self.restoreAction)
        self.trayIconMenu.addSeparator() #间隔线
        self.trayIconMenu.addAction(self.quitAction)
        self.trayIcon.setContextMenu(self.trayIconMenu) #右击托盘 
   
def main():
    config = Config()
    cwd = r"D:\Dhole\PtProject\PtGUI-dev"
    config.setPaths(cwd)
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()    
    #window.show()
    window.showMaximized()
    sys.exit(app.exec_())
    
if __name__ =="__main__":
    main()
    