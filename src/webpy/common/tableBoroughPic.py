#!/usr/bin/env python
#-*-coding:utf-8-*-
#===============================================================================
# 优化小区图片 户型图片表
#===============================================================================
from database import * 
import os.path as osp
import os
import shutil
db = Connection(host='127.0.0.1',database='hihouse',user='dbuser',password='201108')
rootPath = "E:\\home\\wwwroot\\jjr360v1.0\\site.jjr.com\\upfile\\"
desPath = "E:\\home\\house\\pic\\"
test = "borough/picture/bj/5c3449b7bed1c6d3ee9f06948c4ab088.jpg"

def copyFile(src):    
    if osp.isfile(rootPath+src):
        tmp = src.split("/")
        src1 = src.replace(tmp[-1], "")
        print src1
        if not osp.isdir(desPath+src1):
            os.makedirs(desPath+src1) 
        shutil.copy(rootPath+src,desPath+"/"+src)
        return True
    else:
        return False
#copyFile(test)     
for row in db.query('select pic_url from hi_borough_draw'):   
    if not copyFile(row.pic_url):
        db.execute("delete from hi_borough_draw where id = %s",row.id)
        print "delete"
    