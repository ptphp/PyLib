#!user/bin/env python
# -*- coding: utf8 -*- 
'''
Created on Jul 11, 2012

@author: joseph
'''
import os
import subprocess

if __name__ == '__main__':
    output_size = '100x100'
    img_bin = "/usr/bin/convert"
    input_file = "/tmp/upload_temp_dir/0000000029"
    output_file = "/home/joseph/Pictures/test.jpg"
    s=os.system([img_bin,'-thumbnail',output_size,'-background','white','-gravity','center','-extent',output_size,input_file,output_file], stdout=subprocess.PIPE)
    sr=s.stdout.read()