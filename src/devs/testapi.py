import urllib2
import urllib
from hashlib import md5

#print md5("admin").hexdigest()

def try_connect():    
    url = "http://test1.spinutopia.com/users/signin/json"    
    query = {}
    query['username'] = "liseor"
    query['password'] = md5("200898").hexdigest()
    #"username=john@spinutopia.com&password=md5encryptedpasswordorfacebookid"
    data = urllib.urlencode(query)
    req = urllib2.Request(url, data)
    req.add_header("Authorization", "TRUEREST")
    
    h = urllib2.HTTPHandler(debuglevel=1)
    opener = urllib2.build_opener(h)
    res = opener.open(req)
    print res.read()
try_connect()



'''
Request:
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
POST /users/signin/json HTTP/1.1
Accept-Encoding: identity
Content-Length: 57
Host: test1.spinutopia.com
User-Agent: Python-urllib/2.7
Connection: close
Content-Type: application/x-www-form-urlencoded
Authorization: TRUEREST

username=liseor&password=41d2719c9e51140ac190699374a3a38a'


Response:
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
reply: 'HTTP/1.1 200 OK\r\n'
header: Server: nginx
header: Date: Thu, 26 Apr 2012 08:28:40 GMT
header: Content-Type: text/html; charset=UTF-8
header: Transfer-Encoding: chunked
header: Connection: close
header: Vary: Accept-Encoding
header: X-Powered-By: PHP/5.3.10
header: Set-Cookie: PHPSESSID=vk6ova1v7qek927vokr9jbflc2; path=/; domain=spinutopia.com
header: Expires: Thu, 19 Nov 1981 08:52:00 GMT
header: Cache-Control: no-store, no-cache, must-revalidate, post-check=0, pre-check=0
header: Pragma: no-cache
    
{"error_stat":"error","msg":"Incorrect username\/password"}


'''
