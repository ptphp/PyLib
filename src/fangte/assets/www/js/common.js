$(document).delegate('#goLogin', 'click', function() {
	l_username = $("#l_username").val();
	l_password = $("#l_password").val();
	
	if(l_username == ''){
		dialogAlert(this,"手机号不能为空！");
		return;
	}
	if(l_password == ''){
		dialogAlert(this,"密码不能为空！");
		return;
	}
	var param={};
	param = {username:l_username,password:l_password};
	$.ajax({
		data:param,
		type:"post",
		url:"/auth/login",
		dataType:"text",
		success:function(data){
			res = eval('('+data+')');
			if(res.code == 1){		
				location.href="/";
			}
			else{	
				//alert(res.msg);			
				$("#notice").text(res.msg);
				return;
			}
		}
	});
	  
})
$(document).delegate('#goReg', 'click', function() {
	city = $("#city").val();
	username = $("#username").val();
	password = $("#password").val();
	repassword = $("#repassword").val();
	if(city == ''){
		dialogAlert(this,"城市不能为空！");
		return;
	}
	if(username == ''){
		dialogAlert(this,"手机号不能为空！");
		return;
	}
	if(password == ''){
		dialogAlert(this,"密码不能为空！");
		return;
	}
	if(repassword == ''){
		dialogAlert(this,"重复密码不能为空！");
		return;
	}
	if(repassword != password){
		dialogAlert(this,"两次输入的密码不一样");
		return;
	}
	var param={};
	param = {username:username,password:password,city:city};
	
	$.ajax({
		data:param,
		type:"post",
		url:"/auth/sign",
		dataType:"text",
		success:function(data){
			res = eval('('+data+')');
			if(res.code == 1){		
				location.href="/auth";
			}
			else{	
				//alert(res.msg);			
				$("#notice").text(res.msg);
				return;
			}
		}

	});
	  
})
function dialogAlert(d,m){
	message="<div style=\"padding:30px\">"+m+"</div>";
	$(d).simpledialog({
	    'mode' : 'bool',
	    'prompt' : message,
	    'buttons' : {
	      '确定': {
	    	theme: "b",
	        click: function () {
	          //$('#dialogoutput').text($('#dialoglink').attr('data-string'));
	        }
	      },
	    }
	  })
}
function stringFormat(str,args){	
	var result = str;
	for (var key in args) {
        if(args[key]!=undefined){
            var reg = new RegExp("({" + key + "})", "g");
            result = result.replace(reg, args[key]);
        }
    }
	return result;
}
$(document).bind( "pagebeforechange", function( e, data ) {
	if ( typeof data.toPage === "string" ) {
		var u = $.mobile.path.parseUrl( data.toPage ),re = /^#house_.*/;					
		if ( u.hash.search(re) !== -1 ) {	
			showContent( u, data.options );	
			e.preventDefault();
		}
	}
});

function showContent( urlObj, options )
{
	var flag = urlObj.hash.replace( /.*flag=/, "" ),
	houseid = urlObj.hash.replace( /.*houseid=/, "" ),
	pageSelector = urlObj.hash.replace( /\?.*$/, "" );
	if(pageSelector =="#house_list"){					
		if ( flag ) {
			var param = {};
			param = {flag:flag}
			url = "http://mobile.fangtee.com/house/index?callback=?";
			$.getJSON(url,param, function(data){
				parseLists(pageSelector,data.Rows,urlObj,options);						
		    });						
		}

	}else if(pageSelector =="#house_detail"){
		url = "http://mobile.fangtee.com/house/detail?id="+houseid+"&callback=?";
		$.getJSON(url, function(data){
			parseDetail(pageSelector,data,urlObj,options);						
	    });		
	}else if(pageSelector =="#house_map"){
		$.getScript("http://www.google.com/jsapi?key=ABQIAAAAahcO7noe62FuOIQacCQQ7RTHkUDJMJAZieEeKAqNDtpKxMhoFxQsdtJdv3FJ1dT3WugUNJb7xD-jsQ",function(){
			
			google.load("maps", "3", {'other_params':'sensor=true'});
			
			$(document).bind("mobileinit", function () {
				$.mobile.ajaxEnabled  = true;
			});
			$('#house_map').live("pageshow", function() {
				$('#map_canvas_1').gmap({'center': getLatLng()});
				function getLatLng() {
					if ( google.loader.ClientLocation != null ) {
						return new google.maps.LatLng(google.loader.ClientLocation.latitude, google.loader.ClientLocation.longitude);	
					}
					return new google.maps.LatLng(31, 122);
				}
			});
			// To stop the click from looping into nonsense
			$('#house_map').live("pagecreate", function() {
				$('#submit').click(function() {
					$('#map_canvas_1').gmap('displayDirections', { 'origin': $('#from').val(), 'destination': $('#to').val(), 'travelMode': google.maps.DirectionsTravelMode.DRIVING }, { 'panel': document.getElementById('directions')}, function(success, response) {
						if ( success ) {
							$('#results').show();
						} else {
							$('#map_canvas_1').gmap('getService', 'DirectionsRenderer').setMap(null);
							$('#results').hide();
						}
					});
					return false;
				});
			});

			
		});	
		$.getScript("jquery.ui.map.js");
	}
	
}
function setDetail(tag,res){
	data = res.detail;
	dd 	 = res.dd
	if(tag=="house_type"){
		$("#detail_"+tag).text(dd.house_type[data[tag]]["di_caption"]);
	}else if(tag=="toward"){
		$("#detail_"+tag).text(dd.toward[data[tag]]["di_caption"]);
	}else if(tag=="fitment"){
		$("#detail_"+tag).text(dd.fitment[data[tag]]["di_caption"]);
	}else if(tag=="deposit"){
		$("#detail_"+tag).text(dd.deposit[data[tag]]["di_caption"]);
	}else if(tag=="belong"){
		$("#detail_"+tag).text(dd.belong[data[tag]]["di_caption"]);
	}else if(tag=="toward"){
		$("#detail_"+tag).text(dd.toward[data[tag]]["di_caption"]);
	}else{
		$("#detail_"+tag).text(data[tag]);
	}
	
}
function parseDetail(pageSelector,data,urlObj,options){
	
	var $page = $( pageSelector );
	//$content = $page.find( ".content-primary" );
	setDetail("title",data);
	setDetail("price",data);
	setDetail("area",data);
	setDetail("room",data);
	setDetail("hall",data);
	setDetail("toilet",data);
	setDetail("toward",data);
	setDetail("fitment",data);
	setDetail("house_desc",data);
	setDetail("floor",data);
	setDetail("topfloor",data);
	var $page = $( pageSelector ),
	
	
	phtml = '';
	$.each(data.pics,function(i,row){
		phtml += "<p><center><img src='"+row.pic_url+"'></center></p>";
	});
	$("#house_detail_piclists").html(phtml);
	$house = $page.find( "#house_detail_to_list" );
	$house.attr("href","#house_list?flag="+data.detail['house_flag']);
	options.dataUrl = urlObj.href;
	$.mobile.changePage( $page, options );
	
}
function parseLists(pageSelector,data,urlObj,options){
	
	var $page = $( pageSelector ),
	$content = $page.find( ".content-primary" );
	html = "";
	html += '<li style="height:110px">';
	html += '<a href="#house_detail?houseid={id}">';
	html += '	<img style="padding:10px 0 0 10px;" src="{thumb}" />';
	html += '	<h3>{title}</h3>';
	html += '	<p style="line-height:20px">{house_desc}</p>';
	html += '<p style="line-height:20px"><em style="font-size:16px;padding:0 10px 0 10px;font-weight:700">{room}</em>室<em style="font-size:16px;padding:0 10px 0 10px;font-weight:700">{hall}</em>卫 房龄:<em style="font-size:16px;padding:0 10px 0 10px;font-weight:700">{age}</em>年</p>';
	html += '	<p class="ui-li-aside" style="padding-right:20px">';
	html += '<strong>总价</strong><em style="font-size:20px;color:red;padding:0 10px 0 10px;font-weight:700">{price}</em>万<br>';
	html += '<span style="line-height:30px"><strong>楼层</strong>第{floor}层/共{topfloor}层</span></p></a></li>';									
	markup = "<ul data-role='listview' data-inset='true'>",
	
	$.each(data,function(i,row){
		//row[]
		markup += stringFormat(html,row);							
	})
					
	markup += "</ul>";

	$content.html( markup );
	$page.page();
	$content.find( ":jqmData(role=listview)" ).listview();
	options.dataUrl = urlObj.href;
	$.mobile.changePage( $page, options );
}

