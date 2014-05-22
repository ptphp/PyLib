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
from models.pin import Pin

class PinLike(Document):
    bucket_name = globalSetting['pinLikeBucket']
    data = {
             'pin':None,
             'user':None,
             'public':1,
             'createTime':None,
             }
    
    def formatPins(self,data):    
        pin = Pin()    
        board = Board()
        user = User()
        thumb = Thumb()
        comment = Comment()    
        
        marks_dict = []
        
        for pin_row in data:
            _pin = {}
            _pin['pin']               = pin.get(pin_row['pin'])
            _pin['user']              = user.getDetail(pin_row['user'])
            _pin['thumb']             = thumb.get(pin_row['pin'])            
            _pin['board']             = board.getDetail(_pin['pin']['board']) 
            #print _pin['board']
            _pin['comments']         = comment.getByPin(pin_row['pin'])
            
            marks_dict.append(_pin)
            
        return marks_dict
    
    
    
    def __init__(self):
        Document.__init__(self)
        
