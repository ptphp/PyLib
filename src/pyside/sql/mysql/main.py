#!/usr/bin/env python
# -*- coding=utf-8 -*-
'''
Created on 2013-2-2

@author: Joseph
'''

import sys
from PySide import QtSql
from PySide.QtGui import *
from Ui_gui import *
 
def createConnection():
    db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName('test.db')
    #db.setDatabaseName(":memory:")
    
    if db.open():
        query = QtSql.QSqlQuery()
        query.exec_("create table person is not exists(id int primary key, firstname varchar(20), lastname varchar(20))")
        query.exec_("insert into person values(101, 'Danny', 'Young')")
        query.exec_("insert into person values(102, 'Christine', 'Holand')")
        print(QtSql.QSqlDatabase.database())
        print(QtSql.QSqlDatabase.drivers())
        print(db.tables())
        return True
    else:
        print (db.lastError().text())
        return False
    
    
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.model = QtSql.QSqlTableModel(self)
        self.model.setTable("person")
        self.model.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        self.model.select()
        self.tableView.setModel(self.model)



if __name__ == '__main__':
    app =QApplication(sys.argv)
    if createConnection()== False:
        sys.exit(1)
    
    frame = MainWindow()
    frame.show()    
    sys.exit(app.exec_())
    