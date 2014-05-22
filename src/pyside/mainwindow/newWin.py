#coding:utf-8
'''
Created on Sep 24, 2012

@author: joseph
'''
from PySide import QtGui, QtCore

class Window(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        menu = self.menuBar().addMenu(self.tr('View'))
        action = menu.addAction(self.tr('New Window'))
        action.triggered.connect(self.handleNewWindow)

    def handleNewWindow(self):
        window = QtGui.QMainWindow(self)
        window.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        window.setWindowTitle(self.tr('New Window'))
        window.show()
        # or, alternatively
        # self.window = QtGui.QMainWindow()
        # self.window.setWindowTitle(self.tr('New Window'))
        # self.window.show()

if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.resize(300, 300)
    window.show()
    sys.exit(app.exec_())