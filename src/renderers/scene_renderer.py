import os
import bpy
import mathutils

from controllers.segmentation import Segmentation

class SceneRenderer:
    def __init__(self, output_file, collection):
        self.output_file = output_file
        self.collection = collection

    def render_scene(self):
        print("rendering...")
        current_working_directory = str(os.getcwd())
        bpy.data.collections[self.collection]
        scene = bpy.context.scene
        scene.camera = bpy.context.object



        sky_texture = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeTexSky")
        background = bpy.context.scene.world.node_tree.nodes["Background"]
        bpy.context.scene.world.node_tree.links.new(background.inputs["Color"], sky_texture.outputs["Color"])


        sky_texture.sky_type = "PREETHAM"			# or 'PREETHAM' or 'HOSEK_WILKIE'
        sky_texture.turbidity = 5.0
        sky_texture.ground_albedo = 0.4
        sky_texture.sun_direction = mathutils.Vector((1.0, 0.0, 1.0))

        bpy.context.scene.render.filepath = os.path.join(current_working_directory, self.output_file)
        bpy.ops.render.render(use_viewport=True, write_still=True)

        segmentation = Segmentation({
            1: 0xffff, # Make cubes white in the segmentation map
            2: 0xcccc,
            3: 0x9999,
        })
        segmentation_filename = self.output_file.replace(".png", "_seg.png") if self.output_file.endswith(".png") else self.output_file + "_seg.png"
        segmentation.segment(segmentation_filename)
