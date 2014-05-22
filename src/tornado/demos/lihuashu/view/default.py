#!user/bin/env python
# -*- coding: utf8 -*- 
from .frontend import BaseHandler
from models.pin import Pin
from models.category import Category
import simplejson as json 
from config.settings import globalSetting
from common.function import urldecode,dump

class MentionsHandler(BaseHandler):	
	def get(self):
		self.render('mentions.html')

class ActivitiesHandler(BaseHandler):	
	def get(self):
		self.render('activities.html')

class HomeHandler(BaseHandler):	
	def get(self):
		uri = self.request.uri
		request = {}
		pin = Pin()
		
		pin_keys = pin.getByCat('All')
		pin_count = len(pin_keys)
		
		query = {}
		query['q'] 		= "public:1"				
		query['start']  = "0"
		query['rows']   = globalSetting['max_index_pin_rows']
		query['sort']   = "createTime"
		
		if "page" in uri:
			request = urldecode(uri)
			page = int(request['page'])
			query['start']  = query['rows']*page
			#If pin_count < query['rows']*page:
			#	return ''
		
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
			
			dump(marks)
			category = Category()
			cats = category.getCats()
			dump(cats)
			cat_key = 'All'
			
			self.render('index.html',user=self.currentUserInfo(),marks=marks,cats = cats,urlname = cat_key)		
	
class CategoryHandler(BaseHandler):	
	def get(self,cat_key):	
		if cat_key == 'All':
			self.redirect('/')
		else:
			uri = self.request.uri
			request = {}
			pin = Pin()
			
			pin_keys = pin.getByCat(cat_key)
			pin_count = len(pin_keys)
			
			query = {}
			query['q'] 		= "category:%s" % cat_key
					
			query['start']  = "0"
			query['rows']   = globalSetting['max_index_pin_rows']
			query['sort']   = "createTime"
			
			if "page" in uri:
				request = urldecode(uri)
				print request
				page = int(request['page'])
				query['start']  = query['rows']*page
				if pin_count < query['rows']*page:
					return ''
			
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
				return self.write(callback_response)
			else:
				marks = ''			
				for _mark_t in marks_dict:				
					marks = self.render_string('mark.html',mark=_mark_t)+marks
				if marks == '':
					marks = """
					<div class="pin category wfc isotope-item" style="margin-bottom: 15px; position: absolute; left: 0px; top: 0px; -webkit-transform: translate3d(0px, 0px, 0px); ">
					NO PINS
					</div>
					"""
				category = Category()
				cats = category.getCats()
				
				self.render('index.html',user=self.currentUserInfo(),marks=marks,cats = cats,urlname = cat_key)		
		