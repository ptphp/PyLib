# -*- coding: utf-8 -*-
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys,time

class MainWindow(QMainWindow):
    def __init__(self,parent=None):
        super(MainWindow,self).__init__(parent)
        self.setWindowTitle("Splash Example")
        edit=QTextEdit()
        edit.setText("Splash Example")
        self.setCentralWidget(edit)
        self.resize(600,450)
        QThread.sleep(3)
        
app=QApplication(sys.argv)

splash=QSplashScreen(QPixmap("134bb2dbd20d4ef1cd1166bf.jpg"))
splash.show()
app.processEvents()
window=MainWindow()
window.show()
splash.finish(window)
app.exec_()