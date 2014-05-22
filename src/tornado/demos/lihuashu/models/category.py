#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: Joseph
@email:liseor@gmail.com
Created on 2012-7-20
'''
from riakClient.document import Document
from config.settings import globalSetting

class Category(Document):
    bucket_name = globalSetting['categoryBucket']
    data = {
             'name':None,
             'title':None,             
             'desc':None,
             'group':None,
             'order':None,             
             'boards':[],
             }
    
    def __init__(self):
        Document.__init__(self)
    def getCat(self,group):
        #keys = self.getByKeyValues('group', group)
        query = {}
        
        query['q'] = "group:%s" % group
        query['sort'] = "order"
        
        data = self.solr(query)
        #data = self.all(keys)
        #print data
        return data
    def getCats(self):
        cats = {}
        cats['cat1'] = self.getCat(1)
        cats['cat2'] = self.getCat(2)
        cats['cat3'] = self.getCat(3)
        cats['cat4'] = self.getCat(4)        
        return cats
if __name__ == "__main__":
    c = Category()
    print c.data 
    c.data['name'] = '测试'
    c.data['title'] = '文'
    c.data['desc'] = '中'
    c.data['group'] = 1
    c.data['order'] = 1
    
    c.key = c.genKey(c.data['name'])
    print c.data
    c.post()    
    keys = c.allKey()
    print c.all(keys)
    