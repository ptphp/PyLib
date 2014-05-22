# -*- coding=utf-8 -*-
'''
Created on Jan 29, 2013

@author: joseph
'''

import wmi
#wmi_instance = wmi.WMI(moniker="ROOT/WMI")
#ret_instance = wmi_instance.query("SELECT * FROM Win32_BaseBoard WHERE (SerialNumber IS NOT NULL)")
#print ret_instance
#for t in ret_instance:
#    print t.InstanceName,"Current Temperature: ",(t.CurrentTemperature-2732)/10


#wmic DESKTOPMONITOR get name^,ScreenWidth^,ScreenHeight^,PNPDeviceID /value 获取当前显示器型号及分辨率


c = wmi.WMI ()


for cpu in c.Win32_DesktopMonitor():    
    print cpu
    print cpu.StatusInfo
    
    
