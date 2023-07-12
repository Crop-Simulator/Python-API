import json
import requests


class StableDiffusionAPI:
    HTTP_OK = 200

    def __init__(self, url: str):
        self.url = url

    def txt2img(self, config: dict) -> requests.Response:
        # Convert the JSON object to a string
        json_data = json.dumps(config)

        # Set the headers and send the POST request
        headers = {"Content-Type": "application/json"}
        response = requests.post(
            self.url + "/sdapi/v1/txt2img", data=json_data, headers=headers,
        )
        # Check the response status code
        if response.status_code == StableDiffusionAPI.HTTP_OK:
            resp_data = response.json()
            return resp_data
        else:
            raise Exception(f"Request failed with status code {response.status_code}: {response.text}")
