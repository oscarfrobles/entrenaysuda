import datetime

from .models import Medida, Calendario, User, Ejercicio
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
    sesiones = None
    filters = {
        "activo": str(kwargs['activo']),
    }
    if 'id_calendario' in kwargs:
        cal = Calendario.objects.values('comentario', 'fecha', 'completado', 'ejercicios__nombre',
                                        'ejercicios__indicaciones', 'ejercicios__url', 'ejercicios__instagram_code', 'ejercicios__tiempo',
                                        'ejercicios__reps', 'series','calories','steps','estimated_steps','distance',
                                        'heart','bpm','weight')\
            .filter(id=kwargs['id_calendario']).filter(**filters).order_by(order)
        sesiones = Calendario.objects.order_by().values('session_google', 'session_google__name', 'session_google__description',
                                        'session_google__duration','session_google__name','session_google__activityType')\
            .filter(id=kwargs['id_calendario']).filter(**filters).exclude(session_google__isnull=True).distinct()
        print(sesiones.count())

        # str_activo = str(kwargs['activo'])
        # cal = Calendario.objects.raw("SELECT cal.id, eje_m.calendario_id, eje_m.ejercicio_id, cal.comentario, cal.fecha, "
        #                              "cal.completado, cal.series, cal.calories, cal.steps, cal.distance,cal.estimated_steps, "
        #                              "eje.nombre, eje.indicaciones, eje.orden, eje.url, eje.nivel, eje.reps, eje.tiempo  "
        #                              " FROM fitapp_calendario as cal "
        #                              " INNER JOIN fitapp_calendario_ejercicios as eje_m ON cal.id=eje_m.calendario_id "
        #                              " INNER JOIN fitapp_ejercicio as eje ON eje.id = eje_m.ejercicio_id"
        #                              " WHERE cal.activo='" + str_activo + "' and cal.id='" + str(kwargs['id_calendario']) +"'")
        # print(cal)
    else:
        if 'numero' in kwargs:
            cal = Calendario.objects.all().filter(**filters).filter(user_id=request.user.id).order_by(order)[:kwargs['numero']]
        else:
            cal = Calendario.objects.values('completado','fecha','series','id').filter(**filters).filter(user_id=request.user.id)\
                .annotate(dcount=Count('fecha')).order_by(order)
    return cal, sesiones

def checkCalendarToday(**kwargs):
    copy = False
    users = getUsers()
    for user in users:
        numEvents = checkNumEventsToday(user_id=user['id'])
        if numEvents == 0:
            copy = copy_calendar(user['id'])
    return copy

def getUsers():
    users = User.objects.values('id','email', 'username', 'first_name', 'last_name')
    return users

def getDefaultCalendarFilters(**kwargs):
    dt = datetime.datetime.now()
    user = kwargs.get('user_id')
    filters = {
        'fecha': "%d-%02d-%02d" % (dt.year, dt.month, dt.day),
        'user_id': user,
    }
    return filters

def checkNumEventsToday(**kwargs):
    user = kwargs.get('user_id')
    filters = getDefaultCalendarFilters(user_id=user)
    cal = Calendario.objects.filter(**filters)
    return cal.count()

''' Retorna el id del calendario para el día de hoy del usuario recibido por parámetro'''
def getTodayIdEvent(**kwargs):
    result = False
    user_id = kwargs.get('user_id')
    dt = datetime.datetime.now()
    filters = getDefaultCalendarFilters(user_id=kwargs['user_id'])
    calendar_id = Calendario.objects.values('id').filter(**filters)
    if calendar_id.count() > 0:
        result = calendar_id[0]['id']
    return result

''' Retorna el id del calendario para el día de hoy del usuario recibido por parámetro'''
def getLastActiveIdEvent(**kwargs):
    result = False
    user_id = kwargs.get('user_id')
    dt = datetime.datetime.now()
    filters = getDefaultCalendarFilters(user_id=kwargs['user_id'])
    filters.pop('fecha')
    filters['activo'] = False
    filters['completado'] = 0
    calendar_id = Calendario.objects.values('id').filter(**filters).last()
    if str(calendar_id['id']).isnumeric() and None != calendar_id:
        result = calendar_id['id']
    return result




''' Si no existe un entrenamiento para el día de hoy copia el entrenamiento
de hace 7 días y si no existe copia el último que haya
'''
def copy_calendar(user_id):
    dt = datetime.datetime.now() - datetime.timedelta(days=-7)
    today = datetime.datetime.now()
    filters = {
        'user_id': user_id,
        'fecha': "%d-%02d-%02d" % (dt.year, dt.month, dt.day),
    }
    try:
        last = Calendario.objects.values("id", "series", "fecha", "ejercicios__id").filter(**filters)
        if last.count()==0:
            print("no hay en los últimos días")
            if 'fecha' in filters:
                del filters['fecha']
                filters['activo'] = False
                filters['completado'] = 0
            last = Calendario.objects.values("id", "series", "fecha").filter(**filters).last()
            filters['id'] = last['id']
        last = Calendario.objects.values("id", "series", "fecha", "ejercicios__id", "ejercicios__nombre").filter(**filters)\
            .annotate(dcount=Count('id')).order_by()

        data = {
            'ejercicios_id': [],
        }
        for i in last:
            data['ejercicios_id'].append(i['ejercicios__id'])
            data['series']= i['series']
            data['fecha']= datetime.date(today.year, today.month, today.day)


        filters = {
            'activo': True,
            'completado': 0,
            'fecha': data['fecha'],
            'user_id': user_id,
            'series': data['series'],
        }
        new = Calendario.objects.create(**filters)
        related = new.ejercicios.set(data['ejercicios_id'])
    except Exception as e:
        logger.error(str(e))
    return True