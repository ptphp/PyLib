#!user/bin/env python
# -*- coding: utf8 -*- 
import tornado.web
import simplejson as json

class BaseHandler(tornado.web.RequestHandler):
	#current_user function must be call "get_current_user"
	#if not,the auth system will be not work!
	def dumpJson(self,dicts):
		#self.set_header("Content-Type", "application/json;charset=utf-8")
		self.write(json.dumps(dicts))
	def currentUserInfo(self):
		logined = "false"
		if self.get_secure_cookie('user_email'):
			logined = "true"
		user =  {
				'current_user':self.get_current_user,
	            'user_nickname':self.get_secure_cookie('user_nickname'),
	            'user_key':self.get_secure_cookie('user_key'),
	            'avatar':self.get_secure_cookie('user_avatar'),
	            'logined':logined
				}
		return user
	def get_current_user(self):
		if self.get_secure_cookie('user_email'):
			return str(self.get_secure_cookie('user_email'))
		else:
			return None


#404错误页面处理
class NotFoundHandler(BaseHandler):
	def get(self):
		self.render('404.html')