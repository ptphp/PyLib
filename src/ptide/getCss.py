'''
Created on Jan 28, 2013

@author: joseph
'''


import os 


lists = os.listdir('D:\Dhole\PtProject\Core\Application\inspector')
for l in lists:
    if ".css" in l:
        print '<link rel="stylesheet" type="text/css" href="%s">' % l