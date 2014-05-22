#coding=UTF-8
'''
Created on 2011-6-20

@author: Administrator
'''
import urllib2
import cookielib
import re
import urllib
from lxml import etree
import mimetypes
import simplejson
def makePostData(dict):
    params=""
    for item in dict.items():
        params+="&%s=%s"%(urllib.quote(item[0]),urllib.quote(item[1],safe=''))
    return  params;
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
class isRedirect(urllib2.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        e = urllib2.HTTPError(req.get_full_url(), code, msg, headers, fp)
        if e.code in (301,302):
            return True
        else:
            return False
def upload(files,hidBrokerID,comm):
    fields=[
            ('ct','text/html'),
            ('comment',comm!=None and comm or ""),
            ('rt','http://my.anjuke.com/v2/ajax/uploadcallback/'),
            ]
    ffs=files.items()
    jsons={}
    jsons["Comm"]=[]
    jsons["Model"]=[]
    jsons["Room"]=[]
    for ff in ffs:
        for ifile in ff[1]:
            imgdata= file(ifile,"rb")
            files=[
                   ('file',imgdata.name,imgdata.read())
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
            
            
            
            
            
            
#    for ifile in files:
#        imgdata= file(ifile,"rb")
#        files=[
#               ('file',imgdata.name,imgdata.read())
#               ]
#        content_type, upload_data = uploadfile(fields, files)
#        
#        uploadheader={
#                "User-Agent": "Mozilla/5.0 (Windows NT 5.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
#                'Content-Type': content_type,
#                'Content-Length': str(len(upload_data))
#                }
#        #json = urllib2.urlopen(upt[type], upload_data)
#        request = urllib2.Request("http://upd1.ajkimg.com/upload-anjuke", upload_data, uploadheader)
#        br = urllib2.build_opener()
#        json=br.open(request).read()
#        "useImgs":{"Comm":[],"Model":[],"Room":[]},#["d:\\111.jpg"],#
#        return  json
        
def publish(tp,pd):
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
    response=br.open(request).read()
    #print response
    params="act=login&loginName=%s&loginPasswd=%s&history="%(pd['name'],pd['pwd'])
    request = urllib2.Request("http://agent.anjuke.com/v2/login/",params , getheader)
    cookiestore.add_cookie_header(request)
    br = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiestore),urllib2.HTTPRedirectHandler())
    response=br.open(request).read()
    #print response
    if tp==0:
        purl="http://my.anjuke.com/v2/member/broker/property/sale/step1"
    elif tp==1:
        purl="http://my.anjuke.com/v2/member/broker/property/sale/step1"
        
    request = urllib2.Request(purl,None , getheader)
    cookiestore.add_cookie_header(request)
    br = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiestore),urllib2.HTTPRedirectHandler())
    response=br.open(request).read()
    #print response
    if re.search(hidBrokerID_regex, response):
        hidBrokerID=re.search(hidBrokerID_regex, response).group(1)
        pdict["hidBrokerID"]=hidBrokerID
        
   
   
   
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
    response=br.open(request).read()
    #print response
    
   
    
    if re.search(hidCommunityID_regex, response):
        hidCommunityIDlis=re.search(hidCommunityID_regex, response).group(1)
        try:
            lis=etree.HTML(hidCommunityIDlis).xpath("/html/body/li")
        except:
            raise Exception("name error")
        for li in lis:
            if li.xpath("span")[0].text.encode('raw_unicode_escape')==pd['txtCommunity']:
                pdict["txtCommunity"]=pd['txtCommunity']
                pdict["hidCommunityID"]=li.xpath("span")[0].get("rel")
                break
        
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

    ppd=makePostData(pdict)
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
    res = br.open(request)
    posturl=res.geturl()
    response=res.read()
    #print response
    if pflg:
        print "over"*10
        return
#    response='''new anjuke.global.multiupload('apf_id_6','haha.dodo','3','upd1.ajkimg.com','http://my.anjuke.com',{"comment":"{\"copyright\":\"anjuke\",\"name\":\"\\u5218\\u534e\",\"brokerid\":\"416203\"}"},'response.image.id+"|"+response.imgurl+"|||"+response.image.host+"|"+response.image.exif+"|"+response.image.width+"|"+response.image.height+"|"+response.image.size;','2097152','*.jpg;*.gif','8192',4,'pic','ajkimg.com','{"copyright":"anjuke","name":"\u5218\u534e","brokerid":"416203"}','200','200','0');'''
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
        print response
        fpd={}
        
        if re.search('''<input type="hidden" name="hidPubComm" id="hidPubComm" value="(.*)" /> ''', response):
            hidPubComm=re.search('''<input type="hidden" name="hidPubComm" id="hidPubComm" value="(.*)" /> ''', response).group(1)
        else: 
            hidPubComm=""
        print hidPubComm
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
            jstr=simplejson.dumps(jsons)
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
        print fpd
        print fpd["hidPubComm"]
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
        res = br.open(request)
        response=res.read()    
        print response
    


    
    
    
    
    
        
        
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
if __name__=="__main__":
    #出售
    pd1={
        "name":"changna19880422",
        "pwd":"201106",
        "txtCommunity":"兴华园",#这个必须是界面上能自动联想出的名称,否则发布不成功,代码抛出一个异常来终止代码
        #Comm小区,Model房型,室内Room
        #{"Comm":[],"Model":[],"Room":[]}
        "useImgs":{"Comm":["d:\\test.jpg"],"Model":[],"Room":[]},
        "radSaleType":"1",#//1推荐房源,2发布房源,这里有的账号没有推荐只有发布房源,代码会自动判断
        "radHouseOri":"1",#0东,1南,2西,3北,4东南,5东北,6西南,7西北,8南北,9东西
        "hidact":"save",
        "radCurrentState":"1",#租约 1是2否
        "radFitment":"91",#90毛坯,91 普通 ,92精装,93豪装
        "radUseType":"81",    #81 普通住宅 82别墅 83公寓
        "txtAreaNum":"65",#面积
        "txtExplain":"<p> 普通住宅</p>",  #描述内容
        "txtFloorNum":"13",#总楼层
        "txtHallNum":"1",#厅
        "txtHouseAge":"2005",#年
        "txtProFloor":"3",#楼层
        "txtProName":"普通住宅",#描述标题
        "txtProPrice":"100",#价格
        "txtRoomNum":"2",#室
        "txtToiletNum":"1",#卫
        "txtUserDefine":"",#备注(20字)
        
        }
    #出租
    pd2={
        "name":"changna19880422",
        "pwd":"201106",
        "useImgs":{"Comm":[],"Model":[],"Room":["d:\\test.jpg"]},
        
        
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
        "radFitment":"91",    #装修
        "radHouseOri":"1",    #朝向
        "radIsDolmus":"2",    #合租1整租2
        "radSaleType":"2",    #1推荐房源,2发布房源
        "radUseType":"81",    #81 普通住宅 82别墅 83公寓
        "txtAreaNum":"43",    #面积
        "txtCommunity":"兴华园",    
        "txtDepositNum":"3",    #押几
        "txtExplain":"<p> 兴华园</p>",    
        "txtFloorNum":"5",    
        "txtHallNum":"1",    
        "txtHouseAge":"2001",    
        "txtPayNum":"3",    #付几
        "txtProFloor":"3",    
        "txtProName":"兴华园",
        "txtProPrice":"500",    #租金(整数)
        "txtRoomNum":"1", 
        "txtToiletNum":"1",
        "txtUserDefine":"",
        }
    #tp 0 出售,tp=1出租
    tp=1
    
    publish(tp,pd2)