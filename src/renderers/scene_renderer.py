import os
import bpy

from controllers.segmentation import Segmentation, SegmentationColor, SegmentationClass
from controllers.camera_controller import CameraController
from controllers.light_controller import LightController

class SceneRenderer:
    def __init__(self, configs, collection):
        self.collection = collection
        self.cameracon = CameraController("Photo Taker", (0, 0, 0), (1.57057,0.00174533,1.57057), self.collection)
        self.lightcon = LightController()
        self.resolution_data = configs["resolution"]
        self.render_resolution_x = self.resolution_data["x"]
        self.render_resolution_y = self.resolution_data["y"]
        self.output_configs = configs["output"]
        self.num_images = self.output_configs["num_images_per_day"]
        self.directory = self.output_configs["directory"]
        self.output_file = self.output_configs["file_name"]
        self.camera_angle = self.output_configs["camera_angle"]
        self.growth_simulator = configs["growth_simulator"]
        self.total_days = self.growth_simulator["total_days"]
        self.render_samples = 10
        self.preset_camera_angles = {
            "top_down": (0, 0, 0),
            "birds_eye": (15, 0, 0),
            "high_angle": (45, 0, 0),
            "above_shot": (60, 0, 0),
            "straight_on": (90, 0, 0),
            "hero_shot": (120, 0, 0),
            "low_angle": (135, 0, 0),
            "worms_eye": (150, 0, 0),

        }
        self.curr_image = 0

    def render_scene(self, day):
        print("rendering...")
        current_working_directory = str(os.getcwd())
        image_directory = current_working_directory + "/" + self.directory
        bpy.context.view_layer.update()
        self.lightcon.add_light()
        self.lightcon.add_sky()
        self.cameracon.setup_camera()


        while self.curr_image < (self.num_images + day):
            distance = 20

            self.cameracon.update_camera(distance = distance, angle_rotation=(0, 0, 0), camera_angles = self.preset_camera_angles[self.camera_angle])
            current_file = self.output_file + str(self.curr_image)


            # bpy.context.scene.eevee.taa_render_samples = self.render_samples
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
            depth_map_filename = segmentation_filename.replace("_seg.png", "_depth.png")
            segmentation.segment(os.path.join(image_directory, segmentation_filename), os.path.join(image_directory, depth_map_filename))
            self.curr_image += 1
