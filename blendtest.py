import bpy,subprocess, argparse, yaml, os
file_path="test.blend"

parser = argparse.ArgumentParser()
parser.add_argument("infile", nargs="+")
parser.add_argument("outfile", nargs="+")
args = parser.parse_args()
current_working_directory = str(os.getcwd())
openfile = current_working_directory + "/" + args.infile[0]

print(openfile)
input_file = None
with open(openfile, "r") as file:
    input_file = yaml.safe_load(file)

    myargs = ["C:/Program Files/Blender Foundation/Blender 3.3/blender",
            "-b",
            "C:/Users/barba/Documents/UCL/Summer Project/blender_testing/weirdshape.blend",
    ]
    template_object = bpy.data.objects.get('Cube')
    template_object.material_slots[0].link = 'OBJECT'
    matr = None
    if input_file['color'] == "red":
        matr = bpy.data.materials.new("Red")
        matr.diffuse_color = (1,0,0,0.8)
    elif input_file['color'] == "green":
        matr = bpy.data.materials.new("Green")
        matr.diffuse_color = (0,1,0,0.8)
    elif input_file['color'] == "blue":
        matr = bpy.data.materials.new("Blue")
        matr.diffuse_color = (0,0,1,0.8)

    ob = template_object.copy()
    ob.active_material = matr
    bpy.context.collection.objects.link(ob)

    output_loc = args.outfile[0]
    bpy.context.scene.render.filepath = 'C:/Users/barba/Documents/UCL/Summer Project/blender_testing/' + output_loc
    bpy.ops.render.render(use_viewport = True, write_still=True)
    subprocess.run(myargs, shell=True)
    





