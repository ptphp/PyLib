#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dbmysql import *
from dbsqli import *
import urllib, urllib2, time

mysql = MySQL() #@UndefinedVariable
dbname = "db/anjuke_ks.db"
sqli = Sqli(dbname) #@UndefinedVariable
sqli.query("select * from xiaoqu")
r = sqli.show()
for row in r:
    print row['name'], row['link']
    sql = """    
        INSERT INTO  `jjr360`.`fke_borough_web_aj` (
        `id` ,
        `borough_id` ,
        `borough_name` ,
        `borough_letter` ,
        `borough_alias` ,
        `addr` ,
        `link` ,
        `city` ,
        `cityid`,
        `cityarea_id`,
        `cityarea`,
        `borough_section`,
        `section`
        )
        VALUES (
        NULL ,  NULL,'%s', NULL , NULL ,  '%s',  '%s', 'ks' ,  '31', NULL, NULL, NULL, NULL
        );""" % (row['name'], row['addr'], row['link'])
   
    mysql.query(sql)





