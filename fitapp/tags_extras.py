from django.template.defaulttags import register


@register.filter(name='get_fechaEntrenamiento')
def get_fechaEntrenamiento(d):
    try:
        return d[0]['fecha']
    except KeyError:
        raise KeyError('Error de nombre de la clave de entrenamiento')

@register.filter(name='get_comentarioEntrenamiento')
def get_comentarioEntrenamiento(d):
    try:
        return d[0]['comentario']
    except KeyError:
        raise KeyError('Error de nombre de la clave de entrenamiento')

@register.filter(name='get_completadoEntrenamiento')
def get_completadoEntrenamiento(d):
    try:
        return d[0]['completado']
    except KeyError:
        raise KeyError('Error de nombre de la clave de entrenamiento')

@register.filter(name='get_Calories')
def get_Calories(d):
    try:
        return d[0]['calories']
    except KeyError:
        raise KeyError('Error de nombre de calories')


@register.filter(name='get_Steps')
def get_Steps(d):
    try:
        return d[0]['steps']
    except KeyError:
        raise KeyError('Error de nombre de steps')


@register.filter(name='get_EstimatedSteps')
def get_EstimatedSteps(d):
    try:
        return d[0]['estimated_steps']
    except KeyError:
        raise KeyError('Error de nombre de estimated_steps')


@register.filter(name='get_Distance')
def get_Distance(d):
    try:
        return d[0]['distance']
    except KeyError:
        raise KeyError('Error de nombre de distance')


@register.filter(name='get_Heart')
def get_Heart(d):
    try:
        return d[0]['heart']
    except KeyError:
        raise KeyError('Error de nombre de heart')


@register.filter(name='get_Bpm')
def get_Bpm(d):
    try:
        return d[0]['bpm']
    except KeyError:
        raise KeyError('Error de nombre de bpm')


@register.filter(name='get_Weight')
def get_Weight(d):
    try:
        return d[0]['weight']
    except KeyError:
        raise KeyError('Error de nombre de weight')

@register.filter(name='get_Sesiones')
def get_Sesiones(d):
    sesiones = []
    print(d[0]['session_google'])
    #print(d)
    for i in d:
        try:
            # sesiones[i] = d[i]
            # return sesiones
            print(i['session_google'])
        except Exception as e:
            raise e


@register.simple_tag(takes_context=True)
def set_global_context(context, key, value):
    context.dicts[0][key] = value
    return ''