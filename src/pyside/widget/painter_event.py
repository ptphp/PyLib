'''
Created on Jan 22, 2013

@author: joseph
'''

from PySide.QtGui import *
from PySide.QtCore import *
from PySide import QtCore

class MyForm(QWidget):
    def __init__(self,parent=None):
        super(MyForm,self).__init__(parent) 
        self.mask = QBitmap(400,300)
        self.mask.fill(Qt.white)
        painter=QPainter(self.mask)
        painter.setBrush(QColor(0x000000))
        painter.drawRoundRect(0,0,400,300,3,3)
        self.setMask(self.mask)
         
    def paintEvent(self,event):
        painter = QPainter(self)
        painter.drawPixmap(0,0,self.width(),self.height(),QPixmap("painter_event_3.jpg"))
        
    def mousePressEvent(self,event):
        if event.button() == QtCore.Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
            
    def mouseMoveEvent(self,event):
        if event.buttons() ==QtCore.Qt.LeftButton:
            self.move(event.globalPos() - self.dragPosition)
            event.accept()    


if __name__ == "__main__":
    app = QApplication([])
    form = MyForm()
    form.show()
    form.move(400,200)
    app.exec_()