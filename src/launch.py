import argparse
import bpy
import math
import os
import subprocess
import yaml

'''
adding parser arguments for Python CLI interface
-------
example CLI command: python launch.py -i data.yml -o test.png 

''' 
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--infile", nargs="+")
parser.add_argument("-o", "--outfile", nargs="+")
args = parser.parse_args()

'''
Processing the yaml file
-------
locates yaml file from parsed CLI command within current working directory
loads yaml file data to use for presenting the 3D model
'''

current_working_directory = str(os.getcwd())
openfile = current_working_directory + "/" + args.infile[0]
print(openfile)
input_file = None
with open(openfile, "r") as file:
    input_file = yaml.safe_load(file)
    
    ## Need to edit this to fit where blender is on your PC - working on a fix to work without manual change
    myargs = ["C:/Program Files/Blender Foundation/Blender 3.3/blender",
            "-b",
            "C:/Users/barba/Documents/UCL/Summer Project/Python-API/test.blend",
    ]
    
    ## temporarily removing the existing cube object in the blend file
    collection1 = bpy.data.collections.get('Collection')
    cube = collection1.objects.get("Cube")
    collection1.objects.unlink(cube)
    
    ## change camera angle so that it can see all crops
    a = 'camera_one'
    bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(10,0,0), rotation=(1.57057,0.00174533,1.57057))
    bpy.data.objects["Camera"].name = a
    bpy.data.objects[a].data.lens_unit = 'FOV'
    bpy.data.objects[a].data.angle= math.radians(100)
    collection = bpy.data.collections.new(name="Collection")
    bpy.context.scene.collection.children.link(collection)
    
    
    CROP_SIZE = 0.5
    num_crops = input_file['num_crops']
    num_rows = input_file['num_crop_rows']
    crop_distance = input_file['num_crop_distance']
    crop_type = input_file['colors']
    crop_percentage = input_file['percent_crop_type']
    
    split = int(num_crops/num_rows)
    
    row = 0
    origin = 0
    crop_type_counter = 0
    crop_counter = 0
    for crop in range(num_crops):
        
        if crop % split == 0:
            row += 1
            origin = 0
            
        if crop_counter % int(num_crops*crop_percentage[crop_type_counter]) == 0 and crop != 0:
            print(num_crops*crop_percentage[crop_type_counter])
            crop_counter = 0
            if not crop_type_counter >= len(crop_type) - 1:
                print(crop_type[crop_type_counter])
                crop_type_counter += 1
                
                
            
        loc = origin - num_crops/num_rows/2 # trying to center the cubes a little
        locx = origin - num_crops/num_rows/2 - crop_distance*row/2
        origin += 1
        bpy.ops.mesh.primitive_cube_add(location=(locx, loc, loc), size=CROP_SIZE)
        bpy.context.active_object.name = 'cube'
        cube = bpy.context.object
        for ob in cube.users_collection[:]: #unlink from all preceeding object collections
            ob.objects.unlink(cube)
        collection.objects.link(cube)
        
        matr = None
        if crop_type[crop_type_counter] == "red":
            matr = bpy.data.materials.new("Red")
            matr.diffuse_color = (1,0,0,0.8)
        elif crop_type[crop_type_counter] == "green":
            matr = bpy.data.materials.new("Green")
            matr.diffuse_color = (0,1,0,0.8)
        elif crop_type[crop_type_counter] == "blue":
            matr = bpy.data.materials.new("Blue")
            matr.diffuse_color = (0,0,1,0.8)
            
        

        ob = cube.copy()
        ob.active_material = matr
        bpy.context.collection.objects.link(ob)
        crop_counter += 1


    output_loc = args.outfile[0]
    print("CURRENT" + current_working_directory)
    bpy.context.scene.render.filepath = current_working_directory + '/' + output_loc
    bpy.ops.render.render(use_viewport = True, write_still=True)
    subprocess.run(myargs, shell=True)
    





