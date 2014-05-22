#!user/bin/env python
# -*- coding: utf8 -*- 
import tornado.web
class HomeHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('index.html')
	