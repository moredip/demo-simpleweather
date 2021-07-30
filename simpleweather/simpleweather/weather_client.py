from opentelemetry import trace

from noaa_sdk import NOAA

tracer = trace.get_tracer(__name__)

class WeatherClient:
    def __init__(self):
        self._noaa = NOAA()

    def get_current_temp_at_zipcode(self,zip):
        with tracer.start_as_current_span("weather_client/get_current_temp_at_zipcode") as span:
            span.set_attribute('zip',zip)

            with tracer.start_as_current_span("weather_client/get_observations"):
                observations = self._noaa.get_observations(zip,'US')

            with tracer.start_as_current_span("weather_client/get_first_observation"):
                first_observation = next(observations,None)

            if( not first_observation ):
                return None

            return first_observation['temperature']['value']
