#!/usr/bin/env python
#-*- coding:utf-8 -*-
import sys,hashlib,os


reload(sys)
sys.setdefaultencoding('utf-8') #@UndefinedVariable


def checkPath(f1,f2,var):
    hash = hashlib.md5(var).hexdigest().upper() #@UndefinedVariable
    h1 = str(hash[0:2])+"\\"
    h2 = str(hash[2:4])+"\\"
    h3 = str(hash[4:6])+"\\"
    h4 = str(hash[6:])+"\\"
    path = f1+f2+h1+h2+h3+h4
    if os.path.isdir(path):
        return True
    else:
        return False
    
def makePath(f1,f2,var):
    hash = hashlib.md5(var).hexdigest().upper() #@UndefinedVariable
    h1 = str(hash[0:2])+"\\"
    h2 = str(hash[2:4])+"\\"
    h3 = str(hash[4:6])+"\\"
    h4 = str(hash[6:])+"\\"
    path = f1+f2+h1+h2+h3+h4
#    print path
    if not os.path.isdir(path):
        os.makedirs(path)




def toward(str):
    if not str:
        return 6
    dict = { 
  5 : '东西',
  6 : '南北',
  7 : '东南',
  8 : '西南',
  9 : '东北',
  10 : '西北',
  1 :'东',
  2 : '南',
  3 : '西',
  4 : '北',
  }
    res = []
    for v in dict:
        if str.find(dict[v])!=-1:
            res.append(v)
    if res:
        if len(res)==1:
            return res[0]
        else:
            return res[len(res)-1]
def housetype_s(str):
    if not str:
        return 3
    dict ={
  2 : '平房',
  3 : '普通住宅',
  7 : '商住两用',
  4 : '公寓',
  5 : '别墅',
  6 : '其他',
}
    res =''
    for v in dict:
        if str.find(dict[v])!=-1:
            res+='%d,' % v
    return res
def house_room_s(str):
    if not str:
        return 2
    dict ={
  1 : '一居',
  2 : '二居',
  3 : '三居',
  4 : '四居',
}
    res =''
    for v in dict:
        if str.find(dict[v])!=-1:
            res+='%d,' % v
    return res
def house_room_s1(str):
    if str=='1室':        
        return 1
    if str=='2室':        
        return 2
    if str=='3室':        
        return 3
    if str=='4室':        
        return 4
    return 5

def housetype(str):
    if not str:
        return 6
    dict ={
  2 : '平房',
  3 : '普通住宅',
  7 : '商住两用',
  4 : '公寓',
  5 : '别墅',
  6 : '其他',
}
    for v in dict:
        if str.find(dict[v])!=-1:
            return v
    else:
        return 6
def payType(str):
    if str=='季':        
        return 3
    if str=='半年':        
        return 6
    if str=='年':        
        return 12
   
def fitment(str):
    if not str:
        return 2
    dict ={
  1 : '毛坯',
  2 : '中等装修',
  3 : '精装修',
  4 : '豪华装修',
}
    for v in dict:
        if str.find(dict[v])!=-1:
            return v
    else:
        return 2
def fitment_s(str):
    if not str:
        return 2
    dict ={
  1 : '毛坯',
  2 : '中等装修',
  3 : '精装修',
  4 : '豪华装修',
}
    res =''
    for v in dict:
        if str.find(dict[v])!=-1:
            res+='%d,' % v
    return res
    
def belong(str):
    if not str:
        return 0
    dict ={
  1 : '商品房',
  2 : '经济适用房',
  3 : '公房',
  4 : '使用权',
}
    for v in dict:
        if str.find(dict[v])!=-1:
            return v
    else:
        return 0
def install(str):
    if not str:
        return 0
    dict ={
  6 : '床',
  8 : '热水器',
  9 : ' 洗衣机',
  10 : ' 空调',
  11 : ' 冰箱',
  12 : ' 电视机',
  13 : '宽带',
}   
    res =''
    for v in dict:
        if str.find(dict[v])!=-1:
            res+='%d,' % v
    return res
def deposit(str):
    if not str:
        return 0
    dict ={
   2 : '面议',
  1 : '押一付三',
  3 : '押一付一',
  6 : '半年付',
  7 : '年付',
}
    for v in dict:
        if str.find(dict[v])!=-1:
            return v
    else:
        return 2
