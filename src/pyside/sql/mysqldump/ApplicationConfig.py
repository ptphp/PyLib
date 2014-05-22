#!/usr/bin/env python
# -*- coding=utf-8 -*-
'''
Created on 2013-2-2

@author: Joseph
'''

import ConfigParser

########################################################################
class  ApplicationConfig:
    """
    程序相关配置信息
    """

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        self.remoteIp = "127.0.0.1"
        self.remotePort= "3306"
        self.user = "root"
        self.password = ""
        self.databasename= ""
        self.backupdir = "c:\\"
        self.config = ConfigParser.ConfigParser()
    
    #----------------------------------------------------------------------
    def load(self):
        """
        加载配置信息
        """    
        try: 
            self.config.read(r".\ApplicationConfig.cfg")   
            self.remoteIp = self.config.get("mysql", "remoteip")  
            self.remotePort = self.config.get("mysql", "remoteport")
            self.user = self.config.get("mysql", "user")
            self.password = self.config.get("mysql", "password")
            self.databasename = self.config.get("mysql", "databasename")
            self.backupdir = self.config.get("mysql", "backupdir")
        except Exception as ex:
            print "Some exception occured when invoke load(), exception message is ", ex, " please check it !"
            
    #----------------------------------------------------------------------
    def save(self):
        """
        保存配置信息
        """
        self.config.read(r".\ApplicationConfig.cfg")
        if "mysql" not in self.config.sections():
            self.config.add_section("mysql")
        self.config.set("mysql", "remoteip", self.remoteIp)
        self.config.set("mysql", "remoteport", self.remotePort)
        self.config.set("mysql", "user", self.user)
        self.config.set("mysql", "password", self.password)
        self.config.set("mysql", "databasename", self.databasename)
        self.config.set("mysql", "backupdir", self.backupdir)
        fp= open(r".\ApplicationConfig.cfg", "w")
        self.config.write(fp)
    #----------------------------------------------------------------------
    def __str__(self):
        """
        返回相应的字符串表示
        """
        description = "remoteip : \t" + self.remoteIp +  "\n"  + \
                      "user : \t" + self.user +  "\n" +\
                      "password : \t"+  self.password+  "\n"+ \
                      "databasename \t" + self.databasename + "\n" + \
                      "backupdir : \t" + self.backupdir + "\n"
        return description