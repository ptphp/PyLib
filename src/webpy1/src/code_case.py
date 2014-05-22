#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
from web.contrib.auth import DBAuth

web.config.debug = False
urls = (
        "/", "hello",        
        )
render = web.template.render('templates')
settings = dict(
                template_login = render.login,
                template_reset_token  = render.reset_token,
                template_reset_email   = render.reset_email,
                template_reset_change   = render.reset_change,
                )
#db = web.database(dbn='sqlite', db='login.sqlite3.db')
db = web.database(dbn='mysql', db='webpy', user='root', pw='pb200898')
app = web.application(urls, locals())
mysession = web.session.Session(app, web.session.DiskStore('sessions'))
auth = DBAuth(app, db, mysession, **settings)

class hello:
    
    @auth.protected()
    def GET(self):     
        #auth.createUser('admin',None)   
        return 'good luck!'
#class login:
    #def POST(self):        
        #return 'good luck!'


if __name__ == "__main__":
    app.run()