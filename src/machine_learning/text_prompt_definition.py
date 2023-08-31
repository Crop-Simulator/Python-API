from enum import Enum, auto


class Weather(Enum):
    SUNNY = auto()
    CLOUDY = auto()
    WINDY = auto()
    RAINY = auto()
    STORMY = auto()
    SNOWY = auto()
    FOGGY = auto()

    def __str__(self):
        return str(self.name).lower()


class CropType(Enum):
    BARLEY = auto()

    def __str__(self):
        return self.name.replace('_', ' ').lower()


class WeedType(Enum):
    WEED = auto()
    BROADLEAF_WEED = auto()

    def __str__(self):
        return self.name.replace('_', ' ').lower()


class SoilType(Enum):
    BROWN_SOIL = auto()
    LOAM = auto()
    SANDY_LOAM = auto()

    def __str__(self):
        return self.name.replace('_', ' ').lower()


class CameraAngle(Enum):

    TOP_DOWN_90 = "top down view"
    BIRDS_EYE_VIEW_65 = "high angle"
    HIGH_ANGLE_SHOT_45 = "high angle"
    ABOVE_SHOT_30 = "from above"
    SLIGHTLY_ABOVE_15 = "from slightly above"

    STRAIGHT_ON_0 = "front view, straight on"

    HERO_VIEW__15 = "from slightly below"
    LOW_VIEW__45 = "from below"
    WORMS_EYE_VIEW__75 = "from below"

    # fallback case
    EXTREME_VIEW = " "

    def __str__(self):
        return self.value


def camera_angle_interpret(camera_angle: float) -> CameraAngle:

    if camera_angle > 100:
        return CameraAngle.EXTREME_VIEW

    if camera_angle >= 80:
        return CameraAngle.TOP_DOWN_90
    elif camera_angle >= 55:
        return CameraAngle.BIRDS_EYE_VIEW_65
    elif camera_angle >= 37.5:
        return CameraAngle.HIGH_ANGLE_SHOT_45
    elif camera_angle >= 22.5:
        return CameraAngle.ABOVE_SHOT_30
    elif camera_angle >= 7.5:
        return CameraAngle.SLIGHTLY_ABOVE_15

    elif camera_angle >= -7.5:
        return CameraAngle.STRAIGHT_ON_0

    elif camera_angle >= -30:
        return CameraAngle.HERO_VIEW__15
    elif camera_angle >= -60:
        return CameraAngle.LOW_VIEW__45
    elif camera_angle >= -95:
        return CameraAngle.WORMS_EYE_VIEW__75

    else:
        return CameraAngle.EXTREME_VIEW
