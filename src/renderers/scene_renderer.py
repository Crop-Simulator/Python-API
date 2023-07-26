import os
import bpy
import random

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
        self.num_images = configs["num_images"]

    def render_scene(self):
        print("rendering...")
        current_working_directory = str(os.getcwd())
        image_directory = current_working_directory + "/output_images"
        bpy.data.collections[self.collection]
        self.cameracon.setup_camera()

        for i in range(self.num_images):
            angle_x = random.randint(0, 1000)
            angle_y = random.randint(0, 1000)
            angle_z = random.randint(0, 1000)
            distance = random.randint(5, 15)
            self.cameracon.update_camera(distance = distance, angle_rotation=(angle_x,angle_y,angle_z))

            current_file = self.output_file + str(i)


            bpy.context.scene.render.resolution_x = self.render_resolution_x
            bpy.context.scene.render.resolution_y = self.render_resolution_y
            bpy.context.scene.render.filepath = os.path.join(image_directory, current_file)
            bpy.ops.render.render(use_viewport=True, write_still=True)

            segmentation = Segmentation({
                SegmentationClass.BACKGROUND.value: SegmentationColor.LAND_GROUND_SOIL.value, # Background; land;ground;soil
                SegmentationClass.PLANT.value: SegmentationColor.PLANT.value, # Plant
                SegmentationClass.WEED.value: SegmentationColor.GRASS.value,
            })
            segmentation_filename = current_file.replace(".png", "_seg.png") if current_file.endswith(".png") else current_file + "_seg.png"
            segmentation.segment(image_directory + "/" + segmentation_filename)
