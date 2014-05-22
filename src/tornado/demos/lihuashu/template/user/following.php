<div id="wrapper" class="wrapper bl">
    <div id="ProfileSidebar">
        <?php echo LHS::userprofile($urlname);?>
    </div>

    <div class="UserPinContainner">
        <div id="ctx_bar">
            <p class="bar-links">
            <?php echo View::factory('sl/barlinks');?>
            </p>
        </div>
        
        <div id="waterfall">
            <?php echo View::factory('sl/cheat_corner_stamp');?>
            <?php foreach ($users as $user):?>
                <?php echo LHS::userpin( $user -> userid, 'notdefault' );?>
            <?php endforeach;?>
        </div>

    </div>
    
    <div class="clear"></div>
    <?php echo View::factory('sl/loadingbar');?>
</div>