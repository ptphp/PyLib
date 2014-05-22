#trayIcon = QtGui.QSystemTrayIcon(QtGui.QIcon("res/fangtee.ico"), app)
        #trayIcon.showMessage("wwww","ddd")
        #menu = QtGui.QMenu()
        
        #quitAction= QtGui.QAction("&Quit ", self,
                                        #triggered=QtGui.qApp.quit)
        #exitAction = menu.addAction(quitAction)
        #trayIcon.setContextMenu(menu)
        #trayIcon.show() 
        # set margins
        
        #exit=QtGui.QAction(QtGui.QIcon('pix/Moon.bmp'),'Exit',self) #创建一个action "exti"为title self 为parent
        #exit.setSeparator(False)
        #exit.setShortcut('Ctrl+Q') #设置快捷键
        #exit.setShortcut(QKeySequence.New) # QKeySequence 保护标准的快捷按钮 QKeySequence.Paste
        #exit.setStatusTip('Exit Application') #设置状态栏说明
        #exit.setToolTip("exit") #设置tip
        #exit.setText("sdf") #设置title
        #exit.setWhatsThis("string") #设置what's this
        
        #self.connect(exit,QtCore.SIGNAL('triggered()'),QtCore.SLOT('close()')) #设置信号 插槽
        
        
        self.ui.start.setEnabled(False)
        self.ui.stop.setEnabled(True)
        threadData = self.mainFrame.findFirstElement('#threadData').evaluateJavaScript("this.value")
        print threadData
        self.data = json.loads(str(threadData))
        self.threadArr = []
        if len(self.data)>0:            
            for i in range(0,len(self.data)):                              
                self.threadArr.append(Worker()) 
                if self.threadArr[i].stop:            
                    self.threadArr[i]._init(self.data[i])
                
            self.tSql = WorkerSql()
            if self.tSql.stop:            
                self.tSql.start()
            else:
                self.tSql.stop = False
            self.connect(self.tSql, SIGNAL("updatePage(QString)"), self.updatePage)    
            
            if self.param['flag'] == 1:
            baseUrl = 'http://sh.58.com/ershoufang/0/pn%d/';               
        if self.param['flag'] == 2:
            baseUrl = 'http://sh.58.com/zufang/0/pn%d/?selpic=2';      
        if self.param['flag'] == 3:
            baseUrl = 'http://sh.58.com/ershoufang/0/h2/pn%d/';      
        if self.param['flag'] == 4:
            baseUrl = 'http://sh.58.com/qiuzu/0/pn%d/';      
        i = 1
        url = baseUrl % i
        self.__getLinks(url)
        
        
        self.endtime=str(datetime.date.today() -datetime.timedelta(days=7)) 