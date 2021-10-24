jQuery(function ($){

deb = 0;

debug = function(param){
    if (deb==1){
        return console.log(param);
    }
    return false;
}


$(document).ready(function(){

      arr_fechas = [];
      ejercicios = [];
      data = new Array();

      var completado = function(valor){
        switch(valor){
            case 0:
            default:
            comp = "<span class='rojo'>NO REALIZADO</span>";
            break;
            case 1:
            comp = "<span class='naranja'>COMPLETO</span>";
            break;
            case 2:
            comp = "<span class='verde'>SEMICOMPLETO</span>";
            break;
        }
        return comp;
      }

      init = function(){
        data = []
        for(let i =0; i < json_cal.length; i++){
            fecha = json_cal[i]['fecha'];
            if (Array.isArray(data[fecha]) == false){
                data[fecha] = [];
                data[fecha]['ejercicios'] = []
            }
            data[fecha]['comentario'] = json_cal[i]['comentario'];
            data[fecha]['completado'] = json_cal[i]['completado'];
            data[fecha]['series'] = json_cal[i]['series'];

            data[fecha]['ejercicios'].push(json_cal[i]['ejercicios__nombre']);
            debug(data[fecha]['ejercicios']);
            if(json_cal[i]['completado'] == 0)
                 data[fecha]['class_bg'] = 'rojo';
            if(json_cal[i]['completado'] == 1)
                data[fecha]['class_bg'] = 'naranja';
            if(json_cal[i]['completado'] == 2)
                data[fecha]['class_bg'] = 'verde';
        }
    }

        init();


      pickmeup.defaults.locales['es'] = {
  	  days: ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'],
  	  daysShort: ['Dom', 'Lun', 'Mar', 'Mie', 'Jue', 'Vie', 'Sáb'],
  	  daysMin: ['Do', 'Lu', 'Ma', 'Mi', 'Ju', 'Vi', 'Sa'],
  	  months: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
  	  monthsShort: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    };

    var now = new Date();
    pickmeup('.fecha', {
        format	: 'Y-m-d',
		flat : true,
			date      : [
  			new Date
  		],
  		mode      : 'single',
  		locale: 'es',
  		render: function(date){
  		    var fecha_calendario = date.getFullYear() + "-" + ("0" + (date.getMonth() + 1)).slice(-2) + "-" + ("0" + (date.getDate())).slice(-2);
            ev = eval(data[fecha_calendario]);
            dt = '';
            if(Array.isArray(ev)){
                dt = '__' + ev['class_bg'];
            }
  		    return { class_name: 'data_' + fecha_calendario + dt }
  		},
	})


	$(".fecha").on('pickmeup-change', function (e) {
	   // dt = new Date();
        //debug(e.detail.formatted_date); // New date according to current format
        ej = null;
        cal_data = data[e.detail.formatted_date];
        if(cal_data == undefined){
            return true;
        }

        jQuery.noConflict();
        $("#modalcalendario", window.parent.document).modal();
        if (Array.isArray(cal_data) && cal_data['ejercicios'] != undefined){
            ej = cal_data['ejercicios'];
        }
        if (null != ej && ej.length > 0){
            jQuery.each(ej, function(index, value) {
                 $('<li>').text(value).appendTo($('.ejercicios-txt', window.parent.document));
            });
            //$('.ejercicios-txt', window.parent.document).html(ej.join('<br>'));
        }
        $('.fecha-txt', window.parent.document).html(e.detail.formatted_date);
        $('.completado-txt', window.parent.document).html(completado(cal_data['completado']));
        $('.comentario-txt', window.parent.document).html(cal_data['comentario']);
        $('.series-txt', window.parent.document).html(cal_data['series']);
     });




});
});