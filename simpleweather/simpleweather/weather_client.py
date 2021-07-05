from noaa_sdk import NOAA

class WeatherClient:
    def __init__(self):
        self._noaa = NOAA()

    def get_current_temp_at_zipcode(self,zip):
        observations = self._noaa.get_observations(zip,'US')
        first_observation = next(observations,None)
        return first_observation['temperature']['value']
