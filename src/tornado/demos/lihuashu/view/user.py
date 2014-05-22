#!user/bin/env python
# -*- coding: utf8 -*- 
import tornado.web,time,hashlib
from .frontend import BaseHandler
import simplejson as json
from config.settings import globalSetting
from common.function import dump
from common.function import urldecode
from models.board import Board
from models.user import User
from models.userinfo import UserInfo
from models.pin import Pin
from models.avatar import Avatar
from models.userFollow import UserFollow

from config.settings import settings
class InvitesHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        i_url = "%ssignup/?i=" % settings['site_host']
        self.render('invitation.html',i_url = i_url,user=self.currentUserInfo())


class FollowuserHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self,key):
        res = {}         
        user_key = self.get_secure_cookie("user_key")
        if user_key == key:
            res['code'] = 1
            res['msg'] = "您不能关注自己"
            res_str = json.dumps(res)
            return self.write(res_str)
        
        b_key = "%s%s" % (user_key,key)
        
        userFollow = UserFollow()
        
        if userFollow.get(b_key):
            res['code'] = 1
            res['msg'] = "您已关注过了"
        else:
            #oard = Board()
            #board.key = key
            #board.data =  board.get(key)
            #board.data['follow'] = int(board.data['follow']) + 1
            #board.put()            
            #userFollow.key = b_key
            
            userFollow.data['user'] = user_key
            userFollow.data['follow'] = key
            userFollow.data['createTime'] = int(time.time())
            userFollow.post()
            res['code'] = 0
            res['msg'] = "成功"
            print res                
        res_str = json.dumps(res)
        self.write(res_str)
        
        
class RemoveFollowuserHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self,key):        
        res = {} 
        res['code'] = 0
        res['msg'] = "成功"
        userFollow = UserFollow()
        user_key = self.get_secure_cookie("user_key")
        f_key = "%s%s" % (user_key,key)        
        userFollow.delete(f_key)
        res_str = json.dumps(res)
        self.write(res_str)


class MemberHandler(BaseHandler):
    def get(self,key):
        uri = self.request.uri
        request = {}
        board = Board()
        
        pin_keys = board.allKey()
        pin_count = len(pin_keys)
        
        query = {}
        query['q']         = "user:%s" % key
                
        query['start']  = "0"
        query['rows']   = globalSetting['max_index_board_rows']
        query['sort']   = "follow"
        
        if "page" in uri:
            request = urldecode(uri)
            page = int(request['page'])
            query['start']  = query['rows']*page
            #if pin_count < query['rows']*page:
            #    return ''
        
        board_data = board.solr(query)
        print len(board_data)
                
        boards_dict = board.formatBoards(board_data)

        if request:
            #print request['callback']
            #print request['page']            
            callback_result = {
                            'filter':'board:index',
                            'boards':boards_dict
                            }
            
            callback_response = "%s(%s)" % (request['callback'],json.dumps(callback_result))
            self.set_header("Content-Type", "text/html; charset=utf-8")            
            return self.write(callback_response)
        else:            
            user = User()
            boards = ''
            for _board_t in boards_dict:
                boards = self.render_string('board_unit.html',board=_board_t) + boards
                
            u_user = user.getInfo(key)
            
            userFollow = UserFollow()
            counts = {}
            counts['follow'] = len(userFollow.getByKeyValues("user", key))
            
            counts['fans'] = len(userFollow.getByKeyValues("follow", key)) 
 
            self.render('user_board.html',counts=counts,u_user=u_user,user=self.currentUserInfo(),boards=boards)    


class MemberLikesHandler(BaseHandler):
    def get(self,key):
        uri = self.request.uri
        request = {}
        
        from models.pinLike import PinLike
        pinLike = PinLike()
        query = {}
        query['q']         = "user:%s" % key    
        query['start']  = "0"
        query['rows']   = globalSetting['max_index_pin_rows']
        query['sort']   = "createTime"
        
        pin_keys = pinLike.getByKeyValues("user",key)        
        pin_count = len(pin_keys)        
        
        if "page" in uri:
            request = urldecode(uri)
            page = int(request['page'])
            query['start']  = query['rows']*page
            if pin_count < query['rows']*page:
                return ''
        
        pin_data = pinLike.solr(query)
        marks_dict = pinLike.formatPins(pin_data)    
        
        if request:
            #print request
            callback_result = {
                            'filter':'pin:index',
                            'pins':marks_dict
                            }
            
            callback_response = "%s(%s)" % (request['callback'],json.dumps(callback_result))
            self.set_header("Content-Type", "text/html; charset=utf-8")            
            return self.write(callback_response)
        else:
            board = Board()
            user = User()
            marks = ''
            for _mark_t in marks_dict:
                marks = self.render_string('mark.html',mark=_mark_t)+marks
            u_user = user.getInfo(key)
            userFollow = UserFollow()
            counts = {}
            counts['follow'] = len(userFollow.getByKeyValues("user", key))
            
            counts['fans'] = len(userFollow.getByKeyValues("follow", key)) 
            self.render('user_likes.html',counts= counts,u_user=u_user,user=self.currentUserInfo(),board = board.get(key),marks=marks)
            
class MemberPinsHandler(BaseHandler):
    def get(self,key):
        uri = self.request.uri
        request = {}
        pin = Pin()
        
        pin_keys = pin.getByKeyValues("user",key)
        pin_count = len(pin_keys)
        
        query = {}
        query['q']         = "user:%s" % key    
                
        query['start']  = "0"
        query['rows']   = globalSetting['max_index_pin_rows']
        query['sort']   = "createTime"
        
        if "page" in uri:
            request = urldecode(uri)
            page = int(request['page'])
            query['start']  = query['rows']*page
            if pin_count < query['rows']*page:
                return ''
        
        pin_data = pin.solr(query)
        marks_dict = pin.formatPins(pin_data)    
        
        if request:
            #print request
            callback_result = {
                            'filter':'pin:index',
                            'pins':marks_dict
                            }
            
            callback_response = "%s(%s)" % (request['callback'],json.dumps(callback_result))
            self.set_header("Content-Type", "text/html; charset=utf-8")            
            return self.write(callback_response)
        else:
            board = Board()
            user = User()
            marks = ''
            for _mark_t in marks_dict:
                marks = self.render_string('mark.html',mark=_mark_t)+marks
            u_user = user.getInfo(key)
            
            userFollow = UserFollow()
            counts = {}
            counts['follow'] = len(userFollow.getByKeyValues("user", key))
            
            counts['fans'] = len(userFollow.getByKeyValues("follow", key)) 
            self.render('user_pins.html',counts=counts,u_user=u_user,user=self.currentUserInfo(),board = board.get(key),marks=marks)

class LoginHandler(BaseHandler):
    def get(self):
        errMsg = None
        self.render('login.html',user=self.currentUserInfo(),errMsg=errMsg)
        
    def post(self):    
        email     = self.get_argument("email",None)
        password  = self.get_argument("password",None)        
        import hashlib
        errMsg = None
        if email is None:
            errMsg = "Email不能为空"
            return self.render('login.html',user=self.currentUserInfo(),errMsg=errMsg)
        if password is None:
            errMsg = "Email不能为空"
            return self.render('login.html',user=self.currentUserInfo(),errMsg=errMsg)
        
        user_key = hashlib.md5(email).hexdigest()
        user = User()
        user_data = user.getDetail(user_key)
        
        if user_data is None:            
            errMsg = "用户不存在"
        else:
            if hashlib.md5(password).hexdigest() != user_data['password']:
                errMsg = "用户名或密码不正确"      
            else:
                urlname = user_data['nickname']                
                self.set_secure_cookie('user_email',user_data['email'])
                self.set_secure_cookie('user_nickname',urlname)
                self.set_secure_cookie('user_urlname',urlname)
                self.set_secure_cookie('user_key',user_key)
                self.set_secure_cookie('user_avatar',user_data['avatar'])
                #print "login succ!"
                return self.redirect('/')
                
        self.render('login.html',user=self.currentUserInfo(),errMsg=errMsg)
        
class RegisterHandler(BaseHandler):
    def get(self):
        
        errMsg = {}
        errMsg['email'] = None
        errMsg['password'] = None
        errMsg['repassword'] = None
        errMsg['nickname'] = None
        
        self.render('register.html',user=self.currentUserInfo(),errMsg=errMsg)

    def post(self):
        
        errMsg = {}
        errMsg['email'] = None
        errMsg['password'] = None
        errMsg['repassword'] = None
        errMsg['nickname'] = None
        
        email    = self.get_argument("email",None)
        p1       = self.get_argument("password",None)
        p2       = self.get_argument("repassword",None)
        nickname = self.get_argument("nickname",None)        
        
        if email is None:
            errMsg['email'] = "Email不能为空"
            return self.render('register.html',user=self.currentUserInfo(),errMsg=errMsg)
        
        if p1 is None:
            errMsg['password'] = "密码不能为空"
            return self.render('register.html',user=self.currentUserInfo(),errMsg=errMsg)
        
        if p2 is None:
            errMsg['repassword'] = "请确认密码"
            return self.render('register.html',user=self.currentUserInfo(),errMsg=errMsg)
        
        if p1 != p2:
            errMsg['password'] = "您输入的两次密码不一致"
            return self.render('register.html',user=self.currentUserInfo(),errMsg=errMsg)
        
        if nickname is None:
            errMsg['nickname'] = "呢称不能为空"
            return self.render('register.html',user=self.currentUserInfo(),errMsg=errMsg)
        
        user = User()
        
        key = hashlib.md5(email).hexdigest()
        user_data = user.get(key)
        
        if user_data is not None:
            errMsg['email'] = "用户已存在"
            return self.render('register.html',user=self.currentUserInfo(),errMsg=errMsg)
        else:
            user.key                = key
            user.data['email']      = email
            user.data['password']   = hashlib.md5(p1).hexdigest()
            user.data['nickname']   = nickname
            user.data['createTime'] = time.time()            
            user.post()
            
            return self.redirect('/login/')
        return self.render('register.html',user=self.currentUserInfo(),errMsg=errMsg)
            
class SettingsHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        
        user_key = self.get_secure_cookie("user_key")
        user = User()
        user_data = user.getDetails(user_key)
        #print user_data        
        user_data['user_key'] = user_key
        self.render('settings.html',user = user_data)
        
    @tornado.web.authenticated
    def post(self):            
        user_key =self.get_secure_cookie("user_key")
        r = None
        
        user_data = {}
        info_data = {}
        
        
        userInfo = UserInfo()
        user = User()
        user.key = user_key
        user.data = user.get(user_key)
        user.data['nickname'] = self.get_argument("user_nickname",None)
        
        userInfo.key = user_key
        
        userInfo_data = userInfo.get(user_key)
        if userInfo_data:
            userInfo.data = userInfo_data
            
        userInfo.data['city']        = self.get_argument("user_city","")
        userInfo.data['url']         = self.get_argument("user_url","")
        userInfo.data['desc']        = self.get_argument("user_description","")
        
        userInfo.post()
        user.post()        
        
        self.redirect('/settings/')
    
class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_all_cookies()
        self.redirect('/')

    
class AdminDeleteUserHandler(BaseHandler):
    def get(self,key):
        user      = User()
        userInfo = UserInfo()
        avatar =Avatar()
        user.delete(key)
        userInfo.delete(key)
        avatar.delete(key)
        
        
class AdminUserHandler(BaseHandler):    
    def get(self):
        user      = User()
        userInfo = UserInfo()
        
        keys = user.allKey()   
        _data = []
        for row in user.all(keys):
            _data.append(user.getDetails(row['key']))
        #self.dumpJson(_data)
        self.render('manager/user.html',data=_data)

