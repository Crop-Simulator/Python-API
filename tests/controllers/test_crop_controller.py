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
        self.expected_material_name = "stage1"
        self.expected_object_count = 10
        self.expected_segmentation_id = 9
        self.expected_stage_10_count = 2
        self.expected_stage8_count = 8

    def tearDown(self):
        # Clean up test environment
        os.remove(self.test_file)

    def test_setup_crops_material_name(self):
        # Create test data YAML file
        test_data = {
            "crop": {
                "type": ["stage10","stage9","stage8"],
                "size": [0.5, 0.8, 1.0],
                "percentage_share": [0.2, 0.3, 0.5],
                "total_number": 9,
                "num_rows": 2,
                "row_widths": 5,
            },
        }
        with open(self.test_file, "w") as file:
            yaml.safe_dump(test_data, file)


        input_data = YamlReader().read_file(self.test_file)

        crop_controller = CropController(input_data, self.collection)
        material, segmentation_id = crop_controller.assign_crop_type("stage1")
        self.assertEquals(material.name, self.expected_material_name)

    def test_setup_crops_material_seg_id(self):
        # Create test data YAML file
        test_data = {
            "crop": {
                "type": ["stage10","stage9","stage8"],
                "size": [0.5, 0.8, 1.0],
                "percentage_share": [0.2, 0.3, 0.5],
                "total_number": 9,
                "num_rows": 2,
                "row_widths": 5,
            },
        }
        with open(self.test_file, "w") as file:
            yaml.safe_dump(test_data, file)

        input_data = YamlReader().read_file(self.test_file)

        crop_controller = CropController(input_data, self.collection)
        material, segmentation_id = crop_controller.assign_crop_type("stage1")
        self.assertEquals(segmentation_id, self.expected_segmentation_id)

    def test_different_crop_types(self):
        test_data = {
            "crop": {
                "type": ["stage10","stage8"],
                "size": [0.5, 0.8],
                "percentage_share": [0.2, 0.8],
                "total_number": 10,
                "num_rows": 2,
                "row_widths": 5,
            },
        }

        with open(self.test_file, "w") as file:
            yaml.safe_dump(test_data, file)

        input_data = YamlReader().read_file(self.test_file)
        crop_controller = CropController(input_data, self.collection)
        crop_controller.setup_crops()

        stage10_count = 0
        stage8_count = 0

        # remove original models that new models were copied from
        collection1 = bpy.data.collections.get("Collection")
        for ob in bpy.context.scene.objects:
            if ob.name in ["stage10.009", "stage8.009"]:
                duplicate = collection1.objects.get(ob.name)
                collection1.objects.unlink(duplicate)

        for collection in bpy.data.collections:
            for obj in collection.all_objects:
                if "stage10" in obj.name:
                    stage10_count += 1
                if "stage8" in obj.name:
                    stage8_count += 1


        self.assertTrue(stage10_count == self.expected_stage_10_count and stage8_count == self.expected_stage8_count)



if __name__ == "__main__":
    unittest.main()
