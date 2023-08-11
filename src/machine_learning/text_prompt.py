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


class SoilType(Enum):
    BROWN_SOIL = auto()
    LOAM = auto()
    SANDY_LOAM = auto()


class CameraAngle(Enum):
    STRAIGHT_ON_0 = auto()
    SLIGHTLY_ABOVE_15 = auto()
    ABOVE_SHOT_30 = auto()
    HIGH_ANGLE_SHOT_45 = auto()
    BIRDS_EYE_VIEW_65 = auto()
    TOP_DOWN_90 = auto()


def camera_angle_interpreter(camera_tilt: float) -> CameraAngle:
    if 0 <= camera_tilt < 30:
        return CameraAngle.STRAIGHT_ON_0
    elif 30 <= camera_tilt < 60:
        return CameraAngle.HIGH_ANGLE_SHOT_45
    elif 60 <= camera_tilt <= 90:
        return CameraAngle.TOP_DOWN_90
    else:
        raise ValueError("Camera tilt must be between 0 and 90 degrees inclusive.")
