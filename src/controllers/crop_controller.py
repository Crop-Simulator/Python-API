import random
import bpy

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
        self.percentage_share = self.crop_data["percentage_share"]
        self.number_of_crops = self.crop_data["total_number"]
        self.number_of_rows = self.crop_data["num_rows"]
        self.row_widths = self.crop_data["row_widths"]
        self.all_crops = []
        self.all_plants = []
        self.weed_spacing = 0.1  # The bounding area value in for spacing between weed and crop
        self.weed_effect_area = 0.2  # The radius of a crop to be affected by a weed
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
            "stage0" : "stage0.009",
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
            # if not obj.name in [plants.name for plants in self.all_plants]:
            #     target = collection.objects.get(obj.name)
            #     collection.objects.unlink(target)
            #     target.hide_viewport = True
            if obj.name in self.growth_stage.values():
                target = collection.objects.get(obj.name)
                collection.objects.unlink(target)
                target.hide_viewport = True

    def setup_crop_positions(self):
        curr_row = 0
        curr_crop_type = 0
        curr_crop = 0
        location = [0, 0, 0]

        for crop in range(self.number_of_crops):
            # when the crop is divisible by the number of rows
            # add a row and reset the location
            if crop % self.number_of_rows == 0:
                curr_row += 1

            # calculate the number of crops to add based on the percentage share
            num_crops = int(self.number_of_crops * self.percentage_share[curr_crop_type])

            # when the current crop is divisible by the number of crops
            # reset the crop type
            if curr_crop % num_crops == 0 and crop != 0:
                curr_crop = 0
                if not curr_crop_type >= len(self.crop_type) - 1:
                    curr_crop_type += 1

            # add the crop to the scene
            self.add_crop(self.crop_type[curr_crop_type], location)
            self.add_weed(location)
            # when the location is at the end of the row
            # add a row and reset the location
            if location[0] + 1 >= self.number_of_rows:
                location[1] += 1 # next row
                location[0] = 0
            else:
                location[0] += self.row_widths

            curr_crop += 1

    def procedural_generation(self):
        random.seed(self.generation_seed)

    def add_crop(self, crop_type, loc):
        if crop_type == "barley":
            barley = Barley(7, "healthy")
            loc[0] = loc[0] - random.uniform(-.5, .5)
            loc[1] = loc[1] - random.uniform(-.5, .5)
            barley.set_location([loc[0], loc[1], loc[2]])
        self.counter += 1
        bpy.context.collection.objects.link(barley.barley_object)
        self.all_crops.append(barley) # add crop objects to manipulate later
        self.all_plants.append(barley)
        return barley

    def add_weed(self, loc):
        # if bool(random.getrandbits(1)):
        weed = Weed()
        loc[0] = loc[0] - random.uniform(-self.weed_spacing, self.weed_spacing)
        loc[1] = loc[1] - random.uniform(-self.weed_spacing, self.weed_spacing)
        weed.set_location([loc[0], loc[1], loc[2]])
        # weed.set_location([0,0,0])
        bpy.context.collection.objects.link(weed.weed_object)
        self.all_plants.append(weed) # add objects to manipulate later
        # self.populate_area_weeds(weed)
        return weed

    # If X of weed is within X of crop weed radius and Y of weed is within Y of crop weed radius then add it to the crop
    # def populate_area_weeds(self, weed):
    #     for crop in self.all_crops:
    #         if ((crop.get_location()[0] + self.weed_effect_area < weed.get_location()[0]) >
    #                 crop.get_location()[0] - self.weed_effect_area and
    #                 crop.get_location()[1] + self.weed_effect_area < weed.get_location()[1] >
    #                 crop.get_location()[1] - self.weed_effect_area):
    #             crop.add_weed(weed)
