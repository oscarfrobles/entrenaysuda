import json
import requests
from django.db.models import QuerySet
from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from fit.settings import STATIC_URL, URL_BASE
from .apigoogle.oauth import Oauth
from .models import Calendario
from .tasks import do
from .operaciones import insert_medidas, get_calendario, get_medidas, compara_medidas, completados_mes, \
    tipo_ejercicios_mes
import logging
from django.core.paginator import Paginator
from fitapp.apigoogle.googlefit import oauth_authenticate, oauth_login, get_session_oauth, get_data_oauth
from fitapp.apigoogle.crud import updateCalendario, getData
from .utils import get_random_txt
from django.core.serializers.json import DjangoJSONEncoder



logger = logging.getLogger(__name__)


def index(request):
    # check(request) No funciona la escritura en heroku, si lo paso a otro servidor pasar x check en lugar de do
    do(request)
    template = loader.get_template('index.html')
    context = {}
    try:
        pass
    except Exception as e:
        print(e)
    if request.method == "GET":
        if request.user.is_authenticated:
            username = request.user.id
            cal = get_calendario(request, numero=4, activo=True, order='fecha')
            hist = get_calendario(request, numero=4, activo=False, order='-fecha')
            medidas = get_medidas(request) if len(get_medidas(request)['resultado']) > 0 else get_medidas(request,
                                                                                                          ultimo=True)
            diff_medidas = compara_medidas(user_id=username)
            entre_completados_mes = completados_mes(user_id=username, finalizacion=1)
            entre_incompletados_mes = completados_mes(user_id=username, finalizacion=2)
            ejercicios_mes_uno = tipo_ejercicios_mes(user_id=username, zona=1)
            ejercicios_mes_dos = tipo_ejercicios_mes(user_id=username, zona=2)
            ejercicios_mes_tres = tipo_ejercicios_mes(user_id=username, zona=3)
            random_txt = get_random_txt()

            context = {
                'uname': username,
                'calendario': cal,
                'historico': hist,
                'medidas': medidas,
                'diff_medidas': diff_medidas,
                'completados_mes': entre_completados_mes,
                'incompletados_mes': entre_incompletados_mes,
                'ejerc_zona_uno': ejercicios_mes_uno,
                'ejerc_zona_dos': ejercicios_mes_dos,
                'ejerc_zona_tres': ejercicios_mes_tres,
                'random_txt': random_txt,
            }
            return HttpResponse(template.render(context, request))

    if request.method == "POST":
        if 'ajax' in request.POST:
            if 'medidas' in request.POST.get('ajax'):
                try:
                    insert_medidas(request)
                    return redirect('index')
                except Exception as e:
                    logger.error(e)
                    return render(request, 'index.html', {'error_message': 'Error al insertar las medidas'})

        if 'logout' in request.POST and request.POST['logout'] == "1":
            try:
                logout(request)
                return redirect('index')
            except Exception as inst:
                logger.error(inst)

        username = request.POST['uname']
        password = request.POST['pass']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                cal = get_calendario(request, numero=4, activo=True)
                medidas = get_medidas(request) if len(get_medidas(request)) > 0 else get_medidas(request, ultimo=True)
                context = {
                    'uname': username,
                    'calendario': cal,
                    'medidas': medidas
                }
                return HttpResponse(template.render(context, request))
            else:
                return render(request, 'index.html', {'error_message': 'Account Deactivaated'})
        else:
            return render(request, 'index.html', {'error_message': 'Invalid Login'})
    return HttpResponse(template.render(context, request))


def medidas(request):
    template = loader.get_template('medidas.html')
    context = {}
    if request.method == "GET":
        if request.user.is_authenticated:
            username = request.user.id
            medidas = get_medidas(request) if len(get_medidas(request)['resultado']) > 0 else get_medidas(request,
                                                                                                          ultimo=True)
            context = {
                'uname': username,
                'medidas': medidas,
            }
            return HttpResponse(template.render(context, request))


def entrenamientos(request, **kwargs):
    template = loader.get_template('entrenamientos.html')
    context = {}
    calendario_id = kwargs['calendario_id']
    if request.method == "GET":
        if request.user.is_authenticated:
            username = request.user.id
            entrenamientos = get_calendario(request, id_calendario=calendario_id, activo=True)
            context = {
                'uname': username,
                'entrenamientos': entrenamientos,
                # 'ejercicios': ejercicios,
            }
            return HttpResponse(template.render(context, request))
    if request.method == "POST" and request.is_ajax:
        context = False
        # calendario_id = k
        tipo = request.POST.get('tipo')
        data = request.POST.get('data')
        completado_update = entrenamiento_completado(request, data=data, tipo=tipo, calendario_id=calendario_id)
        return HttpResponse(completado_update)


def entrenamiento_completado(request, **kwargs):
    if request.user.is_authenticated:
        try:
            data = kwargs['data']
            if kwargs['tipo'] == 'completado':
                Calendario.objects.filter(id=kwargs['calendario_id']).update(completado=data)
            elif kwargs['tipo'] == 'comentario':
                Calendario.objects.filter(id=kwargs['calendario_id']).update(comentario=data)
            return True
        except Exception as e:
            logger.error(e)
            return False


def historico(request, **kwargs):
    template = loader.get_template('historico.html')
    calendario_id = kwargs['calendario_id']
    if request.method == "GET":
        if request.user.is_authenticated:
            username = request.user.id
            if 'calendario_id' in kwargs:
                historico = get_calendario(request, id_calendario=calendario_id, activo=False, order='fecha')
                all = False
            else:
                historico = get_calendario(request, activo=False, order='-fecha')
                all = True
            context = {
                'uname': username,
                'historico': historico,
                'all': all,
            }
            return HttpResponse(template.render(context, request))


def historico_all(request, **kwargs):
    template = loader.get_template('historico.html')
    context = {}
    if request.method == "GET":
        if request.user.is_authenticated:
            username = request.user.id
            try:
                historico = get_calendario(request, activo=False, order='-fecha')
                paginator = Paginator(historico, 10)

                page_number = request.GET.get('pag', 1)
                page = paginator.page(page_number)

                context = {
                    'uname': username,
                    'historico': page,
                    'all': all,
                    'page': page,
                    'paginator': paginator,
                }
            except Exception as e:
                logger.error(e)
                print(e)
            return HttpResponse(template.render(context, request))


def call_view_google(request):
    template = loader.get_template('google.html')
    session_oauth = get_session_oauth(request)
    data_oauth = get_data_oauth(request)
    if isinstance(session_oauth, HttpResponse):
        return session_oauth
    context = {
        'llamada': {
            'session': session_oauth,
            'data': data_oauth,
        }
    }
    return HttpResponse(template.render(context, request))

def get_connect_json_google(request):
    #"OAUTH_TOKEN" not in request.session
    sess = ''
    session_oauth = get_session_oauth(request)
    if isinstance(session_oauth, HttpResponse):
        data = {'connect': 'false'}
    else:
        data = {'connect': 'true'}
    data = json.dumps(data)
    return HttpResponse(data, content_type="application/json", status=200)

def get_data_json_google(request):
    session_oauth = get_session_oauth(request,url_redirect=request.path)
    data_oauth = get_data_oauth(request,url_redirect=request.path)
    if isinstance(session_oauth, HttpResponse):
        return session_oauth
    filters, inserts = getData(data=data_oauth,user=request.user.id)
    data = {
        'filters': filters,
        'inserts': inserts,
        'session': session_oauth,
    }
    data = json.dumps(data)
    return HttpResponse(data, content_type="application/json", status=200)



''' Devuelve una cantidad de datos infumable '''
''' def get_list_datasets_google(request):
    session_oauth = get_session_oauth(request, url_redirect=request.path)
    if isinstance(session_oauth, HttpResponse):
        return session_oauth
    ds = get_list_datasets(request, url_redirect=request.path)
    print(ds)
    data = {'datasets': ds}
    data = json.dumps(data)
    return HttpResponse(data, content_type="application/json", status=200) '''

def set_data_json_google(request):
    session_oauth = get_session_oauth(request,url_redirect=request.path)
    if isinstance(session_oauth, HttpResponse):
        return session_oauth
    data_oauth = get_data_oauth(request,url_redirect=request.path)
    oauth_data_update = updateCalendario(request, data=data_oauth, type='data')

    filters, inserts = getData(data=data_oauth,user=request.user.id)
    data = {
        'result': oauth_data_update,
    }
    data = json.dumps(data)
    return HttpResponse(data, content_type="application/json", status=200)

def set_session_json_google(request):
    oauth = Oauth(request)
    oauth_user = oauth.getOauth_User()
    session_oauth = get_session_oauth(request,url_redirect=request.path)
    if isinstance(session_oauth, HttpResponse):
        return session_oauth
    oauth_session_update = updateCalendario(request, json_session=session_oauth, type='session', oauth_user=oauth_user['name'])
    #filters, inserts = getData(data=session_oauth,user=request.user.id)
    data = {
        'result': oauth_session_update,
    }
    data = json.dumps(data)
    return HttpResponse(data, content_type="application/json", status=200)


def get_activities_types_json_google(request):
    url = URL_BASE + STATIC_URL + 'js/googlefit_activities_types.json'
    try:
        data = requests.get(url)
    except Exception as e:
        print(e)
    return HttpResponse(data.content, content_type="application/json", status=200)

def call_view_googlefit(request,**kwargs):
    try:
        auth = oauth_login(request, **kwargs)
        return auth
    except Exception as e:
        raise Exception(e)


def call_view_googlefit_authenticate(request):
    try:
        auth = oauth_authenticate(request)
        return auth
    except Exception as e:
        raise Exception(e)


def calendar_view(request):
    """ Mostrará un calendario con los ejercicios"""
    template = loader.get_template('calendario.html')
    username = request.user.id
    entrenamientos = get_calendario(request, activo='False' )




    q = Calendario.objects.values('comentario', 'fecha', 'completado', 'ejercicios__nombre',
                                        'ejercicios__indicaciones', 'ejercicios__url', 'ejercicios__orden', 'ejercicios__tiempo',
                                        'ejercicios__reps', 'series','calories','steps','estimated_steps','distance',
                                        'heart','bpm','weight','session_google', 'session_google__name',
                                        'session_google__duration','session_google__name',
                                        'session_google__activityType').filter(user=username).order_by('ejercicios__orden')


    data = json.dumps(list(q), cls=DjangoJSONEncoder)

    print(data.replace("'", r"\\'").replace("/", r"\\/").replace('\n', '\\n').replace('\r','\\r'))

    context = {'json_cal': data.replace("'", r"\'").replace("/", r"\/").replace('\n', '\\n').replace('\r','\\r') }
    return HttpResponse(template.render(context, request))
