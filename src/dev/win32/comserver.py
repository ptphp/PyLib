# -*- coding: utf-8 -*-
'''
Created on 2011-7-27

@author: dholer
Python 开发Activex组件方法

window.onload = function(){ 
var obj = new ActiveXObject("Python.Utilities"); 

alert(obj.SplitString("Hel")); 
} 

'''
# SimpleCOMServer.py 

class PythonUtilities: 
    _public_methods_ = ['SplitString'] 
    _reg_progid_ = "Python.Utilities" 
    _reg_clsid_ = "{A6688635-62F5-41cb-AF54-CBA84C2F0F86}" 

def SplitString(self, val): 
    return "Hello world ", val 

if __name__ == '__main__': 
    print "Registering COM server..." 
    import win32com.server.register 
    win32com.server.register.UseCommandLine(PythonUtilities) 