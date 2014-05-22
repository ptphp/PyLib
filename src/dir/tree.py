'''
Created on Jan 28, 2013

@author: joseph
'''
from PySide.QtCore import QDir,QFileInfo
import sys


def listFiles(dir):
    res = []
    directory = QDir(dir)
    #directory.setFilter(QDir.Files | QDir.Hidden | QDir.NoSymLinks)
    directory.setSorting(QDir.DirsFirst)
    for entry in directory.entryInfoList():
        it = {}
        if entry.fileName() == '.' or entry.fileName() == '..':
            continue
        path = directory.filePath(entry.fileName())
        fi = QFileInfo(path)        
        it['path'] = path
        #print fi.baseName()
        
        it['basename'] = fi.fileName()
        
        if fi.isDir():
            it['extension'] = "dir"
        else:
            it['extension'] = fi.completeSuffix()
        res.append(it)
    return res
            
if __name__ == "__main__":
    res = listFiles("D:\Dhole\PtProject\Core\Application")
    print res
    