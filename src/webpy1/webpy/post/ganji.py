#coding=UTF-8
'''
Created on 2011-6-18

@author: Administrator
'''
import urllib2
from lxml import etree
import datetime
import time
from urlparse import urlparse
import re
from lxml.cssselect import CSSSelector
import mimetypes
import cookielib
import simplejson as js
import random
page='''
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<script type="text/javascript">
var SPEED_RENDER_BEGIN = new Date().getTime();
</script>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>【4图】实体复式房.独门独户上海同等房价格最低 1280起- 上海赶集网</title>
<meta name="WT.cg_n" content="detail;c-2" />
<meta name="WT.cg_s" content="tg;mc-1" />

<link href="http://s6.ganjistatic1.com/css/housing_tuiguang/detail_ue3.__1303182279__.css" rel="stylesheet" type="text/css" />
<link href="http://s6.ganjistatic1.com/css/validator.__1290678648__.css" rel="stylesheet" type="text/css" />
<script type="text/javascript" src="http://s6.ganjistatic1.com/js/housing/premier/house_premier_public_detail.__1304505358__.js" ></script>
<script type="text/javascript" src="http://sta.ganji.com/cgi/ganji_sta.php?file=ganji"></script>

</head>
<body>
<div class="header">
  <a id="logo_ue3" href="/"><img src="/images/ganjiLogo.gif" /></a>
  <span class="city"><a href="/" class="f13">上海</a><a href="http://www.ganji.com/index.htm" class="f_c_b">[切换城市]</a></span>
  <div id="where4">
    <div class="tophelp2" id="userLoginMsgUe3"></div>
    <a href="/">上海赶集网</a> &gt; <a href="/fang1/">上海租房</a> &gt; <a href="/fang1/yangpu/">杨浦租房</a> &gt; <a href="/fang1/wujiaochang/">五角场租房</a>

  </div>
</div>

<div id="wrapper2">
  <div class="mainbox">
    <div class="detail_infobox">
<div class="detail_title">   <h1>实体复式房.独门独户上海同等房价格最低 1280起<span class="pub_time">06-19</span></h1>
   </div>
<div class="greenbd"></div>
<ul class="d_i">

  <li>租金: <span>1280</span> 元/月&nbsp;(押一付二)</li>
  <li>面积: 20 ㎡</li>
  <li>小区:  <a href="/xiaoqu/handanlu120/" target="_blank">邯郸路120号</a>  (邯郸路120号)</li>
  <li>区域: <a href="/fang1/yangpu/">杨浦</a>  - <a href="/fang1/wujiaochang/">五角场</a>  </li>

  <li>房型:     整租 - 1室1厅1卫     </li>
  <li>楼层: 第2层/总3层</li>
  <li>朝向: 南北</li>
  <li>装修: 精装修</li>
    <li>配置: 床 暖气 煤气 宽带网 有线电视 电视 冰箱 空调 热水器 洗衣机 微波炉 </li>
  </ul>    <ul class="iconbox">

      <li><span  id="detail_page_sms_button"></span>

<script type="text/javascript">
GJ.use('js/app/common/detail/detail.js', function(){
    GJ.createSendSms({
        containerId   : 'detail_page_sms_button',
        content       : 'jp6loK6nnqxfWaqg0Z%2ByksPcylVv161Xb29U0J2yoM3hzZKmyeGZlqWkzZumktbSmWRknKxYa1dt22h0Z4bW1aGoyeGZWXClomd0Z4ZYFNEYIQYK28IXJL0jtSOhTb7gTQrNHsDeTrb0ERz9TOjrSQOxHuK7Trb8ER8qTNPwSg%2BlG%2FLAmRC905Fc6OId5ysN7uRjml4ivBugl2VslFiqumQYBLZlY5Sol2xpnaVOWXCv',
        sp            : 'no'
    });
});
</script>
</li>
      <li><a href="#" onclick="return addFavorite(window.location,document.title);" title="将帖子收藏到浏览器收藏夹" class="shoucang">收藏该房源</a></li>
      <li><a href="http://www.ganji.com/mobile/client.php" target="_blank" style="background: none!important;">下载赶集手机客户端，随时随地找信息！</a></li>
 </ul>
                             <ul class="iconbox">
<li>

<span href="javascript:void(0);" id="share_button" class="ganjifen">分享></span>
<span  id="toShare">
<a class="ganjifen_mr" target='_blank' href="http://v.t.sina.com.cn/share/share.php?appkey=2528754719&url=http%3A%2F%2Fsh.ganji.com%2Ffang1%2Ftuiguang-3108934.htm&title=hi%2C%E6%88%91%E5%9C%A8%23%E8%B5%B6%E9%9B%86%E7%BD%91%23%E5%8F%91%E7%8E%B0%E4%B8%80%E4%B8%AA%23%E3%80%90%E7%A7%9F%E6%88%BF%E3%80%91%23%E4%BF%A1%E6%81%AF%E3%80%90%E5%AE%9E%E4%BD%93%E5%A4%8D%E5%BC%8F%E6%88%BF.%E7%8B%AC%E9%97%A8%E7%8B%AC%E6%88%B7%E4%B8%8A%E6%B5%B7%E5%90%8C%E7%AD%89%E6%88%BF%E4%BB%B7%E6%A0%BC%E6%9C%80%E4%BD%8E%201280%E8%B5%B7%E3%80%91%EF%BC%8C%E6%8C%BA%E5%A5%BD%E7%9A%84%EF%BC%8C%E5%BF%AB%E5%8E%BB%E7%9C%8B%E7%9C%8B%E5%90%A7&content=utf-8&pic=http%3A%2F%2Fimage.ganjistatic1.com%2Ftuiguang%2Fhouse%2F20110321%2F1449%2F1300690171-4235_600-0_6-0.jpg">
新浪微博
</a>

<a class="ganjifen_mr" target='_blank' href="http://v.t.qq.com/share/share.php?url=http%3A%2F%2Fsh.ganji.com%2Ffang1%2Ftuiguang-3108934.htm&appkey=14a01ae9033e40ffa852d3be67a5dbe3&title=hi%2C%E6%88%91%E5%9C%A8%23%E8%B5%B6%E9%9B%86%E7%BD%91%23%23%E3%80%90%E7%A7%9F%E6%88%BF%E3%80%91%23%E9%A2%91%E9%81%93%E7%9C%8B%E5%88%B0%E8%BF%99%E4%B8%AA%E6%9C%89%E7%94%A8%E7%9A%84%E4%BF%A1%E6%81%AF%EF%BC%8C%E5%88%86%E4%BA%AB%E7%BB%99%E5%A4%A7%E5%AE%B6&site=http%3A%2F%2Fsh.ganji.com&pic=http%3A%2F%2Fimage.ganjistatic1.com%2Ftuiguang%2Fhouse%2F20110321%2F1449%2F1300690171-4235_600-0_6-0.jpg">
腾讯微博
</a>

<a class="ganjifen_mr" target='_blank' href="http://sns.qzone.qq.com/cgi-bin/qzshare/cgi_qzshare_onekey?url=http%3A%2F%2Fsh.ganji.com%2Ffang1%2Ftuiguang-3108934.htm&title=%E3%80%90%E5%AE%9E%E4%BD%93%E5%A4%8D%E5%BC%8F%E6%88%BF.%E7%8B%AC%E9%97%A8%E7%8B%AC%E6%88%B7%E4%B8%8A%E6%B5%B7%E5%90%8C%E7%AD%89%E6%88%BF%E4%BB%B7%E6%A0%BC%E6%9C%80%E4%BD%8E%201280%E8%B5%B7%E3%80%91
-%E3%80%90%E7%A7%9F%E6%88%BF%E3%80%91-
%E3%80%90%E8%B5%B6%E9%9B%86%E7%BD%91%E3%80%91">
QQ空间
</a>

<a class="ganjifen_mr" target='_blank' href="http://www.kaixin001.com/repaste/share.php?rurl=http://sh.ganji.com/fang1/tuiguang-3108934.htm&amp;rtitle=%E3%80%90%E5%AE%9E%E4%BD%93%E5%A4%8D%E5%BC%8F%E6%88%BF.%E7%8B%AC%E9%97%A8%E7%8B%AC%E6%88%B7%E4%B8%8A%E6%B5%B7%E5%90%8C%E7%AD%89%E6%88%BF%E4%BB%B7%E6%A0%BC%E6%9C%80%E4%BD%8E%201280%E8%B5%B7%E3%80%91&amp;rcontent=%20%26%23xa0%3B8090%E5%90%8E%E6%98%AF%E4%B8%80%E4%B8%AA%E5%A4%9A%E5%85%83%E5%8C%96%E7%9A%84%E7%BE%A4%E4%BD%93%EF%BC%8C%E4%B8%BA%E4%BA%86%E5%AE%9E%E7%8E%B0%E6%97%B6%E5%B0%9A%E5%92%8C%E8%88%92%E9%80%82%E7%9A%84%E6%9B%B4%E9%AB%98%E7%90%86%E5%BF%B5%EF%BC%8C%E6%88%91%E4%BB%AC%E6%8E%A8...">
开心网

</a>

<a class="ganjifen_mr" target='_blank' href="http://share.renren.com/share/buttonshare.do?link=http://sh.ganji.com/fang1/tuiguang-3108934.htm&amp;title=%E3%80%90%E5%AE%9E%E4%BD%93%E5%A4%8D%E5%BC%8F%E6%88%BF.%E7%8B%AC%E9%97%A8%E7%8B%AC%E6%88%B7%E4%B8%8A%E6%B5%B7%E5%90%8C%E7%AD%89%E6%88%BF%E4%BB%B7%E6%A0%BC%E6%9C%80%E4%BD%8E%201280%E8%B5%B7%E3%80%91
-%E3%80%90%E7%A7%9F%E6%88%BF%E3%80%91-
%E3%80%90%E8%B5%B6%E9%9B%86%E7%BD%91%E3%80%91">
人人网
</a>
</span>
</li>
</ul>    </div>
     <div class="detail_message">
        <div class="greenbd"></div>
        <div class="manager_div"> 
                          <img src="http://image.ganjistatic1.com/tuiguang/customer/20101220/1459/1292828396-2939.jpg"/>
                         <p>政滔滔</p>

            <p>上海独立经纪人</p>
            <div class="ma_renz"> 
            <span class="renz_a1"></span>
                            <span class="renz_b2"></span>
                        </div>
            <div class="renz_jinru"><a href="http://sh.ganji.com/fang_41776/" class="user_history" target="_blank">看看我的店铺 </a><a href="#" onclick="return goto_message_form();" class="messages">请给我留言吧</a></div>
        </div>
     </div>

     
     <div class="detail_sider">
       <div class="greenbd"></div>
        <div class="sider_box">
            <div class="sider_box_r1">
                <p class="tel">经纪人联系电话</p>
                <div class="tel_number ganji_phone_call_class">
                    60519592
                    <!--  <img src="60519592" align="absmiddle"/> -->
                </div> 
                <div class="f_c_gray3" style="text-indent:40px">(联系我时请说是赶集网看到的)</div>

            </div>
            <div class="jubao sc_ju" id="complain">
            <script type="text/javascript">
            var jubao_html = '<p class="f_c_gray">我要举报:</p>';
                            jubao_html += '<p class="pt10" id="jubao"><a href="#" class="jubaobg" onclick="return post.complain(\'3108934\', \'1\', 7)">房源已租或不存在</a><a href="#" class="jubaobg" onclick="return post.complain(\'3108934\', \'1\', 8)">房租不真实</a></p>';
                        $('#complain').html(jubao_html);
            </script>
            </div>
        </div>
  </div>
  <div class="hackDiv"></div>
  <div id="content">

    <div class="bluebg"></div>
    <div class="detail_box">
       <p class="gaikuang gk_noline" id="house_content">   
       <a class="top" href="#" onclick="return backToTop();">返回顶部</a>房屋概况
       </p>
       <div class="tuiguang_text editor" id="id_description"><p class="p0" style="MARGIN-TOP: 0pt; MARGIN-BOTTOM: 0pt; TEXT-ALIGN: justify">&#xa0;8090后是一个多元化的群体，为了实现时尚和舒适的更高理念，我们推出了房高为5米的精致小家，它更为具体的体现了韩式日式的空间理念。有一小厅，让你的生活更加闲致，进退自如，双层阳光大窗，至尊享受，把美景一览无余，一室一卫（大卫），配有空调，液晶电视，热水器，书柜衣柜，写字桌，1.3米的日式踏踏米床垫，还有高速光纤上网和公共的休闲生活设施配备，让你不出国门，就能感受到韩风来袭！</p></div>
              <p class="gaikuang" id="image">
         <a class="top" href="#" onclick="return backToTop();">返回顶部</a>房屋图片
       </p>

       <ul class="detail_img">
              <li>
            <img src="http://image.ganjistatic1.com/tuiguang/house/20110321/1449/1300690171-4235_600-0_6-0.jpg"/>
                     
       </li>
              <li>
            <img src="http://image.ganjistatic1.com/tuiguang/house/20110321/1449/1300690176-1100_600-0_6-0.jpg"/>
                     
       </li>
              <li>
            <img src="http://image.ganjistatic1.com/tuiguang/house/20110321/1449/1300690181-3558_600-0_6-0.jpg"/>

                     
       </li>
              <li>
            <img src="http://image.ganjistatic1.com/tuiguang/house/20110321/1449/1300690195-9087_600-0_6-0.jpg"/>
                     
       </li>
              </ul>
                     <p class="gaikuang" id="traffic">
         <a class="top" href="#" onclick="return backToTop();">返回顶部</a>  
         地图交通
       </p>

       <div id="map_load"></div>
                      <p class="gaikuang" id="xiaoqu">
         <a class="top" href="#" onclick="return backToTop();">返回顶部</a>
         小区介绍
       </p>
       <div class="xiaoqu_box">
          <div class="xiaoqu_info">
             <ul>
               <li>邯郸路120号</li>

               <li><a target="_blank" href="/xiaoqu/handanlu120/">小区详情</a></li>
               <li><a target="_blank" href="/xiaoqu/handanlu120/chuzufang/">小区租房(28)</a></li>
               <li><a target="_blank" href="/xiaoqu/handanlu120/hezufang/">小区合租房(0)</a></li>
               <li><a target="_blank" href="/xiaoqu/handanlu120/ershoufang/">小区二手房(0)</a></li>
             </ul>
            <table width="0" border="0" cellspacing="0" cellpadding="0" >
               <tr>

                 <td class="width3">地址:</td>
                 <td>邯郸路120号</td>
              </tr>
                              <tr>
                    <td class="width3">学校:</td>
                    <td>上海市南湖职业学校第二分校,上海市交通职业技术学校,上海市南湖职业学校第二分校(北门),特爱外语,白玉兰学校</td>
                </tr>

                              <tr>
                    <td class="width3">医院:</td>
                    <td>上海海光医院,五角场医院,岳阳医院(2号门),上海中医药大学附属岳阳中西医结合医院(三号门),上海中医药大学附属岳阳中西医结合医院</td>
                </tr>
                              <tr>
                    <td class="width3">餐饮:</td>
                    <td>谷香园餐厅,成古久家,闻湘记湘菜酒楼,艳芳湘菜馆,池上便当上海邯郸店</td>

                </tr>
                              <tr>
                    <td class="width3">购物:</td>
                    <td>客快超市,华联超市,欧特福超市,运光便利,联华</td>
                </tr>
                          </table>
          </div>
                    <div class="xiaoqu_img">

             <div class="img_small">
                          <a href="/xiaoqu/handanlu120/pic/1/1141293.htm" target="_blank">
             <img src="http://image.ganjistatic1.com/xiaoqu/20110220/1603/1298188982-4442s.jpg"/></a>
                          <a href="/xiaoqu/handanlu120/pic/1/1141292.htm" target="_blank">
             <img src="http://image.ganjistatic1.com/xiaoqu/20110220/1603/1298188980-2193s.jpg"/></a>
                          <a href="/xiaoqu/handanlu120/pic/1/1141291.htm" target="_blank">
             <img src="http://image.ganjistatic1.com/xiaoqu/20110220/1602/1298188979-2259s.jpg"/></a>
                          <a href="/xiaoqu/handanlu120/pic/1/1141290.htm" target="_blank">
             <img src="http://image.ganjistatic1.com/xiaoqu/20110220/1602/1298188965-8069s.jpg"/></a>

                          </div>
             <div class="xiaoqubg1"></div>
             <div class="xiaoqubg2"></div>
             <div class="xiaoqubg3"></div>
             <div class="xiaoqubg4"></div>
          </div> 
           
       </div>
           </div>
    <div class="hackDiv"></div>

    <p class="gaikuang"><span class="f_c_gray3">给政滔滔留言</span> </p>
<div class="message_box show_pseudo_message" id="id_message_panel" >
<div id="id_message_done_prompt" class="msg_done"><div class="content"></div></div>
<form target="_blank"  enctype="multipart/form-data" id="id_message_form">
<table cellspacing="0" cellpadding="0" border="0">
  <tr>
    <td align="right" width="70" valign="top"><span class="f_c_red">*</span>留言内容</td>
    <td class="message2"><textarea id="id_message_content" name="content" rows="5" class="input_bod form_width" ></textarea></td><td class="message3"><span id="tip_span_content" class="form_block"></span></td>

  </tr>
  <tr class="hide_when_pseudo">
    <td align="right" width="70" valign="top"><span class="f_c_red">*</span>联系方式</td>
    <td><input name="contact" type="text" class="input_bod form_input" id="id_message_contact"/></td><td><span id="tip_span_contact" class="form_block"></span></td>
  </tr>
  <tr class="hide_when_pseudo">
    <td align="right" width="70" valign="top"><span class="f_c_red">*</span>验证码</td>

    <td>
    <div style="display:none;height:60px;margin-bottom:5px">
        <span id="authcode_wrapper" class="show_authcode_prompt">
        </span>
        &nbsp;&nbsp;&nbsp;
        <span>请输入左侧字符，不区分大小写</span>
    </div>
    <input id="id_message_checkcode" name="checkcode" onclick="$(this).parent().siblings().css('padding-top', '75px');return post.showAuthCode();" class="input_bod" size="20"/>

    <a id="update_authcode_btn" href="#" onclick="return post.resetAuthCode();" style="display:none;">换一张</a>
    <span id="tip_span_checkcode"></span>
  </td>
  </tr>
  <tr class="hide_when_pseudo">
    <td align="right" width="70">&nbsp;</td>
    <td>
    <input id="id_message_submit_button" type="button" class="btnbg" value="留 言" house_id="3108934" class="btnbg"/>

    </td>
  </tr>
  <tr>
      <td align="right" width="70">&nbsp;</td>
      <td colspan="2"><div class="sider_box_r2">
      <p class="tel">经纪人联系电话</p>
      <div class="tel_number ganji_phone_call_class">
          60519592
        <!-- <img align="absmiddle" src="/tel/0333043155600167046b053104655535_4.png"> -->

      </div>
      <div class="say_ganji f_c_gray3">(联系我时请说是赶集网看到的)</div>
      </div></td>
  </tr>
  </table>
<script type='text/javascript'>
$.validator("content")
.setTipSpanId("tip_span_content")
.setFocusMsg("最多允许输入150个字")
.setRequired("请输入内容")
.setServerCharset("UTF-8")
.setStrlenType("symbol")
.setLength(1, 150, "内容不能超过150个字");

$.validator("contact")
.setTipSpanId("tip_span_contact")
.setFocusMsg("最多允许输入50个字")
.setEmptyValue("请输入您的联系方式（如电话号码，电子邮件等），以便发布人及时联系您！")
.setRequired("请输入联系方式")
.setServerCharset("UTF-8")
.setStrlenType("symbol")
.setLength(1, 50, "联系方式不能超过50个字");

$.validator("checkcode")
.setTipSpanId("tip_span_checkcode")
.setRequired("请填写验证码")
.setAjax("/ajax/check_code.php", "验证码不正确");

</script>
</form>
</div>
<script type="text/javascript">
post.initMessageForm();
$.validator.addFormCallback('id_message_form', function(){
    $.post('/ajax/save_housing_premier_message.php', 
    {id:3108934, type:1, contact:$('#id_message_contact').val(), content:$('#id_message_content').val(), checkcode:$('#id_message_checkcode').val()},
     function(data){
        post.submitMessageDone(data);
    }, 'json');
    return false;
});    
</script>

  </div>
  <div id="rightSide">
    <div class="bdgray"></div>
<!-- -->
            <div class="fangyan">
      <p class="titlebg mt8">附近类似房源 </p>
            <dl class="watched">
         <dt><a href="/fang1/tuiguang-1680884.htm" target="_blank">杨浦-五角场-国京路51号</a></dt>

         <dd>20㎡，1室1厅，<span class="f_c_red">1300</span>元/月</dd>
      </dl>
            <dl class="watched">
         <dt><a href="/fang1/tuiguang-1997264.htm" target="_blank">杨浦-五角场-华浜二村</a></dt>
         <dd>25㎡，1室1厅，<span class="f_c_red">1300</span>元/月</dd>

      </dl>
            <dl class="watched">
         <dt><a href="/fang1/tuiguang-2311035.htm" target="_blank">杨浦-五角场-邯郸路120号</a></dt>
         <dd>15㎡，1室1厅，<span class="f_c_red">1380</span>元/月</dd>
      </dl>
            <dl class="watched">
         <dt><a href="/fang1/tuiguang-2714152.htm" target="_blank">杨浦-五角场-邯郸路120号</a></dt>

         <dd>20㎡，1室1厅，<span class="f_c_red">1380</span>元/月</dd>
      </dl>
            <dl class="watched">
         <dt><a href="/fang1/tuiguang-4449432.htm" target="_blank">杨浦-五角场-杨浦欣园</a></dt>
         <dd>59㎡，1室1厅，<span class="f_c_red">1500</span>元/月</dd>

      </dl>
          </div>
            <div class="fangyan">
      <p class="titlebg">该经纪人热门房源 </p>
            <dl class="watched">
         <dt><a href="/fang1/tuiguang-2310818.htm" target="_blank">杨浦-五角场-邯郸路120号</a></dt>
         <dd>12㎡，1室1厅，<span class="f_c_red">1280</span>元/月</dd>

      </dl>
            <dl class="watched">
         <dt><a href="/fang1/tuiguang-2310894.htm" target="_blank">杨浦-复旦大学-邯郸路120号</a></dt>
         <dd>12㎡，1室1厅，<span class="f_c_red">1280</span>元/月</dd>
      </dl>
            <dl class="watched">
         <dt><a href="/fang1/tuiguang-2801519.htm" target="_blank">杨浦-复旦大学-邯郸路120号</a></dt>

         <dd>20㎡，1室1厅，<span class="f_c_red">1380</span>元/月</dd>
      </dl>
            <dl class="watched">
         <dt><a href="/fang1/tuiguang-2801657.htm" target="_blank">杨浦-复旦大学-邯郸路120号</a></dt>
         <dd>20㎡，1室1厅，<span class="f_c_red">1380</span>元/月</dd>

      </dl>
            <dl class="watched">
         <dt><a href="/fang1/tuiguang-2802614.htm" target="_blank">杨浦-五角场-邯郸路120号</a></dt>
         <dd>20㎡，1室1厅，<span class="f_c_red">1380</span>元/月</dd>
      </dl>
          </div>
         <div class="fangyan" style="border: 0pt none;"><a href="/wu" target="_blank"><img src="http://sta.ganjistatic1.com/src/image/ads/20110402.jpg" width="212" height="150" /></a></div>

    <div id="ad_container_zanzhushang"></div>
   </div>
   <div class="bluebox">
    <div class="bluebg_left "><div class="bluebg"></div></div>
    <div class="bluebg_right">
       <div class="bluebg"></div>
    </div>
</div>
</div>
<script type="text/javascript">
var SPEED_RENDER_END = new Date().getTime();

</script>

<script type="text/javascript">
     (function(){
         var o = {
             type : 'view',      //view,set,fang
             displayType : 'iframe',//iframe panel 弹出层
             containerId : 'map_load',
             cityName : "上海",
             cityDomain : "sh",
             xiaoqu : '邯郸路120号',
             address : '邯郸路120号',
             lngLat: "31.294963,121.496505",
             width:720,
             height:380
         };
         GJ.use('map', function(){
             GJ.createMap(o);
             });
     })();
</script>
<script type="text/javascript">
displayLoginMsg();
DP.addHistory('housing_1',
'<a href="/fang1/tuiguang-3108934.htm">实体复式房.独门独户上海同等房</a>',
'五角场  1室1厅，<b>1280</b>元/月'); 
window.detailPageHelper.enableMagicCopy();
</script>
<script type="text/javascript">
GJ.use('log_tracker', function(){
    GJ.LogTracker.gjch = "/fang/fang1/detail@post_id=3108934@tuiguang=1@ad_type=6";
    GJ.LogTracker.bindAllTrackEvent();
    GJ.LogTracker.trackPageView();
    GJ.LogTracker.trackSpeedEvent();
});
</script>
                <script type="text/javascript">
GJ.use('js/app/common/lottery/lottery.js', function(){
    GJ.lottery();
});
</script>
<script type="text/javascript">
GJ.use('js/app/common/langtaojin/langtaojin.js', function(){
    GJ.ltj.convert('6166', '1', '1表示一个详情页展现');
}); 
</script>
<script type="text/javascript">
GJ.use("js/app/common/adm/adm.js", function(){
   GJ.adm.init();
   GJ.adm.setParams({"pt":4,"sd":"sh","d":"199","s":"5909","mac":20,"c":13,"ca":"7","mic":0,"t":0,"ps":0,"bz":null});
});
</script>

<ul id="footer">

    <li><a target="_blank" rel="nofollow" href="http://www.ganji.com/misc/abouts/index.php?act=about">关于Ganji</a> - <a target="_blank" rel="nofollow" href="http://www.ganji.com/misc/abouts/index.php?act=contact">联系Ganji</a> - <a target="_blank" rel="nofollow" href="http://tuiguang.ganji.com/zhaoshang/index.htm">赶集推广</a> - <a target="_blank" rel="nofollow" href="http://tuiguang.ganji.com/zhaoshang/agent.htm"> 渠道合作 </a> - <a target="_blank" rel="nofollow" href="http://www.ganji.com/misc/abouts/index.php?act=help">帮助中心</a> - <a target="_blank" rel="nofollow" href="http://www.ganji.com/misc/abouts/index.php?act=termofuse">免责声明</a> - <a target="_blank" rel="nofollow" href="http://www.ganji.com/misc/abouts/link.php?act=link">友情链接</a> - <a href="http://www.ganji.com/misc/abouts/index.php?act=job_stu" target="_blank" rel="nofollow">招贤纳士</a>

 - <a target="_blank" rel="nofollow" href="/quxiandaohang/">区县导航</a></li>
    <li>Copyright &copy;2005-2011Ganji 版权所有 <a href="http://www.miibeian.gov.cn/" target="_blank" rel="nofollow">京ICP证080580号</a>&nbsp;京ICP备09085189<br />海淀公安局网络备案编号：1101081759</li>
</ul>

<style> 
#change_city{font-size:13px;background:#FFFFCD;width:205px;position:absolute;z-index:1;display:none} 
#change_city img {border:none} 
#change_city b{display:block;height:1px;line-height:1px;font-size:1px;line-height:1px} 
#change_city p{margin:0;padding:0} 
#change_city .mbody{border-left:1px solid #aaa;border-right:1px solid #aaa;padding:5px;clear:both;} 
#change_city b.a1{margin:0 2px;background:#aaa} 
#change_city b.a2{margin:0 1px;background:#fff;border-left:1px solid #aaa;border-right:1px solid #aaa;} 
#change_city h1{clear:both;zoom:1;border-bottom:1px solid #E4E4E4;line-height:20px;} 
#change_city .closeimg{ position:absolute; top:8px; right:8px;} 
#change_city p{line-height:20px;zoom:1;padding-right:20px} 
#change_city p a{color:#24d; text-decoration:underline;} 
#change_city p a:hover{color:#e40000} 
#change_city p a:visited{color:#24d}
#change_city .arrow{position:absolute; top:-4px;left:19px;} 
</style>
<div id="change_city"><b class="a1">&nbsp;</b><b class="a2">&nbsp;</b><div class="mbody"><a href="#" onclick="javascript:$('#change_city').hide(); return false;"><img src="http://sta.ganjistatic1.com/src/image/other/close.png" width="15" height="15" class="closeimg" /></a> 
<p>如果不是您当前所在城市，可选<br />择<a href="http://www.ganji.com/index.htm">切换城市</a>重新选择</p></div><b class="a2">&nbsp;</b><b class="a1">&nbsp;</b><img src="http://sta.ganjistatic1.com/src/image/other/arrow_up.png" width="7" height="5" class="arrow" /></div>

<script type="text/javascript">
if (GJ.getCookie('rewrite_ip_domain') != null)
{
        var offset = $('.city').position();
    var offsetTop = offset.top + 20 + 'px';
    var offsetLeft = offset.left + 4 + 'px';
    $('#change_city').css({"top": offsetTop, "left": offsetLeft});
    $('#change_city').show();
    GJ.removeCookie('rewrite_ip_domain');
}
</script>
<!-- Analysis Code -->
<SCRIPT language="JavaScript" SRC="http://s1.ganjistatic1.com/js/dcs/fangchan_dcs_tag.js" id="fangchan_dcscdeyp1fhcfnncczq87vdyc_7c6u"></SCRIPT>
 <NOSCRIPT> <IMG ALT="" BORDER="0" NAME="DCSIMG" WIDTH="1" HEIGHT="1" SRC="http://log.ganji.com/dcscdeyp1fhcfnncczq87vdyc_7c6u/njs.gif?dcsuri=/nojavascript&WT.js=No"> </NOSCRIPT>
<!-- End Code -->

<!-- 
<script type="text/javascript"> 
GJ.use('app_global', function(){
    GJ.mvTrackPageview();
}); 
</script>
 --> 

<script type="text/javascript"> 
GJ.use('js/app/common/google/google.js', function(){
    GJ.google.trackPageview();
});
</script></body>
</html>


'''    
house_price_regex="<li>期望租金: (.*)</li>"
house_room_regex="<li>期望房型: (.*)</li>"
house_addr_regex="<li>小区地址:(.*)</li>"
borough_name_regex="<li>期望小区: (.*)</li>"
expect_price_regex="<li>期望售价: (.*)</li>"
house_totalarea_regex="<li>期望面积: (.*)㎡</li>"
cityarea_regex_1="<li>小区:(.*)</li>"
borough_section_regex_1="<li>区域: (.*)</li>"


header={"User-Agent": "Mozilla/5.0 (Windows NT 5.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"}
def QiuZhu(url):
    v ={}
    note=url[url.rfind('''/''')+1:-4]
    v['note'] =note
    v['city'] = urlparse(url)[1].replace('.ganji.com',"")
    response = page#urllib2.urlopen(url).read()
    
    tree = etree.HTML(response) 
    
    posttime=CSSSelector('span.pub_time')(tree) and CSSSelector('span.pub_time')(tree)[0].text.strip() or None
    if posttime:
        Y=int(time.strftime('%Y', time.localtime()))
        M=int(posttime.split(' ')[0].split('-')[0])
        D=int(posttime.split(' ')[0].split('-')[1])
        H=int(posttime.split(' ')[1].split(':')[0])
        min=int(posttime.split(' ')[1].split(':')[1])
        s = datetime.datetime(Y,M,D,H,min)
        posttime=int(time.mktime(s.timetuple()))
        v['posttime'] =posttime 
    else:
        v['posttime'] =None 
    owner_name=CSSSelector('span.Dname')(tree) and CSSSelector('span.Dname')(tree)[0].text.strip() or None
    v['owner_name'] =owner_name 
    if re.search(house_price_regex, response):
        house_price=re.search(house_price_regex, response).group(1)
        if house_price.find("元/月")!=-1:
            house_price_min=int(house_price.replace("元/月","").split("-")[0])
            house_price_max=int(house_price.replace("元/月","").split("-")[1])
            v['house_price_max']=house_price_max  
            v['house_price_min']=house_price_min
        elif house_price.find("元以下/月")!=-1:
            try:
                house_price=int(house_price.replace("元以下/月",""))
            except:
                #该处是折中的办法,因为有这种可能性,但是测试页面还没发生这种异常
                house_price=int(house_price[:4])
            v['house_price_max']=house_price  
            v['house_price_min']=0
        elif house_price.find("元以上/月")!=-1:
            try:
                house_price=int(house_price.replace("元以下/月",""))
            except:
                #该处是折中的办法,因为有这种可能性,但是测试页面还没发生这种异常
                house_price=int(house_price[:4])
            v['house_price_max']=0  
            v['house_price_min']=house_price
        else:
            v['house_price_max']=0  
            v['house_price_min']=0
    else:
        v['house_price_min']=0
        v['house_price_max']=0 
    
    if re.search(house_room_regex, response):
        house_room=re.search(house_room_regex, response).group(1)
        house_room=house_room.replace("室","|").replace("厅","|").replace("卫","")
        v['house_room'] = house_room
    else:
        v['house_room'] =None
        
        
    owner_phone=CSSSelector("span.ganji_phone_call_class img")(tree)[0].get("src") and "http://"+urlparse(url)[1]+CSSSelector("span.ganji_phone_call_class img")(tree)[0].get("src").strip() or None
    v['owner_phone'] = owner_phone
    if re.search(house_addr_regex, response):
        house_addr=re.search(house_addr_regex, response).group(1)
        v['house_addr'] = house_addr
    else:
        v['house_addr'] = None
    
    if re.search(cityarea_regex_1, response):
        cityarea=re.search(cityarea_regex_1, response).group(1)
        if "href" in cityarea: 
            cityarea=etree.HTML(cityarea).xpath("/html/body/a")[0].text.encode('raw_unicode_escape')
        v['cityarea'] = cityarea
    else:
        v['cityarea'] =None
    
    if re.search(borough_section_regex_1, response):
        borough_section_html=re.search(borough_section_regex_1, response).group(1)
        if "href" in borough_section_html: 
            borough_section_txt=etree.HTML(borough_section_html).xpath("/html/body/a")[1]!=None and etree.HTML(borough_section_html).xpath("/html/body/a")[1].text.encode('raw_unicode_escape') or None
        v['borough_section'] = borough_section_txt
    else:
        v['borough_section'] =None
        
    house_desc=CSSSelector("p.text")(tree)[0] !=None and CSSSelector("p.text")(tree)[0].text.strip() or None

    v['house_desc'] = house_desc.replace("联系我时请说明是从赶集网上看到的","")

    if re.search(borough_name_regex, response):
        borough_name=re.search(borough_name_regex, response).group(1)
        if "href" in borough_name: 
            borough_name=etree.HTML(borough_name).xpath("/html/body/a")[0].text.encode('raw_unicode_escape')
        v['borough_name'] = borough_name
    else:
        v['borough_name'] = None
    
    
    house_title=CSSSelector("div.detail_title h1")(tree)[0] !=None and CSSSelector("div.detail_title h1")(tree)[0].text.strip() or None
    v['house_title'] = house_title
    
    #info_type=CSSSelector("span.bq1")(tree)[0] !=None and CSSSelector("span.bq1")(tree)[0].text.strip() or None
    #这里没办法必须写死,页面不标准,lxml解析后 和实际页面不符
    
    info_type=tree.xpath("//span[@class='bq1']/text()")[0] and tree.xpath("//span[@class='bq1']/text()")[0].strip() or None
    v['info_type'] = info_type
    return v

def QiuGou(url):
    v ={}
    note=url[url.rfind('''/''')+1:-4]
    v['note'] =note
    v['city'] = urlparse(url)[1].replace('.ganji.com',"")
    response = page#urllib2.urlopen(url).read()
 
    tree = etree.HTML(response)  
    posttime=CSSSelector('span.pub_time')(tree) and CSSSelector('span.pub_time')(tree)[0].text.strip() or None 
    if posttime:
        Y=int(time.strftime('%Y', time.localtime()))
        M=int(posttime.split(' ')[0].split('-')[0])
        D=int(posttime.split(' ')[0].split('-')[1])
        H=int(posttime.split(' ')[1].split(':')[0])
        min=int(posttime.split(' ')[1].split(':')[1])
        s = datetime.datetime(Y,M,D,H,min)
        posttime=int(time.mktime(s.timetuple()))
        v['posttime'] =posttime 
    else:
        v['posttime'] =None
    owner_name=CSSSelector('span.Dname')(tree) and CSSSelector('span.Dname')(tree)[0].text.strip() or None
    v['owner_name'] =owner_name 
#    owner_name=tree.xpath('/html/body/div[2]/div/div[3]/div[2]/div/p/span') and tree.xpath('/html/body/div[2]/div/div[3]/div[2]/div/p/span')[0].text.strip() or None
#    v['owner_name'] =owner_name 
    if re.search(expect_price_regex, response):
        house_price=re.search(expect_price_regex, response).group(1)
        if house_price.find("万")!=-1:
            house_price_min=int(house_price.replace("万","").split("-")[0])
            house_price_max=int(house_price.replace("万","").split("-")[1])
            v['house_price_max']=house_price_max  
            v['house_price_min']=house_price_min
        elif house_price.find("万以下")!=-1:
            try:
                house_price=int(house_price.replace("万以下",""))
            except:
                #该处是折中的办法,因为有这种可能性,但是测试页面还没发生这种异常
                house_price=int(house_price[:4])
            v['house_price_max']=house_price  
            v['house_price_min']=0
        elif house_price.find("万以上")!=-1:
            try:
                house_price=int(house_price.replace("万以下",""))
            except:
                #该处是折中的办法,因为有这种可能性,但是测试页面还没发生这种异常
                house_price=int(house_price[:4])
            v['house_price_max']=0  
            v['house_price_min']=house_price
        else:
            v['house_price_max']=0  
            v['house_price_min']=0
    else:
        v['house_price_min']=0
        v['house_price_max']=0 
    
    if re.search(house_room_regex, response):
        house_room=re.search(house_room_regex, response).group(1)
        house_room=house_room.replace("室","|").replace("厅","|").replace("卫","")
        v['house_room'] = house_room
    else:
        v['house_room'] =None
        
    
    owner_phone=CSSSelector("span.ganji_phone_call_class img")(tree)[0].get("src") and "http://"+urlparse(url)[1]+CSSSelector("span.ganji_phone_call_class img")(tree)[0].get("src").strip() or None
    v['owner_phone'] = owner_phone
#    owner_phone=tree.xpath('/html/body/div[2]/div/div[3]/div[2]/div/p[2]/span/img/@src') and "http://"+urlparse(url)[1]+tree.xpath('/html/body/div[2]/div/div[3]/div[2]/div/p[2]/span/img/@src')[0].strip() or None
#    v['owner_phone'] = owner_phone
    if re.search(house_addr_regex, response):
        house_addr=re.search(house_addr_regex, response).group(1)
        v['house_addr'] = house_addr
    else:
        v['house_addr'] = None
    if re.search(borough_section_regex_1, response):
        cityarea=re.search(borough_section_regex_1, response).group(1)
        if "href" in cityarea: 
            cityarea=etree.HTML(cityarea).xpath("/html/body/a")[0].text.encode('raw_unicode_escape')
        v['cityarea'] = cityarea
    else:
        v['cityarea'] =None
#    cityarea=tree.xpath('/html/body/div[2]/div/div[3]/div/ul/li/a') and tree.xpath('/html/body/div[2]/div/div[3]/div/ul/li/a')[0].text.strip() or None
#    v['cityarea'] = cityarea
    
    if re.search(borough_section_regex_1, response):
        borough_section_html=re.search(borough_section_regex_1, response).group(1)
        if "href" in borough_section_html: 
            borough_section_txt=etree.HTML(borough_section_html).xpath("/html/body/a")[1]!=None and etree.HTML(borough_section_html).xpath("/html/body/a")[1].text.encode('raw_unicode_escape')
        v['borough_section'] = borough_section_txt
    else:
        v['borough_section'] =None
    
    house_desc=CSSSelector("p.text")(tree)[0] !=None and CSSSelector("p.text")(tree)[0].text.strip() or None
    v['house_desc'] = house_desc.replace("联系我时请说明是从赶集网上看到的","")
    if re.search(borough_name_regex, response):
        borough_name=re.search(borough_name_regex, response).group(1)
        if "href" in borough_name:
            borough_name=etree.HTML(borough_name).xpath("/html/body/a")[0].text.encode('raw_unicode_escape')
        v['borough_name'] = borough_name
    else:
        v['borough_name'] = None
        
    if re.search(house_totalarea_regex, response): 
        house_totalarea=re.search(house_totalarea_regex, response).group(1)
        v['house_totalarea_min'] =house_totalarea          
        v['house_totalarea_max'] = house_totalarea
    else:
        v['house_totalarea_min'] = 0        
        v['house_totalarea_max'] = 0
        
    house_title=CSSSelector("div.detail_title h1")(tree)[0] !=None and CSSSelector("div.detail_title h1")(tree)[0].text.strip() or None
    v['house_title'] = house_title
    info_type=tree.xpath("//span[@class='bq1']/text()")[0] and tree.xpath("//span[@class='bq1']/text()")[0].strip() or None
    v['info_type'] = info_type
    return v
        

    
house_floor_regex="<li>楼层: 第(.*)层/总(.*)层</li>"
house_totalarea_regex="<li>面积: (.*) ㎡</li>"    
house_type_regex="<li>房型: (.*)</li>"
house_toward_regex="<li>朝向: (.*)</li>"
house_type_regex2="<li>类型: (.*)</li>"
cityarea_regex="<li>区域:([\s\S]*?)</li>"
house_age_regex="<li>房龄: (.*)年</li>"
house_fitment_regex="<li>装修: (.*)</li>"
hous_addr_regex="address : '(.*)',"
lngLat_regex='''lngLat: "(.*)",'''
house_support_regex="<li>配置: (.*) </li>"
house_price_regex="<li>售价: <span>(.*)</span>.*</li>"
house_price_regex_2="<li>租金: <span>(.*)</span>.*</li>"
borough_section_regex="<li>小区:[\s\S]*?\((.*)\)[\s\S]*?</li>"
house_deposit_regex="<li>租金: .*\((.*)\)</li>"
def __addText(tag, no_tail=False):
    text = []
    if tag.text:
        text.append(tag.text)
    for child in tag.getchildren():
        text.append(__addText(child))
    if not no_tail and tag.tail:
        text.append(tag.tail)
    return "".join(text)
def getText(html):
    text=[]
    for tag in html:
        text.append(__addText(tag, no_tail=True))
    return ' '.join([t.strip() for t in text if t.strip()])

def ChuShou(url):
    v={}
    v['city'] = urlparse(url)[1].replace('.ganji.com',"")
    v['owner_phone_area']=""
    v['belong']=""
    request = urllib2.Request(url, None, header)
    response =page# urllib2.urlopen(request).read()
    tree = etree.HTML(response)
    
    
    if re.search(house_floor_regex, response):
        house_floor=re.search(house_floor_regex, response).group(1)
        house_topfloor=re.search(house_floor_regex, response).group(2)
        v['house_floor'] = house_floor
        v['house_topfloor'] = house_topfloor
    else:
        v['house_floor'] = None
        v['house_topfloor'] = None   
    
    if re.search(house_totalarea_regex, response):
        house_totalarea=re.search(house_totalarea_regex, response).group(1)
        v['house_totalarea'] = house_totalarea
    else:
        v['house_totalarea'] = None
        
        
    if re.search(house_price_regex, response):
        house_price=re.search(house_price_regex, response).group(1)
        v['house_price'] = house_price
    else:
        v['house_price'] = None
#    house_price=tree.xpath("/html/body/div[2]/div/div/ul/li/span") and tree.xpath("/html/body/div[2]/div/div/ul/li/span")[0].text.strip() or None    
#    v['house_price'] = house_price
    posttime=CSSSelector('span.pub_time')(tree)!=None and CSSSelector('span.pub_time')(tree)[0].text.strip() or None 
    if posttime:
        Y=int(time.strftime('%Y', time.localtime()))
        M=int(posttime.split(' ')[0].split('-')[0])
        D=int(posttime.split(' ')[0].split('-')[1])
        s = datetime.datetime(Y,M,D,0,0)
        posttime=int(time.mktime(s.timetuple()))
        v['posttime'] =posttime 
    else:
        v['posttime'] =None
        
#    posttime=tree.xpath("/html/body/div[2]/div/div/div/h1/span") and tree.xpath("/html/body/div[2]/div/div/div/h1/span")[0].text.strip() or None
#    if posttime:
#        Y=int(time.strftime('%Y', time.localtime()))
#        M=int(posttime.split(' ')[0].split('-')[0])
#        D=int(posttime.split(' ')[0].split('-')[1])
#        s = datetime.datetime(Y,M,D,0,0)
#        posttime=int(time.mktime(s.timetuple()))
#        v['posttime'] =posttime 
#    else:
#        v['posttime'] =None
    if re.search(house_type_regex, response):
        house_type=re.search(house_type_regex, response).group(1)
        try:
            house_type=house_type.strip()
        except:
            pass
        blank=house_type.rfind(" ")
        if house_type.find("室")!= -1:
            house_room=house_type[blank+1:house_type.find("室")]
            blank=house_type.find("室")+3
        else:
            house_room=None
        if house_type.find("厅")!=-1:
            house_hall=house_type[blank:house_type.find("厅")]
            blank=house_type.find("厅")+3
        else:
            house_hall=None
        if house_type.find("卫")!=-1:
            house_toilet=house_type[blank:house_type.find("卫")]
        else:
            house_toilet=None
            
        v['house_room'] = house_room
        v['house_hall'] = house_hall
        v['house_toilet'] = house_toilet
    else:
        v['house_room'] = None
        v['house_hall'] = None
        v['house_toilet'] = None
        
    if re.search(house_toward_regex, response):
        house_toward=re.search(house_toward_regex, response).group(1)
        v['house_toward'] = house_toward
    else:
        v['house_toward'] = None
    owner_phone=CSSSelector("div.ganji_phone_call_class")(tree)[0]!=None and CSSSelector("div.ganji_phone_call_class")(tree)[0].text.strip() or None
    v['owner_phone'] = owner_phone
#    owner_phone=tree.xpath("id('wrapper2')/div[1]/div[3]/div[2]/div[1]/div[1]") and tree.xpath("id('wrapper2')/div[1]/div[3]/div[2]/div[1]/div[1]")[0].text.strip() or None
#    v['owner_phone'] = owner_phone
    owner_name=CSSSelector("div.manager_div p")(tree)[0] !=None and CSSSelector("div.manager_div p")(tree)[0].text.strip() or None
#    owner_name=tree.xpath("id('wrapper2')/div[1]/div[2]/div[2]/p[1]") and tree.xpath("id('wrapper2')/div[1]/div[2]/div[2]/p[1]")[0].text.strip() or None
    v['owner_name'] = owner_name
    house_title=CSSSelector("div.detail_title h1")(tree)[0] !=None and CSSSelector("div.detail_title h1")(tree)[0].text.strip() or None
#    house_title=tree.xpath("id('wrapper2')/div[1]/div[1]/div[1]/h1") and tree.xpath("id('wrapper2')/div[1]/div[1]/div[1]/h1")[0].text.strip() or None
    v['house_title'] = house_title
    
    if re.search(house_type_regex2, response):
        house_type=re.search(house_type_regex2, response).group(1)
        v['house_type'] = house_type
    else:
        v['house_type'] = None
    house_desc=CSSSelector("div#id_description")(tree)
    house_desc=getText(house_desc[0].getchildren())
#    house_desc=tree.xpath("id('id_description')") and tree.xpath("id('id_description')/div/text()") or None
#    house_desc="\r\n".join([ etree.HTML(e).xpath("/html/body/text()") for e in house_desc ])
    v['house_desc'] = house_desc.replace("联系我时请说明是从赶集网上看到的","")
    
    if re.search(cityarea_regex, response):
        cityarea=re.search(cityarea_regex, response).group(1)
        if "href" in cityarea:
            cityarea=etree.HTML(cityarea).xpath("/html/body/a")[0].text.encode('raw_unicode_escape')
        
        v['cityarea'] = cityarea
    else:
        v['cityarea'] = None
    
    if re.search(borough_section_regex, response):
        borough_section=re.search(borough_section_regex, response).group(1)
        if "href" in borough_section:
            borough_section=etree.HTML(borough_section).xpath("/html/body/a")[0].text.encode('raw_unicode_escape')
        
        v['borough_section'] = borough_section
    else:
        v['borough_section'] = None
    
#    borough_section=tree.xpath("id('wrapper2')/div[1]/div[1]/ul[1]/li[3]") and tree.xpath("id('wrapper2')/div[1]/div[1]/ul[1]/li[3]/text()")[1].strip() or None
#    v['borough_section'] = borough_section.replace("(","").replace(")","")
    
    
    if re.search(house_age_regex, response):
        house_age=re.search(house_age_regex, response).group(1)
        v['house_age'] = house_age
    else:
        v['house_age'] = None
    
    
    
    if re.search(house_fitment_regex, response):
        house_fitment=re.search(house_fitment_regex, response).group(1)
        v['house_fitment'] = house_fitment
    else:
        v['house_fitment'] = None
    
    borough_name=tree.xpath("id('wrapper2')/div[1]/div[1]/ul[1]/li[3]/a") and tree.xpath("id('wrapper2')/div[1]/div[1]/ul[1]/li[3]/a")[0].text.strip() or None
    v['borough_name'] = borough_name
    
    if re.search(hous_addr_regex, response):
        hous_addr=re.search(hous_addr_regex, response).group(1)
        v['hous_addr'] = hous_addr
    else:
        v['hous_addr'] = None
    if re.search(lngLat_regex, response):
        lngLat=re.search(lngLat_regex, response).group(1)
        if "," in lngLat:
            v['px']=lngLat.split(",")[0]
            v['py']=lngLat.split(",")[1]
    else:
        v['px']=None
        v['py']=None
    
    
    return v
    
    
    
    
    
    
def ChuZu(url):
    v={}
    v['city'] = urlparse(url)[1].replace('.ganji.com',"")
    v["owner_phone_area"]=""
    v["belong"]=""
    request = urllib2.Request(url, None, header)
    response =page# urllib2.urlopen(request).read()
    tree = etree.HTML(response)
    if re.search(house_floor_regex, response):
        house_floor=re.search(house_floor_regex, response).group(1)
        house_topfloor=re.search(house_floor_regex, response).group(2)
        v['house_floor'] = house_floor
        v['house_topfloor'] = house_topfloor
    else:
        v['house_floor'] = None
        v['house_topfloor'] = None 
    
    if re.search(house_totalarea_regex, response):
        house_totalarea=re.search(house_totalarea_regex, response).group(1)
        v['house_totalarea'] = house_totalarea
    else:
        v['house_totalarea'] = None
    
    if re.search(house_price_regex_2, response):
        house_price=re.search(house_price_regex_2, response).group(1)
        v['house_price'] = house_price
    else:
        v['house_price'] = None
#    house_price=tree.xpath("/html/body/div[2]/div/div/ul/li/span") and tree.xpath("/html/body/div[2]/div/div/ul/li/span")[0].text.strip() or None    
#    v['house_price'] = house_price
    
    posttime=CSSSelector('span.pub_time')(tree)!=None and CSSSelector('span.pub_time')(tree)[0].text.strip() or None 
    if posttime:
        Y=int(time.strftime('%Y', time.localtime()))
        M=int(posttime.split(' ')[0].split('-')[0])
        D=int(posttime.split(' ')[0].split('-')[1])
        s = datetime.datetime(Y,M,D,0,0)
        posttime=int(time.mktime(s.timetuple()))
        v['posttime'] =posttime 
    else:
        v['posttime'] =None
    
    if re.search(house_type_regex, response):
        house_type=re.search(house_type_regex, response).group(1)
        try:
            house_type=house_type.strip()
        except:
            pass
        blank=house_type.rfind(" ")
        if house_type.find("室")!= -1:
            house_room=house_type[blank+1:house_type.find("室")]
            blank=house_type.find("室")+3
        else:
            house_room=None
        if house_type.find("厅")!=-1:
            house_hall=house_type[blank:house_type.find("厅")]
            blank=house_type.find("厅")+3
        else:
            house_hall=None
        if house_type.find("卫")!=-1:
            house_toilet=house_type[blank:house_type.find("卫")]
        else:
            house_toilet=None
        
            
        v['house_room'] = house_room
        v['house_hall'] = house_hall
        v['house_toilet'] = house_toilet
    else:
        v['house_room'] = None
        v['house_hall'] = None
        v['house_toilet'] = None
    
    if re.search(house_toward_regex, response):
        house_toward=re.search(house_toward_regex, response).group(1)
        v['house_toward'] = house_toward
    else:
        v['house_toward'] = None
    
    owner_phone=CSSSelector("div.ganji_phone_call_class")(tree)[0]!=None and CSSSelector("div.ganji_phone_call_class")(tree)[0].text.strip() or None
    v['owner_phone'] = owner_phone
#    owner_phone=tree.xpath("id('wrapper2')/div[1]/div[3]/div[2]/div[1]/div[1]") and tree.xpath("id('wrapper2')/div[1]/div[3]/div[2]/div[1]/div[1]")[0].text.strip() or None
#    v['owner_phone'] = owner_phone
    
    owner_name=CSSSelector("div.manager_div p")(tree)[0] !=None and CSSSelector("div.manager_div p")(tree)[0].text.strip() or None
    v['owner_name'] = owner_name
    
    house_title=CSSSelector("div.detail_title h1")(tree)[0] !=None and CSSSelector("div.detail_title h1")(tree)[0].text.strip() or None
    v['house_title'] = house_title
#    house_title=tree.xpath("id('wrapper2')/div[1]/div[1]/div[1]/h1") and tree.xpath("id('wrapper2')/div[1]/div[1]/div[1]/h1")[0].text.strip() or None
#    v['house_title'] = house_title
    if re.search(house_type_regex2, response):
        house_type=re.search(house_type_regex2, response).group(1)
        v['house_type'] = house_type
    else:
        v['house_type'] = None
    house_desc=CSSSelector("div#id_description")(tree)
    house_desc=getText(house_desc[0].getchildren())
#    house_desc=tree.xpath("id('id_description')/div/div") and tree.xpath("id('id_description')/div/div/text()") or None
    house_desc="".join(house_desc)
    v['house_desc'] = house_desc.replace("联系我时请说明是从赶集网上看到的","")
    
    if re.search(cityarea_regex, response):
        cityarea=re.search(cityarea_regex, response).group(1)
        if "href" in cityarea:
            cityarea=etree.HTML(cityarea).xpath("/html/body/a")[0].text.encode('raw_unicode_escape')
        
        v['cityarea'] = cityarea
    else:
        v['cityarea'] = None
        
    
    if re.search(borough_section_regex, response):
        borough_section=re.search(borough_section_regex, response).group(1)
        if "href" in borough_section:
            borough_section=etree.HTML(borough_section).xpath("/html/body/a")[0].text.encode('raw_unicode_escape')
        
        v['borough_section'] = borough_section
    else:
        v['borough_section'] = None
#    borough_section=tree.xpath("id('wrapper2')/div[1]/div[1]/ul[1]/li[3]") and tree.xpath("id('wrapper2')/div[1]/div[1]/ul[1]/li[3]/text()")[1].strip() or None
#    v['borough_section'] = borough_section.replace("(","").replace(")","")
    
    if re.search(house_age_regex, response):
        house_age=re.search(house_age_regex, response).group(1)
        v['house_age'] = house_age
    else:
        v['house_age'] = None
    if re.search(house_fitment_regex, response):
        house_fitment=re.search(house_fitment_regex, response).group(1)
        v['house_fitment'] = house_fitment
    else:
        v['house_fitment'] = None
    
    borough_name=tree.xpath("id('wrapper2')/div[1]/div[1]/ul[1]/li[3]/a") and tree.xpath("id('wrapper2')/div[1]/div[1]/ul[1]/li[3]/a")[0].text.strip() or None
    v['borough_name'] = borough_name
    
    if re.search(hous_addr_regex, response):
        hous_addr=re.search(hous_addr_regex, response).group(1)
        v['hous_addr'] = hous_addr
    else:
        v['hous_addr'] = None

    if re.search(lngLat_regex, response):
        lngLat=re.search(lngLat_regex, response).group(1)
        if "," in lngLat:
            v['px']=lngLat.split(",")[0]
            v['py']=lngLat.split(",")[1]
    else:
        v['px']=None
        v['py']=None
    if re.search(house_support_regex, response):
        house_support=re.search(house_support_regex, response).group(1)
        v['house_support'] = house_support
    else:
        v['house_support'] = None    
        
    if re.search(house_deposit_regex, response):
        house_deposit=re.search(house_deposit_regex, response).group(1)
        v['house_deposit'] = house_deposit
    else:
        v['house_deposit'] = None     
    return v
#    house_deposit=tree.xpath("id('wrapper2')/div[1]/div[1]/ul[1]/li[1]") and tree.xpath("id('wrapper2')/div[1]/div[1]/ul[1]/li[1]/text()") or None
#    house_deposit="".join(house_deposit)
#    house_deposit=house_deposit[house_deposit.find("(")+1:house_deposit.find(")")]
#    v['house_deposit'] = house_deposit

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
def makePostData(dict):
    params=""
    for item in dict.items():
        params+="&%s=%s"%(item[0],item[1])
    return  params;
def getSID():
    Y=int(time.strftime('%Y', time.localtime()))
    M=int(time.strftime('%m', time.localtime()))
    D=int(time.strftime('%d', time.localtime()))
    s = datetime.datetime(Y,M,D,0,0,0)
    sidtime=int(time.mktime(s.timetuple()))
    sidtime= int(time.time()-sidtime)*1000*1000+random.randint(1000, 9999)
    return str(sidtime)
def getGanji_uuid():
    k=int("%s"%("%s"%time.time()).replace(".","%s"%random.randint(0,9)))
    m=random.randint(10000000,99999999)
    lp="%s%s"%(k,random.randint(1,9))
    o=len(lp)
    print o
    p=[];
    while o>0:
        o=o-1
        p.append(lp[o:o+1])
    n="".join(p)
    return "%s%s"%((int(n) + m) , m)
def publish(type,ifiles):
    types={
           "zufang":"http://anshan.ganji.com/common/pub.php?category=housing&type=1",
           "rizufang":"http://anshan.ganji.com/common/pub.php?category=housing&type=10",
           "qiuzu":"http://anshan.ganji.com/common/pub.php?category=housing&type=2",
           "chushou":"http://anshan.ganji.com/common/pub.php?category=housing&type=5",
           "qiugou":"http://anshan.ganji.com/common/pub.php?category=housing&type=4",
           }   
    pay_type={
              "1":"押一付三",
                "2":"面议",
                "3":"押一付一",
                "4":"押一付二",
                "5":"押二付一",
                "9":"押二付三",
                "6":"半年付不押",
                "7":"年付不押",
                "8":"押一付半年",
              }
    fields=[
            ('MAX_FILE_SIZE','5242880'),
            ('rt','http://my.anjuke.com/v2/ajax/uploadcallback/'),
            ('comment','8'),
            ]
    cookiestore=cookielib.MozillaCookieJar()
    
    getheader={
               "User-Agent": "Mozilla/5.0 (Windows NT 5.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
               }
    request = urllib2.Request(types[type], None, getheader)
    cookiestore.add_cookie_header(request)
    br = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiestore))
    response=br.open(request).read()
    imagesdata=[]
    ###########################################
    for ifile in ifiles:
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
        request = urllib2.Request("http://www.ganji.com/swftool/uploader2/includes/upload.php", upload_data, uploadheader)
        cookiestore.add_cookie_header(request)
        br = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiestore))
        json=br.open(request).read()
        print json
        #js.dumps()
        jsondict=js.loads(json)
        if jsondict["error"]==0:
            imgid="tmp%s"%("%s"%time.time()).replace(".","%s"%random.randint(0,9))
            imgsdict={}
            imgdict={}
            imgdict["image"]=jsondict["info"][0]["url"]
            imgdict["thumb_image"]=jsondict["info"][0]["thumbUrl"]
            imgdict["row_id"]=""
            imgdict["is_new"]=True
            imgdict["id"]=imgid
            imgsdict[imgid]=imgdict
            imagesdata.append(imgsdict)        
            
    ####################################################
    imagesdata.append({})
    publishdoct={
                 "title":"文慧明圆插件租",
                 "xiaoqu":"慧明圆插件插件出租",
                 "district_id":"0,铁东",
                 "street_id":"-1,不限",
                 "xiaoqu_address":"慧明圆插件",
                 "agent":"0",
                 "rent_mode":"1",#1 整租,2合租
                 "huxing_shi":"1",
                 "huxing_ting":"1",
                 "huxing_wei":"1",
                 "area":"30",
                 "price":"500",
                 "pay_type_int":"1",
                 "description":"慧明圆插件出租文慧明圆插件插件出租",
                 "phone":"13425478568",
                 "person":"是读书热",
                 "images":js.dumps(imagesdata)=="[{}]" and  "" or js.dumps(imagesdata) ,
                 "latlng":"",
                 "password":"111111",
                 "checkcode":"",
                 "act":"submit",
                 "major_category":"1",
                 "pinyin":"",
                 }
    content_type, params = uploadfile(publishdoct.items(), [])
    print params
    publishheader={
           "User-Agent": "Mozilla/5.0 (Windows NT 5.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
           "Referer":types[type],
           'Content-Type': content_type,
           'Content-Length': str(len(params))
           }
    sid = cookielib.Cookie(version=0, name='_gl_tracker', value=getSID(), port=None, port_specified=False, domain='ganji.com', domain_specified=False, domain_initial_dot=False, path='/', path_specified=True, secure=False, expires=None, discard=True, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False)
    cookiestore.set_cookie(sid)
    citydomain = cookielib.Cookie(version=0, name='citydomain', value="anshan", port=None, port_specified=False, domain='ganji.com', domain_specified=False, domain_initial_dot=False, path='/', path_specified=True, secure=False, expires=None, discard=True, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False)
    cookiestore.set_cookie(citydomain)
    ganji_uuid = cookielib.Cookie(version=0, name='ganji_uuid', value=getGanji_uuid(), port=None, port_specified=False, domain='ganji.com', domain_specified=False, domain_initial_dot=False, path='/', path_specified=True, secure=False, expires=None, discard=True, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False)
    cookiestore.set_cookie(ganji_uuid)
    ganji_uuid_bak2 = cookielib.Cookie(version=0, name='ganji_uuid_bak2', value="2", port=None, port_specified=False, domain='ganji.com', domain_specified=False, domain_initial_dot=False, path='/', path_specified=True, secure=False, expires=None, discard=True, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False)
    cookiestore.set_cookie(ganji_uuid_bak2)
    
    request = urllib2.Request("http://anshan.ganji.com/common/pub.php?category=housing&type=3",params , publishheader)
    br = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiestore),urllib2.HTTPRedirectHandler())
#    request.add_data(params)
    response=br.open(request).read()
    print response
    
    
#    response =urllib2.urlopen(request).read()
    
    
#    url="http://www.ganji.com/swftool/uploader2/includes/upload.php"
#    req.add_data(postdata)
if __name__=="__main__":
    
#    v=QiuGou("http://bj.ganji.com/fang1/tuiguang-1227717.htm")
#    v=ChuShou("http://sh.ganji.com/fang5/tuiguang-3352073.htm")
#    v=ChuZu("http://sh.ganji.com/fang1/tuiguang-3108934.htm")
#    for d in v.items():
#        print d[0],d[1]

    publish("zufang",["d:\\test.jpg"])


#class QiuZhu(object):
#    def __init__(self,url):
#        self.url=url
#        self.Page=""
#    def getPage(self):
#        response = urllib2.urlopen(self.url).read()  
#        