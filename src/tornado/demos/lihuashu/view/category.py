#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: Joseph
@email:liseor@gmail.com
Created on 2012-7-19
'''
from view.frontend import BaseHandler
from models.category import Category

class AdminCategoryHandler(BaseHandler):
    def get(self):
        cat = Category()
        keys = cat.allKey()
        _data = cat.all(keys)        
        #self.dumpJson(_data)        
        self.render('manager/cat.html',data=_data)
        
class AdminCategoryNewHandler(BaseHandler):
    
    def get(self,key):
        cat = Category()
        data = {}     
        data['name']       = ''
        data['title']       = ''
        data['desc']        = ''
        data['group']       = ''
        data['order']       = ''
        data['key']         = ''
        
        if key:
            data                = cat.get(key)               
                   
        self.render('manager/cat_new.html',data = data)
                
    def post(self,id):        
        key          = self.get_argument("key",None)
        name         = self.get_argument("name",None)
        title        = self.get_argument("title",None)
        desc         = self.get_argument("desc",None)
        group        = self.get_argument("group",None)
        order        = self.get_argument("order",None)
        
        category = Category()
        if key:              
            category.key = key
            category.data = category.get(key)            
            category.data['name']        = name
            category.data['title']       = title
            category.data['desc']        = desc
            category.data['group']       = group
            category.data['order']       = order
            category.put()                 
        else:
            category.key                 = category.genKey(name)            
            category.data['name']        = name
            category.data['title']       = title
            category.data['desc']        = desc
            category.data['group']       = group
            category.data['order']       = order            
            
            category.post()
            #print res
            #self.dumpJson(category.data)            
        self.redirect('/manager/cat/')
      
class AdminDeleteCategoryHandler(BaseHandler):
    def get(self,key):
        cat = Category() 
         
        """
        for board in cat.cboards:   
            for pin in board.pin:                
                for comment in pin.pcomments:
                    pin.pcomments[0].delete()
                board.pin[0].delete()            
            cat.cboards[0].delete()
        """
        cat.delete(key)
