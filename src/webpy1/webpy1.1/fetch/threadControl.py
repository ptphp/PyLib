#coding=UTF-8
'''
Created on 2011-7-5

@author: Administrator
'''
import threading
import fetch
from fetch import soufang
from fetch import ganji
from fetch import tongcheng58
class CThread(threading.Thread):
    def __init__(self,citycode,kind):
        threading.Thread.__init__(self,)
        self.cc=citycode
        self.k=kind
    def run(self):
        soufang=fetch.soufang.fetchData({"citycode":self.cc,"kind":self.k})
        soufang.start()
        sofang=fetch.sofang.fetchData({"citycode":self.cc,"kind":self.k})
        sofang.start()
        ganji=fetch.ganji.fetchData({"citycode":self.cc,"kind":self.k})
        ganji.start()
        tongcheng58=fetch.tongcheng58.fetchData({"citycode":self.cc,"kind":self.k})
        tongcheng58.start()
    def getRun(self):
        pass
    def getResult(self):
        pass
if __name__=="__main__":
    ct=CThread("su",'1')
    ct.start()
        
        
