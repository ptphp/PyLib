#!user/bin/env python
# -*- coding: utf8 -*- 
urls=[
    (r'/', 'view.default.HomeHandler'),
    (r'/category/([a-z0-9A-Z]*)/', 'view.default.CategoryHandler'),    
    (r'/search/', 'view.pins.SearchHandler'),    
    (r'/invites/', 'view.user.InvitesHandler'),    
    (r'/message/mentions/', 'view.default.MentionsHandler'),    
    (r'/message/activities/', 'view.default.ActivitiesHandler'),    
    
    (r'/popular/', 'view.pins.PopularHandler'),
    (r'/boards/popular/', 'view.board.PopularHandler'),
    (r'/boards/([a-z0-9A-Z]*)/', 'view.board.BoardPinHandler'),    
    
    (r'/settings/','view.user.SettingsHandler'),
    (r'/user/([a-z0-9A-Z]*)/','view.user.MemberHandler'),
    (r'/user/([a-z0-9A-Z]*)/pins/','view.user.MemberPinsHandler'),
    (r'/user/([a-z0-9A-Z]*)/likes/','view.user.MemberLikesHandler'),
    
    (r'/signup/','view.user.RegisterHandler'),
    (r'/login/' ,'view.user.LoginHandler'),
    (r'/logout/','view.user.LogoutHandler'),
    
    (r'/mark/([0-9a-zA-Z]+)/', 'view.pins.MarkHandler'),
    
    (r'/manager/user/','view.user.AdminUserHandler'),
    (r'/manager/user/delete/([0-9a-zA-Z]+)','view.user.AdminDeleteUserHandler'),
    
    (r'/manager/cat/','view.category.AdminCategoryHandler'),
    (r'/manager/cat/new/([0-9a-zA-Z]*)','view.category.AdminCategoryNewHandler'),
    (r'/manager/cat/delete/([0-9a-zA-Z]+)','view.category.AdminDeleteCategoryHandler'),
    
    (r'/manager/board/','view.board.AdminBoardHandler'),
    (r'/manager/board/new/([0-9a-zA-Z]*)','view.board.AdminBoardNewHandler'),
    (r'/manager/board/delete/([0-9a-zA-Z]+)','view.board.AdminDeleteBoardHandler'),
    
    (r'/manager/pin/','view.pins.AdminPinHandler'),
    (r'/manager/pin/new/([0-9a-zA-Z]*)','view.pins.AdminPinNewHandler'),
    (r'/manager/pin/delete/([0-9a-zA-Z]+)','view.pins.AdminDeletePinHandler'),
    
    (r'/manager/comment/','view.comments.AdminCommentHandler'),
    (r'/manager/comment/new/([0-9a-zA-Z]*)','view.comments.AdminCommentNewHandler'),
    (r'/manager/comment/delete/([0-9a-zA-Z]+)','view.comments.AdminDeleteCommentHandler'),    
    
    (r'/uploader/choice/','view.backend.UploaderChoiceHandler'),
    (r'/uploader/file/','view.backend.UploaderFileHandler'),
    (r'/uploader/form/','view.backend.UploaderFormHandler'),
    
    (r'/ajax/upload/','view.backend.AjaxUploadHandler'),
    
    (r'/following/', 'view.board.FollowingHandler'),
    
    (r'/ajax/followuser/([0-9a-zA-Z]*)','view.user.FollowuserHandler'),
    (r'/ajax/removefollowuser/([0-9a-zA-Z]*)','view.user.RemoveFollowuserHandler'),
    
    
    (r'/ajax/board/','view.board.AjaxBoardHandler'),
    (r'/ajax/follow/([0-9a-zA-Z]*)','view.board.FolllowHandler'),
    (r'/ajax/removefollow/([0-9a-zA-Z]*)','view.board.RemoveFolllowHandler'),
    (r'/ajax/repin/([0-9a-zA-Z]*)','view.pins.RepinHandler'),
    (r'/ajax/like/([0-9a-zA-Z]*)','view.pins.LikeHandler'),
    (r'/ajax/removelike/([0-9a-zA-Z]*)','view.pins.RemoveLikeHandler'),
    (r'/ajax/hate/([0-9a-zA-Z]*)','view.pins.HateHandler'),
    (r'/ajax/removehate/([0-9a-zA-Z]*)','view.pins.RemoveHateHandler'),
    (r'/ajax/addboard/','view.board.AjaxAddboardHandler'),
    
    (r'/ajax/comment/','view.comments.AjaxCommentHandler'),
    
    (r'/service/upload/','view.service.UploadHandler'),
    (r'/service/form/', 'view.service.FormHandler'),   
    
    #404处理必须放在所有URLS路由的最后
    (r'/.*','view.frontend.NotFoundHandler'),
    ]

