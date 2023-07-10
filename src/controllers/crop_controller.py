import random
import bpy
from mathutils import Vector


class CropController:

    def __init__(self, config, collection):
        self.collection_name = collection
        self.counter = 1
        self.crop_data = config["crop"]
        self.type = self.crop_data["type"]  # list
        self.size = self.crop_data["size"]
        self.percentage_share = self.crop_data["percentage_share"]
        self.total_number = self.crop_data["total_number"]
        self.num_rows = self.crop_data["num_rows"]
        self.row_widths = self.crop_data["row_widths"]
        try:
            self.generation_seed = config["generation_seed"]
        except KeyError:
            self.generation_seed = None
        self.procedural_generation()

    def setup_crops(self):
        curr_row = 0
        curr_loc = 0
        curr_crop_type = 0
        curr_crop = 0
        num_rows = int(self.total_number / self.num_rows)
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
            crop_size = 0.5
            crop_model = self.add_crop(crop_size, loc_z, loc_x, loc_y)
            if loc_x+1 == self.row_widths:
                loc_y += 1
                loc_x = 0
            else:
                loc_x += 1
            material, segmentation_id = self.assign_crop_type(self.type[curr_crop_type])

            crop_model.active_material = material
            crop_model["segmentation_id"] = segmentation_id

            curr_crop += 1

    #TODO procedural_generation Implementation.
    def procedural_generation(self):
        random.seed(self.generation_seed)

        # print(random.random())
        # for crop in range(self.total_number):
        #     add_crop()

    def assign_crop_type(self, crop_type):
        # assign material and segmentation id depending on crop type
        material = None
        segmentation_id = 0
        if crop_type == "red":
            material = bpy.data.materials.new("Red")
            material.diffuse_color = (1, 0, 0, 0.8)
            segmentation_id = 1
        elif crop_type == "green":
            material = bpy.data.materials.new("Green")
            material.diffuse_color = (0, 1, 0, 0.8)
            segmentation_id = 2
        elif crop_type == "blue":
            material = bpy.data.materials.new("Blue")
            material.diffuse_color = (0, 0, 1, 0.8)
            segmentation_id = 3
        return material, segmentation_id

    def add_crop(self, crop_size, loc_z, loc_x, loc_y):
        # bpy.ops.mesh.primitive_cube_add(location=(locx, loc, loc), size=crop_size)

        bpy.data.collections[self.collection_name] #No sure what this does
        bpy.context.active_object.name = "stage11.1"
        cube = bpy.context.scene.objects.get("stage11.1")
        duplicated = cube.copy()
        duplicated.data = cube.data.copy()
        duplicated.location = Vector((loc_x, loc_y,loc_z))
        duplicated.scale = Vector((crop_size, crop_size, crop_size))
        self.counter += 1
        bpy.context.collection.objects.link(duplicated)

        # for ob in cube.users_collection[:]: #unlink from all preceeding object collections
        #     ob.objects.unlink(cube)
        # collection.objects.link(cube)

        # Measure the height of the crop
        crop_height = self.measure_crop_height(duplicated)
        print("The height of the crop is:", crop_height)

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
