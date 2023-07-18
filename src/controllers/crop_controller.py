import random
import bpy

from mathutils import Vector

import os

from .segmentation import SegmentationClass

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
            crop_size = 0.5
            crop_model = self.add_crop(crop_size, loc_z, loc_x, loc_y)
            #TODO Uncomment when different types of objects are able to be added
            # self.add_weed(loc_x, loc_y, loc_z)
            if loc_x + 1 == self.row_widths:
                loc_y += 1
                loc_x = 0
            else:
                loc_x += 1
            material, segmentation_id = self.assign_crop_type(self.type[curr_crop_type])

            # crop_model.active_material = material
            crop_model["segmentation_id"] = segmentation_id

            curr_crop += 1

    # TODO procedural_generation Implementation.
    def procedural_generation(self):
        random.seed(self.generation_seed)

    def assign_crop_type(self, crop_type):
        # assign material and segmentation id depending on crop type
        material = None
        segmentation_id = 0
        if crop_type == "red":
            material = bpy.data.materials.new("Red")
            segmentation_id = SegmentationClass.PLANT.value
        elif crop_type == "green":
            material = bpy.data.materials.new("Green")
            segmentation_id = SegmentationClass.PLANT.value
        elif crop_type == "blue":
            material = bpy.data.materials.new("Blue")
            segmentation_id = SegmentationClass.PLANT.value
        material.use_nodes = True
        bsdf = material.node_tree.nodes["Principled BSDF"]
        cwd = os.getcwd()
        texture_image = material.node_tree.nodes.new("ShaderNodeTexImage")
        texture_image.image = bpy.data.images.load(cwd+"\\src\\blender_assets\\textures\\textures\\texture5.jpg")
        material.node_tree.links.new(bsdf.inputs["Base Color"], texture_image.outputs["Color"])
        return material, segmentation_id

    def add_crop(self, crop_size, loc_z, loc_x, loc_y):
        bpy.context.active_object.name = "stage11.1"
        cube = bpy.context.scene.objects.get("stage11.1")
        duplicated = cube.copy()
        duplicated.data = cube.data.copy()

        duplicated.location = Vector((loc_x, loc_y,loc_z))
        duplicated.scale = Vector((crop_size, crop_size, crop_size))

        loc_x = loc_x - random.uniform(-.2, .2)
        loc_y = loc_y - random.uniform(-.2, .2)
        duplicated.location = (loc_x, loc_y, loc_z)

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
            bpy.context.active_object.name = "BagaPie_Grass_00"
            cube = bpy.context.scene.objects.get("BagaPie_Grass_00")
            duplicated = cube.copy()
            duplicated.data = cube.data.copy()
            loc_x = loc_x - random.uniform(-.2, .2)
            loc_y = loc_y - random.uniform(-.2, .2)
            duplicated.location = (loc_x, loc_y, loc_z)
            self.counter += 1
            bpy.context.collection.objects.link(duplicated)
            return cube

