<a id="settings_return" href="<?php echo Url::site('', true);?>">返回</a>

<div class="wfx">
    <form id="BoardEdit" action="/boards/440430/" method="post" onsubmit="return false;" class="Form StaticForm">
        <input type="hidden" id="id_board_id" name="board_id" value="440430"><h3>编辑画板 /&nbsp;<a href="/boards/440430/">创意</a></h3>
        <ul>
            <li>
                <label for="id_title">
                    标题
                </label>
                <div class="Right">
                    <input type="text" name="title" value="创意" id="id_title">
                </div>
            </li>
            <li>
                <label for="id_description">
                    描述
                </label>
                <div class="Right">
                    <textarea id="id_description" rows="3" cols="40" name="description">
                    </textarea>
                </div>
            </li>
            <li>
                <label>
                    分类
                </label>
                <div class="Right">
                    <input type="hidden" name="category" id="id_category" value="null">
                    <div class="BoardListOverlay">
                    </div>
                    <div class="BoardSelector BoardPicker CategoryPicker">
                        <div class="current">
                            <span class="CurrentBoard">选择分类</span>
                            <span class="DownArrow"></span>
                        </div>
                        <div class="BoardList" style="display: none; ">
                            <div class="BoardListBody">
                                <ul>
                                    <li class="BoardCategory" data="home">
                                        <span>家居</span>
                                    </li>
                                    <li class="BoardCategory" data="travel_places">
                                        <span>旅行</span>
                                    </li>
                                    <li class="BoardCategory" data="food_drink">
                                        <span>美食</span>
                                    </li>
                                    <li class="BoardCategory" data="modeling_hair">
                                        <span>造型/妆发</span>
                                    </li>
                                    <li class="BoardCategory" data="photography">
                                        <span>摄影</span>
                                    </li>
                                    <li class="BoardCategory" data="apparel">
                                        <span>服饰/搭配/街拍</span>
                                    </li>
                                    <li class="BoardCategory" data="kids">
                                        <span>童真</span>
                                    </li>
                                    <li class="BoardCategory" data="wedding_events">
                                        <span>婚纱/婚礼</span>
                                    </li>
                                    <li class="BoardCategory" data="pets">
                                        <span>萌宠</span>
                                    </li>
                                    <li class="BoardCategory" data="diy_crafts">
                                        <span>手工/布艺/玩物</span>
                                    </li>
                                    <li class="BoardCategory" data="design">
                                        <span>创意/设计</span>
                                    </li>
                                    <li class="BoardCategory" data="illustration">
                                        <span>手绘/插画</span>
                                    </li>
                                    <li class="BoardCategory" data="people">
                                        <span>人物</span>
                                    </li>
                                    <li class="BoardCategory" data="film_music_books">
                                        <span>音乐/电影/图书</span>
                                    </li>
                                    <li class="BoardCategory" data="funny">
                                        <span>趣味</span>
                                    </li>
                                    <li class="BoardCategory" data="cars_motorcycles">
                                        <span>汽车</span>
                                    </li>
                                    <li class="BoardCategory" data="beauty">
                                        <span>美女</span>
                                    </li>
                                    <li class="BoardCategory" data="digital">
                                        <span>3C数码</span>
                                    </li>
                                    <li class="BoardCategory" data="men">
                                        <span>男人志</span>
                                    </li>
                                    <li class="BoardCategory" data="sports">
                                        <span>运动/酷玩</span>
                                    </li>
                                    <li class="BoardCategory" data="tips">
                                        <span>生活百科</span>
                                    </li>
                                    <li class="BoardCategory" data="desire">
                                        <span>欲望清单</span>
                                    </li>
                                    <li class="BoardCategory" data="art">
                                        <span>人文艺术</span>
                                    </li>
                                    <li class="BoardCategory" data="architecture">
                                        <span>建筑</span>
                                    </li>
                                    <li class="BoardCategory" data="data_presentation">
                                        <span>数据/图示</span>
                                    </li>
                                    <li class="BoardCategory" data="other">
                                        <span>其它</span>
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </div>
                    <script>
                        (function(){
                            $$("div.CategoryPicker").each(function(a){
                                if (a.retrieve("initialized")) 
                                    return;
                                new CategoryPicker(a), a.store("initialized", !0)
                            })
                        })()
                    </script>
                </div>
            </li>
            <li class="Delete">
                <label>
                    删除
                </label>
                <a data-url="/x155185/" href="#" onclick="return false;" class="btn-del btn btn18 wbtn"><strong> 删除画板</strong><span></span></a>
                <!--if board.is_private--><!--  abtn.btn-hide(size="18", data-url="/#{board.user.urlname}/").disabled 画板已隐藏--><!--else--><!--  abtn.btn-hide(size="18", data-url="/#{board.user.urlname}/") 隐藏画板-->
            </li>
        </ul>
        <div class="Submit">
            <a href="#" onclick="$('#BoardEdit').submit();return false;" class="editpage_submit btn btn24 rbtn"><strong> 保存设置</strong><span></span></a>
        </div>
        <div class="CreateBoardStatus msgr">
        </div>
    </form>
</div>
