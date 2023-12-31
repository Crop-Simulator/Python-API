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
    expected_output_file = os.getcwd() + "/" + test_directory + "/" + test_output + "0rendered_day0.png"
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
        "output" : {
            "num_images_per_day": 1,
            "directory" : test_directory,
            "file_name": test_output,
            "brightness": 0.5,
            "camera_angles": ["top_down"],

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
        "growth_simulator": {
            "days_per_render": 1,
            "total_days": 1,
            "days_per_stage": 30,
            "p_progression": 0.8,
            "p_death": 0.1,
            "growth_coefficient": 0.1,
            "gdd_coefficient": 1,
            "effect_of_irradiance": 0.1,
            "effect_of_temperature": 0.1,
            "effect_of_precipitation": 0.1,
            "maximum_temperature": 40,
            "minimum_temperature": 0,
            "effect_of_weeds": 0.1,
            "gdd": 1,
        },
    }

    @classmethod
    def setUpClass(cls):
        # Create test data YAML file
        with open(cls.test_file, "w") as file:
            yaml.safe_dump(cls.test_data, file)

        # Execute the script with simulated command-line arguments
        root_dir =  Path(__file__).parent.parent
        run(["poetry", "run", "python", "src/launch.py", cls.test_file], cwd = root_dir, check=True)

    @classmethod
    def tearDownClass(cls):
        # Clean up test environment
        os.remove(cls.test_file)
        os.remove(cls.expected_output_file)
        os.remove("tests/expected_output0rendered_day0_seg.png")
        os.remove("tests/expected_output0rendered_day0_depth.png")

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
        self.assertTrue(filecmp.cmp(self.expected_output_file, "tests/expected_output0rendered_day0.png"))


if __name__ == "__main__":
    unittest.main()
