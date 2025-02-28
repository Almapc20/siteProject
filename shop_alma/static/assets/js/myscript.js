$(document).ready(
    function(){
        var urlparser = new URLSearchParams(window.location.search);
        if (urlparser == ""){
            localStorage.clear();
            $("#filter_state").css("display", "none");
        } else {
            $("#filter_state").css("display", "inline-block");
        }
        $('input:checkbox').on('click', function(){
            var fav, favs= [];
            $('input:checkbox').each(function() {
                fav= { id: $(this).attr('id'), value:$(this).prop('checked')};
                favs.push(fav);
            })
            localStorage.setItem('favorites', JSON.stringify(favs));
        })
        var favorites= JSON.parse(localStorage.getItem('favorites'));
        for(var i=0; i<favorites.length; i++){
            $('#'+ favorites[i].id).prop('checked', favorites[i].value);
        }
    }

);


function showVal(x) {
    x= x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    document.getElementById('sel_price').innerText = x;
};


// تابع حذف پارامترهای خط آدرس
function removeURLParameter(url, parametr) {
    var urlparts= url.split('?');
    if (urlparts.length >= 2) {
        var prefix = encodeURIComponent(parametr) + "=" ;
        var pars= urlparts[1].split(/[&;]/g);
        for (var i = pars.length; i-- > 0;) {
            if (pars[i].lastIndexOf(prefix, 0) != -1) {
                pars.splice(i, 1);
            }
        }
        return urlparts[0] + (pars.length > 0 ? '?' + pars.join('&') : '');
    }
    return url
}

// تابع انتخاب مدل مرتب سازی محصولات
function select_sort() {
    var select_sort_value= $("#select_sort").val();
    // $("#select_sort").attr('selected', 'selected');
    var url = removeURLParameter(window.location.href, "sort_type");
    window.location = url + "&sort_type=" + select_sort_value;
}

// shop cart --------------------------------------------------

function status_of_shop_cart(){
    $.ajax({
        type: "GET",
        url: "/orders/status_of_shop_cart/",
        success: function(res){
            $("#indicator__value").text(res);
        }
    });   
}

status_of_shop_cart()

function aad_to_shop_cart(product_id,qty){
    if (qty === 0 ){
        qty=$("#product-quantity").val();
    }
    $.ajax({
        type: "GET",
        url: "/orders/add_to_shop_cart/",
        data:{
            product_id:product_id,
            qty:qty,
        },
        success: function(res){
            alert("کالای مورد نظر به سبد شما اضافه شد");
            $("#indicator__value").text(res);
            status_of_shop_cart()
        }
    });
}


function delete_from_shop_cart(product_id) {
    $.ajax({
        type: "GET",
        url: "/orders/delete_from_shop_cart/",
        data: {
            product_id:product_id,
        },
        success: function(res) {
            alert("کالای مورد نظر از سبد شما حذف شد");
            $("#shop_cart_list").html(res)
            status_of_shop_cart()
        }
    });
}

function update_shop_cart() {
    var product_id_list=[]
    var qty_list=[]
    $("input[id^='qty_'").each(function(index) {
        product_id_list.push($(this).attr('id').slice(4));
        qty_list.push($(this).val());
    });
    console.log(product_id_list);
    console.log(qty_list)
    $.ajax({
        type:"GET",
        url:"/orders/update_shop_cart/",
        data:{
            product_id_list:product_id_list,
            qty_list:qty_list
        },
        success:function (res) {
            alert("ssss");
            $("#shop_cart_list").html(res);
            status_of_shop_cart();
        }
    });
}


// ================ carosel  ========================= 
$('.owl-carousel').owlCarousel({
    rtl:true,
    loop:true,
    margin:10,
    nav:true,
    responsive:{
        0:{
            items:1
        },
        600:{
            items:3
        },
        1000:{
            items:5
        }
    }
  })

// -----------------------------------------------------------------------------------

function showCreateCommentForm(productId, commentId, slug) {
    $.ajax({
        type : "GET",
        url : "/csf/create_comment/" + slug,
        data : {
            productId : productId,
            commentId : commentId,
        },
        success : function(res) {
            $("#btn_"+ commentId).hide();
            $("#comment_form_"+ commentId).html(res);
        }
    });
}

// -----------------------------------------------------------------------------------------------------

function addScore(score, productId) {
    var starRatings = document.querySelectorAll(".fa-star");

    starRatings.forEach(element => {        
    element.classList.remove("checked");     

    });
    for (let i = 1; i <= score; i++) {     
        const element = document.getElementById("star_" + i); 
        element.classList.add("checked");
    }

    $.ajax({
        type : "GET",
        url : "/csf/add_score/",
        data : {
            productId : productId,
            score : score
        },
        success : function(res) {
            alert(res);
        }
    });
    starRatings.forEach(element => {
        element.classList.add("disable");
    });
}
// -----------------------------------------------------------------------------------------------

function addToFavorites(productId) {
    $.ajax({
        type :"GET",
        url : "/csf/add_to_favorite/",
        data : {
            productId : productId,
        },
        success : function(res) { 
            alert(res);
            location.reload();
        }
    });
}

// -------------------------------------------------------------------------------------
document.addEventListener("DOMContentLoaded", function() {
    var searchButton = document.querySelector(".indicator--trigger--click .indicator__button");
    var searchDropdown = document.querySelector(".indicator__dropdown");

    // نمایش و مخفی کردن فرم جستجو با کلیک روی دکمه جستجو
    searchButton.addEventListener("click", function(event) {
        event.stopPropagation();
        searchDropdown.classList.toggle("active");
    });

    // جلوگیری از بسته شدن فرم جستجو هنگام کلیک داخل فرم
    searchDropdown.addEventListener("click", function(event) {
        event.stopPropagation();
    });

    // بستن فرم جستجو وقتی کاربر بیرون از آن کلیک می‌کند
    document.addEventListener("click", function() {
        searchDropdown.classList.remove("active");
    });
});

// --------------------------------------------------------------------------

status_of_compare_list();

//====================status_of_compare_list===============================================
function status_of_compare_list() {
    $.ajax({
        type: "GET",
        url: "/products/status_of_compare_list/",
        success: function(res) { 
            if (Number(res) === 0) {
                $("#compare_count_icon").hide();
            } else {
                $("#compare_count_icon").show();
                $("#compare_count").text(res);
            }
        }
    });
}


//====================addCompare===============================================

function addToCompareList(productId, productGroupId) {
    $.ajax({
        type: "GET",
        url: "/products/add_to_compare_list/",
        data: {
            productId: productId,
            productGroupId: productGroupId
        },
        success: function(res) {
            alert(res); // نمایش پیغام موفقیت
            status_of_compare_list(); // به روز رسانی وضعیت لیست مقایسه
        },
        error: function(xhr, status, error) {
            console.error('Error:', error);
            alert('An error occurred: ' + xhr.responseText);
        }
    });
}
//====================DeleteCompare===============================================

function deleteFromCompareList(productId) {
    $.ajax({
        type: "GET",
        url: "/products/delete_form_compare_product/",
        data: {
            productId: productId,
        },
        success: function(res) {
            alert("حذف با موفقیت انجام شد");
            $("#compare_list").html(res);
            status_of_compare_list();
        }
    });
}

// --------------------------------------------------------------------------------------



// script.js

document.addEventListener('DOMContentLoaded', function() {
    const submenuItems = document.querySelectorAll('.nav-links__item--with-submenu');

    submenuItems.forEach(item => {
        item.addEventListener('mouseover', () => {
            item.querySelector('.nav-links__megamenu')?.classList.add('show');
        });
        
        item.addEventListener('mouseout', () => {
            item.querySelector('.nav-links__megamenu')?.classList.remove('show');
        });
    });
});