import unittest
import bpy
from src.controllers.camera_controller import CameraController


class BlenderScriptTest(unittest.TestCase):
    def setUp(self):
        # Set up test environment
        self.camera_name = "Test Camera"
        self.camera_location=(10,0,0)
        self.camera_rotation=(1.57057,0.00174533,1.57057)
        self.collection = "Test Collection"
        self.camera_controller = CameraController()

    def test_setup_camera_collection_name(self):
        # Create camera controller instance
        collection = self.camera_controller.setup_camera(self.camera_name, self.camera_location, self.camera_rotation, self.collection)
        # Checks that the collection is named correctly
        self.assertTrue(collection.name == self.collection)
        
    def test_setup_camera_collection_scene(self):
        for collection in bpy.data.collections:
            if collection.name == self.collection:
                # Checks that the colelction exists in the scene
                self.assertTrue(collection.name == self.collection)


if __name__ == "__main__":
    unittest.main()
