# -*- coding: utf-8 -*-
import sys
import time
import sitecustomize
import json
import sip
sip.setapi('QVariant', 2)
from PyQt4 import QtCore,QtGui
from PyQt4.QtCore import QThread,SIGNAL,QMutex,QMutexLocker
import sqlModel
from common import *
from fetch import fetch58
from fetch import fetchgj
from fetch import fetchbx
from fetch import fetchsf
from publish import Ganji

try:
	_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
	_fromUtf8 = lambda s: s


from httpWidget import Ui_HttpWidget

_Queue = []

class httpWidget(QtGui.QWidget):
	def __init__(self, parent=None):
		super(httpWidget, self).__init__(parent)
		self.ui = Ui_HttpWidget()
		self.ui.setupUi(self)
		#self.ui.resizeMax()		
		#self.resizeMax()		
		#self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
		self.resize(1024, 768)
		icon2 = QtGui.QIcon()
		icon2.addPixmap(QtGui.QPixmap("title.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.setWindowIcon(icon2)
		l = self.layout()
		l.setMargin(0)
		
		self.curl = "assets/www/index.html"
		self.ui.webView.setUrl(QtCore.QUrl(_fromUtf8(self.curl)))
		self.ui.webView.page().mainFrame().javaScriptWindowObjectCleared.connect(self.populateJavaScriptWindowObject)
		self.mainFrame = self.ui.webView.page().mainFrame()
		

		QtCore.QMetaObject.connectSlotsByName(self)
		self.spider = Worker()
		self.connect(self.spider, SIGNAL("updatePage1(QString)"), self.updatePage1) 
		
		self.postHouse = PostHouse()
		self.connect(self.postHouse, SIGNAL("updatePage(QString)"), self.updatePage)
		self.WorkerQeue = []
		self.username  = ''
		self.spiderContnet = {}
	def resizeMax(self):
		#self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
		desktop = QtGui.QApplication.desktop()
		rect = desktop.availableGeometry()
		self.setGeometry(rect)
		#QString
		
	@QtCore.pyqtSlot("QString","QString","QString","QString")
	def getSpiderList(self,url,web_flag,house_flag,city):		
		print url,web_flag,house_flag
		param = {}
		param['web_flag'] 	= int(web_flag)
		param['house_flag'] = int(house_flag)
		param['url'] 		= str(url)
		param['city'] 		= int(city)
		
		if param['web_flag']   ==  1:			
			cc = fetch58.BaseCrawl(param,_Queue)
		elif param['web_flag'] ==  2:			
			cc = fetchgj.BaseCrawl(param,_Queue)
		elif param['web_flag'] ==  3:			
			cc = fetchbx.BaseCrawl(param,_Queue)
		elif param['web_flag'] ==  4:			
			cc = fetchsf.BaseCrawl(param,_Queue)
		cc.isTest =True
		cc.fetchList()
		print cc.Lists
		self.mainFrame.evaluateJavaScript("""
				parseSpiderList(%s);                  
			""" % json.dumps(cc.Lists))
	@QtCore.pyqtSlot()
	def saveContent(self):
		print self.spiderContnet
		if self.spiderContnet:
			url = "http://client.fangtee.com/houseapi/python"
			r = postContent(url,self.spiderContnet)
			self.mainFrame.evaluateJavaScript("""
				location.href="#house_list";					
			""" )
			self.mainFrame.evaluateJavaScript("""
				location.reload();					
			""" )	
			
	@QtCore.pyqtSlot("QString","QString","QString","QString")
	def fetchContent(self,url,web_flag,house_flag,city):		
		print url,web_flag,house_flag
		
		param = {}
		param['web_flag'] 	= int(web_flag)
		param['house_flag'] = int(house_flag)
		param['url'] 		= str(url)
		param['city'] 		= int(city)
		if param['web_flag']   ==  1:			
			cc = fetch58.BaseCrawl(param,_Queue)
		elif param['web_flag'] ==  2:			
			cc = fetchgj.BaseCrawl(param,_Queue)
		elif param['web_flag'] ==  3:			
			cc = fetchbx.BaseCrawl(param,_Queue)
		elif param['web_flag'] ==  4:			
			cc = fetchsf.BaseCrawl(param,_Queue)
		cc.fetchContent()
		self.spiderContnet = cc.infoT
		if cc.infoT['owner_title']:
			print str(json.dumps(cc.infoT))
			for i in cc.infoT:
				print i,cc.infoT[i]
				self.mainFrame.findFirstElement('#d_'+i).evaluateJavaScript("this.value = %s" % json.dumps(cc.infoT[i]))

	@QtCore.pyqtSlot()
	def resizeReg(self):		
		self.resize(680, 600)
	@QtCore.pyqtSlot()
	def resizeLogin(self):		
		self.resize(480, 420)
	@QtCore.pyqtSlot()
	def resizeNormal(self):		
		self.resize(1024, 768)
	def populateJavaScriptWindowObject(self):
		self.ui.webView.page().mainFrame().addToJavaScriptWindowObject('callApi', self)
	
	def updatePage1(self,s): 	
		self.mainFrame.evaluateJavaScript("""
				setSpiderState('%s');					
			""" % str(s))
		del s
	def updatePage(self,s): 	
		self.mainFrame.evaluateJavaScript("""
				setSpiderResult('%s');					
			""" % str(s))
		del s
	@QtCore.pyqtSlot("QString")
	def startSpider(self,data):
		tData = json.loads(str(data))		
		self.spider._init(tData)
		self.spider.start()
		self.postHouse.start()
		#tt.wait()
		
class PostHouse(QThread):
	def __init__(self, parent = None):
		QThread.__init__(self, parent)
	def run(self):
		while 1:			
			time.sleep(0.1)
			if _Queue:
				time.sleep(0.1)                
				row = _Queue.pop()
				#if checkPath("pagecash",str(row['url'])) == False: 
				url = "http://client.fangtee.com/houseapi/python"
				r = postContent(url,row)
				#makePath("pagecach",str(row['url']))
				res = "%s => %s" % (str(row['uptime']).encode("utf-8"),r)
				print res
				self.emit(SIGNAL("updatePage(QString)"),res)
				
class Worker(QThread):    
	param = {}
	def __init__(self, parent = None):	
		QThread.__init__(self, parent)
		self.moveToThread(self) 		
		self.param = {}
		self.stoped = False		
		self.mutex = QMutex()
		self.isRunC = False
	def _init(self,param):				
		self.param = param
		
		if self.param['web_flag'] == 1:			
			self.cc = fetch58.BaseCrawl(self.param,_Queue)
		elif self.param['web_flag'] == 2:
			self.cc = fetchgj.BaseCrawl(self.param,_Queue)
		elif self.param['web_flag'] == 3:			
			self.cc = fetchbx.BaseCrawl(self.param,_Queue)
		if self.param['web_flag'] == 4:			
			self.cc = fetchsf.BaseCrawl(self.param,_Queue)
		self.emit(SIGNAL("updatePage1(QString)"),"is feteching...")
	def run(self):
		self.cc.run()
		self.emit(SIGNAL("updatePage1(QString)"),"is finished...")
	def __del__(self):
		self.wait() 
		#self.exec_() 


	
if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)	
	myapp = httpWidget()
	myapp.show()
	#myapp.resizeMin()
	sys.exit(app.exec_())
