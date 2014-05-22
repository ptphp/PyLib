#!user/bin/env python
# -*- coding: utf8 -*-
import os

os.system("/data/soft/riak-1.1.4/dev/dev1/bin/riak start")
os.system("/data/soft/riak-1.1.4/dev/dev2/bin/riak start")
os.system("/data/soft/riak-1.1.4/dev/dev3/bin/riak start")
os.system("/data/soft/riak-1.1.4/dev/dev4/bin/riak start")

os.system("/usr/local/bin/fdfs_trackerd /etc/fdfs/tracker.conf")
os.system("/usr/local/bin/fdfs_storaged /etc/fdfs/storage.conf")
os.system("/usr/local/bin/fdhtd /etc/fdht/fdhtd.conf")
