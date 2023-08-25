import bpy, bmesh
from mathutils import Vector
from collections import defaultdict


from src.controllers.segmentation import SegmentationClass
from .object_manager import ObjectManager

class Barley:
    def __init__(self, stage, health):
        self.GDD_PER_STAGE = 139
        self.counter = 0
        self.stage = stage
        self.health = health
        self.growth_stage = ["stage0", "stage1", "stage2", "stage3", "stage4",
                             "stage5", "stage6", "stage7","stage8",
                             "stage9", "stage10"]
        self.active_weeds = []
        self.crop_type = SegmentationClass.PLANT.value
        self.barley_object = self.set_model_stage(self.stage)
        # self.name = self.barley_object.name

    def set_model_stage(self, stage):
        # set collection as active collection

        collection = bpy.context.view_layer.layer_collection.children[self.growth_stage[stage]]
        bpy.context.view_layer.active_layer_collection = collection
        self.counter += 1
        
        object_manager = ObjectManager()
                    
        context = bpy.context
        object_manager.copy(context.scene.collection, context.collection)
        
        for collection in bpy.data.collections:
            print(collection.name)
            
        for obj in bpy.data.collections[self.growth_stage[stage]].objects:
            if ".skeleton" in obj.name:
                return obj

    def set_location(self, location):
        self.barley_object.location = location


    def get_location(self):
        return self.barley_object.location

    def set_height(self, scale):
        self.barley_object.scale = Vector((scale, scale, scale))

    def add_weed(self, weed):
        self.active_weeds.append(weed)

    def get_weeds(self):
        return self.active_weeds

    def measure_height(self, crop_object):
        # Get the coordinates of the object's vertices
        vertices = [v.co for v in crop_object.data.vertices]

        # Get the transformation matrix of the object
        matrix_world = crop_object.matrix_world

        # Initialise min and max Y coordinates
        min_y = float("inf")
        max_y = float("-inf")

        # Calculate the minimum and maximum Y coordinates of the transformed coordinates
        for vertex in vertices:
            transformed_vertex = matrix_world @ vertex
            min_y = min(min_y, transformed_vertex.y)
            max_y = max(max_y, transformed_vertex.y)

        # Calculating the height of an object
        crop_height = max_y - min_y

        return crop_height
