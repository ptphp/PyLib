#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: Joseph
@email:liseor@gmail.com
Created on 2012-7-20
'''
from riakClient.document import Document
from config.settings import globalSetting
from models.user import User
class Comment(Document):
    bucket_name = globalSetting['commentBucket']
    data = {
             'rawtext':None,
             'createTime':None,
             'user':None,
             'pin':None,
             'nickname':None,
             }
    def getByPin(self,key):
        query = {}
        query['q'] = "pin:%s" % key
        query['sort'] = "createTime"
        comment_data = self.solr(query)
        
        #comment_keys = self.getByKeyValues('pin', key)
        #comment_data = self.all(comment_keys)
        user = User()
        res = []
        for row in comment_data:
            row['userInfo'] = user.getDetail(row['user'])
            res.append(row)
        return res
        
    def __init__(self):
        Document.__init__(self)
        
