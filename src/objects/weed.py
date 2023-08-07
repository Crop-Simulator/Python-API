import bpy

from src.controllers.segmentation import SegmentationClass

class Weed:
    def __init__(self):
        self.segmentation_id = SegmentationClass.WEED.value
        self.weed_object = self.get_weed_model()

    def get_weed_model(self):
        bpy.context.active_object.name = "stage4.009"
        weed = bpy.context.scene.objects.get("stage4.009")
        weed_model = weed.copy()
        weed_model.data = weed.data.copy()
        weed_model["segmentation_id"] = self.segmentation_id
        return weed_model

    def set_location(self, location):
        self.weed_object.location = location
