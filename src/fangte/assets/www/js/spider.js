var threadData;
function initThreadData(){
	threadData = [
			{"id":14,"status":0,"name":"搜房出售","web_flag":4,"city":1,"getPhone":"1","house_flag":1,"t":"1","args":{"timelimit":86400,"city":1,"region":"","option":"","q":""}},
			{"id":13,"status":0,"name":"搜房出租","web_flag":4,"city":1,"getPhone":"1","house_flag":2,"t":"1","args":{"timelimit":86400,"city":1,"region":"","option":"","q":""}},
			{"id":11,"status":0,"name":"搜房求租","web_flag":4,"city":1,"getPhone":"1","house_flag":4,"t":"1","args":{"timelimit":86400,"city":1,"region":"","option":"","q":""}},
			{"id":10,"status":0,"name":"百姓出售","web_flag":3,"city":1,"getPhone":"1","house_flag":1,"t":"1","args":{"timelimit":86400,"city":1,"region":"","option":"","q":""}},
			{"id":9,"status":0,"name":"百姓出租","web_flag":3,"city":1,"getPhone":"1","house_flag":2,"t":"1","args":{"timelimit":86400,"city":1,"region":"","option":"","q":""}},
			{"id":8,"status":0,"name":"赶集出售","web_flag":2,"city":1,"getPhone":"1","house_flag":1,"t":"1","args":{"timelimit":86400,"city":1,"region":"","option":"","q":""}},
			{"id":7,"status":0,"name":"赶集出租","web_flag":2,"city":1,"getPhone":"1","house_flag":2,"t":"1","args":{"timelimit":86400,"city":1,"region":"","option":"","q":""}},
			{"id":6,"status":0,"name":"赶集求购","web_flag":2,"city":1,"getPhone":"1","house_flag":3,"t":"1","args":{"timelimit":86400,"city":1,"region":"","option":"","q":""}},
			{"id":5,"status":0,"name":"赶集求租","web_flag":2,"city":1,"getPhone":"1","house_flag":4,"t":"1","args":{"timelimit":86400,"city":1,"region":"","option":"","q":""}},
			{"id":4,"status":0,"name":"58出售","web_flag":1,"city":1,"getPhone":"1","house_flag":1,"t":"2","args":{"timelimit":86400,"city":1,"region":"","option":"","q":""}},
			{"id":3,"status":0,"name":"58出租","web_flag":1,"city":1,"getPhone":"1","house_flag":2,"t":"1","args":{"timelimit":86400,"city":1,"region":"","option":"","q":""}},
			{"id":2,"status":0,"name":"58求购","web_flag":1,"city":1,"getPhone":"1","house_flag":3,"t":"3","args":{"timelimit":86400,"city":1,"region":"","option":"","q":""}},
			{"id":1,"status":0,"name":"58求租","web_flag":1,"city":1,"getPhone":"1","house_flag":4,"t":"4","args":{"timelimit":86400,"city":1,"region":"","option":"","q":""}}];
	
}

function startSpider(){
	var tData = '{"id":8,"status":0,"name":"赶集出售","web_flag":2,"city":1,"getPhone":"1","house_flag":1,"t":"1","args":{"timelimit":86400,"city":1,"region":"","option":"","q":""}}';
	clientApi.startSpider(tData);
}
function setSpiderState(s){
	$("#SpiderState").text(s);
}
function setSpiderResult(s){
	$("#SpiderResult").text(s);
}
function fetchContent(){
	url = $("#url").val();
	web_flag = $("#d_web_flag").val();
	house_flag = $("#d_house_flag").val();
	city = $("#d_city").val();
	clientApi.fetchContent(url,web_flag,house_flag,city);
}
function fetchConResult(s){
	//$("#d_title").val(s.title);
}

function setSpiderContentUrl(url){
	$("#url").val(url);
}

function getSpiderList(){	
	url = $("#l_url").val();
	web_flag = $("#l_web_flag").val();
	house_flag = $("#l_house_flag").val();
	city = $("#l_city").val();
	clientApi.getSpiderList(url,web_flag,house_flag,city);
}
var urlObj1,options1,pageSelector1;
function showSpiderList( urlObj, options )
{
	var flag = urlObj.hash.replace( /.*flag=/, "" ),
	houseid = urlObj.hash.replace( /.*houseid=/, "" ),
	pageSelector = urlObj.hash.replace( /\?.*$/, "" );
	if(pageSelector =="#spider_list"){					
		if ( flag ) {	
			urlObj1 = urlObj;
			options1 =options1;
			pageSelector = pageSelector1;
			url = $("#l_url").val();
			web_flag = $("#l_web_flag").val();
			house_flag = $("#l_house_flag").val();
			city = $("#l_city").val();
			clientApi.getSpiderList(url,web_flag,house_flag,city);
		}
	}	
}

function parseSpiderList(data){
	var $page = $("#spider_list" ),
	$content = $page.find( ".content-primary" );
	html = "";
	html += '<li style="height:110px">';
	html += '<a href="#spider_detail" onclick="setSpiderContentUrl(\'{url}\')">';
	html += '	<h3>{title}</h3>';
	html += '	<p style="line-height:20px">{url}</p>';
	html += '</a></li>';
	
	markup = "<ul data-role='listview' data-inset='true'>",
	
	$.each(data,function(i,row){
		//row[]
		markup += stringFormat(html,row);							
	})
					
	markup += "</ul>";

	$content.html( markup );
	$page.page();
	$content.find( ":jqmData(role=listview)" ).listview();
	//options1.dataUrl = urlObj1.href;
	//$.mobile.changePage( $page, options1 );
}