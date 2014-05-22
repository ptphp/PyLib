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

INCLUDES = ["encodings","encodings.*","PySide.QtNetwork"] 

options = {"py2exe" :
    {"compressed" : 1,
     "optimize" : 2,
     "bundle_files" : 3,
     "includes" : INCLUDES,
     "excludes" : [],
     "dll_excludes": [ ] }}

windows = [{"script": "editor.py",
      "icon_resources": [],
      }]

setup(name = "PtEditor",
      version = "1.0",
      description = "PtEditor",
      author = "joseph",
      author_email ="",
      maintainer = "",
      maintainer_email = "",
      license = "Licence",
      url = "",
      data_files = [],
      #zipfile=None,
      options = options,
      windows = windows,
      )

