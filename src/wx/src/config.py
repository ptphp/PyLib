#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys
from threading import Thread
from subprocess import Popen

#[Environment Section]
SS_PYTHON_EXE = r'C:\Python27\Pythonw.exe'
SS_HOME_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
SS_VERSION = '0.1.2c'

#[Common Section]
# DO NOT CHANGE THIS SECTION UNLESS YOU KNOW WHAT DO THEY DO
SS_PORT = '10101'
SS_UPDATE_METHOD = 'Getids'
SS_UPDATE_URL = 'http://www.simplecd.org/check_update'
SS_UPDATE_SOURCE = 'verycd'
SS_MAX_THREADS = '8'


#[DB Section]
SS_DB_UPDTIME = '1286834582'

#[User Section]
SS_USERNAME = 'trial'
SS_PASSWORD = 'trial'


#[Web Server Section]
SS_WEB_SERVER = None


#[Conf file handling]
cfg = 'default.cfg'
if os.path.exists(SS_HOME_DIR+'/'+cfg):
    settings = open(cfg).read().split('\n')
    for x in settings:
        if x.startswith('SS_'):
            pair = x.split('=')
            globals()[pair[0]]=pair[1]
else:
    settings = globals()
    output = '\n'.join([ k+'='+v for k,v in settings.items() if k.startswith('SS_') and k != 'SS_WEB_SERVER' and v ])
    open(cfg,'w').write(output)

#[Functions]
def savecfg():
    settings = globals()
    output = '\n'.join([ k+'='+v for k,v in settings.items() if k.startswith('SS_') and k != 'SS_WEB_SERVER' and v ])
    open(cfg,'w').write(output)   

def run_server():
    global SS_WEB_SERVER
    #SS_WEB_SERVER = Popen(args=[SS_PYTHON_EXE,['"'+SS_HOME_DIR+'/simplecd/code.py" ',SS_PORT]],cwd=SS_HOME_DIR+'/simplecd')
    SS_WEB_SERVER = Popen(args=[SS_HOME_DIR+'\\simplecd\\server.exe',SS_PORT],cwd=SS_HOME_DIR+'\\simplecd')

def stop_server():
    global SS_WEB_SERVER
    if SS_WEB_SERVER:
        SS_WEB_SERVER.kill()
        SS_WEB_SERVER.wait()
    SS_WEB_SERVER = None

def restart_server():
    stop_server()
    run_server()

if __name__ == '__main__':
    run_server()
    import time
    time.sleep(1)
    stop_server()
