#!user/bin/env python
# -*- coding: utf8 -*- 
'''
Created on Jul 11, 2012

@author: joseph
'''
import urllib,urllib2
import mimetypes


def uploadfile(fields, files):
    BOUNDARY = '----------267402204411258'
    CRLF = '\r\n'
    L = []
    for (key, value) in fields:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"' % key)
        L.append('')
        L.append(value)
    for (key, filename, value) in files:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
        L.append('Content-Type: %s' % mimetypes.guess_type(filename)[0] or 'application/octet-stream')
        L.append('')
        L.append(value)
    L.append('--' + BOUNDARY + '--')
    L.append('')
    body = CRLF.join(L)
    content_type = 'multipart/form-data; boundary=%s' % BOUNDARY

    return content_type, body

if __name__ == '__main__':
    fields=[
            ('_xsrf','28d55624808042768af23188e318500a')
            ]
    ifile = "/home/joseph/Pictures/1.jpg"
    imgdata= file(ifile,"rb")
    files=[
            ('ifile',imgdata.name,imgdata.read())
        ]
    
    content_type, upload_data = uploadfile(fields, files)
            
    uploadheader={
                    "User-Agent": "Mozilla/5.0 (Windows NT 5.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
                    'Content-Type': content_type,
                    'Content-Length': str(len(upload_data))
                    }
    request = urllib2.Request("http://localhost/upload/", upload_data, uploadheader)
    res = urllib2.urlopen(request)
    print res.read()
    
    