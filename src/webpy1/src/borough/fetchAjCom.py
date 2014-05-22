#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbmysql import * 
import urllib,urllib2,time,sys,os
from BeautifulSoup import BeautifulSoup
mysql = MySQL()

#===============================================================================
# 采集安居客小区
#===============================================================================
def getLink():
    mysql.query("delete fke_borough_web_aj where city = 'ks'")
    res = mysql.show()
    for data in res:
        print data['link']
def fetch(url):
    print url
    r = urllib2.urlopen(url).read()
    soup = BeautifulSoup(r)
    print soup.title.string.decode('utf-8')
    

if __name__ == "__main__":
    url = "http://suzhou.anjuke.com/v2/community/view/171807"
    #fetch(url)
    getLink()