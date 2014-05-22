#!/usr/bin/pytthon
#-*-coding:utf-8 -*-
try:
        import json
except ImportError, e:
        import simplejson as json
from amqplib import client_0_8 as amqp
import os, traceback
from Queue import Queue
import thread
import parsebody
from dbMysql import *
import urllib,cookielib,urllib2,yaml,time
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers


mysql = MySQL()
headers = {'User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14',
           'Accept': 'text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5',
           'Accept-Language':'zh-cn,zh;q=0.5',
           'Accept-Charset':'gb2312,utf-8;q=0.7,*;q=0.7',
           'Keep-Alive':'300',
           'Connection':'keep-alive'}
class AMQPServer:
        def __init__(self, host='127.0.0.1:5672', userid="guest", passwd='guest',
                vhost='/', insist=False, max_thread=3):
                self.__conn = amqp.Connection(host=host, userid=userid,
                         password=passwd, virtual_host=vhost, insist=insist)
                self.__chan = self.__conn.channel()
                self.__tokens = Queue(max_thread)
                self.__func_dict = dict()
 
        def queue(self, name, durable=True, exclusive=False, auto_delete=False):
                self.qname = name
                self.__chan.queue_declare(queue=name, durable=durable,
                         exclusive=exclusive, auto_delete=auto_delete)
 
        def exchange(self, name, type='direct', durable=True, auto_delete=False):
                self.ex_name = name
                self.__chan.exchange_declare(exchange=name, type=type,
                        durable=durable, auto_delete=auto_delete)
 
        def bind(self, routing_key):
                self.__chan.queue_bind(queue=self.qname, exchange=self.ex_name,
                        routing_key=routing_key)
 
        def register_function(self, func, func_name):
                self.__func_dict[func_name] = func
 
        def __callback(self, message):
                #print "__callback: %s" % message.body
                data = json.loads(message.body)
                func_name = data['method']
                func_params = data['params']
                func = self.__func_dict.get(func_name, None)
                if not func:
                        return
                try:
                        func(**func_params)
                except Exception, ex:
                        print traceback.format_exc()
                finally:
                        self.__tokens.get(True)
 
        def __handle(self, message):
                self.__tokens.put(message, True)
                thread.start_new_thread(self.__callback, (message,))
 
        def serve_async(self, *args, **kwargs):
                thread.start_new_thread(self.serve_forever, args, kwargs)
 
        def serve_forever(self, exchange=None, queue=None, routing_key=None):
                if exchange:
                        self.exchange(exchange)
                if queue:
                        self.queue(queue)
                if routing_key:
                        self.bind(routing_key)
                self.__chan.basic_consume(queue=self.qname, no_ack=True,
                        callback=self.__handle, consumer_tag="consumer")
                while True:
                        try:
                                self.__chan.wait()
                        except Exception, ex:
                                print traceback.format_exc()
                                break
 
        def close(self):
                self.__chan.close()
                self.__conn.close()
def upimg(img):
    register_openers()
    datagen, headers1 = multipart_encode({"fileUploadInput": open(img,"rb"),
                                       "backFunction": "$.c.Uploader.finish"})
    for k in headers1:
        headers[k] =headers1[k]
    request = urllib2.Request("http://post.58.com/upPicWeb2.aspx", datagen, headers)
    r = urllib2.urlopen(request).read()
    if r :
        return parsebody.rect(r, " '(.*?)',")
    else:
        return False
def publish(msg):
        #print "Thread %s Recevied %s:" % (thread.get_ident(), msg)
        data = msg
        stime = time.time()
        print stime
        print data['type'],data['time']
        
        logindata={}
        logindata = data['login']
        
        postdata = {}
        postdata = data['post']
        id = data['attr']['id']
        attr = data['attr']
        #for item in postdata:
            #print item,postdata[item]
        
        cookie = cookielib.CookieJar()
        datagen = urllib.urlencode(logindata)
        request = urllib2.Request("http://post.58.com/ajax/?action=userreglogin",datagen, headers)
        httpsHandler = urllib2.HTTPHandler()        
        httpsHandler.set_http_debuglevel(1)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie),httpsHandler)
        
        # Actually do the request, and get the response
        result = opener.open(request).read()
        
        if result == "{result:'1', error:''}":
            #print opener.open("http://my.58.com").read()
            #postdata['fileUploadInput'] = ''
            #postdata['Pic'] = upimg(attr['img'])
            #postdata['PicDesc'] = ''
            #postdata['Content'] = '位于东环路沿线，公交路线众多！有园区多家厂车经过！还有家乐福就在对面，生活购物非常方便！房子精装修，有四个空调，其他家电家具都有！拎包入住！有意者从速！好房不等人！'
            #postdata['PicPos'] = 1
            for row in postdata:
                print row,postdata[row]
            time.sleep(0.0001)
            datapost =urllib.urlencode(postdata)
            
            request = urllib2.Request("http://post.58.com/5/8/s5/submit", datapost, headers)
            log = opener.open(request).read()
            #print log
            infoid = parsebody.rect(log, "infoid=(\d+)&")
            postpath = '/home/myapp/workspace/wwwroot/jjr/post/suzhou/'+id+'.html'            
            if infoid:
                           
                open(postpath,'w').write(str(time.time() - stime)+" 网址为:http://su.58.com/zufang/"+infoid+"x.shtml")
                print postpath
                print time.time()
                print time.time() - stime
            else:
                log = parsebody.rect(log, "'(.*?)'") if parsebody.rect(log, "'(.*?)'") else ''
                log1 = parsebody.rect(log, "'msg':\[(.*?)\]") if parsebody.rect(log, "'msg':\[(.*?)\]") else ''
                open(postpath,'w').write(log+log1)
                print postpath
                print time.time()
                print time.time() - stime
                
        
if __name__ == '__main__':
        
        MQ_EXCHANGE = 'amq.direct'
        MQ_QUEUE = 'rpc'
        MQ_ROUTING_KEY = 'rpc'
        mq_server = AMQPServer()
        mq_server.register_function(publish, 'publish')
        try:
                mq_server.serve_forever(MQ_EXCHANGE, MQ_QUEUE, MQ_ROUTING_KEY)
                #mq_server.serve_async(MQ_EXCHANGE, MQ_QUEUE, MQ_ROUTING_KEY)
        except KeyboardInterrupt:
                os.kill(os.getpid(), 9)
        finally:
                mq_server.close()