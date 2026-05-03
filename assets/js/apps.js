/* Validation form */
ValidationFormSelf("validation-newsletter");
ValidationFormSelf("validation-cart");
ValidationFormSelf("validation-user");
ValidationFormSelf("validation-contact");
/* Exists */
$.fn.exists = function(){
    return this.length;
};
function check_rating() {
    var danhgia = $('#danhgia').val();
    var ten = $('#ten').val();
    var dienthoai = $('#dienthoai').val();
    var noidung = $('#noidung').val();
    if(danhgia == 0) {
        alert('Bạn chưa đánh giá bài viết này !');
        event.preventDefault();
        return false;
    }
    if(ten == '') {
        alert('Vui lòng nhập họ tên đầy đủ !');
        event.preventDefault();
        return false;
    }
    if(dienthoai == '') {
        alert('Vui lòng nhập số điện thoại !');
        event.preventDefault();
        return false;
    }
    if(noidung == '') {
        alert('Vui lòng nhập lời nhắn !');
        event.preventDefault();
        return false;
    }
}
/* Paging ajax */
if($(".paging-product").exists())
{
    loadPagingAjax("ajax/ajax_product.php?perpage=8",'.paging-product');
}
/* Paging category ajax */
if($(".paging-product-category").exists())
{
    $(".paging-product-category").each(function(){
        var list = $(this).data("list");
        loadPagingAjax("ajax/ajax_product.php?perpage=8&idList="+list,'.paging-product-category-'+list);
    })
}
NN_FRAMEWORK.Filter = function(){
    function filterProduct() {
        var link = '?filter_active=1';
        if($('#filter_sort_choose li a.checked').data('id')!=undefined) {
            link = link + '&filter_sort_choose=' + $('#filter_sort_choose li a.checked').data('id');
        }
        if($('#filter_os_choose li a.checked').data('id')!=undefined) {
            link = link + '&filter_os_choose=' + $('#filter_os_choose li a.checked').data('id');
        }
        if($('#filter_size_choose li a.checked').data('id')!=undefined) {
            link = link + '&filter_size_choose=' + $('#filter_size_choose li a.checked').data('id');
        }
        if($('#filter_color_choose li a.checked').data('id')!=undefined) {
            link = link + '&filter_color_choose=' + $('#filter_color_choose li a.checked').data('id');
        }
        var current_link = window.location.href.split("?");
        window.location.href = current_link[0] + link;
    }
    $(document).on('click', '.filter_block ul li a', function(event) {
        event.preventDefault();
        $(this).parents('ul').find('a').removeClass('checked');
        $(this).addClass('checked');
        filterProduct();
        return false;
    });
};
NN_FRAMEWORK.AutocompleteSeach = function(){
    $(document).on('keyup', '#keyword-autocomplete', function(event) {
        event.preventDefault();
        if($(this).val().length > 0) {
            $.ajax({
                url: 'ajax/autocomplete.php',
                type: 'post',
                data: {keyword: $(this).val()},
            })
            .done(function(rs) {
                $('.keyword-autocomplete').html(rs);
                $('.keyword-autocomplete').show();
            });
        }
        else {
            $('.keyword-autocomplete').hide();
        }
    });
};
/* Back to top */
NN_FRAMEWORK.BackToTop = function(){
    $(window).scroll(function(){
        if(!$('.scrollToTop').length) $("body").append('<div class="scrollToTop"><img src="'+GOTOP+'" alt="Go Top"/></div>');
        if($(this).scrollTop() > 100) $('.scrollToTop').fadeIn();
        else $('.scrollToTop').fadeOut();
    });
    $('body').on("click",".scrollToTop",function() {
        $('html, body').animate({scrollTop : 0},800);
        return false; 
    });
    $('body').on("click",".copyright__top-btn-icon",function() {
        $('html, body').animate({scrollTop : 0},800);
        return false; 
    });
};
/* Alt images */
NN_FRAMEWORK.AltImages = function(){
    $('img').each(function(index, element) {
        if(!$(this).attr('alt') || $(this).attr('alt')=='')
        {
            $(this).attr('alt',WEBSITE_NAME);
        }
    });
};
/* Fix menu */
NN_FRAMEWORK.FixMenu = function(){
    $(window).scroll(function(){
        if($(window).scrollTop() >= $(".header").height()) {
            $(".menu_desktop").addClass('fix-nav');
            $(".menu-res").addClass('fix-nav');
        }
        else {
            $(".menu_desktop").removeClass('fix-nav');
            $(".menu-res").removeClass('fix-nav');
        }
    });
};
/* Tools */
NN_FRAMEWORK.Tools = function(){
    if($(".toolbar").exists())
    {
        $(".footer").css({marginBottom:$(".toolbar").innerHeight()});
    };
    // $(document).on('click', '.js-openMenuTabs a', function() {
    //   $(this).parents('.block-title').toggleClass('open');
    // });
    // $('.hoverhori').hover(function() {
    //   var vitri = $(this).position().top;
    //   $('.hoverhori> ul').css({
    //     'top': vitri + 'px'
    //   })
    // });
    // $( ".gioithieu__body .nav-link" ).click(function( event ) {
    //   $('.gioithieu__body .nav-link').removeClass("active");
    //   $(this).addClass("active");
    //   var ac_id = $(this).attr("href");
    //   $('.gioithieu--bg .tab-pane').removeClass("active");
    //   $('.gioithieu--bg .tab-pane'+ac_id).addClass("active");
    // });
    $( "a.scrollLink" ).click(function( event ) {
      event.preventDefault();
      $("html, body").animate({ scrollTop: $($(this).attr("href")).offset().top - 100 }, 500);
    });
};
NN_FRAMEWORK.Rating = function(){
    if($("#star1").exists())
    {
        $('#star1').starrr({
          change: function(e, value){
            if (value) {
              $('.your-choice-was').show();
              $('.choice').text(value);
            } else {
              $('.your-choice-was').hide();
            }
          }
        });
    }
};
/* Popup */
NN_FRAMEWORK.Popup = function(){
    if($("#popup").exists())
    {
        $('#popup').modal('show');
    }
};
/* Wow */
NN_FRAMEWORK.WowAnimation = function(){
    new WOW().init();
};
/* Mmenu */
NN_FRAMEWORK.Mmenu = function(){
    if($("nav#menu").exists())
    {
        $('nav#menu').mmenu();
    }
};
/* Toc */
NN_FRAMEWORK.Toc = function(){
    if($(".toc-list").exists())
    {
        $(".toc-list").toc({
            content: "div#toc-content",
            headings: "h2,h3,h4"
        });
        if(!$(".toc-list li").length) $(".meta-toc").hide();
        $('.toc-list').find('a').click(function(){
            var x = $(this).attr('data-rel');
            goToByScroll(x);
        });
    }
};
/* Simply scroll */
NN_FRAMEWORK.SimplyScroll = function(){
    if($(".newshome-scroll ul").exists())
    {
        $(".newshome-scroll ul").simplyScroll({
            customClass: 'vert',
            orientation: 'vertical',
            // orientation: 'horizontal',
            auto: true,
            manualMode: 'auto',
            pauseOnHover: 1,
            speed: 1,
            loop: 0
        });
    }
};
/* Tabs */
NN_FRAMEWORK.Tabs = function(){
    if($(".ul-tabs-pro-detail").exists())
    {
        $(".ul-tabs-pro-detail li").click(function(){
            var tabs = $(this).data("tabs");
            $(".content-tabs-pro-detail, .ul-tabs-pro-detail li").removeClass("active");
            $(this).addClass("active");
            $("."+tabs).addClass("active");
        });
    }
};
/* Photobox */
NN_FRAMEWORK.Photobox = function(){
    if($(".album-gallery").exists())
    {
        $('.album-gallery').photobox('a',{thumbs:true,loop:false});
    }
};
/* Datetime picker */
NN_FRAMEWORK.DatetimePicker = function(){
    if($('#ngaysinh').exists())
    {
        $('#ngaysinh').datetimepicker({
            timepicker: false,
            format: 'd/m/Y',
            formatDate: 'd/m/Y',
            minDate: '01/01/1950',
            maxDate: TIMENOW
        });
    }
};
/* Search */
NN_FRAMEWORK.Search = function(){
    if($(".icon-search").exists())
    {
        $(".icon-search").click(function(){
            if($(this).hasClass('active'))
            {
                $(this).removeClass('active');
                $(".search-grid").stop(true,true).animate({opacity: "0",width: "0px"}, 200);   
            }
            else
            {
                $(this).addClass('active');                            
                $(".search-grid").stop(true,true).animate({opacity: "1",width: "230px"}, 200);
            }
            document.getElementById($(this).next().find("input").attr('id')).focus();
            $('.icon-search i').toggleClass('fa fa-search fa fa-times');
        });
    }
};
/* Videos */
NN_FRAMEWORK.Videos = function(){
    /* Fancybox */
    $('[data-fancybox="something"]').fancybox({
        // transitionEffect: "fade",
        // transitionEffect: "slide",
        // transitionEffect: "circular",
        // transitionEffect: "tube",
        // transitionEffect: "zoom-in-out",
        // transitionEffect: "rotate",
        transitionEffect: "fade",
        transitionDuration: 800,
        animationEffect: "fade",
        animationDuration: 800,
        slideShow: {
            autoStart: true,
            speed: 3000
        },
        arrows: true,
        infobar: false,
        toolbar: false,
        hash: false
    });
    if($(".video").exists())
    {
        $('[data-fancybox="video"]').fancybox({
            transitionEffect: "fade",
            transitionDuration: 800,
            animationEffect: "fade",
            animationDuration: 800,
            arrows: true,
            infobar: false,
            toolbar: true,
            hash: false
        });
    }
};
/* Slick */
NN_FRAMEWORK.SlickPage = function(){
    if($(".cnvdofl ul").exists())
    {
        $('.cnvdofl ul').slick({
            lazyLoad: 'ondemand',
            infinite: true,
            accessibility:false,
            slidesToShow: 2,
            slidesToScroll: 1,
            rows:2,
            autoplay: true,
            autoplaySpeed:3000,
            speed:1000,
            arrows:false,
            centerMode:false,
            dots:false,
            draggable:false,
            responsive: [{
                breakpoint: 1000,
                settings: {
                    slidesToShow: 1
                }
            },{
                breakpoint: 500,
                settings: {
                    slidesToShow: 1
                }
            }]
        });
    };
    if($(".dmnb-slick").exists())
    {
      $('.dmnb-slick').slick({
        lazyLoad: 'ondemand',
        infinite: true,
        accessibility: false,
        slidesToShow: 2,
        slidesToScroll: 1,
        autoplay: JS_AUTOPLAY,
        autoplaySpeed: 3000,
        speed: 1000,
        arrows: true,
        centerMode: false,
        dots: false,
        draggable: true,
        // responsive: [{
        //     breakpoint: 850,
        //     settings: {
        //         slidesToShow: 3
        //     }
        // },{
        //     breakpoint: 500,
        //     settings: {
        //         slidesToShow: 2
        //     }
        // }]
      });
    };
    $('.video-for').slick({
      slidesToShow: 1,
      slidesToScroll: 1,
      arrows: false,
      fade: true,
      asNavFor: '.video-nav'
    });
    $('.video-nav').slick({
      slidesToShow: 1,
      slidesToScroll: 1,
      asNavFor: '.video-for',
      dots: false,
      centerMode: true,
      focusOnSelect: true,
      centerPadding: '23%'
    });
    if($(".spnoibat-main").exists())
    {
      $('.spnoibat-main').slick({
        lazyLoad: 'ondemand',
        infinite: true,
        accessibility: false,
        slidesToShow: 4,
        slidesToScroll: 1,
        autoplay: JS_AUTOPLAY,
        autoplaySpeed: 3000,
        speed: 1000,
        arrows: true,
        centerMode: false,
        dots: false,
        draggable: true,
        responsive: [{
            breakpoint: 850,
            settings: {
                slidesToShow: 2
            }
        },{
            breakpoint: 500,
            settings: {
                slidesToShow: 2
            }
        }]
      });
    };
    if($(".slider-main").exists())
    {
        $('.slider-main').slick({
            lazyLoad: 'ondemand',
            infinite: true,
            accessibility:false,
            slidesToShow: 1,
            slidesToScroll: 1,
            autoplay: JS_AUTOPLAY,
            autoplaySpeed:3000,
            speed:1000,
            arrows:true,
            centerMode:false,
            dots:false,
            draggable:true,
        });
    };
    if($(".tieuchi-slick").exists())
    {
        $('.tieuchi-slick').slick({
          lazyLoad: 'ondemand',
          infinite: true,
          accessibility: false,
          slidesToShow: 4,
          slidesToScroll: 1,
          autoplay: JS_AUTOPLAY,
          autoplaySpeed: 3000,
          speed: 1000,
          arrows: true,
          centerMode: false,
          dots: false,
          draggable: true,
          responsive: [{
              breakpoint: 850,
              settings: {
                  slidesToShow: 2
              }
          },{
              breakpoint: 500,
              settings: {
                  slidesToShow: 1
              }
          }]
      });
    };
    if($(".ykien-slick").exists())
    {
        $('.ykien-slick').slick({
          lazyLoad: 'ondemand',
          infinite: true,
          accessibility: false,
          slidesToShow: 3,
          slidesToScroll: 1,
          autoplay: JS_AUTOPLAY,
          autoplaySpeed: 3000,
          speed: 1000,
          arrows: true,
          centerMode: false,
          dots: false,
          draggable: true,
          responsive: [{
              breakpoint: 850,
              settings: {
                  slidesToShow: 2
              }
          },{
              breakpoint: 500,
              settings: {
                  slidesToShow: 1
              }
          }]
      });
      };
      if($(".tinnb-slick").exists())
      {
        $('.tinnb-slick').slick({
          lazyLoad: 'ondemand',
          infinite: true,
          accessibility: false,
          slidesToShow: 3,
          slidesToScroll: 1,
          autoplay: JS_AUTOPLAY,
          autoplaySpeed: 3000,
          speed: 1000,
          arrows: true,
          centerMode: false,
          dots: false,
          draggable: true,
          responsive: [{
              breakpoint: 850,
              settings: {
                  slidesToShow: 2
              }
          },{
              breakpoint: 500,
              settings: {
                  slidesToShow: 1
              }
          }]
        });
      };
    }
/* Owl */
NN_FRAMEWORK.OwlPage = function(){
    if($(".spstl .owl-carousel").exists())
    {
        $('.spstl .owl-carousel').owlCarousel({
            items: 4,
            rewind: true,
            autoplay: true,
            loop: false,
            lazyLoad: true,
            mouseDrag: true,
            touchDrag: true,
            margin: 60,
            smartSpeed: 250,
            autoplaySpeed: 1000,
            nav: true,
            dots: false,
            responsiveClass:true,
            responsiveRefreshRate: 200,
            responsive:{
                0:{
                    items:2, margin: 15
                },
                600:{
                    items:2, margin: 15
                },
                1000:{
                    items:4, margin: 60
                }
            }
        });
    }
    if($(".dvlg ul").exists())
    {
        $('.dvlg ul').owlCarousel({
            items: 4,
            rewind: true,
            autoplay: true,
            loop: false,
            lazyLoad: true,
            mouseDrag: true,
            touchDrag: true,
            margin: 0,
            smartSpeed: 250,
            autoplaySpeed: 1000,
            nav: false,
            dots: false,
            responsiveClass:true,
            responsiveRefreshRate: 200,
            responsive:{
                0:{
                    items:1, margin: 0
                },
                600:{
                    items:2, margin: 0
                },
                1000:{
                    items:4, margin: 0
                }
            }
        });
    }
    if($(".bg ul").exists())
    {
        $('.bg ul').owlCarousel({
            items: 3,
            rewind: true,
            autoplay: true,
            loop: false,
            lazyLoad: true,
            mouseDrag: true,
            touchDrag: true,
            margin: 32,
            smartSpeed: 250,
            autoplaySpeed: 1000,
            nav: false,
            dots: false,
            responsiveClass:true,
            responsiveRefreshRate: 200,
            responsive:{
                0:{
                    items:1, margin: 0
                },
                600:{
                    items:2, margin: 15
                },
                1000:{
                    items:3, margin: 32
                }
            }
        });
    }
    if($(".tinnb_owl").exists())
    {
        $('.tinnb_owl').owlCarousel({
            items: 3,
            rewind: false,
            autoplay: true,
            loop: true,
            lazyLoad: true,
            mouseDrag: true,
            touchDrag: true,
            margin: 15,
            smartSpeed: 250,
            autoplaySpeed: 1000,
            nav: false,
            dots: false,
            responsiveClass:true,
            responsiveRefreshRate: 200,
            responsive:{
                0:{
                    items:1
                },
                600:{
                    items:2
                },
                1000:{
                    items:3
                }
            }
        });
    }
    if($(".doitac_owl").exists())
    {
        $('.doitac_owl').owlCarousel({
            items: 6,
            rewind: false,
            autoplay: true,
            loop: true,
            lazyLoad: true,
            mouseDrag: true,
            touchDrag: true,
            margin: 15,
            smartSpeed: 250,
            autoplaySpeed: 1000,
            nav: false,
            dots: false,
            responsiveClass:true,
            responsiveRefreshRate: 200,
            responsive:{
                0:{
                    items:2
                },
                600:{
                    items:3
                },
                1000:{
                    items:6
                }
            }
        });
    }
    // if($(".owl-slideshow").exists())
    // {
    //     $('.owl-slideshow').owlCarousel({
    //         items: 1,
    //         rewind: true,
    //         autoplay: true,
    //         loop: false,
    //         lazyLoad: false,
    //         mouseDrag: false,
    //         touchDrag: false,
    //         margin: 0,
    //         smartSpeed: 500,
    //         autoplaySpeed: 3500,
    //         nav: false,
    //         dots: false
    //     });
    //     $('.prev-slideshow').click(function() {
    //         $('.owl-slideshow').trigger('prev.owl.carousel');
    //     });
    //     $('.next-slideshow').click(function() {
    //         $('.owl-slideshow').trigger('next.owl.carousel');
    //     });
    // }
    if($(".owl-brand").exists())
    {
        $('.owl-brand').owlCarousel({
            items: 7,
            rewind: true,
            autoplay: true,
            loop: false,
            lazyLoad: false,
            mouseDrag: true,
            touchDrag: true,
            margin: 10,
            smartSpeed: 250,
            autoplaySpeed: 1000,
            nav: false,
            dots: false,
            responsiveClass:true,
            responsiveRefreshRate: 200,
            responsive: {
                0: {
                    items: 7,
                    margin: 10
                }
            }
        });
        $('.prev-brand').click(function() {
            $('.owl-brand').trigger('prev.owl.carousel');
        });
        $('.next-brand').click(function() {
            $('.owl-brand').trigger('next.owl.carousel');
        });
    }
    if($(".owl-partner").exists())
    {
        $('.owl-partner').owlCarousel({
            items: 7,
            rewind: true,
            autoplay: true,
            loop: false,
            lazyLoad: false,
            mouseDrag: true,
            touchDrag: true,
            margin: 10,
            smartSpeed: 250,
            autoplaySpeed: 1000,
            nav: false,
            dots: false,
            responsiveClass:true,
            responsiveRefreshRate: 200,
            responsive: {
                0: {
                    items: 7,
                    margin: 10
                }
            }
        });
        $('.prev-partner').click(function() {
            $('.owl-partner').trigger('prev.owl.carousel');
        });
        $('.next-partner').click(function() {
            $('.owl-partner').trigger('next.owl.carousel');
        });
    }
};
/* Owl pro detail */
NN_FRAMEWORK.OwlProDetail = function(){
    if($(".owl-thumb-pro").exists())
    {
        $('.owl-thumb-pro').owlCarousel({
            items: 4,
            lazyLoad: false,
            mouseDrag: true,
            touchDrag: true,
            margin: 10,
            smartSpeed: 250,
            nav: false,
            dots: false
        });
        $('.prev-thumb-pro').click(function() {
            $('.owl-thumb-pro').trigger('prev.owl.carousel');
        });
        $('.next-thumb-pro').click(function() {
            $('.owl-thumb-pro').trigger('next.owl.carousel');
        });
    }
};
/* Cart */
NN_FRAMEWORK.Cart = function(){
    $("body").on("click",".addcart",function(){
        var mau = ($(".color-pro-detail input:checked").val()) ? $(".color-pro-detail input:checked").val() : 0;
        var size = ($(".size-pro-detail input:checked").val()) ? $(".size-pro-detail input:checked").val() : 0;
        var id = $(this).data("id");
        var action = $(this).data("action");
        var quantity = ($(".qty-pro").val()) ? $(".qty-pro").val() : 1;
        if(id)
        {
            $.ajax({
                url:'ajax/ajax_cart.php',
                type: "POST",
                dataType: 'json',
                async: false,
                data: {cmd:'add-cart',id:id,mau:mau,size:size,quantity:quantity},
                success: function(result){
                    if(action=='addnow')
                    {
                        $('.count-cart').html(result.max);
                        $.ajax({
                            url:'ajax/ajax_cart.php',
                            type: "POST",
                            dataType: 'html',
                            async: false,
                            data: {cmd:'popup-cart'},
                            success: function(result){
                                $("#popup-cart .modal-body").html(result);
                                $('#popup-cart').modal('show');
                            }
                        });
                    }
                    else if(action=='buynow')
                    {
                        window.location = CONFIG_BASE + "gio-hang";
                    }
                }
            });
        }
    });
    $("body").on("click",".del-procart",function(){
        if(confirm(LANG['delete_product_from_cart']))
        {
            var code = $(this).data("code");
            var ship = $(".price-ship").val();
            $.ajax({
                type: "POST",
                url:'ajax/ajax_cart.php',
                dataType: 'json',
                data: {cmd:'delete-cart',code:code,ship:ship},
                success: function(result){
                    $('.count-cart').html(result.max);
                    if(result.max)
                    {
                        $('.price-temp').val(result.temp);
                        $('.load-price-temp').html(result.tempText);
                        $('.price-total').val(result.total);
                        $('.load-price-total').html(result.totalText);
                        $(".procart-"+code).remove();
                    }
                    else
                    {
                        $(".wrap-cart").html('<a href="" class="empty-cart text-decoration-none"><i class="fa fa-cart-arrow-down"></i><p>'+LANG['no_products_in_cart']+'</p><span>'+LANG['back_to_home']+'</span></a>');
                    }
                }
            });
        }
    });
    $("body").on("click",".counter-procart",function(){
        var $button = $(this);
        var input = $button.parent().find("input");
        var id = input.data('pid');
        var code = input.data('code');
        var oldValue = $button.parent().find("input").val();
        if($button.text() == "+") quantity = parseFloat(oldValue) + 1;
        else if(oldValue > 1) quantity = parseFloat(oldValue) - 1;
        $button.parent().find("input").val(quantity);
        update_cart(id,code,quantity);
    });
    $("body").on("change","input.quantity-procat",function(){
        var quantity = $(this).val();
        var id = $(this).data("pid");
        var code = $(this).data("code");
        update_cart(id,code,quantity);
    });
    if($(".select-city-cart").exists())
    {
        $(".select-city-cart").change(function(){
            var id = $(this).val();
            load_district(id);
            load_ship();
        });
    }
    if($(".select-district-cart").exists())
    {
        $(".select-district-cart").change(function(){
            var id = $(this).val();
            load_wards(id);
            load_ship();
        });
    }
    if($(".select-wards-cart").exists())
    {
        $(".select-wards-cart").change(function(){
            var id = $(this).val();
            load_ship(id);
        });
    }
    if($(".payments-label").exists())
    {
        $(".payments-label").click(function(){
            var payments = $(this).data("payments");
            $(".payments-cart .payments-label, .payments-info").removeClass("active");
            $(this).addClass("active");
            $(".payments-info-"+payments).addClass("active");
        });
    }
    if($(".color-pro-detail").exists())
    {
        $(".color-pro-detail").click(function(){
            $(".color-pro-detail").removeClass("active");
            $(this).addClass("active");
            var id_mau=$("input[name=color-pro-detail]:checked").val();
            var idpro=$(this).data('idpro');
            $.ajax({
                url:'ajax/ajax_color.php',
                type: "POST",
                dataType: 'html',
                data: {id_mau:id_mau,idpro:idpro},
                success: function(result){
                    if(result!='')
                    {
                        $('.left-pro-detail').html(result);
                        MagicZoom.refresh("Zoom-1");
                        NN_FRAMEWORK.OwlProDetail();
                    }
                }
            });
        });
    }
    if($(".size-pro-detail").exists())
    {
        $(".size-pro-detail").click(function(){
            $(".size-pro-detail").removeClass("active");
            $(this).addClass("active");
        });
    }
    if($(".quantity-pro-detail span").exists())
    {
        $(".quantity-pro-detail span").click(function(){
            var $button = $(this);
            var oldValue = $button.parent().find("input").val();
            if($button.text() == "+")
            {
                var newVal = parseFloat(oldValue) + 1;
            }
            else
            {
                if(oldValue > 1) var newVal = parseFloat(oldValue) - 1;
                else var newVal = 1;
            }
            $button.parent().find("input").val(newVal);
        });
    }
};
/* Ready */
$(document).ready(function(){
    // NN_FRAMEWORK.Rating();
    // NN_FRAMEWORK.Filter();
    // NN_FRAMEWORK.AutocompleteSeach();
    NN_FRAMEWORK.Tools();
    NN_FRAMEWORK.Popup();
    NN_FRAMEWORK.WowAnimation();
    NN_FRAMEWORK.AltImages();
    NN_FRAMEWORK.BackToTop();
    NN_FRAMEWORK.FixMenu();
    NN_FRAMEWORK.Mmenu();
    NN_FRAMEWORK.OwlPage();
    NN_FRAMEWORK.OwlProDetail();
    // NN_FRAMEWORK.Toc();
    NN_FRAMEWORK.Cart();
    // NN_FRAMEWORK.SimplyScroll();
    NN_FRAMEWORK.Tabs();
    NN_FRAMEWORK.Videos();
    NN_FRAMEWORK.Photobox();
    NN_FRAMEWORK.Search();
    // NN_FRAMEWORK.DatetimePicker();
    NN_FRAMEWORK.SlickPage();
});