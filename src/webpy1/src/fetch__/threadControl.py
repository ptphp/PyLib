#coding=UTF-8
'''
Created on 2011-7-5

@author: Administrator
'''
import threading
import fetch,time
from fetch import soufang
from fetch import ganji
from fetch import tongcheng58
class CThread(threading.Thread):
    def __init__(self,citycode,kind,tst,lst):
        threading.Thread.__init__(self,)
        self.cc=citycode
        self.k=kind
        self.tst=tst
        self.lst=lst
    def run(self):
        while True:
            #soufang=fetch.soufang.fetchData({"citycode":self.cc,"kind":self.k,"st":self.lst})
            #soufang.start()
            #ganji=fetch.ganji.fetchData({"citycode":self.cc,"kind":self.k,"st":self.lst})
            #ganji.start()
            tongcheng58=fetch.tongcheng58.fetchData({"citycode":self.cc,"kind":self.k,"st":self.lst})
            tongcheng58.start()
            time.sleep(self.tst)
    def getRun(self):
        pass
    def getResult(self):
        pass
if __name__=="__main__":
    try:
        ct=CThread("su",'1',3000,3)
        ct.start()
    except:
        pass