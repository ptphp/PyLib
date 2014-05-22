'''
Created on Oct 20, 2012

@author: joseph
'''
import string, sys
import re, StringIO

TAB=4

def format():
    ss = "unformated.css"
    f = open (ss, "r")
    data = f.read()
    f.close()
    
    dlen = len(data)
    i = 0
    buf = StringIO.StringIO()
    start = 0
    while i < dlen:
        if data[i] == '{':
            
            buf.write(data[start:i] + ' { ')
            i = i + 1
            start = i
        elif data[i] == '}':
            last = string.strip(data[start:i])
            if last:
                buf.write(' '*TAB + last + ';')
            buf.write(' } ')
            i = i + 1
            start = i
            
        elif data[i] == ';':
            line = string.strip(data[start:i])
            
            buf.write(' '*TAB + line + '; ')
            i = i + 1
            start = i
        
        else:
            i = i + 1
    buf.write(data[start:i+1])
    
    return buf.getvalue()
    
    
if __name__ == '__main__':
    #if len(sys.argv) == 1:
        #print 'usage: cssformat.py filename'
        #sys.exit()
    
    ret = format()
    #ret = format(sys.argv[1])
    print ret