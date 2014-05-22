'''
Created on 2011-7-27

@author: dholer

Calling Python from JavaScript in PyQt's QWebkit
QtWebKit makes it very easy to expose methods and properties implemented in Python to JavaScript. 
Qt will automatically expose Qt-slots and Qt-properties to a JavaScript when a QObject is made available 
in the frame's JavaScript context.
https://www.zxproxy.com/browse.php?u=e10eb5d4a2665676f38QnY4aXBVeW1venlqcFRJMFl6V2ZvMnFtcFQ5MFl6QWlvRjhsWlFSalltTmtZMkF1b1RrY296cGdwVXkwblQ5aFlKTWxvMjBnbnpTMkxLQXdwenlqcVAxY292MWpyS1MwcGw1YnFUMWY%3D&b=6&f=norefer
http://pysnippet.blogspot.com/2010/01/calling-python-from-javascript-in-pyqts.html

'''
import sys
from PyQt4 import QtCore, QtGui, QtWebKit

"""Html snippet."""
html = """
<html><body>
  <center>
  <script language="JavaScript">
    document.write('<p>Python ' + pyObj.pyVersion + '</p>')
  </script>
  <button >Press me</button>
  </center>
</body></html>
"""

class StupidClass(QtCore.QObject):
    """Simple class with one slot and one read-only property."""

    @QtCore.pyqtSlot(str)
    def showMessage(self, msg):
        """Open a message box and display the specified message."""
        QtGui.QMessageBox.information(None, "Info", msg)

    def _pyVersion(self):
        """Return the Python version."""
        
        return sys.version

    """Python interpreter version property."""
    pyVersion = QtCore.pyqtProperty(str, fget=_pyVersion)

def main():
    app = QtGui.QApplication(sys.argv)

    myObj = StupidClass()

    webView = QtWebKit.QWebView()
    # Make myObj exposed as JavaScript object named 'pyObj'
    webView.page().mainFrame().addToJavaScriptWindowObject("pyObj", myObj)
    webView.setHtml(html)

    window = QtGui.QMainWindow()
    window.setCentralWidget(webView)
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()