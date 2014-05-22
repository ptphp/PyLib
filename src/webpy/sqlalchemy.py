#!/usr/bin/env python
#-*-coding:utf-8-*-
import string
import random
import web
from sqlalchemy.orm import scoped_session,sessionmaker
from models import *

urls = (
        "/","add",
        "/view","view"
        )
def load_sqla(handler):
    web.ctx.orm = scoped_session(sessionmaker(bind=engine))
    try:
        return handler()
    except web.HTTPError:
        web.ctx.orm.commit()
        raise
    except:
        web.ctx.orm.rolback()
    finally:
        web.ctx.orm.commit
app = web.application(urls,locals())
app.add_processor(load_sqla)

class add:
    def Get(self):
        web.header("Content-type","text/html")
        fname = "".join(random.choice(string.letters) for i in range(4))
        lname = "".join(random.choice(string.letters) for i in range(7))
        u =User(name = fname,
                fullname = fname + " " + lname,
                password = 542
                )
        web.ctx.orm.add(u)
        return "added:" +web.websafe(str(u)) \
                            +"<br />" \
                            +"<a href=\"/view\">view all</a>"
class view:
    def GET(self):
        web.header("Content-type","text/plain")
        return "\n".join(map(str,web.ctx.orm.query(User).all))
if __name__ =="__main__":
    app.run()
        
        
        