import web 

urls=(
      "/","Hello",
      "/(*.?)","Hello",
      )

app = web.application(urls,globals())

class Hello:
    def GET(self):
        return "hello "
    
    
if __name__ =="__main__":
    app.run()