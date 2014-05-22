#coding=UTF-8
'''
Created on 2011-7-15

@author: Administrator
'''
import threading
import tongcheng58
from jjrlog import msglogger, LinkLog
import config
st1=3
st2=60
upc=5

citylist=config.citylist_58

class startCityThread(threading.Thread):
    def __init__(self,city):
        threading.Thread.__init__(self)
        self.city=city
    def run(self):
        args581={"citycode": self.city,"kind":"1","upc":upc,"st1":st1,"st2":st2}
        args582={"citycode": self.city,"kind":"2","upc":upc,"st1":st1,"st2":st2}
        args583={"citycode": self.city,"kind":"3","upc":upc,"st1":st1,"st2":st2}
        args584={"citycode": self.city,"kind":"4","upc":upc,"st1":st1,"st2":st2}
        t581=threading.Thread(target=tongcheng58.getLinks, args=(args581,))
        t582=threading.Thread(target=tongcheng58.getLinks, args=(args582,))
        t583=threading.Thread(target=tongcheng58.getLinks, args=(args583,))
        t584=threading.Thread(target=tongcheng58.getLinks, args=(args584,))
        t581.start()
        t582.start()
        t583.start()
        t584.start()
def main():
    for city in citylist:
        startCityThread(city).start()
        msglogger.info("%s 线程启动"%city)
if __name__=="__main__":
    main()
