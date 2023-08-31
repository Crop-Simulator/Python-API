from .text_prompt_definition import Weather, CropType, WeedType, SoilType, CameraAngle


class TextPromptManager:
    def __init__(self):
        self.weather = None
        self.crop_type = None
        self.weed_type = None
        self.soil_type = None
        self.camera_angle = None

    def get_attribute_string(self):

        # Concat all members' string value with ", ", ignoring None
        return ", ".join([str(getattr(self, key))
                   for key in vars(self).keys()
                   if getattr(self, key) is not None])

    def blip_inference(self):
        # TODO: use blip model to infer prompt, and concat with config specified in training file
        return "TODO:blip_inference"

    def prompt_for_training(self):
        positive_prompt = self.blip_inference() + ", " + \
                          self.get_attribute_string() + \
                          ", best quality, 4k, 8k, ultra highres, raw photo, sharp focus, intricate texture, " \
                          "skin imperfections, crop field, soil, photo, photorealistic"
        negative_prompt = "illustration, anime"
        return {"positive": positive_prompt,
                "negative": negative_prompt}

    def prompt_for_generation(self):
        positive_prompt = self.get_attribute_string() + \
                          ", best quality, 4k, 8k, ultra highres, raw photo, sharp focus, intricate texture, " \
                          "skin imperfections, crop field, soil, photo, photorealistic"
        negative_prompt = "illustration, anime"
        return positive_prompt + "\n" + negative_prompt
