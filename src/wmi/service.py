# -*- coding=utf-8 -*-

import win32serviceutil 
import win32service 
import win32event 


import os, sys
import time
import wmi,zlib,json


def log(log_string):
    f=open("c:\\log.txt",'a+')
    f.write(str(log_string)+"\n\n")
    f.close()
def get_sys_info():
    syinfo = {}
    tmplist = []
    encrypt_str = ""
    c = wmi.WMI ()
    
    cpu_tmp = []
    for cpu in c.Win32_Processor():
        #cpu 序列号
        cpu_item = {}
        #print cpu
        encrypt_str = encrypt_str + cpu.ProcessorId.strip()
        #print "cpu id:", cpu.ProcessorId.strip()
        cpu_item['ProcessorId'] = cpu.ProcessorId.strip()
        cpu_item['Name'] = cpu.Name.strip()
        cpu_tmp.append(cpu_item)    
    syinfo['cpu'] = cpu_tmp
    
    dis_tmp = []    
    for physical_disk in c.Win32_DiskDrive():
        dis_itm = {}
        dis_itm['Caption'] = physical_disk.Caption.strip()
        dis_itm['SerialNumber'] = physical_disk.SerialNumber.strip()
        dis_itm['Size'] = long(physical_disk.Size)/1000/1000/1000
        dis_tmp.append(dis_itm)    
        encrypt_str = encrypt_str+physical_disk.SerialNumber.strip()
    syinfo['disk'] = dis_tmp
    
    
    tmp = {}
    for board_id in c.Win32_BaseBoard():
        #print board_id
        #主板序列号
        tmp['SerialNumber'] = board_id.SerialNumber.strip()
        tmp['Manufacturer'] = board_id.Manufacturer.strip()
        encrypt_str = encrypt_str+board_id.SerialNumber.strip()
    syinfo['board'] = tmp
    
    tmp = {}
    for bios_id in c.Win32_BIOS():
        #print bios_id
        tmp['SerialNumber'] = bios_id.SerialNumber.strip()
        #bios 序列号
        encrypt_str = encrypt_str+bios_id.SerialNumber.strip()
    syinfo['bios'] = tmp   

    #加密算法
    syinfo['encrypt_str'] = zlib.adler32(encrypt_str)
    return syinfo 


class test1(win32serviceutil.ServiceFramework): 
     _svc_name_ = "test_python" 
     _svc_display_name_ = "test_python" 
     def __init__(self, args): 
         win32serviceutil.ServiceFramework.__init__(self, args) 
         self.hWaitStop = win32event.CreateEvent(None, 0, 0, None) 

     def SvcStop(self): 
         self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING) 
         win32event.SetEvent(self.hWaitStop)
         
     def SvcDoRun(self): 
         syinfo = get_sys_info()         
         while 1:
             print syinfo
             syinfo = get_sys_info()      
             log(json.dumps(syinfo))
             time.sleep(1)
         win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE) 

if __name__=='__main__': 
     win32serviceutil.HandleCommandLine(test1)
     