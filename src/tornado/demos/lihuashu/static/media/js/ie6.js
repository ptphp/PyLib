
$(document).ready(function(){
	//alert('ie6');
	$('#menu li').hover(function(){
			//$('#menu li ul').css('visibility', 'hidden');
			$(this).find('ul').css('visibility', 'visible');
		},function(){
			$(this).find('ul').css('visibility', 'hidden');
		});

	$("#waterfall .pin .pinimg").live({
		mouseenter: function(){
			$(this).find('.pinact').show();
		},
		mouseleave: function(){
			$(this).find('.pinact').hide();
		}
	});


});