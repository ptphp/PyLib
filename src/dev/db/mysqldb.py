#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: Joseph
@email:liseor@gmail.com
Created on 2012-6-10
'''
import MySQLdb

#------------------------------------------------------------------------------ 链接数据库
conn = MySQLdb.connect(host="127.0.0.1",user="logic",passwd="logic123",db="drupal7")

cursor = conn.cursor()
print cursor
