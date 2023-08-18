import filecmp
import unittest
import bpy
import os
import yaml
from pathlib import Path

from subprocess import run

class BlenderScriptTest(unittest.TestCase):
    # Set up test environment
    test_file = "test_data.yml"
    test_output = "expected_output"
    test_directory = "tests"
    expected_output_file = os.getcwd() + "/" + test_directory + "/" + test_output + "0.png"
    test_data = {
        "crop": {
            "type": ["stage10", "stage9", "stage8"],
            "size": [0.5, 0.8, 1.0],
            "percentage_share": [0.2, 0.3, 0.5],
            "total_number": 9,
            "num_rows": 2,
            "row_widths": 5,
            "density": 1,
        },
        "output" : {
            "num_images": 1,
            "directory" : test_directory,
            "file_name": test_output,
            "camera_angle": "top_down"
            
        },
        "planting_date": "2023-02-01",
        "latitude": 35.6895,
        "longitude": 139.6917,
        "barley_type": "spring",
        "generation_seed": 10,
        "resolution": {
            "x": 512,
            "y": 512,
        },
        "ground_type": "loam",
    }

    @classmethod
    def setUpClass(cls):
        # Create test data YAML file
        with open(cls.test_file, "w") as file:
            yaml.safe_dump(cls.test_data, file)

        # Execute the script with simulated command-line arguments
        root_dir =  Path(__file__).parent.parent
        run(["poetry", "run", "python", "src/launch.py", cls.test_file], cwd = root_dir)

    @classmethod
    def tearDownClass(cls):
        # Clean up test environment
        os.remove(cls.test_file)
        os.remove(cls.expected_output_file)
        os.remove("tests/expected_output0_seg.png")

    def test_unit_system_metric(self):
        # Check if the unit system is now set to metric
        self.assertEqual(bpy.context.scene.unit_settings.system, "METRIC")

    def test_scale_length_one(self):
        # Check if the scale length is set to 1.0
        self.assertEqual(bpy.context.scene.unit_settings.scale_length, 1.0)

    def test_script_execution(self):
        # Verify that the output file was created
        self.assertTrue(os.path.isfile(self.expected_output_file))

    def test_render_output(self):
        # Verify that the rendering output matches the expected file
        self.assertTrue(filecmp.cmp(self.expected_output_file, "tests/expected_output0.png"))


if __name__ == "__main__":
    unittest.main()
