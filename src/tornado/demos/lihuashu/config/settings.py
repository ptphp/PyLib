#!user/bin/env python
# -*- coding: utf8 -*- 
import os,time,random
from common.function import GetFileSHA256

settings={
    "site_name":"梨花树",
    "site_title":"分享艺术视觉盛宴",
    "site_keywords":"梨花树,梨花树网,画板,家居,旅行,服饰搭配,发型,创意设计,旅行,街拍,摄影,婚纱,手工,时尚",
    "site_description":"提供艺术、绘画、电影、音乐等艺术相关的推荐、收藏评论，以及独特的艺术文化。",
    "site_host":"http://vm.com/",
    "site_imgserver":"http://vm.com/",

    "site_timenow":str(int(time.time())),
    "static_path":os.path.join(os.path.dirname(__file__),"../static"),
    "template_path" : os.path.join(os.path.dirname(__file__), "../template"),
    "login_url":"/login/",
    "xsrf_cookies": True,
    "autoescape":None,
    "gzip" : True, 
    "debug" : True,
    "cookie_secret":GetFileSHA256(os.path.join(os.path.dirname(__file__),"../app.py")),
    "fdfs_tracker_host":"168.168.10.159",
    #"fdfs_tracker_host":"192.168.106.78",
    "fdfs_tracker_http":"http://localhost:8080/"
}

globalSetting = {
     'max_index_pin_rows':5,
     'max_index_board_rows':5,
     'riakPort':8091,
     'riakHost':'192.168.19.138',                            
     'fdfsPort':8080,
     'fdfs_client_conf':'/etc/fdfs/client.conf',     
     'boardBucket':'boardtest2',
     'pinBucket':'pintest2',
     'userBucket':'usertest211',
     'user_infoBucket':'userinfotest',
     'picBucket':'pictest21',
     'pinFollowingBucket':'picfollowingtest21',
     'pinLikeBucket':'picLiketest211',
     'pinHateBucket':'picHatetest211',     
     'thumbBucket':'thumbtest21',
     'avatarBucket':'avatartest2',
     'categoryBucket':'cattest2',
     'commentBucket':'commenttest2111',
     'commonBucket':'commontest11',
     'boardFollowBucket':'boardfollowBucketest11',
     'userFollowBucket':'userfollowBucketest11',     
}
