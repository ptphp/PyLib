#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2,urllib
data={  
        "username":"changna19880422",
        "passwd":"201106",
        "webid":"4",
        "broker_id":"1111",
        "house_title":"昆山花园1111111",
        "city":"2",
        "cityarea_id":"1411",
        "borough_section":"5910",
        "house_type":"3",
        "house_toward":"1",
        "house_fitment":"2",
        "house_kind":"1",
        "house_deposit":"1",
        "belong":"1",
        "house_price":"500",
        "house_totalarea":"120",
        "house_room":"3",
        "house_hall":"2",
        "house_toilet":"1",
        "house_topfloor":"6",
        "house_floor":"2",
        "house_age":"10",
        "house_desc":'''昆山花园昆山花园昆山花园昆山花园''',
        "borough_id":"10",
        "borough_name":"昆山f花",
        "house_drawing":"",
        "house_thumb":"",
        "house_xqpic":"",
        #========================
        "mobile":"111",
        "contact":"苏大生",
        
       }
data1={
    "house_kind":"2",
    "city":"5",
    "citycode":"su",
    "cityarea_id":"11383",
    "borough_section":"5511",
    "username":"liseor666",
    "passwd":"200898",
    "webid":"8",
    "broker_id":"1111",
    "house_title":"精装三房两厅",    
    "house_type":"3",
    "house_toward":"1",
    "house_fitment":"2",    
    "house_deposit":"1",
    "belong":"1",
    "house_price":"500",
    "house_totalarea":"120",
    "house_room":"3",
    "house_hall":"2",
    "house_toilet":"1",
    "house_topfloor":"6",
    "house_floor":"2",
    "house_age":"10",
    "house_desc":'''<SPAN id=comp-paste-div-700>装三房两厅格费，次价格</SPAN>''',
    "borough_id":"10",
    "borough_name":"秀水苑ii",
    "house_drawing":"",
    "house_thumb":"",
    "house_xqpic":"",
    #========================
    "mobile":"13855698654",
    "contact":"苏大生",
   }
url = 'http://suzhou.jjr360.com/login/login.php'
url1 = "http://post.jjr360.com/post_data"
req = urllib2.Request(url)
data_1={}
data_1['action'] = 'findpwd'
data_1['username'] = 'lise1or'
data_1['email'] = 'dhol@qq.com'
r = urllib2.urlopen(req, urllib.urlencode(data_1))
print r.read().decode('gbk')
