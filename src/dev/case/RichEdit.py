#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2011-7-27

@author: dholer
这篇是为了做Rss项目而研究WebKit后的副产品，但是它的意义远大于离线Rss阅读

这是另一个RichEdit 并且编辑起来更容易
而且它很容易转换到B/S结构，不管需求是环肥燕瘦都能适应......

估计这是最简单的一种 xml文档、html预览、RichEdit 三位一体的方案了......
'''
import sys,locale
encoding=locale.getdefaultlocale()[1]
from PyQt4 import Qt
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import QtWebKit

html=r'''<html>
<head></head>
<body>
<script>
function onChanged(e,id) { 
var element =document.getElementById(id);
python.onChanged(id,element.textContent); 
}
</script>
<div id="main">
<h1 id="title"" contenteditable="true" onkeyup="onChanged(event,'title')">T1</h1>
<div id='body'>
<p id='body_line1' contenteditable="true" onkeyup="onChanged(event,'body_line1')">123456</p>
<p id='body_line2' contenteditable="true" onkeyup="onChanged(event,'body_line2')">abdcdef</p>
</div>
</div>
<body>
</html>
'''

class PythonJS(QtCore.QObject):
    
    __pyqtSignals__ = ("contentChanged(const QString &,const QString &)")
    
    @QtCore.pyqtSignature("QString,QString")
    def onChanged(self, id,msg):
        self.emit(QtCore.SIGNAL('contentChanged(const QString &,const QString &)'),id, msg)

    @QtCore.pyqtSignature("", result="QString")
    def message(self): 
        return "Message!"


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.update=True
        
        self.tabs=QtGui.QTabWidget(self)
        self.browser=QtWebKit.QWebView(self.tabs)
        self.edit=QtGui.QPlainTextEdit(self.tabs)
        
        self.tabs.addTab(self.browser,'View')
        self.tabs.addTab(self.edit,'Edit')
        self.html=html
        self.edit.setPlainText(self.html)
        
        self.pjs=PythonJS()
        
        self.connect(self.edit,QtCore.SIGNAL('textChanged()'),self.onTextChanged)
        self.connect(self.pjs,QtCore.SIGNAL('contentChanged(const QString &,const QString &)'),self.onJSMessage)
        self.connect(self.browser.page().mainFrame(),QtCore.SIGNAL('javaScriptWindowObjectCleared ()'),self.onObjectClear)
        
        self.browser.setHtml(self.html)
        
    def onJSMessage(self,id,msg):
        
        self.html= self.browser.page().mainFrame ().toHtml()
        #print unicode(self.html).encode(encoding)
        self.setEditText(self.html)
        
    def resizeEvent(self,s):
        size=self.size()
        self.tabs.resize(size)

    def setEditText(self,str,update=False):
        t=self.update
        self.update=update
        self.edit.setPlainText(str)
        self.update=t
        
            
    def onTextChanged(self):
        if self.update:
            self.html= self.edit.toPlainText() 
            self.browser.setHtml(self.html)
            self.browser.page().mainFrame().addToJavaScriptWindowObject('python',self.pjs) 
            self.browser.reload()
            
    def onObjectClear(self):
        self.browser.page().mainFrame().addToJavaScriptWindowObject('python',self.pjs)  
    
if __name__=='__main__':
    app=QtGui.QApplication(sys.argv)
    frame=MainWindow()
    frame.show()
    sys.exit(app.exec_())       