#!user/bin/env python
# -*- coding: utf8 -*-
##http://www.tornadoweb.org/documentation/index.html
import sys
import tornado.ioloop
import tornado.web
from config.urls import urls
from config.settings import settings
port = 8000
if len(sys.argv) > 1:
    port = int(sys.argv[1])

application = tornado.web.Application(urls,**settings)

if __name__ == "__main__":    
    try:
        print "server is running at: %d" % port
        application.listen(port)
        tornado.ioloop.IOLoop.instance().start()        
    except Exception as what:
        print what
        exit(1)
