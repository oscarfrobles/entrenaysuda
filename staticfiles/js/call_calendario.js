jQuery(function ($){
$(document).ready(function(){
 url = 'calendario/'
 $.ajax({
            url: url,
            type: 'get',
            dataType: 'html',
            async: false,
            success: function(data) {
                $('.calendario').html(unescape(data.toString()));
            }
         });

});
});