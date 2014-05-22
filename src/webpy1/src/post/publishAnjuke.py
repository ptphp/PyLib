#coding=UTF-8
'''
Created on 2011-7-1

@author: Administrator
'''
import cookielib
import urllib2
import urllib
import mimetypes
import simplejson as sj
import re
from lxml import etree
import os
import time
from BeautifulSoup import BeautifulSoup
#from log.dubug import *
picRoot = ""#/home/wwwroot/jjr360v1.1/site.jjr.com/upfile/"
def makePostData(dict):
    params=""
    for item in dict.items():
        params+="&%s=%s"%(urllib.quote(item[0]),urllib.quote(item[1],safe=''))
    return  params;
def uploadfile(fields, files):
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
def upload(files,hidBrokerID,comm):
    fields=[
            ('ct','text/html'),
            ('comment',comm!="" and comm or ""),
            ('rt','http://my.anjuke.com/v2/ajax/uploadcallback/'),
            ]
    ffs=files.items()
    jsons={}
    jsons["Comm"]=[]
    jsons["Model"]=[]
    jsons["Room"]=[]
    for ff in ffs:
        for ifile in ff[1]:
            imgdata= file(picRoot+ifile,"rb")
            files=[
                   ('file',os.path.basename(imgdata.name),imgdata.read())
                   ]
            content_type, upload_data = uploadfile(fields, files)
            
            uploadheader={
                    "User-Agent": "Mozilla/5.0 (Windows NT 5.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
                    'Content-Type': content_type,
                    'Content-Length': str(len(upload_data))
                    }
            #json = urllib2.urlopen(upt[type], upload_data)
            request = urllib2.Request("http://upd1.ajkimg.com/upload-anjuke", upload_data, uploadheader)
            br = urllib2.build_opener()
            json=br.open(request).read()
            #"useImgs":{"Comm":[],"Model":[],"Room":[]},#["d:\\111.jpg"],#
            jsons[ff[0]].append(json)
            
            
    return jsons
def makeSavePicsPostData(jsons):
    jss=jsons.items()
    dd={}
    
    for js in jss:
        jssl=[]
        for j in js[1]:
            jsn=makeSavePicPostData(j)
            jssl.append(jsn)
        dd.update({"hidNewUpd%s"%js[0]:",".join(jssl)})
    return dd
def makeSavePicPostData(json):
    json=json.replace("&quot;","\"")
    rj_reg='''a:8:\{(.*)\}"'''
    if re.search(rj_reg, json):
        rj=re.search(rj_reg, json).group(1)
    else: 
        rj=""
    id_reg='''"id":"([a-z0-9]+)",'''
    if re.search(id_reg, json):
        id=re.search(id_reg, json).group(1)
    else: 
        id=""
    rj=rj.replace("\\\"", "\"")
    st='''%s|http://pic1.ajkimg.com/display/%s/100x75.jpg|||1|a:8:{%s}|600|400|23890|0'''%(id,id,rj)
    return st
def ProcessPublish(pd,iss):
    #print pd 
    if len(pd.items())==21:
        tp=0
    else:
        tp=1
    cookiestore=cookielib.MozillaCookieJar()
    hidBrokerID_regex='''<input type="hidden" name="hidBrokerID" value="(\d+)" />'''
    hidCommunityID_regex="<ul>([\s\S]*?)</ul>"
    pdict={
           
           }
    #login
    getheader={
               "User-Agent": "Mozilla/5.0 (Windows NT 5.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
               }
    request = urllib2.Request("http://agent.anjuke.com/v2/login/", None, getheader)
    cookiestore.add_cookie_header(request)
    br = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiestore))
    try:
        br.open(request)
    except:
        return "puterror|链接超时！"
    #print response
    params="act=login&loginName=%s&loginPasswd=%s&history="%(pd['name'],pd['pwd'])
    request = urllib2.Request("http://agent.anjuke.com/v2/login/",params , getheader)
    cookiestore.add_cookie_header(request)
    br = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiestore),urllib2.HTTPRedirectHandler())
    try:
        response=br.open(request).read()
    except:
        return "puterror|链接超时！"
     
    #print response
    if '''<h1>错误提示</h1>''' in response:
        return "loginerror|登陆有误！"
#    else:
#        if not '''<title>中国网络经纪人 - 我的首页</title>''' in response:
#            return "loginerror|登陆有误2！"
    
    if tp==0:
        purl="http://my.anjuke.com/v2/member/broker/property/sale/step1"
    elif tp==1:
        purl="http://my.anjuke.com/v2/member/broker/property/sale/step1"
        
    request = urllib2.Request(purl,None , getheader)
    cookiestore.add_cookie_header(request)
    br = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiestore),urllib2.HTTPRedirectHandler())
    try:
        response=br.open(request).read()
    except:
        return "puterror|链接超时！"
    #print response
    pdict["hidBrokerID"]=""
    if re.search(hidBrokerID_regex, response):
        hidBrokerID=re.search(hidBrokerID_regex, response).group(1)
        pdict["hidBrokerID"]=hidBrokerID
    if  pdict["hidBrokerID"]=="":
#        makeLog("hidBrokerID is null","line 161")
        return "puterror|参数错误3！"
   
   
   
    pdict["radSaleType"]=pd["radSaleType"]
    if re.search('''<input type="radio" (.*) />''', response):
        radios=re.findall(r'''<input type="radio" (.*) />''', response)
        if "disabled" in radios[0]:
            pdict["radSaleType"]="2"
        elif "disabled" in radios[1]:
            pdict["radSaleType"]="1"
   
    request = urllib2.Request("http://my.anjuke.com/v2/ajax/community/list/W0QQiframeidZifrCommunityListQQhidcommidZhidCommunityIDQQcommunityidZtxtCommunityQQcityidZ40QQkwZ%s"%urllib.quote(pd['txtCommunity']),None , getheader)
    cookiestore.add_cookie_header(request)
    br = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiestore),urllib2.HTTPRedirectHandler())
    try:
        response=br.open(request).read()
    except:
        return "puterror|链接超时！"
    #print response
    
   
    
    if re.search(hidCommunityID_regex, response):
        hidCommunityIDlis=re.search(hidCommunityID_regex, response).group(1)
        try:
            #lis=etree.HTML(hidCommunityIDlis).xpath("/html/body/li")
            hidCommunityIDlis=re.search(hidCommunityID_regex, response).group(1)
            soup = BeautifulSoup(hidCommunityIDlis)
            lis = soup('li')
        except:
            raise Exception("nityError|对方没有匹配小区")
        pdict["txtCommunity"]=""
        pdict["hidCommunityID"]=""
        print lis
        for li in lis:
#            makeLog(li.xpath("span")[0].text.encode('raw_unicode_escape').encode("UTF-8"),"line 194")
#            makeLog(pd['txtCommunity'],"line 194")
#            makeLog( pd['txtCommunity'] in li.xpath("span")[0].text.encode('raw_unicode_escape').encode("UTF-8"),"line 194")
            
            #if li.xpath("span")[0].text.encode('raw_unicode_escape')==unicode(pd['txtCommunity']):
            #if pd['txtCommunity'] in li.xpath("span")[0].text.encode('raw_unicode_escape').encode("UTF-8"):
            if pd['txtCommunity'] in li.span.string:
                #pdict["txtCommunity"]=li.xpath("span")[0].text.encode('raw_unicode_escape')#pd['txtCommunity']
                #pdict["hidCommunityID"]=li.xpath("span")[0].get("rel")
                pdict["txtCommunity"]=li.span.string#pd['txtCommunity']
                pdict["hidCommunityID"]=li.span['rel']
                break
    
    pdict["txtCommunity"]="绿地启航社"#pd['txtCommunity']
    pdict["hidCommunityID"] = 310398
    if pdict["txtCommunity"]=="" or pdict["hidCommunityID"]=="":
#        makeLog("can not fetch txtCommunity  or hidCommunityID ","line 199")
        return "puterror|参数错误4！"
    
    pdict["hidact"]=pd["hidact"]
    if tp==0:
        pdict["radCurrentState"]=pd["radCurrentState"]
    if tp==1:
        pdict["txtPayNum"]=pd["txtPayNum"]
        pdict["txtDepositNum"]=pd["txtDepositNum"]
        pdict["chkHaveElect"]=pd["chkHaveElect"]
        pdict["chkHaveGas"]=pd["chkHaveGas"]
        pdict["chkHaveWater"]=pd["chkHaveWater"]
        pdict["chkHaveWarm"]=pd["chkHaveWarm"]
        pdict["chkHaveTv"]=pd["chkHaveTv"]
        pdict["chkHaveBroad"]=pd["chkHaveBroad"]
        pdict["chkHaveTvbox"]=pd["chkHaveTvbox"]
        pdict["chkHaveRefr"]=pd["chkHaveRefr"]
        pdict["chkHaveAir"]=pd["chkHaveAir"]
        pdict["chkHaveWash"]=pd["chkHaveWash"]
        pdict["chkHaveHotwater"]=pd["chkHaveHotwater"]
        pdict["chkHaveMicro"]=pd["chkHaveMicro"]
        pdict["chkHaveTel"]=pd["chkHaveTel"]
        
     
    pdict["radFitment"]=pd["radFitment"]
    pdict["radHouseOri"]=pd["radHouseOri"]
    
    pdict["radUseType"]=pd["radUseType"]
    pdict["txtAreaNum"]=pd["txtAreaNum"]
    pdict["txtExplain"]=pd["txtExplain"]
    pdict["txtFloorNum"]=pd["txtFloorNum"]
    pdict["txtHallNum"]=pd["txtHallNum"]
    pdict["txtHouseAge"]=pd["txtHouseAge"]
    pdict["txtProFloor"]=pd["txtProFloor"]
    pdict["txtProName"]=pd["txtProName"]
    pdict["txtProPrice"]=pd["txtProPrice"]
    pdict["txtRoomNum"]=pd["txtRoomNum"]
    pdict["txtToiletNum"]=pd["txtToiletNum"]
    pdict["txtUserDefine"]=pd["txtUserDefine"]
    
    
    if len(pd["useImgs"]["Comm"])==0 and len(pd["useImgs"]["Model"])==0 and len(pd["useImgs"]["Room"])==0:
        pflg=True
    else:
        pdict["chkUploadPic"]="1"
        pflg=False

    ppd=urllib.urlencode(pdict)
    pheader={
             "User-Agent": "Mozilla/5.0 (Windows NT 5.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
           'Content-Type': "application/x-www-form-urlencoded",
           'Content-Length': str(len(ppd))
             }
    #request = urllib2.Request("http://my.anjuke.com/v2/user/broker/property/sale/step1",ppd , pheader)
    if tp==0:
        puburl="http://my.anjuke.com/v2/member/broker/property/sale/step1"
    elif tp==1 :
        puburl="http://my.anjuke.com/v2/member/broker/property/rent/step1"
    request = urllib2.Request(puburl,ppd , pheader)
    
    cookiestore.add_cookie_header(request)
    br = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiestore),urllib2.HTTPRedirectHandler())
    #response=br.open(request).read()
    print response
    try:
        res = br.open(request)
    except:
        return "puterror|链接超时！"
    posturl=res.geturl()
    response=res.read()
    #print response
    if pflg:
        if '''src="http://static.anjuke.com/images/right1.gif" /> 发布成功！</p>''' in response:
            if iss:
                manUrl = "http://my.anjuke.com/v2/member/brokerpropmanage/W0QQactZsale#proptop"
            else:
                manUrl = "http://my.anjuke.com/v2/member/brokerpropmanage/W0QQactZrent"
            return "success|%s"%manUrl
        else:
            return "puterror|发布失败"
#    response='''new anjuke.global.multiupload('apf_id_6','haha.dodo','3','upd1.ajkimg.com','http://my.anjuke.com',{"comment":"{\"copyright\":\"anjuke\",\"name\":\"\\u5218\\u534e\",\"brokerid\":\"416203\"}"},'response.image.id+"|"+response.imgurl+"|||"+response.image.host+"|"+response.image.exif+"|"+response.image.width+"|"+response.image.height+"|"+response.image.size;','2097152','*.jpg;*.gif','8192',4,'pic','ajkimg.com','{"copyright":"anjuke","name":"\u5218\u534e","brokerid":"416203"}','200','200','0');'''
    comment=""
    if re.search('''{"comment":"({.*})"}''', response):
        comment=re.search('''{"comment":"({.*})"}''', response).group(1)
#        print comment
   
   
   
    #############
    if not  pflg :
        jsons=upload(pd["useImgs"],hidBrokerID,comment.replace("\\\"", "\"").replace("\\\\", "\\"))
#        q=urllib.quote(json.replace("&quot;","\""))
#        url="http://my.anjuke.com/v2/ajax/uploadcallback/?q="+q
#        request = urllib2.Request(url,None , getheader)
#        cookiestore.add_cookie_header(request)
#        br = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiestore),urllib2.HTTPRedirectHandler())
#        response=br.open(request).read()
        #print response
        fpd={}
        
        if re.search('''<input type="hidden" name="hidPubComm" id="hidPubComm" value="(.*)" /> ''', response):
            hidPubComm=re.search('''<input type="hidden" name="hidPubComm" id="hidPubComm" value="(.*)" /> ''', response).group(1)
        else: 
            hidPubComm=""
        #print hidPubComm
        fpd["hidPubComm"]= hidPubComm
        fpd["hidPubModel"]= ""
        fpd["hidSelComm"]= ""
        fpd["hidSelModel"]= ""    
        fpd["hidUpdComm"]= ""
        fpd["hidUpdModel"]= ""
        fpd["hidUpdRoom"]= ""
        fpd["hidact"]= "savepic"
        fpd["isback"]= "notback"
        fpd["hidDefaultImgID"]= "0"
        fpd["hidDelComm"]= ""
        fpd["hidDelModel"]= ""
        fpd["hidDelRoom"]= ""
        fpd["hidNewUpdComm"]= ""  
        if tp==1:
            jstr=sj.dumps(jsons)
            jstr=jstr.replace("&quot;","\"")
            id_reg='''"id":"([a-z0-9]+)",'''
            if re.search(id_reg, jstr):
                id=re.search(id_reg, jstr).group(1)
            else: 
                id=""
            fpd["markact"]= "ok"
            fpd["txtDesc[%s]"%id]= ""
            fpd["dropDesc[%s]"%id]= ""
        
        dd=makeSavePicsPostData(jsons)
        fpd.update(dd)
#        #小区
#        fpd["hidNewUpdComm"]=""  
#        #房型
#        fpd["hidNewUpdModel"]=""
#        #室内
#        fpd["hidNewUpdRoom"]= makeSavePicPostData(json)
        #print fpd
        #print fpd["hidPubComm"]
        fps=makePostData(fpd)
        pheader={
             "User-Agent": "Mozilla/5.0 (Windows NT 5.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
           'Content-Type': "application/x-www-form-urlencoded",
           'Content-Length': str(len(fps))
             }
        request = urllib2.Request(posturl,fps , pheader)
        cookiestore.add_cookie_header(request)
        br = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiestore),urllib2.HTTPRedirectHandler())
        #response=br.open(request).read()
        try:
            res = br.open(request)
        except:
            return "puterror|链接超时！"
        response=res.read()    
        if '''src="http://static.anjuke.com/images/right1.gif" /> 发布成功！</p>'''  in response:
            if iss:
                manUrl = "http://my.anjuke.com/v2/member/brokerpropmanage/W0QQactZsale#proptop"
            else:
                manUrl = "http://my.anjuke.com/v2/member/brokerpropmanage/W0QQactZrent"
            return "success|%s"%manUrl
        else:
            return "puterror|发布失败！"
    

def doProcessParams(d):
    p={}
    isSell=False
    house_age="5"
    try:
        if len(d["house_age"])!=4:
            Y=int(time.strftime('%Y', time.localtime()))
            house_age="%s"%(Y-int(d["house_age"]))
    except Exception,e:
        #makeLog(e,"line 352")
        pass
    house_drawing =[]
    house_thumb=[]
    house_xqpic =[]
    for pic1 in d.get("house_drawing").split("|"):
        if pic1=="":
            continue
        house_drawing.append(pic1)
    for pic1 in d.get("house_thumb").split("|"):
        if pic1=="":
            continue
        house_thumb.append(pic1)
    for pic1 in d.get("house_xqpic").split("|"):
        if pic1=="":
            continue
        house_xqpic.append(pic1)
    if d["house_kind"]=="1":
        isSell=True
        p={
        "name":d["username"],
        "pwd":d["passwd"],
        "txtCommunity":d["borough_name"],#这个必须是网页上能自动联想出的名称,否则发布不成功,代码抛出一个异常来终止代码
        
        #Comm小区,Model房型,室内Room
        #{"Comm":[],"Model":[],"Room":[]}
        "useImgs":{"Comm":house_xqpic,"Model":house_drawing,"Room":house_thumb},
        "radSaleType":"1",#//1推荐房源,2发布房源,这里有的账号没有推荐只有发布房源,代码会自动判断
        "radHouseOri":d["house_toward"] in ["0","1","2","3","4","5","6","7","8","9"] and d["house_toward"] or "1",#0东,1南,2西,3北,4东南,5东北,6西南,7西北,8南北,9东西
        "hidact":"save",
        "radCurrentState":"2",#租约 1是2否
        "radFitment":d["house_fitment"] in ["90","91","92","93",] and d["house_fitment"] or "91",#90毛坯,91 普通 ,92精装,93豪装
        "radUseType":d["house_type"] in ["81","82","83",] and d["house_type"]or   "81",    #81 普通住宅 82别墅 83公寓
        "txtAreaNum":d["house_totalarea"],#面积
        "txtExplain":"<p> %s</p>"%d["house_desc"],  #描述内容
        "txtFloorNum":d["house_topfloor"],#总楼层
        "txtHallNum":d["house_hall"],#厅
        "txtHouseAge":house_age,#年
        "txtProFloor":d["house_floor"],#楼层
        "txtProName":d["house_title"],#描述标题
        "txtProPrice":d["house_price"],#价格
        "txtRoomNum":d["house_room"],#室
        "txtToiletNum":d["house_toilet"],#卫
        "txtUserDefine":"",#备注(20字)
        
        }
    else:
        if d["house_deposit"] == "1":
            ya="1"
            fu="3"
        elif d["house_deposit"] == "3":
            ya="1"
            fu="1"
        elif d["house_deposit"] == "8":
            ya="2"
            fu="1"
        elif d["house_deposit"] == "6":
            ya="1"
            fu="6"
        elif d["house_deposit"] == "7":
            ya="1"
            fu="12"
        else:
            ya="1"
            fu="3"
        
        p={
        "name":d["username"],
        "pwd":d["passwd"],
        "useImgs":{"Comm":house_xqpic,"Model":house_drawing,"Room":house_thumb},
        "chkHaveElect":"1",#有电
        "chkHaveGas":"1",#有气
        "chkHaveWater":"1",#有水
        "chkHaveWarm":"",   #暖气
        "chkHaveTv":"", #有线电视
        "chkHaveBroad":"", #宽带
        "chkHaveTvbox":"", #电视机
        "chkHaveRefr":"", #冰箱
        "chkHaveAir":"", #空调
        "chkHaveWash":"", #洗衣机
        "chkHaveHotwater":"", #热水器
        "chkHaveMicro":"", #微波炉
        "chkHaveTel":"", #电话
        "hidact":"save",    
        "radFitment":d["house_fitment"] in ["90","91","92","93",] and d["house_fitment"] or "91",    #装修
        "radHouseOri":d["house_toward"] in ["0","1","2","3","4","5","6","7","8","9"] and d["house_toward"] or "1",    #朝向
        "radIsDolmus":"2",    #合租1整租2
        "radSaleType":"1",    #1推荐房源,2发布房源
        "radUseType":d["house_type"] in ["81","82","83",] and d["house_type"]or   "81",    #81 普通住宅 82别墅 83公寓
        "txtAreaNum":d["house_totalarea"],    #面积
        "txtCommunity":d["borough_name"],    
        "txtDepositNum":ya,    #押几
        "txtExplain":"<p> %s</p>"%d["house_desc"],    
        "txtFloorNum":d["house_topfloor"],    
        "txtHallNum":d["house_hall"],    
        "txtHouseAge":house_age,    
        "txtPayNum":fu,    #付几
        "txtProFloor":d["house_floor"],    
        "txtProName":d["house_title"],
        "txtProPrice":d["house_price"],    #租金(整数)
        "txtRoomNum":d["house_room"], 
        "txtToiletNum":d["house_toilet"],
        "txtUserDefine":"",
        }
    return p ,isSell
def Publish(p):
    try:
        pp,iss=doProcessParams(p)
        sts=ProcessPublish(pp,iss)
        return sts
    except Exception,e:
        return str(e)
if __name__=="__main__":
    
    p={
        "username":"changna19880422",
        "passwd":"201106",
        "webid":"8",
        "broker_id":"1111",
        "house_title":"昆山花园",
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
        "house_desc":'''昆山花园昆山花园昆山花园昆山花园''',
        "borough_id":"10",
        "borough_name":"绿地启航社",
        "house_drawing":"",
        "house_thumb":"",
        "house_xqpic":"",
        #========================
        "mobile":"111",
        "contact":"苏大生",
        
       }
    print Publish(p)