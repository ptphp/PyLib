#!/usr/bin/env python
# -*- coding=utf-8 -*-
'''
Created on 2013-3-31
@author: Joseph
'''
import os
import traceback

def trace_back():  
    try:  
        return traceback.format_exc()  
    except:  
        return ''

#单例装饰器(decorator)
def st(cls, *args, **kw):  
    instances = {}  
    def _st():  
        if cls not in instances:  
            instances[cls] = cls(*args, **kw)  
        return instances[cls]  
    return _st  

def mkDir(path):
    if os.path.isdir(path) == False:
        mkDir(os.path.dirname(path))
        return os.mkdir(path)    
    return True

if __name__ == '__main__':
    pass