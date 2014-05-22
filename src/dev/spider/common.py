#coding=UTF-8
'''
Created on 2011-7-13

@author: Administrator
'''
import urllib
import urllib2,time
from jjrlog import msglogger
def postHost(res):
#    print "*"*40
    if res and res['house_title']:
        res1={}
        req=urllib2.Request("http://my.lianxiao.com/Manage/houseApi?"+urllib.urlencode(res))
        br=urllib2.build_opener()
        try:
            p=br.open(req).read().strip()
        except Exception ,eeer:
            print "postHost Exception %s"%eeer
            p=None
        rs=p
       # if p!=None :
            #rs=unicode(p,"GB18030",errors="ignore")
        try:    
            msglogger.debug("%s---->%s"%(res,rs))
        except:
            print "Exception -------->%s"%res
        return rs
def postHost1(res):
    if res==None:
        return
    res1={}
    req=urllib2.Request("http://my.lianxiao.com/manage/houseApi", urllib.urlencode(res))
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
    
    """
出售 求购   house_depoit(压金) 没有此键
出租求租   house_belong(产权) 没有此键
 
出售 出租 无 house_price_max house_area_max
 求购 求租 无 house_price_max house_area_max
 
 
 如果价格采到的格式为 0-2000或者2000以下 则：
house_price_max = 0
house_price_max = 2000

 如果价格采到的格式为 2000-3000则：
house_price_max = 2000
house_price_max = 3000

如果价格采到的格式为 3000以上则：
house_price_max = 3000
house_price_max = 0

面积同价格
    """
    if kind == "1":#出售        
        print 'house_flag'       +dict['house_flag'],     #房源标识  INTERGER  1:出售 2:出租 3:求购 4:求租
        print 'borough_name'     +dict['borough_name']    #小区名       VARCHAR   不为空                                       
        print 'house_addr'       +dict['house_addr']      #地址            VARCHAR
        print 'house_title'      +dict['house_title']     #标题            VARCHAR   不为空                                 
        print 'house_city'       +dict['house_city'],     #城市            VARCHAR   不为空     如：苏州
        print 'house_region'     +dict['house_region']    #区                 VARCHAR   不为空
        print 'house_section'    +dict['house_section']   #版块             VARCHAR
        print 'house_type'       +dict['house_type']      #房源类型   INTERGER
        print 'house_price'      +dict['house_price']     #价格              FLOAT     不为空    default 0
        print 'house_area'       +dict['house_area']      #面积              FLOAT     
        print 'house_room'       +dict['house_room']      #室                   INTERGER
        print 'house_hall'       +dict['house_hall']      #厅                   INTERGER
        print 'house_toilet'     +dict['house_toilet']    #卫                   INTERGER
        print 'house_veranda'    +dict['house_veranda']   #阳台              INTERGER
        print 'house_topfloor'   +dict['house_topfloor']  #总层              INTERGER
        print 'house_floor'      +dict['house_floor']     #层                   INTERGER
        print 'house_age'        +dict['house_age']       #房龄              INTERGER   为四位数 如：2001年 如果采到房龄为8年，则算出值为：2011-8 = 2003
        print 'house_toward'     +dict['house_toward']    #朝向              INTERGER
        print 'house_fitment'    +dict['house_fitment']   #装修              INTERGER
        print 'house_feature'    +dict['house_feature']   #特色              VARCHAR    字典键值用,分隔 如: 1,2,3
        print 'house_belong'     +dict['house_belong']    #产权              INTERGER
        print 'house_desc'       +dict['house_desc']      #描述              VARCHAR
        print 'owner_name'       +dict['owner_name']      #业主名         VARCHAR
        print 'owner_phone'      +dict['owner_phone']     #业主手机     VARCHAR       搜房电话为数字 搜房必须
        print 'owner_phone_pic'  +dict['owner_phone_pic'] #业主手机图片         VARCHAR  58赶集电话为图片地址 必须
        print 'house_posttime'   +dict['house_posttime'] #房源发布时间         VARCHAR   如果没有采到发布时间 则设为当前时间  unix 时间戳
        
    if kind == "2":#出租
        print 'house_flag'       +dict['house_flag'],     #房源标识  INTERGER  1:出售 2:出租 3:求购 4:求租
        print 'borough_name'     +dict['borough_name']    #小区名       VARCHAR   不为空                                       
        print 'house_addr'       +dict['house_addr']      #地址            VARCHAR
        print 'house_title'      +dict['house_title']     #标题            VARCHAR   不为空                                 
        print 'house_city'       +dict['house_city'],     #城市            VARCHAR   不为空     如：苏州
        print 'house_region'     +dict['house_region']    #区                 VARCHAR   不为空
        print 'house_section'    +dict['house_section']   #版块             VARCHAR
        print 'house_type'       +dict['house_type']      #房源类型   INTERGER
        print 'house_price'      +dict['house_price']     #价格              FLOAT     不为空 default 0
        print 'house_area'       +dict['house_area']      #面积              FLOAT     
        print 'house_deposit'    +dict['house_deposit']   #付款方式   INTERGER
        print 'house_room'       +dict['house_room']      #室                   INTERGER
        print 'house_hall'       +dict['house_hall']      #厅                   INTERGER
        print 'house_toilet'     +dict['house_toilet']    #卫                   INTERGER
        print 'house_veranda'    +dict['house_veranda']   #阳台              INTERGER
        print 'house_topfloor'   +dict['house_topfloor']  #总层              INTERGER
        print 'house_floor'      +dict['house_floor']     #层                   INTERGER
        print 'house_age'        +dict['house_age']       #房龄              INTERGER   为四位数 如：2001年 如果采到房龄为8年，则算出值为：2011-8 = 2003
        print 'house_toward'     +dict['house_toward']    #朝向              INTERGER
        print 'house_fitment'    +dict['house_fitment']   #装修              INTERGER
        print 'house_feature'    +dict['house_feature']   #特色              VARCHAR    字典键值用,分隔 如: 1,2,3
        print 'house_desc'       +dict['house_desc']      #描述              VARCHAR
        print 'owner_name'       +dict['owner_name']      #业主名         VARCHAR
        print 'owner_phone'      +dict['owner_phone']     #业主手机     VARCHAR       搜房电话为数字 搜房必须
        print 'owner_phone_pic'  +dict['owner_phone_pic'] #业主手机图片         VARCHAR  58赶集电话为图片地址 必须
        print 'house_posttime'   +dict['house_posttime'] #房源发布时间         VARCHAR   如果没有采到发布时间 则设为当前时间  unix 时间戳

    if kind == "3":#求购
        print 'house_flag'       +dict['house_flag'],     #房源标识  INTERGER  1:出售 2:出租 3:求购 4:求租
        print 'borough_name'     +dict['borough_name']    #小区名       VARCHAR   不为空                                       
        print 'house_addr'       +dict['house_addr']      #地址            VARCHAR
        print 'house_title'      +dict['house_title']     #标题            VARCHAR   不为空                                 
        print 'house_city'       +dict['house_city'],     #城市            VARCHAR   不为空     如：苏州
        print 'house_region'     +dict['house_region']    #区                 VARCHAR   不为空
        print 'house_section'    +dict['house_section']   #版块             VARCHAR
        print 'house_type'       +dict['house_type']      #房源类型   INTERGER
        print 'house_price'      +dict['house_price']     #价格              FLOAT     不为空  default 0   
        print 'house_price_max'  +dict['house_price_max'] #最大价格    FLOAT     不为空  default 0
        print 'house_area'       +dict['house_area']      #面积              FLOAT      default 0
        print 'house_area_max'   +dict['house_area_max']  #最大面积    FLOAT      default 0
        print 'house_room'       +dict['house_room']      #室                   INTERGER   如果采到非数字的室 则用分号分隔  如 1,2,3,
        print 'house_hall'       +dict['house_hall']      #厅                   INTERGER
        print 'house_toilet'     +dict['house_toilet']    #卫                   INTERGER
        print 'house_veranda'    +dict['house_veranda']   #阳台              INTERGER
        print 'house_topfloor'   +dict['house_topfloor']  #总层              INTERGER
        print 'house_floor'      +dict['house_floor']     #层                   INTERGER
        print 'house_age'        +dict['house_age']       #房龄              INTERGER   为四位数 如：2001年 如果采到房龄为8年，则算出值为：2011-8 = 2003
        print 'house_toward'     +dict['house_toward']    #朝向              INTERGER
        print 'house_fitment'    +dict['house_fitment']   #装修              INTERGER
        print 'house_feature'    +dict['house_feature']   #特色              VARCHAR    字典键值用,分隔 如: 1,2,3
        print 'house_belong'     +dict['house_belong']    #产权              INTERGER
        print 'house_desc'       +dict['house_desc']      #描述              VARCHAR
        print 'owner_name'       +dict['owner_name']      #业主名         VARCHAR
        print 'owner_phone'      +dict['owner_phone']     #业主手机     VARCHAR       搜房电话为数字 搜房必须
        print 'owner_phone_pic'  +dict['owner_phone_pic'] #业主手机图片         VARCHAR  58赶集电话为图片地址 必须
        print 'house_posttime'   +dict['house_posttime'] #房源发布时间         VARCHAR   如果没有采到发布时间 则设为当前时间  unix 时间戳
        
    if kind == "4":#求租
        print 'house_flag'       +dict['house_flag'],     #房源标识  INTERGER  1:出售 2:出租 3:求购 4:求租
        print 'borough_name'     +dict['borough_name']    #小区名       VARCHAR   不为空                                       
        print 'house_addr'       +dict['house_addr']      #地址            VARCHAR
        print 'house_title'      +dict['house_title']     #标题            VARCHAR   不为空                                 
        print 'house_city'       +dict['house_city'],     #城市            VARCHAR   不为空     如：苏州
        print 'house_region'     +dict['house_region']    #区                 VARCHAR   不为空
        print 'house_section'    +dict['house_section']   #版块             VARCHAR
        print 'house_type'       +dict['house_type']      #房源类型   INTERGER
        print 'house_price'      +dict['house_price']     #价格              FLOAT     不为空  default 0   
        print 'house_price_max'  +dict['house_price_max'] #最大价格    FLOAT     不为空  default 0
        print 'house_area'       +dict['house_area']      #面积              FLOAT      default 0
        print 'house_area_max'   +dict['house_area_max']  #最大面积   FLOAT      default 0
        print 'house_deposit'    +dict['house_deposit']   #付款方式   INTERGER
        print 'house_room'       +dict['house_room']      #室                   VARCHAR    如果采到非数字的室 则用分号分隔  如 1,2,3,
        print 'house_hall'       +dict['house_hall']      #厅                   INTERGER
        print 'house_toilet'     +dict['house_toilet']    #卫                   INTERGER
        print 'house_veranda'    +dict['house_veranda']   #阳台              INTERGER
        print 'house_topfloor'   +dict['house_topfloor']  #总层              INTERGER
        print 'house_floor'      +dict['house_floor']     #层                   INTERGER
        print 'house_age'        +dict['house_age']       #房龄              INTERGER   为四位数 如：2001年 如果采到房龄为8年，则算出值为：2011-8 = 2003
        print 'house_toward'     +dict['house_toward']    #朝向              INTERGER
        print 'house_fitment'    +dict['house_fitment']   #装修              INTERGER
        print 'house_feature'    +dict['house_feature']   #特色              VARCHAR    字典键值用,分隔 如: 1,2,3
        print 'house_desc'       +dict['house_desc']      #描述              VARCHAR
        print 'owner_name'       +dict['owner_name']      #业主名         VARCHAR
        print 'owner_phone'      +dict['owner_phone']     #业主手机     VARCHAR       搜房电话为数字 搜房必须
        print 'owner_phone_pic'  +dict['owner_phone_pic'] #业主手机图片         VARCHAR  58赶集电话为图片地址 必须
        print 'house_posttime'   +dict['house_posttime'] #房源发布时间         VARCHAR   如果没有采到发布时间 则设为当前时间  unix 时间戳
        
        
    
