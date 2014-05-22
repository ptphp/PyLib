<?php $cur_uri = $request -> uri();?>

<ul id="nav">
<?php foreach ($menu['invites'] as $item => $value):?>
	<li<?php if ($cur_uri == $menu['invites'][$item]['href']):?> class = "selected"<?php endif;?>><a href="<?php echo Url::site($menu['invites'][$item]['href'], true);?>"><?php echo __($item);?></a></li>
<?php endforeach;?>
</ul>