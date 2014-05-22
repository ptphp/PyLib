from kyotocabinet import DB
import sys,time


#format datetime
def format_datetime(timestamp):
         return time.strftime('%Y.%m.%d @ %H:%M',time.localtime(timestamp))

#创建数据库对象
db=DB()

# open the database
if not db.open("../data/db.kch", DB.OWRITER | DB.OCREATE):
         print >>sys.stderr, "open error: " + str(db.error())


cid='1'

#build for marks form
if not db.set("mark:"+cid+":markid", "1") or\
   not db.set("mark:"+cid+":userid", "1") or\
   not db.set("mark:"+cid+":boardid", "1") or\
   not db.set("mark:"+cid+":fileid", "1") or\
   not db.set("mark:"+cid+":description", "mark的内容描述") or\
   not db.set("mark:"+cid+":content", "哇。。阳光暖暖的，好惬意的。") or\
   not db.set("mark:"+cid+":ups", "100") or\
   not db.set("mark:"+cid+":downs", "10") or\
   not db.set("mark:"+cid+":hits", "110") or\
   not db.set("mark:"+cid+":order", "1") or\
   not db.set("maks:"+cid+":createdata", int(time.time())) or\
   not db.set("maks:"+cid+":commentcount", "8") or\
   not db.set("mark:count", "3"):
         print >>sys.stderr, "set error: " + str(db.error())

#build for comments form
if not db.set("comment:"+cid+":markid", "1") or\
   not db.set("comment:"+cid+":userid", "1") or\
   not db.set("comment:"+cid+":content", "1") or\
   not db.set("comment:"+cid+":ups", "100") or\
   not db.set("comment:"+cid+":downs", "10") or\
   not db.set("comment:"+cid+":order", "1") or\
   not db.set("comment:"+cid+":createdata", int(time.time())) or\
   not db.set("comment:count", "3"):
         print >>sys.stderr, "set error: " + str(db.error())


import hashlib
key=hashlib.sha256('ghcjeijcjxojnceicojekncGYGHBJjijjGUiJIjIHijOIIhuiHi').hexdigest()

#build for files form
if not db.set("file:"+key+":id", "1") or\
   not db.set("file:"+key+":server", "1") or\
   not db.set("file:"+key+":key", key) or\
   not db.set("file:"+key+":type", "image/jpeg") or\
   not db.set("file:"+key+":width", "200") or\
   not db.set("file:"+key+":height", "328") or\
   not db.set("file:"+key+":createdata", int(time.time())) or\
   not db.set("file:"+key+":ups", "100") or\
   not db.set("file:"+key+":downs", "10") or\
   not db.set("file:"+key+":hits", "110") or\
   not db.set("file:count", "3"):
         print >>sys.stderr, "set error: " + str(db.error())


cid='1'

#build for categories form
if not db.set("category:"+cid+":name", "艺 术") or\
   not db.set("category:"+cid+":urlname", "art") or\
   not db.set("category:"+cid+":id", "1") or\
   not db.set("category:"+cid+":title", "艺术大类") or\
   not db.set("category:"+cid+":description", "艺术大类的详细内容描述") or\
   not db.set("category:"+cid+":group", "1") or\
   not db.set("category:"+cid+":order", "1") or\
   not db.set("category:"+cid+":createdata", int(time.time())) or\
   not db.set("category:"+cid+":ups", "100") or\
   not db.set("category:"+cid+":downs", "10") or\
   not db.set("category:"+cid+":hits", "110") or\
   not db.set("category:count", "3"):
         print >>sys.stderr, "set error: " + str(db.error())

email='root@some.com'
#build for users form
if not db.set("user:"+email+":email", "root@garning.com") or\
   not db.set("user:"+email+":nickname", "root") or\
   not db.set("user:"+email+":urlname", "root") or\
   not db.set("user:"+email+":password", "paspas") or\
   not db.set("user:"+email+":createdate",  int(time.time())) or\
   not db.set("user:"+email+":avatarid", "1722559") or\
   not db.set("user:"+email+":login_count", "179") or\
   not db.set("user:"+email+":login_date", "2012.06.02") or\
   not db.set("user:"+email+":sex", "male") or\
   not db.set("user:"+email+":id", "10") or\
   not db.set("user:"+email+":ups", "100") or\
   not db.set("user:"+email+":downs", "10") or\
   not db.set("user:"+email+":hits", "110") or\
   not db.set("user:count", "100") or\
   not db.set("user:id:1", "insion@garning.com") or\
   not db.set("user:id:2", "os@garning.com") or\
   not db.set("user:id:3", "system@garning.com"):
         print >>sys.stderr, "set error: " + str(db.error())

# retrieve records
o= format_datetime(float(db.get("file:"+key+":createdata")))
v=db.get("file:"+key+":key")
va=db.get("mark:"+cid+":description")
val = db.get("category:"+cid+":name")
valu = db.get("category:1:id")
value = db.get("user:id:1")
if value:
         print o
         print v
         print va
         print val
         print valu
         print value
else:
         print >>sys.stderr, "get error: " + str(db.error())

# close the database
if not db.close():
         print >>sys.stderr, "close error: " + str(db.error())