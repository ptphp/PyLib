# -*- coding: utf-8 -*-
import re
import sys,hashlib,os

def checkPath(f2,var):
    f1 = os.getcwd()
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
    
def makePath(f2,var):
    f1 = os.getcwd()
    hash = hashlib.md5(var).hexdigest().upper() #@UndefinedVariable
    h1 = str(hash[0:2])+"\\"
    h2 = str(hash[2:4])+"\\"
    h3 = str(hash[4:6])+"\\"
    h4 = str(hash[6:])+"\\"
    path = f1+"\\"+f2+"\\"+h1+h2+h3+h4
#    print path
    if not os.path.isdir(path):
        os.makedirs(path)
def removePath(f2,var):
    f1 = os.getcwd()
    print f1
    hash = hashlib.md5(var).hexdigest().upper() #@UndefinedVariable
    h1 = str(hash[0:2])+"\\"
    h2 = str(hash[2:4])+"\\"
    h3 = str(hash[4:6])+"\\"
    h4 = str(hash[6:])
    path = f1+"\\"+f2+"\\"+h1+h2+h3+h4
#    print path
    if os.path.isdir(path):
        os.rmdir(path)
def regx_data(regx,html,default,d= False,clean=False,rep=''):
    #print regx
    if re.search(regx, html):
        
        data = re.search(regx, html).group(1)
        if clean:
            print rep
            data = re.sub(clean,rep,data)
        if d:
            print data
        return data
    else:             
        return default
def regx_datas(regx,html,default,d= False,clean=False,rep=''):
    #print regx
    if re.findall(regx, html):
        
        _data = re.findall(regx, html)
        
        data = ''
        for r in _data:
           data = "%s|%s" % (r,data)
        if clean:
            data = re.sub(clean,rep,data)
        if d:
            print data   
        return data
    else:             
        return default
def regx_lists(regx,html,default,d= False,clean=False,rep=''):
    #print regx
    if re.findall(regx, html):
        
        _data = re.findall(regx, html)
        
        data = _data
        
        if clean:
            data = re.sub(clean,rep,data)
        if d:
            print data   
        return data
    else:             
        return default
def parseCondition(obj):
    table = obj['obj']
    field = ""
    if obj['field'] == "*":
        field = obj['field']
    else:        
        for i in obj['field']:
            field += ","+i
        field = field[1:]
    
    where = "1"
    for r in obj['where']:
        if obj['where']:
            where += " and "+r+" "+obj['where'][r]
    if obj['limit'] != 1:
        fromRow = obj['limit'] * obj['page']
        limits = "%d,%d" % (fromRow,obj['limit'])
    else:
        limits = 1
    order = "order by"
    for j in obj['order']:
        order += " "+j+" "+obj['order'][j]
    res = {}
    res['sql'] = "select %s from %s where %s %s limit %s" % (field,table,where,order, limits)
    res['count'] = "select count(id) as num from %s where %s " % (table,where)
    return res
def parseSql(infoT):
    sql = "insert into house(%s) values(%s)"
    zd = ""
    value = ""
    for k in infoT:
        if k != "pics":
            zd = "%s,%s" % (zd,k) 
            if str(infoT[k]).find("'") != -1:
                infoT[k] = infoT[k].replace("'","\"")
            value = "%s,'%s'" % (value,str(infoT[k])) 
    sql = sql % (zd[1:],value[1:])
    return sql

def delete_file_folder(src):
    '''delete files and folders'''
    if os.path.isfile(src):
        try:
            os.remove(src)
        except:
            pass
    elif os.path.isdir(src):
        for item in os.listdir(src):
            itemsrc=os.path.join(src,item)
            delete_file_folder(itemsrc) 
        try:
            os.rmdir(src)
        except:
            pass
if __name__ == "__main__":
    makePath("www","wwww")
    removePath("www","wwww")