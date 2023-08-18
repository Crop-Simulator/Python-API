import json

class X2ImgConfig:
    """
    Base config for X2Img API
    """
    def __init__(self, **kwargs) -> None:
        """Initialize the config with default values. Use kwargs to override the defaults."""
        self.config = {
            "prompt": "",
            "styles": [],
            "seed": -1,
            "subseed": -1,
            "subseed_strength": 0,
            "seed_resize_from_h": -1,
            "seed_resize_from_w": -1,
            "sampler_name": "DPM++ 2M Karras",
            "batch_size": 1,
            "n_iter": 1,
            "steps": 30,
            "cfg_scale": 7,
            "width": 512,
            "height": 512,
            "negative_prompt": "",
            "alwayson_scripts": {},
            "script_args": [],
            "sampler_index": "DPM++ 2M Karras",
            "script_name": "",
        }
        self.config.update(kwargs)

    def to_json(self):
        """Convert the config to a JSON string."""
        return json.dumps(self.config)

    def to_dict(self) -> dict:
        return self.config

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

class Img2ImgConfig(X2ImgConfig):
    """
    Config for img2img API
    """
    def __init__(self, **kwargs) -> None:
        """Initialize the config with default values. Use kwargs to override the defaults."""
        super().__init__(**kwargs)
        self.config.update({
            "init_images": [],
            "resize_mode": 0,
            "denoising_strength": 0.75,
            "image_cfg_scale": 0,
            "override_settings": {},
            "override_settings_restore_afterwards": True,
            "include_init_images": False,
            "send_images": True,
            "save_images": False,
        })
        self.config.update(kwargs)

    def set_init_images(self, images: list):
        """
        Set the initial images for the config.

        Args:
            images (list): A list of base64-encoded images.

        Returns:
            None
        """
        self.config["init_images"] = images

class Txt2ImgConfig(X2ImgConfig):
    """
    Config for txt2img API
    """
    def __init__(self, **kwargs) -> None:
        """Initialize the config with default values. Use kwargs to override the defaults."""
        super().__init__(**kwargs)
        self.config.update({
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
        })
