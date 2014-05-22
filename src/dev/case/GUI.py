'''
Created on 2011-7-29

@author: dholer
'''
import os 
import sys 
import MOVtoMXF 
from PyQt4.QtCore import * 
from PyQt4.QtGui import * 
 
class Form(QDialog): 
     def process(self): 
           path = str(self.pathBox.displayText()) 
           if(path == ''): 
                QMessageBox.warning(self, "Empty Path", "You didnt fill something out.") 
                return 
           xmlFile = str(self.xmlFileBox.displayText()) 
           if(xmlFile == ''): 
                QMessageBox.warning(self, "No XML file", "You didnt fill something.") 
                return 
           outFileName = str(self.outfileNameBox.displayText()) 
           if(outFileName == ''): 
                QMessageBox.warning(self, "No Output File", "You didnt do something") 
                return 
           print path + "  " + xmlFile + " " + outFileName 
           mov1 = MOVtoMXF.MOVtoMXF(path, xmlFile, outFileName, self.log) 
           self.log.show() 
           rc = mov1.ScanFile() 
           if( rc < 0): 
               print "something happened" 
           #self.done(0)
    
    def __init__(self, parent=None): 
            super(Form, self).__init__(parent) 
            self.log = Log() 
            self.pathLabel = QLabel("P2 Path:") 
            self.pathBox = QLineEdit("") 
            self.pathBrowseB = QPushButton("Browse") 
            self.pathLayout = QHBoxLayout() 
            self.pathLayout.addStretch() 
            self.pathLayout.addWidget(self.pathLabel) 
            self.pathLayout.addWidget(self.pathBox) 
            self.pathLayout.addWidget(self.pathBrowseB) 
            self.xmlLabel = QLabel("FCP XML File:") 
            self.xmlFileBox = QLineEdit("") 
            self.xmlFileBrowseB = QPushButton("Browse") 
            self.xmlLayout = QHBoxLayout() 
            self.xmlLayout.addStretch() 
            self.xmlLayout.addWidget(self.xmlLabel) 
            self.xmlLayout.addWidget(self.xmlFileBox) 
            self.xmlLayout.addWidget(self.xmlFileBrowseB) 
 
            self.outFileLabel = QLabel("Save to:") 
            self.outfileNameBox = QLineEdit("") 
            self.outputFileBrowseB = QPushButton("Browse") 
            self.outputLayout = QHBoxLayout() 
            self.outputLayout.addStretch() 
            self.outputLayout.addWidget(self.outFileLabel) 
            self.outputLayout.addWidget(self.outfileNameBox) 
            self.outputLayout.addWidget(self.outputFileBrowseB) 
            self.exitButton = QPushButton("Exit") 
            self.processButton = QPushButton("Process") 
            self.buttonLayout = QHBoxLayout() 
            #self.buttonLayout.addStretch() 
            self.buttonLayout.addWidget(self.exitButton) 
            self.buttonLayout.addWidget(self.processButton)  
            self.layout = QVBoxLayout() 
            self.layout.addLayout(self.pathLayout) 
            self.layout.addLayout(self.xmlLayout) 
            self.layout.addLayout(self.outputLayout) 
            self.layout.addLayout(self.buttonLayout) 
            self.setLayout(self.layout) 
            self.pathBox.setFocus() 
            self.setWindowTitle("MOVtoMXF") 
            self.connect(self.processButton, SIGNAL("clicked()"), self.process) 
            self.connect(self.exitButton, SIGNAL("clicked()"), self, SLOT("reject()")) 
            self.ConnectButtons() 
 
class Log(QTextEdit): 
    def __init__(self, parent=None): 
        super(Log, self).__init__(parent) 
        self.timer = QTimer() 
        self.connect(self.timer, SIGNAL("timeout()"), self.updateText()) 
        self.timer.start(2000)  
    def updateText(self): 
        print "update Called" 