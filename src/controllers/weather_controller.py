import requests
from datetime import datetime, timedelta


class WeatherController:
    HTTP_STATUS_OK = 200

    def __init__(self, api_key):
        self.api_key = api_key

    def get_historical_weather(self, start_date, end_date, lat, lon):
        base_url = "https://api.weatherbit.io/v2.0/history/daily"

        params = {
            "key": self.api_key,
            "start_date": start_date,
            "end_date": end_date,
            "lat": lat,
            "lon": lon,
        }
        response = requests.get(base_url, params=params)
        if response.status_code == self.HTTP_STATUS_OK:
            data = response.json()
            processed_data = []
            for day in data["data"]:
                processed_data.append({
                    "date": day["datetime"],
                    "temperature": day["temp"],
                    "precipitation": day["precip"],
                    "humidity": day["rh"],
                })
            return processed_data
        else:
            raise Exception(f"API request error with status code {response.status_code}")

    def get_weather_for_growth_period(self, barley_type, planting_date, lat, lon):
        planting_date = datetime.strptime(planting_date, "%Y-%m-%d")
        if barley_type == "spring":
            harvest_date = planting_date + timedelta(days=180)  # Approx. 6 months
        elif barley_type == "winter":
            harvest_date = planting_date + timedelta(days=270)  # Approx. 9 months
        return self.get_historical_weather(planting_date.strftime("%Y-%m-%d"), harvest_date.strftime("%Y-%m-%d"), lat, lon)


# yaml_reader = YamlReader()
# data = yaml_reader.read_file('Python-API/data.yml')
# planting_date = data['planting_date']
# lat = data['latitude']
# lon = data['longitude']
# barley_type = data['barley_type']


# api_key = "2b8fb3c4f62844189b7edec1063d92f9"
# weather_controller = WeatherController(api_key)
# weather_data = weather_controller.get_weather_for_growth_period(barley_type, planting_date, lat, lon)
# print(weather_data)
