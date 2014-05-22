# -.- coding:utf-8 -.-
'''
Created on 2011-11-19

@author: icejoywoo
'''
import socket
import datetime
import os

s = socket.socket()

host = socket.gethostname()
print host
port = 80
# 绑定服务器socket的ip和端口号
s.bind((host, port))

# 服务器名�?版本�?
server_name = "MyServerDemo/0.1"

# 缓存时间, 缓存�?���?
expires = datetime.timedelta(seconds=60)
# GMT时间格式
GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'

# 可接收五个客户端
s.listen(5)

print "You can see a HelloWorld from this server in ur browser, type in", host, "\r\n"

# 服务器循�?
while True:
    c, addr = s.accept()
    print "Got connection from", addr, "\r\n"
    
    print "--Request Header:"
    # 接收浏览器的请求, 不作处理
    request = c.recv(1024)
    request_lines = request.split('\r\n')
    request_map = {}
    
    request_method = request_lines[0].split(' ')[0] # GET POST DELETE HEAD
    request_url = request_lines[0].split(' ')[1]
    request_http_ver = request_lines[0].split(' ')[2].split('/')[1]
    
    print '''request_method: %s
request_url: %s
request_http_version: %s
    ''' % (request_method, request_url, request_http_ver)
    
    # 提取头信息保存到字典�?
    for line in request_lines[1:-2]:
        if len(line) != 0:
            request_map[line.split(':')[0].strip()] = line.split(':')[1].strip()
    try:
        if request_url == "/":
            content = open("index.html", "rb").read()
            response_code = "200 OK"
        elif os.path.isdir(request_url[1:]):
            content = open(request_url[1:] + "/index.html", "rb").read()
            response_code = "200 OK"
        elif os.path.isfile(request_url[1:]):
            content = open(request_url[1:], "rb").read()
            response_code = "200 OK"
        else:
            response_code = "400 Not Found" # 文件未找�?
            content = "<h1>Page not found!</h1>"
    except:
            response_code = "500 Internal Error" # 执行有错�?
            content = "<h1>500, 你懂�?</h1>"
    
    # 获得请求的时�?
    now = datetime.datetime.utcnow()

    response = '''HTTP/1.1 %s
Server: %s
Date: %s
Expires: %s
Content-Type: text/html;charset=utf8
Content-Length: %s
Connection: keep-alive

%s''' % (
response_code,
server_name,
now.strftime(GMT_FORMAT),
(now + expires).strftime(GMT_FORMAT),
len(content),
content
)
    # 发�?回应
    c.send(response)
    print "--Response:\r\n", response
    c.close()
