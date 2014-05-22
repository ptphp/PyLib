#!/usr/bin/env python
#coding:utf-8

from PyQt4 import QtCore, QtGui, QtNetwork, QtWebKit
import subprocess
import webbrowser
import os
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.progress = 0      
        QtNetwork.QNetworkProxyFactory.setUseSystemConfiguration(True)
        self.resize(320, 485)
        self.homeurl = QtCore.QUrl("file:///D:/Dholer/home/project4JAVA/webkit/assets/www/index.html")
        self.view = QtWebKit.QWebView(self)
        self.view.load(self.homeurl)
        #self.view.setHtml(HTML)
        self.view.page().mainFrame().javaScriptWindowObjectCleared.connect(self.populateJavaScriptWindowObject)
        #self.view.loadFinished.connect(self.adjustLocation)
        self.view.titleChanged.connect(self.adjustTitle)
        self.view.loadProgress.connect(self.setProgress)
        self.view.loadFinished.connect(self.finishLoading)

        #self.locationEdit = QtGui.QLineEdit(self)
        #self.locationEdit.setSizePolicy(QtGui.QSizePolicy.Expanding,
        #        self.locationEdit.sizePolicy().verticalPolicy())
        #self.locationEdit.returnPressed.connect(self.changeLocation)

        #toolBar = self.addToolBar("Navigation")
        #homeAction = QtGui.QAction("Home",self)
        #toolBar.addAction(homeAction)
        #toolBar.addAction(self.view.pageAction(QtWebKit.QWebPage.Back))
        #toolBar.addAction(self.view.pageAction(QtWebKit.QWebPage.Forward))
        #toolBar.addAction(self.view.pageAction(QtWebKit.QWebPage.Reload))
        #toolBar.addAction(self.view.pageAction(QtWebKit.QWebPage.Stop))
        #toolBar.addWidget(self.locationEdit)
        #homeAction.triggered.connect(self.homeGo)
        
        
       
        QtCore.QMetaObject.connectSlotsByName(self)
        self.setCentralWidget(self.view)
        self.setUnifiedTitleAndToolBarOnMac(True)
    def pathRoot(self):
        import os
        os.system("start D:\\Dholer\\")
        #subprocess.Popen("start D:\\Dholer\\")
    def homeGo(self):
        self.view.load(self.homeurl)
    def modMysqlConf(self):
        subprocess.Popen("D:\\Dholer\\bin\\vi.exe D:\\Dholer\\local\\MySQL\\my.ini")
    
    @QtCore.pyqtSlot("QString")
    def goUrl(self, url):
        webbrowser.open_new(url) 
    @QtCore.pyqtSlot("QString", "QString")
    def ServHandler(self, flag, argv):      
        cmd = ""
        if flag == "Apache":
            if argv == "1":
                cmd = "D:\\Dholer\\local\\Apache\\bin\\httpd.exe -k start"   
            elif argv == "2":
                cmd = "D:\\Dholer\\local\\Apache\\bin\\httpd.exe -k stop" 
            elif argv == "3":
                cmd = "D:\\Dholer\\local\\Apache\\bin\\httpd.exe -k install" 
            elif argv == "4":
                cmd = "D:\\Dholer\\local\\Apache\\bin\\httpd.exe -k uninstall" 
        elif flag == "MySQL":
            if argv == "1":
                cmd = "net start mysql"
            elif argv == "2":
                cmd = "net stop mysql"
            elif argv == "3":
                cmd = "D:\\Dholer\\local\\MySQL\\bin\\mysqld --install msyql --defaults-file=D:\\Dholer\\local\\MySQL\\my.ini"   
            else:
                cmd = "D:\\Dholer\\local\\MySQL\\bin\\mysqladmin -u root shutdow"
        elif flag == "Memcached":
            if argv == "1":
                cmd = "D:\\Dholer\\local\\Memcached\\memcached.exe -d start"
            elif argv == "2":
                cmd = "D:\\Dholer\\local\\Memcached\\memcached.exe -d stop"
            elif argv == "3":
                cmd = "D:\\Dholer\\local\\Memcached\\memcached.exe -d install"
            else:
                cmd = "D:\\Dholer\\local\\Memcached\\memcached.exe -d uninstall"
        print flag, argv, cmd        
        subprocess.Popen(
            cmd
            )
        
        self.view.page().mainFrame().evaluateJavaScript("""        
            returnStatus("%s","%s","%s")
        """ % (flag, argv, cmd))
    @QtCore.pyqtSlot("QString")
    def FileHandler(self, flag):
        cmd = ""
        if flag == "101":
            cmd = "D:\\Dholer\\bin\\vi.exe D:\\Dholer\\local\\Apache\\conf\\httpd.conf"
        elif flag == "102":
            cmd = "D:\\Dholer\\bin\\vi.exe D:\\Dholer\\local\\Apache\\conf\\extra\\httpd-vhosts.conf"
        elif flag == "103":
            cmd = "D:\\Dholer\\bin\\vi.exe D:\\Dholer\\local\\Apache\\logs\\error.log"
        elif flag == "201":
            cmd = "D:\\Dholer\\bin\\vi.exe D:\\Dholer\\local\\MySQL\\my.ini"
        elif flag == "301":
            cmd = "D:\\Dholer\\bin\\vi.exe D:\\Dholer\\local\\PHP\\php.ini"
        print cmd
        subprocess.Popen(cmd)
        
    def populateJavaScriptWindowObject(self):
        self.view.page().mainFrame().addToJavaScriptWindowObject('callApi', self)
    def modApacheConf(self):
        subprocess.Popen("D:\\Dholer\\bin\\vi.exe D:\\Dholer\\local\\Apache\\conf\\httpd.conf")
    def modApacheVhost(self):
        subprocess.Popen("D:\\Dholer\\bin\\vi.exe D:\\Dholer\\local\\Apache\\conf\\extra\\httpd-vhosts.conf")
    def modHosts(self):
        subprocess.Popen("D:\\Dholer\\bin\\vi.exe %WINDIR%\\system32\\drivers\\etc\\hosts")
    def runShell(self):
        #os.system("cd D:\\Dholer\\bin\\")
        subprocess.Popen("D:\\Dholer\\bin\\shell.bat")
    def loadService(self):
        #subprocess.Popen("services.msc")
        os.system("services.msc")
    def viewSource(self):
        accessManager = self.view.page().networkAccessManager()
        request = QtNetwork.QNetworkRequest(self.view.url())
        reply = accessManager.get(request)
        reply.finished.connect(self.slotSourceDownloaded)

    def slotSourceDownloaded(self):
        reply = self.sender()
        self.textEdit = QtGui.QTextEdit(None)
        self.textEdit.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.textEdit.show()
        self.textEdit.setPlainText(QtCore.QTextStream(reply).readAll())
        self.textEdit.resize(600, 400)
        reply.deleteLater()

    def adjustLocation(self):
        self.locationEdit.setText(self.view.url().toString())

    def changeLocation(self):
        url = QtCore.QUrl.fromUserInput(self.locationEdit.text())
        self.view.load(url)
        self.view.setFocus()

    def adjustTitle(self):
        if 0 < self.progress < 100:
            self.setWindowTitle("%s (%s%%)" % (self.view.title(), self.progress))
        else:
            self.setWindowTitle(self.view.title())

    def setProgress(self, p):
        self.progress = p
        self.adjustTitle()

    def finishLoading(self):
        self.progress = 100
        self.adjustTitle()

if __name__ == '__main__':
    import sys    
    app = QtGui.QApplication(sys.argv)    
    browser = MainWindow()
    browser.show()
    sys.exit(app.exec_())
