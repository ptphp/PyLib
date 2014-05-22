#-*-coding:utf-8-*-
#lilybbs.py
#Author:Sky_Money
#Python实现自动登录BBS并发帖

import urllib2, urllib, cookielib
import re
import getpass
import sqlite3
import random
import time

class PostRobot():
    def __init__(self,user,pwd,*args,**kwargs):
        self.username = user
        self.password = pwd
        self.args     = args
        self.kwargs   = kwargs
        pass
 
class Discuz:
    def __init__(self,user,pwd,args):
        self.username = user
        self.password = pwd
        self.args = args
        self.regex = {
            'loginreg':'<input\s*type="hidden"\s*name="formhash"\s*value="([\w\W]+?)"\s*\/>',
            'replyreg':'<input\s*type="hidden"\s*name="formhash"\s*value="([\w\W]+?)"\s*\/>',
            #'tidreg':  '<tbody\s*id="normalthread_\d+">[\s\S]+?<span\s*id="thread_(\d+)">',
            'tidreg':'<a\s*href="forum.php\?mod=viewthread&amp;tid=(\d+)&amp;extra=page%3D1"\s*onclick="atarget\(this\)"',
            'logout_regx':'<a\s*href="member\.php\?mod=logging&amp;action=logout&amp;formhash=([\w\W]+?)">'
        }
        self.conn = None
        self.cur = None
        self.islogin = False
        self.formhash = ''

        self.referer = ''

        cj = cookielib.CookieJar() 
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj)) # 创建一个可以接收 cookie 的打开器
        urllib2.install_opener(self.opener)
        user_agent = 'Mozilla/5.0 (Hackinux; Lin64; x64;) AppleWebKit/535.1 (WebKit, like KHTML) Garning/2.2012.0607.2059'
        self.opener.addheaders = [("User-Agent",user_agent),
                                  ("Referer",self.referer)]

        
        self.login()
        self.InitDB()
 
    def login(self):
        try:
            loginPage = urllib2.urlopen(self.args['loginurl']).read() #  首先加载登录页
            formhash = re.search(self.regex['loginreg'], loginPage)   #  然后找到 forumhash 以供后面登录使用
            formhash = formhash.group(1)
            self.formhash = formhash
            print 'Using account %s to loging.' % self.username
            print 'login formhash:', formhash
            print 'start login...'

           
            opener.addheaders = [('User-agent', user_agent)]
            urllib2.install_opener(opener)

            # 构造登录数据,  进行编码, 从而POST 数据到登录链接url
            logindata = urllib.urlencode({
                'cookietime':    2592000,
                'formhash': self.formhash,
                'loginfield':'username',
                'username':    self.username,
                'password':    self.password,
                'questionid':    0,
                'referer': self.args['referer']
                })
            request = urllib2.Request(self.args['loginsubmiturl'] % self.formhash,logindata)
            response = self.opener.open(request)
            self.islogin = True
            print 'login success...'
        except Exception,e:
            print 'loggin error: %s' % e

    def logout(self):
        try:
            request  = urllib2.Request(self.args['logout_url'] % self.formhash)
            response = self.opener.open(request)
            response.close()
            print 'logout success...'
        except Exception,e:
            print 'logout error: %s' % e
 
    def PostReply(self, fid, tid, content):
        try:
            sql = "select * from post where fid='%s' and tid='%s'" % (fid,tid)
            self.cur.execute(sql)
            if self.cur.rowcount == -1:
                #print self.args['tidurl'] %   tid 
                tidurl = self.args['tidurl'] % tid
                replysubmiturl = self.args['replysubmiturl'] % (fid,tid)
                tidPage = urllib2.urlopen(tidurl).read()
                formhash = re.search(self.regex['replyreg'], tidPage)
                formhash = formhash.group(1)
                self.formhash = formhash
                print 'start reply...'
                replydata = urllib.urlencode({
                    'formhash': self.formhash,
                    'message': content,
                    'subject': '  ',
                    'usesig':self.args['usesig'],
                    'posttime':'%0.0f' % time.time()
                    })
                ###发送的Headers，必须要有Cookie
                sendheaders = {
                        'Host': 'dev.i8d.com',
                        'Connection': 'keep-alive',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Encoding': 'gzip,deflate,sdch',
                }
                
                sendheaders['Referer'] = tidurl
                #print sendheaders
                #print replydata
                request = urllib2.Request(replysubmiturl,replydata,headers=sendheaders)
                response = self.opener.open(request)
                print response.code

                sql = "insert into post values ('%s', '%s', '%d')" % (fid, tid, 1)
                self.cur.execute(sql)
                self.conn.commit()
                print response.url
                content = response.read()
                print len(content),content[3:]
                print 'reply success for [%s]' % tidurl
            else:
                print 'Skip! Thread:%s is already replied...' % tid
        except Exception, e:
                print 'reply error: %s' % e
 
    def GetThreadIDs(self, fid):
        if self.islogin:
            fidurl = self.args['fidurl'] % fid
            print fidurl
            response = self.opener.open(fidurl)
            content = response.read()
            #print content
            tids = re.findall(self.regex['tidreg'], content)
            return tids
        else:
            print 'Error Please Login...'
 
    def InitDB(self):
        self.conn = sqlite3.connect('data.db')
        self.cur = self.conn.cursor()
        sql = '''create table if not exists post (
            fid text,
            tid text,
            replied integer)'''
        self.cur.execute(sql)
        self.conn.commit()
 
if __name__ == '__main__':
    #username = raw_input('username:').strip()
    #password = getpass.getpass('password:').strip()
    accounts =(
        # username,  password,   uid
        ('username1', 'password1', '1'),
        ('username2', 'password2', '2'),
    )
    account=random.choice(accounts)
    username = account[0]
    password = account[1]
    usesig   = account[2]
    args = {
            'site_encoding':  'utf-8',
            'loginurl':       'http://dev.i8d.com/member.php?mod=logging&action=login&referer=http%%3A%%2F%%2Fdev.i8d.com%%2Fforum.php',
            'loginsubmiturl': 'http://dev.i8d.com/member.php?mod=logging&action=login&loginsubmit=yes&loginhash=%s',
            'logout_url':     'http://dev.i8d.com/member.php?mod=logging&action=logout&formhash=%s',
            'fidurl':         'http://dev.i8d.com/forum.php?mod=forumdisplay&fid=%s',
            'tidurl':         'http://dev.i8d.com/forum.php?mod=viewthread&tid=%s&extra=page%%3D1',
            'replysubmiturl': 'http://dev.i8d.com/forum.php?mod=post&amp;action=reply&amp;fid=%s&amp;tid=%s&amp;extra=page%%3D1&amp;replysubmit=yes&amp;infloat=yes&amp;handlekey=fastpost',
            'referer':        'http://dev.i8d.com/forum.php',
            'usesig':        usesig
    }
    dz = Discuz(username, password,args)
    fid = '49'
    tids = dz.GetThreadIDs(fid)
    #print tids
    replylist = [
            u'不错，支持一下，呵呵',
            u'已阅，顶一下.......',
            u'看看，顶你，呵呵',
            u'多谢分享，顶一下, 还有吗',
            u'说的不错，支持一下,谢谢分享',
            u'提着水桶到处转，哪里缺水哪里灌！',
            u'你太油菜了!这都被你发现了'
    ]
    if dz.islogin:
        for tid in tids[:2]:
            #print tid
            content = random.choice(replylist)
            content = content.encode('utf-8')
            dz.PostReply(fid, tid, content)
            print 'post %s' % content.decode('utf-8')
            #time.sleep(20)
        dz.logout()
