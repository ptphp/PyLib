#!user/bin/env python
# -*- coding: utf8 -*- 
import tornado.web
import os
from .frontend import BaseHandler
from common.img import Img
from fdfs_client.client import Fdfs_client #@UnresolvedImport

from config.settings import globalSetting
from models.pic import Pic
from models.thumb import Thumb
from models.pin import Pin
from models.board import Board
from common.function import urldecode,dump

class UploadHandler(BaseHandler):
        @tornado.web.authenticated
        def get(self):
            self.render('service.html')
        @tornado.web.authenticated
        def post(self):
            uri = self.request.uri
            
            avatar_sha1=self.get_argument("f_file.sha1",None)
            
            if avatar_sha1:
                user_key = self.get_secure_cookie("user_key")
                res = {}                
                
                upload_file_name=self.get_argument("f_file.name",None)
                ext = upload_file_name.split('.')[1]            
                img_path_t=os.path.join("/tmp/upload_temp_dir/",str(avatar_sha1))            
            
                img_path = "%s.%s" % (img_path_t,ext)
                
                upload_file_path=self.get_argument("f_file.path",None)
                
                os .rename(upload_file_path,img_path)
                
                
                client = Fdfs_client(globalSetting['fdfs_client_conf'])            
                ret = client.upload_by_filename(img_path)
                
                remote_file_id = ret['Remote file_id']
                storage_ip = ret['Storage IP']
                pic_url = "http://%s:%d/%s" % (storage_ip,globalSetting['fdfsPort'],remote_file_id)
                print pic_url
                from models.avatar import Avatar
                avatar = Avatar()
                avatar.key = user_key
                avatar.data['url'] = pic_url
                avatar.post()
                
                res['avatar'] = pic_url
                res['error'] = ''
                
                return self.dumpJson(res)
        
            upload_file_sha1=self.get_argument("ifile.sha1",None)
            #upload_file_size=self.get_argument("ifile.size",None)
            upload_file_path=self.get_argument("ifile.path",None)
            upload_file_name=self.get_argument("ifile.name",None)
            print upload_file_name
            ext = upload_file_name.split('.')[1]            
            
            img_path_t=os.path.join("/tmp/upload_temp_dir/",str(upload_file_sha1))            
            
            img_path = "%s.%s" % (img_path_t,ext)
            img_path_170x170 = "%s_170x170.%s" % (img_path_t,ext)
            
            try:
                i=Img()
                i.open('/usr/bin')
                i.convert_resize(input_file=upload_file_path,output_file=img_path,output_size="500x")                
                i.convert_thumbnail(input_file=img_path,output_file=img_path_170x170,output_size="170x170")                
            except Exception as what:
                #data=file(upload_file_path,'rb').close()                
                print what
                pass                       
            
            client = Fdfs_client(globalSetting['fdfs_client_conf'])            
            ret = client.upload_by_filename(img_path)

            remote_file_id = ret['Remote file_id']
            storage_ip = ret['Storage IP']
            pic_url = "http://%s:%d/%s" % (storage_ip,globalSetting['fdfsPort'],remote_file_id)
            
            ret = client.upload_by_filename(img_path_170x170)            
            remote_file_id = ret['Remote file_id']
            storage_ip = ret['Storage IP']
            thumb_url = "http://%s:%d/%s" % (storage_ip,globalSetting['fdfsPort'],remote_file_id)
            
            user_key = self.get_secure_cookie("user_key")
            
            board  = Board()
            query = {}
            query['q'] = "user:%s" % user_key            
            _data = board.solr(query)     
            
            self.render('upload_form.html',boards = _data,pic_url=pic_url,thumb_url=thumb_url)

class FormHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        import time        
        board_key    = self.get_argument("board",None)
        pic_url      = self.get_argument("pic_url",None)
        thumb_url    = self.get_argument("thumb_url",None)
        content      = self.get_argument("content",None)        
        
        pin       = Pin()
        thumb     = Thumb()
        pic       = Pic()
        board     = Board()
        
        board.data  =board.get(board_key)
        
        user_key = self.get_secure_cookie('user_key')
        
        _tmp = "%s%s" % (content,user_key)
        pin_key = pin.genKey(_tmp)
        
        if pin_key not in board.data['pins']:
            board.data['pins'].append(pin_key)
        board.key      = board.data['key']
        
        pin.key = pin_key
        
        pin.data['rawtext'] = content
        pin.data['user']    = user_key
        pin.data['board']   = board_key
        pin.data['category']   = board.data['category']
        pin.data['createTime'] = int(time.time())
        
        pic.key = pin_key
        pic.data['url'] = pic_url
        
        thumb.key = pin_key
        thumb.data['url'] = thumb_url
        
        try:
            board.put()
            pin.post()
            pic.post()
            thumb.post()
                      
        except Exception as what:
            print what
            self.write(what)
        else:
            self.redirect('/mark/%s/' % pin_key)   
        
        