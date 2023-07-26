import os
import bpy

from controllers.segmentation import Segmentation, SegmentationColor, SegmentationClass
from controllers.camera_controller import CameraController
from controllers.light_controller import LightController

class SceneRenderer:
    def __init__(self, configs, collection):
        self.output_file = configs["outfile"][0]
        self.collection = collection
        self.cameracon = CameraController("Photo Taker", (10,0,0), (1.57057,0.00174533,1.57057), self.collection)
        self.lightcon = LightController()
        self.resolution_data = configs["resolution"]
        self.render_resolution_x = self.resolution_data["x"]
        self.render_resolution_y = self.resolution_data["y"]

    def render_scene(self):
        print("rendering...")
        current_working_directory = str(os.getcwd())
        bpy.data.collections[self.collection]


        self.lightcon.add_light()
        self.lightcon.add_sky()
        self.cameracon.setup_camera()
        self.cameracon.update_camera(distance = 10, crop_location=(2,5,10))


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
