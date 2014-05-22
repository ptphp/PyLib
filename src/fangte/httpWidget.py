# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'httpWidget.ui'
#
# Created: Thu Oct 20 21:47:28 2011
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_HttpWidget(object):
    def setupUi(self, HttpWidget):
        HttpWidget.setObjectName(_fromUtf8("HttpWidget"))
        #HttpWidget.resize(1100, 800)
         
        HttpWidget.setWindowTitle(QtGui.QApplication.translate("HttpWidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.verticalLayout = QtGui.QVBoxLayout(HttpWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        
        
        self.webView = QtWebKit.QWebView(HttpWidget)
        
        #self.webView.setUrl(QtCore.QUrl(_fromUtf8("http://fangtee.sinaapp.com/Broker/")))
        #self.webView.setUrl(QtCore.QUrl(_fromUtf8("http://www.fangtee.com/Broker/index.php")))
		#self.webView.setUrl(QtCore.QUrl(_fromUtf8("http://www.fangtee.com/mobile/index.php")))
        self.webView.setObjectName(_fromUtf8("webView"))
        self.verticalLayout.addWidget(self.webView)

        self.retranslateUi(HttpWidget)
        QtCore.QMetaObject.connectSlotsByName(HttpWidget)
    def resizeMax(self,HttpWidget):
        # 设置窗口标记（无边框）
        HttpWidget.setWindowFlags(QtCore.Qt.FramelessWindowHint)       
         # 得到桌面控件         
        desktop = QtGui.QApplication.desktop()
        rect = desktop.availableGeometry()
        HttpWidget.setGeometry(rect)
    def retranslateUi(self, HttpWidget):
        pass

from PyQt4 import QtWebKit
