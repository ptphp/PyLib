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
		self.resize(680, 500)
		icon2 = QtGui.QIcon()
		icon2.addPixmap(QtGui.QPixmap("title.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.setWindowIcon(icon2)
		l = self.layout()
		l.setMargin(0)
		#self.curl = 'http://localhost/jquery.mobile-1.0/jquery.mobile-1.0/jquery.mobile-1.0.docs/jquery.mobile-1.0/'		
		self.curl = "http://client.fangtee.com/"
		self.ui.webView.setUrl(QtCore.QUrl(_fromUtf8(self.curl)))
		self.ui.webView.page().mainFrame().javaScriptWindowObjectCleared.connect(self.populateJavaScriptWindowObject)
		self.mainFrame = self.ui.webView.page().mainFrame()
		
		QtCore.QObject.connect(self.ui.webView,QtCore.SIGNAL("linkClicked (const QUrl&)"), self.link_clicked)
		QtCore.QObject.connect(self.ui.webView,QtCore.SIGNAL("urlChanged (const QUrl&)"), self.link_clicked)
		QtCore.QObject.connect(self.ui.webView,QtCore.SIGNAL("loadProgress (int)"), self.load_progress)
		QtCore.QObject.connect(self.ui.webView,QtCore.SIGNAL("titleChanged (const QString&)"), self.title_changed)		
		QtCore.QMetaObject.connectSlotsByName(self)
		
		self.workerSql = WorkerSql()
		self.connect(self.workerSql, SIGNAL("updatePage(QString)"), self.updatePage)
		self.WorkerQeue = []
		self.calljs = CallJs()
		self.connect(self.calljs, SIGNAL("callBackFun(QString)"), self.callBackFun)
		self.username  = ''
	def resizeMax(self):
		#self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
		desktop = QtGui.QApplication.desktop()
		rect = desktop.availableGeometry()
		self.setGeometry(rect)
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
	def execJs(self,methodJS):
		self.mainFrame.evaluateJavaScript("""
			%s();					
		""" % methodJS)	
	
	def updatePage(self,s): 
		self.ui.url.setText("")
		
		s = "采集中... >>>> %s" % s
		self.ui.url.setText(_fromUtf8(s))
		del s
		
	@QtCore.pyqtSlot()
	def getUsername(self):
		self.mainFrame.evaluateJavaScript("""
			setUsername('%s');                  
		""" % self.username)	
		
	@QtCore.pyqtSlot()
	def setUsername(self):
		self.username = self.mainFrame.findFirstElement('#g_username').evaluateJavaScript("this.value")
	@QtCore.pyqtSlot()
	def getResult(self):
		param = self.mainFrame.findFirstElement('#param').evaluateJavaScript("this.value")
		#print param
		paramObj = json.loads(str(param))
		
		self.calljs.param = paramObj 
		self.calljs.start()
		self.calljs.wait()

	def callBackFun(self,callbak):		
		self.mainFrame.evaluateJavaScript("""
			callbackfunction(%s);                  
		""" % callbak)	
	def updateQueue(self,s): 
		id = int(s);
		if id in self.WorkerQeue:
			self.WorkerQeue.remove(id)

		s = "%s 结束" % s
		self.mainFrame.evaluateJavaScript("""
				loadSpider();                  
			""" )
		del s
	def getJsParam(self,id):
		threadData = self.mainFrame.findFirstElement('#'+id).evaluateJavaScript("this.value")
		#print threadData
		self.tData = json.loads(str(threadData))
		
		#print self.tData
		return self.tData
	@QtCore.pyqtSlot()
	def getThreadData(self):
		if self.WorkerQeue:
			s = json.dumps(self.WorkerQeue)
			print s
			self.mainFrame.evaluateJavaScript("""
				initThreadData();
				changeThreadSta(%s,1);                  
			""" % s)
		else:
			self.mainFrame.evaluateJavaScript("""
				initThreadData();
			""")
	@QtCore.pyqtSlot()
	def startAll(self):		
		self.getJsParam("threadData");
		#print len(self.WorkerQeue)
		self.workArr = {}
		for list in self.tData:
			
			if list['id'] not in self.WorkerQeue:
				#print self.tData
				self.WorkerQeue.append(list['id'])
				#开启线程
				self.workArr[list['name']] = Worker()
				self.workArr[list['name']]._init(list)
				self.connect(self.workArr[list['name']], SIGNAL("updateQueue(QString)"), self.updateQueue) 
			print list['name']+"启动"
	@QtCore.pyqtSlot()
	def stopAll(self):		
		#self.getJsParam("threadData");
		#print len(self.WorkerQeue)
		#for list in self.tData:
			#if list['id'] in self.WorkerQeue:
				#print self.tData
				#try:
					#self.workArr[list['id']].terminate()
				#except Exception,what:
					#pass
				#else:
					#self.WorkerQeue.remove(list['id'])
		
		for row in self.workArr:
			print row
			self.workArr[row].terminate()

	@QtCore.pyqtSlot()
	def start(self):		
		self.getJsParam("threadData");
		#print len(self.WorkerQeue)
		self.workArr = {}
		if self.tData['id'] not in self.WorkerQeue:
			self.tData['status'] = 1
			#print self.tData
			self.WorkerQeue.append(self.tData['id'])
			#开启线程
			self.workArr[self.tData['name']] = Worker()
			self.workArr[self.tData['name']]._init(self.tData)
			self.connect(self.workArr[self.tData['name']], SIGNAL("updateQueue(QString)"), self.updateQueue) 
			print self.tData['name']+"启动"
			
		if self.workerSql != False:
			self.workerSql.start()
			 
	@QtCore.pyqtSlot()
	def stop(self):		
		self.getJsParam("threadData");
		if self.tData['id'] in self.WorkerQeue:
			self.workArr[self.tData['name']].terminate()
			self.WorkerQeue.remove(self.tData['id'])
			print self.tData['name']+"停止！"
			
	def title_changed(self, title):
		self.setWindowTitle(title)
		
	def link_clicked(self, url):
		pass
	
	def load_progress(self, load):
		if load == 100:
			pass#self.ui.stop.setEnabled(False)
		else:
			pass#self.ui.stop.setEnabled(True)
	@QtCore.pyqtSlot()
	def publish(self):	
		data = self.mainFrame.findFirstElement('#publishData').evaluateJavaScript("this.value")
		param = json.loads(str(data))
		print param
		pub = WorkerPub()
		pub.param = param
		pub.start()
		pub.wait()

class WorkerSql(QThread):
	def __init__(self, parent = None):
		QThread.__init__(self, parent)
		self.isStop = False
	def run(self):
		self.sqlObj = sqlModel.Db("fangtee.db")
		while 1:
			time.sleep(0.5)
			if _Queue:                
				row = _Queue.pop()
				sql = parseSql(row,'house')
				#print sql
				if checkPath("pagecash",str(row['url'])) == False:   
					self.sqlObj.query(sql,True)
					makePath("pagecach",str(row['url']))
				
				#self.emit(SIGNAL("updatePage(QString)"),"")
			elif self.isStop == True:
				break
			else:
				continue
				
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
		if self.param['webFlag'] == 1:			
			self.cc = fetch58.BaseCrawl(self.param,_Queue)
		elif self.param['webFlag'] == 2:			
			self.cc = fetchgj.BaseCrawl(self.param,_Queue)
		elif self.param['webFlag'] == 3:			
			self.cc = fetchbx.BaseCrawl(self.param,_Queue)
		if self.param['webFlag'] == 4:			
			self.cc = fetchsf.BaseCrawl(self.param,_Queue)

		self.start()
			
	def run(self):
		self.cc.run()
		self.emit(SIGNAL("updateQueue(QString)"),str(self.param['id']))	
		self.exec_() 
class WorkerPub(QThread):    
	param = {}
	def __init__(self, parent = None):	
		QThread.__init__(self, parent)
		self.moveToThread(self) 		
		self.param = {}
		self.stoped = False		

	def run(self):
		if self.param['webFlag'] == 2:			
			self.pp = Ganji.browser(self.param)
			self.pp.Publish()
			print self.pp.returnStr

class CallJs(QThread):
	sqlObj = None
	param  = None
	callBack = None
	def __init__(self, parent = None):
		QThread.__init__(self, parent)
	def run(self):			
		self.getRsult()
		self.emit(SIGNAL("callBackFun(QString)"),self.callBack)
	def getRsult(self):
		#获取列表		
		if self.param['type'] == 1:
			self.getList()
		elif self.param['type'] == 2:
			self.getOne()
		elif self.param['type'] == 3:
			self.remove()
		elif self.param['type'] == 4:			
			self.insert()
		elif self.param['type'] == 5:
			self.update()
			
	def getList(self):
		self.sqlObj = sqlModel.Db("fangtee.db")	
		#print self.param
		sql = parseCondition(self.param)
		count = self.sqlObj.count(sql['count'])
		self.sqlObj.query(sql['sql'])
		print self.sqlObj.sql
		
		res = self.sqlObj.showAll()
		self.paramBack = {}
		self.paramBack[u'count'] = count
		self.paramBack[u'result'] = res;	
		self.paramBack[u'type'] = self.param['type'];	
		self.paramBack[u'current_page'] = self.param['condition']['current_page'];		
		self.callBack = str(json.dumps(self.paramBack))
		#print self.callBack
		self.sqlObj = None
	def getOne(self):
		self.sqlObj = sqlModel.Db("fangtee.db")	
		#print self.param
		sql = parseCondition(self.param)
		self.sqlObj.query(sql['sql'])
		#print self.sqlObj.sql		
		res = self.sqlObj.showAll()
		self.paramBack = {}
		self.paramBack[u'result'] = res[0];	
		self.paramBack[u'type'] = self.param['type'];	
		self.callBack = str(json.dumps(self.paramBack))
		#print self.callBack
		self.sqlObj = None
	def remove(self):
		self.sqlObj = sqlModel.Db("fangtee.db")	
		#print self.param
		sql = deleteCondition(self.param)
		self.sqlObj.query(sql['sql'],True)
		#print self.sqlObj.sql		
		self.paramBack = {}
		self.paramBack[u'type'] = self.param['type'];	
		self.callBack = str(json.dumps(self.paramBack))
		self.sqlObj = None
	def update(self):
		self.sqlObj = sqlModel.Db("fangtee.db")	
		#print self.param
		sql = updateCondition(self.param)
		self.sqlObj.query(sql['sql'],True)
		print self.sqlObj.sql		
		self.paramBack = {}
		self.paramBack[u'type'] = self.param['type'];	
		self.callBack = str(json.dumps(self.paramBack))
		self.sqlObj = None
	def insert(self):
		self.sqlObj = sqlModel.Db("fangtee.db")	
		#print self.param
		sql = insertCondition(self.param)
		self.sqlObj.query(sql['sql'],True)
		#print self.sqlObj.sql		
		self.paramBack = {}
		self.paramBack[u'type'] = self.param['type'];	
		self.callBack = str(json.dumps(self.paramBack))
		self.sqlObj = None
	
if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)	
	myapp = httpWidget()
	myapp.show()
	#myapp.resizeMin()
	sys.exit(app.exec_())
