# -*- coding: utf-8 -*-
from distutils.core import setup
import py2exe

includes = ["encodings", "encodings.*","sip","PyQt4.QtNetwork"] 

options = {"py2exe": 
            {   "compressed": 1, 
                "optimize": 2, 
                "includes": includes, 
                "bundle_files": 1 
            } 
          } 
setup(    
    version = "0.0.1", 
    description = "FangTee Desktop", 
    name = "FangTee Desktop", 
    options = options, 
    zipfile=None,  
    windows=[{
        'script':'fangtee.pyw',
        'icon_resources':[(0,'res/fangtee.ico')],
    }]
)
