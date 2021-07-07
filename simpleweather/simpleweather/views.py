from django.http import HttpResponse

from .tasks import task_fetch_temp_at_zip, task_dummy

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
    result = task_fetch_temp_at_zip.delay(zipcode)
    temp = result.get()

    return HttpResponse(f"current temp at {zipcode} is {temp}")

def healthz(request):
    result = task_dummy.delay(40,2)
    assert result.get() == 42

    return HttpResponse('OK')
