# -*- coding: utf-8 -*-
## {{{ http://code.activestate.com/recipes/474070/ (r1)
import time,datetime
a = "2011-10-18 15:39"
print time.strptime(a,"%Y-%m-%d %H:%M")
b = time.mktime(time.strptime(a,"%Y-%m-%d %H:%M"))
print b