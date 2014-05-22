#!/usr/bin/env python
# -*- coding=utf-8 -*-
'''
http://pythonhosted.org/pyquery/
'''

'''
Created on 2013-3-31
@author: Joseph
'''
from pyquery import PyQuery as pq #@UnresolvedImport
from lxml import etree #@UnresolvedImport
import urllib

d = pq("<html></html>")
print d
d = pq(etree.fromstring("<html></html>"))
print d
d = pq(url='http://www.ptphp.net/')
print d("body").text()

if __name__ == '__main__':
    pass