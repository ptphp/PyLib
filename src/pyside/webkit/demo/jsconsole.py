'''
Created on Jan 22, 2013

@author: joseph
'''
from PySide.QtGui import *
from PySide.QtCore import *
from PySide.QtWebKit import QWebView 

html = """
<html>
<body>
    <h1>Hello!</h1><br>
    <h2><a href="#" onclick="printer.text('Message from QWebView')">QObject Test</a></h2>
    <h2><a href="#" onclick="alert('Javascript works!')">JS test</a></h2>
</body>
</html>
"""

class ConsolePrinter(QObject):
    def __init__(self,parent = None):
        super(ConsolePrinter,self).__init__(parent)
        
    @Slot(str)
    def text(self,msg):
        print msg
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    view = QWebView()
    printer = ConsolePrinter()
    
    frame = view.page().mainFrame()
    frame.addToJavaScriptWindowObject('printer',printer)
    frame.evaluateJavaScript("alert(\"hello world\")")
    frame.evaluateJavaScript("printer.text(2222222222)")
    frame.setHtml(html)
    view.show()
    sys.exit(app.exec_())