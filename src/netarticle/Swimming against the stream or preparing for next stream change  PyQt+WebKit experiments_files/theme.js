
    DISQUS.addBlocks('theme')(function ($d) {
        $d.blocks["comment"] = function block_comment ($globals, $locals) {

    var $h = new $d.Builder();

    var localScope = DISQUS.extend({}, $globals, $locals);
    with (localScope) {

$h.put("  \x3Cli id\x3D\x22comment\x2D");
$h.put(($h.esc || function (s) { return s; })(comment.id));
$h.put("\x22/\x3E  \x3Cli id\x3D\x22dsq\x2Dcomment\x2D");
$h.put(($h.esc || function (s) { return s; })(comment.id));
$h.put("\x22 data\x2Ddsq\x2Dcomment\x2Did\x3D\x22");
$h.put(($h.esc || function (s) { return s; })(comment.id));
$h.put("\x22      class\x3D\x22dsq\x2Dcomment dsq\x2Dclearfix        ");
if (comment.num_replies > 0) { 
$h.put("dsq\x2Dcomment\x2Dis\x2Dparent");
}
$h.put("        ");
if (comment.author_is_moderator) { 
$h.put("dsq\x2Dmoderator");
}
$h.put("        ");
if (comment.author_is_founder) { 
$h.put("dsq\x2Dfounder");
}
$h.put("\x22      style\x3D\x22margin\x2Dleft:");
if (forum.max_depth != 0 && comment.depth > forum.max_depth) { 
$h.put(($h.esc || function (s) { return s; })(forum.max_depth * 46));
} else {
$h.put(($h.esc || function (s) { return s; })(comment.depth * 46));
}
$h.put("px\x3B\x22\x3E    \x3Cdiv class\x3D\x22dsq\x2Davatar dsq\x2Dtt\x22 title\x3D\x22");
$h.put($d.interpolate(trans("Expand %(name)s\x26#39\x3Bs profile"), { "name": comment.author.display_name }));
$h.put("\x22\x3E      \x3Ca href\x3D\x22");
$h.put(($h.esc || function (s) { return s; })(comment.author.url));
$h.put("\x22 onclick\x3D\x22DISQUS.dtpl.actions.fire(\x27profile.show\x27, ");
$h.put(($h.esc || function (s) { return s; })(comment.id));
$h.put(", null)\x3B return false\x22\x3E        \x3Cimg src\x3D\x22");
$h.put(($h.esc || function (s) { return s; })(forum.default_avatar_url));
$h.put("\x22 class\x3D\x22dsq\x2Ddeferred\x2Davatar\x22 data\x2Dsrc\x3D\x22");
$h.put(($h.esc || function (s) { return s; })(comment.author.avatar));
$h.put("\x22 alt\x3D\x22\x22/\x3E      \x3C/a\x3E    \x3C/div\x3E    \x3Cdiv id\x3D\x22dsq\x2Dcomment\x2Dbody\x2D");
$h.put(($h.esc || function (s) { return s; })(comment.id));
$h.put("\x22 class\x3D\x22dsq\x2Dcomment\x2Dbody\x22\x3E      \x3Cdiv class\x3D\x22dsq\x2Dcomment\x2Dheader\x22\x3E        ");
if (comment.author.blog) { 
$h.put("\x3Ca href\x3D\x22");
$h.put(($h.esc || function (s) { return s; })(comment.author.blog));
$h.put("\x22 target\x3D\x22_blank\x22              class\x3D\x22dsq\x2Dcommenter\x2Dname\x22 rel\x3D\x22nofollow\x22\x3E");
$h.put(($h.esc || function (s) { return s; })(comment.author.display_name));
$h.put("\x3C/a\x3E");
} else {
$h.put("\x3Cspan class\x3D\x22dsq\x2Dcommenter\x2Dname\x22\x3E");
$h.put(($h.esc || function (s) { return s; })(comment.author.display_name));
$h.put("\x3C/span\x3E");
}
if (forum.ranks_enabled && ranks[comment.user_key]) { 
$h.put("\x3Cspan class\x3D\x22dsq\x2Dbadge\x2Dwrap\x22\x3E");
if (ranks[comment.user_key].rank.has_icon) { 
$h.put("\x3Cdiv class\x3D\x22dsq\x2Dbadge\x2Dimage dsq\x2Dtt\x22 title\x3D\x22Score: \x26nbsp\x3B");
$h.put(($h.esc || function (s) { return s; })(ranks[comment.user_key].score));
$h.put("\x26nbsp\x3B\x26nbsp\x3B Placement: \x26nbsp\x3B");
$h.put(($h.esc || function (s) { return s; })(ranks[comment.user_key].placement));
$h.put("\x22\x3E                    \x3Cimg src\x3D\x22");
$h.put(($h.esc || function (s) { return s; })(ranks[comment.user_key].rank.icon));
$h.put("\x22 alt\x3D\x22\x22 width\x3D\x2232\x22 height\x3D\x2232\x22 /\x3E                \x3C/div\x3E");
} else {
$h.put("\x3Cspan class\x3D\x22dsq\x2Dbadge dsq\x2Dtt dsq\x2Drank\x2D");
$h.put(($h.esc || function (s) { return s; })(ranks[comment.user_key].rank.pie_order));
$h.put("\x22 title\x3D\x22Score: \x26nbsp\x3B");
$h.put(($h.esc || function (s) { return s; })(ranks[comment.user_key].score));
$h.put("\x26nbsp\x3B\x26nbsp\x3B Placement: \x26nbsp\x3B");
$h.put(($h.esc || function (s) { return s; })(ranks[comment.user_key].placement));
$h.put("\x22\x3E");
$h.put(($h.esc || function (s) { return s; })(ranks[comment.user_key].rank.name));
$h.put("\x3C/span\x3E");
}
$h.put("\x3C/span\x3E");
}
if (comment.author.about) { 
$h.put("\x3Cspan class\x3D\x22dsq\x2Dcommenter\x2Dbio\x22\x3E");
if (!forum.ranks_enabled) { 
$h.put(",");
}
$h.put(" ");
$h.put(($h.esc || function (s) { return s; })(comment.author.about));
$h.put("\x3C/span\x3E");
}
$h.put("        ");
$h.put("        \x3Cspan class\x3D\x22dsq\x2Dcollapsed\x2Dcount\x22\x3E          ");
if (comment.num_replies == 0) { 
$h.put("            1 ");
$h.put(trans("comment collapsed"));
$h.put("          ");
} else {
$h.put("            ");
$h.put(($h.esc || function (s) { return s; })(comment.num_replies + 1));
$h.put(" ");
$h.put(trans("comments collapsed"));
$h.put("          ");
}
$h.put("        \x3C/span\x3E        ");
$h.put("        \x3Ca href\x3D\x22#\x22 class\x3D\x22dsq\x2Dcollapse\x2Dtoggle dsq\x2Dcollapse\x22 title\x3D\x22");
$h.put(trans("Collapse thread"));
$h.put("\x22 onclick\x3D\x22DISQUS.dtpl.actions.fire(\x27comments.collapse\x27, ");
$h.put(($h.esc || function (s) { return s; })(comment.id));
$h.put(")\x3B return false\x3B\x22\x3E\x3Cspan\x3E");
$h.put(trans("Collapse"));
$h.put("\x3C/span\x3E\x3C/a\x3E        \x3Ca href\x3D\x22#\x22 class\x3D\x22dsq\x2Dcollapse\x2Dtoggle dsq\x2Dexpand\x22 title\x3D\x22");
$h.put(trans("Expand thread"));
$h.put("\x22 onclick\x3D\x22DISQUS.dtpl.actions.fire(\x27comments.expand\x27, ");
$h.put(($h.esc || function (s) { return s; })(comment.id));
$h.put(")\x3B return false\x3B\x22\x3E\x3Cspan\x3E");
$h.put(trans("Expand"));
$h.put("\x3C/span\x3E\x3C/a\x3E      \x3C/div\x3E      ");
(function () {
var $l = {};
$d.extend($l, $locals);
$d.extend($l, {"cls": "dsq-comment-message"});
$h.put($d.renderBlock("commentMessage", $l));
}());
$h.put("      ");
if (forum.use_media && comment.media && comment.approved && !comment.killed) { 
$h.put("        \x3Cdiv id\x3D\x22dsq\x2Dmedia\x2Dembed\x2D");
$h.put(($h.esc || function (s) { return s; })(comment.id));
$h.put("\x22 class\x3D\x22dsq\x2Dmedia\x2Dembed\x22\x3E          \x3Ch4\x3E\x3C/h4\x3E          ");
$d.each(comment.media, function (media, $index, $collection) {
var $locals = { "media": media, "index": $index };
$h.put("            \x3Ca id\x3D\x22dsq\x2Dmedia\x2Dembed\x2Dthumbnail\x2D");
$h.put(($h.esc || function (s) { return s; })(media.id));
$h.put("\x22 href\x3D\x22#\x22              onclick\x3D\x22return DISQUS.dtpl.actions.fire(\x27thread.expandMediaEmbed\x27, ");
$h.put(($h.esc || function (s) { return s; })(media.id));
$h.put(")\x3B\x22\x3E              \x3Cimg src\x3D\x22");
$h.put(($h.esc || function (s) { return s; })(media.thumbnailURL));
$h.put("\x22 style\x3D\x22width:75px\x3Bheight:75px\x3Bborder:none\x3B\x22/\x3E            \x3C/a\x3E          ");
});
$h.put("        \x3C/div\x3E      ");
}
$h.put("      \x3C!\x2D\x2D edit box dynamically inserted here \x2D\x2D\x3E      \x3Cdiv id\x3D\x22dsq\x2Dappend\x2Dedit\x2D");
$h.put(($h.esc || function (s) { return s; })(comment.id));
$h.put("\x22\x3E\x3C/div\x3E      ");
(function () {
var $l = {};
$d.extend($l, $locals);
$d.extend($l, {});
$h.put($d.renderBlock("commentFooter", $l));
}());
$h.put("      \x3C!\x2D\x2D reply box dynamically inserted here \x2D\x2D\x3E      \x3Cdiv id\x3D\x22dsq\x2Dappend\x2Dreply\x2D");
$h.put(($h.esc || function (s) { return s; })(comment.id));
$h.put("\x22\x3E\x3C/div\x3E    \x3C/div\x3E  \x3C/li\x3E  \x3C!\x2D\x2D new replies dynamically inserted here \x2D\x2D\x3E  \x3Cli id\x3D\x22dsq\x2Dappend\x2Dpost\x2D");
$h.put(($h.esc || function (s) { return s; })(comment.id));
$h.put("\x22\x3E\x3C/li\x3E");
return $h.compile();

}

};
$d.blocks["reactions"] = function block_reactions ($globals, $locals) {

    var $h = new $d.Builder();

    var localScope = DISQUS.extend({}, $globals, $locals);
    with (localScope) {

$h.put("  ");
if (reactions) { 
$h.put("    \x3Ch3 class\x3D\x22dsq\x2Dh3\x2Dreactions\x22\x3E");
$h.put(trans("Reactions"));
$h.put("\x3C/h3\x3E    \x3Cul id\x3D\x22dsq\x2Dreactions\x22 class\x3D\x22dsq\x2Dreactions dsq\x2Dclearfix\x22\x3E      ");
$d.each(reactions, function (reaction, $index, $collection) {
var $locals = { "reaction": reaction, "index": $index };
$h.put("        ");
(function () {
var $l = {};
$d.extend($l, $locals);
$d.extend($l, {});
$h.put($d.renderBlock("reaction", $l));
}());
$h.put("      ");
});
$h.put("    \x3C/ul\x3E    ");
if (context.has_more_reactions) { 
$h.put("      \x3Cdiv id\x3D\x22dsq\x2Dshow\x2Dmore\x2Dreactions\x22 class\x3D\x22dsq\x2Dshow\x2Dmore\x2Dreactions\x22\x3E        \x3Ca href\x3D\x22#\x22 onclick\x3D\x22DISQUS.dtpl.actions.fire(\x27reactions.loadMore\x27)\x3B return false\x3B\x22\x3E          ");
$h.put(trans("Show more reactions"));
$h.put("        \x3C/a\x3E      \x3C/div\x3E    ");
}
$h.put("  ");
}
return $h.compile();

}

};
$d.blocks["trackbacks"] = function block_trackbacks ($globals, $locals) {

    var $h = new $d.Builder();

    var localScope = DISQUS.extend({}, $globals, $locals);
    with (localScope) {

$h.put("  ");
if (forum.linkbacks_enabled) { 
$h.put("    ");
if (context.trackbacks && context.trackbacks.length) { 
$h.put("      \x3Ch3\x3E");
$h.put(trans("Trackbacks"));
$h.put("\x3C/h3\x3E    ");
}
$h.put("    \x3Cdiv class\x3D\x22dsq\x2Dtrackback\x2Durl\x22\x3E      ");
$h.put(trans("Trackback URL"));
$h.put("      \x3Cinput onclick\x3D\x22this.select()\x22 readonly\x3D\x22true\x22 value\x3D\x22");
$h.put(($h.esc || function (s) { return s; })(context.trackback_url));
$h.put("\x22/\x3E    \x3C/div\x3E    ");
if (context.trackbacks && context.trackbacks.length) { 
$h.put("      \x3Cul\x3E        ");
$d.each(context.trackbacks, function (trackback, $index, $collection) {
var $locals = { "trackback": trackback, "index": $index };
$h.put("          \x3Cli\x3E            \x3Ccite\x3E              \x3Ca href\x3D\x22");
$h.put(($h.esc || function (s) { return s; })(trackback.author_url));
$h.put("\x22 rel\x3D\x22nofollow\x22\x3E");
$h.put(($h.esc || function (s) { return s; })(trackback.author_name));
$h.put("\x3C/a\x3E            \x3C/cite\x3E            \x3Cp class\x3D\x22dsq\x2Dtrackback\x2Ddate\x22\x3E");
$h.put(($h.esc || function (s) { return s; })(trackback.date));
$h.put("\x3C/p\x3E            \x3Cp class\x3D\x22dsq\x2Dtrackback\x2Dexcerpt\x22\x3E");
$h.put(($h.esc || function (s) { return s; })(trackback.excerpt));
$h.put("\x3C/p\x3E          \x3C/li\x3E        ");
});
$h.put("      \x3C/ul\x3E    ");
}
$h.put("  ");
}
return $h.compile();

}

};
$d.blocks["commentCount"] = function block_commentCount ($globals, $locals) {

    var $h = new $d.Builder();

    var localScope = DISQUS.extend({}, $globals, $locals);
    with (localScope) {

$h.put("  \x3Ch3\x3E  ");
if (thread.total_posts && thread.total_posts > thread.num_posts) { 
$h.put("    ");
if (thread.pagination_type == 'num') { 
$h.put("      ");
$h.put($d.interpolate(trans("Showing \x3Cspan id\x3D\x27dsq\x2Dnum\x2Dposts\x27\x3E1\x2D%(num)s\x3C/span\x3E of \x3Cspan id\x3D\x27dsq\x2Dtotal\x2Dposts\x27\x3E%(total)s\x3C/span\x3E comments"), { "num": thread.num_posts, "total": thread.total_posts }));
$h.put("    ");
} else {
$h.put("      ");
$h.put($d.interpolate(trans("Showing \x3Cspan id\x3D\x27dsq\x2Dnum\x2Dposts\x27\x3E%(num)s\x3C/span\x3E of \x3Cspan id\x3D\x27dsq\x2Dtotal\x2Dposts\x27\x3E%(total)s\x3C/span\x3E comments"), { "num": thread.num_posts, "total": thread.total_posts }));
$h.put("    ");
}
$h.put("  ");
} else {
$h.put("    ");
if (thread.num_posts == 1) { 
$h.put("      ");
$h.put(trans("Showing \x3Cspan id\x3D\x27dsq\x2Dnum\x2Dposts\x27\x3E1\x3C/span\x3E comment"));
$h.put("    ");
} else {
$h.put("      ");
$h.put($d.interpolate(trans("Showing \x3Cspan id\x3D\x27dsq\x2Dnum\x2Dposts\x27\x3E%(num)s\x3C/span\x3E comments"), { "num": thread.num_posts }));
$h.put("    ");
}
$h.put("  ");
}
$h.put("  \x3C/h3\x3E");
return $h.compile();

}

};
$d.blocks["subscribe"] = function block_subscribe ($globals, $locals) {

    var $h = new $d.Builder();

    var localScope = DISQUS.extend({}, $globals, $locals);
    with (localScope) {

$h.put("  ");
if (context.subscribed) { 
$h.put("    \x3Cli\x3E      \x3Ca href\x3D\x22#\x22 class\x3D\x22dsq\x2Dsubscribe\x2Demail\x22 onclick\x3D\x22return DISQUS.dtpl.actions.fire(\x27thread.unsubscribe\x27)\x3B\x22\x3E        \x3Cspan class\x3D\x22dsq\x2Dfont\x22\x3EM\x3C/span\x3E \x3Cem\x3E");
$h.put(trans("Unsubscribe"));
$h.put("\x3C/em\x3E      \x3C/a\x3E    \x3C/li\x3E  ");
} else {
$h.put("    \x3Cli\x3E      \x3Ca href\x3D\x22#\x22 class\x3D\x22dsq\x2Dsubscribe\x2Demail\x22 onclick\x3D\x22return DISQUS.dtpl.actions.fire(\x27thread.subscribe\x27)\x3B\x22\x3E        \x3Cspan class\x3D\x22dsq\x2Dfont\x22\x3EM\x3C/span\x3E \x3Cem\x3E");
$h.put(trans("Subscribe by email"));
$h.put("\x3C/em\x3E      \x3C/a\x3E    \x3C/li\x3E  ");
}
$h.put("  \x3Cli\x3E    \x3Ca href\x3D\x22");
$h.put(($h.esc || function (s) { return s; })(urls.forum_view));
$h.put("/latest.rss\x22 class\x3D\x22dsq\x2Dsubscribe\x2Drss\x22\x3E      \x3Cspan class\x3D\x22dsq\x2Dfont\x22\x3ES\x3C/span\x3E \x3Cem\x3E");
$h.put(trans("RSS"));
$h.put("\x3C/em\x3E    \x3C/a\x3E  \x3C/li\x3E");
return $h.compile();

}

};
$d.blocks["maintenanceNotice"] = function block_maintenanceNotice ($globals, $locals) {

    var $h = new $d.Builder();

    var localScope = DISQUS.extend({}, $globals, $locals);
    with (localScope) {

$h.put("  ");
if (settings.read_only) { 
$h.put("    \x3Cdiv class\x3D\x22dsq\x2Dnotice dsq\x2Derror\x22\x3E      The Disqus comment system is temporarily in maintenance mode. You can still read comments      during this time, however posting comments and other actions are temporarily delayed.    \x3C/div\x3E  ");
}
return $h.compile();

}

};
$d.blocks["realtimeNotice"] = function block_realtimeNotice ($globals, $locals) {

    var $h = new $d.Builder();

    var localScope = DISQUS.extend({}, $globals, $locals);
    with (localScope) {

$h.put("  ");
if (context.realtime_enabled) { 
$h.put("    \x3Cdiv id\x3D\x22dsq\x2Drealtime\x2Doptions\x22 class\x3D\x22dsq\x2Doptions\x22\x3E      ");
$h.put(trans("Real\x2Dtime updating is"));
$h.put("      \x3Cstrong id\x3D\x22dsq\x2Drealtime\x2Dstatus\x22 style\x3D\x22text\x2Dtransform:lowercase\x22\x3E");
$h.put(trans("enabled"));
$h.put("\x3C/strong\x3E.      \x3Ca href\x3D\x22#\x22 id\x3D\x22dsq\x2Drealtime\x2Dtoggle\x22 style\x3D\x22text\x2Dtransform:capitalize\x22\x3E\x3C/a\x3E    \x3C/div\x3E  ");
}
return $h.compile();

}

};
$d.blocks["commentDate"] = function block_commentDate ($globals, $locals) {

    var $h = new $d.Builder();

    var localScope = DISQUS.extend({}, $globals, $locals);
    with (localScope) {

$h.put("  \x3Ca href\x3D\x22#comment\x2D");
$h.put(($h.esc || function (s) { return s; })(comment.id));
$h.put("\x22    onclick\x3D\x22DISQUS.dtpl.actions.fire(\x27comments.permalink\x27, ");
$h.put(($h.esc || function (s) { return s; })(comment.id));
$h.put(")\x3B\x22    title\x3D\x22");
$h.put($d.interpolate(trans("Link to comment by %(author)s"), { "author": comment.author.display_name }));
$h.put("\x22\x3E    ");
if (comment.is_realtime) { 
$h.put("      ");
$h.put(trans("Just now"));
$h.put("    ");
} else {
$h.put("      ");
$h.put(($h.esc || function (s) { return s; })(comment.date));
$h.put("    ");
}
$h.put("  \x3C/a\x3E");
return $h.compile();

}

};
$d.blocks["postbox"] = function block_postbox ($globals, $locals) {

    var $h = new $d.Builder();

    var localScope = DISQUS.extend({}, $globals, $locals);
    with (localScope) {

$h.put("  \x3Cdiv class\x3D\x22dsq\x2Dreply ");
if (comment) { 
$h.put("dsq\x2Dshow\x2Dtools dsq\x2Dshow\x2Dtools\x2Dfinished");
}
$h.put("\x22 id\x3D\x22dsq\x2Dreply");
if (comment) { 
$h.put("\x2D");
$h.put(($h.esc || function (s) { return s; })(comment.id));
}
$h.put("\x22\x3E    ");
if (!comment) { 
$h.put("      \x3Cdiv id\x3D\x22dsq\x2Daccount\x2Ddropdown\x22\x3E        ");
if (!request.is_authenticated) { 
$h.put("          \x3Ca href\x3D\x22#\x22 onclick\x3D\x22DISQUS.dtpl.actions.fire(\x27auth.login\x27)\x3B return false\x3B\x22\x3E");
$h.put(trans("Login"));
$h.put("\x3C/a\x3E        ");
} else {
$h.put("          ");
if (request.is_sso && config.sso && config.sso.logout) { 
$h.put("            \x3Ca href\x3D\x22");
$h.put(($h.esc || function (s) { return s; })(config.sso.logout));
$h.put("\x22\x3E");
$h.put(trans("Logout"));
$h.put("\x3C/a\x3E          ");
} else {
$h.put("            \x3Ca href\x3D\x22");
$h.put(($h.esc || function (s) { return s; })(urls.logout));
$h.put("?ctkn\x3D");
$h.put(($h.esc || function (s) { return s; })(context.csrf_token));
$h.put("\x22\x3E");
$h.put(trans("Logout"));
$h.put("\x3C/a\x3E          ");
}
$h.put("        ");
}
$h.put("      \x3C/div\x3E      \x3Ch3\x3E");
$h.put(trans("Add New Comment"));
$h.put("\x3C/h3\x3E    ");
} else {
$h.put("      \x3Ch3 style\x3D\x22clear: both\x22\x3E");
$h.put(trans("Replying to"));
$h.put(" ");
$h.put(($h.esc || function (s) { return s; })(comment.author.display_name));
$h.put("\x3C/h3\x3E    ");
}
$h.put("    \x3Cdiv class\x3D\x22dsq\x2Davatar\x22\x3E      ");
if (request.is_authenticated) { 
$h.put("        \x3Ca href\x3D\x22#\x22 onclick\x3D\x22return DISQUS.dtpl.actions.fire(\x27profile.show\x27, null, \x27");
$h.put(($h.esc || function (s) { return s; })(request.userkey));
$h.put("\x27)\x3B return false\x22\x3E          \x3Cimg src\x3D\x22");
$h.put(($h.esc || function (s) { return s; })(urls.request_user_avatar));
$h.put("\x22 alt\x3D\x22");
$h.put(($h.esc || function (s) { return s; })(request.display_username));
$h.put("\x22 \x3E        \x3C/a\x3E      ");
} else {
$h.put("        \x3Cimg src\x3D\x22");
$h.put(($h.esc || function (s) { return s; })(forum.default_avatar_url));
$h.put("\x22/\x3E      ");
}
$h.put("    \x3C/div\x3E    \x3Cdiv class\x3D\x22dsq\x2Dtextarea dsq\x2Dtextarea\x2Dreply\x22\x3E      \x3Cdiv class\x3D\x22dsq\x2Dtextarea\x2Dbackground\x22\x3E        \x3Cdiv class\x3D\x22dsq\x2Dtextarea\x2Dwrapper\x22\x3E          \x3C!\x2D\x2D filled dynamically \x2D\x2D\x3E        \x3C/div\x3E        ");
if (context.switches.upload_media) { 
$h.put("          \x3Cdiv id\x3D\x22dsq\x2Dmedia\x2Dpreview");
$h.put(($h.esc || function (s) { return s; })(comment ? ('-' + comment.id) : ''));
$h.put("\x22 class\x3D\x22dsq\x2Dmedia\x2Dpreview\x22 style\x3D\x22display:none\x22\x3E          \x3C/div\x3E        ");
}
$h.put("        \x3Cdiv class\x3D\x22dsq\x2Dpost\x2Dtools\x22\x3E          \x3Cul\x3E            \x3Cli class\x3D\x22dsq\x2Dpost\x2Das\x22\x3E              ");
if (request.is_authenticated) { 
$h.put("                \x3Cbutton type\x3D\x22button\x22 class\x3D\x22dsq\x2Dbutton\x22                  onclick\x3D\x22DISQUS.dtpl.actions.fire(\x27comments.send\x27, ");
$h.put(($h.esc || function (s) { return s; })(comment ? comment.id : 'null'));
$h.put(", this)\x3B\x22\x3E                  ");
$h.put(trans("Post as"));
$h.put(" ");
$h.put(($h.esc || function (s) { return s; })(request.display_username));
$h.put("                \x3C/button\x3E              ");
} else {
$h.put("                  \x3Cbutton type\x3D\x22button\x22 class\x3D\x22dsq\x2Dbutton\x22                    onclick\x3D\x22DISQUS.dtpl.actions.fire(\x27comments.validate\x27, ");
$h.put(($h.esc || function (s) { return s; })(comment ? comment.id : 'null'));
$h.put(", this)\x3B\x22\x3E                    ");
$h.put(trans("Post as"));
$h.put(" \x26hellip\x3B                  \x3C/button\x3E              ");
}
$h.put("            \x3C/li\x3E            ");
if (context.switches.upload_media && forum.use_media) { 
$h.put("              \x3Cli class\x3D\x22dsq\x2Dattach\x2Dmedia\x22\x3E                \x3Cdiv class\x3D\x22dsq\x2Dattach\x2Dmedia\x2Dcontainer\x22\x3E                  \x3Cspan\x3E");
$h.put(trans("Image"));
$h.put("\x3C/span\x3E                  \x3C!\x2D\x2D filled dynamically \x2D\x2D\x3E                \x3C/div\x3E              \x3C/li\x3E            ");
}
$h.put("            \x3Cli class\x3D\x22dsq\x2Dshare\x2Don dsq\x2Dclearfix\x22\x3E              ");
(function () {
var $l = {};
$d.extend($l, $locals);
$d.extend($l, {});
$h.put($d.renderBlock("commentShare", $l));
}());
$h.put("            \x3C/li\x3E          \x3C/ul\x3E        \x3C/div\x3E      \x3C/div\x3E    \x3C/div\x3E  \x3C/div\x3E");
return $h.compile();

}

};
$d.blocks["header"] = function block_header ($globals, $locals) {

    var $h = new $d.Builder();

    var localScope = DISQUS.extend({}, $globals, $locals);
    with (localScope) {

$h.put("    ");
(function () {
var $l = {};
$d.extend($l, $locals);
$d.extend($l, {});
$h.put($d.renderBlock("maintenanceNotice", $l));
}());
$h.put("    ");
if (!integration.reply_position) { 
$h.put("      ");
if (context.show_reply) { 
$h.put("        ");
(function () {
var $l = {};
$d.extend($l, $locals);
$d.extend($l, {});
$h.put($d.renderBlock("postbox", $l));
}());
$h.put("      ");
}
$h.put("      ");
(function () {
var $l = {};
$d.extend($l, $locals);
$d.extend($l, {});
$h.put($d.renderBlock("realtimeNotice", $l));
}());
$h.put("    ");
}
$h.put("    ");
(function () {
var $l = {};
$d.extend($l, $locals);
$d.extend($l, {});
$h.put($d.renderBlock("permissionNotice", $l));
}());
$h.put("    ");
(function () {
var $l = {};
$d.extend($l, $locals);
$d.extend($l, {});
$h.put($d.renderBlock("commentSort", $l));
}());
$h.put("    ");
(function () {
var $l = {};
$d.extend($l, $locals);
$d.extend($l, {});
$h.put($d.renderBlock("commentCount", $l));
}());
return $h.compile();

}

};
$d.blocks["comments"] = function block_comments ($globals, $locals) {

    var $h = new $d.Builder();

    var localScope = DISQUS.extend({}, $globals, $locals);
    with (localScope) {

$h.put("  ");
(function () {
var $l = {};
$d.extend($l, $locals);
$d.extend($l, {});
$h.put($d.renderBlock("realtimeAlert", $l));
}());
$h.put("  \x3Cul id\x3D\x22dsq\x2Dcomments\x22\x3E    ");
$d.each(comments, function (comment, $index, $collection) {
var $locals = { "comment": comment, "index": $index };
$h.put("      ");
(function () {
var $l = {};
$d.extend($l, $locals);
$d.extend($l, {});
$h.put($d.renderBlock("comment", $l));
}());
$h.put("    ");
});
$h.put("  \x3C/ul\x3E  ");
(function () {
var $l = {};
$d.extend($l, $locals);
$d.extend($l, {});
$h.put($d.renderBlock("realtimeAlert", $l));
}());
return $h.compile();

}

};
$d.blocks["realtimeAlert"] = function block_realtimeAlert ($globals, $locals) {

    var $h = new $d.Builder();

    var localScope = DISQUS.extend({}, $globals, $locals);
    with (localScope) {

$h.put("  ");
if (context.realtime_enabled && !forum.streaming_realtime) { 
$h.put("    \x3Cdiv style\x3D\x22display:none\x3B\x22 class\x3D\x22dsq\x2Dnotice dsq\x2Drealtime\x2Dalert\x22\x3E\x3C/div\x3E  ");
}
return $h.compile();

}

};
$d.blocks["commentLikes"] = function block_commentLikes ($globals, $locals) {

    var $h = new $d.Builder();

    var localScope = DISQUS.extend({}, $globals, $locals);
    with (localScope) {

$h.put("  \x3Ca href\x3D\x22#\x22 id\x3D\x22dsq\x2Dcomment\x2Dlike\x2Dcount\x2D");
$h.put(($h.esc || function (s) { return s; })(comment.id));
$h.put("\x22 class\x3D\x22dsq\x2Dcomment\x2Dlike\x2Dcount\x22    onclick\x3D\x22return DISQUS.dtpl.actions.fire(\x27comments.showUserVotes\x27, ");
$h.put(($h.esc || function (s) { return s; })(comment.id));
$h.put(")\x3B return false\x22\x3E");
$h.put(($h.esc || function (s) { return s; })(comment.points));
$h.put("    ");
if (comment.points > 1) { 
$h.put("      ");
$h.put(trans("Likes"));
$h.put("    ");
} else {
$h.put("      ");
$h.put(trans("Like"));
$h.put("    ");
}
$h.put("  \x3C/a\x3E");
return $h.compile();

}

};
$d.blocks["commentMessage"] = function block_commentMessage ($globals, $locals) {

    var $h = new $d.Builder();

    var localScope = DISQUS.extend({}, $globals, $locals);
    with (localScope) {

$h.put("  \x3Cdiv class\x3D\x22");
$h.put(($h.esc || function (s) { return s; })(cls));
$h.put("\x22 id\x3D\x22dsq\x2Dcomment\x2Dmessage\x2D");
$h.put(($h.esc || function (s) { return s; })(comment.id));
$h.put("\x22\x3E    ");
if (comment.killed) { 
$h.put("      \x3Cem\x3E");
$h.put(trans("Comment removed."));
$h.put("\x3C/em\x3E    ");
} else if (!comment.approved) {
$h.put("      \x3Cem\x3E");
$h.put(trans("This comment was flagged for review."));
$h.put("\x3C/em\x3E    ");
} else {
$h.put("      ");
$h.put("      \x3Cdiv class\x3D\x22dsq\x2Dcomment\x2Dtext\x22 id\x3D\x22dsq\x2Dcomment\x2Dtext\x2D");
$h.put(($h.esc || function (s) { return s; })(comment.id));
$h.put("\x22\x3E        ");
$h.put(($h.esc || function (s) { return s; })(comment.message));
$h.put("      \x3C/div\x3E      ");
$h.put("      ");
if (forum.comment_max_words != 0) { 
$h.put("        \x3Ca href\x3D\x22#\x22 class\x3D\x22dsq\x2Dcomment\x2Dtruncate\x2Dexpand\x22 onclick\x3D\x22return DISQUS.dtpl.actions.fire(\x27comments.text.expand\x27, ");
$h.put(($h.esc || function (s) { return s; })(comment.id));
$h.put(")\x3B\x22\x3E ");
$h.put(trans("show more"));
$h.put("\x3C/a\x3E        \x3Ca href\x3D\x22#\x22 class\x3D\x22dsq\x2Dcomment\x2Dtruncate\x2Dcollapse\x22 onclick\x3D\x22return DISQUS.dtpl.actions.fire(\x27comments.text.collapse\x27, ");
$h.put(($h.esc || function (s) { return s; })(comment.id));
$h.put(")\x3B\x22\x3E ");
$h.put(trans("show less"));
$h.put("\x3C/a\x3E      ");
}
$h.put("      ");
if (comment.last_modified_by == 'moderator') { 
$h.put("        \x3Cp class\x3D\x22dsq\x2Deditedtxt\x22\x3E(");
$h.put(trans("Edited by a moderator"));
$h.put(")\x3C/p\x3E      ");
} else if (comment.last_modified_by == 'author' && comment.has_replies) {
$h.put("        \x3Cp class\x3D\x22dsq\x2Deditedtxt\x22\x3E(");
$h.put(trans("Edited by author"));
$h.put(" ");
$h.put(($h.esc || function (s) { return s; })(comment.last_modified_date));
$h.put(")\x3C/p\x3E      ");
}
$h.put("    ");
}
$h.put("  \x3C/div\x3E");
return $h.compile();

}

};
$d.blocks["commentFooter"] = function block_commentFooter ($globals, $locals) {

    var $h = new $d.Builder();

    var localScope = DISQUS.extend({}, $globals, $locals);
    with (localScope) {

$h.put("  \x3Cdiv class\x3D\x22dsq\x2Dcomment\x2Dfooter\x22\x3E    \x3Cul class\x3D\x22dsq\x2Dcomment\x2Dactions\x22\x3E      ");
if (comment.votable) { 
$h.put("        \x3Cli id\x3D\x22dsq\x2Dlike\x2D");
$h.put(($h.esc || function (s) { return s; })(comment.id));
$h.put("\x22 ");
if (comment.up_voted) { 
$h.put("class\x3D\x22dsq\x2Dis\x2Dliked\x22");
}
$h.put("\x3E          \x3Cspan class\x3D\x22dsq\x2Dlike\x2Dthumb dsq\x2Dfont\x22\x3EA\x3C/span\x3E          ");
$h.put("\x3Ca href\x3D\x22#\x22 onclick\x3D\x22DISQUS.dtpl.actions.fire(\x27comments.like\x27, this,");
$h.put(($h.esc || function (s) { return s; })(comment.id));
$h.put(")\x3B return false\x22\x3E");
if (comment.up_voted) { 
$h.put(trans("Liked"));
} else {
$h.put(trans("Like"));
}
$h.put("\x3C/a\x3E");
$h.put("        \x3C/li\x3E      ");
}
$h.put("      ");
if (comment.can_edit) { 
$h.put("        \x3Cli\x3E          ");
$h.put("\x3Ca href\x3D\x22#\x22 class\x3D\x22dsq\x2Dcomment\x2Dreply\x22 onclick\x3D\x22DISQUS.dtpl.actions.fire(\x27comments.edit\x27,");
$h.put(($h.esc || function (s) { return s; })(comment.id));
$h.put(")\x3B return false\x22\x3E");
$h.put(trans("Edit"));
$h.put("\x3C/a\x3E");
$h.put("        \x3C/li\x3E      ");
}
$h.put("      ");
if (comment.can_reply) { 
$h.put("        \x3Cli\x3E          ");
$h.put("\x3Ca href\x3D\x22#\x22 class\x3D\x22dsq\x2Dcomment\x2Dreply\x22 onclick\x3D\x22DISQUS.dtpl.actions.fire(\x27comments.reply\x27,");
$h.put(($h.esc || function (s) { return s; })(comment.id));
$h.put(", this)\x3B return false\x22\x3E");
$h.put(trans("Reply"));
$h.put("\x3C/a\x3E");
$h.put("        \x3C/li\x3E      ");
}
$h.put("   \x3C/ul\x3E    \x3Cul class\x3D\x22dsq\x2Dcomment\x2Dmeta\x22\x3E      \x3Cli\x3E");
(function () {
var $l = {};
$d.extend($l, $locals);
$d.extend($l, {});
$h.put($d.renderBlock("commentDate", $l));
}());
$h.put("\x3C/li\x3E      ");
if (comment.parent && comment.parent.author.display_name) { 
$h.put("        \x3Cli\x3E          \x3Ca onclick\x3D\x22DISQUS.dtpl.actions.fire(\x27comments.showParent\x27, ");
$h.put(($h.esc || function (s) { return s; })(comment.parent_post_id));
$h.put(")\x3B return false\x22            href\x3D\x22#comment\x2D");
$h.put(($h.esc || function (s) { return s; })(comment.parent_post_id));
$h.put("\x22 title\x3D\x22");
$h.put(trans("Jump to comment"));
$h.put("\x22\x3E            ");
$h.put(trans("in reply to"));
$h.put(" ");
$h.put(($h.esc || function (s) { return s; })(comment.parent.author.display_name));
$h.put("          \x3C/a\x3E        \x3C/li\x3E      ");
}
$h.put("      \x3Cli ");
if (comment.points <= 0) { 
$h.put("style\x3D\x22display:none\x22");
}
$h.put("\x3E        ");
(function () {
var $l = {};
$d.extend($l, $locals);
$d.extend($l, {});
$h.put($d.renderBlock("commentLikes", $l));
}());
$h.put("      \x3C/li\x3E      ");
if (request.is_moderator) { 
$h.put("        \x3Cli class\x3D\x22dsq\x2Dcomment\x2Dmoderate\x22 style\x3D\x22visibility: hidden\x22\x3E          \x3Ca href\x3D\x22#\x22 onclick\x3D\x22return DISQUS.dtpl.actions.fire(\x27comments.moderate.options\x27, ");
$h.put(($h.esc || function (s) { return s; })(comment.id));
$h.put(")\x3B\x22\x3E");
$h.put(trans("Moderate"));
$h.put("\x3C/a\x3E        \x3C/li\x3E      ");
} else {
$h.put("        \x3Cli class\x3D\x22dsq\x2Dcomment\x2Dflag\x22 style\x3D\x22visibility: hidden\x22\x3E          \x3Ca href\x3D\x22#\x22 class\x3D\x22dsq\x2Dcomment\x2Dflag dsq\x2Dfont\x22 onclick\x3D\x22return DISQUS.dtpl.actions.fire(\x27comments.report\x27, ");
$h.put(($h.esc || function (s) { return s; })(comment.id));
$h.put(", false)\x3B\x22\x3EF\x3C/a\x3E        \x3C/li\x3E      ");
}
$h.put("    \x3C/ul\x3E  \x3C/div\x3E");
return $h.compile();

}

};
$d.blocks["editArea"] = function block_editArea ($globals, $locals) {

    var $h = new $d.Builder();

    var localScope = DISQUS.extend({}, $globals, $locals);
    with (localScope) {

$h.put("  \x3Cdiv id\x3D\x22dsq\x2Dedit\x2D");
$h.put(($h.esc || function (s) { return s; })(comment.id));
$h.put("\x22 class\x3D\x22dsq\x2Dedit\x22\x3E    \x3Cdiv class\x3D\x22dsq\x2Dtextarea\x22\x3E      \x3Cdiv class\x3D\x22dsq\x2Dtextarea\x2Dbackground\x22\x3E        \x3Cdiv class\x3D\x22dsq\x2Dtextarea\x2Dwrapper\x22\x3E          \x3C!\x2D\x2D filled dynamically \x2D\x2D\x3E        \x3C/div\x3E      \x3C/div\x3E    \x3C/div\x3E    \x3Cdiv class\x3D\x22dsq\x2Dsave\x2Dedit\x22\x3E      \x3Cbutton type\x3D\x22button\x22 class\x3D\x22dsq\x2Dbutton\x22        onclick\x3D\x22DISQUS.dtpl.actions.fire(\x27comments.edit.send\x27, ");
$h.put(($h.esc || function (s) { return s; })(comment.id));
$h.put(", this)\x3B return false\x22\x3E");
$h.put(trans("Save edit"));
$h.put("\x3C/button\x3E      \x3Cspan\x3E");
$h.put(trans("or"));
$h.put("\x3C/span\x3E      \x3Ca href\x3D\x22#\x22 class\x3D\x22dsq\x2Dcancel\x22 onclick\x3D\x22DISQUS.dtpl.actions.fire(\x27comments.edit.cancel\x27, ");
$h.put(($h.esc || function (s) { return s; })(comment.id));
$h.put(")\x3B return false\x22\x3E        ");
$h.put(trans("Cancel"));
$h.put("      \x3C/a\x3E    \x3C/div\x3E  \x3C/div\x3E");
return $h.compile();

}

};
$d.blocks["reaction"] = function block_reaction ($globals, $locals) {

    var $h = new $d.Builder();

    var localScope = DISQUS.extend({}, $globals, $locals);
    with (localScope) {

$h.put("  \x3Cli id\x3D\x22dsq\x2Dreaction\x2D");
$h.put(($h.esc || function (s) { return s; })(reaction.id));
$h.put("\x22\x3E    \x3Cdiv class\x3D\x22dsq\x2Dreaction\x2Davatar dsq\x2Davatar dsq\x2Dtt\x22 data\x2Ddsq\x2Dcontent\x2Did\x3D\x22dsq\x2Dreaction\x2Dtooltip\x2D");
$h.put(($h.esc || function (s) { return s; })(reaction.id));
$h.put("\x22\x3E      ");
if (request.is_moderator) { 
$h.put("        \x3Ca href\x3D\x22#\x22 class\x3D\x22dsq\x2Dremove\x2Dreaction\x22 title\x3D\x22Remove Reaction\x22 style\x3D\x22display: none\x22          onclick\x3D\x22DISQUS.dtpl.actions.fire(\x27reactions.hide\x27, ");
$h.put(($h.esc || function (s) { return s; })(reaction.id));
$h.put(")\x3B return false\x22\x3EHide reaction\x3C/a\x3E      ");
}
$h.put("      ");
if (reaction.url) { 
$h.put("        \x3Ca target\x3D\x22_blank\x22 href\x3D\x22");
$h.put(($h.esc || function (s) { return s; })(reaction.url));
$h.put("\x22\x3E      ");
}
$h.put("      ");
if (reaction.avatar_url) { 
$h.put("        \x3Cimg src\x3D\x22");
$h.put(($h.esc || function (s) { return s; })(reaction.avatar_url));
$h.put("\x22/\x3E      ");
} else {
$h.put("        \x3Cimg src\x3D\x22");
$h.put(($h.esc || function (s) { return s; })(forum.default_avatar_url));
$h.put("\x22/\x3E      ");
}
$h.put("      ");
if (reaction.url) { 
$h.put("        \x3C/a\x3E      ");
}
$h.put("    \x3C/div\x3E    \x3Cdiv id\x3D\x22dsq\x2Dreaction\x2Dtooltip\x2D");
$h.put(($h.esc || function (s) { return s; })(reaction.id));
$h.put("\x22 class\x3D\x22dsq\x2Dreaction\x2Dtooltip\x22 style\x3D\x22display:none\x22\x3E      \x3Cdiv class\x3D\x22dsq\x2Dreaction\x2Dtooltip\x2Dcontainer\x22\x3E        \x3Cdiv class\x3D\x22dsq\x2Dreaction\x2Dbody\x22\x3E");
$h.put(($h.esc || function (s) { return s; })(reaction.body));
$h.put("\x3C/div\x3E        \x3Cdiv class\x3D\x22dsq\x2Dreaction\x2Ddate\x22\x3E");
$h.put(($h.esc || function (s) { return s; })(reaction.date_created));
$h.put("\x3C/div\x3E        \x3Cdiv class\x3D\x22dsq\x2Dreaction\x2Duser\x22\x3E@");
$h.put(($h.esc || function (s) { return s; })(reaction.author_name));
$h.put("\x3C/div\x3E      \x3C/div\x3E    \x3C/div\x3E  \x3C/li\x3E");
return $h.compile();

}

};
$d.blocks["pagination"] = function block_pagination ($globals, $locals) {

    var $h = new $d.Builder();

    var localScope = DISQUS.extend({}, $globals, $locals);
    with (localScope) {

$h.put("  \x3Cul id\x3D\x22dsq\x2Dfooter\x22 class\x3D\x22dsq\x2Dclearfix\x22\x3E    ");
if (thread.pagination_type == 'num' && thread.num_pages > 1) { 
$h.put("      \x3Cli class\x3D\x22dsq\x2Dnumbered\x2Dpagination\x22\x3E        ");
$h.put("        ");
if (request.page > 1) { 
$h.put("          \x26larr\x3B          ");
$h.put("\x3Ca href\x3D\x22#dsq\x2Dcomments\x22 title\x3D\x22");
$h.put(trans("Previous"));
$h.put("\x22              onclick\x3D\x22DISQUS.dtpl.actions.fire(\x27thread.paginate\x27,");
$h.put(($h.esc || function (s) { return s; })(request.page - 1));
$h.put(")\x3B return false\x22\x3E");
$h.put(trans("Previous"));
$h.put("\x3C/a\x3E");
$h.put("          \x26nbsp\x3B        ");
}
$h.put("        ");
$h.put("        ");
if (request.page != 1 && !lang.contains(thread.page_numbers, 1)) { 
$h.put("          \x3Ca href\x3D\x22#dsq\x2Dcomments\x22 onclick\x3D\x22DISQUS.dtpl.actions.fire(\x27thread.paginate\x27, 1)\x3B return false\x22\x3E1\x3C/a\x3E          \x26hellip\x3B        ");
}
$h.put("        ");
$d.each(thread.page_numbers, function (number, $index, $collection) {
var $locals = { "number": number, "index": $index };
$h.put("          ");
if (request.page == number) { 
$h.put("\x3Cspan\x3E");
$h.put(($h.esc || function (s) { return s; })(number));
$h.put("\x3C/span\x3E");
} else {
$h.put("\x3Ca href\x3D\x22#dsq\x2Dcomments\x22 onclick\x3D\x22DISQUS.dtpl.actions.fire(\x27thread.paginate\x27,");
$h.put(($h.esc || function (s) { return s; })(number));
$h.put(")\x3B return false\x22\x3E");
$h.put(($h.esc || function (s) { return s; })(number));
$h.put("\x3C/a\x3E");
}
$h.put("        ");
});
$h.put("        ");
$h.put("        ");
if (request.page != thread.num_pages && !lang.contains(thread.page_numbers, thread.num_pages)) { 
$h.put("          \x26hellip\x3B          ");
$h.put("\x3Ca href\x3D\x22#dsq\x2Dcomments\x22 onclick\x3D\x22DISQUS.dtpl.actions.fire(\x27thread.paginate\x27,");
$h.put(($h.esc || function (s) { return s; })(thread.num_pages));
$h.put(")\x3B return false\x22\x3E");
$h.put(($h.esc || function (s) { return s; })(thread.num_pages));
$h.put("\x3C/a\x3E");
$h.put("        ");
}
$h.put("        ");
$h.put("        ");
if (request.page < thread.num_pages) { 
$h.put("          \x26nbsp\x3B          ");
$h.put("\x3Ca href\x3D\x22#dsq\x2Dcomments\x22  title\x3D\x22");
$h.put(trans("Next"));
$h.put("\x22              onclick\x3D\x22DISQUS.dtpl.actions.fire(\x27thread.paginate\x27,");
$h.put(($h.esc || function (s) { return s; })(request.page + 1));
$h.put(")\x3B return false\x22\x3E");
$h.put(trans("Next"));
$h.put("\x3C/a\x3E");
$h.put("          \x26rarr\x3B        ");
}
$h.put("      \x3C/li\x3E    ");
}
$h.put("    \x3Cdiv id\x3D\x22dsq\x2Dsubscribe\x22\x3E      ");
(function () {
var $l = {};
$d.extend($l, $locals);
$d.extend($l, {});
$h.put($d.renderBlock("subscribe", $l));
}());
$h.put("    \x3C/div\x3E  \x3C/ul\x3E  ");
if (thread.pagination_type == 'append' && thread.num_pages > 1) { 
$h.put("    ");
if (request.page < thread.num_pages) { 
$h.put("      \x3Ca class\x3D\x22dsq\x2Dmore\x2Dbutton\x22 href\x3D\x22#\x22        onclick\x3D\x22DISQUS.dtpl.actions.fire(\x27thread.paginate\x27, ");
$h.put(($h.esc || function (s) { return s; })(request.page + 1));
$h.put(", this)\x3B return false\x22\x3E        ");
$h.put(trans("Load more comments"));
$h.put("      \x3C/a\x3E    ");
}
$h.put("  ");
}
return $h.compile();

}

};
$d.blocks["permissionNotice"] = function block_permissionNotice ($globals, $locals) {

    var $h = new $d.Builder();

    var localScope = DISQUS.extend({}, $globals, $locals);
    with (localScope) {

$h.put("  ");
if (request.missing_perm && request.missing_perm.match(/locked|blacklist|verify/)) { 
$h.put("    \x3Cdiv class\x3D\x22dsq\x2Dnotice\x22\x3E      ");
if (request.missing_perm == 'locked') { 
$h.put("        ");
$h.put(trans("Comments for this page are closed."));
$h.put("      ");
} else if (request.missing_perm == 'blacklist') {
$h.put("        ");
$h.put(trans("The site has blocked you from posting new comments."));
$h.put("      ");
} else if (request.missing_perm == 'verify') {
$h.put("        ");
$h.put(trans("You must verify your Disqus Profile email address before your comments are approved."));
$h.put("        \x3Ca href\x3D\x22");
$h.put(($h.esc || function (s) { return s; })(urls.verify_email));
$h.put("\x22 target\x3D\x22_blank\x22\x3E");
$h.put(trans("Click here to verify"));
$h.put("\x3C/a\x3E      ");
}
$h.put("    \x3C/div\x3E  ");
}
return $h.compile();

}

};
$d.blocks["thread"] = function block_thread ($globals, $locals) {

    var $h = new $d.Builder();

    var localScope = DISQUS.extend({}, $globals, $locals);
    with (localScope) {

$h.put("  ");
(function () {
var $l = {};
$d.extend($l, $locals);
$d.extend($l, {});
$h.put($d.renderBlock("globalToolbar", $l));
}());
$h.put("  ");
(function () {
var $l = {};
$d.extend($l, $locals);
$d.extend($l, {});
$h.put($d.renderBlock("header", $l));
}());
$h.put("  ");
(function () {
var $l = {};
$d.extend($l, $locals);
$d.extend($l, {});
$h.put($d.renderBlock("comments", $l));
}());
$h.put("  ");
(function () {
var $l = {};
$d.extend($l, $locals);
$d.extend($l, {});
$h.put($d.renderBlock("footer", $l));
}());
return $h.compile();

}

};
$d.blocks["footer"] = function block_footer ($globals, $locals) {

    var $h = new $d.Builder();

    var localScope = DISQUS.extend({}, $globals, $locals);
    with (localScope) {

$h.put("  \x3Cdiv id\x3D\x22dsq\x2Dpagination\x22\x3E    ");
(function () {
var $l = {};
$d.extend($l, $locals);
$d.extend($l, {});
$h.put($d.renderBlock("pagination", $l));
}());
$h.put("  \x3C/div\x3E  ");
if (integration.reply_position) { 
$h.put("    ");
(function () {
var $l = {};
$d.extend($l, $locals);
$d.extend($l, {});
$h.put($d.renderBlock("realtimeNotice", $l));
}());
$h.put("    ");
if (context.show_reply) { 
$h.put("      ");
(function () {
var $l = {};
$d.extend($l, $locals);
$d.extend($l, {});
$h.put($d.renderBlock("postbox", $l));
}());
$h.put("    ");
}
$h.put("  ");
}
$h.put("  ");
(function () {
var $l = {};
$d.extend($l, $locals);
$d.extend($l, {});
$h.put($d.renderBlock("reactions", $l));
}());
$h.put("  ");
(function () {
var $l = {};
$d.extend($l, $locals);
$d.extend($l, {});
$h.put($d.renderBlock("trackbacks", $l));
}());
return $h.compile();

}

};
$d.blocks["cookieFailure"] = function block_cookieFailure ($globals, $locals) {

    var $h = new $d.Builder();

    var localScope = DISQUS.extend({}, $globals, $locals);
    with (localScope) {

$h.put("  \x3Cp class\x3D\x22dsq\x2Dnotice dsq\x2Derror\x22\x3E    \x3Cstrong\x3E");
$h.put(trans("Warning"));
$h.put(":\x3C/strong\x3E ");
$h.put(trans("A browser setting is preventing you from logging in."));
$h.put("    ");
$h.put("\x3Ca href\x3D\x22#\x22 onclick\x3D\x22DISQUS.dtpl.actions.fire(\x27help.login\x27)\x3B return false\x22\x3E");
$h.put(trans("Fix this setting to log in"));
$h.put("\x3C/a\x3E");
$h.put("  \x3C/p\x3E");
return $h.compile();

}

};
$d.blocks["commentSort"] = function block_commentSort ($globals, $locals) {

    var $h = new $d.Builder();

    var localScope = DISQUS.extend({}, $globals, $locals);
    with (localScope) {

$h.put("  \x3Cdiv id\x3D\x22dsq\x2Dsort\x2Dby\x22\x3E    \x3Cselect id\x3D\x22dsq\x2Dsort\x2Dselect\x22 onchange\x3D\x22DISQUS.dtpl.actions.fire(\x27thread.sort\x27, this.value)\x3B\x22\x3E      ");
$d.each(sorting, function (option, $index, $collection) {
var $locals = { "option": option, "index": $index };
$h.put("        \x3Coption value\x3D\x22");
$h.put(($h.esc || function (s) { return s; })(option.value));
$h.put("\x22 ");
if (option.selected) { 
$h.put("selected\x3D\x22selected\x22");
}
$h.put("\x3E          ");
$h.put(trans("Sort by"));
$h.put(" ");
$h.put(($h.esc || function (s) { return s; })(option.label.toLowerCase()));
$h.put("        \x3C/option\x3E      ");
});
$h.put("    \x3C/select\x3E  \x3C/div\x3E");
return $h.compile();

}

};
$d.blocks["commentShare"] = function block_commentShare ($globals, $locals) {

    var $h = new $d.Builder();

    var localScope = DISQUS.extend({}, $globals, $locals);
    with (localScope) {

$h.put("  ");
if (request.is_authenticated && (request.sharing.twitter.enabled || request.sharing.facebook.enabled)) { 
$h.put("    \x3Ch4\x3E");
$h.put(trans("Share on"));
$h.put(":\x3C/h4\x3E    ");
if (request.sharing.twitter.enabled) { 
$h.put("      \x3Cspan class\x3D\x22dsq\x2Dshare\x2Dtwitter\x22        onclick\x3D\x22DISQUS.dtpl.actions.fire(\x27share.toggle\x27, this, \x27twitter\x27, ");
$h.put(($h.esc || function (s) { return s; })(comment ? comment.id : 'null'));
$h.put(")\x3B\x22\x3E        Twitter      \x3C/span\x3E    ");
}
$h.put("    ");
if (request.sharing.facebook.enabled) { 
$h.put("      \x3Cspan class\x3D\x22dsq\x2Dshare\x2Dfacebook\x22        onclick\x3D\x22DISQUS.dtpl.actions.fire(\x27share.toggle\x27, this, \x27facebook\x27, ");
$h.put(($h.esc || function (s) { return s; })(comment ? comment.id : 'null'));
$h.put(")\x3B\x22\x3E        Facebook      \x3C/span\x3E    ");
}
$h.put("    \x3C/div\x3E  ");
}
return $h.compile();

}

};
    });

(function (window, undefined) {
var document = window.document, DISQUS = window.DISQUS;

// CAUTION!
// If you modify this function, bear in mind that
// it is used by both Custom and Next so be careful!
DISQUS.registerActions = function () {
    /**
 * Actions for the Houdini theme
 */

var add  = DISQUS.dtpl.actions.register;
var fire = DISQUS.dtpl.actions.fire;

function eachChildComment(id, callback) {
    var container = DISQUS.nodes.get('#dsq-comments');
    var comments = DISQUS.nodes.get('li.dsq-comment', container);
    var start = -1;
    var rootDepth, root, i;

    // Find *all* comment elements on the page. Locate the triggered
    // comment, and its location (index) in the result set.
    for (i = 0; i < comments.length; i++) {
        if (comments[i].id == 'dsq-comment-' + id) {
            root = comments[i];
            start = i + 1;
            break;
        }
    }

    if (start == -1) {
        return; // should never happen
    }

    // Helper method returns the depth of a comment element.
    function getdepth(node) {
        return DISQUS.jsonData.posts[node.getAttribute('data-dsq-comment-id')].depth;
    }

    rootDepth = getdepth(root);

    for (i = start; i < comments.length; i++) {
        node = comments[i];

        if (getdepth(node) <= rootDepth) {
            break;
        }
        callback(node);
    }
}

add('comments.reply.onCookieFailure', function(id) {
    var noticeId = 'dsq-cookie-failure-notice' + (id ? '-' + id : '');
    if (DISQUS.nodes.get('#' + noticeId)) {
        // Already on page
        return;
    }

    var div = document.createElement('div');
    div.id = noticeId;
    div.innerHTML = DISQUS.renderBlock('cookieFailure');

    DISQUS.nodes.insertAfter(
        DISQUS.nodes.get('#dsq-reply' + (id ? '-' + id : '')),
        div
    );
});

add('comments.reply.onFocus', function(id) {
    // Only affects top-level reply box; replies-to-comments are
    // already expanded
    if (id) {
        return;
    }

    var reply = DISQUS.nodes.get('#dsq-reply');
    DISQUS.nodes.addClass(reply, 'dsq-show-tools');

    // Apply this class after some ms has passed in order to
    // trigger CSS3 transition animation
    var cb = setInterval(function() {
        DISQUS.nodes.addClass(reply, 'dsq-show-tools-finished');
        clearInterval(cb);
    }, 180);
});

add('comments.reply.onResize', function(id, height) {
    var reply = DISQUS.nodes.get('#dsq-reply' + (id ? '-' + id : ''));

    var wrapper = DISQUS.nodes.get('.dsq-textarea-wrapper', reply)[0];
    if (wrapper.style.height !== 'auto') {
        wrapper.style.height = 'auto';
    }

    var frame = DISQUS.nodes.get('iframe', wrapper)[0];
    frame.style.height = parseInt(height, 10) + 'px';
    if (DISQUS.browser.ie && frame.style.width !== '100%') {
        frame.style.width = '100%';
    }

    frame.style.height = parseInt(height, 10) + 'px';
});

/**
 * Reply box open loading animation
 */
add('comments.reply.new.onLoadingStart', function(id) {
    var reply   = DISQUS.nodes.get('#dsq-reply' + (id ? '-' + id : '')),
        wrapper = DISQUS.nodes.get('div.dsq-textarea-wrapper', reply)[0];

    DISQUS.nodes.addClass(wrapper, 'dsq-textarea-loading');

    var loading = document.createElement('div');
    loading.innerHTML = DISQUS.strings.get('Please wait') + '&hellip;';
    DISQUS.nodes.addClass(loading, 'dsq-textarea-loading-text');
    wrapper.appendChild(loading);
});

add('comments.reply.new.onLoadingEnd', function(id) {
    var reply   = DISQUS.nodes.get('#dsq-reply' + (id ? '-' + id : '')),
        wrapper = DISQUS.nodes.get('div.dsq-textarea-wrapper', reply)[0],
        loading = DISQUS.nodes.get('div.dsq-textarea-loading-text', wrapper)[0];

    DISQUS.nodes.remove(loading);
    DISQUS.nodes.removeClass(wrapper, 'dsq-textarea-loading');
});

add('comments.reply.media.upload.onLoadingStart', function(id) {
    var wrapper = DISQUS.nodes.get('#dsq-reply' + (id ? ('-' + id) : ''));
    var button = DISQUS.nodes.get('.dsq-button', wrapper)[0];

    // called right before the image is uploaded
    fire('private.setLoadingButton', button);
});

add('comments.reply.media.upload.onLoadingEnd', function(id) {
    fire('private.setLoadingButton');
});

add('comments.reply.media.upload.onSuccess', function(data, id) {

    // create image preview
    var wrapper = document.createElement('div');
    var close = document.createElement('a');
    var thumb = document.createElement('a');
    id = id || '';

    wrapper.className = 'dsq-media-wrapper';
    wrapper.appendChild(close);
    wrapper.appendChild(thumb);

    // massage the data object
    var media = data;
    data = {
        forum_id: DISQUS.jsonData.forum.id,
        thread_id: DISQUS.jsonData.thread.id,
        id: id,
        media: media
    };

    // create close button and bind close event
    close.href = '#';
    close.className = 'dsq-media-image-close';
    DISQUS.events.add(close, 'click', function(event) {
        DISQUS.dtpl.actions.fire('comments.reply.media.remove', data, id);
        event.preventDefault();
    });

    // create the thumbnail and bind popup
    thumb.href = '#';
    thumb.innerHTML = '<img class="dsq-media-image" src="' + media.thumbnailURL + '" />';
    DISQUS.events.add(thumb, 'click', function(event) {
        DISQUS.popup.popModal(
            DISQUS.renderBlock('mediaEmbedPopup', { media: media }),
            DISQUS.strings.get('Attached file'),
            null, true, 'dsq-media-embed');
        event.preventDefault();
    });

    // add hover events to close image
    DISQUS.events.add(thumb, 'mouseover', function(event) {
        event.preventDefault();
        DISQUS.nodes.show(close);
    });
    DISQUS.events.add(thumb, 'mouseout', function(event) {
        event.preventDefault();
        DISQUS.nodes.hide(close);
    });
    DISQUS.events.add(close, 'mouseover', function(event) {
        event.preventDefault();
        DISQUS.nodes.show(close);
    });
    DISQUS.events.add(close, 'mouseout', function(event) {
        event.preventDefault();
        DISQUS.nodes.hide(close);
    });

    // initially hide the close button
    DISQUS.nodes.hide(close);

    // get preview pane, and insert into DOM
    var preview = DISQUS.nodes.get('#dsq-media-preview' + (id ? ('-' + id) : ''));
    preview.appendChild(wrapper);
    DISQUS.nodes.show(preview);

});

add('comments.reply.media.remove.onSuccess', function(data) {

    // fired immediately after we the removal response from the server
    var preview = DISQUS.nodes.get('#dsq-media-preview' + (data.id ? ('-' + data.id) : ''));
    var regex;
    if (data && data.media && data.media.thumbnail) {
        regex = new RegExp(data.media.thumbnail, 'i');
    }

    // sanity check
    if (!regex || !preview) {
        return;
    }

    // remove matching images from preview pane
    DISQUS.each(DISQUS.nodes.get('img', preview), function(elem) {
        if (regex.test(elem.src)) {
            elem = DISQUS.nodes.closest(elem, '.dsq-media-wrapper');
            elem.parentNode.removeChild(elem);
            return;
        }
    });

    // if there are no more images, hide the preview pane
    if (!DISQUS.nodes.get('.dsq-media-wrapper').length) {
        DISQUS.nodes.hide(preview);
    }

});


add('comments.reply.media.upload.clear', function(id) {
    var elem = DISQUS.nodes.get('#dsq-media-preview' + (id ? ('-' + id) : ''));
    if (elem) {
        elem.innerHTML = '';
    }
});

/**
 * Collapse a comment
 */
add('comments.collapse', function(id) {
    var root = DISQUS.nodes.get('#dsq-comment-' + id);
    DISQUS.nodes.addClass(root, 'dsq-comment-is-collapsed');

    eachChildComment(id, function(node) {
        // Only hide child comments that aren't already hidden by another child
        if (!node.getAttribute('data-dsq-collapsed-parent-id')) {
            node.style.display = 'none';
            node.setAttribute('data-dsq-collapsed-parent-id', id);
        }
    });
});

/**
 * Expand a comment
 */
add('comments.expand', function(id) {
    var root = DISQUS.nodes.get('#dsq-comment-' + id);
    DISQUS.nodes.removeClass(root, 'dsq-comment-is-collapsed');

    eachChildComment(id, function(node) {
        // Only reveal child comments that were directly hidden by this comment
        if (node.getAttribute('data-dsq-collapsed-parent-id') == id) {
            node.style.display = 'block';
            node.removeAttribute('data-dsq-collapsed-parent-id');
        }
    });
});

add('comments.insert.onSuccess', function(afterId, id) {
    var comment = DISQUS.nodes.get('#dsq-comment-' + id);
    DISQUS.nodes.addClass(comment, 'dsq-comment-new');
    var cb = setInterval(function() {
        // Delayed second class to trigger CSS3 transition
        DISQUS.nodes.addClass(comment, 'dsq-comment-new-reveal');
        clearInterval(cb);
    }, 100);
});

add('comments.like.onLoadingStart', function(id) {
    var like = DISQUS.nodes.get('#dsq-like-' + id);
    DISQUS.nodes.addClass(like, 'dsq-loading');
});

add('comments.like.onLoadingEnd', function(id) {
    var like = DISQUS.nodes.get('#dsq-like-' + id);
    DISQUS.nodes.removeClass(like, 'dsq-loading');
});

add('comments.like.onSuccess', function(id, points, vote) {
    var count = DISQUS.nodes.get("#dsq-comment-like-count-" + id),
        container = DISQUS.nodes.get('#dsq-like-' + id),
        link = DISQUS.nodes.get('a', container)[0];

    if (points > 0) {
        successText = points + ' ' + DISQUS.strings.pluralize(points, 'Like', 'Likes');
        count.innerHTML = successText;
        count.style.display = 'inline';
    } else {
        count.style.display = 'none';
    }

    if (vote > 0) {
        link.innerHTML = DISQUS.strings.get('Liked');
        DISQUS.nodes.addClass(container, 'dsq-is-liked');
    } else {
        link.innerHTML = DISQUS.strings.get('Like');
        DISQUS.nodes.removeClass(container, 'dsq-is-liked');
    }
});

add('thread.paginate.onLoadingStart', function() {
    if (DISQUS.jsonData.thread.pagination_type == 'num') {
        DISQUS.window.anchor('disqus_thread');

        // Replace entire comment thread with regular spinner
        DISQUS.nodes.get('#dsq-comments').innerHTML =
            '<img src="' + DISQUS.jsonData.settings.media_url + '/images/loading.gif"/>';
    } else {
        // Replace pagination area with small spinner
        DISQUS.nodes.get('#dsq-pagination').innerHTML =
            '<img src="' + DISQUS.jsonData.settings.media_url + '/images/loading-small.gif"/>';
    }
});

add('thread.paginate.onLoadingEnd', function() {
    // DO NOTHING
});

add('thread.sort.onLoadingStart', function(type) {
    DISQUS.nodes.get('#dsq-comments').innerHTML =
        '<img src="' + DISQUS.jsonData.settings.media_url + '/images/loading.gif"/>';
});

add('thread.sort.onLoadingEnd', function(type) {
    // DO NOTHING
});

add('thread.subscribe.onSuccess', function() {
    var title = DISQUS.strings.get('Subscribed');
    var message = DISQUS.strings.get('You have subscribed to this comment thread. New comments will be sent directly to your email inbox, where you may read and respond by email.');

    DISQUS.popup.popModal(message, title);

    var subscribe = DISQUS.nodes.get('#dsq-subscribe');
    subscribe.innerHTML = DISQUS.renderBlock('subscribe');
});

add('thread.unsubscribe.onSuccess', function() {
    var title = DISQUS.strings.get('Unsubscribed');
    var message = DISQUS.strings.get('You have unsubscribed from this comment thread. New comments will no longer be sent to your email inbox.');

    DISQUS.popup.popModal(message, title);

    var subscribe = DISQUS.nodes.get('#dsq-subscribe');
    subscribe.innerHTML = DISQUS.renderBlock('subscribe');
});

add('comments.delete.onSuccess', function(id) {
    var comment = DISQUS.nodes.get('#dsq-comment-' + id);
    comment.style.display = 'none';

    var notice = document.createElement('div');
    notice.id = 'dsq-comment-restore-' + id;
    DISQUS.nodes.addClass(notice, 'dsq-notice');
    notice.innerHTML =
        '<a href="#" onclick="return DISQUS.dtpl.actions.fire(\'comments.restore\', ' + id + ');">' +
            DISQUS.strings.get('Undo') +
        '</a>';
    comment.parentNode.insertBefore(notice, comment);
});

add('comments.restore.onSuccess', function(id) {
    var notice = DISQUS.nodes.get('#dsq-comment-restore-' + id);
    DISQUS.nodes.remove(notice);

    var comment = DISQUS.nodes.get('#dsq-comment-' + id);
    comment.style.display = 'block';
});

add('comments.spam.onSuccess', function(id) {
    var comment = DISQUS.nodes.get('#dsq-comment-' + id);
    comment.style.display = 'none';
    var notice = document.createElement('div');
    DISQUS.nodes.addClass(notice, 'dsq-notice');
    notice.innerHTML = DISQUS.strings.get('Comment marked as spam.');

    comment.parentNode.insertBefore(notice, comment);
});

};

/*
 * Alias for registerActions
 * because this function is used in Next
 * to load a bunch of Javascript files that
 * contain DISQUS.define's
 */
DISQUS.runThemeScript = DISQUS.registerActions;

}(this));
