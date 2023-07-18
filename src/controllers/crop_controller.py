import random
import bpy


class CropController:

    def __init__(self, config, collection):
        self.collection_name = collection
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
            crop_model = self.add_crop(self.growth_stage[self.type[curr_crop_type]],loc_z, loc_x, loc_y)
            if loc_x+1 == self.row_widths:
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
        segmentation_id = list(self.growth_stage.keys()).index(crop_type) + 1

        return material, segmentation_id

    def add_crop(self, growth_stage, loc_z, loc_x, loc_y):
        bpy.context.active_object.name = growth_stage
        cube = bpy.context.scene.objects.get(growth_stage)
        duplicated = cube.copy()
        duplicated.data = cube.data.copy()
        loc_x = loc_x - random.uniform(-.2, .2)
        loc_y = loc_y - random.uniform(-.2, .2)
        duplicated.location = (loc_x, loc_y, loc_z)
        self.counter += 1
        bpy.context.collection.objects.link(duplicated)
        return cube

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
            return cube
