import bpy, os
from mathutils import Color

possible_dir_names = {
        'ypanel',
        'ypanel-master',
        'yPanel',
        'yPanel-master'
        }

def get_active_material():
    mat = bpy.context.object.active_material
    if mat and mat.use_nodes:
        mat = mat.active_node_material
    return mat

def in_active_layer(obj):
    scene = bpy.context.scene
    space = bpy.context.space_data
    if space.type == 'VIEW_3D' and space.local_view:
        return any([layer for layer in obj.layers_local_view if layer])
    else:
        return any([layer for i, layer in enumerate(obj.layers) if layer and scene.layers[i]])

def get_addon_filepath():

    sep = os.sep

    # Search for addon dirs
    roots = bpy.utils.script_paths()

    for root in roots:
        if os.path.basename(root) != 'scripts': continue
        filepath = root + sep + 'addons'

        dirs = next(os.walk(filepath))[1]
        folders = [x for x in dirs if x in possible_dir_names]

        if folders:
            return filepath + sep + folders[0] + sep

    return 'ERROR: No path found for yPanel!'

def srgb_to_linear_per_element(e):
    if e <= 0.03928:
        return e/12.92
    else: 
        return pow((e + 0.055) / 1.055, 2.4)

def linear_to_srgb_per_element(e):
    if e > 0.0031308:
        return 1.055 * (pow(e, (1.0 / 2.4))) - 0.055
    else: 
        return 12.92 * e

def srgb_to_linear(inp):

    if type(inp) == float:
        return srgb_to_linear_per_element(inp)

    elif type(inp) == Color:

        c = inp.copy()

        for i in range(3):
            c[i] = srgb_to_linear_per_element(c[i])

        return c

def linear_to_srgb(inp):

    if type(inp) == float:
        return linear_to_srgb_per_element(inp)

    elif type(inp) == Color:

        c = inp.copy()

        for i in range(3):
            c[i] = linear_to_srgb_per_element(c[i])

        return c
