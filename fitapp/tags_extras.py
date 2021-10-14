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

@register.simple_tag(takes_context=True)
def set_global_context(context, key, value):
    context.dicts[0][key] = value
    return ''