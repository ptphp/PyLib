#!/usr/bin/env python
# -*- coding=utf-8 -*-
'''
Created on 2013-3-31
@author: Joseph
'''
import PtDb

if __name__ == '__main__':    
    PtDb.config = {
                   'sqlite':{
                             'type':'sqlite',
                             'dbname':"data1.db"
                             },
                   'default':{
                     'type':'mysql',
                     'host':'localhost',
                     'port':3306,
                     'dbname':'game110_dev',
                     'dbuser':'root',
                     'dbpass':'root',
                     'charset':'utf8',
                     },
                   'default1':{
                     'type':'mysql',
                     'host':'localhost',
                     'port':3306,
                     'dbname':'game110_dev',
                     'dbuser':'root',
                     'dbpass':'root',
                     'charset':'utf8',
                     },
                   }
    
    PtDb.init('sqlite').open("test.db")
    PtDb.init('sqlite').open("test1.db")
    PtDb.init()
    print PtDb.init().getAll("select * from orders")
    print PtDb.init().getOne("select * from orders limit 1")
    