#!/usr/bin/env python
# -*- coding: utf-8 -*-

def makeLog(data,name):
    f = open('log_'+name+'.txt','a')
    
    if type(data) == dict:
        for row in data:
            f.write("------------\n")
            f.write(str(row)+" : \n"+str(data[row]).encode('gbk')+"\n")
    else:
        f.write(str(data).encode('gbk'))
    f.write("======================================================\n")
        
        
if __name__ =="__main__":
    d={"houseid":1,"name":"as中dfasd"}
    makeLog(d,"debug")
    