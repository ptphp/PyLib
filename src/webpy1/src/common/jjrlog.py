#coding=UTF-8
'''
Created on 2011-7-11

@author: Administrator
'''
import logging
import os
logfile=os.getcwd()+os.sep+"msg.log"
msglogger=logging.getLogger("message")
handler=logging.FileHandler(logfile)
fmt = logging.Formatter("[%(asctime)s %(levelname)s]: %(message)s","%Y-%m-%d %H:%M:%S")
handler.setFormatter(fmt)
msglogger.addHandler(handler)
msglogger.setLevel(logging.DEBUG)
    
if __name__=="__main__":
    msglogger.info("cccccccccccc")
    msglogger.debug("aaaaaaaaa")
    msglogger.info("cccccccccccc")
    msglogger.debug("aaaaaaaaa")