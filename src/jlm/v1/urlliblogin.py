#coding:utf-8
from urllib import urlencode
import cookielib, urllib2
import re


def regx_data(regx, html, default, d=False, clean=False, rep=''):
    #print regx
    if re.search(regx, html):        
        data = re.search(regx, html).group(1)
        if clean:
            print rep
            data = re.sub(clean, rep, data)
        if d:
            print regx
            print data
        return data
    else:
        if d:
            print regx
            print "没有"
        return default


# cookie
cj = cookielib.LWPCookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)

# Login
user_data = {'name': 'logic',
             'pass': 'logic123',
             'form_build_id':'',
             'form_id':'user_login',
             'op':'Log in'
            }

url_data = urlencode(user_data)
#print url_data
login_r = opener.open("http://www.dev.org/drupal7/user/login", url_data)
res = login_r.read()

if "<strong>logic</strong>" in res:
    print  "登陆成功"
    #print self.returnStr            
else:
    print "登陆失败"
