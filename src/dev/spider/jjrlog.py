#coding=UTF-8
'''
Created on 2011-7-11

@author: Administrator
'''
import logging
import os
import logging.handlers
logfile=os.getcwd()+os.sep+"msg.log"
msglogger=logging.getLogger("message")
handler=logging.handlers.RotatingFileHandler(logfile,maxBytes=1024*1000)#logging.FileHandler(logfile)
fmt = logging.Formatter("[%(asctime)s %(levelname)s]: %(message)s","%Y-%m-%d %H:%M:%S")
handler.setFormatter(fmt)
msglogger.addHandler(handler)
msglogger.setLevel(logging.DEBUG)
logfile=os.getcwd()+os.sep+"link.log"
LinkLog=logging.getLogger("link")
LinkLoghandler=logging.handlers.RotatingFileHandler(logfile,maxBytes=1024*1000)#logging.FileHandler(logfile)
LinkLogfmt = logging.Formatter("[%(asctime)s %(levelname)s]: %(message)s","%Y-%m-%d %H:%M:%S")
LinkLoghandler.setFormatter(LinkLogfmt)
LinkLog.addHandler(LinkLoghandler)
LinkLog.setLevel(logging.DEBUG)
if __name__=="__main__":
    msglogger.info("cccccccccccc")
    msglogger.debug("aaaaaaaaa")
    msglogger.info("cccccccccccc")
    msglogger.debug("aaaaaaaaa")
    LinkLog.debug("11111111111111111")
    LinkLog.info("11111111111111111")