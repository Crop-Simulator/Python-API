import bpy
import os


class CropController:

    def __init__(self, crop_data, collection):
        self.collection_name = collection

        self.type = crop_data["type"] # list
        self.size = crop_data["size"]
        self.percentage_share = crop_data["percentage_share"]
        self.total_number = crop_data["total_number"]
        self.num_rows = crop_data["num_rows"]
        self.row_widths = crop_data["row_widths"]
        self.counter = 1

    def setup_crops(self):
        curr_row = 0
        curr_loc = 0
        curr_crop_type = 0
        curr_crop = 0
        num_rows = int(self.total_number/self.num_rows)

        for crop in range(self.total_number):
            if crop % num_rows == 0:
                # splits crops into rows:
                # increases row num, when reached and
                # increments location by 1
                curr_row += 1
                curr_loc = 0

            num_crops = int(self.total_number*self.percentage_share[curr_crop_type])
            if curr_crop % num_crops == 0 and crop != 0:
                # counts the correct number of crops have
                # been generated based on their percentage share
                # excludes: first crop because it should always be
                # generated and will always return 0
                curr_crop = 0
                if not curr_crop_type >= len(self.type) - 1:
                    # checks that there are more crop types
                    # before changing to next crop type
                    curr_crop_type += 1

            loc = curr_loc - self.total_number/self.num_rows/2  # centers crops
            locx = loc - self.row_widths*curr_row/2
            curr_loc += 1
            crop_size = 0.5
            crop_model = self.add_crop(crop_size, loc, locx)
            material, segmentation_id = self.assign_crop_type(self.type[curr_crop_type])

            crop_model["segmentation_id"] = segmentation_id

            curr_crop += 1

    def assign_crop_type(self, crop_type):
        # assign material and segmentation id depending on crop type
        material = None
        segmentation_id = 0
        if crop_type == "red":
            material = bpy.data.materials.new("Red")
            segmentation_id = 1
        elif crop_type == "green":
            material = bpy.data.materials.new("Green")
            segmentation_id = 2
        elif crop_type == "blue":
            material = bpy.data.materials.new("Blue")
            segmentation_id = 3
        material.use_nodes = True
        bsdf = material.node_tree.nodes["Principled BSDF"]
        cwd = os.getcwd()
        texture_image = material.node_tree.nodes.new("ShaderNodeTexImage")
        texture_image.image = bpy.data.images.load(cwd+"\\src\\blender_assets\\textures\\textures\\texture2.jpg")
        material.node_tree.links.new(bsdf.inputs["Base Color"], texture_image.outputs["Color"])
        return material, segmentation_id

    def add_crop(self, crop_size, loc, locx):
        bpy.data.collections[self.collection_name]
        bpy.context.active_object.name = "stage7.009"
        cube = bpy.context.scene.objects.get("stage7.009")

        duplicated = cube.copy()
        duplicated.data = cube.data.copy()
        duplicated.location = (locx, loc, loc)
        self.counter += 1
        bpy.context.collection.objects.link(duplicated)
        return cube
