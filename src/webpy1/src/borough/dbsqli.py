#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3 as sqlite
import os.path as osp
import sys

class Sqli(object):
    conn = ''
    cursor = ''
    def __init__(self, dbname):        
        try:
            self.conn = sqlite.connect(osp.abspath(dbname))
        except Exception, what:
            print what
            sys.exit()
        self.conn.row_factory = sqlite.Row         
        self.cursor = self.conn.cursor()
        
    def createTable(self):        
        self.cursor.execute('''
    CREATE TABLE IF NOT EXISTS [website](
      [id] INTEGER PRIMARY KEY,
      [siteName] TEXT,
      [loginUrl] TEXT,
      [loginQuery] TEXT,
      [postUrl] TEXT,
      [postQuery] TEXT,
      UNIQUE([siteName]));
            ''')
        print "create table website "
        self.cursor.execute('''
    CREATE INDEX IF NOT EXISTS [website_idx_siteName] ON [website]([siteName]);
            ''')
        print 'create website index'
        self.conn.commit()
    def createTable_com(self):        
        self.cursor.execute('''
    CREATE TABLE IF NOT EXISTS [com](
      [id] INTEGER PRIMARY KEY,
      [title] TEXT,
      [city] TEXT,
      [url] TEXT,
      UNIQUE([url]));
            ''')
        print "create table com "
        self.cursor.execute('''
    CREATE INDEX IF NOT EXISTS [website_idx_url] ON [com]([url]);
            ''')
        print 'create map index'
        self.conn.commit()
    def createTable_58(self):        
        self.cursor.execute('''
    CREATE TABLE IF NOT EXISTS [com](
      [id] INTEGER PRIMARY KEY,
      [title] TEXT,
      [city] TEXT,
      [url] TEXT,
      UNIQUE([url]));
            ''')
        print "create table com "
        self.cursor.execute('''
    CREATE INDEX IF NOT EXISTS [website_idx_url] ON [com]([url]);
            ''')
        print 'create map index'
        self.conn.commit()    
    def query(self, sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception, what:
            print what

   
    def show(self):
        r = self.cursor.fetchall()
        return r
    def showone(self):
        return self.cursor.fetchone()
    
    def __del__(self):
        self.cursor.close()
        self.conn.close()
