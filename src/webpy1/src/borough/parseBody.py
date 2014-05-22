# coding=gbk
import re
import string,urlparse
import os.path as osp

nums         = string.digits

# ���html������Ķ���ո�
def clearBlank(html):
    if not html or html == None : return ;
    html = re.sub('\r|\n|\t','',html)
    html = html.replace('&nbsp;','').replace('  ','').replace('\'','"')
    return html
def clearInfo(html):
    if not html or html == None : return ;    
    html = re.sub('��绰����ʱ����һ��˵����.*?�������ģ�лл��|�������ڣ�.*?<br />|<a .*?>|\[����\]|</a>|<p .*?>','',html).replace('����','����������')
    return html

# html�����ȡ����
def rects(html,regx,cls=''):
    if not html or html == None or len(html)==0 : return ;
    # ������ʽ��ȡ
    if regx[:1]==chr(40) and regx[-1:]==chr(41) :
        reHTML = re.search(regx,html,re.I)
        if reHTML == None : return 
        reHTML = reHTML.group()
        intRegx = re.search(regx,reHTML,re.I)
        R = reHTML[intRegx]
    # �ַ�����ȡ
    else :        
        # ȡ���ַ�����λ��
        pattern =re.compile(regx.lower())
        intRegx=pattern.findall(html.lower()) 
        # �������������ʼ�ַ�������ֱ�ӷ��ؿ�
        if not intRegx : return 
        R = intRegx
    # ��������
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
    # ������ʽ��ȡ
    if regx[:1]==chr(40) and regx[-1:]==chr(41) :
        reHTML = re.search(regx,html,re.I)
        if reHTML == None : return 
        reHTML = reHTML.group()
        intRegx = re.search(regx,reHTML,re.I)
        R = reHTML[intRegx]
    # �ַ�����ȡ
    else :        
        # ȡ���ַ�����λ��
        pattern =re.compile(regx.lower())
        intRegx=pattern.findall(html) 
        # �������������ʼ�ַ�������ֱ�ӷ��ؿ�
        if not intRegx : return 
        R = intRegx[0]
    if cls:
        R = resub(R,cls)
    # ���ؽ�ȡ���ַ�
    return R
# �������
def resub(html,regexs):
    if not regexs: return html
    html  =re.sub(regexs,'',html)
    return html
def rereplace(html,regexs):
    if not regexs: return html
    html  =html.repalce(regexs,'')
    return html
#��ת�绰URL
def telPageReplace(url):
    telUrl=url.split('/')
    finalUrl="phone_%s" % telUrl[len(telUrl)-1]
    return url.replace(telUrl[len(telUrl)-1],finalUrl)
#�ж�����
def check(a):
    if type(a) is not str:
        return False
    else:
        for i in a:
            if i not in nums:
                return False
        return True
#�жϵ绰
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
    # �ж�����
    if re.search('''^(http|https|ftp):(//|\\\\)(([\w/\\\+\-~`@:%])+\.)+([\w/\\\.\=\?\+\-~`@':!%#]|(&amp;)|&)+''',cUrl,re.I) != None :
        # http��ͷ��url����Ҫ����
        return tag
    elif cUrl[:1] == '/' :
        # ����·��
        cUrl = host + cUrl
    elif cUrl[:3]=='../' :
        # ���·��
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
                
    