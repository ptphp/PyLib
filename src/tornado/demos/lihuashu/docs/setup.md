/data/soft/riak-1.1.4/dev/dev1/bin/riak start
/data/soft/riak-1.1.4/dev/dev2/bin/riak start
/data/soft/riak-1.1.4/dev/dev3/bin/riak start
/data/soft/riak-1.1.4/dev/dev4/bin/riak start

/usr/local/bin/fdfs_trackerd /etc/fdfs/tracker.conf
/usr/local/bin/fdfs_storaged /etc/fdfs/storage.conf
/usr/local/bin/fdhtd /etc/fdht/fdhtd.conf

/data/soft/src/riak-1.1.4/dev/dev1/bin/riak restart
/data/soft/src/riak-1.1.4/dev/dev2/bin/riak restart
/data/soft/src/riak-1.1.4/dev/dev3/bin/riak restart
/data/soft/src/riak-1.1.4/dev/dev4/bin/riak restart

/data/soft/src/riak-1.1.4/dev/dev1/bin/riak stop
/data/soft/src/riak-1.1.4/dev/dev2/bin/riak stop
/data/soft/src/riak-1.1.4/dev/dev3/bin/riak stop
/data/soft/src/riak-1.1.4/dev/dev4/bin/riak stop


curl http://192.168.19.138:8091/riak/boardtest11
curl http://192.168.19.138:8091/riak/pintest11111




