
sudo sed -e '/^ {riak_kv/ a {delete_mode, immediate},' \
         -e 's/storage_backend, riak_kv_bitcask_backend/storage_backend, riak_kv_eleveldb_backend/' \
         -e '/^ {riak_search/,+2 s/enabled, false/enabled, true/' -i.bak /data/soft/riak-1.1.4/dev/dev1/etc/app.config
         
sudo sed -e '/^ {riak_kv/ a {delete_mode, immediate},' \
         -e 's/storage_backend, riak_kv_bitcask_backend/storage_backend, riak_kv_eleveldb_backend/' \
         -e '/^ {riak_search/,+2 s/enabled, false/enabled, true/' -i.bak /data/soft/riak-1.1.4/dev/dev2/etc/app.config

sudo sed -e '/^ {riak_kv/ a {delete_mode, immediate},' \
         -e 's/storage_backend, riak_kv_bitcask_backend/storage_backend, riak_kv_eleveldb_backend/' \
         -e '/^ {riak_search/,+2 s/enabled, false/enabled, true/' -i.bak /data/soft/riak-1.1.4/dev/dev3/etc/app.config
         
sudo sed -e '/^ {riak_kv/ a {delete_mode, immediate},' \
         -e 's/storage_backend, riak_kv_bitcask_backend/storage_backend, riak_kv_eleveldb_backend/' \
         -e '/^ {riak_search/,+2 s/enabled, false/enabled, true/' -i.bak /data/soft/riak-1.1.4/dev/dev4/etc/app.config



/data/soft/riak-1.1.4/dev/dev1/bin/riak start
/data/soft/riak-1.1.4/dev/dev2/bin/riak start
/data/soft/riak-1.1.4/dev/dev3/bin/riak start
/data/soft/riak-1.1.4/dev/dev4/bin/riak start


/data/soft/riak-1.1.4/dev/dev1/bin/riak restart
/data/soft/riak-1.1.4/dev/dev2/bin/riak restart
/data/soft/riak-1.1.4/dev/dev3/bin/riak restart
/data/soft/riak-1.1.4/dev/dev4/bin/riak restart

/data/soft/riak-1.1.4/dev/dev2/bin/riak-admin join dev1@127.0.0.1
/data/soft/riak-1.1.4/dev/dev3/bin/riak-admin join dev1@127.0.0.1
/data/soft/riak-1.1.4/dev/dev4/bin/riak-admin join dev1@127.0.0.1


mkdir /home/yuqing
mkdir /home/yuqing/fastdht
mkdir /home/yuqing/fastdfs

FastDFS
sudo yum install libevent libevent-devel

sed -i "s/#WITH_HTTPD=1/WITH_HTTPD=1/g" /data/soft/src/FastDFS/make.sh

sudo sed -i "s/192.168.0.197/192.168.8.157/g" /etc/fdfs/client.conf
sudo sed -i "s/##include http.conf/#include http.conf/g" /etc/fdfs/client.conf
sudo sed -i "s/##include http.conf/#include http.conf/g" /etc/fdfs/tracker.conf
sudo sed -i "s/192.168.209.121/192.168.8.157/g" /etc/fdfs/storage.conf
sudo sed -i "s/##include http.conf/#include http.conf/g" /etc/fdfs/storage.conf

/usr/local/bin/fdfs_trackerd /etc/fdfs/tracker.conf
/usr/local/bin/fdfs_storaged /etc/fdfs/storage.conf

FastDHT

sudo sed -i "s/192.168.0.196:11411/192.168.8.157:11411/g" /etc/fdht/fdht_servers.conf
sudo sed -i "s/192.168.0.116:11411/192.168.8.157:11412/g" /etc/fdht/fdht_servers.conf

/usr/local/bin/fdhtd /etc/fdht/fdhtd.conf

yum install zlib pcre pcre-devel openssl

groupadd www
useradd -s /sbin/nologin -g www www
mkdir -p /home/sites
chmod +w /home/sites
mkdir -p /home/sites/logs
chmod 755 /home/sites/logs
chown -R www:www /home/sites



./configure \
    --user=www\
    --group=www\
    --prefix=/usr/local/nginx\
    --sbin-path=/usr/local/nginx/sbin/nginx\
    --conf-path=/usr/local/nginx/conf/nginx.conf\
    --with-http_stub_status_module\
    --with-http_ssl_module\
    --with-pcre\
    --add-module=/data/soft/src/nginx_module/nginx-upload-progress-module\
    --add-module=/data/soft/src/nginx_module/nginx_upload_module\
    --add-module=/data/soft/src/nginx_module/fastdfs-nginx-module/src


vim /etc/init.d/nginx

加入以下内容
#!/bin/bash
#
# chkconfig: - 85 15
# description: Nginx is a World Wide Web server.
# processname: nginx

nginx=/usr/local/nginx/sbin/nginx
conf=/usr/local/nginx/conf/nginx.conf

case $1 in
       start)
              echo -n "Starting Nginx"
              $nginx -c $conf
              echo " done"
       ;;

       stop)
              echo -n "Stopping Nginx"
              killall -9 nginx
              echo " done"
       ;;

       test)
              $nginx -t -c $conf
       ;;

reload)
              echo -n "Reloading Nginx"
              ps auxww | grep nginx | grep master | awk '{print $2}' | xargs kill -HUP
              echo " done"
       ;;

restart)
$0 stop
$0 start
       ;;

       show)
              ps -aux|grep nginx
       ;;

       *)
              echo -n "Usage: $0 {start|restart|reload|stop|test|show}"
       ;;
esac


chmod +x /etc/init.d/nginx

chkconfig --add nginx
chkconfig nginx on

service nginx start
service nginx test

mv /usr/local/nginx/conf/nginx.conf /usr/local/nginx/conf/nginx.conf_bak
vim /usr/local/nginx/conf/nginx.conf


issue
-------------------------
/usr/lib/python2.7/site-packages/fdfs_client-1.2.1-py2.7.egg/fdfs_client/client.py
for tr in [tracker_list]:


/usr/lib/python2.7/site-packages/fdfs_client-1.2.1-py2.7.egg/fdfs_client/storage_client.py
send_buffer = struct.pack(non_slave_fmt, store_serv.store_path_index, \
                                                    file_size, file_ext_name.encode('utf-8'))



sed -i "s/192.168.8.214/192.168.19.133/g" /etc/fdht/fdht_servers.conf
sed -i "s/192.168.8.214/192.168.19.133/g" /etc/fdfs/storage.conf
sed -i "s/192.168.8.214/192.168.19.133/g" /etc/fdfs/client.conf


sed -i "s/192.168.1.100/192.168.8.157/g" /etc/fdht/fdht_servers.conf
sed -i "s/192.168.1.100/192.168.8.157/g" /etc/fdfs/storage.conf
sed -i "s/192.168.1.100/192.168.8.157/g" /etc/fdfs/client.conf


sed -i "s/192.168.19.133/192.168.19.138/g" /etc/fdht/fdht_servers.conf
sed -i "s/192.168.19.133/192.168.19.138/g" /etc/fdfs/storage.conf
sed -i "s/192.168.19.133/192.168.19.138/g" /etc/fdfs/client.conf





user

{
  'id':'',
  'userid':'',
  'username':'',
  'email': '',
  'urlname':'',
  'password' :'',
  'createdat': '',
  'avatarid': '',
  'logins': '',
  'last_login':'', 
}

board
{
'userid':'',
'title':'',
'description':'',
'categoryid':'',
'seq':'',
'pincount':'',
'followcount':'',
'createdat':'',
'updatedat':'',
'isprivate':'',
}

category

{
'name':'',
'urlname':'',
'title':'',
'description':'',
'group':'',
'order':'',
}

comment
{
'pinid':'',
'userid':'',
'textmeta':'',
'rawtext':'',
'createdat':'',
}

pin
{
'userid':'',
'boardid':'',
'mediatype':'',
'link':'',
'rawtext':'',
'textmeta':'',
'via':'',
'viauserid':'',
'original':'',
'createdat':'',
'likecount':'',
'commentcount':'',
'repincount':'',
'isprivate':'',
'origsource':'',
}


