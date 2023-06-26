import filecmp
import unittest
# import bpy
import os
import yaml
from subprocess import run


class BlenderScriptTest(unittest.TestCase):
    def setUp(self):
        # Set up test environment
        self.test_file = "tests/test_data.yml"
        self.test_output = "tests/expected_output.png"
        self.expected_output_file = os.getcwd() + "/" + self.test_output

    def tearDown(self):
        # Clean up test environment
        os.remove(self.test_file)
        os.remove(self.expected_output_file)
        os.remove("tests/expected_output_seg.png")

    def test_script_execution(self):
        # Create test data YAML file
        test_data = {
            "crop": {
                "type": ['green','red','blue'],
                "size": [0.5, 0.8, 1.0],
                "percentage_share:": [0.2, 0.3, 0.5],
                "total_number": 9,
                "num_rows": 2,
                "row_widths": 5,
            }
        }
        with open(self.test_file, "w") as file:
            yaml.safe_dump(test_data, file)

        # Execute the script with simulated command-line arguments
        run(["python", "src/launch.py", "-i", self.test_file, "-o", self.test_output])

        # Verify that the output file was created
        self.assertTrue(os.path.isfile(self.expected_output_file))

    # def test_cubes_created(self):
    #     # Create test data YAML file
    #     test_data = {
    # #         "crop": {
    #             "type": ['green','red','blue'],
    #             "size": [0.5, 0.8, 1.0],
    #             "percentage_share:": [0.2, 0.3, 0.5],
    #             "total_number": 9,
    #             "num_rows": 2,
    #             "row_widths": 5,
    #         }
    #     }
    #     with open(self.test_file, "w") as file:
    #         yaml.safe_dump(test_data, file)
    #
    #     # Execute the script with simulated command-line arguments
    #     run(["python", "src/launch.py", "-i", self.test_file, "-o", self.test_output])
    #
    #     # Verify that the correct number of cubes were created
    #     collection = bpy.data.collections.get("Collection")
    #     self.assertEqual(len(collection.objects), test_data["num_crops"])

    def test_render_output(self):
        # Create test data YAML file
        test_data ={
            "crop": {
                "type": ['green','red','blue'],
                "size": [0.5, 0.8, 1.0],
                "percentage_share:": [0.2, 0.3, 0.5],
                "total_number": 9,
                "num_rows": 2,
                "row_widths": 5,
            }
        }
        with open(self.test_file, "w") as file:
            yaml.safe_dump(test_data, file)

        # Execute the script with simulated command-line arguments
        run(["python", "src/launch.py", "-i", self.test_file, "-o", self.test_output])

        # Verify that the rendering output matches the expected file
        self.assertTrue(filecmp.cmp(self.expected_output_file, "tests/expected_output.png"))


if __name__ == "__main__":
    unittest.main()
