from opentelemetry import trace
from noaa_sdk import NOAA

from .models import CachedTemperature

tracer = trace.get_tracer(__name__)

class WeatherClient:
    def __init__(self):
        self._noaa = NOAA()

    def get_current_temp_at_zipcode(self,zip):
        with tracer.start_as_current_span("weather_client/get_current_temp_at_zipcode") as span:
            span.set_attribute('zip',zip)

            cached_temp = self.get_temp_from_cache(zip)
            if cached_temp:
                span.set_attribute('weather_client/cache','hit')
                return cached_temp

            span.set_attribute('weather_client/cache','miss')

            temp = self.get_current_temp_at_zipcode_via_api(zip)
            self.write_temp_to_cache(zip=zip,temp=temp)

            return temp

    def write_temp_to_cache(self,zip,temp):
        CachedTemperature.objects.create(zipcode=zip,temperature=temp)

    def get_temp_from_cache(self,zip):
        cached_entry = CachedTemperature.objects.latest_fresh_entry_for_zipcode(zip)
        return cached_entry and cached_entry.temperature or None

    def get_current_temp_at_zipcode_via_api(self,zip):
        with tracer.start_as_current_span("weather_client/get_observations"):
            observations = self._noaa.get_observations(zip,'US')

        with tracer.start_as_current_span("weather_client/get_first_observation"):
            first_observation = next(observations,None)

        if( not first_observation ):
            return None

        temp = first_observation['temperature']['value']

        return temp


