import random
import bpy
from mathutils import Vector

from .light_controller import LightController
from .segmentation import SegmentationClass
from .ground_controller import GroundController

class CropController:

    def __init__(self, config, collection):
        self.config = config
        self.collection_name = collection
        self.crop_size = 0.5
        self.counter = 1
        self.crop_data = config["crop"]
        self.type = self.crop_data["type"]
        self.size = self.crop_data["size"]
        self.percentage_share = self.crop_data["percentage_share"]
        self.total_number = self.crop_data["total_number"]
        self.num_rows = self.crop_data["num_rows"]
        self.row_widths = self.crop_data["row_widths"]
        self.growth_stage = {
            "stage10" : "stage10.009",
            "stage9" : "stage9.009",
            "stage8" : "stage8.009",
            "stage7" : "stage7.009",
            "stage6" : "stage6.009",
            "stage5" : "stage5.009",
            "stage4" : "stage4.009",
            "stage3" : "stage3.009",
            "stage2" : "stage2.009",
            "stage1" : "stage1.009",
            "ground" : "stage9.ground",
        }
        try:
            self.generation_seed = config["generation_seed"]
        except KeyError:
            self.generation_seed = None
        self.procedural_generation()
        self.crop_health = {
            "Healthy": (0.2, 0.8, 0.2, 1),   # Bright green in RGBA
            "Slightly Unhealthy": (0.6, 0.8, 0.2, 1), # Yellow in RGBA
            "Dead": (0.6, 0.4, 0.2, 1),       # Brown in RGBA
        }

    def setup_crops(self):
        for obj in bpy.context.scene.objects:
            if obj.name not in self.growth_stage.values():
                obj.select_set(True)
        bpy.ops.object.delete()

        lightcon = LightController()
        lightcon.add_light()

        groundcon = GroundController(self.config)
        print(self.config["ground_type"])
        groundcon.get_ground_stages()

        self.setup_crop_positions()

        collection = bpy.data.collections.get(self.collection_name)
        for obj in bpy.context.scene.objects:
            if obj.name in self.growth_stage.values():
                duplicate = collection.objects.get(obj.name)
                collection.objects.unlink(duplicate)

    def setup_crop_positions(self):
        curr_row = 0
        curr_loc = 0
        curr_crop_type = 0
        curr_crop = 0
        num_rows = self.num_rows
        loc_z = 0
        loc_y = 0
        loc_x = 0
        for crop in range(self.total_number):

            if crop % num_rows == 0:
                # splits crops into rows:
                # increases row num, when reached and
                # increments location by 1
                curr_row += 1
                curr_loc = 0

            num_crops = int(self.total_number * self.percentage_share[curr_crop_type])
            if curr_crop % num_crops == 0 and crop != 0:
                # counts the correct number of crops have
                # been generated based on their percentage share
                # excludes: first crop because it should always be
                # generated and will always return 0


                curr_crop = 0
                if not curr_crop_type >= len(self.type) - 1:
                    # checks that there are more crop types
                    # before changing to next crop type
                    curr_crop_type += 1

            curr_loc += 1
            crop_model = self.add_crop(self.crop_size, self.growth_stage[self.type[curr_crop_type]], [loc_x, loc_y, loc_z])

            # Set crop health randomly (for demonstration purposes)
            health_status = random.choice(["Healthy", "Dead", "Slightly Unhealthy"])
            self.set_crop_health(crop_model, health_status)

            if loc_x + 1 == self.row_widths:
                loc_y += 1
                loc_x = 0
            else:
                loc_x += 1
            material, segmentation_id = self.assign_crop_type(self.type[curr_crop_type])

            crop_model["segmentation_id"] = segmentation_id

            curr_crop += 1

    # TODO procedural_generation Implementation.
    def procedural_generation(self):
        random.seed(self.generation_seed)

    def assign_crop_type(self, crop_type):
        # assign material and segmentation id depending on crop type
        material = bpy.data.materials.new(crop_type)
        segmentation_id = SegmentationClass.PLANT.value
        return material, segmentation_id

    def add_crop(self, crop_size, growth_stage, loc):
        bpy.context.active_object.name = growth_stage
        cube = bpy.context.scene.objects.get(growth_stage)
        duplicated = cube.copy()
        duplicated.data = cube.data.copy()
        loc[0] - random.uniform(-.2, .2)
        loc[1] - random.uniform(-.2, .2)
        duplicated.location = (loc[0], loc[1], loc[2])

        self.counter += 1
        bpy.context.collection.objects.link(duplicated)

        # for ob in cube.users_collection[:]: #unlink from all preceeding object collections
        #     ob.objects.unlink(cube)
        # collection.objects.link(cube)

        # Measure the height of the crop
        #crop_height = self.measure_crop_height(duplicated)
        #print("The height of the crop is:", crop_height)

        return cube


    def measure_crop_height(self, crop_object):
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

    def resize_crop(self, crop_object, scale):
        crop_object.scale = Vector((scale, scale, scale))

    def add_weed(self, loc_x, loc_y, loc_z):
        if bool(random.getrandbits(1)):
            bpy.context.active_object.name = self.growth_stage["stage3"]
            cube = bpy.context.scene.objects.get(self.growth_stage["stage3"])
            duplicated = cube.copy()
            duplicated.data = cube.data.copy()
            loc_x = loc_x - random.uniform(-.2, .2)
            loc_y = loc_y - random.uniform(-.2, .2)
            duplicated.location = (loc_x, loc_y, loc_z)
            self.counter += 1
            bpy.context.collection.objects.link(duplicated)
            cube["segmentation_id"] = SegmentationClass.WEED.value
            return cube

    def set_crop_health(self, crop_object, health_status):
        color = self.crop_health[health_status]

        # Create a new material
        material = bpy.data.materials.new(name=f"{health_status}_Material")
        material.diffuse_color = color

        # Assign it to object
        if crop_object.data.materials:
            # assign to 1st material slot
            crop_object.data.materials[0] = material
        else:
            # no slots
            crop_object.data.materials.append(material)

