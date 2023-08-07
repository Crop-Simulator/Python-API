import bpy
import math
import mathutils

class CameraController:
    def __init__(self, camera_name, camera_location, camera_rotation, collection_name):
        self.camera_location = camera_location
        self.camera_rotation = camera_rotation
        self.collection_name = collection_name
        self.camera_name = camera_name
        self.camera = bpy.ops.object.camera_add(enter_editmode=False, align="VIEW",
                                  location=self.camera_location, rotation=self.camera_rotation)
    """
    Setup default camera angle and link it to a collection.
    """
    def setup_camera(self):
        self.camera = bpy.ops.object.camera_add(enter_editmode=False, align="VIEW",
                                  location=self.camera_location, rotation=self.camera_rotation)
        scene = bpy.context.scene
        bpy.data.objects["Camera"].name = str(self.camera_name)
        bpy.data.objects[self.camera_name].data.lens_unit = "FOV"
        bpy.data.objects[self.camera_name].data.angle = math.radians(100) # distance of camera from the scene
        collection = bpy.data.collections.new(name=self.collection_name)
        bpy.context.scene.collection.children.link(collection)     # link to the collection containing the crops

        scene.camera = bpy.context.object
        return collection

    def update_camera(self, angle_rotation = (0, 0, 0), distance = 10.0):
        # update camera rotation and distance
        camera_direction = bpy.data.objects[self.camera_name].location - mathutils.Vector(angle_rotation)
        rotation = camera_direction.to_track_quat("Z", "Y")
        bpy.data.objects[self.camera_name].rotation_euler = rotation.to_euler()
        bpy.data.objects[self.camera_name].location = rotation @ mathutils.Vector((0, 0, distance))
