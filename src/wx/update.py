#!/usr/bin/env python
# -*- coding: utf-8 -*-

import config
import urllib2,httplib
import sqlite3
import re
import time
import os

headers = { }

def check_version(url,current_version):
    pass

def try_ungzip(data):
    import zlib
    try:
        data = zlib.decompress(data).decode('utf-8')
        return data
    except Exception as what:
        print what,data
        return data

def update_db_updtime(id):
    try:
        url = config.SS_UPDATE_URL+'/Updtime.'+str(id)
        updtime = urllib2.urlopen(url).read()
        if not updtime.startswith('error'):
            config.SS_DB_UPDTIME = urllib2.urlopen(url).read()
            config.savecfg()
            return 'ok'
    except Exception as what:
        return 'error: '+what.__str__()

def download_updates(dbname='verycd',ids=['5420'],httpconn=httplib.HTTPConnection("www.simplecd.org")):
    uri = '/'+config.SS_UPDATE_URL.rsplit('/',1)[1]+'/'+dbname+'.'+','.join([str(x) for x in ids])
    try:
        httpconn.request('GET', uri)
        r = httpconn.getresponse()
        rawdata = r.read()
        rawdata = try_ungzip(rawdata)
        if rawdata.startswith('error') or rawdata.startswith('<html'):
            print rawdata
            return rawdata
        open(dbname+'.updates','a').write(rawdata.encode('utf-8'))
    except Exception as what:
        print what.__str__()
        return 'error: '+what.__str__()    

def apply_updates(dbname='verycd',dlgupdate=None,max=0):
    args = {
            'verycd':{'len':11,'num':[0],'cnt1':max*3/6+1,'cnt2':max*4/6-2,'pc':10},
            'comment':{'len':4,'num':[0,3],'cnt1':max*4/6+1,'cnt2':max*5/6-2,'pc':100},
            'lock':{'len':7,'num':[0,1,6],'cnt1':max*5/6+1,'cnt2':max*6/6-2,'pc':10},
            }
    repeat = args[dbname]['len']-1
    nums = args[dbname]['num']
    sql = 'replace into '+dbname+' values ('+'?,'*repeat+'?)'
    db = sqlite3.connect(config.SS_HOME_DIR+'/simplecd/'+dbname+'.sqlite3.db')
    db.text_factory=str
    c = db.cursor()
    cnt1 = args[dbname]['cnt1']
    cnt2 = args[dbname]['cnt2']
    feq = args[dbname]['pc']
    try:
        count=1
        if dlgupdate:
            dlgupdate(cnt1,"Reading from "+dbname+'.updates...')
        rawdata = open(config.SS_HOME_DIR+'/'+dbname+'.updates','rb').read().decode('utf-8')
        pat = r'(\d{4,})__>@!@<__'+r'(.*?)__>@!@<__'*repeat
	alls = re.compile(pat,re.DOTALL).findall(rawdata)
#    	pos = [0]
#    	cur = rawdata.find('__>_<__')
#    	while cur != -1:
#            pos.append(cur+7)
#            cur = rawdata.find('__>_<__',cur+1)
#        j = 0
#        alls = []
#        row = []
#        for i in range(len(pos)-1):
#            item = rawdata[pos[i]:pos[i+1]-7]
#            row.append(item)
#            j += 1
#            if j == repeat+1:
#                alls.append(row)
#                j = 0
#                row = []
        count = 0
        nsqls = len(alls)
        for values in alls:
            values = [ x for x in values ]
            for i in nums:
                try:
                    values[i] = long(values[i])
                    if dbname=='lock' and i==1:
                        values[i] = bool(values[i])
                except:
                    continue
            values = tuple(values)
	    try:
                c.execute(sql,values)
            except Exception as what:
                print what,values
            count += 1
            if count % feq == 0 and dlgupdate:
                dlgupdate(cnt1+(cnt2-cnt1)*count/nsqls,"Processing SQL %d"%count)
        if dlgupdate:
            dlgupdate(cnt2,"Commiting changes to "+dbname)
        db.commit()
        c.close()
    except Exception as what:
        print what,dbname
        c.close()
        db.commit()

def delete_tempfiles():
    try:
        os.remove(config.SS_HOME_DIR+'/verycd.updates')
        os.remove(config.SS_HOME_DIR+'/comment.updates')
        os.remove(config.SS_HOME_DIR+'/lock.updates')
        return 'ok'
    except Exception as what:
        print what
	return 'error: file not found'

def update(dbname='verycd',ids=['5420']):
    args = {
            'verycd':{'len':11,'num':[0],},
            'comment':{'len':4,'num':[0,3],},
            'lock':{'len':7,'num':[0,1,6],},
            }
    repeat = args[dbname]['len']-1
    nums = args[dbname]['num']
    sql = 'replace into '+dbname+' values ('+'?,'*repeat+'?)'
    url = config.SS_UPDATE_URL+'/'+dbname+'.'+','.join([str(x) for x in ids])
    req = urllib2.Request( url = url, headers = headers )
    db = sqlite3.connect(config.SS_HOME_DIR+'/simplecd/'+dbname+'.sqlite3.db')
    db.text_factory=str
    c = db.cursor()
    try:
        rawdata = urllib2.urlopen(req).read()
        rawdata = try_ungzip(rawdata)
        if rawdata.startswith('error'):
            return rawdata
        pat = r'(.*?)__>@!@<__'*(repeat+1)
        alls = re.compile(pat,re.DOTALL).findall(rawdata)
        for values in alls:
            values = [ x for x in values ]
            for i in nums:
                values[i] = long(values[i])
            values = tuple(values)
            c.execute(sql,values)
        db.commit()
        c.close()
        return 'ok'
    except Exception as what:
        c.close()
        db.commit()
        return 'error: '+what.__str__()

def update_from_files():
    updts = os.listdir('updates')
    updts = [ x for x in updts if x.endswith('.tar.gz') ]
    for updt in updts:
        import tarfile
        tar = tarfile.open("updates/"+updt)
        tar.extractall()
        tar.close()
        apply_updates('verycd')
        apply_updates('lock')
        apply_updates('comment')
        delete_tempfiles()

def update_timestamp():
    db = sqlite3.connect(config.SS_HOME_DIR+'/simplecd/verycd.sqlite3.db')
    db.text_factory=str
    c = db.cursor()
    c.execute('select updtime from verycd order by updtime desc')
    updtime = c.fetchone()[0]
    c.close()
    config.SS_DB_UPDTIME = str(int(time.mktime(time.strptime(updtime,'%Y/%m/%d %H:%M:%S'))))
    config.savecfg()

def get_update_ids():
    url = config.SS_UPDATE_URL+'/'+config.SS_UPDATE_METHOD+'.'+config.SS_DB_UPDTIME+','+config.SS_VERSION
    req = urllib2.Request( url = url, headers = headers )
    try:
        idstring = urllib2.urlopen(req).read()
        idstring = try_ungzip(idstring)
        if idstring.startswith('new:'):
            return [idstring]
        ids = idstring[4:].split('.')
        if ids[0] =='':
            return []
        else:
            return ids
    except:
        return []

if __name__ == '__main__':
    print get_update_ids()
    print update('verycd',['2800618'])
#    print update_db_updtime('2775316')
#    print apply_updates('verycd')
