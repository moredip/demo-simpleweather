web: gunicorn simpleweather.wsgi -c simpleweather/gunicorn_conf.py
release: python manage.py migrate
worker: celery -A simpleweather worker -l DEBUG
