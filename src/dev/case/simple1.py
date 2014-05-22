'''
Created on 2011-7-28

@author: dholer
'''

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import *
import sys
app=QApplication(sys.argv)  
b=QPushButton("Hello Kitty!")  
b.show()  
app.connect(b,SIGNAL("clicked()"),app,SLOT("quit()"))  
app.exec_()  