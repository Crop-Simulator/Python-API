import unittest
import bpy
import os
import cv2

from src.controllers.segmentation import Segmentation

class SegmentationTest(unittest.TestCase):
    def setUp(self):
        self.output_file = "test_segmentation.png"

    def tearDown(self):
        os.remove(self.output_file)

    def test(self):
        collection = bpy.data.collections.get('Collection')
        cube = collection.objects.get("Cube")
        collection.objects.unlink(cube)
        bpy.ops.mesh.primitive_cube_add()
        o = bpy.context.active_object
        o["segmentation_id"] = 1
        # save a blend file
        segmentation = Segmentation({1: 0xffff})
        segmentation_filename = self.output_file
        segmentation.segment(segmentation_filename)
        im = cv2.imread(segmentation_filename)
        # assert the central point is the color we expect
        self.assertListEqual(im[im.shape[0] // 2, im.shape[1] // 2].tolist(), [255, 255, 255])
        # assert the background is black
        self.assertListEqual(im[0, 0].tolist(), [0, 0, 0])
