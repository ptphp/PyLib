# coding=gbk
import re
import string,urlparse
import os.path as osp

nums         = string.digits

# 清除html代码里的多余空格
def clearBlank(html):
    if not html or html == None : return ;
    html = re.sub('\r|\n|\t','',html)
    html = html.replace('&nbsp;','').replace('  ','').replace('\'','"')
    return html
def clearInfo(html):
    if not html or html == None : return ;    
    html = re.sub('打电话给我时，请一定说明在.*?网看到的，谢谢！|发布日期：.*?<br />|<a .*?>|\[呼叫\]|</a>|<p .*?>','',html).replace('百姓','快速租赁网')
    return html

# html代码截取函数
def rects(html,regx,cls=''):
    if not html or html == None or len(html)==0 : return ;
    # 正则表达式截取
    if regx[:1]==chr(40) and regx[-1:]==chr(41) :
        reHTML = re.search(regx,html,re.I)
        if reHTML == None : return 
        reHTML = reHTML.group()
        intRegx = re.search(regx,reHTML,re.I)
        R = reHTML[intRegx]
    # 字符串截取
    else :        
        # 取得字符串的位置
        pattern =re.compile(regx.lower())
        intRegx=pattern.findall(html.lower()) 
        # 如果搜索不到开始字符串，则直接返回空
        if not intRegx : return 
        R = intRegx
    # 清理内容
    if cls:
        RC = []
        for item in R:
            RC.append(resub(item,cls))            
        return RC
    else:
        return R
    
def rect(html,regx,cls=''):
    #regx = regx.encode('utf-8')
    if not html or html == None or len(html)==0 : return ;
    # 正则表达式截取
    if regx[:1]==chr(40) and regx[-1:]==chr(41) :
        reHTML = re.search(regx,html,re.I)
        if reHTML == None : return 
        reHTML = reHTML.group()
        intRegx = re.search(regx,reHTML,re.I)
        R = reHTML[intRegx]
    # 字符串截取
    else :        
        # 取得字符串的位置
        pattern =re.compile(regx.lower())
        intRegx=pattern.findall(html) 
        # 如果搜索不到开始字符串，则直接返回空
        if not intRegx : return 
        R = intRegx[0]
    if cls:
        R = resub(R,cls)
    # 返回截取的字符
    return R
# 正则清除
def resub(html,regexs):
    if not regexs: return html
    html  =re.sub(regexs,'',html)
    return html
def rereplace(html,regexs):
    if not regexs: return html
    html  =html.repalce(regexs,'')
    return html
#跳转电话URL
def telPageReplace(url):
    telUrl=url.split('/')
    finalUrl="phone_%s" % telUrl[len(telUrl)-1]
    return url.replace(telUrl[len(telUrl)-1],finalUrl)
#判断数字
def check(a):
    if type(a) is not str:
        return False
    else:
        for i in a:
            if i not in nums:
                return False
        return True
#判断电话
def parseNum(a):
    strs=''
    if type(a) is not str:
        return 0
    else:        
        for i in a:
            if i in nums or i == '.':
                strs +=i                
        return strs
def reTel(str,regx):
    #regx = '((13[0-9]|15[0-9]|18[89])\\d{8})'
    p = re.compile(regx)
    #print p
    if p.findall(str):
        return p.findall(str)[0]
    else:
        regx = '((13[0-9]|15[0-9]|18[89])\d{8})'
        #regx = '(13[0-9]|15[0-9]|18[89])\d{8}'
        res = re.search(regx,str).group()
        if res:
            return res
        else:
            return ''

def matchURL(tag,url):
    print tag
    print url
    urls = re.findall('(.*)(src|href)=(.+?)( |/>|>).*|(.*)url\(([^\)]+)\)',tag,re.I)
    if urls == None :
        return tag
    else :
        if urls[0][5] == '' :
            urlQuote = urls[0][2]
        else:
            urlQuote = urls[0][5]

    if len(urlQuote) > 0 :
        cUrl = re.sub('''['"]''','',urlQuote)
    else :
        return tag

    urls = urlparse(url); scheme = urls[0];
    if scheme!='' : scheme+='://'
    host = urls[1]; host = scheme + host
    if len(host)==0 : return tag
    path = osp.dirname(urls[2]);
    if path=='/' : path = '';
    if cUrl.find("#")!=-1 : cUrl = cUrl[:cUrl.find("#")]
    # 判断类型
    if re.search('''^(http|https|ftp):(//|\\\\)(([\w/\\\+\-~`@:%])+\.)+([\w/\\\.\=\?\+\-~`@':!%#]|(&amp;)|&)+''',cUrl,re.I) != None :
        # http开头的url类型要跳过
        return tag
    elif cUrl[:1] == '/' :
        # 绝对路径
        cUrl = host + cUrl
    elif cUrl[:3]=='../' :
        # 相对路径
        while cUrl[:3]=='../' :
            cUrl = cUrl[3:]
            if len(path) > 0 :
                path = osp.dirname(path)
    elif cUrl[:2]=='./' :
        cUrl = host + path + cUrl[1:]
    elif cUrl.lower()[:7]=='mailto:' or cUrl.lower()[:11]=='javascript:' :
        return tag
    else :
        cUrl = host + path + '/' + cUrl
    R = tag.replace(urlQuote,'"' + cUrl + '"')
    return R

def urlencode(str) :
    str=str.decode('utf-8').encode('utf-8')
    reprStr = repr(str).replace(r'\x', '%')
    return reprStr[1:-1]
                
    