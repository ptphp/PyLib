
<?php $user_info = LHS::get_user();?>

<div id="user_info" class="pin wfc" style="margin-bottom:15px;">
    <div id="Profile">
        <div class="profile-basic">
            <a href="<?php echo Url::site($user_info['urlname'], true);?>" title="runlau" class="img x">
            	<img width="64px" height="64px" src="<?php echo $site['imgserver'].$user_info['avatarkey'].'_sq75';?>">
            </a>
            <a href="<?php echo Url::site($user_info['urlname'], true);?>" class="userlink"><?php echo $user_info['username'];?></a>
            <a href="<?php echo Url::site('settings', true);?>" class="settings">帐号设置</a>
        </div>
        <div class="profile-stats">
            <a href="<?php echo Url::site($user_info['urlname'].'/pins', true);?>"><strong>1</strong>采集</a>
            <a href="<?php echo Url::site($user_info['urlname'].'/pins', true);?>"><strong>5</strong>画板</a>
            <a href="<?php echo Url::site($user_info['urlname'].'/followers', true);?>"><strong>0</strong>粉丝</a>
        </div>
        <div class="profile-acts convo">
            <div class="links">
                <a href="<?php echo Url::site('invites', true);?>" class="btn wbtn"><strong><em></em> 查找邀请好友</strong><span></span></a>
            </div>
            <a color="red" href="#" title="添加" size="11" class="add">添加</a>
        </div>
    </div>
</div>

<script type="text/javascript">
$("#Profile a.add").click(function(){

    $.zxxbox.ajax(
        "<?php echo Url::site('ajax/add', true);?>",
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
            },
        }
    );

});
</script>