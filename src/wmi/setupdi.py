'''
Created on Jan 24, 2013

@author: joseph
'''
from ctypes import *
from ctypes.wintypes import *

NULL = 0
INVALID_HANDLE_VALUE = -1
DIGCF_PRESENT = 0x00000002
DIGCF_ALLCLASSE = 0x00000004
SPDRP_DEVICEDESC = 0
NO_ERROR = 0
ERROR_INSUFFICIENT_BUFFER = 122
ERROR_NO_MORE_ITEMS = 259

setupapi = windll.setupapi
SetupDiGetClassDevs = setupapi.SetupDiGetClassDevsW
SetupDiEnumDeviceInfo = setupapi.SetupDiEnumDeviceInfo
SetupDiGetDeviceRegistryProperty = setupapi.SetupDiGetDeviceRegistryPropertyW
SetupDiDestroyDeviceInfoList = setupapi.SetupDiDestroyDeviceInfoList

class GUID(Structure):
    _fields_ = [("Data1", c_ulong),
    ("Data2", c_ushort),
    ("Data3", c_ushort),
    ("Data4", c_ubyte * 8)]

class SP_DEVINFO_DATA(Structure):
    _fields_ = [("cbSize", DWORD),
    ("ClassGuid", GUID),
    ("DevInst", DWORD),
    ("Reserved", c_void_p)
    ]


DeviceInfoData = SP_DEVINFO_DATA()
hDevInfo = SetupDiGetClassDevs(NULL,0,0,DIGCF_PRESENT)# | DIGCF_ALLCLASSE)
print hDevInfo
if hDevInfo == INVALID_HANDLE_VALUE:
    pass#exit(1)
    
print GetLastError(), FormatError()

DeviceInfoData.cbSize = sizeof(SP_DEVINFO_DATA)

for i in range(10000):
    
    #if not SetupDiEnumDeviceInfo(hDevInfo, i, byref(DeviceInfoData)):
    #    break
    DataT = DWORD()
    buff = create_unicode_buffer(0)
    buff_lenth = DWORD(0)
    
    while not SetupDiGetDeviceRegistryProperty(hDevInfo,byref(DeviceInfoData),SPDRP_DEVICEDESC,byref(DataT),byref(buff),buff_lenth,byref(buff_lenth)):
        if GetLastError() == ERROR_INSUFFICIENT_BUFFER:
            buff = create_unicode_buffer(buff_lenth.value)
        else:
            print FormatError()
            break
        
        print u"Result: {}".format(buff.value)
    
        if GetLastError() != NO_ERROR and GetLastError() != ERROR_NO_MORE_ITEMS:
            print FormatError()
            exit(1)