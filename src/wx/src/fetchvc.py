#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: observer
# email: jingchaohu@gmail.com
# blog: http://obmem.com
import urllib
import re
import sqlite3
import time
import os,sys
import config

from threading import Thread
from Queue import Queue

from download import httpfetch

path = os.path.dirname(os.path.realpath(sys.argv[0]))
dbc = sqlite3.connect(path+'/simplecd/comment.sqlite3.db')
db = sqlite3.connect(path+'/simplecd/verycd.sqlite3.db')
dbl = sqlite3.connect(path+'/simplecd/lock.sqlite3.db')
dbc.text_factory = str
dbl.text_factory = str
db.text_factory = str
q = Queue()
MAXC = int(config.SS_MAX_THREADS)
lastid = None
stop = False

def thread_fetch():
    dbc = sqlite3.connect(path+'/simplecd/comment.sqlite3.db')
    db = sqlite3.connect(path+'/simplecd/verycd.sqlite3.db')
    dbl = sqlite3.connect(path+'/simplecd/lock.sqlite3.db')
    dbc.text_factory = str
    dbl.text_factory = str  
    db.text_factory = str
    while True:
        topic = q.get()
        global lastid
        lastid = topic
        if not stop:
            fetch(topic,db=db,dbc=dbc,dbl=dbl)
        q.task_done()

def update_ids(ids,dlgupdate,max):
    for id in ids:
        q.put(id)
    keepGoing = True
    while not q.empty():
        time.sleep(1)
        progress = max-q.qsize()-1
        (keepGoing,skip) = dlgupdate(progress,'Processing %d/%d'%(progress,max))
        if not keepGoing:
            id = lastid
            global stop
            stop = True
            dlgupdate(progress,'Waiting threads...(takes 30 secs)')
            q.join()
            stop = False
            return id
    q.join()
    return lastid

def update(num=10,off=1):
    urlbase = 'http://www.verycd.com/sto/~all/page'
    for i in range(off,num+1):
        print 'fetching list',i,'...'        
        url = urlbase+str(i)
        res = httpfetch(url,needlogin=True)
        res2 = re.compile(r'"topic-list"(.*?)"pnav"',re.DOTALL).findall(res)
        if res2:
            res2 = res2[0]
        else:
            continue
        topics = re.compile(r'/topics/(\d+)',re.DOTALL).findall(res2)
        topics = set(topics)
        print topics    
        for topic in topics:
            q.put(topic)

def fetchall(ran='1-max',debug=False):
	urlbase = 'http://www.verycd.com/archives/'
	if ran == '1-max':
		m1 = 1
		res = urllib.urlopen(urlbase).read()
		m2 = int(re.compile(r'archives/(\d+)').search(res).group(1))
	else:
		m = ran.split('-')
		m1 = int(m[0])
		if m[1]=='max':
			res = urllib.urlopen(urlbase).read()
			m2 = int(re.compile(r'archives/(\d+)').search(res).group(1))
		else:
			m2 = int(m[1])
	print 'fetching list from',m1,'to',m2,'...'
	for i in range(m1,m2+1):
		url = urlbase + '%05d'%i + '.html'
		print 'fetching from',url,'...'
		res = httpfetch(url)
		ids = re.compile(r'topics/(\d+)/',re.DOTALL).findall(res)
		print ids
		for id in ids:
			q.put(id)

def fetchcmt(id,dbc=dbc,debug=False,page=1):
    print 'fetching topic',id,'...'
    urlbase = 'http://www.verycd.com/topics/'
    url = urlbase + str(id) + '/comments/page' + str(page)

    res = ''
    for _ in range(3):
        try:
            res = httpfetch(url,report=True)
            break
        except:
            continue

    if page == 1:
        pages = re.compile(r'/comments/page(\d+)').findall(res)
        if pages:
            pages = set(pages)
            for page in pages:
                if page != 1:
                    fetchcmt(id=id,dbc=dbc,page=page,debug=debug)

    stmts = re.compile(r'<a href="/members/[^>]*>([^<]*)</a>.*?<span class="date-time">(.*?)</span>.*?<!--Wrap-head end-->(.*?)<!--Wrap-tail begin-->',re.DOTALL).findall(res)
    stmts = [ [x[0].replace(r'<.*?>',r'').strip(),x[1].replace(r'<.*?>',r'').strip(),x[2].replace(r'<.*?>',r'').strip()]  for x in stmts]


    for i in range(len(stmts)):
        stmts[i][2] = re.compile(r'(image-\d*)\.verycd\.com',re.I).sub(r'\1.app-base.com',stmts[i][2])
        stmts[i][2] = re.compile(r'<div[^>]*>',re.I).sub(r'',stmts[i][2])
        stmts[i][2] = re.compile(r'</div>',re.I).sub(r'',stmts[i][2])
        stmts[i][2] = re.compile(r'<!--.*-->',re.I).sub(r'',stmts[i][2])
    stmts = [ (int(id),x[0],x[2],int(time.mktime(time.strptime(x[1],'%Y/%m/%d %H:%M:%S')))-8*3600) for x in stmts ]

    if debug:
        print len(stmts)
        for stmt in stmts:
            print stmt[0],stmt[2],stmt[1]

    tries = 0
    while tries<5:
        try:
            c = dbc.cursor()
            c.executemany('replace into comment values (?,?,?,?)',stmts)
            break
        except:
            tries += 1;
            time.sleep(5);            
            continue;
    dbc.commit()
    c.close()
    return

def fetch(id,db=db,dbl=dbl,dbc=dbc,debug=False):
    print 'fetching topic',id,'...'
    urlbase = 'http://www.verycd.com/topics/'
    url = urlbase + str(id)

    res = ''
    for _ in range(3):
        try:
            res = httpfetch(url,report=True,needlogin=False)
            break
        except:
            continue

    abstract = re.compile(r'<h1>.*?visit',re.DOTALL).findall(res)
    if not abstract:
        print res
        if res == '' or '很抱歉' in res:
            print 'resource does not exist'
            return
        else:
            print 'fetching',id,'again...'
            return fetch(id,db)
    abstract = abstract[0]
    
    title = re.compile(r'<h1>(.*?)</h1>',re.DOTALL).findall(abstract)
    if title:
        title=title[0]
    else:
        return
    try:
        status = re.compile(r'"requestWords">(.*?)<',re.DOTALL).search(abstract).group(1)
        brief = re.compile(r'"font-weight:normal">\s*<span>(.*?)</td>',re.DOTALL).search(abstract).group(1)
        brief = re.compile(r'<.*?>',re.DOTALL).sub('',brief).strip()
        pubtime = re.compile(r'"date-time">(.*?)</span>.*?"date-time">(.*?)</span>',re.DOTALL).findall(abstract)[0]
        category1 = re.compile(r'<strong>分类.*?<td>(.*?)&nbsp;&nbsp;(.*?)&nbsp;&nbsp;',re.DOTALL).findall(abstract)[0]
        category = ['','']
        category[0] = re.compile(r'<.*?>',re.DOTALL).sub('',category1[0]).strip()
        category[1] = re.compile(r'<.*?>',re.DOTALL).sub('',category1[1]).strip()
    
        ed2k = re.compile(r'ed2k="([^"]*)" (subtitle_[^=]*="[^"]*"[^>]*)>([^<]*)</a>',re.DOTALL).findall(res)
        ed2k.extend( re.compile(r'ed2k="([^"]*)">([^<]*)</a>',re.DOTALL).findall(res) )
        #delete duplicates
        newed2k = ed2k
        for i in range(len(ed2k)-1,-1,-1):
            if ed2k[i] in ed2k[:i]:
                newed2k.remove(ed2k[i])
        content = re.compile(r'id="iptcomContents">(.*?)<!--Wrap-tail end-->',re.DOTALL).findall(res)
    except:
        return

    if content:
        content = content[0]
        content = re.compile(r'<(img .*?)>').sub(r'[\1]',content)
        content = re.compile(r'<br />',re.DOTALL).sub('\n',content)
        content = re.compile(r'<.*?>',re.DOTALL).sub('',content)
        content = re.compile(r'&.*?;',re.DOTALL).sub(' ',content)
        content = re.compile(r'\n\s+',re.DOTALL).sub('\n',content)
        content = re.compile(r'\[(img .*?)\]').sub(r'<\1><br>',content)
        content = re.compile(r'(image-\d*)\.verycd\.com',re.I).sub(r'\1.app-base.com',content)
        content = content.strip()
    else:
        content=''
    
    vcpv = 0

    #fetch stat
    try:
        staturl = 'http://stat.verycd.com/counters/folder/'+str(id)+'/'
        st = httpfetch(staturl)
        vcpv = int(re.compile(r'\'(\d+)\'').findall(st)[0])
    except:
        pass

    # update lock
    owner = re.compile(r'<div id="userres">.*?<td align="left" valign="top"><p><strong id="username"><a href=.*?>(.*)</a></strong>',re.DOTALL).findall(res)
    if owner:
        owner = owner[0]
        cl=dbl.cursor()
        try:
            cl.execute('replace into lock values (?,?,?,?,?,?,?)',(long(id),True,owner,'',title,pubtime[1],vcpv))
        except:
            pass
        while True:
            try:
                dbl.commit()
                break
            except:
                pass
        cl.close()

    if debug:
        if vcpv:
            print vcpv
        if owner:
            print owner
        print title
        print status
        print brief
        print pubtime[0],pubtime[1]
        print category[0],category[1]
        for x in ed2k:
            print x
        print content

    ed2kstr = ''
    for x in ed2k:
        ed2kstr += '`'.join(x)+'`'

    if ed2kstr == '':
        return

    # update verycd
    try:
        if not dbfind(id,db):
            dbinsert(id,title,status,brief,pubtime,category,ed2kstr,content,db)
        else:
            dbupdate(id,title,status,brief,pubtime,category,ed2kstr,content,db)
    except Exception as what:
        print what

    # update comment
    fetchcmt(id=id,dbc=dbc)

    return pubtime[1]

def dbinsert(id,title,status,brief,pubtime,category,ed2k,content,db):
    c = db.cursor()
    tries = 0
    while tries<10:
        try:
            c.execute('insert into verycd values(?,?,?,?,?,?,?,?,?,?,?)',\
                (id,title,status,brief,pubtime[0],pubtime[1],category[0],category[1],\
                ed2k,content,''))
            break
        except:
            tries += 1
            time.sleep(5)
            continue
    db.commit()
    c.close()

def dbupdate(id,title,status,brief,pubtime,category,ed2k,content,db):
    tries = 0
    c = db.cursor()
    while tries<5:
        try:
            c.execute('update verycd set title=?,status=?,brief=?,pubtime=?,\
            updtime=?,category1=?,category2=?,ed2k=?,content=? where verycdid=?',\
            (title,status,brief,pubtime[0],pubtime[1],category[0],category[1],\
            ed2k,content,id))
            break
        except:
            tries += 1
            time.sleep(1)
            continue
    db.commit()
    c.close()

def dbfind(id,db):
    c = db.cursor()
    c.execute('select verycdid from verycd where verycdid=?',(id,))
    x = c.fetchall()
    if x:
        return True
    else:
        return False
    c.close()

def dblist():
    c = db.cursor()
    c.execute('select * from verycd')
    for x in c:
        for y in x:
            print y

def usage():
    print '''Usage:'''

#initialize thread pool
for i in range(MAXC):
    t = Thread(target=thread_fetch)
    t.setDaemon(True)
    t.start()

if __name__=='__main__':
    if len(sys.argv) == 1:
        usage()
    elif len(sys.argv) == 2:
        if sys.argv[1].startswith('update'):
            if sys.argv[1] == 'update':
                update(20)
            else:
                ran = sys.argv[1][6:].split('-')
                if len(ran) == 2:
                    update(int(ran[1]),int(ran[0]))
                else:
                    update(int(ran[0]))
        elif sys.argv[1] == 'list':
            dblist()
    elif len(sys.argv) == 3:
        if sys.argv[1] != 'fetch':
            usage()
        elif '~' in sys.argv[2]:
            m = sys.argv[2].split('~')
            for i in range(int(m[0]),int(m[1])+1):
                q.put(i)
        elif '-' in sys.argv[2]:
            fetchall(sys.argv[2])
        else:
            fetch(int(sys.argv[2]),debug=True)

    # wait all threads done
    q.join()
