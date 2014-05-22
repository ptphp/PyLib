#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: Joseph
@email:liseor@gmail.com
Created on 2012-7-20
'''
from riakClient.document import Document
from config.settings import globalSetting

class Pic(Document):
    bucket_name = globalSetting['picBucket']
    data = {
             'url':None,
             }
    
    def __init__(self):
        Document.__init__(self)
        
