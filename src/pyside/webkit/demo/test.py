'''
Created on Jan 23, 2013

@author: joseph
'''
from PySide import QtGui, QtCore, QtWebKit


class Window(QtWebKit.QWebView):
    def __init__(self):
        QtWebKit.QWebView.__init__(self)
        


if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    window = Window()
  
    window.load(QtCore.QUrl('https://127.0.0.1/CloudAdmin/'))
    window.show()
    sys.exit(app.exec_())