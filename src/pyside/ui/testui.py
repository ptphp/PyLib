#!/usr/bin/env python
# -*- coding=utf-8 -*-
'''
Created on 2013-2-2

@author: Joseph
'''
import sys

from PySide import QtGui
from PySide import QtCore
from loadui import loadUi

class Inputer(QtGui .QDialog):
    def __init__(self):
        super(Inputer, self).__init__()
        loadUi('form.ui', self)
        self.lineEdit.returnPressed.connect(self.input)
    def input(self):
        print self.lineEdit.text()
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    win = Inputer()
    win.show()
    sys.exit(app.exec_())
