from django.http import HttpResponse

from .weather_client import WeatherClient

weather_client = WeatherClient()

def root(request):
    return HttpResponse("""
        <h2>simpleweather</h2>
        <p>a really simple wrapper over <a href="https://www.weather.gov/documentation/services-web-api">weather.gov's API</a>.</p>
    """)

def temp_at_zip(request, zipcode):
    temp = weather_client.get_current_temp_at_zipcode(zipcode)
    return HttpResponse(f"current temp at {zipcode} is {temp}")
