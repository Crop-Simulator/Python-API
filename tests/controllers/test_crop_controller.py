import unittest
import yaml
import os
from src.controllers.crop_controller import CropController


class BlenderScriptTest(unittest.TestCase):
    def setUp(self):
        # Set up test environment
        self.test_file = "tests/test_data.yml"
        self.test_output = "tests/expected_output.png"
        self.collection = "Test Collection"
        self.expected_output_file = os.getcwd() + "/" + self.test_output
        self.expected_material_name = "Red.001"
        self.expected_material_color = (1,0,0,0.8)
        self.expected_segmentation_id = 1



    def tearDown(self):
        # Clean up test environment
        os.remove(self.test_file)
        # os.remove(self.expected_output_file)
        # os.remove("tests/expected_output_seg.png")

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
        }
        with open(self.test_file, "w") as file:
            yaml.safe_dump(test_data, file)

        crop_controller = CropController(self.test_file, self.collection)
        material, segmentation_id = crop_controller.assign_crop_type("red")
        print(material.name)
        self.assertEquals(material.name, self.expected_material_name)

    def test_setup_crops_material_colour(self):
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
        }
        with open(self.test_file, "w") as file:
            yaml.safe_dump(test_data, file)

        crop_controller = CropController(self.test_file, self.collection)
        material, segmentation_id = crop_controller.assign_crop_type("red")
        self.assertEquals(segmentation_id, self.expected_segmentation_id)





if __name__ == "__main__":
    unittest.main()
