#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: Joseph
@email:liseor@gmail.com
Created on 2012-6-10
http://www.pythonclub.org/python-files/csv
'''
import csv

cfile = open("product.csv")
rows = csv.reader(cfile)
i = 0
for PRIMARY_VND_NUM,VENDOR_NAME,ITEM_NUM,DESCRIPTION_1,DESCRIPTION_2,ITEM_CLASS,DESCRIPTION,CATEGORY_1,CATEGORY_2,CATEGORY_3 in rows:
    #print PRIMARY_VND_NUM,VENDOR_NAME,ITEM_NUM,DESCRIPTION_1,DESCRIPTION_2,ITEM_CLASS,DESCRIPTION,CATEGORY_1,CATEGORY_2,CATEGORY_3
    print i
    i+=1