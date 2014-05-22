# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'formextractor.ui'
#
# Created: Mon Oct 17 01:30:29 2011
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(1103, 823)
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.gridLayout_2 = QtGui.QGridLayout(Form)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.webFormGroupBox = QtGui.QGroupBox(Form)
        self.webFormGroupBox.setTitle(QtGui.QApplication.translate("Form", "Web", None, QtGui.QApplication.UnicodeUTF8))
        self.webFormGroupBox.setObjectName(_fromUtf8("webFormGroupBox"))
        self.gridLayout = QtGui.QGridLayout(self.webFormGroupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.webView = QtWebKit.QWebView(self.webFormGroupBox)
        self.webView.setMinimumSize(QtCore.QSize(200, 150))
        self.webView.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.webView.setObjectName(_fromUtf8("webView"))
        self.gridLayout.addWidget(self.webView, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.webFormGroupBox, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        pass

from PyQt4 import QtWebKit
