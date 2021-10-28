from .oauth import Oauth
from django.http import HttpResponseRedirect
import datetime as dt
from ..utils import getDataTimes
import requests


class Sesiones(Oauth):
    def __init__(self, request, **kwargs):
        super().__init__(request)

    def getSession(self):
        OAUTH_TOKEN = super().getOauth_Token()
        headers = {'content-type': 'application/json; encoding=utf-8',
                   'Authorization': 'Bearer %s' % OAUTH_TOKEN}
        startTime, endTime = getDataTimes(raw=True, timedelta=super().getOauthConfig('timedelta_session'))

        url_s = super().getOauthConfig('url_session') % {'startTime': startTime, 'endTime': endTime}
        q = requests.get(url_s, headers=headers).json()

        data_or_session = super().eval_data_or_session(session=q)
        if data_or_session != True:
            return data_or_session

        if 'session' not in q and 'error' in q:
            if q['error']['code'] == 401:
                return HttpResponseRedirect('/oauth/')
            else:
                raise ValueError(q['error']['message'])

        session = []

        for i in q['session']:
            start = dt.datetime.fromtimestamp(int(i['startTimeMillis']) / 1000.0, tz=dt.timezone.utc)
            end = dt.datetime.fromtimestamp(int(i['endTimeMillis']) / 1000.0, tz=dt.timezone.utc)
            duration = ((end - start).total_seconds() / 60)
            session_aux = {
                'start': int(i['startTimeMillis']),
                'end': int(i['endTimeMillis']),
                'duration': str(round(duration,2)),
                'name': i['name'],
                'description': i['description'],
                'activityType': i['activityType'],
                'id_google': i['id'],
                'application': i['application']['packageName'],
            }
            session.append(session_aux)
            del session_aux

        return session

    ''' Devuelve una cantidad de datos infumable '''
    '''def listDataSets(self):
        OAUTH_TOKEN = super().getOauth_Token()
        headers = {'content-type': 'application/json; encoding=utf-8',
                   'Authorization': 'Bearer %s' % OAUTH_TOKEN}

        url_s = super().getOauthConfig('url_dataSets') % {'key': super().getOauthConfig('OAUTH_API_KEY')}
        q = requests.get(url_s, headers=headers).json()
        return q '''

    ''' Devuelve una cantidad de datos infumable '''
    ''' def listDataSources(self, dataStreamId):
        OAUTH_TOKEN = super().getOauth_Token()
        headers = {'content-type': 'application/json; encoding=utf-8',
                   'Authorization': 'Bearer %s' % OAUTH_TOKEN}

        url_s = super().getOauthConfig('url_dataSources') % {
                                'dataStreamId': dataStreamId,
                                'key': super().getOauthConfig('OAUTH_API_KEY')
                }
        q = requests.get(url_s, headers=headers).json()
        return q '''

