import sys 
from PyQt4.QtGui import QApplication 
from PyQt4.QtCore import QUrl 
from PyQt4.QtWebKit import QWebView, QWebSettings 

from SocketServer import ForkingMixIn 
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer 
from threading import Thread 

class Render(QWebView): 
    def __init__(self, url): 
        self.app = QApplication(sys.argv) 
        QWebView.__init__(self) 

        self.loadFinished.connect(self._loadFinished) 
        self.load(QUrl(url)) 
        self.app.exec_() 

    def _loadFinished(self, result): 
        self.frame = self.page().mainFrame() 
        self.app.quit() 

    def get_data(self): 
        return self.frame.toHtml().toUtf8() 

class ProxyHandler(BaseHTTPRequestHandler): 
    def do_GET(self): 
        try: 
            self._get() 
        except Exception, e: 
            print >> sys.stderr, "do_GET", self.path, repr(e), e 

    def _get(self): 
        try: 
            r = Render(self.path) 
            data = r.get_data() 
        except Exception, e: 
            print repr(e), e 
            self.send_response(417) 
            self.end_headers() 
        else: 
            self.send_response(200) 
            self.send_header("Content-type", "text/html") 
            self.send_header("Content-Length", len(data)) 
            self.end_headers() 
            self.wfile.write(data) 

class JSHttpProxyServer(ForkingMixIn, HTTPServer): 
    "JavaScript Http Proxy Server" 

def main(): 
    jhp = JSHttpProxyServer(("localhost", 3128), ProxyHandler) 
    jhp.serve_forever() 
    Render('http://www.baidu.com')

if __name__ == "__main__": 
    main() 