var slug_lang = "vi";

function init_paging_loai(a = "", t = "", e = 0, n = "", p = "") {
    if ("" != a) {
        0 == $("." + a + " a.active").length &&
            $("." + a + " a")
                .eq(0)
                .addClass("active");
        var d = " and " + $("." + a + " a.active").data("id");
    } else d = " and 1";
    $.ajax({ url: "ajax/paging.php", type: "post", dataType: "html", data: {slug_lang:slug_lang, id_danhmuc: 0, page_per: e, table_select: n, type_select: p, where_select: d, tab_return: t } }).done(function (a) {
        $("." + t).html(a);
    });
}
function init_paging(a = "", t = "", e = 0, n = "", p = "", d = "") {
    if ("" != a) {
        0 == $("." + a + " a.active").length &&
            $("." + a + " a")
                .eq(0)
                .addClass("active");
        var i = $("." + a + " a.active").data("id");
    } else i = 0;
    $.ajax({ url: "ajax/paging.php", type: "post", dataType: "html", data: {slug_lang:slug_lang, id_danhmuc: i, page_per: e, table_select: n, type_select: p, where_select: d, tab_return: t } }).done(function (a) {
        $("." + t).html(a);
    });
}
function init_paging_category(a = 0, t = "", e = 0, n = "", p = "", d = "") {
    $.ajax({ url: "ajax/paging.php", type: "post", dataType: "html", data: {slug_lang:slug_lang, id_danhmuc: a, page_per: e, table_select: n, type_select: p, where_select: d, tab_return: t } }).done(function (a) {
        $("." + t).html(a);
    });
}
function init_paging_category_viewmore(a = 0, t = "", e = 0, n = "", p = "", d = "", z = 1) {
    $.ajax({ url: "ajax/paging.php", type: "post", dataType: "html", data: {viewmore: 1, slug_lang:slug_lang, id_danhmuc: a, page_per: e, table_select: n, type_select: p, where_select: d, tab_return: t } }).done(function (a) {
        $("." + t).append(a);
    });
}
function init_paging_category_list(a = 0, t = "", e = "", n = 0, p = "", d = "", i = "") {
    if ("" != t) {
        0 == $("." + t + " a.active").length &&
            $("." + t + " a")
                .eq(0)
                .addClass("active");
        var l = $("." + t + " a.active").data("id");
    }
    $.ajax({ url: "ajax/paging.php", type: "post", dataType: "html", data: {slug_lang:slug_lang, id_danhmuc: a, page_per: n, table_select: p, type_select: d, where_select: i, tab_return: e, id_list: l } }).done(function (a) {
        $("." + e).html(a);
    });
}
function init_ajax_scroll(a = "", t = 0) {
    $.ajax({ url: "ajax/data.php", type: "post", dataType: "html", data: { page_per: t, tab_return: a } }).done(function (t) {
        $("." + a).append(t);
    });
}
$(document).on("click", ".paging-sm a", function (a) {
    a.preventDefault();
    var t = $(this),
        e = t.attr("data-danhmuc"),
        n = t.attr("data-list"),
        p = t.attr("data-per"),
        d = t.attr("data-table"),
        i = t.attr("data-type"),
        l = t.attr("data-where"),
        c = t.attr("data-tab"),
        r = t.attr("data-page");
    $.ajax({ url: "ajax/paging.php", type: "post", dataType: "html", data: {slug_lang: slug_lang, id_danhmuc: e, page_per: p, table_select: d, type_select: i, where_select: l, tab_return: c, page: r, id_list: n } }).done(function (a) {
        $("." + c).html(a);
    });
});
$(document).on("click", ".btn_viewmore a", function (a) {
    a.preventDefault();
    $(this).parent('.btn_viewmore').remove();
    var t = $(this),
        e = t.attr("data-danhmuc"),
        n = t.attr("data-list"),
        p = t.attr("data-per"),
        d = t.attr("data-table"),
        i = t.attr("data-type"),
        l = t.attr("data-where"),
        c = t.attr("data-tab"),
        r = t.attr("data-page");
    $.ajax({ url: "ajax/paging.php", type: "post", dataType: "html", data: {viewmore: 1, slug_lang: slug_lang, id_danhmuc: e, page_per: p, table_select: d, type_select: i, where_select: l, tab_return: c, page: r, id_list: n } }).done(function (a) {
        $("." + c).append(a);
    });
});