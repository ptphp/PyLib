# -*- coding: utf-8 -*-
import urlparse,os,urllib
from PySide import QtCore
def makeDir(path):
    if os.path.isdir(path) == False:
        makeDir(os.path.dirname(path))
        return os.mkdir(path)    
    return True

def download(url,content):  
    content = ""    
    u = urlparse.urlparse(url)
    filename = "d:/offline/"+u.netloc+u.path    
    name =  os.path.basename(filename)
    if "." not in name:
        filename = filename+".html"
    _dir =  os.path.dirname(filename)
    makeDir(_dir)
    urllib.urlretrieve(url,filename)
    
def download1(url,content):    
    content = ""
    
    u = urlparse.urlparse(url)
    filename = "d:/offline/"+u.netloc+u.path    
    name =  os.path.basename(filename)
    if "." not in name:
        filename = filename+".html"
        
    urllib.urlretrieve(url,filename)
    pass
    #print name
    _dir =  os.path.dirname(filename)
    makeDir(_dir)
    fi = QtCore.QFile(filename)    
    if not fi.open(QtCore.QFile.WriteOnly | QtCore.QFile.Text):
        return    
    print type(content)
    out = QtCore.QTextStream(fi)
    out.setCodec("UTF-8")
    out << content
if __name__ == "__main__":
    download('http://guanjia.qq.com/download.html','')
    
    