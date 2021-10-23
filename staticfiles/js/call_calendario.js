
$(document).ready(function(){
 url = 'calendario/'
// $.ajax({
//            url: url,
//            type: 'get',
//            dataType: 'json',
//            async: false,
//            success: function(data) {
//                $('.calendario').html(data.toString());
//            }
//         }).fail( function(jqXHR, textStatus, errorThrown) {
//                console.log( jqXHR.status + " " + JSON.stringify(jqXHR.responseText) );
//                $('.calendario').html(jqXHR.responseText);
//            });

         $('.calendario').load(url);

});
