#!/usr/bin/python
#encoding:utf8
'''
Created on 11.06.2010
Copyright (C) 2010 Alexander S. Razzhivin ( site http://httpbots.com  )
 
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
# 
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
# 
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see .
'''
import sys
import socket

FILTER=''.join([(len(repr(chr(x)))==3) and chr(x) or '.' for x in range(256)])

def dump(src, length=8):
    N=0; result=''
    while src:
       s,src = src[:length],src[length:]
       hexa = ' '.join(["%02X"%ord(x) for x in s])
       s = s.translate(FILTER)
       result += "%04X   %-*s   %s\n" % (N, length*3, hexa, s)
       N+=length
    return result

def main():
  num_of_packets = 3
  s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
  for i in range(0, num_of_packets):
    packet = s.recv(16000)
    print "Got a %d byte packet\n" % len(packet)
    print dump(packet)
  
if __name__ == '__main__':
  main()