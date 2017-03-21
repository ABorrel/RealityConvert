import bpy
import sys
from shutil import move
from os import path

########################
# Parsing command line #
########################

argv = sys.argv
argv = argv[argv.index("--") + 1:]  # get all args after "--"

prout = argv[1]
pin = argv[0]

#import WRML
bpy.ops.import_scene.x3d(filepath=pin, axis_forward='Z', axis_up='Y')

# remove default cube and camera
bpy.data.objects['Camera'].select = True
bpy.ops.object.delete()

bpy.data.objects["Cube"].select = True
bpy.ops.object.delete()

# joins all meshes -> need to fix for more complex model
for ob in bpy.context.scene.objects:
    if ob.type == 'MESH':
        ob.select = True
        bpy.context.scene.objects.active = ob
    else:
        ob.select = False

bpy.ops.object.join()

# UV wrap
bpy.ops.uv.smart_project()
#bpy.data.screens["Default"]

# export UVmap
bpy.ops.uv.export_layout(filepath=prout + ".png", size=(1024, 1024))
# change folder .png
#move(prout.split("/")[-1] + ".png", path.dirname(prout) + "/" + prout.split("/")[-1] + ".png")

# export obj
bpy.ops.export_scene.obj(filepath=prout + ".obj")




