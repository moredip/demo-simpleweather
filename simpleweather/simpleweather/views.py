from django.http import HttpResponse

def root(request):
    return HttpResponse("""
        <h2>simpleweather</h2>
        <p>a really simple wrapper over <a href="https://www.weather.gov/documentation/services-web-api">weather.gov's API</a>.</p>
    """)
