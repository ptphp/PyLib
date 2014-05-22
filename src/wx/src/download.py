#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: observer
# email: jingchaohu@gmail.com
# blog: http://obmem.com
import os,sys
import urllib,urllib2,cookielib
import re
from time import time,sleep

path = os.path.dirname(os.path.realpath(sys.argv[0]))
islogin = False

def useproxy(proxy='http://localhost:3128'):
    proxies = {'http':proxy}
    proxy_support = urllib2.ProxyHandler(proxies)
    opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
    urllib2.install_opener(opener)
    global isproxy
    isproxy = True

def login():
    print 'try to login...'
    cookie=cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie),urllib2.HTTPHandler)
    urllib2.install_opener(opener)
    print '...getting login form...'
    postdata=urllib.urlencode({'username':'simcdple',
                           'password':'simcdple',
                           'continue':'http://www.verycd.com/',
                           'login_submit':'登录',
                           'save_cookie':1,
    })
    req = urllib2.Request(
        url = 'http://www.verycd.com/signin',
        data = postdata
    )
    req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6')
    req.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    req.add_header('Accept-Encoding','gzip,deflate')
    print '...login form submitted'
    result = urllib2.urlopen(req)
    print '...login succeed!'
    global islogin
    islogin = True

#functions
def report(blocknum, bs, size, t):
    if t == 0:
        t = 1
    if size == -1:
        print '%10s' % (str(blocknum*bs)) + ' downloaded | Speed =' + '%5.2f' % (bs/t/1024) + 'KB/s'
    else:
        percent = int(blocknum*bs*100/size)
        print '%10s' % (str(blocknum*bs)) + '/' + str(size) + 'downloaded | ' + str(percent) + '% Speed =' + '%5.2f'%(bs/t/1024) + 'KB/s'
    
def httpfetch(url, headers={}, reporthook=report, postData=None, report=True, needlogin=False):
    ok = False
    if 'counters' not in url:
        headers['Accept-Encoding']='gzip,deflate'
    if not islogin:
        login()
    for _ in range(10):
        try:
            reqObj = urllib2.Request(url, postData, headers)
            fp = urllib2.urlopen(reqObj)
            headers = fp.info()
            ok = True
            break
        except:
            sleep(1)
            continue            

    if not ok:
        open(path+'/errors','a').write(url+'\n')
        return ''

    rawdata = ''
    bs = 1024*8
    size = -1
    read = 0
    blocknum = 0
    
    if reporthook and report:
        if "content-length" in headers:
            size = int(headers["Content-Length"])
        reporthook(blocknum, bs, size, 1)
        
    t0 = time()
    while 1:
        block = ''
        try:
            block = fp.read(bs)
        except:
            open(path+'/errors','a').write(url+'\n')
            return ''
        if block == "":
            print '...',url,'downloaded' 
            break
        rawdata += block
        read += len(block)
        blocknum += 1
        if reporthook and report:
            reporthook(blocknum, bs, size, time()-t0)
        t0 = time()
            
    # raise exception if actual size does not match content-length header
    if size >= 0 and read < size:
        return ''
        #raise ContentTooShortError("retrieval incomplete: got only %i out "
       #                             "of %i bytes" % (read, size), result)

    if 'counters' not in url:
        try:
            import StringIO
            compressedstream = StringIO.StringIO(rawdata)   
            import gzip
            gzipper = gzip.GzipFile(fileobj=compressedstream)   
            data = gzipper.read()
        except:
            data = rawdata
    else:
        data = rawdata

    return data
    
if __name__ == '__main__':    
    url = 'http://www.verycd.com/topics/2788317'

    #test it
    data = httpfetch(url)
    open('down','w').write(data)

