'''
Created on 2013-2-2

@author: Joseph
'''

from PySide.QtUiTools import QUiLoader
from PySide import QtGui
import sys

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    loader = QUiLoader()
    widget = loader.load('untitled.ui')
    widget.show()
    sys.exit(app.exec_())