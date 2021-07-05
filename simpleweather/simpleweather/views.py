from django.http import HttpResponse

from .weather_client import WeatherClient

weather_client = WeatherClient()

def root(request):
    return HttpResponse("""
        <h2>simpleweather</h2>
        <p>a really simple wrapper over <a href="https://www.weather.gov/documentation/services-web-api">weather.gov's API</a>.</p>
        <p>Example urls:</p>
        <ul>
            <li><a href="/zip/98225/temp">current temp in Bellingham, WA</li>
            <li><a href="/zip/20002/temp">current temp in Washington, DC</li>
            <li><a href="/zip/20000/temp">invalid zip code</li>
        </ul>
    """)

def temp_at_zip(request, zipcode):
    temp = weather_client.get_current_temp_at_zipcode(zipcode)
    return HttpResponse(f"current temp at {zipcode} is {temp}")
