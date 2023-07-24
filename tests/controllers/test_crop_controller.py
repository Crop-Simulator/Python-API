import unittest
import yaml
import bpy
import os
from src.controllers.crop_controller import CropController
from src.controllers.segmentation import SegmentationClass
from src.controllers.yaml_reader import YamlReader


class CameraControllerTest(unittest.TestCase):
    def setUp(self):
        # Set up test environment
        self.test_file = "tests/test_data.yml"
        self.collection = "Collection"
        self.expected_object_count = 10
        self.expected_segmentation_id = SegmentationClass.PLANT.value
        self.expected_stage_10_crops_num = 2
        self.expected_stage_8_crops_num = 8
        self.expected_material_name = ["stage1", "stage2", "stage3", "stage4", "stage5",
                                       "stage6", "stage7", "stage8", "stage9", "stage10"]
        self.num_crops_per_stage = {
            "stage10": 0,
            "stage8": 0,
        }

    def tearDown(self):
        # Clean up test environment
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_setup_crops_material_name(self):
        # Create test data YAML file
        test_data = {
            "crop": {
                "type": ["stage10", "stage9", "stage8"],
                "size": [0.5, 0.8, 1.0],
                "percentage_share": [0.2, 0.3, 0.5],
                "total_number": 9,
                "num_rows": 2,
                "row_widths": 5,
            },
            "resolution": {
                "x": 512,
                "y": 512,
        },
        }
        with open(self.test_file, "w") as file:
            yaml.safe_dump(test_data, file)

        input_data = YamlReader().read_file(self.test_file)
        crop_controller = CropController(input_data, self.collection)
        for i in range(1, 11):
            stage = "stage" + str(i)
            material, segmentation_id = crop_controller.assign_crop_type(stage)
            self.assertEqual(material.name, self.expected_material_name[i - 1])

    def test_setup_crops_material_seg_id(self):
        # Create test data YAML file
        test_data = {
            "crop": {
                "type": ["stage10", "stage9", "stage8"],
                "size": [0.5, 0.8, 1.0],
                "percentage_share": [0.2, 0.3, 0.5],
                "total_number": 9,
                "num_rows": 2,
                "row_widths": 5,
            },
            "resolution": {
                "x": 512,
                "y": 512,
        },
        }
        with open(self.test_file, "w") as file:
            yaml.safe_dump(test_data, file)

        input_data = YamlReader().read_file(self.test_file)

        crop_controller = CropController(input_data, self.collection)
        for i in range(1, 11):
            stage = "stage" + str(i)
            material, segmentation_id = crop_controller.assign_crop_type(stage)
            self.assertEqual(segmentation_id, self.expected_segmentation_id)

    def test_stage_crop_num_correct(self):
        test_data = {
            "crop": {
                "type": ["stage10", "stage8"],
                "size": [0.5, 0.8],
                "percentage_share": [0.2, 0.8],
                "total_number": 10,
                "num_rows": 2,
                "row_widths": 5,
            },
            "resolution": {
                "x": 512,
                "y": 512,
        },
        }

        with open(self.test_file, "w") as file:
            yaml.safe_dump(test_data, file)

        input_data = YamlReader().read_file(self.test_file)
        crop_controller = CropController(input_data, self.collection)
        crop_controller.setup_crops()

        for collection in bpy.data.collections:
            for obj in collection.all_objects:
                obj_name = obj.name.split(".", 1)[0]
                if obj_name in self.num_crops_per_stage.keys():
                    self.num_crops_per_stage[obj_name] += 1

        self.assertTrue(self.num_crops_per_stage["stage10"] == self.expected_stage_10_crops_num)
        self.assertTrue(self.num_crops_per_stage["stage8"] == self.expected_stage_8_crops_num)


if __name__ == "__main__":
    unittest.main()
