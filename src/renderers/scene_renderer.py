import os
import bpy

from controllers.segmentation import Segmentation, SegmentationColor, SegmentationClass
from controllers.camera_controller import CameraController
from controllers.light_controller import LightController

class SceneRenderer:
    def __init__(self, output_file, collection, resolution):
        self.output_file = output_file
        self.collection = collection
        self.cameracon = CameraController()
        self.lightcon = LightController()
        self.render_resolution_x = resolution["x"]
        self.render_resolution_y = resolution["y"]

    def render_scene(self):
        print("rendering...")
        current_working_directory = str(os.getcwd())
        bpy.data.collections[self.collection]


        self.lightcon.add_light()
        self.lightcon.add_sky()
        self.cameracon.setup_camera("camera_one", (10,0,0), (1.57057,0.00174533,1.57057), self.collection)


        bpy.context.scene.render.resolution_x = self.render_resolution_x
        bpy.context.scene.render.resolution_y = self.render_resolution_y
        bpy.context.scene.render.filepath = os.path.join(current_working_directory, self.output_file)
        bpy.ops.render.render(use_viewport=True, write_still=True)

        segmentation = Segmentation({
            SegmentationClass.BACKGROUND.value: SegmentationColor.LAND_GROUND_SOIL.value, # Background; land;ground;soil
            SegmentationClass.PLANT.value: SegmentationColor.PLANT.value, # Plant
            SegmentationClass.WEED.value: SegmentationColor.GRASS.value,
        })
        segmentation_filename = self.output_file.replace(".png", "_seg.png") if self.output_file.endswith(".png") else self.output_file + "_seg.png"
        segmentation.segment(segmentation_filename)
