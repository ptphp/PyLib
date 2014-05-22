# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fangtee.ui'
#
# Created: Thu Oct 20 19:45:56 2011
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
        Form.resize(1341, 800)
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.gridLayout_2 = QtGui.QGridLayout(Form)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label = QtGui.QLabel(Form)
        self.label.setText(QtGui.QApplication.translate("Form", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.webFormGroupBox = QtGui.QGroupBox(Form)
        self.webFormGroupBox.setTitle(QtGui.QApplication.translate("Form", "dddd", None, QtGui.QApplication.UnicodeUTF8))
        self.webFormGroupBox.setObjectName(_fromUtf8("webFormGroupBox"))
        self.gridLayout = QtGui.QGridLayout(self.webFormGroupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.webView = QtWebKit.QWebView(self.webFormGroupBox)
        self.webView.setMinimumSize(QtCore.QSize(200, 150))
        self.webView.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.webView.setObjectName(_fromUtf8("webView"))
        self.gridLayout.addWidget(self.webView, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.webFormGroupBox, 1, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        pass

from PyQt4 import QtWebKit
