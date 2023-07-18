import requests
from datetime import datetime


class WeatherController:
    HTTP_STATUS_OK = 200

    def __init__(self, api_key):
        self.api_key = api_key

    def calculate_weather_conditions(self, lat, lon):
        base_url = "https://api.weatherbit.io/v2.0/current?"
        complete_url = base_url + "lat=" + str(lat) + "&lon=" + str(lon) + "&key=" + self.api_key
        response = requests.get(complete_url)
        data = response.json()

        if response.status_code != self.HTTP_STATUS_OK:
            print(f"API request error with status code {response.status_code}")
            return None

        if data:
            temperature = data["data"][0]["temp"]
            precipitation = data["data"][0]["precip"]
            humidity = data["data"][0]["rh"]
            sun_rise = data["data"][0]["sunrise"]
            sun_set = data["data"][0]["sunset"]

            return temperature, precipitation, humidity, sun_rise, sun_set
        else:
            return None, None, None, None

    def calculate_sunlight_hours(self, sunrise, sunset):
        # Format the sunrise and sunset times as datetime objects
        sunrise_time = datetime.strptime(sunrise, "%H:%M")
        sunset_time = datetime.strptime(sunset, "%H:%M")

        # Calculate the difference in hours between sunrise and sunset
        sunlight_hours = (sunset_time - sunrise_time).seconds / 3600

        return sunlight_hours




