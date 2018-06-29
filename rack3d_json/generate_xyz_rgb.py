#!/usr/local/bin/python3.6

import json
import urllib.request

# set the location of the racktables json page
json_page = ""
# set the json output file
json_out = "dc.json"

# download the json page and convert to a list of dicts
with urllib.request.urlopen(json_page) as response:
   data = json.loads(response.read())

# create a new list of dicts with xyz and color
new_list = []
for oldthing in data:
    newthing = dict()
    newthing['name'] = oldthing['name']
    newthing['id'] = oldthing['id']
    # calculate x,y,z in meters
    if ( oldthing['row']  % 2 == 0 ):
        newthing['xMin'] = ( oldthing['row'] * 2.4 ) + 1.2 - ( oldthing['maxDepth'] * 0.4 ) - 0.4
        newthing['xMax'] = ( oldthing['row'] * 2.4 ) + 1.2 - ( oldthing['minDepth'] * 0.4 )
    else:
        newthing['xMin'] = ( oldthing['row'] * 2.4 ) + ( oldthing['minDepth'] * 0.4 )
        newthing['xMax'] = ( oldthing['row'] * 2.4 ) + ( oldthing['maxDepth'] * 0.4 ) + 0.4
    newthing['yMin'] = ( oldthing['rack'] * 0.6 ) + 0.01
    newthing['yMax'] = ( oldthing['rack'] * 0.6 ) + 0.59
    newthing['zMin'] = ( oldthing['minUnit'] * 0.05 )
    newthing['zMax'] = ( oldthing['maxUnit'] * 0.05 ) + 0.045
    # generate rgb values by object type
    newthing['rgb_blue'] = 0.5
    newthing['rgb_green'] = 0.5
    newthing['rgb_red'] = 0.5
    if ( oldthing['objtype_id'] == '4' ):
        newthing['rgb_blue']=0.75
        newthing['rgb_green']=0.75
        newthing['rgb_red']=1.0
    if ( oldthing['objtype_id'] == '8' ):
        newthing['rgb_blue']=0.75
        newthing['rgb_green']=1.0
        newthing['rgb_red']=0.75
    if ( oldthing['objtype_id'] == '9' ):
        newthing['rgb_blue']=1.0
        newthing['rgb_green']=0.75
        newthing['rgb_red']=0.75
    # flip y axis (optional)
    temp = newthing['yMin']
    newthing['yMin'] = newthing['yMax'] * -1
    newthing['yMax'] = temp * -1
    # rotate -90 on x axis to compensate for blender import script
    temp = newthing['yMin']
    newthing['yMin'] = newthing['zMin']
    newthing['zMin'] = newthing['yMax'] * -1
    newthing['yMax'] = newthing['zMax']
    newthing['zMax'] = temp * -1
    new_list.append(newthing)

# export the new list to a json file
with open(json_out, 'w') as out:
    json.dump( new_list, out )

