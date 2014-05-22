#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: Joseph
@email:liseor@gmail.com
Created on 2012-7-19
'''
import tornado.web
from view.frontend import BaseHandler
import simplejson as json
from config.settings import globalSetting

from models.user import User
from models.board import Board
from models.category import Category
from models.pin import Pin
from common.function import urldecode
from models.boardFollow import BoardFollow
import time

class FollowingHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        uri = self.request.uri
        request = {}
        board = BoardFollow()
        
        #in_keys = board.allKey()
        user_key = self.get_secure_cookie("user_key")
        query = {}
        query['q']         = "user:%s" % user_key
                
        query['start']  = "0"
        query['rows']   = globalSetting['max_index_board_rows']
        query['sort']   = "follow"
        
        if "page" in uri:
            request = urldecode(uri)
            page = int(request['page'])
            query['start']  = query['rows']*page
            #if pin_count < query['rows']*page:
            #    return ''
        
        board_data = board.solr(query)
        #print len(board_data)

        boards_dict = board.formatBoards(board_data)
        
        if request:
            #print request
            callback_result = {
                            'filter':'board:index',
                            'boards':boards_dict
                            }
            
            callback_response = "%s(%s)" % (request['callback'],json.dumps(callback_result))
            self.set_header("Content-Type", "text/html; charset=utf-8")            
            return self.write(callback_response)
        else:
            boards = ''            
            for _board_t in boards_dict:                
                boards = self.render_string('board_unit.html',board=_board_t) + boards
                
            user_key = self.get_secure_cookie("user_key")
            user = User()
            userInfo = user.getDetail(user_key)
            from models.userFollow import UserFollow
            userFollow = UserFollow()
            counts = {}
            pinM = Pin()
            boardM = Board()
            counts['fans'] = len(userFollow.getByKeyValues("follow", user_key)) 
            counts['pins'] = len(pinM.getByKeyValues("user", user_key)) 
            counts['boards'] = len(boardM.getByKeyValues("user", user_key)) 
            
            self.render('board_follow.html',counts=counts,userInfo = userInfo,user=self.currentUserInfo(),boards=boards) 


class FolllowHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self,key):        
        res = {}         
        user_key = self.get_secure_cookie("user_key")
        b_key = "%s%s" % (user_key,key)
        
        boardFollow = BoardFollow()
        
        if boardFollow.get(b_key):
            res['code'] = 1
            res['msg'] = "您已关注过了"
        else:
            board = Board()
            board.key = key
            board.data =  board.get(key)
            board.data['follow'] = int(board.data['follow']) + 1
            board.put()            
            boardFollow.key = b_key
            
            boardFollow.data['user'] = user_key
            boardFollow.data['board'] = key
            boardFollow.data['createTime'] = int(time.time())
            boardFollow.post()
            res['code'] = 0
            res['msg'] = "成功"
            print res                
        res_str = json.dumps(res)
        self.write(res_str)

class RemoveFolllowHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self,key):
        res = {} 
        res['code'] = 0
        res['msg'] = "成功"
        boardFollow = BoardFollow()
        user_key = self.get_secure_cookie("user_key")
        b_key = "%s%s" % (user_key,key)
        boardFollow.delete(b_key)
        res_str = json.dumps(res)
        self.write(res_str)

class BoardPinHandler(BaseHandler):
    def get(self,key):
        uri = self.request.uri
        request = {}
        pin = Pin()
        
        pin_keys = pin.getByKeyValues("board",key)
        pin_count = len(pin_keys)
        
        query = {}
        query['q']         = "board:%s" % key    
                
        query['start']  = "0"
        query['rows']   = globalSetting['max_index_pin_rows']
        query['sort']   = "createTime"
        
        if "page" in uri:
            request = urldecode(uri)
            page = int(request['page'])
            query['start']  = query['rows']*page
            if pin_count < query['rows']*page:
                return ''
        
        pin_data = pin.solr(query)
        print len(pin_data)
        
        marks_dict = pin.formatPins(pin_data)        
        
        if request:
            #print request['callback']
            #print request['page']            
            callback_result = {
                            'filter':'pin:index',
                            'pins':marks_dict
                            }
            
            callback_response = "%s(%s)" % (request['callback'],json.dumps(callback_result))
            self.set_header("Content-Type", "text/html; charset=utf-8")            
            return self.write(callback_response)
        else:
            marks = ''            
            for _mark_t in marks_dict:                
                marks = self.render_string('mark.html',mark=_mark_t)+marks
            board = Board()
            user = User()
            category = Category() 
     
            board_data = board.get(key)
            
            b_user = user.getDetail(board_data['user'])
            b_category = category.get(board_data['category'])
            b_keys = board.getByKeyValues("user", board_data['user'])
            
            if key in b_keys:
                b_keys.remove(key)
                
            b_boards = board.all(b_keys)
        
            self.render('board_pins_list.html',f_board = self.formatFollowBoardData(key), b_boards= b_boards,b_category = b_category,b_user=b_user,user=self.currentUserInfo(),board = board.get(key),marks=marks)
    def formatFollowBoardData(self,key):
        user_key = self.get_secure_cookie("user_key")
        f_board = {}
        if user_key:
            f_key = "%s%s" % (user_key,key)            
            boardFollow = BoardFollow()            
            if boardFollow.get(f_key):
                f_board['rel'] = 1
                f_board['str'] = "取消关注"
            else:
                f_board['rel'] = 0
                f_board['str'] = "关注"            
            
        else:
            f_board['rel'] = 0
            f_board['str'] = "关注"
        
        return f_board
        
class PopularHandler(BaseHandler):
    def get(self):
        uri = self.request.uri
        request = {}
        board = Board()
        
        pin_keys = board.allKey()
        
        query = {}
        query['q']         = "public:1"
                
        query['start']  = "0"
        query['rows']   = globalSetting['max_index_board_rows']
        query['sort']   = "follow"
        
        if "page" in uri:
            request = urldecode(uri)
            page = int(request['page'])
            query['start']  = query['rows']*page
            #if pin_count < query['rows']*page:
            #    return ''
        
        board_data = board.solr(query)
        print len(board_data)

        boards_dict = board.formatBoards(board_data)
        
        if request:
            #print request
            callback_result = {
                            'filter':'board:index',
                            'boards':boards_dict
                            }
            
            callback_response = "%s(%s)" % (request['callback'],json.dumps(callback_result))
            self.set_header("Content-Type", "text/html; charset=utf-8")            
            return self.write(callback_response)
        else:
            boards = ''            
            for _board_t in boards_dict:                
                boards = self.render_string('board_unit.html',board=_board_t) + boards
            
            self.render('board_pop.html',user=self.currentUserInfo(),boards=boards)    

class AjaxBoardHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):   
        category = Category()     
        keys = category.allKey()
        _data =  category.all(keys)
        #print _data        
        self.render('ajax/board.html',cats = _data)

class AjaxAddboardHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        import hashlib
        
        title = self.get_argument("title",None)
        category_key = self.get_argument("category", None)
        user_key = self.get_secure_cookie("user_key")
        
        board          = Board()

        res = {}
        try:
            import time
            _tmp = "%s%s" % (user_key,title)
            key = board.genKey(_tmp)
            board.key = key
            board.data['title'] = title
            board.data['user'] = user_key
            board.data['category'] = category_key          
            board.data['createTime'] = time.time()
            board.data['pins']    = []
            
            board.post()
        except Exception as what:
            print what
            res['code'] = 1
            res['data'] = what
        else:            
            res['code'] = 0
            res['data'] = "sucess"
            obj  = {}
            obj['key'] = board.key
            res['obj'] = obj
          
        body = json.dumps(res)
        print body
        self.set_header("Content-Type", "text/json; charset=UTF-8")
        self.write(body)
            

class AdminBoardHandler(BaseHandler):
    def get(self):        
        board = Board()
        keys = board.allKey()        
        _data = board.all(keys)
        print _data
        #self.dumpJson(keys)       
        self.render('manager/board.html',data=_data)
        
class AdminBoardNewHandler(BaseHandler):
    def get(self,key):
        user = User()
        
        categroy = Category()       
        user_keys = user.allKey()
        category_keys = categroy.allKey()
        
        _data_user =  user.all(user_keys)
        _data_category = categroy.all(category_keys)        
        data = {}
        if key:
            board = Board()
            board.data = board.get(key)
            data['title']       = board.data['title']
            data['key']         = board.data['key']
            data['user']        = board.data['user']
            data['category']    = board.data['category']
            data['createTime']    = board.data['createTime']
            data['follow']    = board.data['follow']
        else:            
            data['title']       = ''
            data['key']         = ''
            data['user']        = ''
            data['category']    = ''            
        
        self.render('manager/board_new.html',data = data,data_user = _data_user,data_category = _data_category)
                
    def post(self,id):
        import hashlib     
        key          = self.get_argument("key",None)
        title        = self.get_argument("title",None)
        
        user_key     = self.get_argument("user",None)
        category_key = self.get_argument("category",None)
                
        _tmp = "%s%s" % (user_key,title)        
        
        board                  = Board()
        user                  = User()
        user_data = user.get(user_key)
        nickname  = user_data['nickname']
        import time
        if key:            
            board.key              = key
            board.data             = board.get(key)
            board.data['user']     = user_key                
            board.data['category'] = category_key
            board.data['title']    = title 
            board.data['createTime']    = time.time() 
            board.data['key']      = key 
            print board.data            
            board.put()
        else:                               
            data = board.get(board.key)
            if data:
                print "exist"
            else:       
                board.key              = board.genKey(_tmp)
                board.data['user']     = user_key                
                board.data['category'] = category_key
                board.data['title']    = title   
                board.data['createTime']    = time.time() 
                board.data['key']      = board.key     
                board.data['pins']    = []      
                board.post()
                
        self.redirect('/manager/board/')
      
class AdminDeleteBoardHandler(BaseHandler):
    def get(self,key):
        board = Board()
        board.delete(key)
        
        
        