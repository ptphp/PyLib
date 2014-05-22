#coding=UTF-8
'''
Created on 2011-7-5

@author: Administrator
'''
import threading
import time
from spider import soufang
from spider import ganji
from spider import tongcheng58

from spider.threadpool import ThreadPool, makeRequests
import urllib2
import urllib
from spider.globalvars import fetch_quere
from spider.jjrlog import msglogger
import gc
import random
import spider

    
































gc.enable()
#gc.set_debug(gc.DEBUG_COLLECTABLE | gc.DEBUG_UNCOLLECTABLE | gc.DEBUG_INSTANCES | gc.DEBUG_OBJECTS)
coctn=True
def linksThead(list):
    
    global coctn
    while True:
        if coctn:
            for args in list:
                ts=[]
                p={"citycode":args[1],"kind":args[2]}
                mod=args[0]
                Tcls=getattr(spider,mod).getLinksThread(p)
                ts.append(Tcls)

            for t in ts:
                t.start()
        else:
            time.sleep(3)
        
class  fetchLinkThreadControl(threading.Thread):
    def __init__(self,data):
        threading.Thread.__init__(self)
        self.data=data
    def run(self):
#        global coctn
        lmain = ThreadPool(len(self.data))
        while True:
            if fetch_quere.empty():
#                coctn=False
                lrequests = makeRequests(self.runFunc, self.data, self.getResult)
                for lreq in lrequests:
                    lmain.putRequest(lreq)
                lmain.wait()
            else:
                time.sleep(3)
            print "*"*80
    def runFunc(self,args):
        p={"citycode":args[1],"kind":args[2]}
        mod=args[0]
        getattr(spider,mod).getLinks(p)
#        args[0].getLinks({"citycode":args[1],"kind":args[2]})
#        print "gc fetchLink------------->%s   ,    %s ,    %s"%(gc.collect(),len(gc.garbage),len(gc.get_objects()))
        del gc.garbage[:] 
        args=0
    def getResult(self,id,res):
        print "fetch_quere.qsize-----------------> %s"%fetch_quere.qsize()
#        for r in res[0]:
#            fetch_quere.put({"link":r,"args":res[1]})
    
class fetchDataThreadControl(threading.Thread):
    def __init__(self,psize):
        threading.Thread.__init__(self)
        self.psize=psize
    def run(self):
#        global coctn
        fmain = ThreadPool(self.psize)
        while True:
            if not fetch_quere.empty() :
                fdata=[]
#                coctn=False
                for i in range(self.psize):
                    try:
                        fdata.append(fetch_quere.get(0))
                    except Exception,e:
                        print "-=-==================%s"%e
#                        coctn=True
                        continue
                
                frequests = makeRequests(self.runFunc, fdata, self.getResult)
                for freq in frequests:
                    fmain.putRequest(freq)
                time.sleep(0.5)
#                main.poll()
                fmain.wait()
#            else:
#                coctn=True
            time.sleep(0.5)
            print "gc fetchData------------->%s   ,    %s ,    %s"%(gc.collect(),len(gc.garbage),len(gc.get_objects()))
            del gc.garbage[:]
            print "-----------------> %s"%fetch_quere.qsize()
            print "%"*60
    def runFunc(self,args):

        res=getattr(spider,args["mod"]).getContent(args["link"],args["citycode"],args["kind"])
        
#        res=cc.extractDict()
#        res=random.randint(1,5)
#        time.sleep(res)
#        msglogger.debug("%s%s"%(args["link"],res))
        args=0
        return res
    def getResult(self,id,res):
#        print res
#        return
        if res==None:
            return
        req=urllib2.Request("http://site.jjr360.com/app.php", urllib.urlencode(res))
        br=urllib2.build_opener()
        try:
            p=br.open(req).read().strip()
        except:
            p=None
        
        rs=""
        if p!=None and p!="":
            rs=p.decode('gbk')
        try:    
            msglogger.debug("%s---->%s"%(res,rs))
        except:
            print "Exception -------->%s"%res
        
#        print p.decode('gbk')

def maingogogo(data):
    fl=fetchLinkThreadControl(data)
    fl.start()
    print ""
    time.sleep(5)
    fd=fetchDataThreadControl(100)
    fd.setDaemon(True)
    fd.start()
if __name__=="__main__":
    

    data=[
#          ["tongcheng58","su","1"],
#          ["tongcheng58","su","2"],
          ["tongcheng58","cz","3"],
#          ["tongcheng58","su","4"],
##          [soufang,"su","1"],
#          ["ganji","su","1"],
#          ["ganji","su","2"],
#          ["ganji","su","3"],
#          ["ganji","su","4"],
          ]
#    linksThead(data)
    fl=fetchLinkThreadControl(data)
    fl.start()
    print ""
    time.sleep(5)
    fd=fetchDataThreadControl(100)
    fd.setDaemon(True)
    fd.start()

#    linksThead(data)
    
#    print getattr(spider,"tongcheng58")
#    lf=file("link.log")
#    idx=0
#    for line in lf.readlines():
#        lk=line.split('|')
#        fetch_quere.put({"mod":"tongcheng58","link":lk[1],"citycode":"su","kind":lk[0]})
#        idx=idx+1
#        if idx%25==0:
#            time.sleep(random.randint(1,30))



#    try:
#        ct=CThread("su",'1',3000,3)
#        ct.start()
#    except:
#        pass