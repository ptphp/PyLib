#!/usr/bin/env python
# -*- coding=utf-8 -*-
import sys
import os

from PySide import QtGui,QtCore,QtWebKit

import re



class MyWebView(QtWebKit.QWebView):    

    def __init__(self,stacker):
        super(MyWebView,self).__init__() 
        #https://deptinfo-ensip.univ-poitiers.fr/ENS/pyside-docs/PySide/QtWebKit/QWebSettings.html
        settings = QtWebKit.QWebSettings.globalSettings()
        
        self.settings().setAttribute(QtWebKit.QWebSettings.WebAttribute.DeveloperExtrasEnabled, True)
        self.settings().setAttribute(QtWebKit.QWebSettings.LocalStorageEnabled, True)
        self.settings().setAttribute(QtWebKit.QWebSettings.LocalStorageDatabaseEnabled, True)
        self.settings().setFontSize(QtWebKit.QWebSettings.DefaultFontSize,12)
        # or globally:
        # QWebSettings.globalSettings().setAttribute(
        #     QWebSettings.WebAttribute.DeveloperExtrasEnabled, True)
        self.inspect = QtWebKit.QWebInspector()
        self.inspect.setPage(self.page())


class MainWindow(QtGui.QMainWindow):
   

    def __init__(self):
        super(MainWindow,self).__init__()        
  
        self.setPtMetaData()
        self.setPtWidget()

        self.loadUrl("http://www.doudou.com/",self.webview)    
        self.addPtSignals()
        
    
        
    def setPtMetaData(self):
        self.icon = QtGui.QIcon()
        #icon_path = "res/title.png"
        
        self.setMinimumSize(400,240)
        #self.resize(600,700)
        self.setGeometry(10, 30, 800, 400)
 
    def setPtWidget(self):   
        stacker = self.stacker = QtGui.QStackedWidget(self)
        self.widget = QtGui.QWidget()
        layout = QtGui.QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)   
        layout.addWidget(stacker)  
        self.widget.setLayout(layout)        
        #self.setCentralWidget(stacker)   
        self.setCentralWidget(self.widget) 
        self.webview  = MyWebView(stacker)
        stacker.addWidget(self.webview)    
        #layout.addWidget(self.webview.inspect)        
        self.mainframe =  self.webview.page().mainFrame()
        self.debugview  = MyWebView(stacker)
        stacker.addWidget(self.debugview)
        self.stacker.setCurrentIndex(0)

    def addPtSignals(self):        
        QtCore.QObject.connect(self.webview,QtCore.SIGNAL("urlChanged (const QUrl&)"), self.urlChanged)
        QtCore.QObject.connect(self.webview,QtCore.SIGNAL("loadProgress (int)"), self.loadProgress)
    def loadProgress(self,load):
        print load
        if load == 100:
          
            js = """
            try{
                $();
            }catch(e){
                getJquery();
            }
            
            function getJquery(){
                var tag = document.createElement('script');
                var head = document.getElementsByTagName("head")[0] || document.documentElement;
                
                tag.src = "http://code.jquery.com/jquery-1.8.3.js";
                tag.type = 'text/javascript';
                tag.setAttribute('charset', "utf-8");
                var script = head.insertBefore(tag, head.lastChild)
                //console.log(tag,head)
                if (window.ActiveXObject) {
                        script.onreadystatechange = function () {
                            if (this.readyState === "loaded" || this.readyState === "complete") {
                                callback();
                            }
                        }
                    } else {
                        script.onload = function () {
                            if (!this.readyState) {
                                console.log("load jquery finished!");
                                $("img").each(function(){
                                console.log(this.src);
                                });
                                $("body *").hover(function(){
                                    console.log($(this).attr("class"),$(this).css("backgroundImage"));
                                    
                                });
                            }
                        }
                    }
            }
            console.log("load jquery finished!");
                                $("img").each(function(){
                                console.log(this.src);
                                });
                                $("body *").hover(function(){
                                    console.log($(this).attr("class"),$(this).css("backgroundImage"));
                                    
                                });
           
            """
            print js         
            self.mainframe.evaluateJavaScript(js)
    def urlChanged(self,url):
        self.url =url.toString()
        print self.url
        js = """
        
       
        """
        #print js         
        self.mainframe.evaluateJavaScript(js)

   
    def loadUrl(self,url,webview):      
        self.currenturl = QtCore.QUrl(url)        
        webview.setUrl(self.currenturl)           
    
     
    def closeEvent(self, event):
        #claer thread      
        pass



def main():
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()    
    window.show()
    sys.exit(app.exec_())
    
if __name__ =="__main__":
    main()
    