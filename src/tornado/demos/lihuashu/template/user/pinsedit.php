<a id="settings_return" href="<?php echo Url::site('', true);?>">返回</a>

<div class="wfx">
    <div id="pin_edit_img" class="pin">
        <a href="/pins/2774829/"><img src="http://img.hb.aicdn.com/390248e1fdb278666eb16ee7c6dcd098723bd90e1067a-sRBYcO_fw192"></a>
        <p>
            戒指
        </p>
    </div>
    <form id="pin_edit_form" action="" method="post" class="Form StaticForm">
        <h3>编辑采集</h3>
        <input type="hidden" name="pin_id" value="2774829" id="id_pin_id">
        <ul>
            <li>
                <label>
                    描述
                </label>
                <div class="Right">
                    <div id="ta_holder" class="editable_shadow pin_edit">
                        <textarea rows="2" name="details" cols="40" id="description_pin_edit" class="expand autocomplete_desc" registered-at="registered" autocomplete="off">
                            戒指
                        </textarea>
                        <ul class="ac-choices" style="display: none; z-index: 42; opacity: 0; ">
                        </ul>
                    </div>
                </div>
            </li>
            <li>
                <label for="id_link">
                    来自
                </label>
                <div class="Right">
                    <input type="text" name="link" value="http://digu.com/pin/tjyp6lhqta" id="id_link">
                </div>
            </li>
            <li>
                <label for="id_board">
                    画板
                </label>
                <div class="Right">
                    <input type="hidden" name="board_id" value="440430" id="id_board">
                    <div class="BoardListOverlay">
                    </div>
                    <div class="BoardSelector BoardPicker">
                        <div class="current">
                            <span class="CurrentBoard">创意</span>
                            <span class="DownArrow"></span>
                        </div>
                        <div class="BoardList">
                            <div class="BoardListBody" style="height: 150px; ">
                                <ul>
                                    <li class="BoardCategory" data="440430">
                                        <span>创意</span>
                                    </li>
                                    <li class="BoardCategory" data="440431">
                                        <span>家居</span>
                                    </li>
                                    <li class="BoardCategory" data="440432">
                                        <span>旅行</span>
                                    </li>
                                    <li class="BoardCategory" data="440433">
                                        <span>想要</span>
                                    </li>
                                    <li class="BoardCategory" data="440434">
                                        <span>音乐、电影、图书</span>
                                    </li>
                                </ul>
                            </div>
                            <div class="CreateBoard">
                                <input id="board_name_input" type="text" placeholder="创建新画板"><a href="#" onclick="return false;" class="nf btn btn18 wbtn disabled"><strong> 创建</strong><span></span></a>
                                <div class="CreateBoardStatus">
                                </div>
                            </div>
                        </div>
                    </div>
                    <script>
                        (function(){
                            $$("div.BoardPicker").each(function(a){
                                if (a.retrieve("initialized")) 
                                    return;
                                var b = a.getElement("div.CreateBoard"), c = $("board_name_input"), d = b.getElement("a.btn"), e = b.getElement(".CreateBoardStatus"), f = $(document.body).getHeight() < 400 ? 5 : 8, g = new BoardPicker(a, {
                                    maxVisibleItems: f
                                }), h = new FancyInput(c);
                                (new Button(d, {
                                    click: function(){
                                        var a = c.get("value").trim();
                                        return a == "" ? (e.set("html", "请输入名称"), !1) : (this.disable(), (new Request.JSON({
                                            url: "/boards/",
                                            data: {
                                                title: a
                                            },
                                            onSuccess: function(a){
                                                a.err ? alert(a.msg || app.COMMON_ERRMSG) : g.add(a.board).hide()
                                            },
                                            onFailure: function(){
                                                alert(app.COMMON_ERRMSG)
                                            },
                                            onComplete: function(){
                                                h.setValue(""), this.enable()
                                            }
                        .bind(this)
                                        })).post(), !1)
                                    }
                                })).disable().bind(h), a.store("initialized", !0)
                            })
                        })()
                    </script>
                </div>
            </li>
            <li>
                <label>
                    删除
                </label>
                <div class="Right">
                    <a href="#" onclick="return false;" class="btn-del btn btn18 wbtn"><strong> 删除采集</strong><span></span></a>
                </div>
            </li>
        </ul>
        <div class="Submit">
            <p>
                <a href="#" onclick="$('#pin_edit_form').submit();return false;" class="btn btn24 rbtn"><strong> 保存采集</strong><span></span></a>
            </p>
        </div>
    </form>
</div>
