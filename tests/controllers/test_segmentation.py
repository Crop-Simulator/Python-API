import unittest
import bpy
import os
import cv2
import yaml
from subprocess import run

from src.controllers.segmentation import Segmentation

class SegmentationTest(unittest.TestCase):
    """
    This class contains unit tests for the Segmentation class.
    """

        # Set up test environment
    test_file = "tests/test_data.yml"
    test_output = "tests/expected_output.png"
    expected_output_file = os.getcwd() + "/" + test_output
    test_data = {
        "crop": {
            "type": ["stage10", "stage9", "stage8"],
            "size": [0.5, 0.8, 1.0],
            "percentage_share": [0.2, 0.3, 0.5],
            "total_number": 9,
            "num_rows": 2,
            "row_widths": 5,
        },
        "outfile": [test_output],
        "generation_seed": 10,
    }

    @classmethod
    def setUpClass(cls):
        # Create test data YAML file
        with open(cls.test_file, "w") as file:
            yaml.safe_dump(cls.test_data, file)

        # Execute the script with simulated command-line arguments
        run(["python", "src/launch.py", cls.test_file])

    def setUp(self):
        """
        This method is called before each test method.
        It sets up the output file name for the test.
        """
        self.output_file = "test_segmentation.png"
        print("segmenation setup")

    def tearDown(self):
        """
        This method is called after each test method.
        It removes the output file created during the test.
        """
        os.remove(self.output_file)
        bpy.ops.wm.read_homefile()

    def test_segmentation(self):
        """
        This method tests the segmentation of a cube object.
        It asserts that the central point of the image is white and the background is black.
        """
        collection = bpy.data.collections.get("Collection")
        cube = collection.objects.get("Cube")
        collection.objects.unlink(cube)
        bpy.ops.mesh.primitive_cube_add()
        o = bpy.context.active_object
        o["segmentation_id"] = 1
        segmentation = Segmentation({0: [0, 0, 0], 1: [255, 255, 255]})
        segmentation_filename = self.output_file
        segmentation.segment(segmentation_filename)
        im = cv2.imread(segmentation_filename)
        print("before assertion")
        # assert the central point is the color we expect
        self.assertListEqual(im[im.shape[0] // 2, im.shape[1] // 2].tolist(), [255, 255, 255])
        # assert the background is black
        self.assertListEqual(im[0, 0].tolist(), [0, 0, 0])


if __name__ == "__main__":
    unittest.main()
