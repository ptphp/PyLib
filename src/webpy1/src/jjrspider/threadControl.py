#coding=UTF-8
'''
Created on 2011-7-13

@author: Administrator
'''
import threading
import tongcheng58
import ganji
import soufun
from optparse import OptionParser
import cmdganji
import cmdsoufun
import cmdtc58

def getArgsDict(l):
    tplargs=("citycode","kind","upc","st1","st2")   
    args={}
    for k in range(len(tplargs)):
        try:
            args[tplargs[k]]=l[k]
        except:
            raise
    return args
def main():
    print u"-模块名 -citycode -kind -电话最大发帖数  -链接访问间隔  -整体循环间隔"
    
    while True:
        ta= raw_input('Enter Arguments: ')
        args=ta.strip().split(" ")
        if len(args)==6:
            mod=eval(args[0])
            dic={}
            try:
                dic=getArgsDict(args[1:])
            except:
                continue
            print dic
            to=threading.Thread(target=mod.getLinks, args=(dic,))
            to.setDaemon(True)
            to.start()
            print u"线程启动"
            
        else:
            print u"参数错误"
#  
def main2():
    cmdganji.main()
    cmdsoufun.main()
    cmdtc58.main()       
if __name__ == "__main__":   
    main2()   

#args581={"citycode":"su","kind":"1","upc":"5","st1":"3","st2":"60"}
#args582={"citycode":"su","kind":"2","upc":"5","st1":"3","st2":"60"}
#args583={"citycode":"su","kind":"3","upc":"5","st1":"3","st2":"60"}
#args584={"citycode":"su","kind":"4","upc":"5","st1":"3","st2":"60"}
#argsgj1={"citycode":"su","kind":"1","upc":"5","st1":"3","st2":"60"}
#argsgj2={"citycode":"su","kind":"2","upc":"5","st1":"3","st2":"60"}
#argsgj3={"citycode":"su","kind":"3","upc":"5","st1":"3","st2":"60"}
#argsgj4={"citycode":"su","kind":"4","upc":"5","st1":"3","st2":"60"}
#soufun1={"citycode":"suzhou","kind":"1","upc":"5","st1":"3","st2":"60"}
#soufun2={"citycode":"suzhou","kind":"2","upc":"5","st1":"3","st2":"60"}
#soufun3={"citycode":"suzhou","kind":"3","upc":"5","st1":"3","st2":"60"}
#soufun4={"citycode":"suzhou","kind":"4","upc":"5","st1":"3","st2":"60"}
#t581=threading.Thread(target=tongcheng58.getLinks, args=(args581,))
#t582=threading.Thread(target=tongcheng58.getLinks, args=(args582,))
#t583=threading.Thread(target=tongcheng58.getLinks, args=(args583,))
#t584=threading.Thread(target=tongcheng58.getLinks, args=(args584,))
#tgj1=threading.Thread(target=ganji.getLinks, args=(argsgj1,))
#tgj2=threading.Thread(target=ganji.getLinks, args=(argsgj2,))
#tgj3=threading.Thread(target=ganji.getLinks, args=(argsgj3,))
#tgj4=threading.Thread(target=ganji.getLinks, args=(argsgj4,))
#tsf1=threading.Thread(target=soufun.getLinks, args=(soufun1,))
#tsf2=threading.Thread(target=soufun.getLinks, args=(soufun2,))
#tsf3=threading.Thread(target=soufun.getLinks, args=(soufun3,))
#tsf4=threading.Thread(target=soufun.getLinks, args=(soufun4,))
#
#t581.start()
#t582.start()
#t583.start()
#t584.start()
#tgj1.start()
#tgj2.start()
#tgj3.start()
#tgj4.start()
##
#tsf1.start()
#tsf2.start()
#tsf3.start()
#tsf4.start()