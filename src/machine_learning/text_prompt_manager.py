from enum import Enum, auto

class Weather(Enum):
    SUNNY = auto()
    RAINY = auto()
    WINDY = auto()

class CameraType(Enum):
    DRONE = auto()
    ROBOT = auto()

class CropType(Enum):
    BARLEY = auto()

class WeedType(Enum):
    WEED = auto()

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


prompt_manager = TextPromptManager(Weather.SUNNY, CameraType.DRONE)
print(prompt_manager.get_prompt())
