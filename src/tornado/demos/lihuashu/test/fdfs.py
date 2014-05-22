#!user/bin/env python
# -*- coding: utf8 -*- 
'''
Created on Jul 11, 2012

@author: joseph
'''
from fdfs_client.client import *

if __name__ == '__main__':
    img_path = "/tmp/upload_temp_dir/00d29d5d146d414f9d577f59c208eaab13dbf349.jpg"
    client = Fdfs_client('/etc/fdfs/client.conf')
    ret = client.upload_by_filename(img_path)
    print ret