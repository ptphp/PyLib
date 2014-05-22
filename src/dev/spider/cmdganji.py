#coding=UTF-8
'''
Created on 2011-7-15

@author: Administrator
'''
import threading
import ganji
from jjrlog import msglogger, LinkLog
import config
st1=3
st2=60
upc=5

citylist=config.citylist_gj

class startCityThread(threading.Thread):
    def __init__(self,city):
        threading.Thread.__init__(self)
        self.city=city
    def run(self):
        argsgj1={"citycode": self.city,"kind":"1","upc":upc,"st1":st1,"st2":st2}
        argsgj2={"citycode": self.city,"kind":"2","upc":upc,"st1":st1,"st2":st2}
        argsgj3={"citycode": self.city,"kind":"3","upc":upc,"st1":st1,"st2":st2}
        argsgj4={"citycode": self.city,"kind":"4","upc":upc,"st1":st1,"st2":st2}
        tgj1=threading.Thread(target=ganji.getLinks, args=(argsgj1,))
        tgj2=threading.Thread(target=ganji.getLinks, args=(argsgj2,))
        tgj3=threading.Thread(target=ganji.getLinks, args=(argsgj3,))
        tgj4=threading.Thread(target=ganji.getLinks, args=(argsgj4,))
        tgj1.start()
        tgj2.start()
        tgj3.start()
        tgj4.start()
def main():
    for city in citylist:
        startCityThread(city).start()
        msglogger.info("%s 线程启动"%city)
if __name__=="__main__":
    main()