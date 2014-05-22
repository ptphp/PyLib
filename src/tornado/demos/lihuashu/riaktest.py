#!user/bin/env python
# -*- coding: utf8 -*-
from config.settings import globalSetting
import os

def search(bucketStr = None):
    cmdStr = "/data/soft/riak-1.1.4/dev/dev1/bin/search-cmd install "
    bucketList = [
                  'pin',
                  'board',
                  'category',
                  'comment',
                  'pinLike',
                  'boardFollow',
                  'userFollow',
                  ]
    if bucketStr:
        bucket = "%sBucket" % bucketStr
        cmdStr = cmdStr +globalSetting[bucket]
        os.system(cmdStr)
        print cmdStr                
    else:        
        for _bucketStr in bucketList:
            bucket = "%sBucket" % _bucketStr
            _cmdStr = cmdStr +globalSetting[bucket]
            os.system(_cmdStr)
    

if __name__  == "__main__":
    #catTest()
    #boardTest()
    #pins()
    search()
    pass
