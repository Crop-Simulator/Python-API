import unittest
import yaml
import bpy
import os
from unittest.mock import MagicMock
from src.controllers.crop_controller import CropController
from src.controllers.segmentation import SegmentationClass
from src.controllers.yaml_reader import YamlReader


class CameraControllerTest(unittest.TestCase):
    # Set up test environment
    test_file = "tests/test_data.yml"
    test_output = "tests/expected_output.png"
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

    @classmethod
    def setUpClass(cls):
        bpy.ops.wm.read_homefile()

    @classmethod
    def tearDownClass(cls):
        # Clean up test environment
        os.remove(cls.test_file)

    def setUp(self):
        # Create test data YAML file
        with open(self.test_file, "w") as file:
            yaml.safe_dump(self.test_data, file)
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


    def test_stage_crop_num_correct(self):
        # Special changed input values compared to other tests
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

    def test_move_cursor_and_snap_selected_to_cursor(self):
        x_distance = 3.0
        y_distance = 4.0
        z_distance = 5.0

        # Create a simulated Blender context
        mock_context = MagicMock()
        mock_context.area.type = 'VIEW_3D'
        mock_context.window.scene = bpy.data.scenes[0]
        mock_context.scene.cursor.location = (0, 0, 0)
        mock_context.selected_objects = [bpy.data.objects.new("Cube", None)]

        # Create a CropController and pass in the parameters.
        input_data = YamlReader().read_file(self.test_file)
        crop_controller = CropController(input_data, "Collection")
        # Assign the simulated context to the CropController
        crop_controller.context = mock_context

        # Call methods to test the operation of moving and attaching objects
        crop_controller.move_cursor_and_snap_selected_to_cursor(x_distance, y_distance, z_distance)

        # Get the selected object and verify that its position is as expected
        for obj in mock_context.selected_objects:
            self.assertEqual(obj.location.x, x_distance)
            self.assertEqual(obj.location.y, y_distance)
            self.assertEqual(obj.location.z, z_distance)
        
    
    
    


if __name__ == "__main__":
    unittest.main()
