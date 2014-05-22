#encoding=gb2312

import sys,time
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.start = QtGui.QPushButton(self.centralWidget)
        self.start.setGeometry(QtCore.QRect(30, 20, 75, 23))
        self.start.setObjectName(_fromUtf8("start"))
        
        self.suspend = QtGui.QPushButton(self.centralWidget)
        self.suspend.setGeometry(QtCore.QRect(120, 20, 75, 23))
        self.suspend.setObjectName(_fromUtf8("suspend"))
        
        
        self.stop = QtGui.QPushButton(self.centralWidget)
        self.stop.setGeometry(QtCore.QRect(210, 20, 75, 23))
        self.stop.setObjectName(_fromUtf8("stop"))
        
        self.memLog = QtGui.QTextEdit(self.centralWidget)
        self.memLog.setGeometry(QtCore.QRect(40, 80, 641, 431))
        self.memLog.setObjectName(_fromUtf8("memLog"))
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.start.setText(QtGui.QApplication.translate("MainWindow", "start", None, QtGui.QApplication.UnicodeUTF8))
        self.suspend.setText(QtGui.QApplication.translate("MainWindow", "suspend", None, QtGui.QApplication.UnicodeUTF8))
        self.stop.setText(QtGui.QApplication.translate("MainWindow", "stop", None, QtGui.QApplication.UnicodeUTF8))
#信用信号和槽来处理日志
class SigalOutLogSender(QObject):
    def SendMsg(self, m):
        self.emit(SIGNAL('DisplayLog(QString)'),m)

aSigalOutLog=SigalOutLogSender()

class OutLog:
    def __init__(self):
        pass
    def write(self, m):
        global aSigalOutLog
        aSigalOutLog.SendMsg(u'%s' % m)

class Timer(QThread): 
    def __init__(self, parent=None):
        super(Timer, self).__init__(parent)
        self.stoped = False
        self.suspended = False
        self.mutex = QMutex()
    
    def run(self):
        with QMutexLocker(self.mutex):
            self.stoped = False
        while True:
            while self.suspended:
                self.wait()  
                return
            if self.stoped:
                return 
            self.emit(SIGNAL("updateTime()"))
            time.sleep(1)
 
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
        
class StartQt4(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.sec = 0
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.timer = Timer()
        self.ui.stop.setEnabled(False)
        self.ui.suspend.setEnabled(False)
        QtCore.QObject.connect(self.ui.start,QtCore.SIGNAL("clicked()"), self.start, 1)
        QtCore.QObject.connect(self.ui.suspend,QtCore.SIGNAL("clicked()"), self.suspend, 1)
        QtCore.QObject.connect(self.ui.stop,QtCore.SIGNAL("clicked()"), self.stop, 1)
        
        #捕捉系统输出        
        sys.stdout = OutLog()
        sys.stderr = OutLog()
        self.connect(self.timer, SIGNAL("updateTime()")
                        , self.updateTime)
        #使用信号和槽来处理日志
        global aSigalOutLog
        QtCore.QObject.connect(aSigalOutLog,QtCore.SIGNAL("DisplayLog(QString)"), self.DisplayLog, 1)
    def start(self):
        self.ui.start.setEnabled(False)
        self.ui.stop.setEnabled(True)
        self.ui.suspend.setEnabled(True)
        self.timer.suspended = False
        self.timer.start()
        
        
    def suspend(self):
        self.ui.start.setEnabled(True)
        self.ui.stop.setEnabled(True)
        self.ui.suspend.setEnabled(False)
        self.timer.suspend()
        self.ui.memLog.moveCursor(QtGui.QTextCursor.NextRow)
        self.ui.memLog.insertPlainText("suspend\n")
    def stop(self):
        self.timer.stop()
        self.ui.stop.setEnabled(False)
        self.ui.start.setEnabled(True)
        self.ui.suspend.setEnabled(False)
        self.ui.memLog.moveCursor(QtGui.QTextCursor.NextRow)
        self.ui.memLog.insertPlainText("stop\n")
        self.sec = 0

    def updateTime(self):
        global aSigalOutLog
        print "Time: %s s" % self.sec
        self.sec += 1
        
    def DisplayLog(self,log):
        self.ui.memLog.moveCursor(QtGui.QTextCursor.End)
        self.ui.memLog.insertPlainText(log)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = StartQt4()
    myapp.show()
    sys.exit(app.exec_())