# -*- coding: utf-8 -*-
#!/usr/bin/env python
#pyuic4 formextractor.ui > ui_formextractor.py
import sip
import time,random
sip.setapi('QVariant', 2)
import json
from PyQt4 import QtCore, QtGui,QtSql
from PyQt4.QtCore import * 
import sqlModel
from fetch58 import * 
from ui_fangtee import Ui_Form
QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8")) 

_Queue = []
class WorkerSql(QThread): 
    def __init__(self, parent = None):    
        QThread.__init__(self, parent)
        
    def run(self):
        self.sqlObj = sqlModel.Db("fangtee.db")
        while 1:
            time.sleep(0.1)
            if _Queue:                
                row = _Queue.pop()
                sql = parseSql(row)
                #print sql
                self.sqlObj.query(sql,True)
                makePath("pagecach",row['url'])
                self.emit(SIGNAL("updatePage(QString)"),row['title']+str(row['posttime']))

class Worker(QThread):    
    param = {}
    def __init__(self, parent = None):    
        QThread.__init__(self, parent)        
        self.param = {}
        self.stoped = False
        self.suspended = False
        self.mutex = QMutex()
    #def __del__(self):        
        #self.wait()
    def _init(self,param): 
        self.param = param
        self.start()

    def run(self):
        with QMutexLocker(self.mutex):
            self.stoped = False
        while self.suspended:
            self.wait()  
            return
        if self.stoped:
            return            
        cc = BaseCrawl(self.param,_Queue)
        cc.run()            
    def stop(self):
        with QMutexLocker(self.mutex):
            self.stoped = True
            self.suspended = False
            
    def suspend(self):
        with QMutexLocker(self.mutex):
            self.suspended = True
            self.stoped = False
    def isStoped(self):    
        with QMutexLocker(self.mutex):
            return self.stope

class FangWebView(QtGui.QWidget):
    def __init__(self, parent=None):
        self.sqlObj = sqlModel.Db("fangtee.db")
        super(FangWebView, self).__init__(parent)
        
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.l = self.ui.label        
        webView = self.ui.webView
        webView.setUrl(QtCore.QUrl('http://www.fangtee.com/Broker/index.php'))
        webView.page().mainFrame().javaScriptWindowObjectCleared.connect(self.populateJavaScriptWindowObject)
        self.mainFrame = self.ui.webView.page().mainFrame()
        
        
    def updatePage(self,s): 
        self.l.setText(s)
    @QtCore.pyqtSlot()
    def test(self): 
        
        
        param = self.mainFrame.findFirstElement('#param').evaluateJavaScript("this.value")
        paramObj = json.loads(str(param))
        
        print paramObj
        limts = paramObj['page']*10
        sql = parseCondition(paramObj)
        count = self.sqlObj.count(sql['count'])
        print count
        #sql = 'select title,price,room,desc from house limit %d,10' % limts
        self.sqlObj.query(sql['sql'])
        print self.sqlObj.sql
        
        res = self.sqlObj.showAll()
        paramObj['count'] = count
        paramObj['result'] = res;
        result = str(json.dumps(paramObj))

        self.mainFrame.evaluateJavaScript("""
            callbackfunction(%s);                  
        """ % result)
        
    @QtCore.pyqtSlot()
    def tStart(self):
        self.threadArr = []
        data1 = {}
        data1['flag'] = 1
        data1['city'] = 1
        data1['getPhone'] = 1
        data2 = {}
        data2['flag'] = 2
        data2['city'] = 1
        data2['getPhone'] = 1
        data3 = {}
        data3['flag'] = 3
        data3['city'] = 1
        data3['getPhone'] = 1
        data4 = {}
        data4['flag'] = 4
        data4['city'] = 1
        data4['getPhone'] = 1
        data = [data1,
                data2,
                data3,
                data4,
                ]       
        
        for i in range(0,4):            
            self.threadArr.append(Worker())            
            self.threadArr[i]._init(data[i])
        self.tSql = WorkerSql()
        self.connect(self.tSql, SIGNAL("updatePage(QString)"), self.updatePage)
        self.tSql.start()
        
    @QtCore.pyqtSlot()
    def tStop(self):
        self.thread.stoped = True
        self.thread.suspended = False
        
    @QtCore.pyqtSlot()
    def tSuspend(self):
        self.thread.stoped = False
        self.thread.suspended = True
        

    def execJs(self,methodJS):
        self.mainFrame.evaluateJavaScript("""
            %s();                    
        """ % methodJS)
    def populateJavaScriptWindowObject(self):
        self.ui.webView.page().mainFrame().addToJavaScriptWindowObject(
                'callApi', self)


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.createActions()
        self.createMenus()
        webView = self.ui.webView
        webView.setUrl(QtCore.QUrl('http://www.fangtee.com/Broker/index.php'))
        webView.page().mainFrame().javaScriptWindowObjectCleared.connect(
                self.populateJavaScriptWindowObject)

        self.mainFrame = self.webView.page().mainFrame()
        
        
        self.centralWidget = FangWebView(self)
        self.setCentralWidget(self.centralWidget)
        self.setUnifiedTitleAndToolBarOnMac(True)
        self.setWindowTitle(self.tr("房特易"))
        self.resize(1200, 860)
    
    def createActions(self):
        self.exitAct = QtGui.QAction("E&xit", self,
                statusTip="Exit the application",
                shortcut=QtGui.QKeySequence.Quit, triggered=self.close)
        self.aboutAct = QtGui.QAction("&About", self,
                statusTip="Show the application's About box",
                triggered=self.about)

        self.aboutQtAct = QtGui.QAction(self.tr("关于"), self,
                statusTip="Show the Qt library's About box",
                triggered=QtGui.qApp.aboutQt)

    def createMenus(self):
        fileMenu = self.menuBar().addMenu("&File")
        fileMenu.addAction(self.exitAct)
        self.menuBar().addSeparator()
        helpMenu = self.menuBar().addMenu("&Help")
        helpMenu.addAction(self.aboutAct)
        helpMenu.addAction(self.aboutQtAct)

    def about(self):
        QtGui.QMessageBox.about(self, self.tr("这是我们的第一个例子"))


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)    
    QtGui.QApplication.addLibraryPath("C:\\Python27\\Lib\\site-packages\\PyQt4\\plugins")
    mainWindow = MainWindow()    
    mainWindow.show()

    sys.exit(app.exec_())
