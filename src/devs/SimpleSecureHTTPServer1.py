# -*- coding:utf8 -*- 
import httplib 
import cookielib
import urllib2
import urllib

# 用chilkat拆分pfx得到key,cert的pem格式
key_file = 'chilkat_pkey.pem'
cert_file = 'chilkat_cert.pem'

class HTTPSClientAuthConnection(httplib.HTTPSConnection):
    def __init__(self, host, timeout=None):
        httplib.HTTPSConnection.__init__(self, host, key_file=key_file, cert_file=cert_file)
        self.timeout = timeout # Only valid in Python 2.6

class HTTPSClientAuthHandler(urllib2.HTTPSHandler):
    def https_open(self, req):
        return self.do_open(HTTPSClientAuthConnection, req)

class ICBCAPI(object):
    def __init__(self):
        self._cookiejar = cookielib.CookieJar()

    def get(self, url, **data):
        parameters = urllib.urlencode(data)
        opener = urllib2.build_opener(urllib2.HTTPHandler(), HTTPSClientAuthHandler(), urllib2.HTTPCookieProcessor(self._cookiejar))
        req = urllib2.Request(url, parameters)
        server_response = opener.open(req).read()
        return urllib2.unquote(server_response)

def test():
    api = ICBCAPI()
    apiUrl = "https://corporbank3.dccnet.com.cn/servlet/ICBCINBSEBusinessServlet"
    merReqData = '''
    <?xml version="1.0" encoding="GBK\" standalone="no" ?>
    <ICBCAPI>
        <in>
            <orderNum>填你们自己的</orderNum>
            <tranDate>填你们自己的</tranDate>
            <ShopCode>填你们自己的</ShopCode>
            <ShopAccount>填你们自己的</ShopAccount>
        </in>
    </ICBCAPI>'''
    print api.get(apiUrl, APIName='EAPI', APIVersion='001.001.002.001', MerReqData=merReqData)
    
if __name__ == '__main__':
    test() 
