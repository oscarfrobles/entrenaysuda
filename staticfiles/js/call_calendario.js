jQuery(function ($){
$(document).ready(function(){
 url = 'calendario/'
 $.ajax({
            url: url,
            type: 'get',
            dataType: 'html',
            async: false,
            success: function(data) {
                result = data.connect;
                $('.calendario').html(data);
            }
         });

});
});