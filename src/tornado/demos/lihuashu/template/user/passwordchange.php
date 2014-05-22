<a id="settings_return" href="<?php echo Url::site('settings', true);?>">返回</a>

<div class="wfx profile">

    <form id="profile_edit" action="<?php echo Url::site('password/change');?>" method="post" name="profile_edit" class="Form StaticForm">
        <h3>修改密码</h3>
        <ul>
            <li>
                <label for="id_old_password">
                    当前密码
                </label>
                <div class="Right">
                    <input id="id_old_password" type="password" name="password[old]"><span class="help_text">安全起见，请先输入当前密码。
                        <br>
                        如果没有设置过密码，不用输入。
                    </span>
                </div>
            </li>
            <li>
                <label for="id_new_password">
                    新密码
                </label>
                <div class="Right">
                    <input id="id_new_password" type="password" name="password[new]"><span class="help_text">密码必须为6-32个字符</span>
                </div>
            </li>
            <li>
                <label for="id_confirm_password">
                    确认新密码
                </label>
                <div class="Right">
                    <input id="id_confirm_password" type="password" name="password[confirm]"><span class="help_text">再输一次新密码</span>
                </div>
            </li>
        </ul>
        <div class="Submit">
            <a id="submit_btn" href="#" onclick="$('#profile_edit').submit();return false;" class="btn btn24 rbtn"><strong> 保存密码</strong><span></span></a>
        </div>
    </form>

</div>
