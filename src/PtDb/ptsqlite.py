#!/usr/bin/env python
# -*- coding=utf-8 -*-
'''
Created on 2013-3-31
@author: Joseph
'''

import os
import sqlite3
from ptpy import st,mkDir

@st
class PtSqlite(object):
    conn = None
    cursor = None    
    def dict_factory(self,cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d
    
    def deleteDb(self,dbname):        
        self.cursor.close()
        self.conn.close()
        os.remove(os.path.abspath(dbname))
    def open(self,dbname):
        #print dbname
        mkDir(os.path.dirname(os.path.abspath(dbname)))
        self.conn = sqlite3.connect(os.path.abspath(dbname))
        self.conn.row_factory = self.dict_factory    
        self.cursor = self.conn.cursor()
        return self
        
    def insertid(self):
        return self.cursor.lastrowid
    
    def query(self, sql,param = None):
        #print sql
        try:
            if param is None:
                self.cursor.execute(sql)
            else:
                self.cursor.execute(sql,param)            
        except Exception as what:
            self.conn.rollback()
        else:
            self.conn.commit()
            return self
   
    def getAll(self):
        r = self.cursor.fetchall()
        return r
    def getOne(self):
        return self.cursor.fetchone()    
    def where(self,condition):
        where = ""
        ww = []        
        if condition:
            for cc in condition:
                ww.append(cc+"= '"+str(condition[cc])+"'")
            where  = "where "+",".join(ww)
        return where
    def parseUpdate(self,table,param,condition):
        _sets = []
        for pp in param:
            _sets.append(pp+"= ?")
        sets = "set "+",".join(_sets)
        
        sql = "update %s %s %s" % (table,sets,self.where(condition))
        #print sql
        
        pp =  tuple(param.values())
        return sql,pp
    def update(self,table,param,condition):
        #print param,condition
        sql, pp = self.parseUpdate(table, param, condition)
        self.query(sql, pp)
    def parseInsert(self,table,param):
        sql = ""
        t = param.keys()
        fields = ",".join(t)
        _values = "?," *len(t)
        values =  _values[:-1]
        sql = "insert into %s(%s) values(%s) " % (table,fields,values)
        pp =  tuple(param.values())
        return sql,pp
        
    def insert(self,table, args):
        sql,param = self.parseInsert(table,args)
        self.query(sql, param)
        
        return self.insertid()
    
    def exists(self,table,condition):
        sql = "select id from %s %s" % (table,self.where(condition))
        #print sql
        self.query(sql)
        res = self.getOne()
        
        if res:
            return True
        else:
            return False
    def close(self):
        self.cursor.close()
        self.conn.close()
    #def __del__(self):
    #    self.cursor.close()
    #    self.conn.close()


if __name__ == '__main__':
    db = PtSqlite();    
    db.open("db.db")
    