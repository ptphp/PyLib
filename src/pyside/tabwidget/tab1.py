'''
Created on 2013-1-23

@author: Joseph
'''
from PySide.QtCore import *
from PySide.QtGui import *

class Tabbar(QTabBar):
    def __init__(self,parent = None):
        QTabBar.__init__(self,parent)
        self.setMovable(True)
        self.setTabsClosable(True)


class AppForm(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.create_main_frame()       

    def create_main_frame(self):        
        self.tabs = tabs = QTabWidget()
        tabs.setTabBar(Tabbar())
        # Create first page
        page1 = QWidget()
        button1 = QPushButton('Add Tab', page1)
        vbox1 = QVBoxLayout()
        vbox1.addWidget(button1)
        page1.setLayout(vbox1)
      
        tabs.addTab(page1, 'First page')
        button1.clicked.connect(self.addTab)        
        self.setCentralWidget(tabs)
        self.tabs.tabCloseRequested.connect(self.tabRemove)
        
    def tabRemove(self,index):
        self.tabs.removeTab(index)
        
    def addTab(self):
        page2 = QWidget()
        self.tabs.addTab(page2, 'Second page')

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = AppForm()
    form.resize(600,500)
    form.show()
    app.exec_()