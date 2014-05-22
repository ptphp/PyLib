# coding=utf-8
import sys,re
import urllib2,urllib,sys,socket,re
from PyQt4.QtCore import *
import urllib,time
from BeautifulSoup import BeautifulSoup

reload(sys) 
sys.setdefaultencoding('utf-8') #@UndefinedVariable


class baseSpider(QThread):
    def __init__(self,parent = None):
        super(baseSpider,self).__init__(parent)
        self.suspended = False
        self.stoped = False
        self.mutex = QMutex()
    def _init(self,s,e):
        self.start_p = s
        self.end_p =e
    def start(self):
        with QMutexLocker(self.mutex):
            self.stoped = False
            
        #for i in range(self.start_p,self.end_p):
        for i in range(1,3):
            while self.suspended:
                self.wait()  
                return
            if self.stoped:
                return
            url ="http://www.99fang.com/service/agency/a1/?p=%d" % i
            print url            
            
            try:
                r = urllib2.urlopen(url).read()
                soup = BeautifulSoup(r)
                box = soup.find("div",{'class':'agency-call-box'})
                lis = box("li")
                for li in lis:
                    
                    tel = li.a.string
                    print tel
                    r =urllib2.urlopen("http://suzhou.jjr360.com/app.php?c=spider&a=index&city=&tel=%s" % tel)
                    print r.read()
            except:
                pass
            else:
                #self.emit(SIGNAL("updateTime()"))
                time.sleep(1)
    def stop(self):
        with QMutexLocker(self.mutex):
            self.stoped = True
            self.suspended = False
            
    def suspend(self):
        with QMutexLocker(self.mutex):
            self.suspended = True
            self.stoped = False
if __name__ == "__main__":
    c = baseSpider()
    c._init(1,3)
    c.start()
        