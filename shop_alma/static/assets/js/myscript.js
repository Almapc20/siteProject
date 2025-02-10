$(document).ready(
    function(){
        var urlParams = new URLSearchParams(window.location.search);
        if (urlParams == ""){
            localStorage.clear();
            $("#filter_state").css("display", "none");
        } else {
            $("#filter_state").css("display", "inline-block");
        }
        $('input:checkbox').on('click', function(){
            var fav, favs = [];
            $('input:checkbox').each(function(){
                $('input:checkbox').each(function(){
                    fav = { id: $(this).attr('id'), value: $(this).prop('checked')};
                    favs.push(fav);
                })
                localStorage.setItem("favorites", JSON.stringify(favs));
            })
            var favorites = JSON.parse(localStorage.getItem('favorites'));
            for (var i = 0; i < favorites.length; i++){
                $('#' + favorites[i].id).prop('checked' , favorites[i].value);
            }
        })
    }
)




function select_sort() {
    var select_sort_value = $("#select_sort").val();
    $("#select_sort").attr('selected','selected');
    var url = removeURLParameter(window.location.href,"sort_type");
    window.location=url + "&sort_type=" + select_sort_value;
}