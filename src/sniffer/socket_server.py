#!/usr/bin/env python
# -*- coding=utf-8 -*-

import socket
import sys
import binascii

HOST = ''    # Symbolic name meaning all available interfaces
PORT = 0    # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + repr(msg[1])
    sys.exit()
    
print 'Socket bind complete'

s.listen(10)
print 'Socket now listening'

while 1:
    print 1
    #wait to accept a connection - blocking call
    conn, addr = s.recv(65535)
    
    #display client information
    print 'Connected with ' + addr[0] + ':' + str(addr[1])