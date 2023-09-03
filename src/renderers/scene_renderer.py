import os
import bpy

from controllers.segmentation import Segmentation, SegmentationColor, SegmentationClass
from controllers.camera_controller import CameraController
from controllers.light_controller import LightController

from src.machine_learning.text_prompt_definition import camera_angle_interpret


class SceneRenderer:
    def __init__(self, configs, collection):
        self.collection = collection
        self.resolution_data = configs["resolution"]
        self.render_resolution_x = self.resolution_data["x"]
        self.render_resolution_y = self.resolution_data["y"]
        self.output_configs = configs["output"]
        self.num_images = self.output_configs["num_images_per_day"]
        self.directory = self.output_configs["directory"]
        self.output_file = self.output_configs["file_name"]
        self.camera_angles = self.output_configs["camera_angles"]
        
        self.brightness = self.output_configs["brightness"]
        self.growth_simulator = configs["growth_simulator"]
        self.total_days = self.growth_simulator["total_days"]
        self.sun_direction = (0, 0, self.brightness)
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
        self.close_camera_angles = ["straight_on", "high_angle", "above_shot"]
        self.closest_camera_angle = ["low_angle", "worms_eye", "hero_shot"]
        self.curr_image = 0
        
        self.cameracon = CameraController("Photo Taker", (0, 0, 0), (1.57057, 0.00174533, 1.57057), self.collection)
        self.lightcon = LightController(sun_direction=self.sun_direction)

    def setup_render(self):
        self.lightcon.add_light()
        self.lightcon.add_sky()
        self.cameracon.setup_camera()
    
    def reset_camera_position(self):
        self.cameracon.camera_location = (0, 0, 0)
        self.cameracon.camera_rotation = (0, 0, 0)

    def update_scene(self, day, text_prompt_manager):
        print("rendering...EPOCH: ", day)
        current_working_directory = str(os.getcwd())
        image_directory = current_working_directory + "/" + self.directory

        for i in range(self.num_images):
            
            distance = 20
            if self.camera_angles[i] in self.close_camera_angles:
                distance = 10
            elif self.camera_angles[i] in self.closest_camera_angle:
                distance = -1

            self.reset_camera_position()
            self.cameracon.update_camera(distance = distance, angle_rotation=(0, 0, 0), camera_angles = self.preset_camera_angles[self.camera_angles[i]])

            current_file = self.output_file + str(i) + "rendered_day" + str(day)

            # bpy.context.scene.eevee.taa_render_samples = self.render_samples
            bpy.context.scene.render.resolution_x = self.render_resolution_x
            bpy.context.scene.render.resolution_y = self.render_resolution_y
            bpy.context.scene.render.filepath = os.path.join(image_directory, current_file)
            bpy.data.scenes['Scene'].render.border_min_x = 0.25
            bpy.data.scenes['Scene'].render.border_max_x = 0.75
            bpy.data.scenes['Scene'].render.border_min_y = 0.25
            bpy.data.scenes['Scene'].render.border_max_y = 0.75
            bpy.ops.render.render(use_viewport=True, write_still=True)
            text_prompt_manager.camera_angle = camera_angle_interpret(self.cameracon.get_photography_camera_angle())
            with open(os.path.join(image_directory, self.output_file + str(i) + "rendered_day" + str(day) + ".txt"), "w") as file:
                file.write(text_prompt_manager.prompt_for_generation())

            segmentation = Segmentation({
                SegmentationClass.BACKGROUND.value: SegmentationColor.SKY.value,  # Background;
                SegmentationClass.PLANT.value: SegmentationColor.PLANT.value,  # Plant
                SegmentationClass.WEED.value: SegmentationColor.GRASS.value,
                SegmentationClass.SOIL.value: SegmentationColor.LAND_GROUND_SOIL.value,  # land;ground;soil
            })
            segmentation_filename = current_file.replace(".png", "_seg.png") if current_file.endswith(
                ".png") else current_file + "_seg.png"
            depth_map_filename = segmentation_filename.replace("_seg.png", "_depth.png")
            segmentation.segment(os.path.join(image_directory, segmentation_filename),
                                 os.path.join(image_directory, depth_map_filename))
            self.curr_image += 1

