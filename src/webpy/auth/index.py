import web
from web.contrib.auth import DBAuth

urls = (
    '/', 'index',
    '/Login', 'Login',
    '/login', 'Login',
    '/somePage', 'somePage',
)
app = web.application(urls, locals())
db = web.database(dbn='mysql', db='webpy_demo', user='dbuser', pw='201108')

render = web.template.render('templates')
settings = dict(
    template_login = render.login,
)
mysession = web.session.Session(app, web.session.DiskStore('sessions'))
auth = DBAuth(app, db, mysession, **settings)

class index:
    def GET(self):
        return "hello!"
class somePage:
    @auth.protected()
    def GET(self):
        return "somep other!"
if __name__ =="__main__":
    app.run()