$(document).ready(function() {

    $('[data-toggle="tooltip"]').tooltip();

    $('.btn-completado').change(function(){
        data = $(this).val();
        url = window.location.href;
        csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
        $.ajax({
                url: url,
                type: 'POST',
                data: {
                        'tipo': 'completado',
                        'data': data,
                        'csrfmiddlewaretoken': csrf_token,
                },
                success: function(response){
                    if(response == 'True'){
                       $('.label_actualizado').show(2000);
                       $('.label_actualizado').hide(1000);
                    }
                }

     });
    });

    $('.comentario').bind('keypress',function(evt){
        if(evt.which == 13){
        label_actualizado = 0;
        data = $(this).val();
        url = window.location.href;
        csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
        $.ajax({
                url: url,
                type: 'POST',
                data: {
                        'tipo': 'comentario',
                        'data': data,
                        'csrfmiddlewaretoken': csrf_token,
                },
                success: function(response){
                    if(response == 'True' && label_actualizado == 0){
                       $('.label_actualizado').show(2000);
                       $('.label_actualizado').hide(1000);
                       label_actualizado = 1;
                    }
                }

     });
     }
    });

});