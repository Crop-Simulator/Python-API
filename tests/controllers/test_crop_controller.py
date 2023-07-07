import unittest
import yaml
import bpy
import os
from src.controllers.crop_controller import CropController
from src.controllers.yaml_reader import YamlReader


class CameraControllerTest(unittest.TestCase):
    def setUp(self):
        # Set up test environment
        self.test_file = "tests/test_data.yml"
        self.collection = "Test Collection"
        self.expected_material_name = "Red"
        self.expected_segmentation_id = 1

    def tearDown(self):
        # Clean up test environment
        os.remove(self.test_file)

    def test_setup_crops_material_name(self):
        # Create test data YAML file
        test_data = {
            "crop": {
                "type": ["green","red","blue"],
                "size": [0.5, 0.8, 1.0],
                "percentage_share": [0.2, 0.3, 0.5],
                "total_number": 9,
                "num_rows": 2,
                "row_widths": 5,
            },
            "outfile": [self.test_output],
        }
        with open(self.test_file, "w") as file:
            yaml.safe_dump(test_data, file)


        input_data = YamlReader().read_file(self.test_file)

        crop_controller = CropController(input_data["crop"], self.collection)
        material, segmentation_id = crop_controller.assign_crop_type("red")
        self.assertEquals(material.name, self.expected_material_name)

    def test_setup_crops_material_seg_id(self):
        # Create test data YAML file
        test_data = {
            "crop": {
                "type": ["green","red","blue"],
                "size": [0.5, 0.8, 1.0],
                "percentage_share": [0.2, 0.3, 0.5],
                "total_number": 9,
                "num_rows": 2,
                "row_widths": 5,
            },
            "outfile": [self.test_output],
        }
        with open(self.test_file, "w") as file:
            yaml.safe_dump(test_data, file)

        input_data = YamlReader().read_file(self.test_file)

        crop_controller = CropController(input_data["crop"], self.collection)
        material, segmentation_id = crop_controller.assign_crop_type("red")
        self.assertEquals(segmentation_id, self.expected_segmentation_id)

    def test_setup_crops_total_number(self):
        # Checks right number of crops are created
        # Create test data YAML file
        test_data = {
            "crop": {
                "type": ["green","red","blue"],
                "size": [0.5, 0.8, 1.0],
                "percentage_share": [0.2, 0.3, 0.5],
                "total_number": 9,
                "num_rows": 2,
                "row_widths": 5,
            },
            "outfile": [self.test_output],
        }
        with open(self.test_file, "w") as file:
            yaml.safe_dump(test_data, file)

        input_data = YamlReader().read_file(self.test_file)
        crop_controller = CropController(input_data["crop"], self.collection)
        crop_controller.add_crop(0, 1, 1)
        object_count = 0
        for collection in bpy.data.collections:
            for obj in collection.all_objects:
                print("obj: ", obj.name)
                object_count += 1
        # Objects: camera, light, 1 crop and 1 original crop
        # check later
        self.assertEqual(object_count, 8)


if __name__ == "__main__":
    unittest.main()
