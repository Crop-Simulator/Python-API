import random
import bpy
import math

from .light_controller import LightController
from src.objects.barley import Barley
from src.objects.weed import Weed


class CropController:

    def __init__(self, config, collection):
        self.collection_name = collection
        self.crop_size = 0.5
        self.counter = 1
        self.crop_data = config["crop"]
        self.crop_type = self.crop_data["type"]
        self.crop_size = self.crop_data["size"]
        self.percentage_share = self.crop_data["percentage_share"]
        self.number_of_crops = self.crop_data["total_number"]
        self.number_of_rows = self.crop_data["num_rows"]
        self.row_widths = self.crop_data["row_widths"]
        self.all_crops = []
        self.weed_spacing = .2  # The bounding area value in for spacing between weed and crop
        self.weed_effect_area = 0.3  # The radius of a crop to be affected by a weed
        self.growth_stage = {
            "stage10": "stage10.009",
            "stage9": "stage9.009",
            "stage8": "stage8.009",
            "stage7": "stage7.009",
            "stage6": "stage6.009",
            "stage5": "stage5.009",
            "stage4": "stage4.009",
            "stage3": "stage3.009",
            "stage2": "stage2.009",
            "stage1": "stage1.009",
        }
        try:
            self.generation_seed = config["generation_seed"]
        except KeyError:
            self.generation_seed = None
        self.procedural_generation()

    def setup_crops(self):
        for obj in bpy.context.scene.objects:
            if obj.name not in self.growth_stage.values():
                obj.select_set(True)
        bpy.ops.object.delete()

        lightcon = LightController()
        lightcon.add_light()

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
        location = [0, 0, 0]
        for crop in range(self.number_of_crops):
            if crop % self.number_of_rows == 0:
                curr_row += 1
                curr_loc = 0

            num_crops = math.ceil(self.number_of_crops * self.percentage_share[curr_crop_type])
            if curr_crop % num_crops == 0 and crop != 0:
                curr_crop = 0
                if not curr_crop_type >= len(self.crop_type) - 1:
                    curr_crop_type += 1

            curr_loc += 1
            crop_model = self.add_crop(self.crop_size, self.crop_type[curr_crop_type], location)
            self.all_crops.append(crop_model)  # add crop objects to manipulate later
            self.add_weed(location)
            if location[0] + 1 >= self.number_of_rows:
                location[1] += 1
                location[0] = 0
            else:
                location[0] += self.row_widths

            curr_crop += 1

    def procedural_generation(self):
        random.seed(self.generation_seed)

    def add_crop(self, crop_size, growth_stage, loc):
        barley = Barley(growth_stage, "healthy")
        loc[0] = loc[0] - random.uniform(-.5, .5)
        loc[1] = loc[1] - random.uniform(-.5, .5)
        barley.set_location([loc[0], loc[1], loc[2]])
        self.counter += 1
        bpy.context.collection.objects.link(barley.barley_object)
        return barley

    def add_weed(self, loc):
        if bool(random.getrandbits(1)):
            weed = Weed()
            loc[0] = loc[0] - random.uniform(-self.weed_spacing, self.weed_spacing)
            loc[1] = loc[1] - random.uniform(-self.weed_spacing, self.weed_spacing)
            weed.set_location([loc[0], loc[1], loc[2]])
            self.counter += 1
            bpy.context.collection.objects.link(weed.weed_object)
            self.populate_area_weeds(weed)
            return weed

    # If X of weed is within X of crop weed radius and Y of weed is within Y of crop weed radius then add it to the crop
    def populate_area_weeds(self, weed):
        for crop in self.all_crops:
            if ((crop.get_location()[0] + self.weed_effect_area < weed.get_location()[0]) >
                    crop.get_location()[0] - self.weed_effect_area and
                    crop.get_location()[1] + self.weed_effect_area < weed.get_location()[1] >
                    crop.get_location()[1] - self.weed_effect_area):
                crop.add_weed(weed)
