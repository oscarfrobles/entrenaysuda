jQuery(function ($){
    $(document).ready(function() {

        function oauth_connect(){
            url = '/googlefit_ajax_connect/'
            result = null;
            $.ajax({
                url: url,
                type: 'get',
                dataType: 'json',
                async: false,
                success: function(data) {
                    result = data.connect;
                }
             });
            return result;
        }

        function getActivitiesTypes(){
             url = '/googlefit_activities_types';
                result = null;
             $.ajax({
                url: url,
                type: 'get',
                dataType: 'json',
                async: false,
                success: function(resultado){
                    result = resultado;
                }
             });
             return result;
        }



        $('.googlefit-btn').click(function() {
            conexion = oauth_connect();
            if (conexion == 'false'){
                window.location.href= '/oauth/?redirect=' + encodeURIComponent(window.location.pathname);
            }
            activities = getActivitiesTypes();
             url = '/googlefit_ajax/';
             $(".sesiones").remove();
            $.ajax({
                url: url,
                type: 'get',
                dataType: 'json',
                async: false,
                success: function(data) {
                    exclude = ['start','end', 'id_google']
                    $(".general-txt").html(data);
                    $(".googlefit_save-btn").removeClass("d-none");
                    $.each(data.inserts, function(index, value){
                        $(".general-txt").append(index + ': ' + value + "<br>");
                    });
                    //console.log(data);
                    if(data.session.length > 0){
                        $(".general-txt").parent().append("<p><div class='sesiones'></div></p>");
                        $(".sesiones-txt").html('<p class="numSesiones">Existen ' + data.session.length +' sesiones:</p>');
                        $(".sesiones-txt").append("<div class='cont'></div>");
                        $.each(data.session, function(index, value){
                            $(".cont").append("<p><ul class='uls_"+ index+"'></ul</p>");
                            $.each(value, function(i, v){
                                if ( $.inArray(i, exclude) == -1){
                                    v = (i == 'activityType') ? activities[v]: v;
                                    $(".uls_" + index).append("<li>" + i + ": " + v  + "</li>");
                                }
                            });
                        });
                    }
                }
            });
        });


        $(document).on('click','.googlefit_save-btn', function() {
            type = ($(this).attr('id') == 'btn-save-session') ? 'session' : 'data';
            if (type == 'session')
                url = "/googlefit_ajax_save_session/";
            else
                url = "/googlefit_ajax_save_data/";
            $.get(url, function(data){
                if(type == 'data')
                    $(".general-txt").html(data);

                if(data.result == true){
                    if(type == 'data'){
                        txt = 'Se han guardado correctamente los datos';
                        $("#btn-save-data").addClass("d-none");
                    }
                    else{
                        txt = 'Se han guardado correctamente las sesiones';
                        $("#btn-save-session").addClass("d-none");
                    }

                }
                else{
                    txt = 'Ha habido un error';
                }
                if(type == 'data')
                    $(".general-txt").html(txt);
                else
                    $(".sesiones-txt").html(txt);
            });
        });

        function init(){
            conexion = oauth_connect();
            if(conexion== 'false'){
                $(".googlefit-btn").html('Conectar con GOOGLE');
                $(".googlefit-btn").removeAttr('data-toggle');
                $(".googlefit-btn").on("click", function(){
                 console.log(window.location);
                    window.location.href= '/oauth/?redirect=' + encodeURIComponent(window.location.pathname);
                });
            }
            else {
                $(".googlefit-btn").html('Recoger los datos de GOOGLE');
            }
        }
        init();


    });
});
