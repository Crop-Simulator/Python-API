import requests
from datetime import datetime, timedelta
import csv
from io import StringIO

class WeatherController:
    HTTP_STATUS_OK = 200
    DATE_LENGTH = 10
    SUNNY_IRRADIANCE_THRESHOLD = 200
    BASE_URL = "https://api.weather.com/v3"

    def __init__(self, api_key):
        self.api_key = api_key

    def get_historical_weather(self, start_date, end_date, lat, lon):
        api_url = f"{self.BASE_URL}/wx/hod/r1/direct"
        params = {
            "apiKey": self.api_key,
            "startDateTime": f"{start_date}T00Z",
            "endDateTime": f"{end_date}T23Z",
            "geocode": f"{lat},{lon}",
            "format": "json",
            "units": "e",
        }

        response = requests.get(api_url, params=params)
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

    def get_irradiance(self, start_date, end_date, lat, lon):
        api_url = f"{self.BASE_URL}/wx/observations/historical/analytical/ext"
        params = {
            "apiKey": self.api_key,
            "startDate": start_date.replace("-", ""),
            "endDate": end_date.replace("-", ""),
            "geocode": f"{lat},{lon}",
            "format": "csv",
            "units": "s",
            "productId": "GlobalHorizontalIrradiance",
            "language": "en-US",
        }
        response = requests.get(api_url, params=params)
        if response.status_code == self.HTTP_STATUS_OK:
            csv_reader = csv.DictReader(StringIO(response.text))
            data = [row for row in csv_reader]
            return data
        else:
            raise Exception(f"API request error with status code {response.status_code}. Response: {response.text}")


    def extract_evapotranspiration_data(self, data):
        result = []
        for row in data:
            result.append({
                "date": row.get("date", ""),
                "irradiance": row.get("GlobalHorizontalIrradianceLocalDaytimeAvg", 0),
                "snow": row.get("SnowAmountLocalDaytimeMax"),
            })
        return result

    def get_weather_for_growth_period(self, barley_type, planting_date, lat, lon):
        planting_date = datetime.strptime(planting_date, "%Y-%m-%d")
        if barley_type == "spring":
            harvest_date = planting_date + timedelta(days=10)  # Approx. 6 months
        elif barley_type == "winter":
            harvest_date = planting_date + timedelta(days=10)  # Approx. 9 months
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

    @staticmethod
    def convert_date_format(date_str):
        if len(date_str) == WeatherController.DATE_LENGTH:
            return date_str
        year, month, day = date_str[:4], date_str[4:6], date_str[6:]
        return f"{year}-{month}-{day}"

    @staticmethod
    def determine_label(entry):
        irradiance = entry.get("irradiance", 0)
        if entry.get("snow") is not None:
            return "snowy"
        elif entry.get("precipitation", 0.0) > 0:
            return "rainy"
        elif irradiance and float(irradiance) > WeatherController.SUNNY_IRRADIANCE_THRESHOLD:
            return "sunny"
        else:
            return "cloudy"

    def merge_data_based_on_date(self, weather_data, et_data):
        def convert_to_dict_by_date(data_list):
            return {self.convert_date_format(data["date"]): data for data in data_list}


        def merge_dicts(dict1, dict2):
            merged = {}
            for key, value in dict1.items():
                if key not in merged:
                    merged[key] = {}
                merged[key].update(value)

            for key, value in dict2.items():
                if key not in merged:
                    merged[key] = {}
                merged[key].update(value)
            for key in merged:
                merged[key]["label"] = WeatherController.determine_label(merged[key])

            return list(merged.values())

        weather_dict = convert_to_dict_by_date(weather_data)
        et_dict = convert_to_dict_by_date(et_data)
        return merge_dicts(weather_dict, et_dict)

    def get_merged_weather_data(self, barley_type, start_date, lat, lon):
        if barley_type == "spring":
            period = 10
        elif barley_type == "winter":
            period = 10
        end_date = (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=period)).strftime("%Y-%m-%d")
        weather_data = self.get_weather_for_growth_period(barley_type, start_date, lat, lon)
        daily_weather_data = self.extract_daily_data(weather_data)

        et_data = self.get_irradiance(start_date, end_date, lat, lon)
        daily_et_data = self.extract_evapotranspiration_data(et_data)

        return self.merge_data_based_on_date(daily_weather_data, daily_et_data)



