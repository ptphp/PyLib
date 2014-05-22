#!/usr/bin/env python
# -*- coding: utf-8 -*-
#http://stackoverflow.com/questions/4629595/using-pysides-qtwebkit-under-windows-with-py2exe
#http://qt-project.org/wiki/Packaging_PySide_applications_on_Windows
__author__ = 'joseph'

from distutils.core import setup  
import py2exe  
import sys

# If run without args, build executables, in quiet mode.
if len(sys.argv) == 1:
    sys.argv.append("py2exe")
    sys.argv.append("-q")

RT_MANIFEST = 24

INCLUDES = ["wmi"] 

options = {"py2exe" :
    {"compressed" : 1,#压缩
     "optimize" : 2,
     "bundle_files" : 2, #1 所有文件打包成一个exe文件 }
     "includes" : INCLUDES,
     "excludes" : [],
     "dll_excludes": [ "MSVCP90.dll","MSVCR90.dll","MSVCM90.dll"] }}

windows = [{"script": "main.py",
      "icon_resources": [(0, "fav.ico")],
      }]

setup(name = "AMW",
      version = "1.0",
      description = "AMW Hardware listener",
      author = "joseph",
      author_email ="liseor@gmail.com",
      maintainer = "amwnet.cn",
      maintainer_email = "liseor@gmail.com",
      license = "Licence",
      url = "http://www.amwnet.cn",
      data_files = [
            "MSVCP90.dll","MSVCR90.dll","MSVCM90.dll", 'fav.ico'   
            ],
      #zipfile=None,#不生成library.zip文件
      options = options,
      windows = windows,
      )

