import unittest
import bpy
import mathutils
from mathutils import Vector

from src.controllers.light_controller import LightController

class LightControllerTest(unittest.TestCase):
    # TODO: fix infinite build on GitHub Actions
    def setUp(self):
        # Set up test environment
        self.light_position = (10, 5, 0)
        self.expected_light_position = Vector((10.0, 5.0, 0.0))
        self.expected_sky_texture = "Sky Texture"
        self.initial_sky_type = "PREETHAM"
        self.changed_sky_type = "HOSEK_WILKIE"
        self.changed_sun_direction = mathutils.Vector((1.0, 0.0, 1.0))

    def test_add_light(self):
        light_controller = LightController()
        light_controller.add_light()

        get_position = bpy.context.object.matrix_world.to_translation()

        # Verify that the output file was created
        self.assertEqual(get_position, self.expected_light_position)
        
    def test_add_sky(self):
        light_controller = LightController()
        light_controller.add_sky()
        get_texture = bpy.context.scene.world.node_tree.nodes[self.expected_sky_texture]
        self.assertTrue(get_texture)
        
    def test_change_sky_type(self):
        light_controller = LightController()
        get_sky_type = bpy.context.scene.world.node_tree.nodes[self.expected_sky_texture].sky_type
        self.assertEqual(get_sky_type, self.initial_sky_type)
        light_controller.change_sky_type(self.changed_sky_type)
        get_sky_type = bpy.context.scene.world.node_tree.nodes[self.expected_sky_texture].sky_type
        self.assertTrue(get_sky_type, self.changed_sky_type)

if __name__ == "__main__":
    unittest.main()
