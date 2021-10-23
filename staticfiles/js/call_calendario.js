
$(document).ready(function(){
 url = '/calendario/'
 $.ajax({
            url: url,
            type: 'get',
            dataType: 'html',
            async: false,
            success: function(data) {
                $('.calendario').html("<iframe seamless src='"+url+"'><"+"/iframe>");
            }
         }).fail( function(jqXHR, textStatus, errorThrown) {
                console.log( jqXHR.status + " " + JSON.stringify(jqXHR.responseText) );
                $('.calendario').html("<iframe seamless  src='" + url + "'><"+"/iframe>");
            });



});
