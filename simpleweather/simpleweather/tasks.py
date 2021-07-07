from ..celery import app

from .weather_client import WeatherClient

weather_client = WeatherClient()

@app.task
def task_dummy(x,y):
    result = x+y
    print(f'{x} + {y} = {result}')
    return result

@app.task
def task_fetch_temp_at_zip(zipcode):
    temp = weather_client.get_current_temp_at_zipcode(zipcode)
    return temp
