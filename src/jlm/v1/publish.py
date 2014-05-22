#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cookielib
import urllib2
import mimetypes
import os
import re
import urllib
import traceback 
import json
import time,datetime
import random

import time, MySQLdb,csv

#连接    
conn=MySQLdb.connect(host="localhost",user="root",passwd="",db="drupal7",charset="utf8")
cursor = conn.cursor()

header = {
            "User-Agent":'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB6.6; .NET CLR 3.5.30729)',
        }

def regx_data(regx,html,default,d= False,clean=False,rep=''):
    #print regx
    if re.search(regx, html):        
        data = re.search(regx, html).group(1)
        if clean:
            print rep
            data = re.sub(clean,rep,data)
        if d:
            print regx
            print data
        return data
    else:
        if d:
            print regx
            print "没有"
        return default
class MyException(Exception):
    def __init__(self, type,note):
        self.type = type
        self.note=note
    def __str__(self):
        return str("%s|%s"%(self.type,self.note))

class browser():
    def __init__(self,param):
        cj = cookielib.MozillaCookieJar()
        
        self.br=urllib2.build_opener(urllib2.HTTPHandler(),urllib2.HTTPCookieProcessor(cj),urllib2.HTTPRedirectHandler())
        self.cj = cj
        self.pdb={}
        self.header=header
        self.param=param
        self.returnStr = ""
        
        #self.subdict={
    def saveCookie(self):
        self.cj.save(ignore_discard=True, ignore_expires=True)
        
    def goLogin(self):
        self.loginUrl = "http://www.dev.org/drupal7/user/login"
        
        req=urllib2.Request(self.loginUrl , None, self.header)
        self.br.open(req)
        
        loginData = "name=logic&pass=logic123&form_build_id=form-4-CNVrvMURp9zOwIffIoBUF6by9EBMRL2EaPK1YhOMw&form_id=user_login&op=Log+in"
        req=urllib2.Request(self.loginUrl , loginData, self.header)
        res =  self.br.open(req).read()
        #print res
        
        if "<strong>logic</strong>" in res:
            self.returnStr =  "登陆成功"
            #print self.returnStr            
        else:
            raise Exception("loginError|登陆失败")
        
    
    def debugPostData(self):
        if DEBUG:
            for i in self.subdict:
                print i,self.subdict[i]
                
    def Login(self):
        self.goLogin()
    def Publish(self):
        try:
            self.Login()
        except Exception,e:
            print traceback.format_exc() 
            self.returnStr = str(e) 
    
        
    
    def genform(self,fields):
        BOUNDARY = '----------267402204411258'
        CRLF = '\r\n'
        L = []
        for (key, value) in fields:
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="%s"' % key)
            L.append('')
            L.append(value)
            
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="files[uc_product_image_und_0]"; filename=""')
        L.append('Content-Type: application/octet-stream')
        L.append('')
        L.append('')
        
        L.append('--' + BOUNDARY + '--')
        L.append('')
        body = CRLF.join(L)
        content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
        return content_type, body
    def gopub1(self):
        
        req=urllib2.Request("http://www.dev.org/drupal7/node#overlay=node/add/product", None, self.header)
        
        #loginData = "name=logic&pass=logic123&form_build_id=form-4-CNVrvMURp9zOwIffIoBUF6by9EBMRL2EaPK1YhOMw&form_id=user_login&op=Log+in"
        publishdoct_sell = {
                            "title":"wwwwwwwwwwww",
                            "body[und][0][summary]":"wwwwwwwwwwww",
                            "body[und][0][value]":"wwwwwwwwwwwwwwwwwwww",
                            "uc_product_image[und][0][_weight]":"0",
                            "uc_product_image[und][0][fid]":"0",
                            "uc_product_image[und][0][display]":"1",
                            "taxonomy_catalog[und][]":"173",
                            "field_vendor[und]":"25",
                            "changed":"",
                            "form_build_id":"form-_UdHiSthEi2ntVdZ7qR5FtEyyXJ1JQ28No29a30cdlg",
                            "form_token":"e6y0hWVyEn4r_0IaZzTc3aQcSvZfIPFhzAcrCPEXDHw",
                            "form_id":"product_node_form",
                            "model":"ww",
                            "list_price":"0",
                            "cost":"0",
                            "sell_price":"0",
                            "shippable":"1",
                            "weight":"0",
                            "weight_units":"lb",
                            "dim_length":"0",
                            "dim_width":"0",
                            "dim_height":"0",
                            "length_units":"in",
                            "pkg_qty":"1",
                            "ordering":"0",
                            "gc_salable":"1",
                            "shipping_type":"",
                            "shipping_address[first_name]":"",
                            "shipping_address[last_name]":"",
                            "shipping_address[company]":"",
                            "shipping_address[street1]":"",
                            "shipping_address[street2]":"",
                            "shipping_address[city]":"",
                            "shipping_address[zone]":"0",
                            "shipping_address[country]":"840",
                            "shipping_address[postal_code]":"",
                            "shipping_address[phone]":"",
                            "usps[container]":"VARIABLE",
                            "ups[pkg_type]":"02",
                            "menu[link_title]":"v",
                            "menu[description]":"",
                            "menu[parent]":"main-menu:0",
                            "menu[weight]":"0",
                            "log":"",
                            "path[alias]":"",
                            "comment":"2",
                            "name":"logic",
                            "date":"",
                            "status":"1",
                            "promote":"1",
                            "additional_settings__active_tab":"edit-base",
                            "op":"Save"
            }       
        
        content_type, params = self.genform(publishdoct_sell.items())
        print params
        publishheader={
               "User-Agent":"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB6.6; .NET CLR 3.5.30729)",
               "Referer":"http://www.dev.org/drupal7/node/add/product?render=overlay",
               'Content-Type': content_type,
               'Content-Length': str(len(params))
               }
        
        request = urllib2.Request("http://www.dev.org/drupal7/node/add/product?render=overlay&render=overlay",params, publishheader)
        res = self.br.open(request).read()        
        #print res
    def publish(self):
        pass
    def gopub(self,title,description_1,description_2,vendor,catalog):
        #req=urllib2.Request("http://www.dev.org/drupal7/node#overlay=node/add/product", None, self.header)     
        publishdoct = {                       
                       'title': '', 
                       'field_description_2[und][0][value]': '', 
                       'field_description_1[und][0][value]': '', 
                       'field_vendor[und]': '',
                       'taxonomy_catalog[und][]': '',
                       'model': 'sku',
                       
                       'comment': '2', 
                       'status': '1', 
                       'list_price': '0', 
                       'weight': '0',      
                       'cost': '0',                                              
                       'weight_units': 'lb',                          
                       'pkg_qty': '1', 
                       'name': 'logic', 
                       'sell_price': '0',                         
                       'menu[weight]': '0',                        
                       'length_units': 'in', 
                       'additional_settings__active_tab': 'edit-base', 
                       'shipping_address[phone]': '', 
                       'shipping_address[city]': '',
                       'shipping_address[postal_code]': '',
                       'shipping_address[last_name]': '', 
                       'shipping_address[first_name]': '', 
                       'shipping_address[company]': '',
                       'shipping_address[street2]': '', 
                       'shipping_address[zone]': '0', 
                       'shipping_address[country]': '840', 
                       'shipping_address[street1]': '',
                       'shipping_type': '', 
                       'ups[pkg_type]': '02',                         
                       'usps[container]': 'VARIABLE', 'date': '',    
                       'dim_width': '0',                        
                       'dim_length': '0',
                       'gc_salable': '1',                        
                       'promote': '1', 
                       'shippable': '1',                        
                       'path[alias]': '',
                       'dim_height': '0',
                       'ordering': '0', 
                       'changed': '', 
                       'menu[parent]': 'main-menu:0', 
                       'menu[link_title]': '',                       
                       'menu[description]': '',                          
                       'log': '', 
                       'form_token': 'L5bpClXSTkbmOECOPZLjBdJsI2hUL2C0miY5a0_bHHU',
                       'form_build_id': 'form-CB0hbTiWtWxditpjJ061qW7TWsWqMWUFNXz4YKJg3dw', 
                       'form_id': 'product_node_form', 
                       'op': 'Save'
        }
        
        publishdoct['title'] = title
        publishdoct['field_description_1[und][0][value]'] = description_1
        publishdoct['field_description_2[und][0][value]'] = description_2
        publishdoct['field_vendor[und]'] = vendor
        publishdoct['taxonomy_catalog[und][]'] = catalog        
        
        pubdata = urllib.urlencode(publishdoct)
        #self.br.addheaders(self.header)
        res = self.br.open("http://www.dev.org/drupal7/node/add/product?render=overlay&render=overlay",pubdata).read()  
        print "发布成功�?
    
def Publish(p):
    try:
        br=browser(p)
        #login
        br.goLogin()
        
        
        sql = """
        select * from tmp_products_
        """
        cursor.execute(sql)
        
        rows = cursor.fetchall()
        i = 0
        for row in rows:
            i = i+1
            #print i
            #print row
            title         = row[5]
            description_1 = row[6]
            description_2 = row[7]
            vendor        = row[1]
            catalog       = row[2]
            print "正在发布�?d" % i
            print title,description_1,description_2,vendor,catalog
            br.gopub(title,description_1,description_2,vendor,catalog)
            
        
        
    except Exception,e:
        print traceback.format_exc() 
        return str(e) 


if __name__=="__main__":
    reg={
       "username":"jjj22us1",
       "password":"112233",
       "password2":"112233",
       "next":"http%3A%2F%2Fsh.ganji.com%2F",
       "second":"",
       "email":"",
       "checkcode":"",
       "affirm":"on"
    }
    login={
       "source":"passport",
       "username":"housemain",
       "password":"112233",
       "expireDays":"365",
       "setcookie":"365",
       "next":""
    }
    p={}
    p['reg'] = reg
    p['login'] = login
    p['publish'] = ""
    p['citycode'] = "sh"
    DEBUG = 1
    Publish(p)
    #Reg(p)
    #Login(p)
cursor.close()
    #关闭    
conn.close()      

    