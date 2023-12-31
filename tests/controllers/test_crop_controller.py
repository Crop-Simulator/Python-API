import unittest
import yaml
import bpy
import os

from src.controllers.crop_controller import CropController
from src.controllers.segmentation import SegmentationClass
from src.controllers.yaml_reader import YamlReader


class CropControllerTest(unittest.TestCase):
    # Set up test environment
    test_file = "tests/test_data.yml"
    test_output = "tests/expected_output.png"
    test_data = {
        "crop": {
            "type": ["barley"],
            "percentage_share": [1.0],
            "total_number": 9,
            "num_rows": 2,
            "row_widths": 5,
            "density": 1,
            "barley_position_randomness": 0.4,
        },
        "weed_likelihood": 1.0,
        "resolution": {
            "x": 512,
            "y": 512,
        },
        "ground_type": "loam",
        "growth_simulator": {
            "days_per_render": 5,
            "days_per_stage": 30,
            "p_progression": 0.8,
            "p_death": 0.1,
            "growth_coefficient": 0.1,
            "gdd": 1,
            "gdd_coefficient": 1,
            "effect_of_irradiance": 0.1,
            "effect_of_temperature": 0.1,
            "effect_of_precipitation": 0.1,
            "maximum_temperature": 40,
            "minimum_temperature": 0,
            "effect_of_weeds": 0.1,
        },
        "planting_date": "2023-02-01",
        "latitude": 35.6895,
        "longitude": 139.6917,
        "barley_type": "spring",
    }

    @classmethod
    def setUpClass(cls):
        bpy.ops.wm.read_homefile(filepath="src/blender_assets/CropAssets.blend")

    @classmethod
    def tearDownClass(cls):
        # Clean up test environment
        os.remove(cls.test_file)

    def setUp(self):
        bpy.ops.wm.read_homefile(filepath="src/blender_assets/CropAssets.blend")
        # Create test data YAML file
        with open(self.test_file, "w") as file:
            yaml.safe_dump(self.test_data, file)
        self.input_data = YamlReader().read_file(self.test_file)
        self.collection = "Collection"
        self.expected_object_count = 10
        self.expected_segmentation_id = SegmentationClass.PLANT.value
        self.expected_stage_10_crops_num = 2
        self.expected_stage_8_crops_num = 8
        self.expected_weed_list = []
        self.expected_material_name = ["stage1", "stage2", "stage3", "stage4", "stage5",
                                       "stage6", "stage7", "stage8", "stage9", "stage10"]

    def test_add_weed_within_effect_area(self):
        test_controller = CropController(self.input_data, self.collection)
        test_controller.setup_crops()
        for crops in test_controller.all_crops:
            self.expected_weed_list.append(crops.get_weeds())
        self.assertTrue(any(self.expected_weed_list))


if __name__ == "__main__":
    unittest.main()
