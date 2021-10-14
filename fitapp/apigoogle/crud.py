from fitapp.models import Calendario, SesionesGoogle
import datetime


def getData(**kwargs):
    data = kwargs['data']
    filters = {}
    inserts = {}
    for i in data:
        if len(str(data[i]['value'])) > 0:
            inserts[i] = data[i]['value']
            start = int(data[i]['start'])
            date = datetime.datetime.fromtimestamp(start / 1000.0)
            filters['fecha'] = date.strftime('%Y-%m-%d')
        filters['user'] = kwargs['user']
    return filters, inserts


def updateData(**kwargs):
    filters, inserts = getData(**kwargs)
    try:
        query = Calendario.objects.filter(**filters).update(**inserts)
    except Exception as e:
        raise ValueError(e)
    return True


def updateSession(**kwargs):
    filters = {}
    filters_calendario = {}
    ids_sessions = []
    try:
        for i in kwargs['data']:
            if kwargs['oauth_user'] is not None:
                i['user_google'] = kwargs['oauth_user']
            q = SesionesGoogle.objects.filter(**filters).update_or_create(**i)
            fecha = datetime.datetime.fromtimestamp(q[0].start / 1000.0)
            filters_calendario['fecha'] = fecha.strftime('%Y-%m-%d')
            ids_sessions.append(q[0].id)
    except Exception as e:
        raise ValueError(e)

    if len(ids_sessions) > 0:
        try:
            filters_calendario['user'] = kwargs['user']
            num = Calendario.objects.filter(**filters_calendario).count()
            if num > 0:
                query = Calendario.objects.get(**filters_calendario)
                q = query.session_google.add(*ids_sessions)
        except Exception as e:
            raise ValueError(e)

    return True


def updateCalendario(request, **kwargs):
    user = request.user.id
    oauth_user = kwargs.get('oauth_user', None)
    type = kwargs.get("type")
    if type == 'data':
        upd = updateData(data=kwargs['data'], user=user)
    if type == 'session':
        upd = updateSession(data=kwargs['json_session'], user=user, oauth_user=oauth_user)
    return upd
