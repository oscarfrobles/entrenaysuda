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
            comp = "<span class='verde'>COMPLETO</span>";
            break;
            case 2:
            comp = "<span class='naranja'>SEMICOMPLETO</span>";
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
            data[fecha]['id'] = json_cal[i]['id'];
            data[fecha]['comentario'] = json_cal[i]['comentario'];
            data[fecha]['completado'] = json_cal[i]['completado'];
            data[fecha]['series'] = json_cal[i]['series'];
            if(json_cal[i]['calories'])
                 data[fecha]['calories'] = json_cal[i]['calories'];
            if(json_cal[i]['bpm'])
                 data[fecha]['bpm'] = json_cal[i]['bpm'];
            if(json_cal[i]['distance'])
                 data[fecha]['distance'] = json_cal[i]['distance'];
            if(json_cal[i]['weight'])
                 data[fecha]['weight'] = json_cal[i]['weight'];

            data[fecha]['ejercicios'].push(json_cal[i]['ejercicios__nombre']);
            debug(data[fecha]['ejercicios']);
            if(json_cal[i]['completado'] == 0)
                 data[fecha]['class_bg'] = 'rojo';
            if(json_cal[i]['completado'] == 1)
                data[fecha]['class_bg'] = 'verde';
            if(json_cal[i]['completado'] == 2)
                data[fecha]['class_bg'] = 'naranja';
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
//	   $('.calorias-txt, .bpm-txt, .distance-txt, .weight-txt', window.parent.document).attr("class", "hide");
       $('.calorias-txt, .bpm-txt, .distancia-txt, .peso-txt', window.parent.document).removeClass("show").addClass("hide");
       $('.calorias-txt > span,  .bpm-txt > span, .distancia-txt > span, .peso-txt > span').empty();

        cal_data = data[e.detail.formatted_date];
        debug(cal_data);
        if(cal_data == undefined || Array.isArray(cal_data)== false){
            return true;
        }

        jQuery.noConflict();
        $("#modalcalendario", window.parent.document).modal();

        if (Array.isArray(cal_data['ejercicios']) && cal_data['ejercicios'].length > 0){
            $('.ejercicios-txt > li', window.parent.document).remove();
            jQuery.each(cal_data['ejercicios'], function(index, value) {
                debug(index + " " + value);
                 $('<li>').text(value).appendTo($('.ejercicios-txt', window.parent.document));
            });
            //$('.ejercicios-txt', window.parent.document).html(ej.join('<br>'));
        }
        var hoy = now.getFullYear() + '-' + ("0" + now.getMonth()).slice(-2) + '-' + ("0" + now.getDate()).slice(-2);
        var enlace = (hoy > e.detail.formatted_date) ? '/historico/id/' : '/entrenamientos/';
        $('.fecha-txt', window.parent.document).html(e.detail.formatted_date);
        $('.link-entrenamiento', window.parent.document).attr('href', enlace + cal_data['id']);
        $('.completado-txt', window.parent.document).html(completado(cal_data['completado']));
        $('.comentario-txt', window.parent.document).html(cal_data['comentario']);
        $('.series-txt', window.parent.document).html(cal_data['series']);

        if(undefined != cal_data['calories'] && $.isNumeric(cal_data['calories'])){
            debug("calories: "+ cal_data['calories']);
            $('.calorias-txt > span', window.parent.document).html(cal_data['calories']);
            $('.calorias-txt', window.parent.document).addClass("show").removeClass("hide");

        }
        if(undefined != cal_data['bpm'] && $.isNumeric(cal_data['bpm'])){
            debug("bpm: "+ cal_data['bpm']);
            $('.bpm-txt > span', window.parent.document).html(cal_data['bpm']);
            $('.bpm-txt', window.parent.document).addClass("show").removeClass("hide");
        }
        if(undefined != cal_data['distance'] && $.isNumeric(cal_data['distance'])){
        debug("distance: "+ cal_data['distance']);
            $('.distancia-txt > span', window.parent.document).html(cal_data['distance']);
            $('.distancia-txt', window.parent.document).addClass("show").removeClass("hide");;
        }
        if(undefined != cal_data['weight'] && $.isNumeric(cal_data['weight'])){
        debug("weight: "+ cal_data['weight']);
            $('.peso-txt > span', window.parent.document).html(cal_data['weight']);
            $('.peso-txt', window.parent.document).addClass("show").removeClass("hide");
        }
        if(undefined != cal_data['steps'] && $.isNumeric(cal_data['steps'])){
        debug("steps: "+ cal_data['steps']);
            $('.pasos-txt > span', window.parent.document).html(cal_data['steps']);
            $('.pasos-txt', window.parent.document).addClass("show").removeClass("hide");
        }
     });




});
});