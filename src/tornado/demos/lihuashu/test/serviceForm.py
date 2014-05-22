#!user/bin/env python
# -*- coding: utf8 -*- 
'''
Created on Jul 11, 2012

@author: joseph
'''
import urllib,urllib2


if __name__ == '__main__':
    regData = {}
    regData['content']      = "desc content"
    regData['_xsrf']      = "28d55624808042768af23188e318500a"
    regData['img_key']   = "222222"
    regData['img_value'] = "222222"
    regQuery = urllib.urlencode(regData)
    print regQuery
    url = "http://localhost/service/form/"
    req = urllib2.Request(url,regQuery)
    res = urllib2.urlopen(req)
    print res.read()
    