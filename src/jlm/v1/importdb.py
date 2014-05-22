# -*- coding: utf-8 -*-     
#mysqldb    
import time, MySQLdb, csv

#连接    
conn = MySQLdb.connect(host="localhost", user="root", passwd="", db="drupal7", charset="utf8")
cursor = conn.cursor()

def insertTable(sql, param):
    #写入
    #sql = "insert into category(category,parent) values(%s,%s)"    
    #param = (Category,parent)
    #print sql
    try:
        n = cursor.execute(sql, param)    
        conn.commit()
        return cursor.lastrowid
    except Exception as what:
        print what
        return False

#insert into `taxonomy_term_data` (vid, name, description, format, weight) values ( 3, 't', 'tt', 'filter_html', 0)
#insert into `taxonomy_term_hierarchy` (tid, parent) values (null, 0)
def updateVendor():    
    cursor = conn.cursor()
    #写入    
    sql = "select distinct Vendor_Number,Vendor_Name from tmp_products_"
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        Vendor_Number = row[0]
        Vendor_Name = row[1]
        sql_d = "insert into `taxonomy_term_data` (vid, name, description, format, weight) values ( 3, %s, %s, 'filter_html', 0)"
        param_d = (Vendor_Number, Vendor_Name)
        sql_h = "insert into `taxonomy_term_hierarchy` (tid, parent) values (%s, 0)"
        tid = insertTable(sql_d, param_d)
        print tid
        param_h = (tid)
        insertTable(sql_h, param_h)
        
def updateCategory1():    
    cursor = conn.cursor()
    #写入    
    #sql = "select distinct Category_1,Category_2,Category_3 from `tmp_products_` where Category_3 <> ''"
    #sql = "select distinct Category_1,Category_2 from `tmp_products_` where Category_2 <> ''"
    sql = "select distinct Category_1 from `tmp_products_` where Category_1 <> ''"
    cursor.execute(sql)
    rows = cursor.fetchall()
    i = 0
    for row in rows:
        category = row[0]
        category1 = row[0]
        sql_d = "insert into `taxonomy_term_data` (vid, name, description, format, weight) values ( 2, %s, %s, 'filter_html', 0)"
        param_d = (category, category1)
        sql_h = "insert into `taxonomy_term_hierarchy` (tid, parent) values (%s, 0)"
        tid = insertTable(sql_d, param_d)
        print tid
        param_h = (tid)
        insertTable(sql_h, param_h)
        
        
        print row
        i = i + 1
    print i


def queryParentId(name):
    sql = "select tid from `taxonomy_term_data` where name = %s"
    param = (name)
    cursor.execute(sql, param)
    res = cursor.fetchone()
    return res[0]



def updateCategory2():    
    cursor = conn.cursor()
    #写入    
    #sql = "select distinct Category_1,Category_2,Category_3 from `tmp_products_` where Category_3 <> ''"
    sql = "select distinct Category_1,Category_2 from `tmp_products_` where Category_2 <> ''"
    cursor.execute(sql)
    rows = cursor.fetchall()
    i = 0
    for row in rows:
        category1 = row[0]
        category2 = row[1]
        
        pid = queryParentId(category1)
        print pid
        i = i + 1
        #continue
        sql_d = "insert into `taxonomy_term_data` (vid, name, description, format, weight) values ( 2, %s, %s, 'filter_html', 0)"
        param_d = (category2, category2)
        sql_h = "insert into `taxonomy_term_hierarchy` (tid, parent) values (%s, %s)"
        tid = insertTable(sql_d, param_d)
        print tid
        print pid
        param_h = (tid, pid)
        insertTable(sql_h, param_h)
    print i

def queryParentCount(name, tid1):
    
    sql = "select d.name,d.tid,h.tid,h.parent from `taxonomy_term_data`  as d left join `taxonomy_term_hierarchy`  as h on d.tid = h.tid  where d.name = %s and h.parent = %s"
    param = (name, tid1)
    cursor.execute(sql, param)
    res = cursor.fetchone()
    #print res[1]
    #print len(res)
    return res[1]

def updateCategory3():    
    cursor = conn.cursor()
    #写入    
    sql = "select distinct Category_1,Category_2,Category_3 from `tmp_products_` where Category_3 <> ''"
    cursor.execute(sql)
    rows = cursor.fetchall()
    i = 0
    for row in rows:
        category1 = row[0]
        category2 = row[1]
        category3 = row[2]
        
        tid1 = queryParentId(category1)
        #print tid1
        pid = queryParentCount(category2, tid1)
        #print pid
        i = i + 1
        #continue
        sql_d = "insert into `taxonomy_term_data` (vid, name, description, format, weight) values ( 2, %s, %s, 'filter_html', 0)"
        param_d = (category3, category3)
        sql_h = "insert into `taxonomy_term_hierarchy` (tid, parent) values (%s, %s)"
        tid = insertTable(sql_d, param_d)
        print tid
        print pid
        param_h = (tid, pid)
        insertTable(sql_h, param_h)
    print i
#queryParentId("Auto Operators")
#updateCategory3()
#updateVendor()

def updateTid(id, tid):
    #写入
    sql = "update tmp_products_ set vid = %s where id = %s"    
    param = (tid, id)
    #print sql
    try:
        n = cursor.execute(sql, param)
        
    except Exception as what:
        print what
        return False
def updateCid(id, tid):
    #写入
    sql = "update tmp_products_ set cid = %s where id = %s"    
    param = (tid, id)
    #print sql
    try:
        n = cursor.execute(sql, param)
        
    except Exception as what:
        print what
        return False

def updateProductV():    
    cursor = conn.cursor()
    #写入    
    sql = "select t.id,t.Vendor_Number,d.tid from `tmp_products_`  as t left join taxonomy_term_data as d on t.Vendor_Number = d.name where d.vid =3"
    cursor.execute(sql)
    rows = cursor.fetchall()
    i = 0
    for row in rows:
        i = i + 1
        id = row[0]
        tid = row[2]
        print id, tid
        updateTid(id, tid)
    print i
    conn.commit()
    
def updateProductC():    
    cursor = conn.cursor()
    #写入    
    sql = """
    select t.Category_1,t.id,d.tid as d_tid,d.name from `tmp_products_`  as t 
left join taxonomy_term_data as d on t.Category_1  = d.name 
left join taxonomy_term_hierarchy as h on d.tid  = h.tid 
where t.Category_2 = '' and d.vid = 2 and h.parent= 0
    """
    
    cursor.execute(sql)
    rows = cursor.fetchall()
    i = 0
    for row in rows:
        i = i + 1
        id = row[1]
        tid = row[2]
        print id, tid
        updateCid(id, tid)
        
    print i
    conn.commit()
def updateProductC1():    
    cursor = conn.cursor()
    #写入    
    sql = """
    select Category_1,Category_2 from `tmp_products_` where Category_3 = '' and Category_2 <> ''
    """
    
    cursor.execute(sql)
    rows = cursor.fetchall()
    i = 0
    for row in rows:
        i = i + 1
        Category_1 = row[0]
        Category_2 = row[1]
        print Category_1, Category_2
        sql = """
        select parent from `taxonomy_term_hierarchy` where parent = %s
        """
        p = (Category_1)
        cursor.execute(sql, p)
        rows = cursor.fetchall()
        print rows
        #updateCid(id,tid)
        
    print i
    conn.commit()
    
def updateProductC3():    
    cursor = conn.cursor()
    #写入    
    sql = """
        select h.tid,h.parent,d.tid,d.name from `tmp_taxonomy_term_hierarchy`  as h left join taxonomy_term_data as d on h.tid = d.tid  where h.parent = 0
    """
    
    cursor.execute(sql)
    rows = cursor.fetchall()
    i = 0
    for row in rows:
        i = i + 1
        print row
       # continue
        sql = """
        update `tmp_taxonomy_term_hierarchy`  set Category_1 = %s where tid= %s and parent = %s
        """
        p = (row[3], row[0], row[1])
        cursor.execute(sql, p)
        
    print i
    conn.commit()    
def updateProductC4():    
    cursor = conn.cursor()
    #写入    
    sql = """
        select h.tid,h.parent,d.tid,d.name from `tmp_taxonomy_term_hierarchy`  as h left join taxonomy_term_data as d on h.parent = d.tid 
    """
    
    cursor.execute(sql)
    rows = cursor.fetchall()
    i = 0
    for row in rows:
        i = i + 1
        print row
        sql = """
        update `tmp_taxonomy_term_hierarchy`  set pname = %s where tid= %s and parent = %s
        """
        print row[3], row[0], row[1]
        p = (row[3], row[0], row[1])
        #cursor.execute(sql,p)
        cursor.execute(sql, p)
        #updateCid(id,tid)
        
    print i
    conn.commit()    

def updateProductC5():    
    cursor = conn.cursor()
    #写入    
    sql = """
        select h.tid,h.parent,d.tid,d.name from `tmp_taxonomy_term_hierarchy`  as h left join taxonomy_term_data as d on h.parent = d.tid 
    """
    
    cursor.execute(sql)
    rows = cursor.fetchall()
    i = 0
    for row in rows:
        i = i + 1
        print row
        sql = """
        update `tmp_taxonomy_term_hierarchy`  set pname = %s where tid= %s and parent = %s
        """
        print row[3], row[0], row[1]
        p = (row[3], row[0], row[1])
        #cursor.execute(sql,p)
        cursor.execute(sql, p)
        #updateCid(id,tid)
        
    print i
    conn.commit() 
updateProductC3()
cursor.close()
    #关闭    
conn.close()      

