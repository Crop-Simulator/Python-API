import random
import bpy
import os

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
            "stage1" : "stage1.009"
        }
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
            crop_model = self.add_crop(crop_size, self.growth_stage[self.type[curr_crop_type]],loc_z, loc_x, loc_y)
            if loc_x+1 == self.row_widths:
                loc_y += 1
                loc_x = 0
            else:
                loc_x += 1
            material, segmentation_id = self.assign_crop_type(self.type[curr_crop_type])

            # crop_model.active_material = material
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
        if crop_type == "stage10":
            material = bpy.data.materials.new("Red")
            segmentation_id = 1
        elif crop_type == "stage9":
            material = bpy.data.materials.new("Green")
            segmentation_id = 2
        elif crop_type == "stage7":
            material = bpy.data.materials.new("Blue")
            segmentation_id = 3
        # material.use_nodes = True
        # bsdf = material.node_tree.nodes["Principled BSDF"]
        # cwd = os.getcwd()
        # texture_image = material.node_tree.nodes.new("ShaderNodeTexImage")
        # texture_image.image = bpy.data.images.load(cwd+"\\src\\blender_assets\\textures\\textures\\texture5.jpg")
        # material.node_tree.links.new(bsdf.inputs["Base Color"], texture_image.outputs["Color"])
        return material, segmentation_id

    def add_crop(self, crop_size, growth_stage, loc_z, loc_x, loc_y):
        # bpy.ops.mesh.primitive_cube_add(location=(locx, loc, loc), size=crop_size)

        bpy.data.collections[self.collection_name] #No sure what this does
        bpy.context.active_object.name = growth_stage
        cube = bpy.context.scene.objects.get(growth_stage)
        duplicated = cube.copy()
        duplicated.data = cube.data.copy()
        duplicated.location = (loc_x, loc_y, loc_z)
        self.counter += 1
        bpy.context.collection.objects.link(duplicated)
        return cube
