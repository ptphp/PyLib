#!/usr/bin/env python
#-*-coding:utf-8-*-
import web
import sys,logging
import config
urls = ("","reurl","/(.*)/","redirect","/ww(.*)","index")
render = web.template.render("templates/",cache = False)
app = web.application(urls,globals())

#===============================================================================
# 加载钩子 卸载钩子
#===============================================================================
def my_loadhook():
    print "my load hook"

def my_unloadhook():
    print "my unload hook"
app.add_processor(web.loadhook(my_loadhook))
app.add_processor(web.unloadhook(my_unloadhook))

def notfound():
    return web.notfound("Sorry, the page you were looking for was not found.")
        # You can use template result like below, either is ok:
        #return web.notfound(render.notfound())
        #return web.notfound(str(render.notfound()))
def internalerror():
    return web.internalerror("Bad, bad server. No donut for you.")
app.notfound = notfound
app.internalerror = internalerror
#===============================================================================
# 保证网址有无"/",都指向同一个类
#===============================================================================
class redirect:
    def GET(self,path):
        web.seeother("/" +path)
class reurl:
    def GET(self):
        raise web.seeother("/") 

class index:
    def GET(self,code):
        ctx = web.ctx.env
        print ctx
        web.header("Content-Type","text/xml")
        return render.response(code)
    def POST(self):
        data = web.data()
        return data
web.webapi.internalerror = web.debugerror
if __name__ =="__main__":
    app.run()