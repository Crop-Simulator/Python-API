import unittest
import bpy
import os
import yaml

from src.controllers.ground_controller import GroundController


class GroundControllerTest(unittest.TestCase):
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
        "ground_type": "loam",
    }
    @classmethod
    def setUpClass(cls):
        bpy.ops.wm.read_homefile()

    def setUp(self):
        # Create test data YAML file
        with open(self.test_file, "w") as file:
            yaml.safe_dump(self.test_data, file)
        self.config = {
            "ground_type": "loam",
            "crop": {
                "total_number": 10,
                "num_rows": 5,
                "row_widths": 2,
            },
        }
        self.controller = GroundController(self.config)

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.test_file)


    def test_get_ground_stages(self):
        bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, align="WORLD")
        plane = bpy.context.active_object
        plane.name = "ground"

        self.controller.get_ground_stages()
        obj = bpy.data.objects.get("ground")
        self.assertIsNotNone(obj, "ground object not found!")
        self.assertTrue(any(mat.name == "Texture_Material" for mat in obj.data.materials), "Texture_Material not found in ground materials!")



if __name__ == "__main__":
    unittest.main()
