#!user/bin/env python
# -*- coding: utf8 -*- 
import os,time,random

settings={
    "static_path":'D:\Dhole\PtProject\PtWebos\Public\static',
    "template_path" : os.path.join(os.path.dirname(__file__), "../template"),
    "login_url":"/login/",
    "xsrf_cookies": True,
    "autoescape":None,
    "gzip" : True, 
    "debug" : True,
    "cookie_secret":'cookie_secret',
}
