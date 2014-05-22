'''
Created on Jan 24, 2013

@author: joseph
'''
#!/usr/bin/env python
# -*- coding=utf-8 -*-
from _winreg import *

class Registry():
    def query(self):
        key = OpenKey(HKEY_CLASSES_ROOT, r'*\shell\PtEditor', 0, KEY_ALL_ACCESS) 
        res = QueryValueEx(key, "")
        print res    
        
    def setRightKeyForVi(self):
        keyVal_root = '*\shell\PtEditor'
        keyVal_cmd  = '*\shell\PtEditor\Command'
        name        = ""
        value_root  = "Open with PtEditor"
        value_cmd   = "D:\pteditor\editor.exe %1"
        self.set(HKEY_CLASSES_ROOT,keyVal_root,name,value_root)
        self.set(HKEY_CLASSES_ROOT,keyVal_cmd,name,value_cmd)
        print "set %s for %s" % (keyVal_cmd,value_root)
        
    def listall(self):
        try:
            i = 0
            while True:
                subkey = EnumKey(HKEY_USERS, i)
                print subkey
            i += 1
        except WindowsError:
            # WindowsError: [Errno 259] No more data is available    
            pass

    def set(self,root,keyVal,name,value):        
        try:
            key = OpenKey(root, keyVal, 0, KEY_ALL_ACCESS)
        except:
            key = CreateKey(root, keyVal)
        SetValueEx(key, name, 0, REG_SZ, value)
        CloseKey(key)

def main():
    reg = Registry()
    reg.setRightKeyForVi()

if __name__ == '__main__':
    main()
