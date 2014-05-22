#!/usr/bin/env python
# -*- coding=utf-8 -*-
'''
Created on 2013-2-2

@author: Joseph
'''
from PySide import QtSql, QtGui


if __name__ == '__main__':
    db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
    #db.setDatabaseName("test.db")
    db.setDatabaseName(":memory:")
    
    if not db.open():
        print "wtf"
    
    query = QtSql.QSqlQuery()
    query.exec_("create table person(id int primary key, firstname varchar(20), lastname varchar(20))")
    query.exec_("insert into person values(101, 'Danny', 'Young')")
    query.exec_("insert into person values(102, 'Christine', 'Holand')")
