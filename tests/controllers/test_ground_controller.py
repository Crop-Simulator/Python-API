import unittest
import bpy
from src.controllers.ground_controller import GroundController


class GroundControllerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, align="WORLD", location=(0, 0, 0))
        plane = bpy.context.active_object
        plane.name = "stage9.ground"

    @classmethod
    def tearDownClass(cls):
        bpy.ops.object.select_all(action="DESELECT")
        bpy.data.objects["stage9.ground"].select_set(True)
        bpy.ops.object.delete()

    def test_ground_controller(self):
        config = {
            "ground_type": "sandy",
            "crop": {
                "total_number": 10,
                "num_rows": 5,
                "row_widths": 2,
            },
        }
        ground_controller = GroundController(config)
        ground_controller.get_ground_stages()

        ground = bpy.data.objects["stage9.ground"]
        self.assertTrue(any(mat.name == "Texture_Material" for mat in ground.data.materials))




if __name__ == "__main__":
    unittest.main()
