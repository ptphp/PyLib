'''
Created on 2011-7-29

@author: dholer
'''
import os 
import sys 
import time 
import string 
import FileUtils 
import shutil 
import re 
class MOVtoMXF: 
    #Class to do the MOVtoMXF stuff. 
    def __init__(self, path, xmlFile, outputFile, edit): 
        self.MXFdict = {} 
        self.MOVDict = {} 
        self.path = path 
        self.xmlFile = xmlFile 
        self.outputFile = outputFile 
        self.outputDirectory = outputFile.rsplit('/',1) 
        self.outputDirectory = self.outputDirectory[0] 
        sys.stdout = OutLog( edit, sys.stdout) 
 
class OutLog(): 
    def __init__(self, edit, out=None, color=None): 
        """(edit, out=None, color=None) -> can write stdout, stderr to a 
        QTextEdit. 
        edit = QTextEdit 
        out = alternate stream ( can be the original sys.stdout ) 
        color = alternate color (i.e. color stderr a different color) 
        """ 
        self.edit = edit 
        self.out = None 
        self.color = color 
 
    def write(self, m): 
        if self.color: 
            tc = self.edit.textColor() 
            self.edit.setTextColor(self.color) 
        #self.edit.moveCursor(QtGui.QTextCursor.End) 
        self.edit.insertPlainText( m ) 
        if self.color: 
            self.edit.setTextColor(tc) 
        if self.out: 
            self.out.write(m) 
        self.edit.show() 