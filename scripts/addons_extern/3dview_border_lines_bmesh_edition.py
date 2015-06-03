# ##### BEGIN GPL LICENSE BLOCK #####
#
#  3dview_border_lines_bmesh_edition.py
#  Draw thicker lines for border edges - using bmesh in edit mode
#  Copyright (C) 2015 Quentin Wenger
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
# ##### END GPL LICENSE BLOCK #####



bl_info = {"name": "Border Lines - BMesh Edition",
           "description": "Draw thicker lines for border edges; this is a version "\
                          "of the addon which should be faster than the original; "\
                          "it allows thick display of active edge color, but notof fancy "\
                          "edges (freestyle, crease, seam, sharp, etc.), which are "\
                          "nevertheless shown normally.",
           "author": "Quentin Wenger (Matpi)",
           "version": (1, 5),
           "blender": (2, 74, 0),
           "location": "3D View(s) -> Properties -> Shading",
           "warning": "",
           "wiki_url": "",
           "tracker_url": "",
           "category": "3D View"
           }



import bpy
from bpy_extras.mesh_utils import edge_face_count
from mathutils import Vector
from bgl import glBegin, glLineWidth, glColor3f, glColor4f, glVertex3f, glEnd, GL_LINES
import bmesh

handle = []
do_draw = [False]
point_size = [3.0]
bm_old = [None]



def drawColorSize(coords, color):
    glColor3f(*color[:3])
    for coord in coords:
        glVertex3f(*coord)

def drawCallback():
    obj = bpy.context.object
    if obj and obj.type == 'MESH' and obj.data:
        if do_draw[0]:
            mesh = obj.data
            matrix_world = obj.matrix_world
            settings = bpy.context.user_preferences.themes[0].view_3d

            transform = settings.transform
            edge_select = settings.edge_select
            wire_edit = settings.wire_edit
            wire = settings.wire
            object_active = settings.object_active

            glLineWidth(point_size[0])
            glBegin(GL_LINES)

            if bpy.context.mode == 'EDIT_MESH':

                if bm_old[0] is None or not bm_old[0].is_valid:
                    bm = bm_old[0] = bmesh.from_edit_mesh(mesh)

                else:
                    bm = bm_old[0]

                active = bm.select_history.active
                for edge in bm.edges:
                    if edge.is_valid and edge.is_boundary:
                        coords = [matrix_world*vert.co for vert in edge.verts]

                        if active == edge:
                            drawColorSize(coords, transform)
                        elif edge.select:
                            drawColorSize(coords, edge_select)
                        else:
                            drawColorSize(coords, wire_edit)

            elif bpy.context.mode == 'OBJECT' and (obj.show_wire or bpy.context.space_data.viewport_shade == 'WIREFRAME'):
                counts = edge_face_count(mesh)
                if obj.select:
                    for edge, count in zip(mesh.edges, counts):
                        # border edges
                        if count == 1:
                            coords = [matrix_world*Vector(mesh.vertices[i].co) for i in edge.key]
                            drawColorSize(coords, object_active)
                else:
                    for edge, count in zip(mesh.edges, counts):
                        # border edges
                        if count == 1:
                            coords = [matrix_world*Vector(mesh.vertices[i].co) for i in edge.key]
                            drawColorSize(coords, wire)
                    
            glEnd()
            glLineWidth(1.0)
            



def updateBGLData(self, context):
    point_size[0] = self.borderlines_width
    if self.borderlines_use:
        do_draw[0] = True
        return

    do_draw[0] = False


class BorderLinesCollectionGroup(bpy.types.PropertyGroup):
    borderlines_use = bpy.props.BoolProperty(
        name="Border Lines",
        description="Display border edges thicker",
        default=False,
        update=updateBGLData)
    borderlines_width = bpy.props.FloatProperty(
        name="Width",
        description="Border lines width in pixels",
        min=1.0,
        max=20.0,
        default=3.0,
        subtype='PIXEL',
        update=updateBGLData)
    updating_locked = bpy.props.BoolProperty(
        name="Locked Refresh",
        description="Whether to continuously update values",
        default=False)


    
    
def displayBorderLinesPanel(self, context):
    layout = self.layout

    border_lines = context.window_manager.border_lines

    layout.prop(border_lines, "borderlines_use")

    if border_lines.borderlines_use:
        layout.prop(border_lines, "borderlines_width")        
        

def register():
    bpy.utils.register_module(__name__)
    bpy.types.WindowManager.border_lines = bpy.props.PointerProperty(
        type=BorderLinesCollectionGroup)
    bpy.types.VIEW3D_PT_view3d_shading.append(displayBorderLinesPanel)
    if handle:
        bpy.types.SpaceView3D.draw_handler_remove(handle[0], 'WINDOW')
    handle[:] = [bpy.types.SpaceView3D.draw_handler_add(drawCallback, (), 'WINDOW', 'POST_VIEW')]

    

def unregister():
    bpy.types.VIEW3D_PT_view3d_shading.remove(displayBorderLinesPanel)
    del bpy.types.WindowManager.border_lines
    if handle:
        bpy.types.SpaceView3D.draw_handler_remove(handle[0], 'WINDOW')
        handle[:] = []
    bpy.utils.unregister_module(__name__)
    

if __name__ == "__main__":
    register()
