'''
Created on Jan 22, 2013

@author: joseph
'''
#_*_ coding:utf-8 _*_
from PySide import QtGui ,QtCore
 
 
class MoveDemo(QtGui.QMainWindow):
    def __init__(self,parent = None):
        super(MoveDemo,self).__init__(parent)
        self.setMouseTracking(True)
        self.setWindowFlags(QtCore.Qt.WindowSystemMenuHint)
    def mousePressEvent(self,event):
        if event.button() == QtCore.Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
            
    def mouseMoveEvent(self,event):
        if event.buttons() ==QtCore.Qt.LeftButton:
            self.move(event.globalPos() - self.dragPosition)
            event.accept()    
    
 
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    frm = MoveDemo()
    frm.show()
    sys.exit(app.exec_())