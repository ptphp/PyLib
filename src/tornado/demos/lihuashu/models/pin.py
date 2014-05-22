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

class Pin(Document):
    bucket_name = globalSetting['pinBucket']
    data = {
             'rawtext':None,
             'createTime':None,
             'board':None,
             'category':None,
             'user':None, 
             'public':1,
             'like':0,
             'hate':0,      
             }
    def getByCat(self,cat):
        if cat == 'All':
            return self.allKey()
        else:
            return self.getByKeyValues("category", cat)        
    
    def formatPins(self,data):        
        board = Board()
        user = User()
        thumb = Thumb()
        comment = Comment()    
        
        marks_dict = []
        
        for pin in data:
            _pin = {}
            _pin['pin']               = pin
            _pin['user']              = user.getDetail(pin['user'])
            _pin['thumb']             = thumb.get(pin['key'])
            
            _pin['board']             = board.getDetail(pin['board']) 
            #print _pin['board']
            _pin['comments']         = comment.getByPin( pin['key'])
            
            marks_dict.append(_pin)
            
        return marks_dict
    def getPinDetail(self,key):        
        board = Board()
        user = User()
        thumb = Thumb()        
        pic = Pic()        
        comment = Comment()    
        
        marks_dict = []
        pin = self.get(key)
        _pin = {}
        _pin['pin']               = self.get(key)
        _pin['user']              = user.getDetail(pin['user'])
        _pin['pin']['pic']        = pic.get(pin['key'])['url']
        
        
        _pin['board']             = board.getDetailWithPinThumb(pin['board']) 
        
        _pin['comments']         = comment.getByPin( pin['key'])           
            
        return _pin
    def __init__(self):
        Document.__init__(self)
        
