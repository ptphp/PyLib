#!/usr/bin/env python
# -*- coding=utf-8 -*-
'''
Created on 2013-3-31
@author: Joseph
'''
import threading
import time

class Test(threading.Thread):
    def __init__(self, num):
        threading.Thread.__init__(self)
        self._run_num = num
    
    def run(self):
        global count, mutex
        threadname = threading.currentThread().getName()    
        for x in xrange(0, int(self._run_num)):
            mutex.acquire()
            count = count + 1
            mutex.release()
            print threadname, x, count
            print "\n";
            time.sleep(1)

if __name__ == '__main__':
    global count, mutex
    threads = []
    num = 10
    count = 1
    # 创建锁
    mutex = threading.Lock()
    # 创建线程对象
    for x in xrange(0, num):
        threads.append(Test(10))
    # 启动线程
    for t in threads:
        t.start()
    # 等待子线程结束
    for t in threads:
        t.join()  