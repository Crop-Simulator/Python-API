from enum import Enum, auto
from text_prompt import Weather, CameraType, CropType, WeedType


class TextPromptManager:
    def __init__(self, weather: Weather, camera_type: CameraType):
        self.weather = weather
        self.camera_type = camera_type

    def validate_prompt(self):
        if self.weather not in Weather:
            raise ValueError(f"Invalid weather: {self.weather}")

        if self.camera_type not in CameraType:
            raise ValueError(f"Invalid camera type: {self.camera_type}")

    def get_prompt(self):
        self.validate_prompt()
        return f"Weather: {self.weather.name}, Camera Type: {self.camera_type.name}"

    def blip_inference(self):
        # TODO: use blip model to infer prompt, and concat with config specified in training file
        return 1

    def prompt_for_training(self):
        # TODO: generate prompt for training
        return 1

    def prompt_for_generation(self):
        # TODO: generate prompt for generation
        return 1

prompt_manager = TextPromptManager(Weather.SUNNY, CameraType.DRONE)
print(prompt_manager.get_prompt())
