import bpy
import math

class CameraController:
    # """
    # Setup default camera angle and link it to a collection.
    # """
    # def setup_camera(self, cam="camera_one", camera_location=(10,5,0),
    #                  camera_rotation=(1.57057,0.00174533,1.57057), collection_name="Collection"):
    #     bpy.ops.object.camera_add(enter_editmode=False, align="VIEW",
    #                               location=camera_location, rotation=camera_rotation)
    #     print("getting to render")

    #     bpy.data.objects["Camera"].name = str(cam)
    #     bpy.data.objects[cam].data.lens_unit = "FOV"
    #     bpy.data.objects[cam].data.angle = math.radians(100) # distance of camera from the scene
    #     collection = bpy.data.collections.new(name=collection_name)
    #     bpy.context.scene.collection.children.link(collection)     # link to the collection containing the crops
    #     return collection
    def setup_camera(self, cam="camera_one", camera_location=(10,5,0),
                     camera_rotation=(1.57057,0.00174533,1.57057), collection_name="Collection"):
        bpy.ops.object.camera_add(enter_editmode=False, align="VIEW",
                                  location=camera_location, rotation=camera_rotation)
        print("getting to render")

        bpy.data.objects["Camera"].name = str(cam)
        bpy.data.objects[cam].data.lens_unit = "FOV"
        bpy.data.objects[cam].data.angle = math.radians(100) # distance of camera from the scene
        collection = bpy.data.collections.new(name=collection_name)
        bpy.context.scene.collection.children.link(collection)     # link to the collection containing the crops
        return collection
    