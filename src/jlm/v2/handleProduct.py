#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: Joseph
@email:liseor@gmail.com
Created on 2012-6-10
'''
import MySQLdb,csv,time
import hashlib

class Product():
    def __init__(self):
        self.conn = MySQLdb.connect(host="127.0.0.1",user="logic",passwd="logic123",db="drupal7")
        self.cursor = self.conn.cursor()
    def delteTable(self):
        self.cursor.execute("drop table if exists jlm_product")
    def createTable(self):
        '''
        PRIMARY_VND_NUM
        VENDOR_NAME
        ITEM_NUM
        DESCRIPTION_1
        DESCRIPTION_2
        ITEM_CLASS
        DESCRIPTION
        CATEGORY_1
        CATEGORY_2
        CATEGORY_3
        '''
        sql = """
        CREATE TABLE IF NOT EXISTS `jlm_product` (
          `PRIMARY_VND_NUM` varchar(255) DEFAULT NULL,
          `VENDOR_NAME` varchar(255) DEFAULT NULL,
          `ITEM_NUM` varchar(255) NOT NULL DEFAULT '',
          `DESCRIPTION_1` varchar(255) DEFAULT NULL,
          `DESCRIPTION_2` varchar(255) DEFAULT NULL,
          `ITEM_CLASS` varchar(255) DEFAULT NULL,
          `DESCRIPTION` varchar(255) DEFAULT NULL,
          `CATEGORY_1` varchar(255) DEFAULT NULL,
          `CATEGORY_2` varchar(255) DEFAULT NULL,
          `CATEGORY_3` varchar(255) DEFAULT NULL,
          PRIMARY KEY (`ITEM_NUM`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        """
        print sql
        self.cursor.execute(sql)
        self.conn.commit()
                
    def getRows(self):
        cfile = open("product.csv")
        return csv.reader(cfile)
    def insertTabale(self):
        products = self.getRows()
        i = 0
        for PRIMARY_VND_NUM,VENDOR_NAME,ITEM_NUM,DESCRIPTION_1,DESCRIPTION_2,ITEM_CLASS,DESCRIPTION,CATEGORY_1,CATEGORY_2,CATEGORY_3 in products:
            #print PRIMARY_VND_NUM,VENDOR_NAME,ITEM_NUM,DESCRIPTION_1,DESCRIPTION_2,ITEM_CLASS,DESCRIPTION,CATEGORY_1,CATEGORY_2,CATEGORY_3
            i +=1
            if i == 1: continue
            print i            
            sql = "insert into jlm_product(`PRIMARY_VND_NUM`, `VENDOR_NAME`, `ITEM_NUM`, `DESCRIPTION_1`, `DESCRIPTION_2`, `ITEM_CLASS`, `DESCRIPTION`, `CATEGORY_1`, `CATEGORY_2`, `CATEGORY_3`)"
            sql +=" values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" 
            print sql
            param = (PRIMARY_VND_NUM.strip(),VENDOR_NAME.strip(),ITEM_NUM.strip(),DESCRIPTION_1.strip(),DESCRIPTION_2.strip(),ITEM_CLASS.strip(),DESCRIPTION.strip(),CATEGORY_1.strip(),CATEGORY_2.strip(),CATEGORY_3.strip())
            self.cursor.execute(sql,param)
        self.conn.commit()
    def getPorducts(self):
        
        self.cursor.execute("""
            select  p.ITEM_NUM , p.DESCRIPTION_1 , d.tid as vid,dd.tid as cid from jlm_product as p 
            left join taxonomy_term_data as d on p.VENDOR_NAME = d.name and d.vid = 3
            left join taxonomy_term_data as dd on p.CATEGORY_1 = dd.name and dd.vid = 2
            where dd.tid <> '' and d.tid <> ''
        """)
        
        return self.cursor.fetchall()
    def products(self,data):
        try:
            i = 0
            for row in data:
                print i
                i += 1
                t = int(time.time())
                title = row[0]
                desc = row[1]
                vid = row[2]
                catId = row[3]
                
                self.cursor.execute("""
                    INSERT INTO `node` (`type`, `language`, `title`, `uid`, `status`, `created`, `changed`, `comment`, `promote`, `sticky`, `tnid`, `translate`) VALUES
                    ('product', 'und', %s, 1, 1, %s, %s, 1, 1, 0, 0, 0)
                    """,(title,t,t))
                
                nid = self.cursor.lastrowid
                
                uid = hashlib.md5(str(nid)).hexdigest()
                
                self.cursor.execute("""
                    update `node` set `vid` = %s where nid = %s
                """,(nid,nid))                   
                
                self.cursor.execute("""
                    INSERT INTO `node_comment_statistics` (`nid`, `cid`, `last_comment_timestamp`, `last_comment_name`, `last_comment_uid`, `comment_count`) VALUES
                    (%s, 0, %s, null, 1, 0)
                    """,(nid,t))                
                
                self.cursor.execute("""
                    INSERT INTO `node_revision` (`nid`, `vid`, `uid`, `log`, `title`, `timestamp`, `status`, `comment`, `promote`, `sticky`) VALUES
                    (%s, %s, 1 , "",%s, %s, 1,1,1, 0)
                    """,(nid,nid,title,t))
                
                self.cursor.execute("""
                    INSERT INTO `field_data_body` (`entity_type`, `bundle`, `deleted`, `entity_id`, `revision_id`, `language`, `delta`, `body_value`, `body_summary`, `body_format`) VALUES
                    ('node', 'product', 0 , %s, %s, 'und' , 0 ,%s, '', 'filtered_html')
                    """,(nid,nid,desc))                
                
                self.cursor.execute("""                    
                    INSERT INTO `field_revision_body` (`entity_type`, `bundle`, `deleted`, `entity_id`, `revision_id`, `language`, `delta`, `body_value`, `body_summary`, `body_format`) VALUES
                    ('node', 'product', 0 , %s, %s, 'und' , 0 ,%s, '', 'filtered_html')
                    """,(nid,nid,desc))
                
                self.cursor.execute("""                    
                    INSERT INTO `field_data_taxonomy_catalog` (`entity_type`, `bundle`, `deleted`, `entity_id`, `revision_id`, `language`, `delta`, `taxonomy_catalog_tid`) VALUES
                    ('node', 'product', 0 , %s, %s, 'und' , 0 ,%s)
                    """,(nid,nid,catId))
                
                self.cursor.execute("""                    
                    INSERT INTO `field_revision_taxonomy_catalog` (`entity_type`, `bundle`, `deleted`, `entity_id`, `revision_id`, `language`, `delta`, `taxonomy_catalog_tid`) VALUES
                    ('node', 'product', 0 , %s, %s, 'und' , 0 ,%s)
                    """,(nid,nid,catId))
                
                self.cursor.execute("""                    
                    INSERT INTO `field_data_field_vendor` (`entity_type`, `bundle`, `deleted`, `entity_id`, `revision_id`, `language`, `delta`, `field_vendor_tid`) VALUES
                    ('node', 'product', 0 , %s, %s, 'und' , 0 ,%s)
                    """,(nid,nid,vid))
                
                self.cursor.execute("""                    
                    INSERT INTO `field_revision_field_vendor` (`entity_type`, `bundle`, `deleted`, `entity_id`, `revision_id`, `language`, `delta`, `field_vendor_tid`) VALUES
                    ('node', 'product', 0 , %s, %s, 'und' , 0 ,%s)
                    """,(nid,nid,vid))                
                
                self.cursor.execute("""                    
                    INSERT INTO `taxonomy_index` (`nid`, `tid`, `sticky`,`created`) VALUES
                    ( %s, %s , 0 , %s);
                    """,(nid,catId,t))
                
                self.cursor.execute("""                    
                    INSERT INTO `taxonomy_index` (`nid`, `tid`, `sticky`,`created`) VALUES
                    ( %s, %s , 0 , %s);
                    """,(nid,vid,t))
                
                self.cursor.execute("""                    
                    INSERT INTO `uc_ups_products` (`nid`, `vid`, `pkg_type`) VALUES
                    ( %s, %s , '02')
                    """,(nid,nid))
                
                self.cursor.execute("""                    
                    INSERT INTO `uc_usps_products` (`nid`, `vid`, `container`) VALUES
                    ( %s, %s , 'VARIABLE')
                    """,(nid,nid))
                
                self.cursor.execute("""                          
                    INSERT INTO `uc_products` (`nid`, `vid`, `model`, `list_price`, `cost`, `sell_price`, `weight`, `weight_units`, `length`, `width`, `height`, `length_units`, `pkg_qty`, `default_qty`, `unique_hash`, `ordering`, `shippable`) VALUES
                    (%s,%s,'sku',11.00,0,11.00,0,'1b',0,0,0,"in",1,1,%s,0,1)
                    """,(nid,nid,uid))
                
            #self.conn.rollback()    
            self.conn.commit()
        except Exception as what:
            print what
            self.conn.rollback()
        
    def getVendors(self):        
        self.cursor.execute("select DISTINCT VENDOR_NAME from jlm_product where VENDOR_NAME <> ''")
        return self.cursor.fetchall()
    
    def handleV(self,data):
        for row in data:
            
            self.cursor.execute("""
                    INSERT INTO `taxonomy_term_data` (`vid`,`name`, `description`, `format`, `weight`) VALUES
                    (3, %s, %s, 'filtered_html', 0)
                    """,(row[0],row[0]))
            id = self.cursor.lastrowid
            print id
            self.cursor.execute("""
                    INSERT INTO `taxonomy_term_hierarchy` (`tid`, `parent`) VALUES
                    ( %s , 0 )
                    """,(id))
        self.conn.commit()
        
    def initProduct(self):
        pass
        sql = """        
        TRUNCATE TABLE node;
        TRUNCATE TABLE node_comment_statistics;
        TRUNCATE TABLE node_revision;
        TRUNCATE TABLE field_data_body;
        TRUNCATE TABLE field_revision_body;
        TRUNCATE TABLE field_data_taxonomy_catalog;
        TRUNCATE TABLE field_revision_taxonomy_catalog;
        TRUNCATE TABLE taxonomy_index;
        TRUNCATE TABLE uc_ups_products;
        TRUNCATE TABLE uc_usps_products;
        TRUNCATE TABLE uc_products;
        TRUNCATE TABLE field_data_field_vendor;
        TRUNCATE TABLE field_revision_field_vendor
        """
        self.cursor.execute(sql)
        
    def run(self):
#------------------------------------------------------------------------------ create table

        #self.delteTable()
        #self.createTable()
        #self.insertTabale()        

#------------------------------------------------------------------------------ init product

        #self.initProduct()
        
#------------------------------------------------------------------------------ handle product

        data = self.getPorducts()
        self.products(data)   
        #print len(data)
        #print data[0]
        
        #t = []
        #t.append(data[0])
        #t.append(data[1])
        #self.products(t) 
             
#------------------------------------------------------------------------------ handle vendor

        #v = self.getVendors()
        #print len(v)
        #self.handleV(v)        
        pass    
    
if __name__ == '__main__':
    p = Product()
    p.run()
    