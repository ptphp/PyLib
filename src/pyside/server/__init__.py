import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
HandlerClass = SimpleHTTPRequestHandler
ServerClass  = BaseHTTPServer.HTTPServer
server_address = ('127.0.0.1', 8000)
HandlerClass.protocol_version = "HTTP/1.0"
httpd = ServerClass(server_address, HandlerClass)
sa = httpd.socket.getsockname()
httpd.serve_forever()