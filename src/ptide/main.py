# -*- coding: utf-8 -*-
#!/usr/bin/env python

from PySide import QtCore, QtGui,QtWebKit
from ptpy.pyside.webkit.webview import WebView
from ptpy.dir.tree import listFiles
from ptpy.file.main import getContent
from ptpy.offline.main import download
import json

PREVIEW_URL = "http://dev.game110.cn"

class Editor(QtCore.QObject):
    def __init__(self,parent = None):
        super(Editor,self).__init__(parent)
        self.htmlSrc = ""
        
    @QtCore.Slot(result=str)
    def getHtmlSrc(self):
        return self.htmlSrc
    
    @QtCore.Slot(str,result=str)
    def getFiles(self,path):
        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        files = listFiles(path)      
        QtGui.QApplication.restoreOverrideCursor()           
        return json.dumps(files)
    
    @QtCore.Slot(str,str,result=str)
    def saveContent(self,filename,content):    
        fi = QtCore.QFile(filename)
        if not fi.open(QtCore.QFile.WriteOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(self, "Dock Widgets",
                    "Cannot write file %s:\n%s." % (filename, file.errorString()))
            return

        out = QtCore.QTextStream(fi)
        out.setCodec("UTF-8")
        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        out << content
        QtGui.QApplication.restoreOverrideCursor()    
        return ""
    
    @QtCore.Slot(str,result=str)
    def getContent(self,path):        
        return getContent(path)


class MainWindow(QtGui.QMainWindow):    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.createActions()
        self.createMenus()
        self.setupWebView()        
        #self.createToolBars()       
        self.setWindowTitle("Pt IDE")
        
        sb = self.createStatusbar()
        self.setStatusBar(sb)
        
    def save(self):
        filename, filtr = QtGui.QFileDialog.getSaveFileName(self,
                "Choose a file name", '.', "HTML (*.html *.htm)")
        if not filename:
            return

        fi = QtCore.QFile(filename)
        if not fi.open(QtCore.QFile.WriteOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(self, "Dock Widgets",
                    "Cannot write file %s:\n%s." % (filename, file.errorString()))
            return

        out = QtCore.QTextStream(fi)
        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        out << self.textEdit.toHtml()
        QtGui.QApplication.restoreOverrideCursor()

        self.statusBar().showMessage("Saved '%s'" % filename, 2000)


    def about(self):
        QtGui.QMessageBox.about(self, "About PtIde",
                "The <b>PtIde</b> Vervsion 1.0")
    def font(self):
        font, ok = QtGui.QFontDialog.getFont()
        #print font
        if ok:
            self.webview.setFont(font)
            self.textEdit.setFont(font)
            
    def createActions(self):
        self.quitAct = QtGui.QAction("&Quit", self, shortcut="Ctrl+Q",
                statusTip="Quit the application", triggered=self.close)
        
        self.fontAct = QtGui.QAction("&Font", self,
                statusTip="Set Font",
                triggered=self.font)
        self.aboutAct = QtGui.QAction("&About", self,
                statusTip="Show the application's About box",
                triggered=self.about)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.fontAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.quitAct)

        self.viewMenu = self.menuBar().addMenu("&View")
        self.menuBar().addSeparator()
        self.helpMenu = self.menuBar().addMenu("&Help")
        
        self.helpMenu.addAction(self.aboutAct)
    
    def createToolBars(self):
        #self.fileToolBar = self.addToolBar("File")
        #self.fileToolBar.addAction(self.printAct)

        self.locationEdit = QtGui.QLineEdit(self)
        self.locationEdit.setSizePolicy(QtGui.QSizePolicy.Expanding,
                 self.locationEdit.sizePolicy().verticalPolicy())
        self.locationEdit.returnPressed.connect(self.changeLocation)    
                       
        #self.WebViewBar = self.addToolBar("WebView Bar")
        
        self.WebViewBar.addAction(self.webview.pageAction(QtWebKit.QWebPage.Back))
        self.WebViewBar.addAction(self.webview.pageAction(QtWebKit.QWebPage.Forward))
        self.WebViewBar.addAction(self.webview.pageAction(QtWebKit.QWebPage.Reload))
        self.WebViewBar.addAction(self.webview.pageAction(QtWebKit.QWebPage.Stop))
        
        homveact = QtGui.QAction(self)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/home.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        homveact.setIcon(icon)
        self.WebViewBar.addAction(homveact)
        homveact.triggered.connect(self.loadPage)
        self.WebViewBar.addWidget(self.locationEdit)
        
    #def createStatusBar(self):
    #    self.statusBar().showMessage("Ready")
    
    def createStatusbar(self):
        sb = self.statusBar()
        sb.progress = QtGui.QProgressBar()
        sb.progress.setMaximumHeight(13)
        sb.addPermanentWidget(sb.progress)
        return sb
    def consolePanel(self):
        dock = QtGui.QDockWidget("Console", self)    
        dock.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea | QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        
        self.consoleView = QtWebKit.QWebView()        
        self.consoleView.load("ui/console.html")
        
        dock.setWidget(self.consoleView)        
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, dock)
        self.viewMenu.addAction(dock.toggleViewAction())
        
    def previewPanel(self):
        dock = QtGui.QDockWidget("Preview", self)    
        dock.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea | QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        
        self.webview = WebView(self)
        
        self.connect(self.webview.page().networkAccessManager(),QtCore.SIGNAL("replyStart(QString)"), self.replyStart)
        self.connect(self.webview.page().networkAccessManager(),QtCore.SIGNAL("replyFinish(QString)"), self.replyFinish)
        #self.loadPage()
        self.webview.loadStarted.connect(self.loadStart)
        self.webview.titleChanged.connect(self.adjustTitle)
        self.webview.loadProgress.connect(self.setProgress)
        self.webview.loadFinished.connect(self.adjustLocation)
        self.webview.linkClicked.connect(self.linkclick)
        self.webview.page().javaScriptConsoleMessage = self.consolePrint
        self.locationEdit = QtGui.QLineEdit(self)
        self.locationEdit.setSizePolicy(QtGui.QSizePolicy.Expanding,
                 self.locationEdit.sizePolicy().verticalPolicy())
        self.locationEdit.returnPressed.connect(self.changeLocation)
        
        widget = QtGui.QWidget()
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.locationEdit)
        layout.addWidget(self.webview)
        layout.setSpacing(0)
        layout.setContentsMargins(0,0,0,0)
        widget.setLayout(layout)
        dock.setWidget(widget)        
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, dock)
        self.viewMenu.addAction(dock.toggleViewAction())
        
        self.inspector = inspector = QtWebKit.QWebInspector()
        inspector.setPage(self.webview.page())
        QtGui.QShortcut(QtGui.QKeySequence('F5'), self,self.refreshPrev)
    def setupWebView(self):
        self.editorView = QtWebKit.QWebView()        
        self.editorView.load("ui/index.html")
        self.editorView.page().mainFrame().javaScriptWindowObjectCleared.connect(self.addEditorJsObj)        
        self.previewPanel()
        self.consolePanel()
        self.setCentralWidget(self.editorView)
        
        
    def consolePrint(self,msg,line,id):
        #print msg,line,id
        #print json.dumps(msg)
        self.consoleView.page().mainFrame().evaluateJavaScript("$.console.addConPanel('%s','%s','%s')" % (msg,str(line),id))
    def refreshPrev(self):   
        url = self.webview.url().toString()
        if url == '':
            url = PREVIEW_URL
        self.webview.load(url)
    def addEditorJsObj(self):
        self.editor = editor = Editor()
        self.editorView.page().mainFrame().addToJavaScriptWindowObject("editor",editor)
        
    def setHtmlSrc(self,html):        
        self.editor.htmlSrc = html
        self.editorView.page().mainFrame().evaluateJavaScript("setHtmlSrc()")
        
    def replyStart(self,url):
        #self.editorView.page().mainFrame().evaluateJavaScript(js)
        self.consoleView.page().mainFrame().evaluateJavaScript("$.console.addPanel('%s')" % (url))
        #print "start:++++>",url
    def replyFinish(self,url):
        print "finish:===>",url
        if self.webview.page().networkAccessManager().cache().data(url):            
            download(url,self.webview.page().networkAccessManager().cache().data(url).readAll())
        #print self.webview.page().networkAccessManager().cache().data(url).readAll()
        #print self.webview.page().networkAccessManager().cache().metaData(url).rawHeaders()
        js = "reply('%s')" % url
        #self.editorView.page().mainFrame().evaluateJavaScript(js)
    def loadPage(self):
        self.webview.load("http://www.baidu.com")
    def loadStart(self):
        pass#self.setHtmlSrc("")
        #self.editorView.page().mainFrame().evaluateJavaScript('clearRequest()')
    def linkclick(self,url):
        pass#print url
    def changeLocation(self):
        url = QtCore.QUrl.fromUserInput(self.locationEdit.text())
        self.locationEdit.setText(url.toString())
        self.webview.load(QtCore.QUrl(url))
        self.webview.setFocus()        
    def adjustTitle(self):
        self.statusBar().showMessage(self.webview.title())
        #self.setWindowTitle(self.webview.title())            
    def adjustLocation(self):
        self.locationEdit.setText(self.webview.url().toString())       
        #self.setHtmlSrc(self.webview.page().mainFrame().toHtml())        
    def setProgress(self, progress):
        self.statusBar().progress.setValue(progress)


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.showMaximized()
    sys.exit(app.exec_())
