#coding:utf-8
import sys
from pprint import pprint
#import xml.etree.cElementTree as ElementTree
from PySide import QtCore
from PySide import QtGui
from PySide import QtWebKit
from PySide import QtNetwork
 
class MyWebView(QtWebKit.QWebView):
    def createWindow(self, p):
        pprint(p)
 
    def link_clicked(self, url):
        pprint(url)
 
class Mainwin(QtGui.QMainWindow):
     
    def __init__(self, title = "Test"):
        super(Mainwin, self).__init__()
        self.setWindowTitle(title)
 
        splitter = self.splitter = QtGui.QSplitter(self)
 
        stacker = self.stacker = QtGui.QStackedWidget(self)
 
        self.view = MyWebView(stacker)
        tw = self.tw = QtGui.QTreeWidget(self)
 
        splitter.addWidget(tw)
        splitter.addWidget(stacker)
         
        self.setCentralWidget(splitter)
        stacker.addWidget(self.view)
         
        self.view2 = MyWebView(stacker)
        stacker.addWidget(self.view2)
 
        self.menubar = self.createMenus()
        self.setMenuBar(self.menubar)
 
        self.locationEdit = QtGui.QLineEdit(self)
        self.locationEdit.setSizePolicy(QtGui.QSizePolicy.Expanding,
            self.locationEdit.sizePolicy().verticalPolicy())
        self.locationEdit.returnPressed.connect(self.onChangeLocation)
 
        self.createToolbar()
 
        self.statusbar = self.createStatusBar()
        self.setStatusBar(self.statusbar)
        self.view.loadProgress.connect(self.statusbar.progress.setValue)
 
        self.view.linkClicked.connect(self.change_location_to)
        self.view.urlChanged.connect(self.adjustLocation)
 
        self.view.page().linkHovered.connect(self.onLinkHovered)
        self.view2.page().linkHovered.connect(self.onLinkHovered)
         
        #self.view.loadFinished.connect(self.pageLoaded)
        #self.view2.loadFinished.connect(self.pageLoaded)
        self.layout()
 
    def createMenus(self):
        mb = QtGui.QMenuBar()
        fm = mb.addMenu("&File")
        act_open = fm.addAction("&Open")
        act_load = fm.addAction("&Load")
        act_exit = fm.addAction("E&xit")
        act_open.triggered.connect(self.OnOpenFile)
        act_load.triggered.connect(self.OnLoadUrl)
        act_exit.triggered.connect(self.close)
        act_exit.setShortcut("Ctrl+Q")
         
        viewMenu = mb.addMenu("&View")
        self.act_xml = act_viewXml = QtGui.QAction(
            self.style().standardIcon(
                        QtGui.QStyle.SP_DirOpenIcon),
                                               "View Xml", self)
        act_viewXml.triggered.connect(self.printDocument)
        viewMenu.addAction(act_viewXml)
 
        menu_ctl = mb.addMenu("&Ctrl")
        act_hide_show = menu_ctl.addAction("&Show hidden window")
        act_hide_show.setCheckable(True)
        #act_hide_show.setChecked(True)
        act_hide_show.toggled.connect(self.onShowView2)
 
        edit = mb.addMenu("&Edit")
        act_back = edit.addAction("&Back")
        act_back.triggered.connect(self.view.back)
        act_forward = edit.addAction("&Forward")
        act_forward.triggered.connect(self.view.forward)
        hl = mb.addMenu("&Help")
        self.act_help = hl.addAction("&About Qt")
        return mb
     
    def createToolbar(self):
        toolBar = self.addToolBar("Navigation")
        toolBar.addAction(self.view.pageAction(QtWebKit.QWebPage.Back))
        toolBar.addAction(self.view.pageAction(QtWebKit.QWebPage.Forward))
        toolBar.addAction(self.view.pageAction(QtWebKit.QWebPage.Reload))
        toolBar.addAction(self.view.pageAction(QtWebKit.QWebPage.Stop))
        act_link = QtGui.QAction(
            self.style().standardIcon(
                        QtGui.QStyle.SP_DirLinkIcon),
                        "Load", self
        )
        act_link.triggered.connect(self.onLoadHome)
        toolBar.addAction(act_link)
        toolBar.addAction(self.act_xml)
        toolBar.addWidget(self.locationEdit)
     
    def createStatusBar(self):
        sb = QtGui.QStatusBar()
        sb.progress = QtGui.QProgressBar()
        sb.addPermanentWidget(sb.progress)
        return sb
 
    def printDocument(self):
        document = self.view.page().mainFrame().documentElement()
        if not document.isNull():
            h3_tag = document.find
       
    def loopElement(self, element, level = 0):
        e = element.firstChild()
        while not e.isNull():
            print '  ' * level, e.localName()
            self.loopElement(e, level+1)
            e = e.nextSibling()
 
    def pageLoaded(self):
        document = self.view2.page().mainFrame().documentElement()
        print document.tagName()
        self.loopElement(document)
     
    def adjustLocation(self):
        self.locationEdit.setText(self.view.url().toString())
 
    def change_location_to(self, location):
        self.view.load(location)
        self.view.setFocus()
 
    def onLoadHome(self):
        self.view.load("http://localhost:8999/")
 
    def onChangeLocation(self):
        url = QtCore.QUrl.fromUserInput(self.locationEdit.text())
        self.view.load(url)
        self.view2.load(url)
        self.view.setFocus()
 
    def onShowView2(self, p):
        if p:
            self.stacker.setCurrentIndex(1)
        else:
            self.stacker.setCurrentIndex(0)
 
    def onLinkHovered(self, p):
        if p:
            self.statusbar.showMessage(p, 0)
        else:
            self.statusbar.showMessage(p)
 
    def OnLoadUrl(self):
        self.view.load("http://localhost:8999")
 
    def OnOpenFile(self):
        t = QtGui.QFileDialog.getOpenFileName(self, "Open file dialog", "/", "All files(*.*)")
        if t[0] != "":
            print "you selected", t[0]
 
 
def main():
    app = QtGui.QApplication(sys.argv)
    mw = Mainwin("Test title")
    mw.show()
 
    QtNetwork.QNetworkProxyFactory.setUseSystemConfiguration(True)
 
    mw.act_help.triggered.connect(app.aboutQt)
    app.exec_()
 
if __name__ == '__main__':
    main()