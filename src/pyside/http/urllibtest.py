# -*- coding: utf-8 -*-
import urllib  
import urllib2
def cbk(a, b, c):  
    '''''回调函数 
    @a: 已经下载的数据块 
    @b: 数据块的大小 
    @c: 远程文件的大小 
    '''  
    per = 100.0 * a * b / c  
    if per > 100:  
        per = 100  
    print '%.2f%%' % per  
  
url = u'http://i2.51fanli.net/logoimages90/images/upfile/淘宝网.gif?20120913'  
local = u'd:\\淘宝网.gif'  

print url
req = urllib2.urlopen(url)
res =  req.read()
open(local,"wb").write(res)
urllib.urlretrieve(url, local, cbk)