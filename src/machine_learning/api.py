import json
import requests
import warnings


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
            self.url + "/sdapi/v1/txt2img",
            data=json_data,
            headers=headers,
        )
        # Check the response status code
        if response.status_code == StableDiffusionAPI.HTTP_OK:
            resp_data = response.json()
            return resp_data
        else:
            raise requests.exceptions.HTTPError(
                f"Request failed with status code {response.status_code}: {response.text}",
            )


class Txt2ImgConfig:
    """
    Config for txt2img API
    """
    def __init__(self, **kwargs) -> None:
        """Initialize the config with default values. Use kwargs to override the defaults."""
        self.config = {
            "enable_hr": False,
            "denoising_strength": 0,
            "firstphase_width": 0,
            "firstphase_height": 0,
            "hr_scale": 2,
            "hr_upscaler": "string",
            "hr_second_pass_steps": 0,
            "hr_resize_x": 0,
            "hr_resize_y": 0,
            "hr_sampler_name": "string",
            "hr_prompt": "",
            "hr_negative_prompt": "",
            "prompt": "",
            "styles": ["string"],
            "seed": -1,
            "subseed": -1,
            "subseed_strength": 0,
            "seed_resize_from_h": -1,
            "seed_resize_from_w": -1,
            "sampler_name": "Euler",
            "batch_size": 1,
            "n_iter": 1,
            "steps": 35,
            "cfg_scale": 7,
            "width": 512,
            "height": 512,
            "restore_faces": False,
            "tiling": False,
            "do_not_save_samples": False,
            "do_not_save_grid": False,
            "negative_prompt": "",
            "eta": 0,
            "s_min_uncond": 0,
            "s_churn": 0,
            "s_tmax": 0,
            "s_tmin": 0,
            "s_noise": 1,
            "override_settings": {
                "sd_model_checkpoint": "dreamlike-photoreal-2.0",
            },
            "override_settings_restore_afterwards": True,
            "script_args": [],
            "sampler_index": "Euler",
            "script_name": "",
            "send_images": True,
            "save_images": False,
            "alwayson_scripts": {},
        }
        for key, value in kwargs.items():
            if key in self.config:
                self.config[key] = value
            else:
                warnings.warn(f"Unknown txt2img config key: {key}", stacklevel=1)

    def add_controlnet_segmentation(self, model: str, seg_map: str, depth_map: str = None):
        self.config["alwayson_scripts"]["controlnet"] = {
            "args": [{
                "module": "none",
                "model": model,
                "input_image": seg_map,
                "processor_res": 512,
                "resize_mode": 1, # 1 = "inner fit", 2 = "outer fit"
            },
            {
                "module": "none",
                "model": "control_v11f1p_sd15_depth [cfd03158]",
                "input_image": depth_map,
                "processor_res": 512,
                "threshold_a": -1,
                "threshold_b": -1,
                "resize_mode": 1,
            },
            ],
        }

    def to_dict(self) -> dict:
        return self.config
