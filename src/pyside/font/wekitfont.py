# -*- coding: utf-8 -*-
#!/usr/bin/env python
css = u"""

body
{
font-family:"YaHei Consolas Hybrid";
}
#test1
{
font-family:"hello";  
}

#test2
{
font-family:"Times New Roman";
}

#test3
{
font-family:"";
}
#test4
{
font-family:"YaHei Consolas Hybrid";
}
"""
html = u"""
<html>
<head>
<body>

<p id='test1'>hello</p> <!-- does not fallback to default font specified -->
<p id='test2'>hello</p>  <!-- Works !! -->
<p id='test3'>hello d d d的的的的</p> <!-- Works !! fallbacks to default font -->
<p id='test4'>hello 的的的</p>
<p >hello 的的的</p> <!-- Works !! fallbacks to default font -->

</body>
</html>
"""

from PySide import QtCore, QtGui,QtWebKit
import base64

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.webview = QtWebKit.QWebView(self)
        self.webview.settings().setAttribute(
            QtWebKit.QWebSettings.WebAttribute.DeveloperExtrasEnabled, True)
        
        encodeStr = base64.encodestring(css)
        self.webview.settings().setUserStyleSheetUrl("data:text/css;charset=utf-8;base64,%s==" % encodeStr)
        self.inspector = QtWebKit.QWebInspector()
        self.webview.setHtml(html)
        #self.webview.load(QtCore.QUrl("http://localhost:8999/ptwebos/ide/?path=D:\Dhole\Workspace/netcafe"))
        self.inspector.setPage(self.webview.page())
        self.inspector.show()
        self.setCentralWidget(self.webview)
        self.createActions()
        self.createMenus()

        self.setWindowTitle("Dock Widgets")
    def createActions(self):
        self.fontAct = QtGui.QAction("&Font", self,
                statusTip="Set Font",
                triggered=self.font)

    def createMenus(self):
        self.menuBar().addSeparator()
        self.helpMenu = self.menuBar().addMenu("&Font")
        self.helpMenu.addAction(self.fontAct)
        
    def font(self):
        font, ok = QtGui.QFontDialog.getFont()
        if ok:
            self.webview.setFont(font)

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
