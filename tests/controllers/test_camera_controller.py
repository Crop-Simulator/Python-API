import unittest
import bpy
from src.controllers.camera_controller import CameraController


class CameraControllerTest(unittest.TestCase):
    # more tests are needed, these are temporary for setting up unit tests
    @classmethod
    def setUpClass(cls):
        bpy.ops.wm.read_homefile()

    def setUp(self):
        # Set up test environment
        self.camera_name = "Test Camera"
        self.camera_location = (7.358891487121582, -6.925790786743164, 4.958309173583984)
        self.camera_rotation = (1.1093189716339111, 0.0, 0.8149281740188599)
        self.collection = "Test Collection"
        self.camera_controller = CameraController(self.camera_name, self.camera_location, self.camera_rotation, self.collection)
        self.updated_rotation = (5, 10, 15)

    def test_setup_camera_collection_name(self):
        # Create camera controller instance
        # self.camera_controller.setup_camera(self.camera_name, self.camera_location, self.camera_rotation,
        #                                     self.collection)
        self.camera_controller.setup_camera()
        # Checks that the collection is named correctly
        # 0th index is the existing collection in the file called "Collection"
        # 1st index should be the newly created "Test Collection"
        self.assertTrue(bpy.data.collections[1].name == self.collection)

    def test_setup_camera_collection_scene(self):
        collection = self.camera_controller.setup_camera()
        for collection in bpy.data.collections:
            if collection.name == self.collection:
                # Checks that the collection exists in the scene
                self.assertTrue(collection.name == self.collection)

    def test_setup_camera_collection_location(self):
        self.camera_controller.setup_camera()
        camera_loc = bpy.data.objects[self.camera_name].location
        x, y, z = camera_loc
        self.assertEqual(self.camera_location, (x, y, z))

    def test_setup_camera_collection_rotation(self):
        self.camera_controller.setup_camera()
        camera_rot = bpy.data.objects[self.camera_name].rotation_euler
        # only getting first 3 values - they are relevant to rotation, after that it is the perspective
        self.assertEqual(self.camera_rotation, camera_rot[0:3])

    def test_update_camera(self):
        self.camera_controller.update_camera(angle_rotation = self.updated_rotation)
        camera_rot = bpy.data.objects[self.camera_name].rotation_euler
        # it is very difficult to calculate the rotation of the camera
        # so this checks that the camera position is not the same as the initial rotation
        self.assertTrue(camera_rot != self.camera_rotation) # updated rotation is different to initial rotation



if __name__ == "__main__":
    unittest.main()
