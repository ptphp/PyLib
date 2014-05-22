#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys


class changeHosts():
    systemRoot = "C:\\Windows\\System32\\drivers\\etc\\hosts"
    
    content_local = """
222.73.17.25 www.10086.com
222.73.17.25 www.myproject.com
127.0.0.1 www.mysql.org

127.0.0.1 jjr360.com 
127.0.0.1 www.jjr360.com
127.0.0.1 shop.jjr360.com
127.0.0.1 site.jjr360.com
127.0.0.1 www.rrr.jjr360.com
127.0.0.1 tt.jjr360.com
127.0.0.1 upload.jjr360.com
127.0.0.1 my.jjr360.com #北京
127.0.0.1 static.jjr360.com #上海
127.0.0.1 post.jjr360.com #昆山
127.0.0.1 suzhou.jjr360.com #北京
127.0.0.1 bj.jjr360.com #北京
127.0.0.1 sh.jjr360.com #上海
127.0.0.1 ks.jjr360.com #昆山
127.0.0.1 gz.jjr360.com #广州
127.0.0.1 sz.jjr360.com #深圳
127.0.0.1 hz.jjr360.com #杭州
127.0.0.1 nj.jjr360.com #南京
127.0.0.1 cz.jjr360.com #常州
127.0.0.1 wx.jjr360.com #无锡
127.0.0.1 nb.jjr360.com #宁波
127.0.0.1 zz.jjr360.com #郑州
127.0.0.1 wz.jjr360.com #温州
127.0.0.1 tc.jjr360.com #太仓
127.0.0.1 zjg.jjr360.com #张家�?
127.0.0.1 cd.jjr360.com #成都
127.0.0.1 cq.jjr360.com #重庆
127.0.0.1 tj.jjr360.com #天津
127.0.0.1 wh.jjr360.com #武汉
127.0.0.1 dg.jjr360.com #东莞
127.0.0.1 www.name.jjr360.com
127.0.0.1 sy.jjr360.com #沈阳
127.0.0.1 dl.jjr360.com #大连
127.0.0.1 jn.jjr360.com #济南
127.0.0.1 hn.jjr360.com #海南
127.0.0.1 sanya.jjr360.com #三亚
127.0.0.1 hf.jjr360.com #合肥
    """
    content_pro = """
222.73.17.25 www.10086.com
222.73.17.25 www.myproject.com
127.0.0.1 www.mysql.org
127.0.0.1 ks.jjr360.com
127.0.0.1 suzhou.jjr360.com
127.0.0.1 my.jjr360.com
127.0.0.1 static.jjr360.com
    """
    def do(self, flag):
        if flag == 1:            
            data = self.content_local
            s = "content_local"
        else:
            data = self.content_pro
            s = "content_pro"
        open(self.systemRoot, 'w').write(data)
        print s + "写入成功"

def main():
    flag = input('enter:')
    obj = changeHosts()
    obj.do(flag)
if __name__ == "__main__":
    main()
