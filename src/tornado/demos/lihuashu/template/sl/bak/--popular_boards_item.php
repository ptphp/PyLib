<?php $boards = LHS::boards(40);?>
<?php foreach ($boards as $board):?>

<div data-id="<?php echo $board['board_id'] ; ?>" data-seq="<?php echo $board['board_id'] ; ?>" class="Board wfc" style="margin-bottom:15px;">
	<h3><?php echo $board['title'] ; ?></h3>
	<div class="pin-count">(<?php echo $board['pin_count'] ; ?>)</div>
	<a href="<?php echo Url::site('boards').'/'.$board['board_id'], true;?>" class="link x">
		<?php $files = LHS::files($board['board_id']);?>
		<?php foreach ($files as $file):?>
			<img src="<?php echo $site['imgserver'].'/';?><?php echo $file['key'] ;?>_sq75">
		<?php endforeach;?>
	</a>
</div>

<?php endforeach;?>