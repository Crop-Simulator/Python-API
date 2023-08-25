import random
import bpy
import copy
from .light_controller import LightController
from .ground_controller import GroundController
from src.objects.barley import Barley
from src.objects.weed import Weed
from collections import  defaultdict


class CropController:

    def __init__(self, config, collection):
        self.scene = bpy.context.scene
        self.collection = bpy.context.collection
        self.config = config
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
        self.weed_spacing = 0.2  # The bounding area value in for spacing between weed and crop
        self.weed_effect_area = 0.3  # The radius of a crop to be affected by a weed
        self.growth_stage = {
            "stage10": "stage10",
            "stage9": "stage9",
            "stage8": "stage8",
            "stage7": "stage7",
            "stage6": "stage6",
            "stage5": "stage5",
            "stage4": "stage4",
            "stage3": "stage3",
            "stage2": "stage2",
            "stage1": "stage1",
            "stage0" : "stage0",
        }
        try:
            self.generation_seed = config["generation_seed"]
        except KeyError:
            self.generation_seed = None
        self.procedural_generation_seed_setter()

    def setup_crops(self):

        # lightcon = LightController()
        # lightcon.add_light()

        # groundcon = GroundController(self.config)
        # groundcon.get_ground_stages()

        self.setup_crop_positions()

        # collection = bpy.data.collections.get(self.collection_name)
        
        # for object in bpy.data.collections:
        #     if object.name != "stage7":
        # bpy.data.collections["stage7"].CollectionChildren.link(bpy.data.collections["stage1"])
        
        # collection = bpy.context.view_layer.layer_collection.children['stage1']
        # bpy.context.view_layer.active_layer_collection = collection

        # def copy_objects(from_col, to_col, dupe_lut):
        #     for obj in from_col.objects:
        #         dupe = obj.copy()
        #         dupe.data = dupe.data.copy()
        #         to_col.objects.link(dupe)
        #         dupe_lut[obj] = dupe

        # def copy(parent, collection, new_collection_name):
        #     dupe_lut = defaultdict(lambda : None)
        #     def _copy(parent, collection):
        #         new_collection = bpy.data.collections.new(new_collection_name)
        #         copy_objects(collection, new_collection, dupe_lut)

        #         for c in collection.children:
        #             _copy(new_collection, c)

        #         parent.children.link(new_collection)
            
        #     _copy(parent, collection)
        #     print(dupe_lut)
        #     for obj, dupe in tuple(dupe_lut.items()):
        #         parent = dupe_lut[obj.parent]
        #         if parent:
        #             dupe.parent = parent
                    
        # context = bpy.context
        # scene = context.scene
        # col = context.collection

        # copy(scene.collection, col, "new_stage1")
        # for collection in bpy.data.collections:
        #     print(collection.name)
            
        # for obj in bpy.data.collections["stage1"].objects:
        #     obj.location = (0,0,0)
        # for obj in bpy.data.collections["new_stage1"].objects:
        #     obj.location = (0,1,0)
        # bpy.context.view_layer.active_layer_collection = layer_collection.children[-1]
        # print("ACTIVE COLLECTIOn", bpy.context.view_layer.active_layer_collection.name) 

        
        # print("ACTIVE COLLECTIOn", bpy.context.view_layer.active_layer_collection.name)

        
        # bpy.context.scene.collection.children.link(duplicate)
        print(bpy.context.collection)
        # for object in bpy.data.collections["stage7"].objects:
        #     print(object.name)
            
        for object in bpy.context.collection.objects:
            print(object.name)
                
        for collection in bpy.data.collections:
            if collection.name in self.growth_stage.values():
                print("hi")
                # bpy.context.view_layer.layer_collection.children.get(collection.name).hide_viewport = True
                bpy.data.collections.remove(collection)

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

            i = crop % 11
                
            crop_model = self.add_crop(self.crop_type[curr_crop_type], location, 6)
            self.all_crops.append(crop_model)  # add crop objects to manipulate later
            self.add_weed(location)

            if curr_row + 1 >= self.number_of_rows:
                location[1] += 1 / self.crop_data["density"]
                location[0] = 0
            else:
                location[0] += self.row_widths / self.crop_data["density"]
            curr_crop += 1
            curr_row += 1

    def procedural_generation_seed_setter(self):
        random.seed(self.generation_seed)

    def add_crop(self, crop_type, loc, stage):
        crop = None
        if crop_type == "barley":
            crop = Barley(stage, "healthy")
        loc[0] = loc[0] - random.uniform(-.5, .5)
        loc[1] = loc[1] - random.uniform(-.5, .5)
        crop.set_location([loc[0], loc[1], loc[2]])
        self.counter += 1
        self.all_crops.append(crop) # add crop objects to manipulate later
        self.all_plants.append(crop)
        return crop

    def add_weed(self, loc):
        if bool(random.getrandbits(1)):
            weed = Weed()
            loc[0] = loc[0] - random.uniform(-self.weed_spacing, self.weed_spacing)
            loc[1] = loc[1] - random.uniform(-self.weed_spacing, self.weed_spacing)
            weed.set_location([loc[0], loc[1], loc[2]])
            bpy.context.collection.objects.link(weed.weed_object)
            self.all_plants.append(weed) # add objects to manipulate later
            self.populate_area_weeds(weed)
            return weed
        return False

    # If X of weed is within X of crop weed radius and Y of weed is within Y of crop weed radius then add it to the crop
    def populate_area_weeds(self, weed):
        for crop in self.all_crops:
            if ((crop.get_location()[0] + self.weed_effect_area < weed.get_location()[0]) >
                    crop.get_location()[0] - self.weed_effect_area and
                    crop.get_location()[1] + self.weed_effect_area < weed.get_location()[1] >
                    crop.get_location()[1] - self.weed_effect_area):
                crop.add_weed(weed)
