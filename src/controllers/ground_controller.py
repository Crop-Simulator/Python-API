import bpy
import mathutils
import os

class GroundController:
    def __init__(self,config):
        self.collection_name = 'GroundStages'
        self.collection = bpy.data.collections.new(self.collection_name)
        bpy.context.scene.collection.children.link(self.collection)
        self.groundtype = config["ground_type"]

    def get_ground_stages(self):
        ground_stages = [obj for obj in bpy.data.objects if obj.name.startswith('stage') and obj.name.endswith('.ground')]
        for obj in ground_stages:
            self.collection.objects.link(obj)
            obj.location = (1, 0.5, -5)
            obj.scale = mathutils.Vector((1, 1, 1))
        
        print
        
        file_path = "src/blender_assets/textures/textures/soil_texture.jpg"
        texture_image = bpy.data.images.load(file_path)
        material = bpy.data.materials.new(name="Texture_Material")
        material.use_nodes = True
        node_tree = material.node_tree
        principled_node = node_tree.nodes.get('Principled BSDF')
        texture_node = node_tree.nodes.new('ShaderNodeTexImage')
        texture_node.image = texture_image
        links = node_tree.links
        link = links.new(texture_node.outputs[0], principled_node.inputs[0])  # color to base color
        # Assign it to object
        if "stage9.ground" in bpy.data.objects:  # replace with your object's name
            obj = bpy.data.objects["stage9.ground"]
            if obj.data.materials:
                # assign to 1st material slot
                obj.data.materials[0] = material
            else:
                # no slots
                obj.data.materials.append(material)    

