import bpy
from mathutils import Vector


from src.controllers.segmentation import SegmentationClass
from src.growth_simulator.growth_manager import GrowthManager, CropHealth

class Barley:
    def __init__(self, config, stage, health, weather_data):
        self.GDD_PER_STAGE = 139

        self.stage = stage
        self.health = health
        self.weather_data = weather_data
        self.growth_stage = ["stage0.stand", "stage1.stand", "stage2.stand", "stage3.stand", "stage4.stand",
                             "stage5.stand", "stage6.stand", "stage7.stand","stage8.stand",
                             "stage9.stand", "stage10.stand"]
        self.active_weeds = []
        self.crop_type = SegmentationClass.PLANT.value
        self.barley_object = None
        self.location = None
        self.set_model_stage(self.stage)
        self.name = self.barley_object.name
        self.config = config
        self.days_per_stage = self.config["growth_simulator"]["days_per_stage"]
        self.growth_manager = GrowthManager(self.config, self.barley_object, self.days_per_stage, self.weather_data)
        self.crop_health = {
            "healthy": (0.2, 0.8, 0.2, 1),  # Green in RGBA
            "unhealthy": (0.6, 0.8, 0.2, 1),  # Yellow-green in RGBA
            "dead": (0.0, 0.0, 0.0, 1.0),  # Brown in RGBA
        }

    def set_model_stage(self, stage):
        duplicate = bpy.context.scene.objects.get(self.growth_stage[stage])
        barley_object = duplicate.copy()
        barley_object.data = duplicate.data.copy()
        barley_object["segmentation_id"] = self.crop_type
        bpy.context.collection.objects.link(barley_object)
        self.barley_object = barley_object
        self.name = barley_object.name

    def set_location(self, location):
        self.location = location
        self.barley_object.location = location

    def get_location(self):
        return self.location

    def set_height(self, scale):
        self.barley_object.scale = Vector((scale, scale, scale))

    def add_weed(self, weed):
        self.active_weeds.append(weed)

    def get_weeds(self):
        return self.active_weeds

    def measure_height(self, crop_object):
        # Get the coordinates of the object's vertices
        vertices = [v.co for v in crop_object.data.vertices]

        # Get the transformation matrix of the object
        matrix_world = crop_object.matrix_world

        # Initialise min and max Y coordinates
        min_y = float("inf")
        max_y = float("-inf")

        # Calculate the minimum and maximum Y coordinates of the transformed coordinates
        for vertex in vertices:
            transformed_vertex = matrix_world @ vertex
            min_y = min(min_y, transformed_vertex.y)
            max_y = max(max_y, transformed_vertex.y)

        # Calculating the height of an object
        crop_height = max_y - min_y

        return crop_height

    def set_color(self, color):
        material = bpy.data.materials.new(name="Barley_Material")
        material.diffuse_color = color
        if self.barley_object.data.materials:
            self.barley_object.data.materials[0] = material
        else:
            self.barley_object.data.materials.append(material)
        self.barley_object.active_material = material
        
    def grow(self, location):
        self.growth_manager.progress_day()
        self.stage = self.growth_manager.progress_stage()
        self.set_model_stage(self.stage)
        self.set_location(location)
        self.growth_manager.evaluate_plant_health()
        self.health = self.growth_manager.update_health_status()
        if not self.growth_manager.status == CropHealth.HEALTHY.value:
            self.set_color(self.crop_health[self.growth_manager.status])
        self.name = self.barley_object.name
