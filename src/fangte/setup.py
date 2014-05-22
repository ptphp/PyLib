# -*- coding: utf-8 -*-
from distutils.core import setup
import py2exe

includes = ["encodings", "encodings.*","sip","PyQt4.QtNetwork"] 

options = {"py2exe": 
            {   "compressed": 1, 
                "optimize": 2, 
                "includes": includes, 
                "bundle_files": 3
            } 
          } 
setup(    
    version = "0.0.1", 
    description = "FangTee Desktop", 
    name = "FangTee Desktop", 
    options = options, 
    data_files = [
            ('imageformats', [
                'C:\\Python27\\Lib\\site-packages\\PyQt4\\plugins\\imageformats\\qgif4.dll',
                'C:\\Python27\\Lib\\site-packages\\PyQt4\\plugins\\imageformats\\qjpeg4.dll',
                'C:\\Python27\\Lib\\site-packages\\PyQt4\\plugins\\imageformats\\qico4.dll'
                ])
                  ],                
    zipfile=None,  
    windows=[{
        'script':'fangtee.py',
        'icon_resources':[(0,'res/fangtee.ico')],
    }]
)
