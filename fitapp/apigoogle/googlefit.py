from django.http import HttpResponseRedirect
from .oauth import Oauth
from .sesiones import Sesiones
from .datos import Datos

def get_data_oauth(request, **kwargs):
    login_failed_url = '/oauth/?redirect=' + kwargs.get('url_redirect', '/')
    if "OAUTH_TOKEN" not in request.session:
        return HttpResponseRedirect('{loginfailed}'.format(loginfailed=login_failed_url))
    data = Datos(request)
    return data.getData()


def get_session_oauth(request, **kwargs):
    login_failed_url = '/oauth/?redirect=' + kwargs.get('url_redirect', '/')
    oauth = Oauth(request)
    if oauth.getOauth_Token() is None:
        return HttpResponseRedirect('{loginfailed}'.format(loginfailed=login_failed_url))
    sesion = Sesiones(request, **kwargs)
    return sesion.getSession()


''' Devuelve una cantidad de datos infumable '''
''' def get_list_datasets(request, **kwargs):
    login_failed_url = '/oauth/?redirect=' + kwargs.get('url_redirect', '/')
    oauth = Oauth(request)
    if oauth.getOauth_Token() is None:
        return HttpResponseRedirect('{loginfailed}'.format(loginfailed=login_failed_url))
    sesion = Sesiones(request, **kwargs)
    dt = sesion.listDataSets()

    ds = []
    for i in dt['dataSource']:
        #Incluye elementos como distance steps weight bpm watts
        id = i['dataStreamId']
        tipo =i['dataType']['field'][0]['name']
        ds.append(sesion.listDataSources(id))
    return ds '''

def oauth_login(request):
    if 'redirect' in request.GET:
        # del request.session['redirect']
        request.session['redirect'] = request.GET['redirect']
    oauth = Oauth(request)
    login = oauth.login()
    return login


def oauth_authenticate(request):
    code = request.GET['code']
    oauth = Oauth(request)
    login = oauth.authenticate(request,code=code)
    return login

def get_datasets_list_oauth(request):
    oauth = Oauth(request)
    if oauth.getOauth_Token() is None:
        return HttpResponseRedirect('/error')
    sesion = Sesiones(request)
    return sesion.listDataSources()
