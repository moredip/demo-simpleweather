import beeline
from noaa_sdk import NOAA

class WeatherClient:
    def __init__(self):
        self._noaa = NOAA()

    @beeline.traced(name='weather_client/get_current_temp_at_zipcode')
    def get_current_temp_at_zipcode(self,zip):
        beeline.add_context_field("zip", zip)

        with beeline.tracer(name="weather_client/get_observations"):
            observations = self._noaa.get_observations(zip,'US')

        with beeline.tracer(name="weather_client/get_first_observation"):
            first_observation = next(observations,None)

        if( not first_observation ):
            return None

        return first_observation['temperature']['value']
