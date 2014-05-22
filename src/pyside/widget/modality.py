'''
Created on Jan 22, 2013

@author: joseph
'''
from PySide import QtCore, QtGui
class Widget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)

    def mousePressEvent(self, evt):
        self.w = QtGui.QWidget()
        #self.w.setWindowModality(QtCore.Qt.NonModal)
        self.w.setWindowModality(QtCore.Qt.WindowModal)        
        #self.w.setWindowModality(QtCore.Qt.ApplicationModal)
        
        self.w.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.w.show()

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())