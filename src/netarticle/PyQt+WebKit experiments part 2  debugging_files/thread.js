/*jslint evil:true */
/**
 * Dynamic thread loader
 *
 * 
 *  * 
 * 
*/

// 
var DISQUS;
if (!DISQUS || typeof DISQUS == 'function') {
    throw "DISQUS object is not initialized";
}
// 

// json_data and default_json django template variables will close
// and re-open javascript comment tags

(function () {
    var jsonData, cookieMessages, session, key;

    /* */ jsonData = {"reactions": [], "reactions_limit": 10, "ordered_highlighted": [], "posts": {"457712066": {"edited": false, "author_is_moderator": false, "from_request_user": null, "up_voted": false, "can_edit": false, "ip": "", "last_modified_date": null, "dislikes": 0, "raw_message": "You should avoid \"*\"-Imports! Even if you just want to show something it is better to write pythonic code :-)", "has_replies": true, "vote": false, "votable": true, "last_modified_by": null, "real_date": "2012-02-03_19:06:59", "date": "8 months ago", "message": "<p>You should avoid \"*\"-Imports! Even if you just want to show something it is better to write pythonic code :-)</p>", "approved": true, "is_last_child": false, "author_is_founder": false, "can_reply": true, "likes": 0, "user_voted": null, "num_replies": 3, "down_voted": false, "is_first_child": false, "has_been_anonymized": false, "highlighted": false, "parent_post_id": null, "depth": 0, "points": 0, "user_key": "77b7f22990c0a840ce0f5aa4f89950dc", "author_is_creator": false, "email": "", "killed": false, "is_realtime": false}, "645750795": {"edited": false, "author_is_moderator": false, "from_request_user": null, "up_voted": false, "can_edit": false, "ip": "", "last_modified_date": null, "dislikes": 0, "raw_message": "You should avoid \"*\"-Imports! Even if you just want to show something it is better to write pythonic code :-)", "has_replies": false, "vote": false, "votable": true, "last_modified_by": null, "real_date": "2012-02-03_19:06:59", "date": "8 months ago", "message": "<p>You should avoid \"*\"-Imports! Even if you just want to show something it is better to write pythonic code :-)</p>", "approved": true, "is_last_child": false, "author_is_founder": false, "can_reply": true, "likes": 0, "user_voted": null, "num_replies": 3, "down_voted": false, "is_first_child": false, "has_been_anonymized": false, "highlighted": false, "parent_post_id": null, "depth": 0, "points": 0, "user_key": "77b7f22990c0a840ce0f5aa4f89950dc", "author_is_creator": false, "email": "", "killed": false, "is_realtime": false}, "645750799": {"edited": false, "author_is_moderator": false, "from_request_user": null, "up_voted": false, "can_edit": false, "ip": "", "last_modified_date": null, "dislikes": 0, "raw_message": "I usually do this, but I don't think it really matters for PyQt4 classes. Since all Qt classes are prefixed with \"Q\" it is clear where they come from.", "has_replies": false, "vote": false, "votable": true, "last_modified_by": null, "real_date": "2012-02-03_21:23:05", "date": "8 months ago", "message": "<p>I usually do this, but I don't think it really matters for PyQt4 classes. Since all Qt classes are prefixed with \"Q\" it is clear where they come from.</p>", "approved": true, "is_last_child": false, "author_is_founder": false, "can_reply": true, "likes": 0, "user_voted": null, "num_replies": 2, "down_voted": false, "is_first_child": true, "has_been_anonymized": false, "highlighted": false, "parent_post_id": 645750795, "depth": 1, "points": 0, "user_key": "6300af216639777da5f4150c2886e95f", "author_is_creator": false, "email": "", "killed": false, "is_realtime": false}, "645750801": {"edited": false, "author_is_moderator": false, "from_request_user": null, "up_voted": false, "can_edit": false, "ip": "", "last_modified_date": null, "dislikes": 0, "raw_message": "Yes it matters; of course the problems might seem less important than in other cases, but think of your own class you design. In context of Qt it will start with \"Q\" either... and there you are ;-)", "has_replies": false, "vote": false, "votable": true, "last_modified_by": null, "real_date": "2012-02-04_20:12:12", "date": "8 months ago", "message": "<p>Yes it matters; of course the problems might seem less important than in other cases, but think of your own class you design. In context of Qt it will start with \"Q\" either... and there you are ;-)</p>", "approved": true, "is_last_child": false, "author_is_founder": false, "can_reply": true, "likes": 0, "user_voted": null, "num_replies": 1, "down_voted": false, "is_first_child": false, "has_been_anonymized": false, "highlighted": false, "parent_post_id": 645750799, "depth": 2, "points": 0, "user_key": "77b7f22990c0a840ce0f5aa4f89950dc", "author_is_creator": false, "email": "", "killed": false, "is_realtime": false}, "645750802": {"edited": false, "author_is_moderator": false, "from_request_user": null, "up_voted": false, "can_edit": false, "ip": "", "last_modified_date": null, "dislikes": 0, "raw_message": "Just like I would never create a class starting with \"Q\" when writing Qt C++ code, I will never create a class starting with \"Q\" when writing PyQt code.", "has_replies": false, "vote": false, "votable": true, "last_modified_by": null, "real_date": "2012-02-04_23:53:20", "date": "8 months ago", "message": "<p>Just like I would never create a class starting with \"Q\" when writing Qt C++ code, I will never create a class starting with \"Q\" when writing PyQt code.</p>", "approved": true, "is_last_child": true, "author_is_founder": false, "can_reply": true, "likes": 0, "user_voted": null, "num_replies": 0, "down_voted": false, "is_first_child": false, "has_been_anonymized": false, "highlighted": false, "parent_post_id": 645750801, "depth": 3, "points": 0, "user_key": "6300af216639777da5f4150c2886e95f", "author_is_creator": false, "email": "", "killed": false, "is_realtime": false}, "457712596": {"edited": false, "author_is_moderator": false, "from_request_user": null, "up_voted": false, "can_edit": false, "ip": "", "last_modified_date": null, "dislikes": 0, "raw_message": "I usually do this, but I don't think it really matters for PyQt4 classes. Since all Qt classes are prefixed with \"Q\" it is clear where they come from.", "has_replies": true, "vote": false, "votable": true, "last_modified_by": null, "real_date": "2012-02-03_21:23:05", "date": "8 months ago", "message": "<p>I usually do this, but I don't think it really matters for PyQt4 classes. Since all Qt classes are prefixed with \"Q\" it is clear where they come from.</p>", "approved": true, "is_last_child": false, "author_is_founder": false, "can_reply": true, "likes": 0, "user_voted": null, "num_replies": 2, "down_voted": false, "is_first_child": true, "has_been_anonymized": false, "highlighted": false, "parent_post_id": 457712066, "depth": 1, "points": 0, "user_key": "6300af216639777da5f4150c2886e95f", "author_is_creator": false, "email": "", "killed": false, "is_realtime": false}, "457712598": {"edited": false, "author_is_moderator": false, "from_request_user": null, "up_voted": false, "can_edit": false, "ip": "", "last_modified_date": null, "dislikes": 0, "raw_message": "Yes it matters; of course the problems might seem less important than in other cases, but think of your own class you design. In context of Qt it will start with \"Q\" either... and there you are ;-)", "has_replies": true, "vote": false, "votable": true, "last_modified_by": null, "real_date": "2012-02-04_20:12:12", "date": "8 months ago", "message": "<p>Yes it matters; of course the problems might seem less important than in other cases, but think of your own class you design. In context of Qt it will start with \"Q\" either... and there you are ;-)</p>", "approved": true, "is_last_child": false, "author_is_founder": false, "can_reply": true, "likes": 0, "user_voted": null, "num_replies": 1, "down_voted": false, "is_first_child": false, "has_been_anonymized": false, "highlighted": false, "parent_post_id": 457712596, "depth": 2, "points": 0, "user_key": "77b7f22990c0a840ce0f5aa4f89950dc", "author_is_creator": false, "email": "", "killed": false, "is_realtime": false}, "645750804": {"edited": false, "author_is_moderator": false, "from_request_user": null, "up_voted": false, "can_edit": false, "ip": "", "last_modified_date": null, "dislikes": 0, "raw_message": "awesome tutorial", "has_replies": false, "vote": false, "votable": true, "last_modified_by": null, "real_date": "2012-04-13_19:38:20", "date": "5 months ago", "message": "<p>awesome tutorial</p>", "approved": true, "is_last_child": false, "author_is_founder": false, "can_reply": true, "likes": 0, "user_voted": null, "num_replies": 0, "down_voted": false, "is_first_child": false, "has_been_anonymized": false, "highlighted": false, "parent_post_id": null, "depth": 0, "points": 0, "user_key": "a925741058f1440c69bb74c7deee2c5f", "author_is_creator": false, "email": "", "killed": false, "is_realtime": false}, "457712730": {"edited": false, "author_is_moderator": false, "from_request_user": null, "up_voted": false, "can_edit": false, "ip": "", "last_modified_date": null, "dislikes": 0, "raw_message": "Just like I would never create a class starting with \"Q\" when writing Qt C++ code, I will never create a class starting with \"Q\" when writing PyQt code.", "has_replies": false, "vote": false, "votable": true, "last_modified_by": null, "real_date": "2012-02-04_23:53:20", "date": "8 months ago", "message": "<p>Just like I would never create a class starting with \"Q\" when writing Qt C++ code, I will never create a class starting with \"Q\" when writing PyQt code.</p>", "approved": true, "is_last_child": true, "author_is_founder": false, "can_reply": true, "likes": 0, "user_voted": null, "num_replies": 0, "down_voted": false, "is_first_child": false, "has_been_anonymized": false, "highlighted": false, "parent_post_id": 457712598, "depth": 3, "points": 0, "user_key": "6300af216639777da5f4150c2886e95f", "author_is_creator": false, "email": "", "killed": false, "is_realtime": false}}, "ordered_posts": [645750795, 645750799, 645750801, 645750802, 457712066, 457712596, 457712598, 457712730, 645750804], "realtime_enabled": false, "ready": true, "mediaembed": [], "has_more_reactions": false, "realtime_paused": true, "integration": {"receiver_url": null, "hide_user_votes": false, "reply_position": true, "disqus_logo": false}, "highlighted": {}, "reactions_start": 0, "media_url": "http://mediacdn.disqus.com/1349204341", "users": {"77b7f22990c0a840ce0f5aa4f89950dc": {"username": "Hyperion", "tumblr": "", "about": "", "display_name": "Hyperion", "url": "http://disqus.com/guest/77b7f22990c0a840ce0f5aa4f89950dc/", "registered": false, "remote_id": null, "linkedin": "", "blog": "", "remote_domain": "", "points": 0, "facebook": "", "avatar": "http://mediacdn.disqus.com/1349204341/images/noavatar32.png", "delicious": "", "is_remote": false, "verified": false, "flickr": "", "twitter": "", "remote_domain_name": ""}, "a925741058f1440c69bb74c7deee2c5f": {"username": "enzo", "tumblr": "", "about": "", "display_name": "enzo", "url": "http://disqus.com/guest/a925741058f1440c69bb74c7deee2c5f/", "registered": false, "remote_id": null, "linkedin": "", "blog": "", "remote_domain": "", "points": 0, "facebook": "", "avatar": "http://mediacdn.disqus.com/1349204341/images/noavatar32.png", "delicious": "", "is_remote": false, "verified": false, "flickr": "", "twitter": "", "remote_domain_name": ""}, "6300af216639777da5f4150c2886e95f": {"username": "Aur\u00e9lien", "tumblr": "", "about": "", "display_name": "Aur\u00e9lien", "url": "http://disqus.com/guest/6300af216639777da5f4150c2886e95f/", "registered": false, "remote_id": null, "linkedin": "", "blog": "", "remote_domain": "", "points": 0, "facebook": "", "avatar": "http://mediacdn.disqus.com/uploads/anonusers/3133/2310/avatar32.jpg?1281549414", "delicious": "", "is_remote": false, "verified": false, "flickr": "", "twitter": "", "remote_domain_name": ""}}, "user_unapproved": {}, "messagesx": {"count": 0, "unread": []}, "thread": {"voters_count": 0, "offset_posts": 0, "slug": "httpagateaucom20120203pyqtwebkit_experiments_part_2_debugging", "paginate": true, "num_pages": 1, "days_alive": 0, "moderate_none": false, "voters": {}, "total_posts": 9, "realtime_paused": true, "queued": false, "pagination_type": "append", "user_vote": null, "likes": 0, "num_posts": 9, "closed": false, "per_page": 40, "id": 600626671, "killed": false, "moderate_all": false}, "forum": {"use_media": true, "avatar_size": 32, "apiKey": "orh5qRtXNsN75XunECQyRbkL0umUecbqcslpJYpsMCwx0kyMBsQHc31h6paMAppU", "features": {}, "comment_max_words": 0, "mobile_theme_disabled": false, "is_early_adopter": false, "login_buttons_enabled": false, "streaming_realtime": false, "reply_position": true, "id": 1320801, "default_avatar_url": "http://mediacdn.disqus.com/1349204341/images/noavatar32.png", "template": {"url": "http://mediacdn.disqus.com/1349204341/uploads/themes/7884a9652e94555c70f96b6be63be216/theme.js?254", "mobile": {"url": "http://mediacdn.disqus.com/1349204341/uploads/themes/mobile/theme.js?254", "css": "http://mediacdn.disqus.com/1349204341/uploads/themes/mobile/theme.css?254"}, "api": "1.1", "name": "Houdini", "css": "http://mediacdn.disqus.com/1349204341/uploads/themes/7884a9652e94555c70f96b6be63be216/theme.css?254"}, "max_depth": 0, "ranks_enabled": false, "lastUpdate": 1331033694, "linkbacks_enabled": true, "allow_anon_votes": true, "revert_new_login_flow": false, "stylesUrl": "http://mediacdn.disqus.com/uploads/styles/132/801/agateau.css", "show_avatar": true, "reactions_enabled": true, "disqus_auth_disabled": false, "name": "Aur\u00e9lien&#39;s room", "language": "en", "mentions_enabled": true, "url": "agateau", "allow_anon_post": true, "thread_votes_disabled": false, "hasCustomStyles": false, "moderate_all": false}, "settings": {"realtimeHost": "qq.disqus.com", "uploads_url": "http://media.disqus.com/uploads", "ssl_media_url": "https://securecdn.disqus.com/1349204341", "realtime_url": "http://rt.disqus.com/forums/realtime-cached.js", "facebook_app_id": "52254943976", "minify_js": true, "recaptcha_public_key": "6LdKMrwSAAAAAPPLVhQE9LPRW4LUSZb810_iaa8u", "read_only": false, "facebook_api_key": "52254943976", "juggler_url": "http://juggler.services.disqus.com", "realtimePort": "80", "debug": false, "disqus_url": "http://disqus.com", "media_url": "http://mediacdn.disqus.com/1349204341"}, "ranks": {}, "request": {"sort": "oldest", "is_authenticated": false, "user_type": "anon", "subscribe_on_post": 0, "missing_perm": null, "user_id": null, "remote_domain_name": "", "remote_domain": "", "is_verified": false, "profile_url": "", "username": "", "is_global_moderator": false, "sharing": {}, "timestamp": "2012-10-02_21:02:08", "is_moderator": false, "ordered_unapproved_posts": [], "unapproved_posts": {}, "forum": "agateau", "is_initial_load": true, "display_username": "", "points": null, "has_email": false, "moderator_can_edit": false, "is_remote": false, "userkey": "", "page": 1}, "context": {"use_twitter_signin": false, "use_fb_connect": false, "show_reply": true, "sigma_chance": 10, "use_google_signin": false, "switches": {"olark_admin_addons": true, "use_rs_paginator_30m": true, "es_index_threads": true, "discovery_best_comment": true, "digests:events:2": true, "digests:events:3": true, "postsort": true, "digests:events:1": true, "discovery_next:promoted": true, "olark_admin_packages": true, "upload_media": true, "website_addons": true, "firehose_gnip_http": true, "textdigger_classification": true, "google_translate": true, "digests:events": true, "next_realtime": true, "firehose_message_db_lookup": true, "digests": true, "juggler_thread_onReady": true, "website_homepage_https_off": true, "juggler_enabled": true, "discovery_network": true, "promoted_discovery_budget": true, "use_impermium": true, "digests:render": true, "notifications": true, "shardpost:index": true, "usertransformer_reputation": true, "fingerprint": true, "discovery_click_optimization": true, "firehose_push": true, "shardpost": true, "train_impermium": true, "discovery_analytics": true, "discovery_next:truncate": true, "limit_get_posts_days_30d": true, "website_base_template": true, "firehose_pubsub_throttle": true, "discovery_next:dark_promoted": true, "new_moderate": true, "redis_threadcount": true, "html_email": true, "listactivity_replies": true, "postsort:index": true, "phoenix_reputation": true, "next_thread_sharing": true, "use_master_for_api": true, "next_realtime_indicators": true, "community_icon": true, "discovery_jones": true, "originalauthor_switchover": true, "static_styles": true, "firehose": true, "realtime": true, "redis_notification_tokens": true, "discovery_next": true, "show_captcha_on_links": true, "olark_support": true, "firehose_gnip": true, "firehose_pubsub": true, "olark_addons": true, "phoenix_optout": true, "edits_to_spam": true, "promoted_discovery_random": true, "discovery_community": true, "phoenix": true, "discovery_redirect_event": true, "use_rs_paginator_5m": true, "theme_editor_disabled": true, "textdigger_crawler": true, "listactivity_replies_30d": true, "send_to_impermium": true, "next_discard_low_rep": true, "google_analytics": true, "mentions": true, "olark_install": true}, "forum_facebook_key": "", "use_yahoo": false, "subscribed": false, "active_gargoyle_switches": ["community_icon", "digests", "digests:events", "digests:events:1", "digests:events:2", "digests:events:3", "digests:render", "discovery_analytics", "discovery_best_comment", "discovery_click_optimization", "discovery_community", "discovery_jones", "discovery_network", "discovery_next", "discovery_next:dark_promoted", "discovery_next:promoted", "discovery_next:truncate", "discovery_redirect_event", "edits_to_spam", "es_index_threads", "fingerprint", "firehose", "firehose_gnip", "firehose_gnip_http", "firehose_message_db_lookup", "firehose_pubsub", "firehose_pubsub_throttle", "firehose_push", "google_analytics", "google_translate", "html_email", "juggler_enabled", "juggler_thread_onReady", "limit_get_posts_days_30d", "listactivity_replies", "listactivity_replies_30d", "mentions", "new_moderate", "next_discard_low_rep", "next_realtime", "next_realtime_indicators", "next_thread_sharing", "notifications", "olark_addons", "olark_admin_addons", "olark_admin_packages", "olark_install", "olark_support", "originalauthor_switchover", "phoenix", "phoenix_optout", "phoenix_reputation", "postsort", "postsort:index", "promoted_discovery_budget", "promoted_discovery_random", "realtime", "redis_notification_tokens", "redis_threadcount", "send_to_impermium", "shardpost", "shardpost:index", "show_captcha_on_links", "static_styles", "textdigger_classification", "textdigger_crawler", "theme_editor_disabled", "train_impermium", "use_impermium", "use_master_for_api", "use_rs_paginator_30m", "use_rs_paginator_5m", "usertransformer_reputation", "website_addons", "website_base_template", "website_homepage_https_off"], "realtime_speed": 15000, "use_openid": false}}; /* */
    /* __extrajson__ */
    cookieMessages = {"user_created": null, "post_has_profile": null, "post_twitter": null, "post_not_approved": null}; session = {"url": null, "name": null, "email": null};

    DISQUS.jsonData = jsonData;
    DISQUS.jsonData.cookie_messages = cookieMessages;
    DISQUS.jsonData.session = session;

    if (DISQUS.useSSL) {
        DISQUS.useSSL(DISQUS.jsonData.settings);
    }

    // The mappings below are for backwards compatibility--before we port all the code that
    // accesses jsonData.settings to DISQUS.settings

    var mappings = {
        debug:                'disqus.debug',
        minify_js:            'disqus.minified',
        read_only:            'disqus.readonly',
        recaptcha_public_key: 'disqus.recaptcha.key',
        facebook_app_id:      'disqus.facebook.appId',
        facebook_api_key:     'disqus.facebook.apiKey'
    };

    var urlMappings = {
        disqus_url:    'disqus.urls.main',
        media_url:     'disqus.urls.media',
        ssl_media_url: 'disqus.urls.sslMedia',
        realtime_url:  'disqus.urls.realtime',
        uploads_url:   'disqus.urls.uploads'
    };

    if (DISQUS.jsonData.context.switches.realtime_setting_change) {
        urlMappings.realtimeHost = 'realtime.host';
        urlMappings.realtimePort = 'realtime.port';
    }
    for (key in mappings) {
        if (mappings.hasOwnProperty(key)) {
            DISQUS.settings.set(mappings[key], DISQUS.jsonData.settings[key]);
        }
    }

    for (key in urlMappings) {
        if (urlMappings.hasOwnProperty(key)) {
            DISQUS.jsonData.settings[key] = DISQUS.settings.get(urlMappings[key]);
        }
    }
}());

DISQUS.jsonData.context.csrf_token = '21bc467119200cb06806902fa8e2f5b0';

DISQUS.jsonData.urls = {
    login: 'http://disqus.com/profile/login/',
    logout: 'http://disqus.com/logout/',
    upload_remove: 'http://agateau.disqus.com/thread/httpagateaucom20120203pyqtwebkit_experiments_part_2_debugging/async_media_remove/',
    request_user_profile: 'http://disqus.com/AnonymousUser/',
    request_user_avatar: 'http://mediacdn.disqus.com/1349204341/images/noavatar92.png',
    verify_email: 'http://disqus.com/verify/',
    remote_settings: 'http://agateau.disqus.com/_auth/embed/remote_settings/',
    edit_profile_window: 'http://disqus.com/embed/profile/edit/',
    embed_thread: 'http://agateau.disqus.com/thread.js',
    embed_vote: 'http://agateau.disqus.com/vote.js',
    embed_thread_vote: 'http://agateau.disqus.com/thread_vote.js',
    embed_thread_share: 'http://agateau.disqus.com/thread_share.js',
    embed_queueurl: 'http://agateau.disqus.com/queueurl.js',
    embed_hidereaction: 'http://agateau.disqus.com/hidereaction.js',
    embed_more_reactions: 'http://agateau.disqus.com/more_reactions.js',
    embed_subscribe: 'http://agateau.disqus.com/subscribe.js',
    embed_highlight: 'http://agateau.disqus.com/highlight.js',
    embed_block: 'http://agateau.disqus.com/block.js',
    update_moderate_all: 'http://agateau.disqus.com/update_moderate_all.js',
    update_days_alive: 'http://agateau.disqus.com/update_days_alive.js',
    show_user_votes: 'http://agateau.disqus.com/show_user_votes.js',
    forum_view: 'http://agateau.disqus.com/httpagateaucom20120203pyqtwebkit_experiments_part_2_debugging',
    cnn_saml_try: 'http://disqus.com/saml/cnn/try/',
    realtime: DISQUS.jsonData.settings.realtime_url,
    thread_view: 'http://agateau.disqus.com/thread/httpagateaucom20120203pyqtwebkit_experiments_part_2_debugging/',
    twitter_connect: DISQUS.jsonData.settings.disqus_url + '/_ax/twitter/begin/',
    yahoo_connect: DISQUS.jsonData.settings.disqus_url + '/_ax/yahoo/begin/',
    openid_connect: DISQUS.jsonData.settings.disqus_url + '/_ax/openid/begin/',
    googleConnect: DISQUS.jsonData.settings.disqus_url + '/_ax/google/begin/',
    community: 'http://agateau.disqus.com/community.html',
    admin: 'http://agateau.disqus.com/admin/moderate/',
    moderate: 'http://agateau.disqus.com/admin/moderate/',
    moderate_threads: 'http://agateau.disqus.com/admin/moderate-threads/',
    settings: 'http://agateau.disqus.com/admin/settings/',
    unmerged_profiles: 'http://disqus.com/embed/profile/unmerged_profiles/',
    juggler: DISQUS.jsonData.settings.juggler_url,

    channels: {
        def:      'http://disqus.com/default.html', /* default channel */
        auth:     'https://disqus.com/embed/login.html',
        tweetbox: 'http://disqus.com/forums/integrations/twitter/tweetbox.html?f=agateau',
        edit:     'http://agateau.disqus.com/embed/editcomment.html'
    }
};


// 
//     
DISQUS.jsonData.urls.channels.reply = 'http://mediacdn.disqus.com/1349204341/build/system/reply.html';
DISQUS.jsonData.urls.channels.upload = 'http://mediacdn.disqus.com/1349204341/build/system/upload.html';
DISQUS.jsonData.urls.channels.sso = 'http://mediacdn.disqus.com/1349204341/build/system/sso.html';
DISQUS.jsonData.urls.channels.facebook = 'http://mediacdn.disqus.com/1349204341/build/system/facebook.html';
//     
// 
