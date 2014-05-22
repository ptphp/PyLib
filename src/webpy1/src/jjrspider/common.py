#coding=UTF-8
'''
Created on 2011-7-13

@author: Administrator
'''
import urllib
import urllib2
from jjrlog import msglogger
def postHost(res):
    if res==None:
        return
    res1={}
    res1['c']='houseapi'
    res1['a']='savehouse'    
    req=urllib2.Request("http://site.jjr360.com/app.php", urllib.urlencode(res))
    br=urllib2.build_opener()
    try:
        p=br.open(req).read().strip()
    except:
        p=None
    
    rs=""
    if p!=None :
        rs=unicode(p,"GB18030",errors="ignore")
    try:    
        msglogger.debug("%s---->%s"%(res,rs))
    except:
        print "Exception -------->%s"%res
    return rs
def printRsult(dict,kind):
    print "++++++++++++++++++++++++++++++++++++"
    if kind == "1":
        print "posttime        : "+str(dict['posttime1'])
        print "ciytname        : "+dict['cityname']
        print "citycode        : "+dict['citycode']
        print "house_title     : "+dict['house_title']
        print "owner_phone     : "+dict['owner_phone']
        print "owner_name      : "+dict['owner_name']
        print "borough_name    : "+dict['borough_name']
        print "cityarea        : "+dict['cityarea']
        print "borough_section : "+dict['borough_section']
        print "house_addr      : "+dict['house_addr']        
        print "house_price     : "+dict['house_price']
        print "house_totalarea : "+dict['house_totalarea']
        print "house_age       : "+dict['house_age']
        print "belong          : "+dict['belong']
        
        print "house_room      : "+dict['house_room']
        print "house_hall      : "+dict['house_hall']
        print "house_toilet    : "+dict['house_toilet']
        print "house_floor     : "+dict['house_floor']
        print "house_topfloor  : "+dict['house_topfloor']
        
        print "house_deposit   : "+dict['house_deposit']
        print "house_toward    : "+dict['house_toward']
        print "house_type      : "+dict['house_type']
        print "house_fitment   : "+dict['house_fitment']
        print "house_support   : "+dict['house_support']
        print "house_desc      : "+dict['house_desc']
    if kind == "2":
        print "posttime        : "+str(dict['posttime1'])
        print "ciytname        : "+dict['cityname']
        print "citycode        : "+dict['citycode']
        print "house_title     : "+dict['house_title']
        print "owner_phone     : "+dict['owner_phone']
        print "owner_name      : "+dict['owner_name']
        print "borough_name    : "+dict['borough_name']
        print "cityarea        : "+dict['cityarea']
        print "borough_section : "+dict['borough_section']
        print "house_addr      : "+dict['house_addr']
        
        print "house_price     : "+dict['house_price']
        print "house_totalarea : "+dict['house_totalarea']
        print "house_age       : "+dict['house_age']
        
        print "house_room      : "+dict['house_room']
        print "house_hall      : "+dict['house_hall']
        print "house_toilet    : "+dict['house_toilet']
        print "house_floor     : "+dict['house_floor']
        print "house_topfloor  : "+dict['house_topfloor']
        
        print "house_deposit   : "+dict['house_deposit']
        print "house_toward    : "+dict['house_toward']
        print "house_type      : "+dict['house_type']
        print "house_fitment   : "+dict['house_fitment']
        print "house_support   : "+dict['house_support']
        print "house_desc      : "+dict['house_desc']
    if kind == "3":
        print "posttime        : "+str(dict['posttime1'])
        print "ciytname        : "+dict['cityname']
        print "citycode        : "+dict['citycode']
        print "house_title     : "+dict['house_title']
        print "owner_phone     : "+dict['owner_phone']
        print "owner_name      : "+dict['owner_name']
        print "borough_name    : "+dict['borough_name']
        print "cityarea        : "+dict['cityarea']
        print "borough_section : "+dict['borough_section']
        print "house_addr      : "+dict['house_addr']
        
        print "house_price     : "+dict['house_price']
        print "house_price_min : "+dict['house_price_min']
        print "house_price_max : "+dict['house_price_max']
        print "house_totalarea : "+dict['house_totalarea']
        print "house_age       : "+dict['house_age']
        print "house_totalarea_min : "+dict['house_totalarea_min']
        print "house_totalarea_max : "+dict['house_totalarea_max']
        
        #print "house_room1     : "+dict['house_room1']
        print "house_room      : "+dict['house_room']
        print "house_hall      : "+dict['house_hall']
        print "house_toilet    : "+dict['house_toilet']
        print "house_floor     : "+dict['house_floor']
        print "house_topfloor  : "+dict['house_topfloor']
        
        print "belong          : "+dict['belong']
        print "house_toward    : "+dict['house_toward']
        print "house_type      : "+dict['house_type']
        print "house_fitment   : "+dict['house_fitment']
        print "house_support   : "+dict['house_support']
        print "house_desc      : "+dict['house_desc']
        
    if kind == "4":
        print "posttime        : "+str(dict['posttime1'])
        print "ciytname        : "+dict['cityname']
        print "citycode        : "+dict['citycode']
        print "house_title     : "+dict['house_title']
        print "owner_phone     : "+dict['owner_phone']
        print "owner_name      : "+dict['owner_name']
        print "borough_name    : "+dict['borough_name']
        print "cityarea        : "+dict['cityarea']
        print "borough_section : "+dict['borough_section']
        print "house_addr      : "+dict['house_addr']
        
        print "house_price     : "+dict['house_price']
        print "house_price_min : "+dict['house_price_min']
        print "house_price_max : "+dict['house_price_max']
        print "house_totalarea : "+dict['house_totalarea']
        print "house_age       : "+dict['house_age']
        print "house_totalarea_min : "+dict['house_totalarea_min']
        print "house_totalarea_max : "+dict['house_totalarea_max']
        
        print "house_room1     : "+dict['house_room1']
        print "house_hall      : "+dict['house_hall']
        print "house_toilet    : "+dict['house_toilet']
        print "house_floor     : "+dict['house_floor']
        print "house_topfloor  : "+dict['house_topfloor']
        
        print "house_deposit   : "+dict['house_deposit']
        print "house_toward    : "+dict['house_toward']
        print "house_type      : "+dict['house_type']
        print "house_fitment   : "+dict['house_fitment']
        print "house_support   : "+dict['house_support']
        print "house_desc      : "+dict['house_desc']
        
    