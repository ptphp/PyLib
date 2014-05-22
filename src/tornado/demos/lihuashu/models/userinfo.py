#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: Joseph
@email:liseor@gmail.com
Created on 2012-7-20
'''
from riakClient.document import Document
from config.settings import globalSetting

class UserInfo(Document):
    bucket_name = globalSetting['user_infoBucket']
    data = {
             'city':None,
             'url':None,
             'desc':None,
             }
    
    def __init__(self):
        Document.__init__(self)
        
