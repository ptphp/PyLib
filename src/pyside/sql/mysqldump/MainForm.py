#!/usr/bin/env python
# -*- coding=utf-8 -*-
'''
Created on 2013-2-2
@author: Joseph
'''
import sys

from PySide.QtCore import *
from PySide.QtGui import *
import os
import time
import subprocess
import zipfile


from ApplicationConfig import ApplicationConfig

class ConfigurationPage(QWidget):
    def __init__(self, parent=None):
        super(ConfigurationPage, self).__init__(parent)
        self.configGroup = QGroupBox(u"相关配置信息")
        
        self.remoteIPLabel = QLabel(u"数据库所在IP地址:")
        self.editRemoteIP = QLineEdit(u"数据库所在IP地址")
        self.remotePortLabel= QLabel(u"使用端口:")
        self.editPort = QLineEdit(u"使用端口")
        self.userLabel = QLabel(u"用户名:")
        self.editUser = QLineEdit(u"用户名")
        self.passwordLabel= QLabel(u"密码:")
        self.editPassword= QLineEdit(u"密码")
        self.dabasenameLabel= QLabel(u"数据库名:")
        self.editDatabaseName= QLineEdit(u"数据库名")
        self.backupdirLabel = QLabel(u"备份文件存放目录:")
        self.editBackupDir = QLineEdit(u"备份文件存放目录")
        self.browseButton = QPushButton(u"浏览")
        self.browseButton.clicked.connect(self.onBrowse)
        
        self.paremeterLayout= QGridLayout();
        self.paremeterLayout.addWidget(self.remoteIPLabel, 0, 0)
        self.paremeterLayout.addWidget(self.editRemoteIP, 0, 1, 1, 2)
        self.paremeterLayout.addWidget(self.remotePortLabel, 1, 0)
        self.paremeterLayout.addWidget(self.editPort, 1, 1, 1, 2)
        self.paremeterLayout.addWidget(self.userLabel, 2, 0)
        self.paremeterLayout.addWidget(self.editUser, 2, 1, 1, 2)
        self.paremeterLayout.addWidget(self.passwordLabel, 3, 0)
        self.paremeterLayout.addWidget(self.editPassword, 3, 1, 1, 2)
        self.paremeterLayout.addWidget(self.dabasenameLabel, 4, 0)
        self.paremeterLayout.addWidget(self.editDatabaseName, 4, 1, 1, 2)
        self.paremeterLayout.addWidget(self.backupdirLabel, 5, 0)
        self.paremeterLayout.addWidget(self.editBackupDir, 5, 1)
        self.paremeterLayout.addWidget(self.browseButton, 5, 2)
        
        self.btnSave = QPushButton(u"保存")
        self.btnSave.setMinimumHeight(50)
        self.btnSave.clicked.connect(self.onSave)
        
        self.configGroup.setLayout(self.paremeterLayout)
        
        self.mainLayout= QVBoxLayout()
        self.mainLayout.addWidget(self.configGroup)
        self.mainLayout.addSpacing(20)
        self.mainLayout.addWidget(self.btnSave)
        self.mainLayout.addStretch(1)
        
        self.setLayout(self.mainLayout)
        
        self.config = ApplicationConfig()
        self.doInitialize()
    #----------------------------------------------------------------------
    def onSave(self):
        """保存处理"""
        try:
            self.config.remoteIp = self.editRemoteIP.text()
            self.config.remotePort = self.editPort.text()
            self.config.user = self.editUser.text()
            self.config.password = self.editPassword.text()
            self.config.databasename = self.editDatabaseName.text()
            self.config.backupdir = self.editBackupDir.text()
            self.config.save()
        except:
            print "some exceptions occured when invoke onSave() method, please check it!"
        #print unicode(self.config.remoteIp)
    #----------------------------------------------------------------------
    def onBrowse(self):
        """选择目录"""
        directory= QFileDialog.getExistingDirectory(self, u"查找备份目录",
                                                    QDir.currentPath())
        if directory:
            self.editBackupDir.setText(directory)
        
    #----------------------------------------------------------------------
    def doInitialize(self):
        """初始化相关参数"""
        self.config.load()
        self.editRemoteIP.setText(unicode(self.config.remoteIp))
        self.editPort.setText(unicode(self.config.remotePort))
        self.editUser.setText(unicode(self.config.user))
        self.editPassword.setText(unicode(self.config.password))
        self.editDatabaseName.setText(unicode(self.config.databasename))
        self.editBackupDir.setText(unicode(self.config.backupdir))
        

########################################################################
class BackupThread(QThread):
    """备份数据库线程"""
    dataReady = Signal(object)
    config = ApplicationConfig()
    #----------------------------------------------------------------------
    def run(self):
        """具体执行部分"""
        self.dataReady.emit(u"正在执行，请稍后......")
        #加载配置信息
        self.config.load()
        #组织备份数据库所需要的命令
        filestamp= time.strftime("%Y-%m-%d")
        
        filename = "%s-%s.sql" % (self.config.databasename, filestamp)
        filename = os.path.join(self.config.backupdir, filename)
        #mysqldumpfile = os.path.join(os.getcwd(), "mysqldump.exe")
        mysqldumpfile = "mysqldump"
        command= "%s -u %s -p%s -h %s -e --opt -c %s" % (mysqldumpfile, self.config.user, self.config.password, self.config.remoteIp, self.config.databasename)
        print command
        pipe = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        #print pipe.stdout.readlines()
        #promptMsg= "".join(pipe.stdout.readlines())
        #print "promptMsg is:", promptMsg
        fp= open(filename, "w")
        item = None
        for line in pipe.stdout:
            fp.writelines(line)
            self.dataReady.emit(line)
        fp.close()
        completeMsg= "";
        #取出最后一个item，判断里面的内容是否包含
        if item is not None:
            text= item.text()
            if text.find("Dump completed") > 0:
                print "Completed"
                completeMsg = u"开始压缩，请稍后......"
                #计算压缩后的文件名
                compressedfilename= os.path.splittext(filename)[0] + ".zip" #@UndefinedVariable
                if self.compress(filename, compressedfilename):
                    completeMsg = u"压缩文件出错，请检查！"
                else:
                    completeMsg = u"操作已完成，请检查！"
            else:
                completeMsg = u"操作过程中出现错误，请检查！"
        else:
            completeMsg = u"操作过程中出现错误，请检查！"
        
        self.dataReady.emit(completeMsg)
    
########################################################################
class BackupPage(QWidget):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent=None):
        """Constructor"""
        super(BackupPage, self).__init__(parent)
        self.backupButton = QPushButton(u"备份数据库")
        self.backupButton.setMinimumHeight(50)
        self.backupButton.clicked.connect(self.doBackupOperation)
        self.labelPrompt = QLabel(u"提示信息") #执行结果显示
        self.listPrompt = QListWidget()
        self.labelPrompt.setWordWrap(True)
        self.layout = QVBoxLayout()
        self.layout.addStretch()
        self.layout.addWidget(self.backupButton)
        #self.layout.addSpacing(20)
        self.layout.addWidget(self.labelPrompt)
        self.layout.addWidget(self.listPrompt)
        self.layout.addStretch()
        self.config = ApplicationConfig()
        self.thread = BackupThread() #备份线程
        self.thread.dataReady.connect(self.updateUI, Qt.QueuedConnection)
        self.setLayout(self.layout)
    #----------------------------------------------------------------------
    def doBackupOperation(self):
        """执行备份数据库的任务"""
        #self.labelPrompt.setText(u"正在执行，请稍后......")
        ##加载配置信息
        #self.config.load()
        ##组织备份数据库所需要的命令
        #filestamp= time.strftime("%Y-%m-%d")
        
        #filename = "%s-%s.sql" % (self.config.databasename, filestamp)
        #filename = os.path.join(self.config.backupdir, filename)
        #mysqldumpfile = os.path.join(os.getcwd(), "mysqldump.exe")
        #command= "%s -u %s -p%s -h %s -e --opt -c %s" % (mysqldumpfile, self.config.user, self.config.password, self.config.remoteIp, self.config.databasename)
        #print command
        #pipe = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        #fp= open(filename, "w")
        #item = None
        #for line in pipe.stdout:
            #fp.writelines(line)
            #item = QListWidgetItem(line)
            #self.listPrompt.addItem(item)
            #if self.listPrompt.count() > 0:
                #self.listPrompt.setCurrentRow(self.listPrompt.count() - 1)
                #pass
        #fp.close()
        #self.listPrompt.setFocus()
        #completeMsg= "";
        ##取出最后一个item，判断里面的内容是否包含
        #if item is not None:
            #text= item.text()
            #if text.find("Dump completed") > 0:
                #print "Completed"
                #completeMsg = u"开始压缩，请稍后......"
                ##计算压缩后的文件名
                #compressedfilename= os.path.splittext(filename)[0] + ".zip"
                #if self.compress(filename, compressedfilename):
                    #completeMsg = u"压缩文件出错，请检查！"
                #else:
                    #completeMsg = u"操作已完成，请检查！"
            #else:
                #completeMsg = u"操作过程中出现错误，请检查！"
        #else:
            #completeMsg = u"操作过程中出现错误，请检查！"
        #self.labelPrompt.setText(completeMsg)
        
        self.thread.start() #启动线程
    #----------------------------------------------------------------------
    def updateUI(self, data):
        """更新UI部分处理"""
        item = QListWidgetItem(data)
        self.listPrompt.addItem(data)
        self.listPrompt.setFocus()
    #----------------------------------------------------------------------
    def compress(self, infilename, dstfilename, level = 9):
        """压缩"""
        result= False;
        try:
            zfile = zipfile.ZipFile(dstfilename, "w")
            zfile.write(infilename, os.path.split(infilename)[1])
            zfile.close()
            result = True
        except:
            print "some error occured when invoke (), please check it!"
            result = False
            
        return result;
        
        
########################################################################
class HelpPage(QWidget):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent=None):
        """Constructor"""
        super(HelpPage, self).__init__(parent)
        self.helpLabel = QLabel(u"使用说明:\n\t"
                                u"（1）备份数据前请检查相关配置信息是否正确\n\t"
                                u"（2）点击备份数据库按钮，等待本分操作完成\n\t"
                                u"（3）请留意备份过程中是否有错误信息\n\t")
        
        self.layout = QVBoxLayout()
        self.layout.addSpacing(10)
        self.layout.addWidget(self.helpLabel)
        self.layout.addStretch(1)
        
        self.setLayout(self.layout)
        
class MainDialog(QDialog):
    #----------------------------------------------------------------------
    def __init__(self, parent=None):
        """初始化函数
        """
        super(MainDialog, self).__init__(parent)
        
        #Create Widgets
        
        self.contentsWidget = QListWidget()
        self.contentsWidget.setViewMode(QListView.IconMode)
        self.contentsWidget.setIconSize(QSize(96, 84))
        self.contentsWidget.setMovement(QListView.Static)
        self.contentsWidget.setMaximumWidth(128 + 10)
        self.contentsWidget.setMinimumHeight((84 + 12 ) * 4)
        self.contentsWidget.setSpacing(12)
        
        self.pagesWidget = QStackedWidget()
        self.pagesWidget.addWidget(ConfigurationPage())
        self.pagesWidget.addWidget(BackupPage())
        self.pagesWidget.addWidget(HelpPage())
        
        self.closeButton = QPushButton(u"退出")

        self.createIcons()
        self.contentsWidget.setCurrentRow(0)

        self.closeButton.clicked.connect(self.close)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.addWidget(self.contentsWidget)
        self.horizontalLayout.addWidget(self.pagesWidget, 1)

        self.buttonsLayout = QHBoxLayout()
        self.buttonsLayout.addStretch(1)
        self.buttonsLayout.addWidget(self.closeButton)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.horizontalLayout)
        self.mainLayout.addSpacing(12)
        self.mainLayout.addLayout(self.buttonsLayout)
        
        self.setLayout(self.mainLayout)
        
        #Add button
        self.setWindowTitle(u"数据库备份")
        
    def changePage(self, current, previous):
        if not current:
            current = previous

        self.pagesWidget.setCurrentIndex(self.contentsWidget.row(current))

    def createIcons(self):
        configButton = QListWidgetItem(self.contentsWidget)
        configButton.setIcon(QIcon('./images/config.png'))
        configButton.setText(u"相关配置信息")
        configButton.setTextAlignment(Qt.AlignHCenter)
        configButton.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        updateButton = QListWidgetItem(self.contentsWidget)
        updateButton.setIcon(QIcon('./images/update.png'))
        updateButton.setText(u"备份")
        updateButton.setTextAlignment(Qt.AlignHCenter)
        updateButton.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        queryButton = QListWidgetItem(self.contentsWidget)
        queryButton.setIcon(QIcon('./images/query.png'))
        queryButton.setText(u"使用说明")
        queryButton.setTextAlignment(Qt.AlignHCenter)
        queryButton.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        self.contentsWidget.currentItemChanged.connect(self.changePage)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = MainDialog()
    form.show()
    sys.exit(app.exec_())
   