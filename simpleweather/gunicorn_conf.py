from simpleweather.honeycomb import beeline_init

accesslog = '-'

def post_worker_init(worker):
    beeline_init()
