$(function() {

  var resetWidth = function(){
      $('#page>#header>.wrapper, #ctx_bar, #nav_bar .wrapper, #unauth_callout .wrapper').css({
        'width': $container.width()
      });
      $('#view>#header>.wrapper').css({
        'width': $container.width() + 236
      });
      $('#ProfileSidebar').css({
        'left': ($(window).width() - $container.width() + 236)/2 -236
      });
  }

  if ($.browser.msie == true) {
    $(window).resize(function() {
      resetWidth();
    });
  }

  //
  $.Isotope.prototype.reLayout = function( callback ) {

    this[ '_' +  this.options.layoutMode + 'Reset' ]();
    this.layout( this.$filteredAtoms, callback );

    //alert($container.width());
    resetWidth();

  };

  $.Isotope.prototype._getCenteredMasonryColumns = function() {
    this.width = this.element.width();

    var parentWidth = this.element.parent().width();
    // i.e. options.masonry && options.masonry.columnWidth
    var colW = this.options.masonry && this.options.masonry.columnWidth ||
    // or use the size of the first item
    this.$filteredAtoms.outerWidth(true) ||
    // if there's no items, use size of container
    parentWidth;

    var cols = Math.floor(parentWidth / colW);
    cols = Math.max(cols, 1);

    // i.e. this.masonry.cols = ....
    this.masonry.cols = cols;
    // i.e. this.masonry.columnWidth = ...
    this.masonry.columnWidth = colW;

  };

  $.Isotope.prototype._masonryReset = function() {
    // layout-specific props
    this.masonry = {};
    // FIXME shouldn't have to call this again
    this._getCenteredMasonryColumns();
    //this._getSegments();
    var i = this.masonry.cols;
    this.masonry.colYs = [];
    while (i--) {
      this.masonry.colYs.push(0);
    }

    if (this.options.masonry.cornerStampSelector) {
      var $cornerStamp = this.element.find(this.options.masonry.cornerStampSelector),
        stampWidth = $cornerStamp.outerWidth(true) - (this.element.width() % this.masonry.columnWidth),
        cornerCols = Math.ceil(stampWidth / this.masonry.columnWidth),
        cornerStampHeight = $cornerStamp.outerHeight(true);
      for (i = Math.max(this.masonry.cols - cornerCols, cornerCols); i < this.masonry.cols; i++) {
        this.masonry.colYs[i] = cornerStampHeight;
      }
    }

  };


  $.Isotope.prototype._masonryResizeChanged = function() {
    var prevColCount = this.masonry.cols;
    // get updated colCount
    this._getCenteredMasonryColumns();
    return (this.masonry.cols !== prevColCount);
  };

  $.Isotope.prototype._masonryGetContainerSize = function() {
    var unusedCols = 0,
      i = this.masonry.cols;
    // count unused columns
    while (--i) {
      if (this.masonry.colYs[i] !== 0) {
        break;
      }
      unusedCols++;
    }

    return {
      height: Math.max.apply(Math, this.masonry.colYs),
      // fit container to columns that have been used;
      width: (this.masonry.cols - unusedCols) * this.masonry.columnWidth
    };

  };


  var $container = $('#waterfall');

  if ($container.find(".wfc").length + $container.find(".corner-stamp").length > 0) {
    $container.isotope({
      itemSelector: '.wfc',
      masonry: {
        columnWidth: 235,
        cornerStampSelector: '.corner-stamp'
      }
    });
  }

var calls = function(){
  alert('calls');
}
  /*
        var $user_container = $('#wrapper');
        
        $user_container.isotope({
                itemSelector: '.wfc'
        });
*/
  var errorStamp = false;
  var ajaxError = function() {
      //alert('error');
      //$loadingItem.text('Could not load examples :(');
      $('#loading_bar').attr("class", 'stoploading');
      errorStamp = true;
    };

  // dynamically load items using Masonry from server
  var appendItems = function(data) {
      if (!data) {
        ajaxError();
        //alert('nodata');
        return;
      }

      var filter = data.filter.length ? data.filter : false;
      var filter_type = filter.split(":", 1);
      //alert(filter_type);
      var items = [],
        item, datum;

      if (filter_type == "pin") {
        //alert(filter_type);
        // proceed only if we have data
        if (!data.pins.length) {
          ajaxError();
          return;
        }


        for (var i = 0, len = data.pins.length; i < len; i++) {
          mark = data.pins[i];
          // alert(datum.user.urlname);
          //var imgsrc = app.imghost + '' + datum.file.key + '_fw192';
          //var avatarsrc = app.imghost + '' + datum.user.avatar.key + '_sq75';
          //var imgheight = parseInt(192 * datum.file.height / datum.file.width);
          //var userurl = app.host + '' + datum.user.urlname;
          ///var pinurl = app.host + 'pins/' + datum.pin_id;
          //var boardurl = app.host + 'boards/' + datum.board.board_id;
          //var isvideoicon = function(data) {
          //    var videoicon;
           //   if (data == 1) {
            //    videoicon = '<img src="' + app.host + 'media/img/media_video.png' + '" class="video-icon">';
             // } else {
              //  videoicon = '';
              //}
           //   return videoicon;
            //};

          //default style
          //item = '<div data-id="' + datum.pin_id + '" data-seq="' + datum.pin_id + '" class="pin wfc" style="margin-bottom:15px;">' + '<div class="hidden">' + '<a href="' + userurl + '">' + datum.user.username + '</a>' + '采集到' + '<a href="' + boardurl + '">' + datum.board.title + '</a>' + '</div>' + '<div class="actions">' + '<div class="right">' + '<a data-id="' + datum.pin_id + '" href="#" onclick="return false;" class="like btn btn11 wbtn">' + '<strong><em></em>喜欢</strong><span></span>' + '</a>' + '<a href="#" onclick="return false;" class="comment clickable btn btn11 wbtn">' + '<strong><em></em>评论</strong><span></span>' + '</a>' + '</div>' + '<div class="left">' + '<a onclick="if (app.forceLogin()) app.showDialog("repin", "' + datum.pin_id + '"); return false" href="#" class="repin btn btn11 wbtn">' + '<strong><em></em>转采</strong><span></span>' + '</a>' + '</div>' + '</div>' + '<a href="' + pinurl + '" class="img x">' + '<img src="' + imgsrc + '" width="192" height="' + imgheight + '" alt="">' + isvideoicon(datum.media_type) + '</a>' + '<p class="description">' + datum.raw_text + '</p>' + '<p class="stats less"></p>' + '<div class="convo attribution clearfix">' + '<p>' + '<a href="' + userurl + '" title="' + datum.user.username + '" class="img x">' + '<img src="' + avatarsrc + '">' + '</a>' + '<a href="' + userurl + '">' + datum.user.username + '</a>' + '&nbsp;采集到&nbsp;' + '<a href="' + boardurl + '">' + datum.board.title + '</a>' + '</p>' + '<a title="回复" class="replyButton"></a>' + '</div>' + '<div style="display:none;" class="comments muted"></div>' + '</div>';
          //lihuashu style
          //item = '<div data-id="' + datum.pin_id + '" data-seq="' + datum.pin_id + '" class="pin wfc" style="margin-bottom:15px;">' + '<div class="hidden">' + '<a href="' + userurl + '">' + datum.user.username + '</a>' + '采集到' + '<a href="' + boardurl + '">' + datum.board.title + '</a>' + '</div>' + '<div class="pinimg">' + '<a href="' + pinurl + '" class="img x">' + '<img src="' + imgsrc + '" width="192" height="' + imgheight + '" alt="">' + isvideoicon(datum.media_type) + '</a>' + '<div class="pinact">' + '<a href="#" onclick="return false;" class="collect">收藏</a>' + '<a href="#" onclick="return false;" class="like">喜欢</a>' + '<a href="#" onclick="return false;" class="hate">讨厌</a>' + '<a href="#" onclick="return false;" class="comment">评价</a>' + '</div>' + '</div>' + '<p class="description">' + datum.raw_text + '</p>' + '<p class="stats less"></p>' + '<div class="convo attribution clearfix">' + '<p>' + '<a href="' + userurl + '" title="' + datum.user.username + '" class="img x">' + '<img src="' + avatarsrc + '">' + '</a>' + '<a href="' + userurl + '">' + datum.user.username + '</a>' + '&nbsp;采集到&nbsp;' + '<a href="' + boardurl + '">' + datum.board.title + '</a>' + '</p>' + '<a title="回复" class="replyButton"></a>' + '</div><div style="" class="comments muted"></div>' + $.app.commentWrite(datum.pin_id) + '</div>';
		item = '';
		item += '  <div data-id="'+mark.pin.key+'" data-seq="'+mark.pin.key+'" class="pin wfc" style="margin-bottom:15px;">';
		item += '			<div class="pinimg">';
		item += '			<a href="/mark/'+mark.pin.key+'/" class="img x">';
		item += '				<img src="'+mark.thumb.url+'" width="192" height="256" alt="">';
		item += '			</a>';

		item += '			<div class="pinact">';
		item += '				<a href="#" onclick="return false;" class="collect">收藏</a>';
		item += '				<a href="#" onclick="return false;" class="like">喜欢</a>';
		item += '				<a href="#" onclick="return false;" class="hate">讨厌</a>';
		item += '				<a href="#" onclick="return false;" class="comment">评价</a>';
		item += '			</div>';
		item += '		</div>';
		item += '			<p class="description">'+mark.pin.rawtext+'</p>';
					
		item += '			<p class="stats less"></p>';
					
		item += '			<div class="convo attribution clearfix">';
		item += '				<p>';
		item += '					<a href="#/lihuashu/lesliecheung" title="" class="img x">';
		item += '						<img src="/static/media/img/iconor-50x50.png">';
		item += '					</a>';
		item += '					<a href="#/lihuashu/"> /</a>&nbsp;采集到&nbsp;';
		item += '					<a href="#/lihuashu/boards/">'+mark.board.title+'</a>';
		item += '				</p>';
		item += '				<a title="回复" class="replyButton"></a>';
		item += '			</div>';
					
		//item += '			<div style="" class="comments muted">';
		//item += '				<div class="convo attribution clearfix">';
		//item += '					<p><a href="#http://www.lihuashu.org/lihuashu/bono" title="beibei" class="img x">';														
		//item += '						<img src="/static/media/img/iconor-50x50.png">';								
		//item += '						<a href="#http://www.lihuashu.org/lihuashu/bono">'+comment.nickname+'</a>&nbsp;';
		//item += '						'+comment.rawtext+'</p>';
		//item += '						<a title="回复" class="replyButton"></a>';
		//item += '				</div>';


		item += '			</div>';
					
		item += '			<div style="display: none;" class="write convo clearfix">';
		item += '				<a href="/lihuashu/jinlisha1" title="默然相爱寂静喜欢" class="img x ">';
		item += '					<img src="/img/imgs//2b6a2f2cc95fb410102e33db818d8d5a43bd826e3789-hJMYZu_sq75">';
		item += '				</a>';
		item += '				<form action="/lihuashu/pins/3889706/comments" method="POST">';
		item += '					<textarea placeholder="添加评论或把采集@给好友" class="GridComment ani-affected " registered-at="registered" autocomplete="off"></textarea>';
		item += '					<ul class="ac-choices" style="display: none; z-index: 42; opacity: 0; "></ul>';
		item += '					<a href="#" onclick="return false" class="grid_comment_button"></a>';
		item += '				</form>';
		item += '			</div>';
		item += '		</div>';

          items.push(item);
        }
      } else if (filter_type == "board") {

        //alert(filter_type);
        // proceed only if we have data
        if (!data.boards.length) {
          ajaxError();
          return;
        }

        for (var i = 0, boardslen = data.boards.length; i < boardslen; i += 1) {
          //alert(data.boards.length + '--' + i);
          board = data.boards[i];
          // alert(datum.board_id);
          //var pins_avatar_item = [],
            //pins_avatar = '';
          //var boardurl = app.host + 'boards/' + datum.board_id;
          ///var pins = datum.pins;

          //for (var j = 0, pinslen = pins.length; j < pinslen; j += 1) {
            //pins_avatar_item = pins[j];
            //pins_avatar_src = app.imghost + '' + pins_avatar_item.file.key + '_sq75';

            //pins_avatar += '<img src="' + pins_avatar_src + '">';
          //}

          //item = '<div data-id="' + datum.board_id + '" data-seq="' + datum.seq + '" class="Board wfc" style="margin-bottom:15px;">' + '<h3>' + datum.title + '</h3>' + '<div class="pin-count">(' + datum.pin_count + ')</div>' + '<a href="' + boardurl + '" class="link x">' + pins_avatar + '</a>' + '</div>';
		item = '';
		item += '<div data-id="'+board.key+'" data-seq="'+board.key+'" class="Board wfc" style="margin-bottom:15px;">';
		item += '	<h3>'+board.title+'</h3>';
		item += '	<div class="pin-count">('+board.pins.length+')</div>';
		item += '	<a href="/boards/'+board.key+'/" class="link x">';
		$.each(board.pin_pics,function(i,row){			
			item += '		<img src="'+row+'">';
		});		
		item += '	</a>';
		item += '</div>';	
		
          items.push(item);
          //alert(i);
        }

        //alert(items);
      } else if (filter_type == "user") {

      } else {
        alert('else');
      }

      var $items = $(items.join(''));
      $items.imagesLoaded(function() {
        $container.append($items).isotope('appended', $items);
        //$user_container.append( $items )
        //                    .isotope( 'appended', $items );
      });
    };



  //endlessScroll
  $(document).ready(function() {
    //resetWidth();
    if ($container.find(".wfc").length + $container.find(".corner-stamp").length > 1) {
      $(document).endlessScroll({
        bottomPixels: 300,
        fireOnce: true,
        ceaseFire: function() {
          return errorStamp
        },
        callback: function(page) {
          //alert(page);
          //stop loading if reach maxpage
          var cur_href = window.location.href.replace(/#/, '')
          //alert(cur_href);
          var para_con = '?';

          if (cur_href.indexOf("?") > 0) {
            para_con = '&';
          }

          var url = cur_href + para_con + 'page=' + page + '&callback=?';
          //alert(url);
          $.getJSON(url).error(ajaxError).success(appendItems);

        }
      });
    }

  });


  var displayedBack = false;
  var IEversion = $.browser.version.split(".");


  if ($.browser.msie == true && IEversion[0] == 7) {
    $('#elevator').hide();
  } else {
    $(window).scroll(

    function() {
      if ($(document).scrollTop() > 800) {

        if (!displayedBack) {
          $('#elevator').show();
          displayedBack = true;
        }
      } else {
        if (displayedBack) {
          $('#elevator').hide();
          displayedBack = false;
        }
      }
    });
  }

  //$('#elevator').click(function(){$('html,body').animate({scrollTop: '0px'}, 800);});
  $('#elevator').click(
      function() {
          $("html,body").animate({
            scrollTop: 0
          }, 600, function() {
            displayedBack = false;
          });
      });

      $("#nav_user_mentions").pageslide();
      $("#nav_user_activities").pageslide();
      $("#zoomr_show").pageslide({
          direction: "left",
          modal: true
  });

$('.replyButton, .pinact .collect, .pinact .like, .pinact .hate, .pinact .comment').live('click',
    function() {
        //alert('clicked');
        $.app.forceLogin();
});

$('#CloseupComment').focus(function() {
    $('#PinAddCommentControls').show();
});

$('.repin-button a').live('click',
    function() {
    	
    	if(app.logined == false){
    			alert("请先登陆");
    			location.href = "/login/";
    			return "";
    		}
    	
    	
    var pinid = $(this).attr('data-id');
    var repinurl = app.host + 'ajax/repin/' + pinid;
    //alert(pinid);
    $.zxxbox.ajax(
        repinurl,
        {},
        {
            bar: false,
            bg:false,
            //bgclose: true,
            btnclose:false,
            onshow:function(){
                $("body").css("overflow", "hidden");
            },
            onclose:function(){
                $("body").css("overflow", "visible");
            }
        }
    );
});
$('#board_follow11').live('click',
    function() {
    	alert(22);
    }
);


$('#followuser').live('click',
    function() {
    	
    	if(app.logined == false){
    			alert("请先登陆");
    			location.href = "/login/";
    			return "";
    		}
    	
    var key = $(this).attr('data-id');
    var rel = $(this).attr('rel');
    if(rel == 1){    	
    	var url = app.host + 'ajax/removefollowuser/' + key;
    	$.get(url,function(data){
	    	//alert(data);    	
	    	if(data.code == 0){
	    		$('#followuser strong').html("关注");
	    		$('#followuser').attr('rel','0');
	    	}else{
	    		alert(data.msg);
	    	}
	    },"json");
    }else{    	
    	var url = app.host + 'ajax/followuser/' + key;
    	$.get(url,function(data){
	    	//alert(data);    	
	    	if(data.code == 0){
	    		$('#followuser strong').html("取消关注");
	    		$('#followuser').attr('rel','1');
	    	}else{
	    		alert(data.msg);
	    	}
	    },"json");
    }
  
});

$('#board_follow').live('click',
    function() {
    	if(app.logined == false){
    			alert("请先登陆");
    			location.href = "/login/";
    			return "";
    		}
    	
    var key = $(this).attr('data-id');
    var rel = $(this).attr('rel');
    if(rel == 1){    	
    	var url = app.host + 'ajax/removefollow/' + key;
    	$.get(url,function(data){
	    	//alert(data);    	
	    	if(data.code == 0){
	    		$('#board_follow strong').html("关注");
	    		$('#board_follow').attr('rel','0');
	    	}else{
	    		alert(data.msg);
	    	}
	    },"json");
    }else{    	
    	var url = app.host + 'ajax/follow/' + key;
    	$.get(url,function(data){
	    	//alert(data);    	
	    	if(data.code == 0){
	    		$('#board_follow strong').html("取消关注");
	    		$('#board_follow').attr('rel','1');
	    	}else{
	    		alert(data.msg);
	    	}
	    },"json");
    }
  
});

$('.like-button a').live('click',
    function() {
    	
    	if(app.logined == false){
    			alert("请先登陆");
    			location.href = "/login/";
    			return "";
    		}
    	
    var pinid = $(this).attr('data-id');
    var rel = $(this).attr('rel');
    if(rel == 1){    	
    	var url = app.host + 'ajax/removelike/' + pinid;
    	$.get(url,function(data){
	    	//alert(data);    	
	    	if(data.code == 0){
	    		$('.like-button strong').html("<em></em>喜欢");
	    		$('.like-button a').attr('rel','0');
	    	}else{
	    		alert(data.msg);
	    	}
	    },"json");
    }else{
    	
    	var url = app.host + 'ajax/like/' + pinid;
    	$.get(url,function(data){
	    	//alert(data);    	
	    	if(data.code == 0){
	    		$('.like-button strong').html("<em></em>取消喜欢");
	    		$('.like-button a').attr('rel','1');
	    	}else{
	    		alert(data.msg);
	    	}
	    },"json");
    }
  
});

$('.hate-button a').live('click',
    function() {
    	
    	if(app.logined == false){
    			alert("请先登陆");
    			location.href = "/login/";
    			return "";
    		}
    	
    var pinid = $(this).attr('data-id');
    
    var rel = $(this).attr('rel');
    if(rel == 1){    	
    	var url = app.host + 'ajax/removehate/' + pinid;
    	$.get(url,function(data){
	    	//alert(data);    	
	    	if(data.code == 0){
	    		$('.hate-button strong').html("<em></em>讨厌");
	    		$('.hate-button a').attr('rel','0');
	    	}else{
	    		alert(data.msg);
	    	}
	    },"json");
    }else{
    	
    	var url = app.host + 'ajax/hate/' + pinid;
    	$.get(url,function(data){
	    	//alert(data);    	
	    	if(data.code == 0){
	    		$('.hate-button strong').html("<em></em>取消讨厌");
	    		$('.hate-button a').attr('rel','1');
	    	}else{
	    		alert(data.msg);
	    	}
	    },"json");
    }
    
    
  
});



$('.pinact .like').live('click',
    function() {
    	if(app.logined == false){
    			alert("请先登陆");
    			location.href = "/login/";
    			return "";
    		}
	    var pinid = $(this).closest('.pin').attr('data-id');
	    var url = app.host + 'ajax/like/' + pinid;
	    //alert(url);
	    $.get(url,function(data){
	    	alert(data.msg);
	    },"json");
  
});

$('.pinact .hate').live('click',
    function() {
    	if(app.logined == false){
    			alert("请先登陆");
    			location.href = "/login/";
    			return "";
    		}
    	
    	
    	
    var pinid = $(this).closest('.pin').attr('data-id');
    var url = app.host + 'ajax/hate/' + pinid;
    //alert(url);
    $.get(url,function(data){
    	alert(data.msg);
    },"json")
  
});

$('.pinact .collect').live('click',
    function() {
    	
    	
    	if(app.logined == false){
    			alert("请先登陆");
    			location.href = "/login/";
    			return "";
    		}
    	
    var pinid = $(this).closest('.pin').attr('data-id');
    var repinurl = app.host + 'ajax/repin/' + pinid;
    //alert(pinid);
    $.zxxbox.ajax(
        repinurl,
        {},
        {
            bar: false,
            bg:false,
            //bgclose: true,
            btnclose:false,
            onshow:function(){
                $("body").css("overflow", "hidden");
            },
            onclose:function(){
                $("body").css("overflow", "visible");
            }
        }
    );
});


$('.replyButton, .pinact .comment').live('click',
    function() {
        $(this).closest('.pin').find('.write').show();
        $container.isotope();
});

$('.grid_comment_button').live('click',
    function() {
    		if(app.logined == false){
    			alert("请先登陆");
    			location.href = "/login/";
    			return "";
    		}
	        var $currentpin = $(this).closest('.pin');
	        var txt = $currentpin.find('.GridComment').val().trim();
	        var item ='';
	        if(txt == ''){
	          alert('好歹输两个字吧,亲!');
	        }
	        var url = "/ajax/comment/";
	        //alert(url);
	        var pinid = $(this).closest('.pin').attr('data-id');
	        
	        _xsrf = document.cookie.match("\\b_xsrf=([^;]*)\\b")[1];
	        $.post(url,{"text":txt,'_xsrf':_xsrf,'pinid':pinid},function(data){
	            //$("span").html(result);
	        	if(data.code == 1){	        		
	        		alert(data.data);	        		
	        	}else if(data.code == 0){	        		
	        		var comment = data.obj;	        		
	        		if(comment.userInfo.avatar){
	        			avatar_url = comment.userInfo.avatar;
	        		}else{
	        			avatar_url ='/static/media/img/iconor-50x50.png';	        			
	        		}
	        		
		            var item = '<div class="comment convo clearfix">';
		            item += '<a href="#" title="" class="img x"><img src="'+avatar_url+'"></a>';
		            item += '<p><a href="#" class="author">' + comment.userInfo.nickname + '</a>:&nbsp;' + comment.rawtext + '</p>';
		            item += '<a title="回复" class="replyButton"></a>';
		            item += '</div>';
		            $currentpin.find('.comments').append(item);
		            $currentpin.find('.GridComment').val('');
		            $currentpin.find('.write').hide();
		            $container.isotope();		            
	        	}else{	        		
	        		alert("system errot");
	        	}	            
	
	        },"json");
	

        //alert(txt);
});


jQuery.app = {
    foo: function() {
        alert('This is a test. This is only a test.');          
    },
    bar: function(param) {
       alert('This function takes a parameter, which is "' + param + '".');    
    },

    forceLogin: function(){
        //alert('asdf');'{"name":"John"}'
        //alert(app.req.user.avatar.key);
        return app.req.user ? ! 0 : (window.location.href = app.host + "login/?next=" + app.page.url, !1)
    },

    commentWrite: function(pinid){
        var con = '';
        if(app.req.user){
            var commenturl = app.host + 'pins/' + pinid + '/comments';
            var userurl = app.host + app.req.user.urlname;
            var avatarsrc = app.imghost + app.req.user.avatar.key + '_sq75';

            con = '<div style="display: none;" class="write convo clearfix">'
                + '<a href="' + userurl + '" title="' + app.req.user.username + '" class="img x ">'
                + '<img src="' + avatarsrc + '">'
                + '</a>'
                + '<form action="' + commenturl + '" method="POST">'
                + '<textarea placeholder="添加评论给好友" class="GridComment ani-affected " registered-at="registered" autocomplete="off"></textarea>'
                + '<ul class="ac-choices" style="display: none; z-index: 42; opacity: 0; ">'
                + '</ul>'
                + '<a href="#" onclick="return false;" class="grid_comment_button"></a>'
                + '</form>'
                + '</div>';
        }
        return con;
    },

    postComment: function(){
        //alert('haha');
        var txt = $('#CloseupComment').val().trim();
        if(txt == ''){
          alert('好歹输两个字吧,亲!');
        }
        var url = app.host + app.page.url + "/comments";
        //alert(url);
        $.post(url,{"text":txt},function(data){
            //$("span").html(result);
            //alert(data);
            var datum = data.comment;
            //alert(datum.comment_id);

            var item = '<div data-id="' + datum.comment_id + '" class="comment clearfix" style="background-color: transparent; ">'
              + '<div id="comment_action_btns" class="fr">'
              + '<a data-name="' + datum.comment_id + '" title="回复" class="pinViewReplyButton"></a>'
              + '<a data-url="' + url + '/' + datum.comment_id + '" title="删除" class="DeleteComment"></a>'
              + '</div>'
              + '<a href="' + app.host + datum.user.urlname + '" title="' + datum.user.username + '" class="img x">'
              + '<img src="' + app.imghost + datum.user.avatar.key + '_sq75" class="avatar">'
              + '</a>'
              + '<p class="meta">'
              + '<a href="' + app.host + datum.user.urlname + '" class="author">' + datum.user.username + '</a>&nbsp;-&nbsp;<span data-ts="' + datum.created_at + '" class="ts-words">刚才</span>说：'
              + '</p>'
              + '<p class="text">' + datum.raw_text + '</p>'
              + '</div>';

            $('#pin_comments').show(3000).append(item);
            $('#CloseupComment').val('');

        },"json");
    }

/**/



};


});