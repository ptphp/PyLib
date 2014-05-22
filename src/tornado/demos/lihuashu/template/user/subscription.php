<a id="settings_return" href="<?php echo Url::site('settings');?>">返回</a>

<div class="wfx">
    <form id="subscription_settings" action="<?php echo Url::site('settings/subscription');?>" method="post" class="Form StaticForm">
        <h3>修改订阅设置</h3>
        <ul>
            <li>
                <label>
                    <input type="checkbox" name="weekly" checked="checked">订阅花瓣周刊
                </label>
            </li>
        </ul>
        <div class="Submit">
            <a id="submit_btn" href="#" onclick="$('#subscription_settings').submit();return false;" class="btn btn24 rbtn"><strong> 提交</strong><span></span></a>
        </div>
    </form>
</div>
