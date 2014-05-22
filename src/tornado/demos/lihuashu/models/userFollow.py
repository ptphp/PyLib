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

class UserFollow(Document):
    bucket_name = globalSetting['userFollowBucket']
    data = {
             'follow':None,
             'user':None,
             'public':1,
             'createTime':None,
             }
    
    def __init__(self):
        Document.__init__(self)
        
    def formatBoards(self,board_data):
        data = []
        boardModel = Board()
        for board in board_data:
            #print "******************"
            _board = {}
            _board =  boardModel.get(board['board'])  
                
            _board['pin_pics'] = []
            board_pins_max = 9
            i = 0
            for pin_key in _board['pins']:
                thumb = Thumb()                
                thumb.data = thumb.get(pin_key)
                #print thumb.data
                i = i + 1
                if i <= board_pins_max and thumb.data:                
                    _board['pin_pics'].append(thumb.data['url'])    
            data.append(_board)      
        return data   
