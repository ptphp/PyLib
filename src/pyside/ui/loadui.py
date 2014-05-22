'''
Created on 2013-2-2

@author: Joseph
'''
from PySide.QtUiTools import QUiLoader
from PySide.QtCore import QMetaObject


class MyQUiLoader(QUiLoader):
    def __init__(self, baseinstance):
        super(MyQUiLoader, self).__init__()
        self.baseinstance = baseinstance
    
    def createWidget(self, className, parent=None, name=""):
        widget = QUiLoader.createWidget(self, className, parent, name)
        if parent is None:
            return self.baseinstance
        else:
            setattr(self.baseinstance, name, widget)
            return widget

def loadUi(uifile, baseinstance=None):
    loader = MyQUiLoader(baseinstance)
    ui = loader.load(uifile)
    QMetaObject.connectSlotsByName(ui)
    return ui



