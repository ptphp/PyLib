#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: Joseph
@email:liseor@gmail.com
Created on 2012-7-20
'''
from riakClient.document import Document
from config.settings import globalSetting
from models.avatar import Avatar
from models.userinfo import UserInfo

class User(Document):
    bucket_name = globalSetting['userBucket']
    data = {
             'email':None,
             'password':None,
             'createTime':None,
             'nickname':None
             }
    def getInfo(self,key):
        userInfo = UserInfo()
        userInfo_data = userInfo.get(key)
        userDetail = self.getDetail(key)
        
        if userInfo_data:            
            userDetail['city'] = userInfo_data['city']
            userDetail['desc'] = userInfo_data['desc']
            userDetail['url'] = userInfo_data['url']
        else:
            userDetail['city'] = ''
            userDetail['desc'] = ''
            userDetail['url'] = ''
        return userDetail
    
    def getDetail(self,key):
        avatar = Avatar()
        avatar_data = avatar.get(key)
        
        user_data = self.get(key)
        #print user_data
        if avatar_data:
            user_data['avatar'] = avatar_data['url']
        else:
            user_data['avatar'] = ""            
        return user_data
    def getDetails(self,key):
        avatar = Avatar()
        avatar_data = avatar.get(key)
        
        user_data = self.getInfo(key)
        #print user_data
        if avatar_data:
            user_data['avatar'] = avatar_data['url']
        else:
            user_data['avatar'] = ""            
        return user_data
    
    def __init__(self):       
        Document.__init__(self)
        
