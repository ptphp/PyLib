#!user/bin/env python
# -*- coding: utf8 -*- 
from .frontend import BaseHandler
import tornado.web

class UploaderChoiceHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('upload_choice.html',current_user=self.current_user,current_user_nickname=self.get_secure_cookie('user_nickname'))

class UploaderFileHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('upload_file.html',current_user=self.current_user,current_user_nickname=self.get_secure_cookie('user_nickname'))

class UploaderFormHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):        
        self.render('upload_form.html',current_user=self.current_user,current_user_nickname=self.get_secure_cookie('user_nickname'))

class AjaxAddHandler(BaseHandler):
    def get(self):
        self.render('ajax/add.html')
        
class AjaxScrapeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('ajax/scrape.html')
        
class AjaxUploadHandler(BaseHandler):
    def get(self):
        self.render('ajax/upload.html')
        

   
        
        
        