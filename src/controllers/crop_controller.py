import bpy

from .yaml_reader import YamlReader

class CropController:

    def __init__(self, crop_datafile, collection):
        reader = YamlReader()
        crop_data = reader.read_file(crop_datafile)

        self.collection_name = collection

        self.type = crop_data["crop"]["type"] # list
        self.size = crop_data["crop"]["size"]
        self.percentage_share = crop_data["crop"]["percentage_share"]
        self.total_number = crop_data["crop"]["total_number"]
        self.num_rows = crop_data["crop"]["num_rows"]
        self.row_widths = crop_data["crop"]["row_widths"]

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

            crop_model.active_material = material
            crop_model["segmentation_id"] = segmentation_id

            curr_crop += 1

    def assign_crop_type(self, crop_type):
        # assign material and segmentation id depending on crop type
        material = None
        segmentation_id = 0
        if crop_type == "red":
            material = bpy.data.materials.new("Red")
            material.diffuse_color = (1,0,0,0.8)
            segmentation_id = 1
        elif crop_type == "green":
            material = bpy.data.materials.new("Green")
            material.diffuse_color = (0,1,0,0.8)
            segmentation_id = 2
        elif crop_type == "blue":
            material = bpy.data.materials.new("Blue")
            material.diffuse_color = (0,0,1,0.8)
            segmentation_id = 3
        return material, segmentation_id

    def add_crop(self, crop_size, loc, locx):
        bpy.ops.mesh.primitive_cube_add(location=(locx, loc, loc), size=crop_size)
        collection = bpy.data.collections[self.collection_name]
        bpy.context.active_object.name = "cube"
        cube = bpy.context.object
        for ob in cube.users_collection[:]: #unlink from all preceeding object collections
            ob.objects.unlink(cube)
        collection.objects.link(cube)
        return cube
