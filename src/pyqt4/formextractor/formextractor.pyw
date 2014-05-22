#!/usr/bin/env python
#pyuic4 formextractor.ui > ui_formextractor.py
import sip
import test

sip.setapi('QVariant', 2)

from PyQt4 import QtCore, QtGui

import formextractor_rc

from ui_formextractor import Ui_Form

class FormExtractor(QtGui.QWidget):
    def __init__(self, parent=None):
        super(FormExtractor, self).__init__(parent)

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        webView = self.ui.webView
        webView.setUrl(QtCore.QUrl('http://www.fangtee.com/index.php/test'))
        webView.page().mainFrame().javaScriptWindowObjectCleared.connect(
                self.populateJavaScriptWindowObject)

        self.resize(1024, 768)
 
    @QtCore.pyqtSlot()
    def submit(self):
        frame = self.ui.webView.page().mainFrame()
        url = frame.findFirstElement('#url')
        s = url.evaluateJavaScript('this.value')
        frame.evaluateJavaScript("""
            $("h1").html("%s");
        """ % test.test(s))
        #self.ui.firstNameEdit.setText(firstName.evaluateJavaScript('this.value'))
        
    def populateJavaScriptWindowObject(self):
        self.ui.webView.page().mainFrame().addToJavaScriptWindowObject(
                'formExtractor', self)


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.createActions()
        self.createMenus()
        self.centralWidget = FormExtractor(self)
        self.setCentralWidget(self.centralWidget)
        self.setUnifiedTitleAndToolBarOnMac(True)
    
    def createActions(self):
        self.exitAct = QtGui.QAction("E&xit", self,
                statusTip="Exit the application",
                shortcut=QtGui.QKeySequence.Quit, triggered=self.close)

        self.aboutAct = QtGui.QAction("&About", self,
                statusTip="Show the application's About box",
                triggered=self.about)

        self.aboutQtAct = QtGui.QAction("About &Qt", self,
                statusTip="Show the Qt library's About box",
                triggered=QtGui.qApp.aboutQt)

    def createMenus(self):
        fileMenu = self.menuBar().addMenu("&File")
        fileMenu.addAction(self.exitAct)
        self.menuBar().addSeparator()
        helpMenu = self.menuBar().addMenu("&Help")
        helpMenu.addAction(self.aboutAct)
        helpMenu.addAction(self.aboutQtAct)

    def about(self):
        QtGui.QMessageBox.about(self, "About Form Extractor",
                "The <b>Form Extractor</b> example demonstrates how to "
                "extract data from a web form using QtWebKit.")


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)

    mainWindow = MainWindow()
    mainWindow.setWindowTitle("Form ")
    mainWindow.resize(1024, 768)
    mainWindow.show()

    sys.exit(app.exec_())
