import os
from pathlib import Path

import bpy
import mathutils

from src.utils import get_project_root


class GroundController:
    def __init__(self, config):
        self.collection_name = "GroundStages"
        self.collection = bpy.data.collections.new(self.collection_name)
        bpy.context.scene.collection.children.link(self.collection)
        self.ground_type = config["ground_type"]
        self.crop_data = config["crop"]
        self.total_number = self.crop_data["total_number"]
        self.num_rows = self.crop_data["num_rows"]
        self.row_widths = self.crop_data["row_widths"]

    def get_texture_file(self):
        texture_dir = get_project_root() + "/blender_assets/textures/"
        if self.ground_type == "sandy":
            return texture_dir + "sandy_loam.jpg"
        elif self.ground_type == "loam":
            return texture_dir + "loam.jpg"
        elif self.ground_type == "brown_soil":
            return texture_dir == "brown_soil.jpg"
        else:
            raise ValueError(f"Unknown ground type {self.ground_type}")

    def get_ground_stages(self):
        ground_stages = [obj for obj in bpy.data.objects if obj.name.startswith("stage") and obj.name.endswith(".ground")]
        # ground_size = self.total_number/self.num_rows*self.row_widths
        for obj in ground_stages:
            self.collection.objects.link(obj)
            obj.location = (1, 0.5, -5)
            obj.scale = mathutils.Vector((10, 10, 1))

        file_path = self.get_texture_file()
        texture_image = bpy.data.images.load(file_path)
        material = bpy.data.materials.new(name="Texture_Material")
        material.use_nodes = True
        node_tree = material.node_tree
        principled_node = node_tree.nodes.get("Principled BSDF")
        texture_node = node_tree.nodes.new("ShaderNodeTexImage")
        texture_node.image = texture_image

        coord_node = node_tree.nodes.new("ShaderNodeTexCoord") # new node for coordinates
        mapping_node = node_tree.nodes.new("ShaderNodeMapping") # new node for mapping

        # setup mapping scale (higher values will make the texture smaller, thus repeating it more times)
        mapping_node.inputs["Scale"].default_value = (4, 5, 4) # adjust the value as needed

        # link new nodes
        links = node_tree.links
        links.new(coord_node.outputs["UV"], mapping_node.inputs["Vector"])
        links.new(mapping_node.outputs["Vector"], texture_node.inputs["Vector"])
        links.new(texture_node.outputs[0], principled_node.inputs[0])  # color to base color


        # Assign it to object
        if "stage9.ground" in bpy.data.objects:  # replace with your object's name
            obj = bpy.data.objects["stage9.ground"]
            if obj.data.materials:
                # assign to 1st material slot
                obj.data.materials[0] = material
            else:
                # no slots
                obj.data.materials.append(material)

