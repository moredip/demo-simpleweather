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
            <li><a href="/healthz">healthcheck (verifies worker tasks are functioning)</li>
        </ul>
    """)

def temp_at_zip(request, zipcode):
    # Doing this in a worker then blocking on the result pretty much entirely defeats the point of doing it in the worker.
    # This is unnecessarily contrived, and only done in order to demonstrate observability.
    # result = task_fetch_temp_at_zip.delay(zipcode)
    # temp = result.get()

    temp = task_fetch_temp_at_zip(zipcode)

    return HttpResponse(f"current temp at {zipcode} is {temp}")

def healthz(request):
    result = task_dummy.delay(40,2)
    assert result.get() == 42

    return HttpResponse('OK')
