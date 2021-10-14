from .oauth import Oauth
from django.http import HttpResponseRedirect
import datetime as dt
from ..utils import getDataTimes
import requests
import json


class Datos(Oauth):
    def __init__(self, request):
        super().__init__(request)


    def getData(self):
        startTimeMillis, endTimeMillis = getDataTimes()
        OAUTH_TOKEN = super().getOauth_Token()
        data = {
            "aggregateBy": [
                {
                    'dataTypeName': super().getOauthConfig('dataTypeCaloriesName')
                },
                {
                    'dataTypeName': super().getOauthConfig('dataTypeDistanceName')
                },
                {
                    # 'dataTypeName': dataTypeStepsName
                    'dataSourceId': 'derived:com.google.step_count.delta:com.google.android.gms:merge_step_deltas'
                },
                {
                    'dataTypeName': super().getOauthConfig('dataTypeActiveName')
                },
                {
                    "dataTypeName": super().getOauthConfig('dataTypeHeartName')
                },
                {
                    "dataSourceId": "derived:com.google.weight:com.google.android.gms:merge_weight"
                },
                {
                    "dataTypeName": super().getOauthConfig('dataTypeFatName')
                },
                {
                    "dataTypeName": super().getOauthConfig('dataTypeWattsName')
                },
                # {
                #     "dataTypeName": super().getOauthConfig('dataTypeActivitySegmentName']
                # },
            ],
            "bucketByTime": {
                "durationMillis": super().getOauthConfig('durationMillis'),
                "period": {
                    "timeZoneId": "Europe/Madrid",
                    "type": "day",
                    "value": 2,
                }
            },
            "startTimeMillis": str(startTimeMillis),
            "endTimeMillis": str(endTimeMillis),
        }
        try:
            headers = {'content-type': 'application/json; encoding=utf-8',
                       'Authorization': 'Bearer %s' % OAUTH_TOKEN}
            r = requests.post(super().getOauthConfig('url_aggregate'), json.dumps(data), headers=headers).json()
        except Exception as e:
            print(e)

        data_or_session = super().eval_data_or_session(data=r)
        if data_or_session != True:
            return data_or_session

        data = {}

        for i in r['bucket']:
            if len(i['dataset'][0]['point']) > 0:
                data['calories'] = {}
                data['calories']['value'] = int(i['dataset'][0]['point'][0]['value'][0]['fpVal'])
                longStart = dt.datetime.fromtimestamp(int(i['startTimeMillis']) / 1000.0, tz=dt.timezone.utc)
                data['calories']['longstart'] = str(longStart)
                data['calories']['start'] = i['startTimeMillis']
                longEnd = dt.datetime.fromtimestamp(int(i['endTimeMillis']) / 1000.0, tz=dt.timezone.utc)
                data['calories']['longend'] = str(longEnd)
                data['calories']['end'] = i['endTimeMillis']

            if len(i['dataset'][1]['point']) > 0:
                data['distance'] = {}
                data['distance']['value'] = int(i['dataset'][1]['point'][0]['value'][0]['fpVal'])
                longStart = dt.datetime.fromtimestamp(int(i['startTimeMillis']) / 1000.0, tz=dt.timezone.utc)
                data['distance']['longstart'] = str(longStart)
                data['distance']['start'] = i['startTimeMillis']
                longEnd = dt.datetime.fromtimestamp(int(i['endTimeMillis']) / 1000.0, tz=dt.timezone.utc)
                data['distance']['longend'] = str(longEnd)
                data['distance']['end'] = i['endTimeMillis']

            if len(i['dataset'][2]['point']) > 0:
                data['steps'] = {}
                data['steps']['value'] = i['dataset'][2]['point'][0]['value'][0]['intVal']
                longStart = dt.datetime.fromtimestamp(int(i['startTimeMillis']) / 1000.0, tz=dt.timezone.utc)
                data['steps']['longstart'] = str(longStart)
                data['steps']['start'] = i['startTimeMillis']
                longEnd = dt.datetime.fromtimestamp(int(i['endTimeMillis']) / 1000.0, tz=dt.timezone.utc)
                data['steps']['longend'] = str(longEnd)
                data['steps']['end'] = i['endTimeMillis']

            if len(i['dataset'][3]['point']) > 0:
                data['estimated_steps'] = {}
                data['estimated_steps']['value'] = i['dataset'][3]['point'][0]['value'][0]['intVal']
                longStart = dt.datetime.fromtimestamp(int(i['startTimeMillis']) / 1000.0, tz=dt.timezone.utc)
                data['estimated_steps']['longstart'] = str(longStart)
                data['estimated_steps']['start'] = i['startTimeMillis']
                longEnd = dt.datetime.fromtimestamp(int(i['endTimeMillis']) / 1000.0, tz=dt.timezone.utc)
                data['estimated_steps']['longend'] = str(longEnd)
                data['estimated_steps']['end'] = i['endTimeMillis']

            if len(i['dataset'][4]['point']) > 0:
                data['heart'] = {}
                data['heart']['value'] = i['dataset'][4]['point'][0]['value'][0]['fpVal']
                longStart = dt.datetime.fromtimestamp(int(i['startTimeMillis']) / 1000.0, tz=dt.timezone.utc)
                data['heart']['longstart'] = str(longStart)
                data['heart']['start'] = i['startTimeMillis']
                longEnd = dt.datetime.fromtimestamp(int(i['endTimeMillis']) / 1000.0, tz=dt.timezone.utc)
                data['heart']['longend'] = str(longEnd)
                data['heart']['end'] = i['endTimeMillis']

            if len(i['dataset'][5]['point']) > 0:
                data['weight'] = {}
                data['weight']['value'] = round(i['dataset'][5]['point'][0]['value'][0]['fpVal'], 1)
                longStart = dt.datetime.fromtimestamp(int(i['startTimeMillis']) / 1000.0, tz=dt.timezone.utc)
                data['weight']['longstart'] = str(longStart)
                data['weight']['start'] = i['startTimeMillis']
                longEnd = dt.datetime.fromtimestamp(int(i['endTimeMillis']) / 1000.0, tz=dt.timezone.utc)
                data['weight']['longend'] = str(longEnd)
                data['weight']['end'] = i['endTimeMillis']

            if len(i['dataset'][6]['point']) > 0:
                data['fat'] = {}
                data['fat']['value'] = i['dataset'][6]['point'][0]['value'][0]['fpVal']
                longStart = dt.datetime.fromtimestamp(int(i['startTimeMillis']) / 1000.0, tz=dt.timezone.utc)
                data['fat']['longstart'] = str(longStart)
                data['fat']['start'] = i['startTimeMillis']
                longEnd = dt.datetime.fromtimestamp(int(i['endTimeMillis']) / 1000.0, tz=dt.timezone.utc)
                data['fat']['longend'] = str(longEnd)
                data['fat']['end'] = i['endTimeMillis']

            if len(i['dataset'][7]['point']) > 0:
                data['watts'] = {}
                data['watts']['value'] = i['dataset'][8]['point'][0]['value'][0]['fpVal']
                longStart = dt.datetime.fromtimestamp(int(i['startTimeMillis']) / 1000.0, tz=dt.timezone.utc)
                data['watts']['longstart'] = str(longStart)
                data['watts']['start'] = i['startTimeMillis']
                longEnd = dt.datetime.fromtimestamp(int(i['endTimeMillis']) / 1000.0, tz=dt.timezone.utc)
                data['watts']['longend'] = str(longEnd)
                data['watts']['end'] = i['endTimeMillis']

            # if len(i['dataset'][8]['point']) > 0:
            #     data['activity_segments'] = {}
            #     data['activity_segments']['value'] = i['dataset'][7]['point'][0]['value'][0]['intVal']
            #     longStart = dt.datetime.fromtimestamp(int(i['startTimeMillis']) / 1000.0, tz=dt.timezone.utc)
            #     data['activity_segments']['longstart'] = str(longStart)
            #     data['activity_segments']['start'] = i['startTimeMillis']
            #     longEnd = dt.datetime.fromtimestamp(int(i['endTimeMillis']) / 1000.0, tz=dt.timezone.utc)
            #     data['activity_segments']['longend'] = str(longEnd)
            #     data['activity_segments']['end'] = i['endTimeMillis']

        return data
