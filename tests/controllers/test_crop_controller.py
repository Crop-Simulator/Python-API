import unittest
import yaml
import os
from src.controllers.crop_controller import CropController
from src.controllers.yaml_reader import YamlReader


class BlenderScriptTest(unittest.TestCase):
    def setUp(self):
        # Set up test environment
        self.test_file = "tests/test_data.yml"
        self.test_output = "tests/test_output.png"
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


        # input_data = YamlReader().read_file(self.test_file)
        
        crop_controller = CropController(test_data, self.collection)
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
            
        # input_data = YamlReader().read_file(self.test_file)

        crop_controller = CropController(test_data, self.collection)
        material, segmentation_id = crop_controller.assign_crop_type("red")
        self.assertEquals(segmentation_id, self.expected_segmentation_id)


if __name__ == "__main__":
    unittest.main()
