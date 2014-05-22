#coding:utf-8
'''

1、想写一个监视服务器是否运行的简单服务，网上搜到的例程不太完善，如梅劲松的许�?
没有更新，�?且SvcDoRun写得不完整（见http://www.chinaunix.net/jh/55/558190.html�?
不知道是不是原始出处）；而mail.python.org中的没有定义_svc_name_等变量（�?
http://mail.python.org/pipermail/python-list/2005-December/315190.html�?
2、这个实现功能很�?��，就是把当前时间写入‘c:\\temp\\time.txt’文件，�?��即知�?
大家可以随意扩充�?
3、用
service install 安装
service start   启动
service stop    停止
service debug   调试
service remove  删除

service.py
---代码�?��
'''

import win32serviceutil
import win32service
import win32event
import win32evtlogutil
import time

class service(win32serviceutil.ServiceFramework):
        _svc_name_ = "test_python"
        _svc_display_name_ = "test_python"
        def __init__(self, args):
                win32serviceutil.ServiceFramework.__init__(self, args)
                self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
                print 'service starts'
        def SvcDoRun(self):
                import servicemanager
                #------------------------------------------------------
                # Make entry in the event log that this service started
                #------------------------------------------------------
                servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE, servicemanager.PYS_SERVICE_STARTED, (self._svc_name_, ''))
                #-------------------------------------------------------------
                # Set an amount of time to wait (in milliseconds) between runs
                #-------------------------------------------------------------
                self.timeout = 100
                while 1:
                        #-------------------------------------------------------
                        # Wait for service stop signal, if I timeout, loop again
                        #-------------------------------------------------------
                        rc = win32event.WaitForSingleObject(self.hWaitStop, self.timeout)
                        #
                        # Check to see if self.hWaitStop happened
                        #
                        if rc == win32event.WAIT_OBJECT_0:
                                #
                                # Stop signal encountered
                                #
                                break
                        else:
                                #
                                # Put your code here
                                #
                                #
                                f = open('c:\\temp\\time.txt', 'w', 0)
                                f.write(time.ctime(time.time()))
                                f.close()
                                print 'service in running'
                                time.sleep(1)
                        #
                        # Only return from SvcDoRun when you wish to stop
                        #
                return

        def SvcStop(self):
#---------------------------------------------------------------------
                # Before we do anything, tell SCM we are starting the stop process.
#---------------------------------------------------------------------
                self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
#---------------------------------------------------------------------
                # And set my event
#---------------------------------------------------------------------
                win32event.SetEvent(self.hWaitStop)
                print 'service ends'
                return
if __name__ == '__main__':
        win32serviceutil.HandleCommandLine(service)
#---代码结束
