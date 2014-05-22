#coding:utf-8  
import re
import sys
reload(sys)  
sys.setdefaultencoding('utf-8')  
import PyQt4
import signal
from PyQt4 import QtCore, QtGui
from PyQt4 import uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from PyQt4.QtNetwork import *
class Baidu(QtCore.QObject):
  
    def __init__(self):
        QObject.__init__(self)
        #self.page = QWebPage()#如果想看图形窗口的话，注释掉本行，把下三已注释行取消注释即可
        self.webview = QWebView()
        self.page=self.webview.page()
        self.current = "http://qun.qq.com/air/#"
        self.logged = False 
        self.frame = self.page.mainFrame()     
        QtCore.QObject.connect(self.frame,QtCore.SIGNAL('loadFinished(bool)'),self.do_do)   
        self.webview.show()
    def start(self,username,password):
        self.username=username
        self.password=password
        self.frame.load(QUrl(self.current))
    def do_do(self,bool):
        url = self.frame.url()
        print url.toString()
        
        if url.toString() == "http://qun.qq.com/air/#" :
            if self.logged == False:          
                self.do_login()
                self.logged=True
            else:           
                #e = self.frame.findFirstElement("td[id=errortd]")
                if 'url=url.replace(/^/.///gi,"http://passport.baidu.com/");' not in self.frame.toHtml():
                    print 'login failed'
                    sys.exit(1)
        if url.toString() == "http://passport.baidu.com/center" :
            print 'login successed'            
            self.frame.load(QUrl('http://hi.baidu.com/'+self.username+'/ihome/ihomefeed'))
        if url.toString() == "http://hi.baidu.com/"+self.username+"/ihome/ihomefeed":
            self.do_coin()
         
    def do_login(self):
        print 'do login'
        #js_file = open('baidu_login.js','r')
        #js = js_file.read()
        #js_file.close()
        
        #js="frm=document.forms[0];frm.username.value='"+self.username+"';frm.normModPsp.value='"+self.password+"';checkForm(frm);frm.submit();"
        js = "login = window.frames['loginFrameEmbed'].document;login.getElementById('u').value='dhol@qq.com';login.getElementById('p').value='pb200898';return ptui_onLoginEx(login.getElementById('loginform'), 'qq.com');login.getElementById('loginform').submit()"
        print js   
        self.frame.evaluateJavaScript(js)
    
    def do_coin(self):
        print 'do coin'
        #js_file = open('baidu_coin.js','r')
        #js = js_file.read()
        #js_file.close()
        js="if(baidu.g('dumili-get-btn').className=='able'){App.points.savePoints();}"     
        self.frame.evaluateJavaScript(js)
        sys.exit(1)
     
       
if __name__ == "__main__":
    app = QApplication(sys.argv)
    baidu = Baidu()
    baidu.start("dhol@qq.com","pb200898")
    sys.exit(app.exec_())