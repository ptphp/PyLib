'''
Created on Jan 23, 2013

@author: joseph
'''
from PySide import QtGui, QtCore, QtWebKit


class Window(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        
        self.view = QtWebKit.QWebView(self)
        self.view.settings().setAttribute(
            QtWebKit.QWebSettings.WebAttribute.DeveloperExtrasEnabled, True)
        self.inspector = QtWebKit.QWebInspector(self)
        self.inspector.setPage(self.view.page())
        print self.inspector.page().mainFrame().url()
        self.inspector.show()
        
        self.inspector.setFont(QtGui.QFont('SIMYOU', 12))
        
        self.splitter = QtGui.QSplitter(self)
        self.splitter.addWidget(self.view)
        self.splitter.addWidget(self.inspector)
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.splitter)
        QtGui.QShortcut(QtGui.QKeySequence('F7'), self,
            self.handleShowInspector)
        
    def handleShowInspector(self):
        print self.inspector.children()
        self.inspector.setShown(self.inspector.isHidden())

if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    window = Window()
  
    #window.view.load(QtCore.QUrl(''))
    window.show()
    sys.exit(app.exec_())