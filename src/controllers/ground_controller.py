import bpy

class GroundController:
    def __init__(self):
        self.collection_name = 'GroundStages'
        self.collection = bpy.data.collections.new(self.collection_name)
        bpy.context.scene.collection.children.link(self.collection)

    def get_ground_stages(self):
        ground_stages = [obj for obj in bpy.data.objects if obj.name.startswith('stage') and obj.name.endswith('.ground')]
        for obj in ground_stages:
            self.collection.objects.link(obj)
            obj.location = (0, 0, 0)