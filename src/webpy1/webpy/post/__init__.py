#coding=UTF-8
'''
Created on 2011-6-28

@author: Administrator
'''
import cookielib
import urllib2
import mimetypes
import os
import re
import simplejson as sj
import urllib
class MyException(Exception):
    def __init__(self, type,note):
        self.type = type
        self.note=note
    def __str__(self):
        return str("%s|%s"%(self.type,self.note))

class browser():
    def __init__(self,ppms):
#        self.br = mechanize.Browser()
        cj = cookielib.MozillaCookieJar()
        self.br=urllib2.build_opener(urllib2.HTTPHandler(),urllib2.HTTPCookieProcessor(cj),urllib2.HTTPRedirectHandler())
        
#        self.br.set_cookiejar(cj)
#        self.br.set_handle_equiv(True)
#        self.br.set_handle_gzip(False)
#        self.br.set_handle_redirect(True)
#        self.br.set_handle_referer(True)
#        self.br.set_handle_robots(False)
        
        self.pdb={}
        self.header={
            "User-Agent":'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB6.6; .NET CLR 3.5.30729)',
        }
        self.ppms=ppms
        self.errortype={
                        
                        }
        #======================================
        self.city="3"
        self.images=[]
        self.uname=""
        self.upass=""
        self.email=""
        self.concecter="李新佳"
        self.PicL=[]
        self.localArea="1411"
        self.localDiduan="5910"
        self.ObjectType="3"
        self.toward=""
        self.fitType="2"
        self.fukuanfangshi="1"
        self.title="闸北新立小区花园整间出租"
        self.xiaoqu="闸北新立小区花园整间出租"
        self.content="<SPAN id=comp-paste-div-700>闸北新立小区花园整间出租<SPAN id=comp-paste-div-700>闸北新立小区花园整间出租</SPAN></SPAN>"
        self.MinPrice="面议"
        self.area="43"
        self.jushishuru="1"
        self.huxingting="1"
        self.huxingwei="1"
        self.Floor="2"
        self.zonglouceng="33"
        self.gobalsokey_p1=""
        self.gobalsokey_p2=""
        #self.subdict={
        
    def goPublishPage(self):
        req=urllib2.Request("http://post.58.com/%s/"%self.city, None, self.header)
        self.br.open(req)
        req=urllib2.Request("http://track.58.com/referrer2.js", None, self.header)
        self.br.open(req)
        #print self.br._ua_handlers['_cookies'].cookiejar
    def goUploadPics(self):
        for pic  in self.images[0:8]:
            self.processUploadPics(pic)
        self.subdict["Pic"]="%s"%"|".join(self.PicL)
        self.subdict["PicPos"]="1"
    def goLogin(self):
        params="uname=%s&upass=%s&email=%s&typeid=0&cityid=%s"%(self.uname,self.upass,self.email,self.city)
        req=urllib2.Request("http://post.58.com/ajax/?action=userreglogin", params, self.header)
        pp=self.br.open(req).read()
        error=""
        if re.search('''{result:'0', error:'(.*)'}''', pp):
            error=re.search('''{result:'0', error:'(.*)'}''', pp).group(1)
        if error !="":
            raise Exception("loginerror|%s"%error)
    def makePostData(self,dict):
        params=""
        for item in dict.items():
            params+="&%s=%s"%(urllib.quote(item[0]),urllib.quote(item[1],safe=''))
        return  params;
    def goSubmit(self):
        fp=self.makePostData(self.subdict)
        req=urllib2.Request("http://post.58.com/%s/8/s5/submit"%self.city, fp, self.header)
        try:
            page=self.br.open(req).read()
        except Exception,e:
            return "%s|%s"%("puterror",e)
        note=""
        print page
        if '''<script>parent.window.location.href='http://my.58.com/InfoPressSuccess/?infoid='''in page:
            if re.search('''<script>parent.window.location.href='(.*)'</script></form>''', page):
                note=re.search('''<script>parent.window.location.href='(.*)'</script></form>''', page).group(1)
                return "success|%s"%(note,)
        else:
            
            if re.search('''parent\.\$\.c\.Error\.showError\('(.*)'\);''', page):
                note=re.search('''parent\.\$\.c\.Error\.showError\('(.*)'\);''', page).group(1)
                return "incomplete|%s"%(note,)
             
            elif "errorInfo.S_Message" in page:
                if re.search(''''msg':\['(.*)'\],''', page):
                    note=re.search(''''msg':\['(.*)'\],''', page).group(1)
                    if "<span class=currentMaxValue>" in note:
                        return "maxhouse|您的该账号今日可发房源数已满"
                    else:
                        return "samehouse|%s"%(note,)
            
                
                
    def uploadfile(self,fields, files):
        BOUNDARY = '----------267402204411258'
        CRLF = '\r\n'
        L = []
        for (key, value) in fields:
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="%s"' % key)
            L.append('')
            L.append(value)
        for (key, filename, value) in files:
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
            L.append('Content-Type: %s' % mimetypes.guess_type(filename)[0] or 'application/octet-stream')
            L.append('')
            L.append(value)
        L.append('--' + BOUNDARY + '--')
        L.append('')
        body = CRLF.join(L)
        content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
        return content_type, body
    def porcessGetParams(self):
        ppmkvs=self.ppms.split("&")
        for pm in ppmkvs:
            ppm=pm.split("=")
            if ppm[0]=="username":
                self.uname=ppm[1]
            elif ppm[0]=="passwd":
                self.upass=ppm[1]
            elif ppm[0]=="house_title":
                self.title=ppm[1]
            elif ppm[0]=="city":
                self.city=ppm[1]
            elif ppm[0]=="cityarea_id":
                self.localArea=ppm[1]
            elif ppm[0]=="borough_section":
                self.localDiduan=ppm[1]
            elif ppm[0]=="house_type":
                #2平房,3普通住宅,4公寓,5别墅,6其他,7商住两用
                
                house_type={"2":"平房","3":"普通住宅","4":"公寓","5":"别墅","6":"其他","7":"商住两用"}
                if not ppm[1] in house_type.keys():
                    raise Exception("nityError")
                self.gobalsokey_p1=house_type[ppm[1]]
                self.ObjectType=ppm[1]
            elif ppm[0]=="house_toward":
                self.toward=ppm[1]
            elif ppm[0]=="house_deposit":
                house_deposit=["0","1","3","8","6","7",]
                if not ppm[1] in house_deposit:
                    raise Exception("nityError")
                self.fukuanfangshi=ppm[1]
            elif ppm[0]=="house_price":
                self.MinPrice=ppm[1]
            elif ppm[0]=="house_totalarea":
                self.area=ppm[1]
            elif ppm[0]=="house_room":
                self.jushishuru=ppm[1]
                self.huxingshi=ppm[1]
            elif ppm[0]=="house_hall":
                self.huxingting=ppm[1]
            elif ppm[0]=="house_toilet":
                self.huxingwei=ppm[1]
            elif ppm[0]=="house_topfloor":
                self.zonglouceng=ppm[1]
            elif ppm[0]=="house_floor":
                self.Floor=ppm[1]
            elif ppm[0]=="house_age":
                pass
            elif ppm[0]=="house_desc":
                self.content=ppm[1]
            elif ppm[0]=="house_fitment":
                house_fitment={"1":"毛坯","2":"简单装修","3":"中等装修","4":"精装修","5":"豪华装修",}
                if not ppm[1] in house_fitment.keys():
                    raise Exception("nityError")
                self.fitType=ppm[1]
                self.gobalsokey_p2=house_fitment[ppm[1]]
            elif ppm[0]=="borough_id":
                pass
            elif ppm[0]=="borough_name":
                self.xiaoqu=ppm[1]
            elif ppm[0]=="house_drawing" or ppm[0]=="house_thumb" or ppm[0]=="house_xqpic":
                for img in ppm[1].split("|"):
                    if img=="":
                        continue
                    self.images.append(img)
            
        self.subdict={
             "area":self.area,
             "backFunction":"$.c.Uploader.finish",
             "busdistance":"",
             "Content":urllib.unquote(self.content),
             "daxue":"",
             "distancetime":"",
             "ditiexian":"",
             "ditiezhan":"",
             "dizhi":"",
             "fileUploadInput":"filename="" Content-Type: application/octet-stream",
             "FitType":self.fitType,
             "Floor":self.Floor,
             "fukuanfangshi":self.fukuanfangshi,
             "gobalsokey":"%s居室,%s居,%s室|%s层,%s楼|%s|%s"%(self.jushishuru,self.jushishuru,self.jushishuru,self.Floor,self.Floor,self.gobalsokey_p1,self.gobalsokey_p2),
             "goblianxiren":"%s"%self.concecter,
             "gongjiaoxian":"",
             "gongjiaozhan":"",
             "hiddenTextBoxJoinValue":"%s:%s:%s:%s"%(self.xiaoqu,"",self.MinPrice=="" and "面议" or self.MinPrice,self.concecter),
             "HireType":"2",
             "HouseAllocation":"6",
             "HouseAllocation":"8",
             "huxingshi":self.huxingshi,
             "huxingting":self.huxingting,
             "huxingwei":self.huxingwei,
             "jushishuru":self.jushishuru,
             "localArea":"%s"%self.localArea,
             "localDiduan":"%s"%self.localDiduan,
             "MinPrice":self.MinPrice,
             "ObjectType":self.ObjectType,
             "Phone":"13425147896",
             "PicDesc":"",
             "PicPos":"0",
             "postRegLogin":"0",
             "radioHasAccount":"1",
             "stationdistance":"",
             "Title":self.title,
             "Toward":self.toward,
             "xianluzhoubian":"",
             "xiaoqu":self.xiaoqu,
             "zonglouceng":self.zonglouceng,
             
             }    
                
                
        print  self.subdict       
                
                
    def getCityarea_id(self,caid):
        return "1411"
    def getBorough_section(self,bs):
        return "5910"
    def processUploadPics(self,pic):
        #self.br.handlers[6].cookiejar
        publishdict={
                 "area":"",
                 "backFunction":"$.c.Uploader.finish",
                 "busdistance":"",
                 "Content":"例如对求租者的要求，房间情况，附近环境，周边配套信息…",
                 "daxue":"",
                 "distancetime":"",
                 "ditiexian":"",
                 "ditiezhan":"",
                 "dizhi":"",
                 "FitType":"2",
                 "Floor":"",
                 "fukuanfangshi":"1",
                 "goblianxiren":"",
                 "gongjiaoxian":"",
                 "gongjiaozhan":"",
                 "HireType":"2",
                 "HouseAllocation":"6",
                 "HouseAllocation":"8",
                 "huxingshi":"",
                 "huxingting":"",
                 "huxingwei":"",
                 "jushishuru":"",
                 "localArea":"",
                 "localDiduan":"",
                 "MinPrice":"面议",
                 "ObjectType":"3",
                 "Phone":"",
                 "Pic":"",
                 "PicDesc":"",
                 "PicPos":"1",
                 "postRegLogin":"1",
                 "stationdistance":"",
                 "Title":"",
                 "Toward":"",
                 "xianluzhoubian":"",
                 "xiaoqu":"",
                 "zonglouceng":"",
                 }
        imgdata= file(pic,"rb")
        files=[
               ('fileUploadInput',os.path.basename(pic),imgdata.read())
               ]
        content_type, upload_data = self.uploadfile(publishdict.items(), files)
        uploadheader={
                "User-Agent": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB6.6; .NET CLR 3.5.30729)",
                'Content-Type': content_type,
                'Content-Length': str(len(upload_data))
                }
        req = urllib2.Request("http://post.58.com/upload", upload_data, uploadheader)
        page=self.br.open(req).read()
        if re.search(r'''finish\(\d, '(.*)', \d\);''', page):
            self.PicL.append(re.search(r'''finish\(\d, '(.*)', \d\);''', page).group(1))
            
            
def Publish(p):
    try:
        br=browser(p)
        br.porcessGetParams()
        br.goPublishPage()
        br.goUploadPics()
        br.goLogin()
        sts=br.goSubmit()  
        return sts  
    except Exception,e:
        return str(e)
        
if __name__=="__main__":
    content="%3Cspan%20id%3D%22comp-paste-div-700%22%3E%E5%A5%BD%E6%88%BF%E6%B2%B3%E7%95%94%E8%8A%B1%E5%9B%AD%E4%BA%8C%E6%9C%9F%E5%A5%BD%E5%93%88%E5%93%88%E5%93%A6%E5%91%B5%E5%91%B5%E4%BA%86%E8%A7%A3%E4%BA%86%E8%A7%A3%3Cspan%20_moz_dirty%3D%22%22%20style%3D%22color%3Ared%22%3E%E5%9B%AD%E6%95%B4%E9%97%B4%E5%87%BA%E7%A7%9F%3C/span%3E%3Cspan%20id%3D%22comp-paste-div-700%22%3E%E5%A5%BD%E6%88%BF%E6%B2%B3%E7%95%94%E8%8A%B1%E5%9B%AD%E4%BA%8C%E6%9C%9F%E5%A5%BD%E5%93%88%E5%93%88%E5%93%A6%E5%91%B5%E5%91%B5%E4%BA%86%E8%A7%A3%E4%BA%86%E8%A7%A3%3C/span%3E%3C/span%3E"
    p="username=justtestpublish2&passwd=6279115590&webid=8&broker_id=1111&house_title=人华的东方图看看&city=3&cityarea_id=1411&borough_section=5910&house_type=3&house_toward=1&house_fitment=2&house_kind=1&house_deposit=1&belong=1&house_price=512.23&house_totalarea=43&house_room=1&house_hall=2&house_toilet =3&house_topfloor=5&house_floor=5&house_age=2001&house_desc=%3CSPAN%20id%3Dcomp-paste-div-700%3E%3Cfont%20color%3D%27red%27%3E%E4%B8%9C%E6%96%B9%E4%BA%BA%E5%8D%8E%E7%9A%84%E5%9B%BE%E7%9C%8B%E7%9C%8B%E4%B8%9C%E6%96%B9%E4%BA%BA%E5%8D%8E%E7%9A%84%E5%9B%BE%E7%9C%8B%E7%9C%8B%E4%B8%9C%E6%96%B9%E4%BA%BA%E5%8D%8E%E7%9A%84%E5%9B%BE%E7%9C%8B%E7%9C%8B%E4%B8%9C%E6%96%B9%E4%BA%BA%E5%8D%8E%E7%9A%84%E5%9B%BE%E7%9C%8B%E7%9C%8B%E4%B8%9C%E6%96%B9%E4%BA%BA%E5%8D%8E%E7%9A%84%E5%9B%BE%E7%9C%8B%E7%9C%8B%3C/font%3E%3C/SPAN%3E&borough_id=10&borough_name=人华的东方图看看&house_drawing=d:/111.jpg&house_thumb=d:/111.jpg&house_xqpic=d:/111.jpg"
    print Publish(p)
#    br=browser(p)
#    br.porcessGetParams()
#    br.goPublishPage()
#    br.goUploadPics()
#    br.goLogin()
#    br.goSubmit()