#coding=UTF-8
'''
Created on 2011-7-2

@author: Administrator
'''
try:
    import cookielib
    import mechanize
    import simplejson as sj
    import random
    import time
    import urllib
    import os
    from pyquery.pyquery import PyQuery
    import re
    import mimetypes
except Exception,e:
    raise  "puterror1|%s"%e
    
class SouFangbrowser():
    def __init__(self,pdb):
        self.br = mechanize.Browser()
        self.cj = cookielib.MozillaCookieJar()#LWPCookieJar()
        self.br.set_cookiejar(self.cj)
        self.br.set_handle_equiv(True)
        #self.br.set_handle_gzip(True)
        self.br.set_handle_redirect(True)
        self.br.set_handle_referer(True)
        self.br.set_handle_robots(False)
        self.br._factory.encoding = "GB18030"
        self.br._factory._forms_factory.encoding = "GB18030"
        self.br._factory._links_factory._encoding = "GB18030"
        self.br.addheaders = [
                              ('User-agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.2.13) Gecko/20101203 Firefox/3.6.13 (.NET CLR 3.5.21022)'),
                              ]
        
        self.xqs=[]
        self.deaufltimages=[]
        self.customimages=[]
        self.subdict={}
        self.countid=0
        
        
        
        self.pdb=pdb
        self.uname=self.pdb["username"]#"changna19880422"
        self.upwd=self.pdb["passwd"]#"19880422"
        self.area=self.pdb["citycode"]
        self.picRoot =""#"/home/wwwroot/jjr360v1.1/site.jjr.com/upfile/"
        self.house_drawing=[]
        self.house_thumb=[]
        self.house_xqpic=[]
        
        #self.ucityname=urllib.quote(self.cityname.decode("UTF-8").encode("GB18030"))
        
    def getUqGlCode(self):
        a=[]
        b="%X"%random.randint(000000000,999999999)
        while len(b)<8:
            b = "0" + b
        a.append(b)
        a.append("%s%s"%(int(time.time()),random.randint(000,999)))
        c="%X"%random.randint(000000000,999999999)
        while len(c)<8:
            c = "0" + c
        a.append(c)
        
        gc="-".join(a)
        
        
        global_cookie=cookielib.Cookie(version=0, name='global_cookie', value=gc, port=None, port_specified=False, domain='.soufun.com', domain_specified=False, domain_initial_dot=True, path='/', path_specified=True, secure=False, expires=None, discard=True, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False)
        self.br._ua_handlers['_cookies'].cookiejar.set_cookie(global_cookie)
        uc="U_%s"%gc
        unique_cookie=cookielib.Cookie(version=0, name='unique_cookie', value=uc, port=None, port_specified=False, domain='.soufun.com', domain_specified=False, domain_initial_dot=True, path='/', path_specified=True, secure=False, expires=None, discard=True, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False)
        self.br._ua_handlers['_cookies'].cookiejar.set_cookie(unique_cookie)
        jiatxShopWindow=cookielib.Cookie(version=0, name='jiatxShopWindow', value="1", port=None, port_specified=False, domain='.soufun.com', domain_specified=False, domain_initial_dot=True, path='/', path_specified=True, secure=False, expires=None, discard=True, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False)
        self.br._ua_handlers['_cookies'].cookiejar.set_cookie(jiatxShopWindow)
        mmovenum_cookie=cookielib.Cookie(version=0, name='mmovenum_cookie', value="1", port=None, port_specified=False, domain='.soufun.com', domain_specified=False, domain_initial_dot=True, path='/', path_specified=True, secure=False, expires=None, discard=True, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False)
        self.br._ua_handlers['_cookies'].cookiejar.set_cookie(mmovenum_cookie)
        
        
#        agent_city=cookielib.Cookie(version=0, name='agent_city', value="%c0%a5%c9%bd", port=None, port_specified=False, domain='soufun.com', domain_specified=False, domain_initial_dot=False, path='/', path_specified=True, secure=False, expires=None, discard=True, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False)
#        self.br._ua_handlers['_cookies'].cookiejar.set_cookie(agent_city)
#        citys=cookielib.Cookie(version=0, name='citys', value="%c0%a5%c9%bd", port=None, port_specified=False, domain='soufun.com', domain_specified=False, domain_initial_dot=False, path='/', path_specified=True, secure=False, expires=None, discard=True, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False)
#        self.br._ua_handlers['_cookies'].cookiejar.set_cookie(citys)
#        agent_agentemail=cookielib.Cookie(version=0, name='agent_agentemail', value=self.uname, port=None, port_specified=False, domain='soufun.com', domain_specified=False, domain_initial_dot=False, path='/', path_specified=True, secure=False, expires=None, discard=True, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False)
#        self.br._ua_handlers['_cookies'].cookiejar.set_cookie(agent_agentemail)
#        self.br.open("http://agents.soufun.com/magent/DealSeparateLogin.aspx")
    def goLogin(self):
        
        url='''http://esf.%s.soufun.com/newsecond/include/DefaultUserLoginNew.aspx?method=login&name=%s&pwd=%s'''%(self.area,self.uname,self.upwd)
        page=self.br.open(url).read()
        sts=sj.loads(page)
        
        
        print sts["url2"]
        print sts["url1"]
        if "http://agents.soufun.com/magent/main.aspx" !=sts["url1"]:
            return u"loginerror|登陆有误"
        self.getUqGlCode()
    def makeUploadUrl(self,FName, fiName, cutype, city, isNorth, bakurl):
        sid=random.randint(0000000,999999999)
        action=""
        if isNorth == "Y":
            action = 'http://img1nu.soufun.com/upload/agents/houseinfo2?channel=agent.houseinfo&city=%s&kind=houseinfo&sid=%s&backurl=%s&type=%s&drawtext='%(city,sid,bakurl ,cutype)
        else:
            action = 'http://img1u.soufun.com/upload/agents/houseinfo2?channel=agent.houseinfo&city=%s&kind=houseinfo&sid=%s&backurl=%s&type=%s&drawtext='%(city,sid,bakurl,cutype )

        citys=cookielib.Cookie(version=0, name='citys', value=urllib.quote("city"), port=None, port_specified=False, domain='.soufun.com', domain_specified=False, domain_initial_dot=True, path='/', path_specified=True, secure=False, expires=None, discard=True, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False)
        self.br._ua_handlers['_cookies'].cookiejar.set_cookie(citys)
        agent_city=cookielib.Cookie(version=0, name='agent_city', value=urllib.quote("city"), port=None, port_specified=False, domain='.soufun.com', domain_specified=False, domain_initial_dot=True, path='/', path_specified=True, secure=False, expires=None, discard=True, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False)
        self.br._ua_handlers['_cookies'].cookiejar.set_cookie(agent_city)
        return action
    def goSalePage(self):
        url="http://agents.soufun.com/magent/main.aspx?p=/magent/house/sale/saleinput.aspx"
        self.br.open(url)
        url="http://agents.soufun.com/magent/Manager.aspx?p=/magent/house/sale/saleinput.aspx"
        self.br.open(url)
#        cdd=self.br._ua_handlers['_cookies'].cookiejar._cookies
#        for cd in self.br._ua_handlers['_cookies'].cookiejar._cookies[".soufun.com"]["/"]:
#            print cd
    def doUpLoadPics(self):
        cpics=[]
        pixr='''UploadImageForOne\('(.*)','(.*)','','''
        if len(self.house_drawing)>0:
            for img in self.house_drawing:
                self.countid=self.countid+1
                self.br.select_form(nr=0)
                self.br.form.add_file(open(self.picRoot+img,"rb"), mimetypes.guess_type(self.picRoot+img)[0], os.path.basename(img), name='Hfile', id='Hfile')
                self.br.form.set_all_readonly(False)
                self.br.form.fixup()
                #self.br.set_debug_http(True)
                self.br.form.action=self.Hfileaction
                self.br.form.enctype="multipart/form-data"
                self.br.submit()
                resp=self.br.response().read()
                if re.search(pixr,resp):
                    img=re.search(pixr,resp).group(1)
                    wh=re.search(pixr,resp).group(2)
                    
                #print resp.decode("GB18030") 
                cpics.append(("txtImageDes_3_%s"%self.countid,"户型图".encode("GB18030")))
                cpics.append(("txtImage_3_%s"%self.countid,img))
                cpics.append(("inpUrlsExtend_3_%s"%self.countid,wh))
                cpics.append(("inputIsProj_3_%s"%self.countid,"undefined"))
                cpics.append(("inputOrderIndex_3_%s"%self.countid,self.countid))
                self.br.back(1)
                
        if len(self.house_thumb)>0:
            for img in self.house_drawing:
                self.countid=self.countid+1
                self.br.select_form(nr=0)
                self.br.form.add_file(open(self.picRoot+img,"rb"), mimetypes.guess_type(self.picRoot+img)[0], os.path.basename(img), name='Hfile', id='Hfile')
                self.br.form.set_all_readonly(False)
                self.br.form.fixup()
                self.br.set_debug_http(True)
                self.br.form.action=self.Sfileonchange
                self.br.form.enctype="multipart/form-data"
                self.br.submit()
                resp=self.br.response().read()
                if re.search(pixr,resp):
                    img=re.search(pixr,resp).group(1)
                    wh=re.search(pixr,resp).group(2)
                    
                #print resp.decode("GB18030") 
                cpics.append(("txtImageDes_1_%s"%self.countid,"室内图".encode("GB18030")))
                cpics.append(("txtImage_1_%s"%self.countid,img))
                cpics.append(("inpUrlsExtend_1_%s"%self.countid,wh))
                cpics.append(("inputIsProj_1_%s"%self.countid,"undefined"))
                cpics.append(("inputOrderIndex_1_%s"%self.countid,self.countid))
                
                self.br.back(1)
            
        if len(self.house_xqpic)>0:
            for img in self.house_drawing:
                self.countid=self.countid+1
                self.br.select_form(nr=0)
                self.br.form.add_file(open(self.picRoot+img,"rb"), mimetypes.guess_type(self.picRoot+img)[0], os.path.basename(img), name='Hfile', id='Hfile')
                self.br.form.set_all_readonly(False)
                self.br.form.fixup()
                self.br.set_debug_http(True)
                self.br.form.action=self.Xfileonchange
                self.br.form.enctype="multipart/form-data"
                self.br.submit()
                resp=self.br.response().read()
                if re.search(pixr,resp):
                    img=re.search(pixr,resp).group(1)
                    wh=re.search(pixr,resp).group(2)
                    
                #print resp.decode("GB18030") 
                cpics.append(("txtImageDes_2_%s"%self.countid,"小区相关图".encode("GB18030")))
                cpics.append(("txtImage_2_%s"%self.countid,img))
                cpics.append(("inpUrlsExtend_2_%s"%self.countid,wh))
                cpics.append(("inputIsProj_2_%s"%self.countid,"undefined"))
                cpics.append(("inputOrderIndex_2_%s"%self.countid,self.countid))
                
                self.br.back(1)
        self.customimages.extend(cpics)  
#    def setDefaultValues(self):
#        GMT_FORMAT = '%a %b %d %H:%M:%S UTC+0800 %Y'
#        gmt= time.strftime(GMT_FORMAT,time.localtime(time.time()))
#        url='''http://agents.soufun.com/MAgent/House/getDistrictList.aspx?key=%s&type=%%22%%D7%%A1%%D5%%AC%%22&num=%s'''%(urllib.quote(self.borough_name.decode("UTF-8").encode("GB18030")),urllib.quote(gmt.decode("UTF-8").encode("GB18030")))
#        resp=self.br.open(url).read()
#        
#        #for xq in resp.split("~"):
#        #    xqdl=[]
#        #    for xqd in xq.split("|"):
#        #        xqdl.append(xqd)
#        #    self.xqs.append(xqdl)
#        if resp=="":
#            return False
#            raise Exception("nityError|对方没有匹配小区")
#        xqkey=""
#        try:
#            for xq in resp.split("~"):
#                xqd=xq.split("|")
#                if self.borough_name in xqd[0].decode("GB18030").encode("UTF-8"):
#                    self.subdict["input_y_str_PROJNAME"]=xqd[0]
#                    self.subdict["input_n_str_CONTENT"]=xqd[0]
#                    self.subdict["hiddenProjname"]=xqd[0]
#                    self.subdict["input_y_str_ADDRESS"]=xqd[1]
#                    self.subdict["input_y_str_DISTRICT"]=xqd[2]
#                    self.subdict["input_y_str_COMAREA"]=xqd[3]
#                    xqkey=xqd[4]
#                    break
#        except:
#            raise Exception("nityError|对方没有匹配小区")
#        if not self.subdict.has_key("input_y_str_PROJNAME"):
#            raise Exception("nityError|对方没有匹配小区")
#        
#        
#        url="http://agents.soufun.com/MAgent/House/GetProjData.aspx?newcode=%s&purpose=%%D7%%A1%%D5%%AC&num=%s"%(xqkey,urllib.quote(gmt.decode("UTF-8").encode("GB18030")))
#        #print url
#        resp=self.br.open(url).read()
#        TRAF_SUBW=resp.split("#$%")
#        self.subdict["input_n_str_TRAFFICINFO"]=TRAF_SUBW[0]
#        self.subdict["input_n_str_SUBWAYINFO"]=TRAF_SUBW[1]
#        
#        url='''http://agents.soufun.com/MAgent/House/GetProjAllImg.aspx?imgtype=2&keyword=%%CD%%E2%%BE%%B0%%CD%%BC&newcode=%s&imgname=%%D1%%A1%%D4%%F1%%D0%%A1%%C7%%F8%%CD%%BC'''%xqkey
#        #print url
#        resp=self.br.open(url).read()
#        if re.search('''var ranLis="(.*)"\.split\(','\);''',resp):
#            txtImages=re.search('''var ranLis="(.*)"\.split\(','\);''',resp).group(1).split(",")
#        dom=PyQuery(resp)
#        for i in range(len(txtImages)):
#            i=i+1
#            dimage={}
#            dimage["txtImageDes_2_%s"%i]="%CD%E2%BE%B0%CD%BC"
#            dimage["txtImage_2_%s"%i]=dom("input#pic%s"%i).attr("value")
#            dimage["inpUrlsExtend_2_%s"%i]=""
#            dimage["inputIsProj_2_%s"%i]="2"
#            dimage["inputOrderIndex_2_%s"%i]="%s"%i
#        self.deaufltimages.append(dimage)
#        
#        
#            
#            
#            
#        #print resp.decode("GB18030")
    def initCitys(self,page):
        cityreg='''<script type="text/javascript" src="(/magent/js/city/.*City.js.*)"></script>'''
        d1r='''var Districts = \[(.*)\];'''
        d2r='''name:'(.*)',index:(\d+)'''
        d3r='''},{'''
        a1r='''Area\[(\d+)\]=\[(.*)\];'''
        cl=""
        darr={}
        aarr=[]
        if re.search(cityreg,page):
            cl=re.search(cityreg,page).group(1)
        if cl=="":
            raise Exception("rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr")
        resp=self.br.open(cl).read()
        resp=resp.decode("GB18030")
        if re.search(d1r,resp):
            alld=re.search(d1r,resp).group(1)
            alld=alld.split("},{")
            for ld in alld :
                if re.search(d2r,ld):
                    dk=re.search(d2r,ld).group(1)
                    dv=re.search(d2r,ld).group(2)
                    darr[dk]=dv
        print darr
        if re.search(a1r,resp):
            re.search(a1r,resp).groups()
    def getinput_Hid(self,str):
        strArray = str.split('_');
        lengthA = int(strArray[0]);
        lengthB =  int(strArray[2]);
        strArray2 = strArray[1];
        aaa = "";
        bbb = "";
        index = 0;
        indexA = 0;
        indexB = 0;
        while index < (lengthA + lengthB):
            if indexA < lengthA:
            
                indexA+=1
                aaa += strArray2[index:index+1]
                index+=1
            
            if indexB < lengthB:
                indexB+=1
                bbb += strArray2[index:index+1]
                index+=1
    
        
        return( aaa,bbb) 
    def goPublishCZPage(self):
        url="http://agents.soufun.com/magent/house/lease/leaseinput.aspx"
        resp=self.br.open(url).read()
        pbpage=resp.decode("GB18030").encode("UTF-8")
#        print  pbpage
        if '您今日的发布条数已满'  in resp.decode("GB18030").encode("UTF-8"):
            return "maxhouse|您的该账号今日可发房源数已满"
        self.br.select_form(nr=0)
        Hfileonchange=self.br.form.find_control('Hfile').attrs["onchange"]
        Hfileonchange=Hfileonchange.replace("return UploadPic(","").replace(");","").replace("'","")
        Hfileonchange=Hfileonchange.split(",")
        self.Hfileaction=self.makeUploadUrl(Hfileonchange[0],Hfileonchange[1],Hfileonchange[2],Hfileonchange[3],Hfileonchange[4],Hfileonchange[5],)
        #print self.Hfileaction
        Sfileonchange=self.br.form.find_control('Sfile').attrs["onchange"]
        Sfileonchange=Sfileonchange.replace("return UploadPic(","").replace(");","").replace("'","")
        Sfileonchange=Sfileonchange.split(",")
        self.Sfileonchange=self.makeUploadUrl(Sfileonchange[0],Sfileonchange[1],Sfileonchange[2],Sfileonchange[3],Sfileonchange[4],Sfileonchange[5],)
        #print self.Sfileonchange
        Xfileonchange=self.br.form.find_control('Xfile').attrs["onchange"]
        Xfileonchange=Xfileonchange.replace("return UploadPic(","").replace(");","").replace("'","")
        Xfileonchange=Xfileonchange.split(",")
        self.Xfileonchange=self.makeUploadUrl(Xfileonchange[0],Xfileonchange[1],Xfileonchange[2],Xfileonchange[3],Xfileonchange[4],Xfileonchange[5],)
        #print self.Xfileonchange
        self.doUpLoadPics()
        #self.setDefaultValues()
        #self.br.back(self.countid)
        self.br.select_form( nr=0)
        input_y_str_COMPANYNAME=PyQuery(pbpage)("input#input_y_str_COMPANYNAME") and PyQuery(pbpage)("input#input_y_str_COMPANYNAME").attr("value") or  ""
        input_y_str_PRICETYPE=PyQuery(pbpage)("input#input_PRICETYPE") and PyQuery(pbpage)("input#input_PRICETYPE").attr("value") or ""
        VIEWSTATE=PyQuery(pbpage)("input#__VIEWSTATE") and PyQuery(pbpage)("input#__VIEWSTATE").attr("value") or ""
        d=[
            ("__VIEWSTATE",VIEWSTATE.decode("UTF-8").encode("GB18030")),
            ("input_y_str_PROJNAME","凤栖园".decode("UTF-8").encode("GB18030")),
            ("input_y_str_ADDRESS","凤栖园".decode("UTF-8").encode("GB18030")),
            ("input_y_str_DISTRICT0","锦溪镇".decode("UTF-8").encode("GB18030")),
            ("input_y_str_COMAREA0","锦溪".decode("UTF-8").encode("GB18030")),
            ("str_infocode",""),
#            ("azoq",""),
            ("str_innerid",""),
            ("input_ROOM","1"),
            ("input_HALL","1"),
            ("input_TOILET","1"),
            ("input_KITCHEN","1"),
            ("input_BALCONY","1"),
#            ("coe5g5","on"),
            ("input_str_HouseStructure","平层".decode("UTF-8").encode("GB18030")),
            ("input_y_num_PRICE","700"),
            ("input_y_str_LEASESTYLE","整租".decode("UTF-8").encode("GB18030")),
            ("input_n_str_leaseRoomType","单间".decode("UTF-8").encode("GB18030")),
            ("input_n_str_leaseDetail","性别不限".decode("UTF-8").encode("GB18030")),
            ("input_y_str_PAYDETAIL","无押年付".decode("UTF-8").encode("GB18030")),
            ("input_y_str_PAYINFO","年付".decode("UTF-8").encode("GB18030")),
            ("6b5e2e9binput9d54","42"),
            ("input_n_str_CREATETIME","2008"),
#            ("0xvam6",""),
            ("input_FLOOR","3"),
            ("input_ALLFLOOR","8"),
#            ("89ml8","38gh6rxex"),
            ("input_n_str_FORWARD","南".decode("UTF-8").encode("GB18030")),
            ("input_n_str_FITMENT",u"简装修".decode("UTF-8").encode("GB18030")),
#            ("n","on"),
            ("input_n_str_BASESERVICE","水".decode("UTF-8").encode("GB18030")),
            ("input_n_str_BASESERVICE","电".decode("UTF-8").encode("GB18030")),
            ("input_n_str_BASESERVICE","煤气/天然气".decode("UTF-8").encode("GB18030")),
            ("input_n_str_BASESERVICE","暖气".decode("UTF-8").encode("GB18030")),
            ("input_n_str_BASESERVICE","有线电视".decode("UTF-8").encode("GB18030")),
            ("input_n_str_BASESERVICE","宽带".decode("UTF-8").encode("GB18030")),
            ("input_n_str_BASESERVICE","电梯".decode("UTF-8").encode("GB18030")),
            ("input_n_str_BASESERVICE","车位/车库".decode("UTF-8").encode("GB18030")),
            ("input_n_str_BASESERVICE","储藏室/地下室".decode("UTF-8").encode("GB18030")),
            ("input_n_str_BASESERVICE","露台/花园".decode("UTF-8").encode("GB18030")),
#            ("2vl2s9gcfmk",""),
            ("input_n_str_EQUITMENT","电话".decode("UTF-8").encode("GB18030")),
            ("input_n_str_EQUITMENT","热水器".decode("UTF-8").encode("GB18030")),
            ("input_n_str_EQUITMENT","空调".decode("UTF-8").encode("GB18030")),
            ("input_n_str_EQUITMENT","冰箱".decode("UTF-8").encode("GB18030")),
            ("input_n_str_EQUITMENT","洗衣机".decode("UTF-8").encode("GB18030")),
            ("input_n_str_EQUITMENT","床".decode("UTF-8").encode("GB18030")),
            ("input_n_str_EQUITMENT","家具".decode("UTF-8").encode("GB18030")),
            ("input_n_str_EQUITMENT","微波炉".decode("UTF-8").encode("GB18030")),
            ("input_n_str_EQUITMENT","厨具".decode("UTF-8").encode("GB18030")),
            ("input_n_str_LOOKHOUSE","非工作时间".decode("UTF-8").encode("GB18030")),
            ("input_n_str_LIVETIME",""),
            ("5fed3002input40d5","凤栖园凤栖园凤栖园".decode("UTF-8").encode("GB18030")),
            ("input_n_str_CONTENT","凤栖园凤栖园凤栖园凤栖园凤栖园".decode("UTF-8").encode("GB18030")),
            ("input_n_str_TRAFFICINFO","111111111111111111111111".decode("UTF-8").encode("GB18030")),
            ("input_n_str_SUBWAYINFO","122222222222222222222222222222".decode("UTF-8").encode("GB18030")),
            ("Hfile",""),
            ("Sfile",""),
            ("Xfile",""),
#            ("uu6bhjw0bq","y0mjc"),
            ("inputdrawtext",""),
            ("hdHouseDicCity","0"),
#            ("3321","on"),
            ("input_y_str_DISTRICT","锦溪镇".decode("UTF-8").encode("GB18030")),
            ("input_y_str_COMAREA","锦溪".decode("UTF-8").encode("GB18030")),
#            ("p8hs8s7dm",""),
            ("inputT","2011-07-08+14:00:05"),
            ("input_y_str_PURPOSE","住宅".decode("UTF-8").encode("GB18030")),
            ("imageCount","%s"%self.countid),
            ("coverPhoto",""),
            ("newcode",""),
#            ("hil9",""),
            ("newprojimgs",""),
            ("guidCode",""),
            ("tempprojimgs",""),
#            ("ms3_uqj",""),
            ("ComareasNum",""),
            ("UseProjImage",""),
#            ("ltm2qlvc5iq0","egwie53i8fz"),
            ("input_y_str_MANAGERNAME",self.uname.decode("UTF-8").encode("GB18030")),
            ("input_y_str_BUSINESSTYPE","CZ"),
#            ("5ay16wf2dlos","kb3y2hkhq8"),
            ("input_y_str_COMPANYNAME",input_y_str_COMPANYNAME.decode("UTF-8").encode("GB18030")),
            ("input_y_str_PRICETYPE",input_y_str_PRICETYPE.decode("UTF-8").encode("GB18030")),
#            ("0bimthmw",""),
            ("hiddenProjname",""),
#            ("8ozbneiouo2yq","on"),
            ("input_DelegateIDAndAgentID","0"),
            ("input_draftsID","0"),
#            ("input_Hid","17_831d4414be712518iinnppuutt42493609_17"),
            ("hdUseMode",""),
#            ("cxj3p8tlkok","jj9i"),
#            ("8141b721input4430","3d44e158input2969"),
#            ("b832bsdf4inpu","9e03a5input")
           ]
#        urllib.urlencode(d)
        d.extend(self.customimages)
#        urllib.urlencode(d)
        postkeys=[ c[0] for c in d ]
        ppp=PyQuery(pbpage)("inpt")
        if re.search('''<inpt name="(.*)" value="(.*)"></inpt>''', pbpage):
            hdname=re.search('''<inpt name="(.*)" value="(.*)"></inpt>''', pbpage).group(1)
            hdvalue=re.search('''<inpt name="(.*)" value="(.*)"></inpt>''', pbpage).group(2)
            d.append((hdname,hdvalue))
        print "+"*60
        for ctrl in self.br.form.controls:
            if ctrl.name==None or ctrl.name=="":
                continue
            if ctrl.name=="input_Hid":
                hid=self.getinput_Hid(ctrl.value)
                d.append(hid)
            nk=""
            nv=""
            if not ctrl.name in  postkeys:
                nk=ctrl.name
                if ctrl.value==None:
                    nv=""
                else:
                    if type(ctrl.value)==list:
                        if ctrl.value!=[]:
                            nv=random.choice(ctrl.value)
                    else:
                        nv=ctrl.value
#                if ctrl.name=="tempHouseID":
#                    nv=ctrl.value
                d.append((nk,nv))
#        print  "="*60
#        for ddi in d:
#            print ddi[0],ddi[1].decode("GB18030").encode("UTF-8")
#        print  "="*60        
                
        
        data=urllib.urlencode(d)
        print data
        self.br.addheaders = [("Referer", "http://agents.soufun.com/magent/house/sale/saleinput.aspx")] 
        resp=self.br.open("http://agents.soufun.com/MAgent/house/InputSave.aspx?flag=2",data)
        
        
        
#        resp=self.br.submit()
        respage=resp.read().decode("GB18030")
#        print respage
        if "window.location.replace" in respage :
            if re.search('''window\.location\.replace\('(.*)'\);''',respage):
                sts=re.search('''window\.location\.replace\('(.*)'\);''',respage).group(1)
                return "success|%s"%sts
            else:
                return "puterror3|%s"%"无正确相应结果"
        else:
            if re.search('''alert\('(.*)'\)''',respage):
                sts=re.search('''alert\('(.*)'\)''',respage).group(1)
                return "puterror4|%s"%sts
            else:
                return respage
    def goPublishPage(self):
#        url='''http://agents.soufun.com/magent/Manager.aspx'''
#        resp=self.br.open(url).read()
#        if '''src="/magent/Right.aspx" name="mainFrame"''' in resp:
#            
#        print  resp.decode("GB18030").encode("UTF-8")
        
        
        
        url='''http://agents.soufun.com/magent/house/sale/saleinput.aspx'''
        resp=self.br.open(url).read()
        pbpage=resp.decode("GB18030").encode("UTF-8")
        #print  pbpage
        #===========================================================================
        if '您今日的发布条数已满'  in resp.decode("GB18030").encode("UTF-8"):
            return "maxhouse|您的该账号今日可发房源数已满"
        #===========================================================================
        #self.initCitys(resp)
        
        self.br.select_form(nr=0)
        Hfileonchange=self.br.form.find_control('Hfile').attrs["onchange"]
        Hfileonchange=Hfileonchange.replace("return UploadPic(","").replace(");","").replace("'","")
        Hfileonchange=Hfileonchange.split(",")
        self.Hfileaction=self.makeUploadUrl(Hfileonchange[0],Hfileonchange[1],Hfileonchange[2],Hfileonchange[3],Hfileonchange[4],Hfileonchange[5],)
        #print self.Hfileaction
        Sfileonchange=self.br.form.find_control('Sfile').attrs["onchange"]
        Sfileonchange=Sfileonchange.replace("return UploadPic(","").replace(");","").replace("'","")
        Sfileonchange=Sfileonchange.split(",")
        self.Sfileonchange=self.makeUploadUrl(Sfileonchange[0],Sfileonchange[1],Sfileonchange[2],Sfileonchange[3],Sfileonchange[4],Sfileonchange[5],)
        #print self.Sfileonchange
        Xfileonchange=self.br.form.find_control('Xfile').attrs["onchange"]
        Xfileonchange=Xfileonchange.replace("return UploadPic(","").replace(");","").replace("'","")
        Xfileonchange=Xfileonchange.split(",")
        self.Xfileonchange=self.makeUploadUrl(Xfileonchange[0],Xfileonchange[1],Xfileonchange[2],Xfileonchange[3],Xfileonchange[4],Xfileonchange[5],)
        #print self.Xfileonchange
        self.doUpLoadPics()
        #self.setDefaultValues()
        #self.br.back(self.countid)
        self.br.select_form( nr=0)
        
        
        
#        self.br.form.new_control('input', "input_y_str_DISTRICT0", {'value':""})
#        self.br.form.new_control('input', "input_y_str_COMAREA0", {'value':""})
#        self.br.form.new_control('input', "input_str_PropertySubType", {'value':u"普通住宅".decode("UTF-8").encode("GB18030")})
#        self.br.form.new_control('input', "input_y_str_PAYINFO0", {'value':u"个人产权".decode("UTF-8").encode("GB18030")})
#        self.br.form.find_control('input_y_str_PAYINFO').attrs["value"]=u"个人产权".decode("UTF-8").encode("GB18030")
#        self.br.form.new_control('input', "input_ROOM", {'value':""})
#        self.br.form.new_control('input', "input_HALL", {'value':""})
#        self.br.form.new_control('input', "input_TOILET", {'value':""})
#        self.br.form.new_control('input', "input_KITCHEN", {'value':""})
#        self.br.form.new_control('input', "input_BALCONY", {'value':""})
#        self.br.form.new_control('input', "input_FLOOR", {'value':""})
#        self.br.form.new_control('input', "input_ALLFLOOR", {'value':""})
#        self.br.form.find_control('imageCount').attrs["value"]=u"1"
#        self.br.form.new_control('input', "rwepp", {'value':""})
#        self.br.form.find_control('input_y_str_BUSINESSTYPE').attrs["value"]=u"CS"
        
        
        
        
        
        
        
        
        
        
#        self.br.form.set_all_readonly(False)
#        self.br.form.fixup()
#        self.br.set_debug_http(True)
#        self.br.form.action=Hfileaction
#        self.br.form.enctype="multipart/form-data"
        
#        print self.br.form
        
        for d in self.subdict.items():
            print d[0].decode("GB18030"),d[1].decode("GB18030")
        print "*"*60
#        for ctrl in self.br.form.controls:
#            if ctrl.name==None:
#                continue
#            print "%s=%s"%(ctrl.name,ctrl.value)
            
            
        print "="*60
#        cdd=self.br._ua_handlers['_cookies'].cookiejar._cookies
#        for cd in self.br._ua_handlers['_cookies'].cookiejar._cookies[".soufun.com"]["/"].items():
#            if cd[0]=="agent_loginname":
#                
#            print "%s=%s"%(cd[0],cd[1])
#        self.br.set_debug_http(True)   
        
        
#        str='''input_y_str_PROJNAME=%C0%A5%C9%BD%BB%A8%D4%B0&input_y_str_ADDRESS=%B3%A4%BD%AD%B1%B1%C2%B7118%BA%C5&input_y_str_DISTRICT0=&input_y_str_COMAREA0=&str_infocode=&6z1qdys=&_mnzh=&ldfzgdaj=&opj28c2s5=&str_innerid=&input_str_PropertySubType=%C9%CC%D7%A1%C2%A5&input_y_str_PAYINFO0=%CA%B9%D3%C3%C8%A8&input_y_str_PAYINFO=%CA%B9%D3%C3%C8%A8&input_y_num_PRICE=123&input_ROOM=3&input_HALL=2&input_TOILET=1&input_KITCHEN=1&input_BALCONY=1&input_str_HouseStructure=%C6%BD%B2%E3&input_str_BuildingType=%C6%BD%B7%BF&6b5e2e9binput9d54=133&input_y_num_LIVEAREA=120&input_n_str_CREATETIME=2008&input_FLOOR=1&input_ALLFLOOR=1&input_n_str_FORWARD=%B6%AB&input_n_str_FITMENT=%BE%AB%D7%B0%D0%DE&input_n_str_BASESERVICE=%C3%BA%C6%F8%2F%CC%EC%C8%BB%C6%F8&input_n_str_BASESERVICE=%C5%AF%C6%F8&input_n_str_BASESERVICE=%B5%E7%CC%DD&input_n_str_BASESERVICE=%B3%B5%CE%BB%2F%B3%B5%BF%E2&input_n_str_BASESERVICE=%B4%A2%B2%D8%CA%D2%2F%B5%D8%CF%C2%CA%D2&input_n_str_BASESERVICE=%BB%A8%D4%B0%2F%D0%A1%D4%BA&input_n_str_BASESERVICE=%C2%B6%CC%A8&input_n_str_BASESERVICE=%B8%F3%C2%A5&input_n_str_LOOKHOUSE=%CB%E6%CA%B1%BF%B4%B7%BF&33na757zgma=&zdenhy2ra=&dum5b=&input_OoOo0w=&spa56kn51z=&5fed3002input40d5=%C0%A5%C9%BD%BB%A8%D4%B0111&input_n_str_CONTENT=%C0%A5%C9%BD%BB%A8%D4%B0222&9jyxfua=&2acttyl=&6bpd0egym=&x5srlukvi=&mkntqby6=&input_n_str_TRAFFICINFO=7%C2%B7%A1%A2122%C2%B7&0l229rkh11s=&gtc5lwpt9dq0k=&1mm_a=&5_q_6r=&input_n_str_SUBWAYINFO=%B4%F3%D1%A7%A3%BA%BD%AD%CB%D5%B9%E3%B2%A5%B5%E7%CA%D3%B4%F3%D1%A7%C0%A5%C9%BD%D1%A7%D4%BA%0D%0A%D6%D0%D0%A1%D1%A7%A3%BA+%D4%A3%D4%AA%CA%B5%D1%E9%D0%A1%D1%A7++%0D%0A%D3%D7%B6%F9%D4%B0%A3%BA+%D3%FD%D3%A2%B9%FA%BC%CA%D3%D7%B6%F9%D4%B0%0D%0A%C9%CC%B3%A1%A3%BA%D2%D7%B3%F5%B0%AE%C1%AB%B3%AC%CA%D0%A1%A2%CD%FB%D7%E5%C9%CC%B3%C7%A1%A2%B6%A5%D0%C2%B3%AC%CA%D0%0D%0A%D3%CA%BE%D6%A3%BA%C0%A5%C9%BD%CA%D0%D3%CA%D5%FE%BE%D6%D6%DC%CA%D0%D6%A7%BE%D6%0D%0A%D2%F8%D0%D0%A3%BA%C5%A9%D2%B5%D2%F8%D0%D0%B9%A4%C9%CC%D2%F8%D0%D0+%0D%0A%D2%BD%D4%BA%A3%BA%C0%A5%C9%BD%C5%AE%D7%D3%D2%BD%D4%BA++%0D%0A%C6%E4%CB%FB%A3%BA%CA%D0%D5%FE%B9%AB%D4%B0%A1%A2%D5%FE%B8%AE%B9%E3%B3%A1%A1%A2%B9%FA%BC%CA%D0%A1%D1%A7%A1%A2%B3%A4%BD%AD%B9%AB%D4%B0%0D%0A&q2et=&hsud8uj5ouv=&iacojw0gg=&iltb=&Hfile=&Sfile=&Xfile=&txtImageDes_2_1=%CD%E2%BE%B0%CD%BC&txtImage_2_1=http%3A%2F%2Fimg1.soufunimg.com%2Fagents%2F2010_12%2F26%2F34%2F39%2Fkunshan%2Fhouseinfo%2F404953452400.jpg&inpUrlsExtend_2_1=&inputIsProj_2_1=2&inputOrderIndex_2_1=1&txtImageDes_2_2=%CD%E2%BE%B0%CD%BC&txtImage_2_2=http%3A%2F%2Fimg1.soufunimg.com%2Fagents%2F2010_11%2F14%2Fkunshan%2Fhouseinfo%2F1289721720264_000.jpg&inpUrlsExtend_2_2=&inputIsProj_2_2=2&inputOrderIndex_2_2=2&txtImageDes_2_3=%CD%E2%BE%B0%CD%BC&txtImage_2_3=http%3A%2F%2Fimg.soufun.com%2Fhouse%2F2006_03%2F23%2F1143101889347.jpeg&inpUrlsExtend_2_3=&inputIsProj_2_3=2&inputOrderIndex_2_3=3&wkh8ebuwdh=&89ml8=&inputdrawtext=&hdHouseDicCity=0&viy=&hj8i5uou=&1x3rbatnm=&_6a12z=&inputT=2011-07-04+03%3A11%3A40&d93n55y=&1hyco2dz=&input_y_str_DISTRICT=%D3%F1%C9%BD%D5%F2&input_y_str_COMAREA=%B3%C7%B1%B1&ms3_uqjz=&_iu1d5qkzr=&xi5ufs=&bvupejg3w=&hmzz0xhmgz9so8=&input_y_str_PURPOSE=%D7%A1%D5%AC&imageCount=3&frl=&c1dw8z3p8v=&9edutf68t=&dmsxci0o6pupc=&1apzon=&coverPhoto=&newcode=1823067409&a87ec=&y199pm3zd=&sfpfpd=&ed7fqm=&00d3=&tempprojimgs=&newprojimgs=&UseProjImage=&2teq8xop=&idr9=&input_y_str_MANAGERNAME=changna19880422&lnike2x=&nmckj0923h=&asdmkljsdqouwev=&71o93j32y=&lfx6sb01pq=&input_Hid=17_831d4414be712518iinnppuutt42493609_17&input_y_str_BUSINESSTYPE=CS&32dmk=&rej8nqkx=&1ebam6b3y7dgzyp=&fgwoe_eor8s7lqj=&zjuejsaju=&input_y_str_COMPANYNAME=%BE%FD%D4%C3%B2%BB%B6%AF%B2%FA&input_y_str_PRICETYPE=%CD%F2%D4%AA%2F%CC%D7&hiddenProjname=%C0%A5%C9%BD%BB%A8%D4%B0&hdUseMode=&guidCode=&input_DelegateIDAndAgentID=0&input_draftsID=0&t90rvw3m1fz=&v6cscj3qyx0yqg=&g35l1rxxqgj=&u8plx5eehn_mfh=&66kxksm18qp=&1yb=&ww1k5txq=&coe5g5=&tempHouseID=47986041-ac2b-45e0-9adf-f858db9ec5a5&8141b721input4430=3d44e158input2969&b832bsdf4inpu=9e03a5input'''
##        str= urllib.unquote(str)
       
#        data=urllib.urlencode(d)
#        data=data[1:]
#        str="input_y_str_PROJNAME=%C0%A5%C9%BD%BB%A8%D4%B0&input_y_str_ADDRESS=%B3%A4%BD%AD%B1%B1%C2%B7118%BA%C5&input_y_str_DISTRICT0=&input_y_str_COMAREA0=&str_infocode=&6z1qdys=&_mnzh=&ldfzgdaj=&opj28c2s5=&str_innerid=&input_str_PropertySubType=%C9%CC%D7%A1%C2%A5&input_y_str_PAYINFO0=%CA%B9%D3%C3%C8%A8&input_y_str_PAYINFO=%CA%B9%D3%C3%C8%A8&input_y_num_PRICE=123&input_ROOM=3&input_HALL=2&input_TOILET=1&input_KITCHEN=1&input_BALCONY=1&input_str_HouseStructure=%C6%BD%B2%E3&input_str_BuildingType=%C6%BD%B7%BF&6b5e2e9binput9d54=133&input_y_num_LIVEAREA=120&input_n_str_CREATETIME=2008&input_FLOOR=1&input_ALLFLOOR=1&input_n_str_FORWARD=%B6%AB&input_n_str_FITMENT=%BE%AB%D7%B0%D0%DE&input_n_str_BASESERVICE=%C3%BA%C6%F8%2F%CC%EC%C8%BB%C6%F8&input_n_str_BASESERVICE=%C5%AF%C6%F8&input_n_str_BASESERVICE=%B5%E7%CC%DD&input_n_str_BASESERVICE=%B3%B5%CE%BB%2F%B3%B5%BF%E2&input_n_str_BASESERVICE=%B4%A2%B2%D8%CA%D2%2F%B5%D8%CF%C2%CA%D2&input_n_str_BASESERVICE=%BB%A8%D4%B0%2F%D0%A1%D4%BA&input_n_str_BASESERVICE=%C2%B6%CC%A8&input_n_str_BASESERVICE=%B8%F3%C2%A5&input_n_str_LOOKHOUSE=%CB%E6%CA%B1%BF%B4%B7%BF&33na757zgma=&zdenhy2ra=&dum5b=&input_OoOo0w=&spa56kn51z=&5fed3002input40d5=%C0%A5%C9%BD%BB%A8%D4%B0111&input_n_str_CONTENT=%C0%A5%C9%BD%BB%A8%D4%B0222&9jyxfua=&2acttyl=&6bpd0egym=&x5srlukvi=&mkntqby6=&input_n_str_TRAFFICINFO=7%C2%B7%A1%A2122%C2%B7&0l229rkh11s=&gtc5lwpt9dq0k=&1mm_a=&5_q_6r=&input_n_str_SUBWAYINFO=%B4%F3%D1%A7%A3%BA%BD%AD%CB%D5%B9%E3%B2%A5%B5%E7%CA%D3%B4%F3%D1%A7%C0%A5%C9%BD%D1%A7%D4%BA%0D%0A%D6%D0%D0%A1%D1%A7%A3%BA+%D4%A3%D4%AA%CA%B5%D1%E9%D0%A1%D1%A7++%0D%0A%D3%D7%B6%F9%D4%B0%A3%BA+%D3%FD%D3%A2%B9%FA%BC%CA%D3%D7%B6%F9%D4%B0%0D%0A%C9%CC%B3%A1%A3%BA%D2%D7%B3%F5%B0%AE%C1%AB%B3%AC%CA%D0%A1%A2%CD%FB%D7%E5%C9%CC%B3%C7%A1%A2%B6%A5%D0%C2%B3%AC%CA%D0%0D%0A%D3%CA%BE%D6%A3%BA%C0%A5%C9%BD%CA%D0%D3%CA%D5%FE%BE%D6%D6%DC%CA%D0%D6%A7%BE%D6%0D%0A%D2%F8%D0%D0%A3%BA%C5%A9%D2%B5%D2%F8%D0%D0%B9%A4%C9%CC%D2%F8%D0%D0+%0D%0A%D2%BD%D4%BA%A3%BA%C0%A5%C9%BD%C5%AE%D7%D3%D2%BD%D4%BA++%0D%0A%C6%E4%CB%FB%A3%BA%CA%D0%D5%FE%B9%AB%D4%B0%A1%A2%D5%FE%B8%AE%B9%E3%B3%A1%A1%A2%B9%FA%BC%CA%D0%A1%D1%A7%A1%A2%B3%A4%BD%AD%B9%AB%D4%B0%0D%0A&q2et=&hsud8uj5ouv=&iacojw0gg=&iltb=&Hfile=&Sfile=&Xfile=&txtImageDes_2_1=%CD%E2%BE%B0%CD%BC&txtImage_2_1=http%3A%2F%2Fimg1.soufunimg.com%2Fagents%2F2010_12%2F26%2F34%2F39%2Fkunshan%2Fhouseinfo%2F404953452400.jpg&inpUrlsExtend_2_1=&inputIsProj_2_1=2&inputOrderIndex_2_1=1&txtImageDes_2_2=%CD%E2%BE%B0%CD%BC&txtImage_2_2=http%3A%2F%2Fimg1.soufunimg.com%2Fagents%2F2010_11%2F14%2Fkunshan%2Fhouseinfo%2F1289721720264_000.jpg&inpUrlsExtend_2_2=&inputIsProj_2_2=2&inputOrderIndex_2_2=2&txtImageDes_2_3=%CD%E2%BE%B0%CD%BC&txtImage_2_3=http%3A%2F%2Fimg.soufun.com%2Fhouse%2F2006_03%2F23%2F1143101889347.jpeg&inpUrlsExtend_2_3=&inputIsProj_2_3=2&inputOrderIndex_2_3=3&wkh8ebuwdh=&89ml8=&inputdrawtext=&hdHouseDicCity=0&viy=&hj8i5uou=&1x3rbatnm=&_6a12z=&inputT=2011-07-04+03%3A11%3A40&d93n55y=&1hyco2dz=&input_y_str_DISTRICT=%D3%F1%C9%BD%D5%F2&input_y_str_COMAREA=%B3%C7%B1%B1&ms3_uqjz=&_iu1d5qkzr=&xi5ufs=&bvupejg3w=&hmzz0xhmgz9so8=&input_y_str_PURPOSE=%D7%A1%D5%AC&imageCount=3&frl=&c1dw8z3p8v=&9edutf68t=&dmsxci0o6pupc=&1apzon=&coverPhoto=&newcode=1823067409&a87ec=&y199pm3zd=&sfpfpd=&ed7fqm=&00d3=&tempprojimgs=&newprojimgs=&UseProjImage=&2teq8xop=&idr9=&input_y_str_MANAGERNAME=changna19880422&lnike2x=&nmckj0923h=&asdmkljsdqouwev=&71o93j32y=&lfx6sb01pq=&input_Hid=17_831d4414be712518iinnppuutt42493609_17&input_y_str_BUSINESSTYPE=CS&32dmk=&rej8nqkx=&1ebam6b3y7dgzyp=&fgwoe_eor8s7lqj=&zjuejsaju=&input_y_str_COMPANYNAME=%BE%FD%D4%C3%B2%BB%B6%AF%B2%FA&input_y_str_PRICETYPE=%CD%F2%D4%AA%2F%CC%D7&hiddenProjname=%C0%A5%C9%BD%BB%A8%D4%B0&hdUseMode=&guidCode=&input_DelegateIDAndAgentID=0&input_draftsID=0&t90rvw3m1fz=&v6cscj3qyx0yqg=&g35l1rxxqgj=&u8plx5eehn_mfh=&66kxksm18qp=&1yb=&ww1k5txq=&coe5g5=&tempHouseID=47986041-ac2b-45e0-9adf-f858db9ec5a5&8141b721input4430=3d44e158input2969&b832bsdf4inpu=9e03a5input"
#        print str.count("&")
        input_y_str_COMPANYNAME=PyQuery(pbpage)("input#input_y_str_COMPANYNAME") and PyQuery(pbpage)("input#input_y_str_COMPANYNAME").attr("value").decode("UTF-8").encode("GB18030") or ""
        input_y_str_PRICETYPE=PyQuery(pbpage)("input#input_PRICETYPE") and PyQuery(pbpage)("input#input_PRICETYPE").attr("value").decode("UTF-8").encode("GB18030") or ""
        d=[
            ("input_y_str_PROJNAME","淀山假期花园".decode("UTF-8").encode("GB18030")),#楼盘名
            ("input_y_str_ADDRESS","时的发生地方".decode("UTF-8").encode("GB18030")),
            ("input_y_str_DISTRICT0","淀山湖镇".decode("UTF-8").encode("GB18030")),#区域
            ("input_y_str_COMAREA0","淀山湖".decode("UTF-8").encode("GB18030")),#商圈
            ("str_infocode",""),
            ("str_innerid",""),
            
            ("input_str_PropertySubType",""),
            ("input_str_PropertySubType","普通住宅".decode("UTF-8").encode("GB18030")),
            ("input_y_str_PAYINFO0","个人产权".decode("UTF-8").encode("GB18030")),
            ("input_y_str_PAYINFO","个人产权".decode("UTF-8").encode("GB18030")),#出租为支付方式
            ("input_y_num_PRICE","100"),
            ("input_ROOM","2"),
            ("input_HALL","1"),
            ("input_TOILET","1"),
            ("input_KITCHEN","1"),
            ("input_BALCONY","1"),
            ("input_str_HouseStructure","平层".decode("UTF-8").encode("GB18030")),
            ("input_str_BuildingType","板楼".decode("UTF-8").encode("GB18030")),
            ("6b5e2e9binput9d54","80"),
            ("input_y_num_LIVEAREA","75"),
            ("input_n_str_CREATETIME","2008"),
            ("input_FLOOR","1"),
            ("input_ALLFLOOR","12"),
            ("input_n_str_FORWARD","南".decode("UTF-8").encode("GB18030")),
            ("input_n_str_FITMENT","精装修".decode("UTF-8").encode("GB18030")),
            ("input_n_str_BASESERVICE","煤气/天然气".decode("UTF-8").encode("GB18030")),
            ("input_n_str_BASESERVICE","暖气".decode("UTF-8").encode("GB18030")),
            ("input_n_str_BASESERVICE","电梯".decode("UTF-8").encode("GB18030")),
            ("input_n_str_BASESERVICE","车位/车库".decode("UTF-8").encode("GB18030")),
            ("input_n_str_BASESERVICE","储藏室/地下室".decode("UTF-8").encode("GB18030")),
            ("input_n_str_BASESERVICE","花园/小院".decode("UTF-8").encode("GB18030")),
            ("input_n_str_BASESERVICE","露台".decode("UTF-8").encode("GB18030")),
            ("input_n_str_BASESERVICE","阁楼".decode("UTF-8").encode("GB18030")),
            ("input_n_str_LOOKHOUSE","随时看房".decode("UTF-8").encode("GB18030")),
            #("rxb8wpzr8tq2vz",""),
            #("wk9hvpfj",""),
            
            ("5fed3002input40d5","1111111111".decode("UTF-8").encode("GB18030")),#房源标题
            ("input_n_str_CONTENT","22222222222222222".decode("UTF-8").encode("GB18030")),#房源描述
            #("fmrswpxl0c",""),
            #("g2q9qd16c3l",""),
            #("i3uw67kq",""),
            #("sxjgo2m",""),
            #("gyu5rq",""),
            ("input_n_str_TRAFFICINFO",""),#交通
            #("zxk52i3krqah1y",""),
            #("pkyrpq9i",""),
            #("hr6w2z",""),
            #("input_str_mzznd",""),
            #("t0usn6u1",""),
            ("input_n_str_SUBWAYINFO",""),#周边
            #("0u3pqm",""),
            #("2kp3dnjzkr",""),
            #("a3jev19req",""),
            #("yk2ql07r5090ws",""),
            #("ndvgci99d",""),
            ("Hfile",""),
            ("Sfile",""),
            ("Xfile",""),
            #("231t",""),
            #("ao8h6a",""),
            #("kveko73zbtl",""),
            #("dgrh",""),
            #("tyr20",""),
            ("inputdrawtext",""),
            ("hdHouseDicCity","0"),
            #("hhou3k",""),
            #("rnk30r",""),
            #("uonmqghrbx",""),
            #("mgturnn2bw56a1",""),
            ("inputT","2011-07-04+04:26:35"),
            ("input_y_str_DISTRICT","淀山湖镇".decode("UTF-8").encode("GB18030")),
            ("input_y_str_COMAREA","淀山湖".decode("UTF-8").encode("GB18030")),
            #("z7wzt",""),
            #("jexu3yhh3ftt",""),
            #("901sqsdn7v",""),
            #("ztw000fb",""),
            ("input_y_str_PURPOSE","住宅".decode("UTF-8").encode("GB18030")),
            ("imageCount",self.countid),
            
            
#            ("txtImageDes_2_1","外景图".encode("GB18030")),
#            ("txtImage_2_1","http://img1.soufunimg.com/agents/2010_12/26/34/39/kunshan/houseinfo/404953452400.jpg"),
#            ("inpUrlsExtend_2_1",""),
#            ("inputIsProj_2_1","2"),
#            ("inputOrderIndex_2_1","1"),
#            ("txtImageDes_2_2","外景图".encode("GB18030")),
#            ("txtImage_2_2","http://img1.soufunimg.com/agents/2010_11/14/kunshan/houseinfo/1289721720264_000.jpg"),
#            ("inpUrlsExtend_2_2",""),
#            ("inputIsProj_2_2","2"),
#            ("inputOrderIndex_2_2","2"),
#            ("txtImageDes_2_3","外景图".encode("GB18030")),
#            ("txtImage_2_3","http://img.soufun.com/house/2006_03/23/1143101889347.jpeg"),
#            ("inpUrlsExtend_2_3",""),
#            ("inputIsProj_2_3","2"),
#            ("inputOrderIndex_2_3","3"),
#            
            
            
            
            
            
            
            
            #("pr3zy6qu",""),
            #("rcvmlss1t",""),
            ("coverPhoto",""),
            ("newcode",""),
            #("a87ec",""),
            #("hqkbz6ayd",""),
            #("lrx0ejh2kypv",""),
            #("c2zdjc",""),
            #("16uwcs3l",""),
            #("s023",""),
            ("tempprojimgs",""),
            ("newprojimgs",""),
            ("UseProjImage",""),
            ("input_y_str_MANAGERNAME",self.uname),
            #("bvrn_nq9hhy",""),
            #("59i8cxj",""),
            #("input_Hid","17_831d4414be712518iinnppuutt42493609_17"),
            ("input_y_str_BUSINESSTYPE","CS"),
            #("yknjvjd1s",""),
            #("6ek79w",""),
            
            ("input_y_str_COMPANYNAME",input_y_str_COMPANYNAME),
            ("input_y_str_PRICETYPE",input_y_str_PRICETYPE),
            
            ("hiddenProjname",""),
            ("hdUseMode",""),
            ("guidCode",""),
            ("input_DelegateIDAndAgentID","0"),
            ("input_draftsID","0"),
            #("ncx0o",""),
            #("8sglz",""),
            #("frc",""),
            #("input_str_zaqwer2134fgvaf",""),
            #("rzeys2x2t",""),
            #("o0q8",""),
            #("tempHouseID","9ef614bc-92bd-44c4-ab33-f6cafeb19007"),
#            ("8141b721input4430","3d44e158input2969"),
            #("b832bsdf4inpu","9e03a5input")

           ]
       
        
        
        

#        if self.pdb["house_kind"]=="2":
#            pass
#            d.append(("input_y_str_LEASESTYLE","整租".decode("UTF-8").encode("GB18030")))
#            d.append(("input_n_str_leaseRoomType","单间".decode("UTF-8").encode("GB18030")))
#            d.append(("input_n_str_leaseDetail","性别不限".decode("UTF-8").encode("GB18030")))
#            d.append(("input_y_str_PAYDETAIL","面议".decode("UTF-8").encode("GB18030")))
#            d.append(("input_n_str_EQUITMENT","电话".decode("UTF-8").encode("GB18030")))
#            d.append(("input_n_str_EQUITMENT","热水器".decode("UTF-8").encode("GB18030")))
#            d.append(("input_n_str_EQUITMENT","空调".decode("UTF-8").encode("GB18030")))
#            d.append(("input_n_str_EQUITMENT","冰箱".decode("UTF-8").encode("GB18030")))
#            d.append(("input_n_str_EQUITMENT","洗衣机".decode("UTF-8").encode("GB18030")))
#            d.append(("input_n_str_EQUITMENT","床".decode("UTF-8").encode("GB18030")))
#            d.append(("input_n_str_EQUITMENT","家具".decode("UTF-8").encode("GB18030")))
#            d.append(("input_n_str_EQUITMENT","微波炉".decode("UTF-8").encode("GB18030")))
#            d.append(("input_n_str_EQUITMENT","厨具".decode("UTF-8").encode("GB18030")))
#            d.append(("input_y_str_PAYINFO","其他".decode("UTF-8").encode("GB18030")))
#        else:
#            d.insert(6, ("input_y_str_PAYINFO","个人产权".decode("UTF-8").encode("GB18030")))
#            d.insert(6, ("input_y_str_PAYINFO0","个人产权".decode("UTF-8").encode("GB18030")))
#            d.insert(6, ("input_str_PropertySubType","普通住宅".decode("UTF-8").encode("GB18030")))
#            d.insert(6, ("input_str_PropertySubType",""))
            
#            d.append(("input_n_str_FORWARD","南".decode("UTF-8").encode("GB18030")))
#            d.append(("input_n_str_FITMENT","精装修".decode("UTF-8").encode("GB18030")))
#            d.append(("input_n_str_BASESERVICE","煤气/天然气".decode("UTF-8").encode("GB18030")))
#            d.append(("input_n_str_BASESERVICE","暖气".decode("UTF-8").encode("GB18030")))
#            d.append(("input_n_str_BASESERVICE","电梯".decode("UTF-8").encode("GB18030")))
#            d.append(("input_n_str_BASESERVICE","车位/车库".decode("UTF-8").encode("GB18030")))
#            d.append(("input_n_str_BASESERVICE","储藏室/地下室".decode("UTF-8").encode("GB18030")))
#            d.append(("input_n_str_BASESERVICE","花园/小院".decode("UTF-8").encode("GB18030")))
#            d.append(("input_n_str_BASESERVICE","露台".decode("UTF-8").encode("GB18030")))
#            d.append(("input_n_str_BASESERVICE","阁楼".decode("UTF-8").encode("GB18030")))
#            d.append(("input_n_str_LOOKHOUSE","随时看房".decode("UTF-8").encode("GB18030")))
        d.extend(self.customimages)
        postkeys=[ c[0] for c in d ]
        ppp=PyQuery(pbpage)("inpt")
        for ipt in ppp:
            if (PyQuery(ipt).attr("name")!="" ) and (PyQuery(ipt).attr("value")!=""):
                print PyQuery(ipt).attr("name"), PyQuery(ipt).attr("value")
                #d.append((PyQuery(ipt).attr("name"), PyQuery(ipt).attr("value")))
                
        if re.search('''<inpt name="(.*)" value="(.*)"></inpt>''', pbpage):
            hdname=re.search('''<inpt name="(.*)" value="(.*)"></inpt>''', pbpage).group(1)
            hdvalue=re.search('''<inpt name="(.*)" value="(.*)"></inpt>''', pbpage).group(2)
            d.append((hdname,hdvalue))
        print "+"*60
        for ctrl in self.br.form.controls:
            if ctrl.name==None:
                continue
            if ctrl.name=="input_Hid":
                hid=self.getinput_Hid(ctrl.value)
                d.append(hid)
            
            if not ctrl.name in  postkeys:
#                print ctrl.name,ctrl.value
#                if ctrl.name=="input_y_str_COMPANYNAME":
#                    d.append(("input_y_str_COMPANYNAME",ctrl.value))
#                elif ctrl.name=="input_y_str_PRICETYPE":
#                    d.append(("input_y_str_PRICETYPE",ctrl.value))
#                else:
                nk=ctrl.name
                if ctrl.value==None:
                    nv=""
                else:
                    if type(ctrl.value)==list:
                        nv=random.choice(ctrl.value)
                    else:
                        nv=ctrl.value
                d.append((nk,nv))
        for dd in d:
            print dd
        data=urllib.urlencode(d)
        print data
        self.br.addheaders = [("Referer", "http://agents.soufun.com/magent/house/sale/saleinput.aspx")] 
        resp=self.br.open("http://agents.soufun.com/MAgent/house/InputSave.aspx?flag=2",data)
        
        
        
#        resp=self.br.submit()
        respage=resp.read().decode("GB18030")
        print respage
        if "window.location.replace" in respage :
            if re.search('''window\.location\.replace\('(.*)'\);''',respage):
                sts=re.search('''window\.location\.replace\('(.*)'\);''',respage).group(1)
                return "success|%s"%sts
            else:
                return "puterror3|%s"%"无正确相应结果"
        else:
            if re.search('''alert\('(.*)'\)''',respage):
                sts=re.search('''alert\('(.*)'\)''',respage).group(1)
                return "puterror4|%s"%sts
            else:
                return respage
       
        
#        self.br.submit()
#        resp=self.br.response().read()
#        print resp.decode("GB18030") 
        
        #UploadPic('mainform','Hfile',3,'ks','N','http%3a%2f%2fagents.soufun.com%2fMagent%2fPicInterface%2fSingleHousePicUploadFinish.aspx');
        
        
#        self.br.form.add_file(open("d:/111.jpg"), 'image/jpeg', "111.jpg", name='Hfile')
#        self.br.form.action]=
#        self.br.submit()
#        resp=self.br.response().read()
#        print resp.decode("GB18030") 
        
def makePostData(dict):
    params=""
    for item in dict.items():
        params+="&%s=%s"%(item[0],item[1])
    return  params;    
def  Publish(d):
    try:
        br=SouFangbrowser(d)
        br.goLogin()
        br.goSalePage()
        sts=""
        if d["house_kind"]=="1":
            sts=br.goPublishPage()
        else:
            sts=br.goPublishCZPage()
        return sts
    except Exception,e:
        return "%s"%e
if __name__=="__main__":
    p={  
        "username":"changna19880422",
        "passwd":"19880422",
        "webid":"3",
        "broker_id":"1111",
        "citycode":"ks",
        "house_title":"新华小区3333333",
        "city":"2",
        "cityarea_id":"1411",
        "borough_section":"5910",
        "house_type":"3",
        "house_toward":"1",
        "house_fitment":"2",
        "house_kind":"2",
        "house_deposit":"1",
        "belong":"1",
        "house_price":"500",
        "house_totalarea":"120",
        "house_room":"3",
        "house_hall":"2",
        "house_toilet":"1",
        "house_topfloor":"6",
        "house_floor":"2",
        "house_age":"10",
        "house_desc":'''新华小区3333333新华小区3333333新华小区3333333''',
        "borough_id":"10",
        "borough_name":"新华小区3333333新华小区3333333",
        "house_drawing":"",
        "house_thumb":"",
        "house_xqpic":"",
        #========================
        "mobile":"13333334444",
        "contact":"苏大生",
        
       }
    print Publish(p)