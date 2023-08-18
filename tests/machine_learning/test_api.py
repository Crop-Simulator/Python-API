import unittest
from unittest.mock import patch, Mock

import requests
from src.machine_learning.api import StableDiffusionAPI
from src.machine_learning.x2img_config import Txt2ImgConfig


class TestStableDiffusionAPI(unittest.TestCase):
    def setUp(self):
        self.api = StableDiffusionAPI("http://localhost:8000")

    @patch("requests.post")
    def test_txt2img_success(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"image": "base64-encoded-image"}
        mock_post.return_value = mock_response

        config = Txt2ImgConfig(prompt="A cat sitting on a couch")
        response = self.api.txt2img(config.config)

        self.assertEqual(response, {"image": "base64-encoded-image"})

    @patch("requests.post")
    def test_txt2img_failure(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_post.return_value = mock_response

        config = Txt2ImgConfig(prompt="A cat sitting on a couch")
        with self.assertRaises(requests.exceptions.HTTPError):
            self.api.txt2img(config.config)



    def test_add_controlnet_segmentation(self):
        model = "my_model"
        input_image = "42"
        config = Txt2ImgConfig()
        config.add_controlnet_segmentation(model, input_image)
        expected_config = {
            "alwayson_scripts": {
                "controlnet": {
                    "args": [{
                        "module": "none",
                        "model": model,
                        "input_image": input_image,
                        "processor_res": 512,
                        "resize_mode": 1,
                    }],
                },
            },
        }
        self.assertEqual(config.to_dict()["alwayson_scripts"]["controlnet"]["args"][0], expected_config["alwayson_scripts"]["controlnet"]["args"][0])



if __name__ == "__main__":
    unittest.main()
