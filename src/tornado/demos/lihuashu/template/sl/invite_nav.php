<?php $cur_uri = $request -> uri();?>

<ul id="nav">
<?php foreach ($menu['friends'] as $item => $value):?>
	<li<?php if ($cur_uri == $menu['friends'][$item]['href']):?> class = "selected"<?php endif;?>><a href="<?php echo Url::site($menu['friends'][$item]['href'], true);?>"><?php echo __('friends '.$item);?></a></li>
<?php endforeach;?>
</ul>