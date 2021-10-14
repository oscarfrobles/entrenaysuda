from .models import Medida, Calendario
from django.db.models import Count
from datetime import date
import logging

logger = logging.getLogger(__name__)


def insert_medidas(request):
    exclude_filter = {'csrfmiddlewaretoken', 'uname', 'ajax'}
    if request.user.is_authenticated:
        try:
            filters = {}
            post = request.POST
            for key in post:
                if key not in exclude_filter and len(post[key]) > 0:
                    filters[key] = post[key]
            fecha = date.today()
            year = int(fecha.strftime("%Y"))
            month = fecha.month
            filters['anyo'] = year
            filters['mes'] = month
            filters['user_id'] = request.user.id

            if 'id' not in filters:
                query = Medida.objects.create(**filters)
            else:
                query = Medida.update(**filters)
            return True
        except Exception as e:
            logger.error(e)
            return False


def compara_medidas(**kwargs):
    fecha = date.today()
    year = fecha.strftime("%Y")
    month = fecha.month
    diff = {}
    try:
        medidas_actual = Medida.objects.values().filter(mes=month, anyo=year, user_id=kwargs['user_id'])
        medidas_anterior = Medida.objects.values().filter(mes__lt=month, user_id=kwargs['user_id'])[:1]

        peso_actual = medidas_actual[0]['peso']
        peso_anterior = medidas_anterior[0]['peso']

        imc_actual = medidas_actual[0]['imc']
        imc_anterior = medidas_anterior[0]['imc']

        grasa_actual = medidas_actual[0]['grasa']
        grasa_anterior = medidas_anterior[0]['grasa']

        musculo_actual = medidas_actual[0]['musculo']
        musculo_anterior = medidas_anterior[0]['musculo']

        caliper_actual = medidas_actual[0]['caliper']
        caliper_anterior = medidas_anterior[0]['caliper']

        pecho_actual = medidas_actual[0]['pecho']
        pecho_anterior = medidas_anterior[0]['pecho']

        cintura_actual = medidas_actual[0]['cintura']
        cintura_anterior = medidas_anterior[0]['cintura']

        gemelo_actual = medidas_actual[0]['gemelo']
        gemelo_anterior = medidas_anterior[0]['gemelo']

        biceps_actual = medidas_actual[0]['biceps']
        biceps_anterior = medidas_anterior[0]['biceps']

        muslo_actual = medidas_actual[0]['muslo']
        muslo_anterior = medidas_anterior[0]['muslo']
        

        diff_peso = round(peso_actual - peso_anterior, 2)
        diff_imc = round(imc_actual - imc_anterior, 2)
        diff_grasa = round(grasa_actual - grasa_anterior, 2)
        diff_musculo = round(musculo_actual - musculo_anterior, 2)
        diff_caliper = round(caliper_actual - caliper_anterior, 2)
        diff_muslo = round(muslo_actual - muslo_anterior, 2)
        diff_cintura = round(cintura_actual - cintura_anterior, 2)
        diff_biceps = round(biceps_actual - biceps_anterior, 2)
        diff_gemelo = round(gemelo_actual - gemelo_anterior, 2)
        diff_pecho = round(pecho_actual - pecho_anterior, 2)


        if isinstance(diff_peso, float) and peso_anterior != 0.0 and peso_actual != 0.0:
            diff['peso'] = diff_peso
        if isinstance(diff_imc, float) and imc_anterior != 0.0 and imc_actual != 0.0:
            diff['imc'] = diff_imc
        if isinstance(diff_grasa, float) and grasa_anterior != 0.0 and grasa_actual != 0.0:
            diff['grasa'] = diff_grasa
        if isinstance(diff_musculo, float) and musculo_anterior != 0.0 and musculo_actual != 0.0:
            diff['musculo'] = diff_musculo
        if isinstance(diff_caliper, float) and caliper_anterior != 0.0 and caliper_actual != 0.0:
            diff['caliper'] = diff_caliper
        if isinstance(diff_gemelo, float) and gemelo_anterior != 0.0 and gemelo_actual != 0.0:
            diff['gemelo'] = diff_gemelo
        if isinstance(diff_cintura, float) and cintura_anterior != 0.0 and cintura_actual != 0.0:
            diff['cintura'] = diff_cintura
        if isinstance(diff_biceps, float) and biceps_anterior != 0.0 and biceps_actual != 0.0:
            diff['biceps'] = diff_biceps
        if isinstance(diff_muslo, float) and muslo_anterior != 0.0 and muslo_actual != 0.0:
            diff['muslo'] = diff_muslo
        if isinstance(diff_pecho, float) and pecho_anterior != 0.0 and pecho_actual != 0.0:
            diff['pecho'] = diff_pecho

        return diff
    except Exception as e:
        logger.error(e)
        return False


def completados_mes(**kwargs):
    fecha = date.today()
    year = fecha.strftime("%Y")
    month = fecha.month
    try:
        finalizacion = kwargs['finalizacion']
        num = Calendario.objects.all().filter(user_id=kwargs['user_id'], fecha__year=year, fecha__month=month,
                                              completado=finalizacion).count()
        return num
    except Exception as e:
        logger.error(e)
        return False


def tipo_ejercicios_mes(**kwargs):
    fecha = date.today()
    year = fecha.strftime("%Y")
    month = fecha.month
    try:
        zona = kwargs['zona']
        num = Calendario.objects.select_related('ejercicios'). \
        filter(user_id=kwargs['user_id'], fecha__year=year, fecha__month=month, ejercicios__zona=zona,
               completado__range=[1, 2]). \
        values('id', 'fecha', 'ejercicios', 'ejercicios__zona', 'ejercicios__nombre', 'completado').count()
        return num
    except Exception as e:
        logger.error(e)
        return False


def get_medidas(request, **kwargs):
    fecha = date.today()
    year = fecha.strftime("%Y")
    month = fecha.month
    if 'ultimo' in kwargs:
        query = Medida.objects.filter(user_id=request.user.id)[: 1]
        medidas = {'resultado': query, 'mesAnterior': True}
    else:
        query = Medida.objects.filter(user_id=request.user.id).filter(anyo=year).filter(mes=month)
        medidas = {'resultado': query, 'mesAnterior': False}
    return medidas


def get_calendario(request, **kwargs):
    order = kwargs['order'] if 'order' in kwargs else 'ejercicios__orden'
    filters = {
        "activo": kwargs['activo'],
    }
    if 'id_calendario' in kwargs:
        cal = Calendario.objects.values('comentario', 'fecha', 'completado', 'ejercicios__nombre',
                                        'ejercicios__indicaciones', 'ejercicios__url', 'ejercicios__tiempo',
                                        'ejercicios__reps', 'series').filter(id=kwargs['id_calendario']).filter(
            **filters).order_by(order)
    else:
        if 'numero' in kwargs:
            cal = Calendario.objects.all().filter(**filters).filter(user_id=request.user.id).order_by(order)[:kwargs['numero']]
        else:
            cal = Calendario.objects.values('completado','fecha','series','id').filter(**filters).filter(user_id=request.user.id)\
                .annotate(dcount=Count('fecha')).order_by(order)
    return cal
