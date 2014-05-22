#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: Joseph
@email:liseor@gmail.com
Created on 2012-7-20
'''
from riakClient.document import Document
from config.settings import globalSetting
from models.thumb import Thumb

class Board(Document):
    bucket_name = globalSetting['boardBucket']
    data = {
             'title':None,
             'user':None,
             'category':None,
             'user':None,
             'public':1,
             'follow':0,
             'createTime':None,
             'pins':[]
             }
    
    def formatBoards(self,board_data):
        data = []
        for board in board_data:
            #print "******************"
            _board = {}
            _board = board
            
            if board.has_key('pins'):
                if " " in board['pins']:
                    _board['pins'] =board['pins'].split(" ")
                else:
                    b_pins = []
                    b_pins.append(board['pins'])
                    _board['pins'] = b_pins   
            else:
                _board['pins'] = []
                
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
        
        
    def getDetailWithPinThumb(self,key):        
        data = self.get(key)   
        board_pins_pic = []
        board_pins_max = 9
        thumb = Thumb()
        i = 0
        
        for pin_key in data['pins']:
            i = i + 1
            if i > board_pins_max:
                break
            thumb_data = thumb.get(pin_key)
            if thumb_data:
                board_pins_pic.append(thumb_data['url'])            
        data['pin_pics'] = board_pins_pic        
        return data
        
        
    def getDetail(self,key):
        board = self.get(key)       
        return board
    
    def __init__(self):
        Document.__init__(self)
        
