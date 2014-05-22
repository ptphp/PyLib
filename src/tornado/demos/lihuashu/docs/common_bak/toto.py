#coding:utf8
#from fdfs import Fdfs
#fs=Fdfs()
#fs.open()
from kyototycoon import KyotoTycoon
k=KyotoTycoon()
k.open()
po=k.set("编解码;编解码","编码编码编码编码编码",60)
print(po)
'''
p=k.remove('jia')
print(p)
'''
p=k.get_str("编解码;编解码")
print(p)