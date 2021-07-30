from simpleweather.open_telemetry import otel_init

accesslog = '-'

def post_fork(server,worker):
    otel_init()
