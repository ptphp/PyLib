#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: Joseph
@email:liseor@gmail.com
Created on 2012-7-19
'''
import tornado.web
from view.frontend import BaseHandler
from models.pin import Pin
import simplejson as json 
from config.settings import globalSetting
from common.function import urldecode,dump
from models.board import Board
from models.pic import Pic
from models.thumb import Thumb
from models.pinLike import PinLike
from models.pinHate import PinHate
import hashlib,time
class RemoveHateHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self,key):
        user_key = self.get_secure_cookie("user_key")
        pinHate = PinHate()
        l_key = hashlib.md5("%s%s" % (user_key,key)).hexdigest()
        res = {} 
        res['code'] = 0
        res['msg'] = "成功"
        pinHate.delete(l_key)
        res_str = json.dumps(res)
        self.write(res_str)
class HateHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self,key):
        user_key = self.get_secure_cookie("user_key")
        pinHate = PinHate()
        l_key = hashlib.md5("%s%s" % (user_key,key)).hexdigest()        
        l_data = pinHate.get(l_key) 
        res = {}
        if l_data:
            res['code'] = 1
            res['msg'] = "您已讨厌过"
        else :
            pinHate.key = l_key
            pinHate.data['user'] = user_key
            pinHate.data['pin'] = key
            pinHate.data['createTime'] = int(time.time())
            pinHate.post()
            pin =Pin()
            data = pin.get(key)               
            pin.key = key
            pin.data = data
            pin.data['hate'] = int(data['hate']) - 1
            pin.put()
            dump(data)
            res['code'] = 0
            res['msg'] = "成功"
        res_str = json.dumps(res)
        self.write(res_str)
class RemoveLikeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self,key):
        user_key = self.get_secure_cookie("user_key")
        pinLike = PinLike()
        l_key = hashlib.md5("%s%s" % (user_key,key)).hexdigest()
        res = {} 
        res['code'] = 0
        res['msg'] = "成功"
        pinLike.delete(l_key)
        res_str = json.dumps(res)
        self.write(res_str)
               
class LikeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self,key):
        user_key = self.get_secure_cookie("user_key")
        print user_key
        pinLike = PinLike()
        l_key = hashlib.md5("%s%s" % (user_key,key)).hexdigest()
        
        l_data = pinLike.get(l_key)     
        #return self.dumpJson(l_data) 
        res = {}  
        if l_data:
            res['code'] = 1
            res['msg'] = "您已喜欢过"
        else :
            pinLike.key = l_key
            pinLike.data['user'] = user_key
            pinLike.data['pin'] = key
            pinLike.data['createTime'] = int(time.time())
            pinLike.post()
            pin =Pin()
            data = pin.get(key)
            pin.key = key
            pin.data = data
            pin.data['like'] = int(data['like']) + 1
            pin.put()        
            dump(data)
            res['code'] = 0
            res['msg'] = "成功"
        res_str = json.dumps(res)
        self.write(res_str)
        
class RepinHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self,key):
        user_key = self.get_secure_cookie("user_key")
            
        board  = Board()
        query = {}
        query['q'] = "user:%s" % user_key            
        _data = board.solr(query)  
        
        thumb = Thumb()        
        pic = Pic() 
        
        pic_url = pic.get(key)['url']
        thumb_url = thumb.get(key)['url']
        
        self.render('repin.html',boards = _data,pic_url=pic_url,thumb_url=thumb_url)

class SearchHandler(BaseHandler):
    def get(self):
        uri = self.request.uri
        request = {}
        pin = Pin()
        request = urldecode(uri)
        q = request['q']    
        
        query = {}
        query['q']         = "rawtext:*%s*" % q                
        #query['start']  = "0"
        #query['rows']   = globalSetting['max_index_pin_rows']
        query['sort']   = "like"
        
        #if "page" in uri:
        #    page = int(request['page'])
        #    query['start']  = query['rows']*page
            #If pin_count < query['rows']*page:
            #    return ''
        
        pin_data = pin.solr(query)
        #print len(pin_data)        
        marks_dict = pin.formatPins(pin_data)
        
        #if request:
            #print request                
        #    callback_result = {
        #                    'filter':'pin:index',
        #                    'pins':marks_dict
        #                    }
            
        #    callback_response = "%s(%s)" % (request['callback'],json.dumps(callback_result))
        #    self.set_header("Content-Type", "text/html; charset=utf-8")            
        #    self.write(callback_response)
        #else:            
        marks = ''            
        for _mark_t in marks_dict:                
            marks = self.render_string('mark.html',mark=_mark_t)+marks

        self.render('pins_search.html',query = q,user=self.currentUserInfo(),marks=marks)  

class PopularHandler(BaseHandler):
    def get(self):
        uri = self.request.uri
        request = {}
        pin = Pin()
        
        
        query = {}
        query['q']         = "public:1"                
        query['start']  = "0"
        query['rows']   = globalSetting['max_index_pin_rows']
        query['sort']   = "like"
        
        if "page" in uri:
            request = urldecode(uri)
            page = int(request['page'])
            query['start']  = query['rows']*page
            #If pin_count < query['rows']*page:
            #    return ''
        
        pin_data = pin.solr(query)
        #print len(pin_data)        
        marks_dict = pin.formatPins(pin_data)
        
        if request:
            #print request                
            callback_result = {
                            'filter':'pin:index',
                            'pins':marks_dict
                            }
            
            callback_response = "%s(%s)" % (request['callback'],json.dumps(callback_result))
            self.set_header("Content-Type", "text/html; charset=utf-8")            
            self.write(callback_response)
        else:            
            marks = ''            
            for _mark_t in marks_dict:                
                marks = self.render_string('mark.html',mark=_mark_t)+marks

            self.render('pins_popular.html',user=self.currentUserInfo(),marks=marks)        

class MarkHandler(BaseHandler):
    def get(self,key):        
        pin = Pin()
        pin_data = pin.getPinDetail(key)
        
        user_key = self.get_secure_cookie("user_key")
        _l_data = {}
        _h_data = {}
        if user_key:
            pinLike = PinLike()
            pinHate = PinHate()
            
            l_key = hashlib.md5("%s%s" % (user_key,key)).hexdigest()
            h_key = l_key
            l_data = pinLike.get(l_key)
            h_data = pinHate.get(h_key)
            
            
            if l_data:
                _l_data['str'] = "取消喜欢"
                _l_data['rel'] = 1
            else:
                _l_data['str'] = "喜欢"
                _l_data['rel'] = 0
                
            
            if h_data:
                _h_data['str'] = "取消讨厌"
                _h_data['rel'] = 1
            else:
                _h_data['str'] = "讨厌"
                _h_data['rel'] = 0
        else:
            _l_data['str'] = "喜欢"
            _l_data['rel'] = 0
            _h_data['str'] = "讨厌"
            _h_data['rel'] = 0
        #print pin_data
        self.render('mark_template.html',user=self.currentUserInfo(),mark=pin_data,like = _l_data,hate = _h_data)
        
    @tornado.web.authenticated
    def post(self,markid):
        self.write(markid)


class AdminPinHandler(BaseHandler):
    def get(self):
        query = {}
        query['q']         = "public:1"                
        query['start']  = "0"
        query['rows']   = globalSetting['max_index_pin_rows']
        query['sort']   = "createTime"
        pin = Pin()
        pin_data = pin.solr(query)
        #print len(pin_data)        
        _data = pin.formatPins(pin_data)
        
        self.render('manager/pin.html',data=_data)
        
class AdminPinNewHandler(BaseHandler):
    def get(self,key):        
        pass
                
    def post(self,id):
        pass
      
class AdminDeletePinHandler(BaseHandler):
    def get(self,key):
        obj = Pin() 
        obj.delete(key)