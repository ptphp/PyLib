#coding:utf-8

import sys, os
import time
import random
from PySide import QtCore, QtGui
import threading

class MThread( QtCore.QThread ):
    infomsgSignal = QtCore.Signal( unicode )
    errmsgSignal = QtCore.Signal( unicode )
    running  = QtCore.Signal(bool)
    def __init__( self ):
        super( MThread, self ).__init__()

    def getName( self ):
        if not hasattr( self, "name" ):
            self.name = threading.currentThread().getName()
        return self.name

    def emitInfo( self, msg ):
        self.infomsgSignal.emit( msg )

    def emitError( self, msg ):
        self.errmsgSignal.emit( msg )

    def run( self ):
        self.running.emit(True)
        for i in range( 10 ):
            s = self.getName() + " " + str( i )
            print s
            v = random.random() * 10
            if v > 8:
                self.emitError( s )
            else:
                self.emitInfo( s )
            time.sleep( 1 )
        print self.getName(), "stopping"
        self.running.emit(False)

class Mainwin( QtGui.QMainWindow ):
    def __init__( self ):
        super( Mainwin, self ).__init__()
        self.widget = QtGui.QWidget( self )
        self.setCentralWidget( self.widget )
        layout = QtGui.QVBoxLayout()
        self.widget.setLayout( layout )
        btn = QtGui.QPushButton( "Start Thread", self.widget )
        btn.clicked.connect( self.onThreadBtnClicked )
        layout.addWidget( btn )
        self.te = QtGui.QTextEdit( self.widget )
        self.te.setReadOnly( True )
        layout.addWidget( self.te )
        self.sb = self.statusBar()
        self.createToolbar()
        #self.layout()
        self.thread = threading.currentThread()
        self.workers = []

    def createToolbar( self ):
        toolbar = QtGui.QToolBar( self )
        self.threadAction = QtGui.QAction( 
            QtGui.QIcon( 'res/title.png' ),
            "ThreadStatus",
            self
        )
        self.threadAction.setCheckable(True)
        self.threadAction.triggered.connect( self.onThreadBtnClicked )
        toolbar.addAction( self.threadAction )
        self.addToolBar( toolbar )

    def onThreadBtnClicked( self ):
        t = MThread()
        t.infomsgSignal.connect( self.onThreadInfoMsg )
        t.errmsgSignal.connect( self.onThreadErrorMsg )
        t.running.connect(self.threadAction.setChecked)
        #t.finished.connect(self.threadAction.toggled)
        self.workers.append( t )
        t.start()

    def onNewLog( self, msg ):
        self.te.append( msg )

    def onThreadInfoMsg( self, msg ):
        self.onNewLog( "INFO  " + msg )
        self.sb.showMessage( "INFO  " + msg )

    def onThreadErrorMsg( self, msg ):
        self.onNewLog( "ERROR " + msg )
        self.sb.showMessage( "ERROR " + msg )
        print self.thread.getName(), "ERROR " + msg

    def closeEvent( self, *args, **kwargs ):

        for w in self.workers:
            w.terminate()
        for w in self.workers:
            w.wait()
        return super( Mainwin, self ).closeEvent( *args, **kwargs )

def main():
    app = QtGui.QApplication( [] )
    mw = Mainwin()
    mw.show()
    app.exec_()

if __name__ == '__main__':
    main()