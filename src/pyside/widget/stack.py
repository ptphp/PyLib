'''
Created on Jan 22, 2013

@author: joseph
'''
import sys
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtWebKit import *

app = QApplication(sys.argv)

# Create a stack with 2 webviews
stack = QStackedWidget()
mapper = QSignalMapper(stack)
mapper.mapped[int].connect(stack.setCurrentIndex)
for i in range(2):
    web = QWebView(stack)
    stack.addWidget(web)
    # When a webview finishes loading, switch to it
    web.loadFinished[bool].connect(mapper.map)
    mapper.setMapping(web, i)

# load the page in the non visible webview
stack.widget(1).load(QUrl("http://www.baidu.com"))
stack.show()

sys.exit(app.exec_())
