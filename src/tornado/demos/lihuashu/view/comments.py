#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: Joseph
@email:liseor@gmail.com
Created on 2012-7-19
'''
import tornado.web,os,time
from view.frontend import BaseHandler
import simplejson as json
from models.comment import Comment
from models.user import User
from models.userinfo import UserInfo

class AjaxCommentHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        import hashlib,time
        user_key      = self.get_secure_cookie('user_key')        
        pin_key       = self.get_argument("pinid",None)
        nickname      = self.get_secure_cookie('user_nickname')
        rawtext       = self.get_argument("text",None)
        res = {}
        if rawtext is None:
            res['code'] = 1
            res['data'] = "请输入评论"
            body = json.dumps(res)
            self.set_header("Content-Type", "text/json; charset=UTF-8")
            self.write(body)
        
        comment = Comment()
        _tmp = "%s%s" % (user_key,rawtext)
        key = comment.genKey(_tmp)
        
        comment.key = key
        comment.data['rawtext'] = rawtext
        comment.data['user']    = user_key
        comment.data['pin']     = pin_key
        comment.data['createTime']     = int(time.time())
        
        try: 
            comment.post()
        except Exception as what:
            print what
            res['code'] = 1
            res['data'] = what
        else:            
            res['code'] = 0
            res['data'] = "sucess"
            obj  = {}
            user = User()
            obj['key']        = comment.key
            obj['userInfo']   = user.getDetail(user_key)
            obj['rawtext']    = comment.data['rawtext']
            obj['createTime'] = comment.data['createTime']
            print obj['userInfo']
            res['obj'] = obj
          
        body = json.dumps(res)
        print body
        self.set_header("Content-Type", "text/json; charset=UTF-8")
        self.write(body)
       
class AdminCommentHandler(BaseHandler):
    def get(self):
        query = {}
        _data = []
        self.render('manager/comment.html',data=_data)
        
class AdminCommentNewHandler(BaseHandler):
    def get(self,key):
        pass
        
    def post(self,id):       
        pass
class AdminDeleteCommentHandler(BaseHandler):
    def get(self,key):
        obj = CommentModel.get(key) #@UndefinedVariable
        obj.delete()
        