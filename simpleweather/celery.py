import os

from celery import Celery, signals

from .open_telemetry import otel_init

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simpleweather.settings')

app = Celery('simpleweather')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@signals.worker_process_init.connect(weak=False)
def initialize_otel(**kwargs):
    otel_init()
