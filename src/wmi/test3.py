#-*- coding:utf-8 -*-
import time
import datetime
import re
import subprocess
import sys
import wmi
import os
import ConfigParser
import _winreg
import win32net
import win32api
import win32con
import win32netcon
import win32security
#DEBUG=True
#DEBUG=False
#LOGFILE=r'c:\win.log'
TIME_FORMAT=r'%Y-%m-%d %H:%M:%S'
#c=wmi.WMI(privileges=["Admin","Shutdown","Security"])
#实例化wmi类
c=wmi.WMI()
#定义myWmi类并返回实例化对象
class myWmi(object):
    #定义构造器
    def __init__(self,wmiclass,info={},name=""):
        if name:
            self.obj=wmiclass(Name=name)
        else:
            self.obj=wmiclass()
        self.info=info
        return self.obj
#定义myOs类用于系统信息查询及设置
class myOs(object):
    #定义构造器
    def __init__(self,wmiobj=c,info={}):
        #创建wmi实例
        self.obj=wmiobj.Win32_OperatingSystem()[0]                                          #用于获取计算机运行环境信息
        self.cobj=wmiobj.Win32_ComputerSystem()[0]                                          #用于获取计算机CPU数量,内存大小,主板相关信息
        self.disk_obj= wmiobj.Win32_DiskDrive()                                             #用于获取硬盘相关信息
        self.Partition_obj= wmiobj.Win32_LogicalDisk()                                      #用于获取分区相关信息
        self.networkAdapter_obj = wmiobj.Win32_NetworkAdapterConfiguration (IPEnabled=1)    #用于配置及获取网络连接相关信息
        self.process_obj = wmiobj.Win32_Processor()[0]                                      #用于获取CPU详细信息
        self.update_obj = wmiobj.Win32_QuickFixEngineering()                                #用于获取windows更新补丁相关信息
        self.info=info                                                                      #定义用于存放配置信息的字典
    def get_os_info(self):
        """
                    返回系统相关信息
        """
        self.info["os"]=self.obj.Caption                                                                                         #获取系统版本
        self.info["version"]=self.obj.CSDVersion                                                                                 #操作系统更新版本
        self.info["fullname"]=self.obj.CSName                                                                                    #获取计算机名
        self.info["localtime"]=datetime.datetime.strptime(str(str(self.obj.LocalDateTime ).split('.')[0]),'%Y%m%d%H%M%S')        #获取系统本地时间
        self.info["lastboottime"]=datetime.datetime.strptime(str(str(self.obj.LastBootUpTime ).split('.')[0]),'%Y%m%d%H%M%S')    #获取系统上次启动时间
        self.info["os_architecture"]=self.obj.OSArchitecture                                                                     #获取操作系统类型(32bit/64bit)
        self.info["mu_languages"]=self.obj.MUILanguages[0]                                                                       #获取操作系统语言版本
        self.info["SerialNumber"]=self.obj.SerialNumber                                                                          #获取操作系统序列号
        self.info["cpu_count"]=self.cobj.NumberOfProcessors                                                                      #获取cpu数量
        self.info["mainboard"]=self.cobj.Manufacturer                                                                            #获取主板厂商信息
        self.info["board_model"]=self.cobj.Model                                                                                 #获取主板型号
        self.info["systemtype"]=self.cobj.SystemType                                                                             #获取主板架构类型
        self.info["physical_memory"]=int(self.cobj.TotalPhysicalMemory)/1024/1024                                                #获取内存容量
        self.info["cpu_name"] = self.process_obj.Name                                                                            #获取cpu类型
        self.info["clock_speed"] = self.process_obj.MaxClockSpeed                                                                #获取操作系统主频
        self.info["number_core"] = self.process_obj.NumberOfCores                                                                #获取核心数量
        self.info["data_width"] = self.process_obj.DataWidth                                                                     #获取计算机的CPU数据宽度
        self.info["socket_desigination"] = self.process_obj.SocketDesignation                                                    #获取主板cpu接口类型
        self.info["l2_cache"] = self.process_obj.L2CacheSize                                                                     #获取cpu二级缓存大小
        self.info["l3_cache"] = self.process_obj.L3CacheSize                                                                     #获取cpu三级缓存大小
        return self.info
    #打印补丁更新信息
    def update_information(self):
        output=open(log_path,"a+")
        output.write('\n')
        output.write('[Update information]\r\n')
        for s in self.update_obj:
            output.write('%-10s %-10s %-20s %-10s\n' %(s.HotFixID,s.InstalledOn,s.Description,s.InstalledBy))
        output.write('\n')
    #打印磁盘信息
    def get_diskinfo(self):
        for item in self.disk_obj:
            output=open(log_path,"a+")
            output.write('\n')
            output.write('[disk info]\r\n')
            for item in self.disk_obj:
                output.write('%-25s Partition: %-3s SN: %-30s %-3sG\n' %(item.Caption,str(item.Partitions),item.SerialNumber,str(int(item.Size)/1024/1024/1024)))
                #output.write('%-30s Partition: %-5s SN: %-30s %-10s G\n' %(item.Caption,str(item.Partitions),item.SerialNumber,str((item.Size)/1024/1024/1024)))
                output.write('\n')
            break
    #打印磁盘分区信息
    def get_partitioninfo(self):
        Partition_count = len(self.Partition_obj)
        output=open(log_path,"a+")
        output.write('\n')
        output.write('[Partition info]\r\n')
        output.write('\r\n')
        for x in range(len(self.Partition_obj)):
                if self.Partition_obj[x].DriveType == 3:
                    output.write('DeviceID = %-4s FileSystem = %-5s TotalSize = %-1sG    FreeSpace = %-1sG\n' %(self.Partition_obj[x].DeviceID,self.Partition_obj[x].FileSystem,str(int(self.Partition_obj[x].Size)/1024/1024/1024),str(int(self.Partition_obj[x].FreeSpace)/1024/1024/1024)))
                    output.write('\n')
    #打印网络配置信息
    def get_networkadapter(self):
        output=open(log_path,"a+")
        output.write('\n')
        output.write('[network info]\r\n')
        for interface in self.networkAdapter_obj:
            output.write('IP Address:  %-10s\n' %interface.IPAddress[0])
            output.write('NET Mask:    %-10s\n' %interface.IPSubnet[0])
            output.write('Gateway:     %-10s\n' %interface.DefaultIPGateway)
            output.write('Pri DNS:     %-10s\n' %str(interface.DNSServerSearchOrder[0]))
            output.write('Sec DNS:     %-10s\n' %str(interface.DNSServerSearchOrder[1]))
            output.write('Real Mac:    %-10s\n' %interface.MACAddress)
            output.write('\n')
            break
    #强制关机
    def win32shutdown(self):
        self.obj.Win32Shutdown()
    #重启操作系统
    def reboot(self):
        self.obj.Reboot()
    #关闭操作系统
    def shutdown(self):
        self.obj.Shutdown()
#定义network_config类用于网络设置信息查询及设置
class network_config(object):
    #定义构造器
    def __init__(self,wmiobj=c):
        #实例化对象
        self.obj = wmiobj.Win32_NetworkAdapterConfiguration
    #设置LMHOSTS
    def config_setup(self):
        self.obj.EnableWINS(WINSEnableLMHostsLookup=False)
    #设置dns
    def tcp_config(self):
        interfaces = c.Win32_NetworkAdapterConfiguration(IPEnabled=True)
        device_count = len(interfaces)
        start_num = 0
        dns = ['202.106.196.115','202.106.0.20']
        while True:
            for first_if in interfaces:
                dns_result = first_if.SetDNSServerSearchOrder(DNSServerSearchOrder = dns)
                netbios_result = first_if.SetTcpipNetbios(TcpipNetbiosOptions = 2)
                start_num += 1
                if start_num > device_count:
                    break
            return dns_result,netbios_result
#############################
#                           #
#   Service                 #
#                           #
#############################
#定于myService()类用于系统服务检查及设置
class myService(object):
    """
    control system service
    """
    #定义构造器
    def __init__(self,name="",wmiobj=c,**kargs):
        self.name=name
        kargs={}
        args=""
        if self.name:
            self.obj=wmiobj.Win32_Service(Name=self.name)[0]    #obj in the list
        elif kargs:
            for key in kargs:
                args+=key+'='+'"'+kargs[key]+'"'+','
            args=args[:-1]
            cmd="wmiobj.Win32_Service("+args+")"
            self.obj=eval(cmd)
        else:
            self.obj=wmiobj.Win32_Service()
    def get_service_info(self):
        service_list=[]
        for ser in self.obj:
            service_dict={}
            service_dict["name"]=ser.Name
            service_dict["displayname"]=ser.Caption
            service_dict["pid"]=ser.ProcessID
            service_dict["stat"]=ser.State
            service_dict["startmode"]=ser.StartMode
            service_list.append(service_dict)
        return service_list
    #获取系统服务状态
    def status(self):
        return self.obj.State
    #启动服务
    def start(self):
        self.obj.StartService()
    #停止服务
    def stop(self):
        self.obj.StopService()
    #关闭黑名单中系统服务
    def change_mode(self,mode):
        blacklist_path = sys.path[0]+'/svr_blacklist.txt'
        f=open(blacklist_path)
        svr_blacklist = f.readlines()
        f.close()
        for b in svr_blacklist:
            b = b.strip()
            for s in self.obj:
                if  b in s.Name:
                    """
                    Three mode available: Auto, Manual and Disabled
                    """
                    s.ChangeStartMode(mode)
                else:
                    continue
            break
        #obj.ChangeStartMode(mode)
    #删除系统服务
    def delete(self):
        print "You should not delete a service, stop it instead."

#############################
#                           #
#   Process                 #
#                           #
#############################
#定义myProcess类用于进程查看
class myProcess(myWmi):
    def __init__(self,name=""):
        self.name=name
        myWmi.__init__(self,c.Win32_Process,name=self.name)
    def get_process_info(self):
        processlist=[]
        for process in self.obj:
            processlist.append((process.ProcessID,process.Name,process.CreationDate,process.ExecutablePath,process.Caption))
        return processlist
    def get_process_owner(self):
        return self.obj[0].GetOwner()
    def terminate(self):
        self.obj[0].Terminate()
#############################
#                           #
#   Software                #
#                           #
#############################
#定义mySoft类用于安装软件检查
class mySoft(myWmi):
    def __init__(self,name=""):
        self.name=name
        myWmi.__init__(self,c.Win32_Product,name=self.name)
    def get_software(self):
        softlist=[]
        for soft in self.obj:
            softlist.append((soft.Name,soft.InstallDate))
        return softlist
    def uninstall(self):
        #self.obj[0].Uninstall()
        pass
#############################
#                           #
#      User and Group       #
#                           #
#############################
'''
def dump(dict):
    for key,value in dict.items():
        print key,"=",str(value)'''
#定义myAccount类用于帐号检查及设置
class myAccount(myWmi):
    #类构造器
    def __init__(self,name="",group=""):
        self.uname=name
        self.gname=group
        self.uobj=myWmi.__init__(self,c.Win32_UserAccount,name=self.uname)
        self.guobj=myWmi.__init__(self,c.Win32_GroupUser,name=self.gname)
   #返回账户列表
    def show_user_list(self):
        ulist=[]
        for user in self.uobj:
            ulist.append(user.Name)
        return ulist
    #返回禁用的账户列表
    def show_user_info(self,username):
        info=win32net.NetUserGetInfo(None,username,3)
        info["disabled"]=user.Disabled      #Disabled is true means the account is disabled.
        info["status"]=user.Status
        return ulist
    #返回用户组
    def show_user_in_group(self):
        gulist={}
        for gu in self.guobj:
            if gu.GroupComponent.Name not in gulist:
                gulist[gu.GroupComponent.Name]=[gu.PartComponent.Name]
            else:
                gulist[gu.GroupComponent.Name].append(gu.PartComponent.Name)
        return gulist
    #返回管理员用户列表
    def show_userlist_admin(self):
        uresume = 0
        while True:
            admin_list = []
            users, total, uresume = win32net.NetLocalGroupGetMembers (None, 'Administrators', 0, uresume)
            for sid in (u['sid'] for u in users):
                username, domain, type = win32security.LookupAccountSid (None, sid)
                admin_list.append(username)
            return admin_list
            if uresume == 0:
                break
    #获取当前用户
    def get_current_user(self):
        return win32api.GetUserName()
    #删除用户
    def delete_user(self,username):
        win32net.NetUserDel(None,username)
    #添加用户
    def add_user(self,name,passwd,flags=win32netcon.UF_NORMAL_ACCOUNT|win32netcon.UF_SCRIPT,privileges=win32netcon.USER_PRIV_ADMIN):
        udata={}    #user info dict, can be gotten by win32net.NetUserGetInfo
        udata["name"]=name
        udata["password"]=passwd
        udata["flags"]=flags
        udata["priv"]=privileges
        win32net.NetUserAdd(None, 1, udata)
   #设置用户信息
    def modify_user(self,username,udict,level=2):
        win32net.NetUserSetInfo(None,username,level,udict)
    #修改用户密码
    def change_passwd(self,username,oldpass,newpass):
        win32net.NetUserChangePassword(None,username,oldpass,newpass)
    #重命名账户
    def rename_user(self,oldname,newname):
        for item in self.uobj:
            if oldname in item.id:
                item.Rename('admin')
            else:
                continue
#############################
#                           #
#   Registry                #
#                           #
#############################
#定义myRegistry类用于注册表项目检查及设置
class myRegistry(object):
    """
    #print myRegistry().get_value(win32con.HKEY_LOCAL_MACHINE,r'SAM\SAM\Domains\Account\Users','Names')
    #myRegistry().add_key(_winreg.HKEY_LOCAL_MACHINE,'SOFTWARE\TJTG')
    #print myRegistry().list_keys(_winreg.HKEY_LOCAL_MACHINE,r'SAM\SAM\Domains\Account\Users\Names')
    #myRegistry().add_value(_winreg.HKEY_LOCAL_MACHINE,'SOFTWARE\TJTG','AtionName','TJ7PP')
    #myRegistry().delete_value(_winreg.HKEY_LOCAL_MACHINE,'SOFTWARE\TJTG','AtionName')
    #myRegistry().delete_key(_winreg.HKEY_LOCAL_MACHINE,'SOFTWARE\TJTG')
    #print myRegistry().get_value(_winreg.HKEY_LOCAL_MACHINE,r'SOFTWARE\Tracker Software\pdfxctrl.PdfPrinterPreferences','XCL_PATH')
    """
    #定义构造函数
    def __init__(self):
        #self.obj=wmi.Registry()
        self.obj=wmi.WMI(namespace='DEFAULT').StdRegProv
    #列出注册表项
    def list_keys(self,root,subkey):
        result,names=self.obj.EnumKey(hDefKey=root,sSubKeyName=subkey)
        if result == 2:
            print "No such keys"
        return names
    #返回对应注册表项键值
    def get_value(self,root,subkey,valuename,type="string"):
        if type == "string":
            result,value = self.obj.GetExpandedStringValue(hDefKey=root,sSubKeyName=subkey,sValueName=valuename)
        elif type == "dword":
            result,value = self.obj.GetDWORDValue(hDefKey=root,sSubKeyName=subkey,sValueName=valuename)
        else:
            result,value = self.obj.GetBinaryValue(hDefKey=root,sSubKeyName=subkey,sValueName=valuename)
        return value
    #添加注册表项
    def add_key(self,root,subkey):
        return self.obj.CreateKey(hDefKey=root,sSubKeyName=subkey)
    #old value can be overwritten
    #设置键值
    def set_value(self,root,subkey,valuename,value,type):
            if type == "string":
                    value = self.obj.SetStringValue(hDefKey=root,sSubKeyName=subkey,sValueName=valuename,sValue=value)
            else:
                    value = self.obj.SetDWORDValue(hDefKey=root,sSubKeyName=subkey,sValueName=valuename,uValue=value)
            return value
    #删除注册表项
    def delete_key(self,root,subkey):
        return self.obj.DeleteKey(root,subkey)
    #删除键值
    def delete_value(self,root,subkey,valuename):
        return self.obj.DeleteValue(root,subkey,valuename)
#获取注册表中用户列表
def get_sys_sid():
    pass
    reg_user_list = myRegistry().list_keys(_winreg.HKEY_LOCAL_MACHINE,r'SAM\SAM\Domains\Account\Users')
    sid_admin = u'000001F4'
    reg_user_list.remove(sid_admin)
    length =len(reg_user_list)
    key_list = []
    raw_pattern = re.compile(r'^00000')
    n = 0
    while True:
        for m in reg_user_list:
            if raw_pattern.match(m):
                n += 1
                if n < length:
                    key_list.append(m)
                else:
                    break
        break
    return key_list
#检查克隆账户
def chk_clone_account():
    a = get_sys_sid()
    sid_value = myRegistry().get_value(_winreg.HKEY_LOCAL_MACHINE, r'SAM\SAM\Domains\Account\Users\000001F4', r'F','')
    #print sid_value
    #检查SID值是否为管理员SID值
    for each_value in a:
        path = 'SAM\SAM\Domains\Account\Users\\'+ each_value
        key_value = myRegistry().get_value(_winreg.HKEY_LOCAL_MACHINE,path, r'F','')
        if sid_value == key_value:
            #print 'Clone Account SID is %s' %each_value
            return True
        else:
            continue
    #检查注册表项中是否有隐藏帐号
    reg_user_list=myRegistry().list_keys(_winreg.HKEY_LOCAL_MACHINE,r'SAM\SAM\Domains\Account\Users\Names')
    ulist = myAccount().show_user_list()
    for user in reg_user_list:
        if user not in ulist:
            #print 'Clone Account is %s' %user
            return True
#############################
#                           #
#        Win_Base_setup     #
#                           #
#############################
#定义win_Base类用于系统基本配置
class win_Base():
    #实例化
    def __init__(self):
        #?????ﾩW??????
        self.cf=ConfigParser.ConfigParser()
        self.cf.read(sys.path[0]+'/data/win_reg.ini')
    #根据win_reg.ini中读取到的配置选项,修改对应注册表项及对应键值
    def win_setup(self):
        #???????ﾩW??
        section_start = 0
        section_count = len(self.cf.sections())
        section_item = self.cf.sections()
        for user in section_item:
            while True:
                for user in section_item:
                    #?????ﾩW???ﾩW??????????
                    name = self.cf.get(user,"root")
                    subkey = self.cf.get(user,"sub_key")
                    valuename = self.cf.get(user,"value_name")
                    regtype = self.cf.get(user,"reg_type")
                    #???????ﾡ￪????
                    if name == 'HKEY_LOCAL_MACHINE':
                        a = _winreg.HKEY_LOCAL_MACHINE
                    elif name == 'HKEY_CLASSES_ROOT':
                        a = _winreg.HKEY_CLASSES_ROOT
                    elif name == 'HKEY_CURRENT_USER':
                            a = _winreg.HKEY_CURRENT_USER
                    else:
                        return name
                    #??????????
                    if regtype == "dword":
                        value = int(self.cf.get(user,"value"))
                    else:
                        value = self.cf.get(user,"value")
                    #???????ﾡ￪????
                    myRegistry().add_key(a,subkey)
                    myRegistry().set_value(a,subkey,valuename,value,regtype)
                    section_start += 1
                    if section_start == section_count:
                        break
#############################
#                           #
#   Startup                 #
#                           #
#############################
#定义show_startupcommand类用于系统启动项目检查
def show_startupcommand():
    startup_list=[]
    obj=c.Win32_StartupCommand()
    for s in obj:
        startup_info = {}
        startup_info['Name'] = s.Name
        startup_info['Command'] = s.Command
        #startup_info['Location'] = s.Location
        #startup_info['User'] = s.User
        startup_list.append(startup_info)
        #if s.Command not in startup_list:
        #    start_value = s.Command + ' ' + s.Location
        #    startup_list.append((start_value))
    return startup_list
    '''startup_list=[]
    obj=c.Win32_StartupCommand()
    for s in obj:
        if s.Command not in startup_list:
            start_value = s.Command + ' ' + s.Location
            startup_list.append((start_value))
    return startup_list'''
#############################
#                           #
#   Audit Log               #
#                           #
#############################
def reg(string):
    """
instance of Win32_NTLogEvent
{
    Category = 9;
    CategoryString = "Account Logon";
    ComputerName = "MICROSOF-5524EC";
    EventCode = 680;
    EventIdentifier = 680;
    EventType = 5;
    InsertionStrings = {"MICROSOFT_AUTHENTICATION_PACKAGE_V1_0", "joe", "MICROSOF-5524EC", "0xC000006A"};
    Logfile = "Security";
    Message = "Logon attempt by: MICROSOFT_AUTHENTICATION_PACKAGE_V1_0
\n
\nLogon account:  joe
\n
\nSource Workstation: MICROSOF-5524EC
\n
\nError Code: 0xC000006A
\n
\n";
    RecordNumber = 16267;
    SourceName = "Security";
    TimeGenerated = "20100424000915.000000+480";
    TimeWritten = "20100424000915.000000+480";
    Type = "audit failure";
    User = "NT AUTHORITY\\SYSTEM";
};
instance of Win32_NTLogEvent
{
    Category = 2;
    CategoryString = "Logon/Logoff";
    ComputerName = "MICROSOF-5524EC";
    EventCode = 529;
    EventIdentifier = 529;
    EventType = 5;
    InsertionStrings = {"joe", "MICROSOF-5524EC", "2", "Advapi  ", "Negotiate", "MICROSOF-5524EC"};
    Logfile = "Security";
    Message = "Logon Failure:
\n
\n\tReason:\t\tUnknown user name or bad password
\n
\n\tUser Name:\tjoe
\n
\n\tDomain:\t\tMICROSOF-5524EC
\n
\n\tLogon Type:\t2
\n
\n\tLogon Process:\tAdvapi
\n
\n\tAuthentication Package:\tNegotiate
\n
\n\tWorkstation Name:\tMICROSOF-5524EC
\n";
    RecordNumber = 16251;
    SourceName = "Security";
    TimeGenerated = "20100423091037.000000+480";
    TimeWritten = "20100423091037.000000+480";
    Type = "audit failure";
    User = "NT AUTHORITY\\SYSTEM";
};
    regex=re.compile(r'(User Name|Logon account):\s*\w*')
    r=re.search(regex,string)
    if r:
        return r.group()
    else:
        return 0
class myAuditLog():
    def __init__(self):
        cc=wmi.WMI(privileges=["Security"])
        self.obj=cc.Win32_NTLogEvent()
    #type'll be success or failure.
    def get_history(self,type):
        log_type={'success':4,'failure':5}
        s_log=[]
        for s in self.obj:
            if s.EventType == log_type[type]:
                m=reg(s.Message)
                if m:
                    s_log.append(s.CategoryString+', '+reg(s.Message)+', '+s.TimeWritten+', '+s.Type)
        return s_log"""
#############################
#                           #
#        Share              #
#                           #
#############################
#定义myShare类用于共享检查及设置
class myShare(myWmi):
    def __init__(self,name=""):
        myWmi.__init__(self,c.Win32_Share)
    def show_share(self):
        share_list=[]
        for s in self.obj:
            item_str = s.Name + ' ' +s.Path
            share_list.append(item_str)
            #print s.Name,'\t',s.Path
        return share_list

    def delete(self):
        for s in self.obj:
            s.Delete()
"""def mycmd(cmd):
    try:
        p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        (stdoutput,erroutput)=p.communicate()
    except OSError:
        print "command %s wrong, check the command please!" % cmd
    return (stdoutput,erroutput)"""
def log(log_file,log_string,description):
    try:
        f=open(log_file,'a+')
        #f.write(time.strftime(TIME_FORMAT))
        f.write(description + '\n')
        f.write(str(log_string))
        f.write('\n\n')
        #f.write(time.strftime(TIME_FORMAT)+' '+log_string+'\n')
        f.close()
    except IOError,e:
        print e
        #print "Can't open log file %s." % log_file
        sys.exit()
def log_server(log_file,log_string):
    try:
        f=open(log_file,'a+')
        f.write(str(log_string))
        f.close()
    except IOError,e:
        print e
        #print "Can't open log file %s." % log_file
        sys.exit()
if __name__=='__main__':
    #log_path = sys.path[0]+'/data/win.log'
    log_path = r'c:\win.log'
    #网络配置
    network_config().config_setup()
    network_config().tcp_config()
    #系统服务设置
    myService().change_mode('disabled')
    #基础配置
    win_Base().win_setup()
    #重命名管理员账户
    t = myAccount()
    if 'Administrator' in t.show_userlist_admin():
        t.rename_user('administrator','admin')
    elif 'admin' in t.show_userlist_admin():
        print 'user_admin has been chanaged!'
    else:
        print t.show_userlist_admin()
    print 'Windows base setup has finished!!'
    #帐号列表
    t =  myAccount().show_user_list()
    output=open(log_path,"a+")
    output.write('[Account List]\n')
    for user in t:
        output.write('Windows Account is %s\n' %user)
    output.write('\n')
    #系统服务
    t = myService().get_service_info()
    '''item_count  = len(t)
    n = 0
    log_server(log_path,'[Service List]\n')
    while True:
        for item in t:
            item_value = '<' +str(item['pid'])+ '> <' + item['stat']+ '> <' + item['displayname']+ '>  <' + item['name'] + '> <' + item['startmode']+ '>'+'\n'
            log_server(log_path,item_value)
            n += 1
            if n > item_count:
                break
        break
    log_server(log_path,'\n')'''
    output=open(log_path,"a+")
    output.write('\n')
    output.write('[Server List]\n')
    for item in t:
        output.write('%-35s %-60s %-5s %-8s %-10s \n' %(item['name'],item['displayname'],item['pid'],item['stat'],item['startmode']))
    output.write('\n')
    #系统启动项列表
    t = show_startupcommand()
    output=open(log_path,"a+")
    output.write('\n')
    output.write('[Startup_List]\n')
    for item in t:
#        output.write('%-18s %-20s %-s \n' %(item['Name'],item['Command'],item['Location']))
        output.write('%-20s %-s \n' %(item['Name'],item['Command']))
    output.write('\n')
    '''n = 0
    item_count = len(t)
    log_server(log_path,'[Start up]\n')
    while True:
        for item in t:
            item_value = '<' + item +  '>' + '\n'
            log_server(log_path,item_value)
            n += 1
            if n > item_count:
                break
        break
    log_server(log_path,'\n')'''
    #共享模块
    t = myShare().show_share()
    output=open(log_path,"a+")
    output.write('[Share Information]\n')
    for user in t:
        output.write('Share item is %s\n' %user)
    output.write('\n')
    #系统信息检查
    t = myOs().get_os_info()
    output=open(log_path,"a+")
    output.write('\n')
    output.write('[OS Information]\n')
    for m in t.keys():
        output.write("%-20s: %-s\n" %(m,t[m]))
    output.write('\n')
    '''
    log_server(log_path,'[OS Information]\n')
    item_value = '<' + str(t['fullname'])+ '> <' + str(t['version'])+ '> <'  + str(t['lastboottime']) + '>' + '\n'
    log_server(log_path,item_value)
    log_server(log_path,'\n')'''
    #Windows 更新补丁检查
    myOs().update_information()
    #/*********Windows安全检查***************/
    #克隆帐号检查
    t = chk_clone_account()
    if chk_clone_account():
        Item_value = 'Account has been clone!\n'
        log_server(log_path,'[Clone Account Check]\n')
        log_server(log_path,Item_value)
        log_server(log_path,'\n')
    else:
        Item_value = 'Account has not clone!\n'
        log_server(log_path,'[Clone Account Check]\n')
        log_server(log_path,Item_value)
        log_server(log_path,'\n')
    #系统服务设置
    output=open(log_path,"a+")
    toclose=[]
    blacklist_path = sys.path[0]+'/data/svr_blacklist.txt'
    f=open(blacklist_path)
    svr_blacklist = f.readlines()
    f.close()
    s=myService()
    svr_stat=s.get_service_info()
    #print svr_blacklist
    #print svr_stat
    for b in svr_blacklist:
      b=b.strip()
      for svr in svr_stat:
        if svr["name"] == b and svr["startmode"] != "Disabled":
          toclose.append(b)
    #output.write('*'*50+'\r\n')
    output.write('[Service check]\r\n')
    #output.write('*'*50+'\r\n')
    for s in toclose:
      output.write("%s should be disabled\r\n" % s)
    #磁盘信息
    myOs().get_diskinfo()
    #磁盘分区信息
    myOs().get_partitioninfo()
    #网卡信息
    myOs().get_networkadapter()
    #系统进程列表
    t = myProcess().get_process_info()
    output=open(log_path,"a+")
    output.write('\n')
    output.write('[System processlist]\r\n')
    for x in t:
        if x[2] != None:
            output.write('%-22s %-5s %-20s %-s\n' %(x[1],x[0],datetime.datetime.strptime(str(str(x[2]).split('.')[0]),'%Y%m%d%H%M%S'),x[3]))
    output.write('\n')
    #系统服务设置
    #toclose=[]
    blacklist_path = sys.path[0]+'/data/svr_blacklist.txt'
    f=open(blacklist_path)
    svr_blacklist = f.readlines()
    f.close()
    for b in svr_blacklist:
        b = b.strip()
        myService().change_mode(b,'Disabled')
    print 'Windows check has finished!!'
    sys.exit