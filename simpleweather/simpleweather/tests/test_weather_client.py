from django.test import SimpleTestCase

from ..weather_client import WeatherClient

# integrated tests 

def test_fetching_current_temperature_for_a_zipcode():
    client = WeatherClient()

    result = client.get_current_temp_at_zipcode(98225)

    assert -100 < result and result < 100

