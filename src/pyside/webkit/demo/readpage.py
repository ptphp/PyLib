'''
Created on 2013-1-26

@author: Joseph
'''
#coding:utf8
 
import sys
from PySide import QtCore
from PySide import QtGui
from PySide import QtWebKit
from PySide import QtNetwork
from pprint import pprint

class Mainwin(QtGui.QMainWindow):
    def __init__(self, parent= None):
        super(Mainwin, self).__init__( parent)
        
        QtNetwork.QNetworkProxyFactory.setUseSystemConfiguration(True)
        
        splitter = self.splitter = QtGui.QSplitter(self)
        
        self.view = QtWebKit.QWebView(splitter)
        self.view.load("about:blank")
        self.view.loadStarted.connect(self.adjustLocation)
        self.view.titleChanged.connect(self.adjustTitle)
        self.view.loadProgress.connect(self.setProgress)
        self.view.loadFinished.connect(self.adjustLocation)

        self.locationEdit = QtGui.QLineEdit(self)
        self.locationEdit.setSizePolicy(QtGui.QSizePolicy.Expanding,
                self.locationEdit.sizePolicy().verticalPolicy())
        self.locationEdit.returnPressed.connect(self.changeLocation)

        toolBar = self.addToolBar("Navigation")
        toolBar.addAction(self.view.pageAction(QtWebKit.QWebPage.Back))
        toolBar.addAction(self.view.pageAction(QtWebKit.QWebPage.Forward))
        toolBar.addAction(self.view.pageAction(QtWebKit.QWebPage.Reload))
        toolBar.addAction(self.view.pageAction(QtWebKit.QWebPage.Stop))
        act = QtGui.QAction(self)
        toolBar.addAction(act)
        act.triggered.connect(self.loadPage)
        toolBar.addWidget(self.locationEdit)

        viewMenu = self.menuBar().addMenu("&View")
        viewSourceAction = QtGui.QAction("Page Source", self)
        viewSourceAction.triggered.connect(self.viewSource)
        viewMenu.addAction(viewSourceAction)
        
#        listview =  QtGui.QListView()
#        splitter.addWidget(listview)
#        treeview =  QtGui.QTreeView()
#        splitter.addWidget(treeview)
        textedit =  QtGui.QTextEdit()
        splitter.addWidget(textedit)

        splitter.addWidget(self.view)
        
        self.setCentralWidget(splitter)
        
        sb = self.createStatusbar()
        self.setStatusBar(sb)
        page = self.view.page()
        page.linkHovered.connect(self.linkHovered)
        #act.connect(sb.showMessage)
    
    def loadPage(self):
        self.view.load("http://localhost")
    
    def linkHovered(self, p):
        sb = self.statusBar()
        sb.showMessage(p)
        
    def viewSource(self):
        accessManager = self.view.page().networkAccessManager()
        request = QtNetwork.QNetworkRequest(self.view.url())
        reply = accessManager.get(request)
        reply.finished.connect(self.slotSourceDownloaded)
    
    def slotSourceDownloaded(self):
        reply = self.sender()
        self.textEdit = QtGui.QTextEdit(None)
        self.textEdit.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.textEdit.show()
        self.textEdit.setPlainText(QtCore.QTextStream(reply).readAll())
        self.textEdit.resize(600, 400)
        reply.deleteLater()
        
    def createStatusbar(self):
        sb = self.statusBar()
        sb.progress = QtGui.QProgressBar()
        sb.addPermanentWidget(sb.progress)
        return sb

    def adjustTitle(self):
        self.setWindowTitle(self.view.title())
            
    def adjustLocation(self):
        self.locationEdit.setText(self.view.url().toString())
    
    def changeLocation(self):
        url = QtCore.QUrl.fromUserInput(self.locationEdit.text())
        self.view.load(url)
        self.view.setFocus()
    
    def setProgress(self, progress):
        self.statusBar().progress.setValue(progress)
        
        
def main():
    app = QtGui.QApplication(sys.argv)
    mw = Mainwin()
    mw.show()
    app.exec_()
    
    
if __name__ == "__main__":
    main()