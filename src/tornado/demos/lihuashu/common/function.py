#coding:utf8
import sys,os
import hashlib
import binascii
import time
from urllib import unquote
import logging
import simplejson as json

#from config.settings import settings
settings= {}
settings['debug']  = True
def dump(data):	
	if settings['debug'] is False:
		return	
	logging.basicConfig(
					filename="log.log",
					datefmt='%m/%d/%Y %I:%M:%S %p',
					format='%(levelname)s %(asctime)s :%(message)s',
					level =logging.WARN,
					filemode='w'
					)
	logging.warn(json.dumps(data))
	
def urldecode(uri1): 
	uri = uri1.split("?")[1]
	result={}
	for i in uri.split("&"):
		i=i.split("=",1)
		if len(i)==2:
			result[unquote(i[0])]=unquote(i[1])
	return result 

def formatTime(str):
	strTime = int(str)
	nowTime = int(time.time())
	spaceTime = nowTime - strTime
	if spaceTime < 60:		
		return "刚才"
	if spaceTime >= 60 and spaceTime < 3600:
		return "%d 分钟 前" % int(spaceTime/60)
	if spaceTime >= 3600 and spaceTime < 3600*24:
		return "%d 小时 前" % int(spaceTime/3660)
	if spaceTime >= 3600*24 and spaceTime < 3600*24*7:
		return "%d 天 前" % int(spaceTime/(3600*24))
	if spaceTime >= 3600*24*7 and spaceTime < 3600*24*7*4:
		return "%d 周 前" % int(spaceTime/(3600*24*7))
	if spaceTime >= 3600*24*7*4 and spaceTime < 3600*24*7*4*12:
		return "%d 月 前" % int(spaceTime/(3600*24*7*4))
	if spaceTime >= 3600*24*7*4*12:
		return "%d 年 前" % int(spaceTime/(3600*24*7*4*12))
	
def GetFileCRC32(filename):
	if not os.path.isfile(filename):
		return
	try: 
		blocksize = 1024 * 2
		f = open(filename,"rb") 
		str = f.read(blocksize) 
		crc = 0 
		while(len(str) != 0): 
			crc = binascii.crc32(str, crc) 
			str = f.read(blocksize) 
		f.close() 
	except: 
		print('get file crc error!')
		return 0 
	return crc

#大文件的MD5值
def GetFileMd5(filename):
	if not os.path.isfile(filename):
		return
	myhash = hashlib.md5()
	f = open(filename,'rb')
	while True:
		b = f.read(8096)
		if not b :
			break
		myhash.update(b)
	f.close()
	return myhash.hexdigest().upper()
#----------------------------------------------------


#大文件的SHA256值
def GetFileSHA256(filename):
	if not os.path.isfile(filename):
		return
	myhash = hashlib.sha256()
	f = open(filename,'rb')
	while True:
		b = f.read(8096)
		if not b :
			break
		myhash.update(b)
	f.close()
	return myhash.hexdigest().upper()
#----------------------------------------------------
#for email

def isEmail(email):
	import re
	p = re.compile(r"\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*")
	m=p.match(email)
	if (not m):
		return False
	else:
		return True
#----------------------------------------------------
if __name__ == "__main__":
	dump()
	dump()