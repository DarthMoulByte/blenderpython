# BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Mira Tools",
    "author": "Paul Geraskin",
    "version": (0, 1, 0),
    "blender": (2, 74, 0),
    "location": "3D Viewport",
    "description": "Mira Tool",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Tools"}


if "bpy" in locals():
    import imp
    imp.reload(mi_base)
    imp.reload(mi_deform)
    imp.reload(mi_extrude)
else:
    from . import mi_base
    from . import mi_deform
    from . import mi_extrude


import bpy
from bpy.props import *


def register():

    bpy.utils.register_module(__name__)

    # bpy.types.Scene.mira_curve_points = PointerProperty(
    #     name="Mira Tool Variables",
    #     type=mi_base.MR_CurvePoint,
    #     description="Mira Curve"
    # )

    bpy.types.Object.mi_curves = CollectionProperty(
        name="Mira Tool Variables",
        type=mi_base.MI_CurveObject,
        description="Mira Curve"
    )

    bpy.types.Scene.mi_extrude_settings = PointerProperty(
        name="Mira Tool Variables",
        type=mi_extrude.MI_ExtrudeSettings,
        description="Mira Curve"
    )

def unregister():
    import bpy

    #del bpy.types.Scene.miraTool
    del bpy.types.Object.mi_curves  # need to investigate if i need to delete it
    del bpy.types.Scene.mi_extrude_settings
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
