import random
import bpy
from .ground_controller import GroundController
from src.objects.barley import Barley
from src.objects.weed import Weed
from src.machine_learning.text_prompt_manager import TextPromptManager
from src.machine_learning.text_prompt_definition import CropType, SoilType


class CropController:

    def __init__(self, config, collection):
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
        self.growth_simulator = config["growth_simulator"]
        self.days_per_stage = self.growth_simulator["days_per_stage"]
        self.all_crops = []
        self.all_plants = []
        self.crop_health = {
            "healthy": (0.2, 0.8, 0.2, 1),  # Green in RGBA
            "unhealthy": (0.6, 0.8, 0.2, 1),  # Yellow-green in RGBA
            "dead": (0.0, 0.0, 0.0, 1.0),  # Brown in RGBA
        }
        self.weed_spacing = 1 # The bounding area value in for spacing between weed and crop
        self.weed_effect_area = 0.3  # The radius of a crop to be affected by a weed
        self.growth_stage = {
            "stage10": "stage10.stand",
            "stage9": "stage9.stand",
            "stage8": "stage8.stand",
            "stage7": "stage7.stand",
            "stage6": "stage6.stand",
            "stage5": "stage5.stand",
            "stage4": "stage4.stand",
            "stage3": "stage3.stand",
            "stage2": "stage2.stand",
            "stage1": "stage1.stand",
            "stage0" : "stage0.stand",
            "ground" : "ground",
            "weed" : "weed",
        }
        try:
            self.generation_seed = config["generation_seed"]
        except KeyError:
            self.generation_seed = None
        self.procedural_generation_seed_setter()

    def setup_crops(self):
        for obj in bpy.context.scene.objects:
            if obj.name not in self.growth_stage.values():
                obj.select_set(True)
        bpy.ops.object.delete()

        groundcon = GroundController(self.config)
        groundcon.get_ground_stages()

        self.setup_crop_positions()

        collection = bpy.data.collections.get(self.collection_name)
        for obj in bpy.context.scene.objects:
            if obj.name in self.growth_stage.values():
                target = collection.objects.get(obj.name)
                collection.objects.unlink(target)


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

            stage = crop % 10

            crop_model = self.add_crop(self.crop_type[curr_crop_type], location, stage)
            self.all_crops.append(crop_model)  # add crop objects to manipulate later
            self.add_weed(location)

            if curr_row + 1 >= self.number_of_rows:
                location[1] += 1 / self.crop_data["density"]
                location[0] = 0
                curr_row = 0
            else:
                location[0] += self.row_widths / self.crop_data["density"]
            curr_crop += 1
            curr_row += 1

    def procedural_generation_seed_setter(self):
        random.seed(self.generation_seed)

    def add_crop(self, crop_type, loc, stage):
        crop = None
        if crop_type == "barley":
            crop = Barley(8, "healthy")
            # growth_manager = GrowthManager(self.config, crop, self.days_per_stage)
            # planting_date = self.config["planting_date"]
            # lat = self.config["latitude"]
            # lon = self.config["longitude"]
            # barley_type = self.config["barley_type"]
            # api_key = os.environ["WEATHER_API"]
            # weather_controller = WeatherController(api_key)
            # weather_data = weather_controller.get_merged_weather_data(barley_type, planting_date, lat, lon)
            # health_status = growth_manager.evaluate_plant_health(weather_data)
            # crop.set_color(self.crop_health[health_status])
        loc[0] = loc[0] - random.uniform(-.5, .5)
        loc[1] = loc[1] - random.uniform(-.5, .5)
        crop.set_location([loc[0], loc[1], loc[2]])
        self.counter += 1
        bpy.context.collection.objects.link(crop.barley_object)
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

    def update_text_prompt_manager(self, manager: TextPromptManager):

        for crop in CropType:
            if str(crop) == self.crop_type[0]:
                manager.crop_type = crop

        for soil in SoilType:
            if str(soil) == self.config["ground_type"]:
                manager.soil_type = soil
