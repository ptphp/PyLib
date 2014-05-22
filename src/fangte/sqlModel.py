#!/bin/env python
# -*- coding: utf-8 -*-
import sqlite3
import time,sys
import os.path as osp

class Db():
    conn = ''
    cursor = ''
    sql = ''
    def __init__(self, dbname):    
        #check_same_thread=False    
        try:
            self.conn = sqlite3.connect(osp.abspath(dbname))
        except Exception, what:
            print what
            sys.exit()
        self.conn.row_factory = sqlite3.Row   
        self.cursor = self.conn.cursor()  
        self.createTable()      
    def createFollow(self): 
        sql = """
            CREATE TABLE IF NOT EXISTS [follow](
            [id] INTEGER PRIMARY KEY,
            [house_id] INTEGER,
            [content] TEXT,
            [addtime] TEXT            
           );
        """
        self.cursor.execute(sql)
        self.cursor.execute('''
        create index IF NOT EXISTS house_follow_index on follow(content);
           
            ''')
        self.conn.commit()
    def createTable(self): 
               
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS [house](
           [id] INTEGER PRIMARY KEY,
           [flag] INTEGER,
           [title] TEXT,
           [posttime] TEXT,
           [price] INTEGER,
           [price_min] INTEGER,
           [deposit] TEXT,
           [belong] TEXT,
           [room] TEXT,
           [hall] INTEGER,
           [toilet] INTEGER,
           [yt] INTEGER,
           [area] INTEGER,
           [area_min] INTEGER,
           [houseType] TEXT,
           [fitment] TEXT,
           [floor] INTEGER,
           [topfloor] INTEGER,
           [toward] TEXT,
           [age] TEXT,
           [equ] TEXT,
           [city] TEXT,
           [region] TEXT,
           [section] TEXT,
           [borough] TEXT,
           [addr] TEXT,
           [phone] TEXT,
           [phone_pic] BLOB,           
           [owner] TEXT,
           [desc] TEXT,
           [info] TEXT,
           [search] TEXT,
           [url] TEXT NOT NULL UNIQUE,
           [thumb] TEXT,
           [webFlag] TEXT,
           [stat] INTEGER,
           [pics] TEXT,
           [isPerson] INTEGER,
           [collected] INTEGER,
           [followNum] INTEGER,
           [picNum] INTEGER,
           [map1] TEXT,
           [map2] TEXT
           );
        ''')
        self.cursor.execute('''
        create index IF NOT EXISTS house_title_index on house(title);
           
            ''')
        self.cursor.execute('''
           create index IF NOT EXISTS house_search_index on house(search);
           
            ''')
        self.cursor.execute('''
           create index IF NOT EXISTS house_desc_index on house(desc);           
            ''')
        
        #print "create table page "
        self.conn.commit()  
        self.createFollow() 
    def query(self, sql,commit=False):  
        self.sql = sql
        try:
            flag = self.cursor.execute(sql)
            if commit == True:
                self.commit()
            return flag
        except Exception as e:
            print('SQL Error:',e)
            

    def commit(self):
        self.conn.commit()
    def getField(self):
        dict = []
        for fieldDesc in self.cursor.description:
            dict.append(fieldDesc[0])
        return dict
    def count(self,sql):
        self.query(sql)
        return self.showOne()['num']
        
    def showAll(self):
        r = self.cursor.fetchall()
        res = []
        field = self.getField()
        for row in r:
            _row = {}
            for k in field:
                _row[k] = row[k]
            res.append(_row)
        return res
    def showOne(self):
        r = self.cursor.fetchone()
        field = self.getField()
        
        row = {}
        for k in field:
            row[k] = r[k]
        return row
    
    def __del__(self):
        self.cursor.close()
        self.conn.close()
        
