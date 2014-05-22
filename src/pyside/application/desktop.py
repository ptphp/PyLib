'''
Created on Jan 22, 2013

@author: joseph
'''

import sys
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtWebKit import *


app = QApplication(sys.argv)
view = QWidget()
desktop = QApplication.desktop()
rect = desktop.availableGeometry()
view.setGeometry(rect)
view.show()

sys.exit(app.exec_())



