# -*- coding: utf-8 -*-     
import time, MySQLdb, csv

#连接    
conn = MySQLdb.connect(host="localhost", user="root", passwd="", db="drupal7", charset="utf8")
cursor = conn.cursor()



#===============================================================================
# Main Table:  tmp_products_ 
# Slave Table: taxonomy_term_data (tid,name)
# Slave Table: taxonomy_term_hierarchy (tid,parent)
# 
#===============================================================================
#更新 product vendor id
def updateProductVendor(): 
    sql = """
    select p.id,p.Item_Number,p.Vendor_Number,d.tid from tmp_products_ as p left join taxonomy_term_data as d on d.name = p.Vendor_number where d.vid = 3
    """
    cursor.execute(sql)
    rows = cursor.fetchall()
    i = 0
    for row in rows:
        i = i + 1
        #print row
        id = row[0]
        vid = row[3]
        param = (vid, id)
        print param
        sql1 = ""
        sql1 = "update tmp_products_ set vid = %s where id = %s"
        cursor.execute(sql1, param)
    print i
    conn.commit()
    print len(rows)

#更新 product cid
#产品分类�?��分类
def updateProductCategory1(): 
    sql = """
    select p.id,p.Item_Number,p.Category_1,p.Category_2,d.name,d.tid from tmp_products_ as p 
    left join taxonomy_term_data as d  on p.Category_1 =  d.name
    left join taxonomy_term_hierarchy as h on h.tid = d.tid
    where d.vid = 2 and p.Category_2 = '' and h.parent = 0
    """
    cursor.execute(sql)
    rows = cursor.fetchall()
    i = 0
    for row in rows:
        i = i + 1
        print row
        id = row[0]
        vid = row[5]
        param = (vid, id)
        #print param
        sql1 = ""
        sql1 = "update tmp_products_ set cid = %s where id = %s"
        #cursor.execute(sql1,param)
    print i
    conn.commit()
    print len(rows)
#更新 product cid
#产品分类二级分类
def updateProductCategory2(): 
    
    sql = """
    select     
    p.id,p.Item_Number,p.Category_1,p.Category_2,p.Category_3,
    d.tid ,d.name,
    h.tid,h.parent    
    from tmp_products_ as p 
    left join taxonomy_term_data as d  on p.Category_2 =  d.name
    left join taxonomy_term_data as dd  on p.Category_1 =  dd.name    
    left join taxonomy_term_hierarchy as h on h.tid = d.tid and dd.tid = h.parent    
    where d.vid = 2 and p.Category_3 = '' and p.Category_2 <> '' and h.parent > 0 
    """
    cursor.execute(sql)
    rows = cursor.fetchall()
    i = 0
    for row in rows:
        i = i + 1
        print row
        id = row[0]
        vid = row[5]
        param = (vid, id)
        #print param
        sql1 = ""
        sql1 = "update tmp_products_ set cid = %s where id = %s"
        #cursor.execute(sql1,param)
    print i
    conn.commit()
    print len(rows)

#更新 product cid
#产品分类三级分类
def updateProductCategory3(): 
    
    sql = """
    select     
    p.id,p.Item_Number,p.Category_1,p.Category_2,p.Category_3,
    d.tid ,d.name,
    h.tid,h.parent    
    from tmp_products_ as p 
    left join taxonomy_term_data as d  on p.Category_3 =  d.name
    left join taxonomy_term_data as dd  on p.Category_2 =  dd.name    
    left join taxonomy_term_hierarchy as h on h.tid = d.tid and dd.tid = h.parent    
    where d.vid = 2 and p.Category_3 <> '' and h.parent > 0 
    """
    cursor.execute(sql)
    rows = cursor.fetchall()
    i = 0
    for row in rows:
        i = i + 1
        print row
        id = row[0]
        vid = row[5]
        param = (vid, id)
        #print param
        sql1 = ""
        sql1 = "update tmp_products_ set cid = %s where id = %s"
        #cursor.execute(sql1,param)
    print i
    conn.commit()
    print len(rows)
    #13719 + 5245 + 730


#updateProductVendor()
updateProductCategory1()
#updateProductCategory2()
#updateProductCategory3()
print 13719 + 5245 + 730


cursor.close()
#关闭    
conn.close()      


