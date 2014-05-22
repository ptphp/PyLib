#coding=UTF-8
'''
Created on 2011-6-27

@author: Administrator
'''
import mechanize
import cookielib
import re
import simplejson as sj
import time
import cPickle
pks = cPickle.load(open('e:\ganji.pdb','rb'))
for row in pks:
    print row
    for item in pks[row]:
        print item,pks[row]
    


    