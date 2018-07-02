#!/usr/local/bin/python3.6

# this script downloads the json, builds the model files and the python files to import them, then runs blender.

import json
import urllib.request
import subprocess

# settings
jsonUrl = "https://raw.githubusercontent.com/magnusmichaelson/rack3d/master/rack3d_json/example.json"
objFile = "/tmp/dc.obj"
mtlFile = "/tmp/dc.mtl"
importFile = "/tmp/dc.py"
blender = "/Applications/Blender/blender.app/Contents/MacOS/blender"

# download the json and import into a list of dicts
print("downloading json")
with urllib.request.urlopen(jsonUrl) as response:
   data = json.loads(response.read())

# process the list of dicts
print("processing data")
for thing in data:
    # generate rgb values by object type
    thing['rgb_blue'] = 0.5
    thing['rgb_green'] = 0.5
    thing['rgb_red'] = 0.5
    if ( thing['objtype_id'] == '4' ):
        thing['rgb_blue']=0.75
        thing['rgb_green']=0.75
        thing['rgb_red']=1.0
    if ( thing['objtype_id'] == '8' ):
        thing['rgb_blue']=0.75
        thing['rgb_green']=1.0
        thing['rgb_red']=0.75
    if ( thing['objtype_id'] == '9' ):
        thing['rgb_blue']=1.0
        thing['rgb_green']=0.75
        thing['rgb_red']=0.75
    # scale down from mm to meters
    thing['xMin'] = thing['xMin'] * 0.001
    thing['xMax'] = thing['xMax'] * 0.001
    thing['yMin'] = thing['yMin'] * 0.001
    thing['yMax'] = thing['yMax'] * 0.001
    thing['zMin'] = thing['zMin'] * 0.001
    thing['zMax'] = thing['zMax'] * 0.001
    # rotate -90 on x axis to compensate for blender import script
    temp = thing['yMin']
    thing['yMin'] = thing['zMin']
    thing['zMin'] = thing['yMax'] * -1
    thing['yMax'] = thing['zMax']
    thing['zMax'] = temp * -1

# export obj file
print("exporting obj file")
vert=0
face=0
with open(objFile, 'w') as obj:
    for thing in data:
        obj.write("o {}\n".format(thing['name']))
        obj.write("v {} {} {}\n".format(thing['xMin'],thing['yMin'],thing['zMin']))
        obj.write("v {} {} {}\n".format(thing['xMin'],thing['yMax'],thing['zMin']))
        obj.write("v {} {} {}\n".format(thing['xMax'],thing['yMax'],thing['zMin']))
        obj.write("v {} {} {}\n".format(thing['xMax'],thing['yMin'],thing['zMin']))
        obj.write("v {} {} {}\n".format(thing['xMin'],thing['yMin'],thing['zMax']))
        obj.write("v {} {} {}\n".format(thing['xMin'],thing['yMax'],thing['zMax']))
        obj.write("v {} {} {}\n".format(thing['xMax'],thing['yMax'],thing['zMax']))
        obj.write("v {} {} {}\n".format(thing['xMax'],thing['yMin'],thing['zMax']))
        obj.write("vn 0.0 0.0 -1.0\n")
        obj.write("vn 0.0 0.0 1.0\n")
        obj.write("vn 0.0 1.0 0.0\n")
        obj.write("vn 1.0 0.0 0.0\n")
        obj.write("vn 0.0 -1.0 0.0\n")
        obj.write("vn -1.0 0.0 0.0\n")
        obj.write("usemtl {}\n".format(thing['name']))
        obj.write("s off\n")
        obj.write("f {}//{} {}//{} {}//{} {}//{}\n".format( (vert+1), (face+1), (vert+2), (face+1), (vert+3), (face+1), (vert+4), (face+1)))
        obj.write("f {}//{} {}//{} {}//{} {}//{}\n".format( (vert+5), (face+2), (vert+8), (face+2), (vert+7), (face+2), (vert+6), (face+2)))
        obj.write("f {}//{} {}//{} {}//{} {}//{}\n".format( (vert+2), (face+3), (vert+6), (face+3), (vert+7), (face+3), (vert+3), (face+3)))
        obj.write("f {}//{} {}//{} {}//{} {}//{}\n".format( (vert+3), (face+4), (vert+7), (face+4), (vert+8), (face+4), (vert+4), (face+4)))
        obj.write("f {}//{} {}//{} {}//{} {}//{}\n".format( (vert+4), (face+5), (vert+8), (face+5), (vert+5), (face+5), (vert+1), (face+5)))
        obj.write("f {}//{} {}//{} {}//{} {}//{}\n".format( (vert+1), (face+6), (vert+5), (face+6), (vert+6), (face+6), (vert+2), (face+6)))
        obj.write("\n")
        vert = vert + 8
        face = face + 6

# export mtl file 
print("exporting mtl file")
with open(mtlFile, 'w') as mtl:
    for thing in data:
        mtl.write("newmtl {}\n".format(thing['name']))
        mtl.write("Ns 96.078431\n")
        mtl.write("Ka 1.000000 1.000000 1.000000\n");
        mtl.write("Kd {} {} {}\n".format(thing['rgb_red'],thing['rgb_green'],thing['rgb_blue']))
        mtl.write("Ks 0.500000 0.500000 0.500000\n");
        mtl.write("Ke 0.000000 0.000000 0.000000\n");
        mtl.write("Ni 1.000000\n");
        mtl.write("d 1.000000\n");
        mtl.write("illum 2\n");
        mtl.write("\n");

# build the import python script
print("exporting python import scripts")
with open(importFile, 'w') as load:
    load.write("import bpy\n");
    load.write("full_path_to_file = \"{}\"\n".format(objFile))
    load.write("bpy.ops.import_scene.obj(filepath=full_path_to_file)\n")

# run blender
print("running blender")
process=subprocess.run([blender,"-P",importFile])
print(process.returncode)
