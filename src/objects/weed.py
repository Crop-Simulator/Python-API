import bpy

from src.controllers.segmentation import SegmentationClass

class Weed:
    def __init__(self):
        self.segmentation_id = SegmentationClass.WEED.value
        self.weed_object = self.get_weed_model()
        self.name = self.weed_object.name

    def get_weed_model(self):
        weed = bpy.context.scene.objects.get("weed")
        weed_model = weed.copy()
        weed_model.data = weed.data.copy()
        weed_model["segmentation_id"] = self.segmentation_id
        return weed_model

    def set_location(self, location):
        self.weed_object.location = location

    def get_location(self):
        return self.weed_object.location
