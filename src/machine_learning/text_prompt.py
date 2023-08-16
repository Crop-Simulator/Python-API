from enum import Enum, auto


class Weather(Enum):
    SUNNY = auto()
    CLOUDY = auto()
    WINDY = auto()
    RAINY = auto()
    STORMY = auto()
    SNOWY = auto()
    FOGGY = auto()


class CameraType(Enum):
    DRONE = auto()
    ROBOT = auto()


class CropType(Enum):
    BARLEY = auto()


class WeedType(Enum):
    WEED = auto()


class SoilType(Enum):
    BROWN_SOIL = auto()
    LOAM = auto()
    SANDY_LOAM = auto()


class CameraAngle(Enum):

    TOP_DOWN_90 = auto()
    BIRDS_EYE_VIEW_65 = auto()
    HIGH_ANGLE_SHOT_45 = auto()
    ABOVE_SHOT_30 = auto()
    SLIGHTLY_ABOVE_15 = auto()

    STRAIGHT_ON_0 = auto()

    HERO_VIEW__15 = auto()
    LOW_VIEW__45 = auto()
    WORMS_EYE_VIEW__75 = auto()

    # fallback case
    EXTREME_VIEW = auto()


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
