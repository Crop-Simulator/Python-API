import bpy
import mathutils

class LightController:
    def __init__(self, sky_type="PREETHAM", turbidity=5.0, ground_albedo=0.4, sun_direction=(0.0, 0.0, 0.5)):
        self.sky_type = sky_type
        self.turbidity = turbidity
        self.ground_albedo = ground_albedo
        self.sun_direction = mathutils.Vector(sun_direction)

    def add_sky(self):
        sky_texture = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeTexSky")
        background = bpy.context.scene.world.node_tree.nodes["Background"]
        bpy.context.scene.world.node_tree.links.new(background.inputs["Color"], sky_texture.outputs["Color"])

        sky_texture.sky_type = self.sky_type			# 'PREETHAM' or 'HOSEK_WILKIE'
        sky_texture.turbidity = self.turbidity
        sky_texture.ground_albedo = self.ground_albedo
        sky_texture.sun_direction = self.sun_direction

    def add_light(self, light_location=(10, 5, 0)):
        # create light datablock, set attributes
        light_data = bpy.data.lights.new(name="light", type="AREA")
        light_data.energy = 50

        # create new object with our light datablock
        light_object = bpy.data.objects.new(name="light", object_data=light_data)

        # link light object and set active
        bpy.context.collection.objects.link(light_object)
        bpy.context.view_layer.objects.active = light_object

        #change location
        light_object.location = mathutils.Vector(light_location)

        # update scene to move light location
        dg = bpy.context.evaluated_depsgraph_get()
        dg.update()


    def change_sky_type(self, sky_type):
        self.sky_type = sky_type
