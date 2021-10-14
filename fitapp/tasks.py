# Python Code
# project/myapp/tasks.py

from datetime import date, timedelta
import os

from django.conf import settings
from .models import Calendario
import logging

logger = logging.getLogger(__name__)

def deleteDateFiles(self):
    res = True
    try:
        directory = settings.MEDIA_ROOT
        logger.debug(directory)
        files_in_directory = os.listdir(directory)
        filtered_files = [file for file in files_in_directory if file.endswith(".date")]
        for file in filtered_files:
            path_to_file = os.path.join(directory, file)
            os.remove(path_to_file)
            logger.info('borrado: ' +  path_to_file)
    except Exception as e:
        print(e)
        logger.error(e)
        res = False
    return res

def check(self):
    res = True
    try:
        today = str(date.today().strftime("%d%m%Y"))
        url = os.path.join(settings.MEDIA_ROOT,'{0}.date').format(today)
        if os.path.isfile(url):
            logger.debug("Existe fichero")
        else:
            deleteDateFiles(self)
            do(self)
            f = open(url, "w+")
            f.close()
    except Exception as e:
        print(e)
        logger.error(e)
        res = False
    return res


def do(self):
    res = True
    # 2 días antes
    #calendario = Calendario.objects.only('id').filter(fecha__lt=date.today() - timedelta(days=2) ).filter(activo=True)
    calendario = Calendario.objects.only('id').filter(fecha__lt=date.today() - timedelta(days=1)).filter(activo=True)
    if len(calendario) == 0:
        return True
    try:
        data_id_calendario = []
        for i in calendario:
            id_calendario = int(i.id)
            data_id_calendario.append(id_calendario)
        Calendario.objects.filter(id__in=data_id_calendario).update(activo=False)
        logger.debug('Inactivando calendarios')
        res = True
    except Exception as e:
        print(e)
        logger.error(e)
        res = False
    return res