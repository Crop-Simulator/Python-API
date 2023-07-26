import os

import unittest
from src.machine_learning import connector

class TestConnector(unittest.TestCase):
    def setUp(self):
        self.temp_seg_file_path = "seg.tmp"

    def tearDown(self):
        # remove the temporary segmentation mask file
        if os.path.exists(self.temp_seg_file_path):
            os.remove(self.temp_seg_file_path)

    def test_read_segmentation_mask(self):
        # Test reading a segmentation mask from a file
        # Create a temporary segmentation mask file
        with open(self.temp_seg_file_path, "wb") as temp_file:
            temp_file.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
        expected_output = connector.read_segmentation_mask(self.temp_seg_file_path)
        expected_output2 = "AAAAAAAAAAAAAAAA"
        self.assertEqual(expected_output, expected_output2)

if __name__ == "__main__":
    unittest.main()
