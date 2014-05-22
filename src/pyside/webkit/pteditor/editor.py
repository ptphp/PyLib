#coding:utf-8
'''
Created on 2013-1-23

@author: Joseph
'''
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtWebKit import *
import ace_rc

HTML = """
<html>
<head>
<style>
html,body{margin:0;padding:0;font-family:'YaHei Consolas Hybrid'}
pre.ace_editor{
font-family:'YaHei Consolas Hybrid'
}
</style>
<script type="text/javascript" src="qrc:/pteditor/ace/src-noconflict/ace.js"></script>
</head>
<body>
<pre id="editor" style="position:absolute;top:0;left:0;right:0;bottom:0">

</pre>
<script type="text/javascript">
var e = ace.edit("editor");
e.setTheme("ace/theme/monokai");
e.getSession().setMode("ace/mode/python");
e.setValue(editor.content());
console.log(editor.content())
</script>
</body>
</html>
"""

class Tabbar(QTabBar):
    def __init__(self,parent = None):
        QTabBar.__init__(self,parent)
        self.setMovable(True)
        self.setTabsClosable(True)

class Editor(QObject):
    def __init__(self,filePath,parent = None):
        super(Editor,self).__init__(parent)
        self.filePath = filePath
        if self.filePath:
            fileInfo =  QFileInfo(self.filePath)
            inFile = QFile(self.filePath)
            if inFile.open(QFile.ReadOnly | QFile.Text):
                text = str(inFile.readAll())    
                print text   
            ab_path =  fileInfo.absoluteFilePath()
            filename = fileInfo.fileName()
            print ab_path
        else:
            filename = "New File"
            text = u"""
def test():
    print 11
#的的大的 
            """
        self.text = text
        self.filename = filename
    @Slot(result=str)
    def content(self):        
        return self.text
        
class PtEditor(QMainWindow):
    def __init__(self, fileName,parent=None):
        QMainWindow.__init__(self, parent)
        self.fileName = fileName
        self.create_main_frame()       

    def create_main_frame(self):        
        self.tabs = tabs = QTabWidget()
        tabs.setTabBar(Tabbar())
        self.addTab()      
        self.setCentralWidget(tabs)
        self.tabs.tabCloseRequested.connect(self.tabRemove)
        
    def tabRemove(self,index):
        self.tabs.removeTab(index)
        
    def showDialog(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.view.setFont(font)
            
    def addTab(self):
        self.view = view = QWebView()
        view.setFont(QFont("YaHei Consolas Hybrid",12))
        view.settings().setAttribute(QWebSettings.WebAttribute.DeveloperExtrasEnabled, True)
        editor = Editor(self.fileName)
        frame = view.page().mainFrame()
        frame.addToJavaScriptWindowObject('editor',editor)
        self.inspect = QWebInspector()
        self.inspect.setPage(view.page())        
        view.setHtml(HTML)
        self.tabs.addTab(view,editor.filename)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    
    if len(sys.argv) >= 2:
        fileName = sys.argv[1]
    else:
        fileName = ""
    editor = PtEditor(fileName)
    editor.showMaximized()
    app.exec_()