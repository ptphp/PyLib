# -*- coding: utf-8 -*- 
#!/usr/bin/env python 
#http://www.linuxany.com/archives/667.html
#http://blog.csdn.net/jhqin/article/details/5548656
import os, sys
import time
import wmi,zlib

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
if __name__ == "__main__":
#     a = get_cpu_info()
     syinfo = get_sys_info()
     print syinfo
     
     
     
"""
def get_cpu_info() :
    tmpdict = {}
    tmpdict["CpuCores"] = 0
    c = wmi.WMI()
    #print c.Win32_Processor().['ProcessorId']
    #print c.Win32_DiskDrive()
    for cpu in c.Win32_Processor():     
        #print cpu
        print "cpu id:", cpu.ProcessorId.strip()
        tmpdict["CpuType"] = cpu.Name
        try:
            tmpdict["CpuCores"] = cpu.NumberOfCores
        except:
            tmpdict["CpuCores"] += 1
            tmpdict["CpuClock"] = cpu.MaxClockSpeed 
    return tmpdict
 
def _read_cpu_usage():
    c = wmi.WMI ()
    for cpu in c.Win32_Processor():
        return cpu.LoadPercentage
 
def get_cpu_usage():
    cpustr1 =_read_cpu_usage()
    if not cpustr1:
        return 0
    time.sleep(2)
    cpustr2 = _read_cpu_usage()
    if not cpustr2:
        return 0
    cpuper = int(cpustr1)+int(cpustr2)/2
    return cpuper
"""