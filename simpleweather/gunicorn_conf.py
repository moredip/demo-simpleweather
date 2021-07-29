from simpleweather.honeycomb import beeline_init
from simpleweather.open_telemetry import otel_init

accesslog = '-'

def post_fork(server,worker):
    otel_init()
    #beeline_init()
