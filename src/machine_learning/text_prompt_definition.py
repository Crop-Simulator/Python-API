from enum import Enum, auto
from typing import List, Tuple


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
        return self.name.replace("_", " ").lower()


class WeedType(Enum):
    WEED = auto()
    BROADLEAF_WEED = auto()

    def __str__(self):
        return self.name.replace("_", " ").lower()


class SoilType(Enum):
    BROWN_SOIL = auto()
    LOAM = auto()
    SANDY_LOAM = auto()

    def __str__(self):
        return self.name.replace("_", " ").lower()


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


# Define constants for each threshold value
EXTREME_THRESHOLD = 100
TOP_DOWN_90_THRESHOLD = 80
BIRDS_EYE_VIEW_65_THRESHOLD = 55
HIGH_ANGLE_SHOT_45_THRESHOLD = 37.5
ABOVE_SHOT_30_THRESHOLD = 22.5
SLIGHTLY_ABOVE_15_THRESHOLD = 7.5
STRAIGHT_ON_0_THRESHOLD = -7.5
HERO_VIEW__15_THRESHOLD = -30
LOW_VIEW__45_THRESHOLD = -60
WORMS_EYE_VIEW__75_THRESHOLD = -95


def camera_angle_interpret(camera_angle: float) -> CameraAngle:
    thresholds: List[Tuple[float, CameraAngle]] = [
        (EXTREME_THRESHOLD, CameraAngle.EXTREME_VIEW),
        (TOP_DOWN_90_THRESHOLD, CameraAngle.TOP_DOWN_90),
        (BIRDS_EYE_VIEW_65_THRESHOLD, CameraAngle.BIRDS_EYE_VIEW_65),
        (HIGH_ANGLE_SHOT_45_THRESHOLD, CameraAngle.HIGH_ANGLE_SHOT_45),
        (ABOVE_SHOT_30_THRESHOLD, CameraAngle.ABOVE_SHOT_30),
        (SLIGHTLY_ABOVE_15_THRESHOLD, CameraAngle.SLIGHTLY_ABOVE_15),
        (STRAIGHT_ON_0_THRESHOLD, CameraAngle.STRAIGHT_ON_0),
        (HERO_VIEW__15_THRESHOLD, CameraAngle.HERO_VIEW__15),
        (LOW_VIEW__45_THRESHOLD, CameraAngle.LOW_VIEW__45),
        (WORMS_EYE_VIEW__75_THRESHOLD, CameraAngle.WORMS_EYE_VIEW__75),
    ]

    # Loop through the thresholds and return the corresponding CameraAngle for the first match.
    for threshold, angle in thresholds:
        if camera_angle >= threshold:
            return angle

    # If no thresholds match, return the most extreme view.
    return CameraAngle.EXTREME_VIEW
