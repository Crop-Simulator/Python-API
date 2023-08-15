import requests
from datetime import datetime, timedelta
import os

class WeatherController:
    HTTP_STATUS_OK = 200

    def __init__(self, api_key):
        self.api_key = api_key

    def get_historical_weather(self, start_date, end_date, lat, lon):
        base_url = "https://api.weather.com/v3/wx/hod/r1/direct"
        params = {
            "apiKey": self.api_key,
            "startDateTime": f"{start_date}T00Z",
            "endDateTime": f"{end_date}T23Z",
            "geocode": f"{lat},{lon}",
            "format": "json",
            "units": "e",
        }

        response = requests.get(base_url, params=params)
        if response.status_code == self.HTTP_STATUS_OK:
            data = response.json()
            processed_data = []
            processed_data.append({
                "date": data["validTimeUtc"],
                "max_temperature": data["temperatureMax24Hour"],
                "min_temperature": data["temperatureMin24Hour"],
                "precipitation": data.get("precip1Hour", 0),
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

def extract_daily_data(self, data):
    result = []

    dates = data[0]["date"]
    max_temps = data[0]["max_temperature"]
    min_temps = data[0]["min_temperature"]
    precipitations = data[0]["precipitation"]

    current_day_data = {}

    for i in range(len(dates)):
        current_date = dates[i][:10]

        if "date" not in current_day_data:
            current_day_data["date"] = current_date
            current_day_data["max_temperature"] = max_temps[i]
            current_day_data["min_temperature"] = min_temps[i]
            current_day_data["precipitation"] = precipitations[i]
        elif current_date == current_day_data["date"]:
            current_day_data["max_temperature"] = max(current_day_data["max_temperature"], max_temps[i])
            current_day_data["min_temperature"] = min(current_day_data["min_temperature"], min_temps[i])
            current_day_data["precipitation"] += precipitations[i]
        else:
            result.append(current_day_data.copy())
            current_day_data["date"] = current_date
            current_day_data["max_temperature"] = max_temps[i]
            current_day_data["min_temperature"] = min_temps[i]
            current_day_data["precipitation"] = precipitations[i]

    result.append(current_day_data)
    return result



# api_key = os.environ["WEATHER_API"]
# weather_controllerr = WeatherController(api_key)
# weather_data = weather_controllerr.get_weather_for_growth_period("spring", "2023-02-01", 35.6895, 149)
# daily_weather_data = weather_controllerr.extract_daily_data(weather_data)
# print(daily_weather_data)

