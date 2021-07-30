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


# # start a trace with the start of each task
# @signals.task_prerun.connect
# def start_celery_trace(task_id, task, args, kwargs, **rest_args):
#     queue_name = task.request.delivery_info.get("exchange", None)
#     task.request.trace = beeline.start_trace(
#         context={
#             "name": "celery",
#             "celery.task_id": task_id,
#             "celery.args": args,
#             "celery.kwargs": kwargs,
#             "celery.task_name": task.name,
#             "celery.queue": queue_name,
#         }
#     )

# # finish and send the trace at the end of each task
# @signals.task_postrun.connect
# def end_celery_trace(task, state, **kwargs):
#     beeline.add_field("celery.status", state)
#     beeline.finish_trace(task.request.trace)
