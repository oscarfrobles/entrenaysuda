from fit.settings import GOOGLEFIT_CONFIG
from django.http import HttpResponseRedirect
from httplib2 import Http
from urllib import parse
import json


class Oauth(object):
    __instance = None
    OAUTH_TOKEN = None
    session = None

    def __init__(self,request):
        self.session = request.session

    def Oauth(self):
        if Oauth.__instance is None:
            Oauth.__instance = Oauth()
        return Oauth._instance

    def login(self):
        token_request_uri = "https://accounts.google.com/o/oauth2/auth"
        response_type = "code"
        client_id = GOOGLEFIT_CONFIG['CLIENT_ID']
        redirect_uri = GOOGLEFIT_CONFIG['REDIRECT_URI']
        scope =GOOGLEFIT_CONFIG['OAUTH_SCOPES']
        url = "{token_request_uri}?response_type={response_type}&client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}".format(
            token_request_uri=token_request_uri,
            response_type=response_type,
            client_id=client_id,
            redirect_uri=redirect_uri,
            scope=scope,
        )
        return HttpResponseRedirect(url)

    def authenticate(self, request, **kwargs):
        parser = Http()
        login_failed_url = '/'
        if 'error' in request.GET or 'code' not in request.GET:
            return HttpResponseRedirect('{loginfailed}'.format(loginfailed=login_failed_url))

        params = parse.urlencode({
            'code': kwargs['code'],
            'redirect_uri': GOOGLEFIT_CONFIG['REDIRECT_URI'],
            'client_id': GOOGLEFIT_CONFIG['CLIENT_ID'],
            'client_secret': GOOGLEFIT_CONFIG['APP_SECRET_KEY'],
            'grant_type': 'authorization_code',
        })
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        resp, content = parser.request(GOOGLEFIT_CONFIG['access_token_uri'], method='POST', body=params, headers=headers)
        token_data = json.loads(content)

        self.session["OAUTH_TOKEN"] = token_data['access_token']
        self.setOauth_Token(token_data['access_token'])
        resp, content = parser.request(
            "https://www.googleapis.com/oauth2/v1/userinfo?access_token={accessToken}".format(
                accessToken=token_data['access_token']))
        self.setOauth_Profile(json.loads(content))
        url_redirect = request.session.get('redirect', '/google')
        return HttpResponseRedirect(url_redirect)

    def setOauth_Token(self, token):
        self.session['OAUTH_TOKEN'] = token

    def getOauth_Token(self):
        token = None
        if 'OAUTH_TOKEN' in self.session:
            token = self.session['OAUTH_TOKEN']
        return token

    def setOauth_Profile(self, profile):
        if 'error' not in profile:
            profile_aux = profile
        else:
            profile_aux = None
        self.session['OAUTH_profile'] = profile_aux

    def getOauth_User(self):
        profile = None
        if 'OAUTH_profile' in self.session:
            profile = self.session['OAUTH_profile']
        return profile

    def getOauthConfig(self, key):
        if key in GOOGLEFIT_CONFIG:
            return GOOGLEFIT_CONFIG[key]
        else:
            raise ValueError('No existe la clave ' + key)

    def eval_data_or_session(self, **kwargs):
        if 'data' in kwargs and 'bucket' not in kwargs['data'] and 'error' in kwargs['data']:
            if kwargs['data']['error']['code'] == 401:
                return HttpResponseRedirect('/oauth/')
            else:
                raise ValueError(kwargs['data']['error']['message'])
        else:
            if 'session' in kwargs and 'session' in kwargs['session'] and 'error' in kwargs['session']:
                if kwargs['session']['error']['code'] == 401:
                    return HttpResponseRedirect('/oauth/')
                else:
                    raise ValueError(kwargs['session']['error']['message'])
            else:
                return True
