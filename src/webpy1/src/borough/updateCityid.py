#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dbmysql import *
from dbsqli import *
import urllib, urllib2, time

mysql = MySQL() #@UndefinedVariable


def do():
    mysql.query("select id,city from fke_broker_store")
    res = mysql.show()
    for row in res:        
        mysql.query("select * from fke_web_config where id ='%s'" % row['city'])
        r = mysql.show()
        if r and r[0]['city_id']:
            print row['city'],r[0]['id'],r[0]['city_id']
            print "update fke_broker_store set city_id = %d,city = '%s' where id = %d" % (r[0]['city_id'],r[0]['base_domain'],row['id'])
            mysql.query("update fke_broker_store set city_id = %d,city = '%s'  where id = %d" % (r[0]['city_id'],r[0]['base_domain'],row['id']))
            print "update!"



if __name__ == "__main__":
    do()