#coding=UTF-8
'''
Created on 2011-7-5

@author: Administrator
'''
import threading
import soufang
class CThread(threading.Thread):
    def __init__(self,citycode,kind):
        threading.Thread.__init__(self,)
        self.cc=citycode
        self.k=kind
    def run(self):
        soufang.getDict({"citycode":self.cc,"kind":self.k})
        
if __name__=="__main__":
    ct=CThread("su",'1')
    ct.start()
        
        
