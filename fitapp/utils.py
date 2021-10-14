import random
import datetime as dt
from datetime import datetime, timezone, timedelta


def get_random_txt():
    txt = [
        'A por ello!',
        'Gota a gota',
        'Just do it!!!',
        'A quemar y endurecer!!!',
    ]
    return random.choice(txt)

def getDataTimes(**kwargs):
    tmdelta = kwargs['timedelta'] if 'timedelta' in kwargs else 0
    today = dt.date.today() - timedelta(tmdelta)
    # today = dt.date.today()

    if 'raw' in kwargs:
        now = datetime.utcnow() - timedelta(tmdelta)
        # now = datetime.utcnow()
        mañana = now.replace(tzinfo=timezone.utc).strftime('%Y-%m-%dT8:00:00Z')
        noche = now.replace(tzinfo=timezone.utc).strftime('%Y-%m-%dT23:59:59Z')
        return mañana, noche
    else:
        m = dt.time(hour=8, minute=00)
        t = dt.time(hour=23, minute=59)
        mañana = int(dt.datetime.combine(today, m).timestamp() * 1000.0)
        noche = int(dt.datetime.combine(today, t).timestamp() * 1000.0)
    return mañana, noche
