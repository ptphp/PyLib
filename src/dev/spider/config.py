#!/usr/bin/env python
#-*- coding:utf-8 -*-
import sys,hashlib,os
#add
isDEV=0
def getDefaultVal(flg):
    dict={}
    if str(flg)=="1":
        dict['house_flag']=1
        dict['borough_name']=""
        dict['house_addr']=""
        dict['house_title']=""
        dict['house_city']=""
        dict['house_region']=""
        dict['house_section']=""
        dict['house_type']=0
        dict['house_price']=0
        dict['house_area']=0
        dict['house_room']=0
        dict['house_hall']=0
        dict['house_toilet']=0
        dict['house_veranda']=0
        dict['house_topfloor']=0
        dict['house_floor']=0
        dict['house_age']=0
        dict['house_toward']=0
        dict['house_fitment']=0
        dict['house_feature']=""
        dict['house_belong']=0
        dict['house_desc']=""
        dict['owner_name']=""
        dict['owner_phone']=""
        dict['owner_phone_pic']=""
        dict['house_posttime']=""
    elif str(flg)=="2":
        dict['house_flag']=2
        dict['borough_name']=""
        dict['house_addr']=""
        dict['house_title']=""
        dict['house_city']=""
        dict['house_region']=""
        dict['house_section']=""
        dict['house_type']=0
        dict['house_price']=0
        dict['house_area']=0
        dict['house_deposit']=0
        dict['house_room']=0
        dict['house_hall']=0
        dict['house_toilet']=0
        dict['house_veranda']=0
        dict['house_topfloor']=0
        dict['house_floor']=0
        dict['house_age']=0
        dict['house_toward']=0
        dict['house_fitment']=0
        dict['house_feature']=""
        dict['house_desc']=""
        dict['owner_name']=""
        dict['owner_phone']=""
        dict['owner_phone_pic']=""
        dict['house_posttime']=""
    elif str(flg)=="3":
        dict['house_flag']=3
        dict['borough_name']=""
        dict['house_addr']=""
        dict['house_title']=""
        dict['house_city']=""
        dict['house_region']=""
        dict['house_section']=""
        dict['house_type']=0
        dict['house_price']=0
        dict['house_price_max']=0
        dict['house_area']=0
        dict['house_area_max']=0
        dict['house_room']=0
        dict['house_hall']=0
        dict['house_toilet']=0
        dict['house_veranda']=0
        dict['house_topfloor']=0
        dict['house_floor']=0
        dict['house_age']=0
        dict['house_toward']=0
        dict['house_fitment']=0
        dict['house_feature']=""
        dict['house_belong']=0
        dict['house_desc']=""
        dict['owner_name']=""
        dict['owner_phone']=""
        dict['owner_phone_pic']=""
        dict['house_posttime']=""
    else:
        
        dict['house_flag']=4
        dict['borough_name']=""
        dict['house_addr']=""
        dict['house_title']=""
        dict['house_city']=""
        dict['house_region']=""
        dict['house_section']=""
        dict['house_type'] =""
        dict['house_price']=0
        dict['house_price_max']=0
        dict['house_area']=0
        dict['house_area_max']=0
        dict['house_deposit']=""
        dict['house_room']=""
        dict['house_hall']=""
        dict['house_toilet']=""
        dict['house_veranda']=""
        dict['house_topfloor']=0
        dict['house_floor']=0
        dict['house_age']=0
        dict['house_toward']=0
        dict['house_fitment']=0
        dict['house_feature'] =""
        dict['house_desc'] =""
        dict['owner_name']=""
        dict['owner_phone']=""
        dict['owner_phone_pic']=""
        dict['house_posttime']=""
    return dict


#add end


#citylist_58=["su","cz","sh","wx","nb","nj","hz","zz"]
citylist_58=["su"]
#citylist_gj=["su","changzhou","sh","wx","nb","nj","hz","zz"]
citylist_gj=["su"]
#citylist_sf=["suzhou","ks","cz","sh","wuxi","nb","nanjing","hz","zz"]
citylist_sf=["ks"]
citynameDict_sf11 ={
    #add
    'su':u'苏州',                 
    'suzhou':u'苏州',
    'ks':u'昆山',
    'cz':u'常州',
    'sh':u'上海',
    'wuxi':u'无锡',
    'nb':u'宁波',
    'nj':u'南京',
    'hz':u'杭州',
    'zz':u'郑州',
    'nanjing':u'南京',
    }
citynameDict_sf ={
    'ks':u'昆山',
    }
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
