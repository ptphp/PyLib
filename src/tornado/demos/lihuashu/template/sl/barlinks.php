<?php $cur_action = $request -> action();?>
<?php $cur_user = $request -> param('id');?>

<?php $count = count($menu['barlinks']);?>
<?php $i = 1;?>

<?php foreach ($menu['barlinks'] as $item => $value):?>
	<?php if ($cur_action == $menu['barlinks'][$item]['href']):?>
		<span class="selected"><?php echo __($item);?></span>
	<?php else:?>
		<a href="<?php echo Url::site($cur_user.'/'.$menu['barlinks'][$item]['href'], true);?>" ><?php echo __($item);?></a>
	<?php endif;?>

	<?php if($i < $count):?>
		&nbsp;·&nbsp;
	<?php endif;?>
	<?php $i++ ;?>

<?php endforeach;?>
