#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: Joseph
@email:liseor@gmail.com
Created on 2012-7-20
'''
from riakClient.document import Document
from config.settings import globalSetting

from models.board import Board
from models.user import User
from models.userinfo import UserInfo
from models.pic import Pic
from models.thumb import Thumb
from models.avatar import Avatar
from models.comment import Comment
from models.category import Category

class PinHate(Document):
    bucket_name = globalSetting['pinHateBucket']
    data = {
             'pin':None,
             'user':None,
             'public':1,
             'createTime':None,
             }
    
    def __init__(self):
        Document.__init__(self)
        
