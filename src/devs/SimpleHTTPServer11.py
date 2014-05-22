import BaseHTTPServer, SimpleHTTPServer
import ssl

web_server = BaseHTTPServer.HTTPServer(('localhost', 443), SimpleHTTPServer.SimpleHTTPRequestHandler)
web_server.socket = ssl.wrap_socket (web_server.socket,
                                     server_side=True,
                                     certfile="D:\\Dholer\\local\\Apache2.2\\conf\\sslcert\\server.crt",
                                     keyfile="D:\\Dholer\\local\\Apache2.2\\conf\\sslcert\\server.key")
web_server.serve_forever()
