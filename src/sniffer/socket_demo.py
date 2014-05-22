#!/usr/bin/env python
# -*- coding=utf-8 -*-
'''
Created on 2013-3-16
@author: Joseph
#http://www.cnblogs.com/MikeZhang/archive/2012/08/30/pythonSniffer20120829.html
http://www.cnblogs.com/rollenholt/archive/2012/07/14/2591017.html
#http://www.binarytides.com/packet-sniffer-code-in-c-using-linux-sockets-bsd-part-2/
http://my.oschina.net/yisenn/blog/85065
http://www.binarytides.com/category/sockets/python-sockets-sockets/
http://www.rosoo.net/a/201003/8774.html

/*
 * Protocols (RFC 1700)
 */
#define IPPROTO_IP              0               /* dummy for IP */
#define IPPROTO_UDP             17              /* user datagram protocol */
#define IPPROTO_TCP             6               /* tcp */

'''
import socket
import binascii

def decodeIpHeader(packet):
    mapRet = {}
    mapRet["version"] = (int(ord(packet[0])) & 0xF0)>>4
    mapRet["headerLen"] = (int(ord(packet[0])) & 0x0F)<<2
    mapRet["serviceType"] = hex(int(ord(packet[1])))
    mapRet["totalLen"] = (int(ord(packet[2])<<8))+(int(ord(packet[3])))
    mapRet["identification"] = (int( ord(packet[4])>>8 )) + (int( ord(packet[5])))
    mapRet["id"] = int(ord(packet[6]) & 0xE0)>>5
    mapRet["fragOff"] = int(ord(packet[6]) & 0x1F)<<8 + int(ord(packet[7]))
    mapRet["ttl"] = int(ord(packet[8]))
    mapRet["protocol"] = int(ord(packet[9]))
    mapRet["checkSum"] = int(ord(packet[10])<<8)+int(ord(packet[11]))
    mapRet["srcaddr"] = "%d.%d.%d.%d" % (int(ord(packet[12])),int(ord(packet[13])),int(ord(packet[14])), int(ord(packet[15])))
    mapRet["dstaddr"] = "%d.%d.%d.%d" % (int(ord(packet[16])),int(ord(packet[17])),int(ord(packet[18])), int(ord(packet[19])))
    mapRet["Options"] = ord(packet[24])>>8
    return mapRet 
# the public network interface 
HOST = socket.gethostbyname(socket.gethostname())
print HOST
# create a raw socket and bind it to the public interface
#socket.IPPROTO_IP
#socket.IPPROTO_TCP
s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
s.bind((HOST, 80))
while 1:    

    # Include IP headers
    #s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    
    # receive all packages
    s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
    # receive a package
    rec = s.recvfrom(65565)
    packet = rec[0]
    
    # disabled promiscuous mode
    s.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
    
    print rec[1]
    print rec[0]
    if len(packet) == 0:
        s.close()
    else:
        
        mapIpTmp = decodeIpHeader(packet)   
        #print mapIpTmp     
        l = ['74.125.128.125','61.135.169.125','114.112.54.243','74.125.235.201']
        if mapIpTmp['protocol'] == 6 and mapIpTmp['srcaddr'] not in l:       
            pass
            #print mapIpTmp['Options']
            #print packet
            #print packet
            #print binascii.hexlify(packet) 
        
        
        
    
if __name__ == '__main__':
    pass