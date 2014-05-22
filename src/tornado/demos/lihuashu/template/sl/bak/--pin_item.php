<?php $pins = LHS::pins(40, 'boardid'); ?>
<?php foreach ($pins as $item):?>
	<?php //print_r($item); ?>
	<?php //echo View::factory('sl/pin_item');?>

<div data-id="<?php echo $item['pin_id'] ;?>" data-seq="<?php echo $item['pin_id'] ;?>" class="pin wfc" style="margin-bottom:15px;">
	<div class="hidden">
		<a href="<?php echo Url::site('pins/'.$item['user']['urlname'], true);?>"><?php echo $item['user']['username'] ;?></a>
		采集到
		<a href="<?php echo Url::site('boards/'.$item['board']['board_id'], true);?>"><?php echo $item['board']['title'] ;?></a>
	</div>
	<div class="actions">
		<div class="right">
			<a data-id="<?php echo $item['pin_id'] ;?>" href="#" onclick="return false;" class="like btn btn11 wbtn">
				<strong><em></em>喜欢</strong><span></span>
			</a>
			<a href="#" onclick="return false;" class="comment clickable btn btn11 wbtn">
				<strong><em></em>评论</strong><span></span>
			</a>
		</div>
		<div class="left">
			<a onclick="if (app.forceLogin()) app.showDialog('repin', '<?php echo $item['pin_id'] ;?>'); return false" href="#" class="repin btn btn11 wbtn">
				<strong><em></em>转采</strong><span></span>
			</a>
		</div>
	</div>
	<a href="<?php echo Url::site('pins/'.$item['pin_id'], true);?>" class="img x">
		<img src="<?php echo $site['imgserver'].'/';?><?php echo $item['file']['key'] ;?>_fw192" width="192" height="<?php echo intval($item['file']['height']*192/$item['file']['width']) ;?>" alt="">
	</a>
	<p class="description"><?php echo nl2br($item['raw_text']) ;?></p>
	<p class="stats less"></p>
	<div class="convo attribution clearfix">
		<p>
			<a href="<?php echo Url::site('pins/'.$item['user']['urlname'], true);?>" title="<?php echo $item['user']['username'] ;?>" class="img x">
				<img src="<?php echo $site['imgserver'].'/';?><?php echo $item['user']['avatar']['key'] ;?>_sq75">
			</a>
			<a href="<?php echo Url::site('pins/'.$item['user']['urlname'], true);?>"><?php echo $item['user']['username'] ;?></a>
			&nbsp;采集到&nbsp;
			<a href="<?php echo Url::site('boards/'.$item['board']['board_id'], true);?>"><?php echo $item['board']['title'] ;?></a>
		</p>
		<a title="回复" class="replyButton"></a>
	</div>
	<div style="display:none;" class="comments muted"></div>
</div>


<?php endforeach;?>