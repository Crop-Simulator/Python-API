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

    def update_camera(self, angle_rotation = (0, 0, 0), distance = 10.0, camera_angles = (0, 0, 0)):

        # update camera rotation and distance around object
        camera_object = bpy.data.objects[self.camera_name]
        camera_direction = camera_object.location - mathutils.Vector(angle_rotation)
        rotation = camera_direction.to_track_quat("Z", "Y")

        camera_object.rotation_euler = rotation.to_euler()
        camera_object.location = rotation @ mathutils.Vector((0,0, distance))

        # update camera angles in place
        camera_object.rotation_mode = "XYZ"

        pi = math.pi
        x = camera_angles[0] * pi / 180
        y = camera_angles[1] * pi / 180
        z = camera_angles[2] * pi / 180

        scene = bpy.context.scene
        scene.camera.rotation_euler[0] = x
        scene.camera.rotation_euler[1] = y
        scene.camera.rotation_euler[2] = z

