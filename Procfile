release: python manage.py migrate
web: gunicorn fit.wsgi --log-file -
worker: python manage.py qcluster
