# -*- coding: utf-8 -*-
'''
Created on Jan 30, 2013

@author: joseph
'''
from PySide.QtCore import QFile,QIODevice,QTextStream
def getContent(path):
    file = QFile(path)
    if not file.open(QIODevice.ReadOnly | QIODevice.Text):
        return
    ts = QTextStream(file)
    ts.setCodec("UTF-8")
    res = ts.readAll()
    return res
    
if __name__ == "__main__":
    getContent('D:/Dhole/PtProject/PTGUI-dev/ptpy/ptide/ui/index.html')