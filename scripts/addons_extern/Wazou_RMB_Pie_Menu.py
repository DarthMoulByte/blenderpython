# -*- coding: utf-8 -*-

# ##### BEGIN GPL LICENSE BLOCK #####
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

bl_info = {
    "name": "Wazou Right clic Pie Menu",
    "author": "Cédric Lepiller",
    "version": (0, 2, 3),
    "blender": (2, 76, 0),
    "location": "View3D > RMB",
    "description": "Right Click Pie Menu",
    "category": "Pie Menu"}

"""
Right Click Pie Menu
This adds a the Right Click Pie Menu in the View3D.
Left mouse is SELECTION.
Left Alt + Double click sets the 3D cursor.

"""

import bpy
import bmesh
from bpy.types import Menu
from bpy.props import IntProperty, FloatProperty, BoolProperty
from bl_ui.properties_paint_common import (
    UnifiedPaintPanel,
    brush_texture_settings,
    brush_texpaint_common,
    brush_mask_texture_settings,
)
import rna_keymap_ui


########################
#      Properties      #
########################

class WazouRightMenuPiePrefs(bpy.types.AddonPreferences):
    """Creates the tools in a Panel, in the scene context of the properties editor"""
    bl_idname = __name__

    bpy.types.Scene.Enable_Tab_RMB_01 = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.Enable_Tab_RMB_02 = bpy.props.BoolProperty(default=False)

    def draw(self, context):
        layout = self.layout

        layout.prop(context.scene, "Enable_Tab_RMB_01", text="Keymap", icon="QUESTION")
        if context.scene.Enable_Tab_RMB_01:
            col = layout.column()
            kc = bpy.context.window_manager.keyconfigs.addon
            for km, kmi in addon_keymaps:
                km = km.active()
                col.context_pointer_set("keymap", km)
                rna_keymap_ui.draw_kmi([], kc, km, kmi, col, 0)

        layout.prop(context.scene, "Enable_Tab_RMB_02", text="URL's", icon="URL")
        if context.scene.Enable_Tab_RMB_02:
            row = layout.row()

            row.operator("wm.url_open", text="Pitiwazou.com").url = "http://www.pitiwazou.com/"
            row.operator("wm.url_open", text="Wazou's Ghitub").url = "https://github.com/pitiwazou/Scripts-Blender"
            row.operator("wm.url_open", text="BlenderLounge Forum ").url = "http://blenderlounge.fr/forum/"


#######################
#       Classes       #
#######################

# Add Mesh #
class AddMenu(bpy.types.Menu):
    bl_label = "Add Mesh"

    def draw(self, context):
        layout = self.layout

        layout.operator("mesh.primitive_cube_add", text="Cube", icon='MESH_CUBE')
        layout.operator("mesh.primitive_plane_add", text="Plane", icon='MESH_PLANE')
        layout.operator("mesh.primitive_uv_sphere_add", text="UV Sphere", icon='MESH_UVSPHERE')
        layout.operator("mesh.primitive_cylinder_add", text="Cylinder", icon='MESH_CYLINDER')
        layout.operator("mesh.primitive_grid_add", text="Grid", icon='MESH_GRID')
        layout.operator("mesh.primitive_ico_sphere_add", text="Ico Sphere", icon='MESH_ICOSPHERE')
        layout.operator("mesh.primitive_circle_add", text="Circle", icon='MESH_CIRCLE')
        layout.operator("mesh.primitive_cone_add", text="Cone", icon='MESH_CONE')
        layout.operator("mesh.primitive_torus_add", text="Torus", icon='MESH_TORUS')
        layout.operator("mesh.primitive_monkey_add", text="Monkey", icon='MESH_MONKEY')
        layout.separator()
        layout.operator("object.camera_add", icon='OUTLINER_OB_CAMERA')
        layout.separator()
        layout.operator("object.lamp_add", text="Area", icon='LAMP_AREA').type = 'AREA'
        layout.operator("object.lamp_add", text="Sun", icon='LAMP_SUN').type = 'SUN'
        layout.operator("object.lamp_add", text="Hemi", icon='LAMP_HEMI').type = 'HEMI'
        layout.operator("object.lamp_add", text="Point", icon='LAMP_POINT').type = 'POINT'
        layout.operator("object.lamp_add", text="Spot", icon='LAMP_SPOT').type = 'SPOT'
        layout.separator()
        layout.operator("curve.primitive_bezier_circle_add", icon='CURVE_BEZCIRCLE')
        layout.operator("curve.primitive_bezier_curve_add", icon='CURVE_BEZCURVE')
        layout.operator("curve.primitive_nurbs_path_add", icon='CURVE_PATH')
        layout.separator()
        layout.operator("object.empty_add", text="Empty AXE", icon='OUTLINER_OB_EMPTY').type = 'PLAIN_AXES'
        layout.operator("object.empty_add", text="Empty CUBE", icon='OUTLINER_OB_EMPTY').type = 'CUBE'
        layout.operator("object.add", text="Lattice", icon='OUTLINER_OB_LATTICE').type = 'LATTICE'
        layout.operator("object.text_add", text="Text", icon='OUTLINER_OB_FONT')
        layout.operator("object.armature_add", text="Armature", icon='OUTLINER_OB_ARMATURE')


# Subsurf 2
class SubSurf2(bpy.types.Operator):
    bl_idname = "object.subsurf2"
    bl_label = "SubSurf 2"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.subdivision_set(level=2)
        bpy.context.object.modifiers["Subsurf"].show_only_control_edges = True

        if bpy.context.object.mode == "EDIT":
            bpy.ops.object.subdivision_set(level=2)
            bpy.context.object.modifiers["Subsurf"].show_on_cage = True
            bpy.ops.object.mode_set(mode='EDIT')
        return {'FINISHED'}


# Remove Subsurf
class RemoveSubsurf(bpy.types.Operator):
    bl_idname = "remove.subsurf"
    bl_label = "Remove Subsurf"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.modifier_remove(modifier="Subsurf")
        return {'FINISHED'}


# Add Mirror Object
class AddMirrorObject(bpy.types.Operator):
    bl_idname = "add.mirrorobject"
    bl_label = "Add Mirror Object"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.modifier_add(type='MIRROR')
        bpy.context.object.modifiers["Mirror"].use_clip = True
        return {'FINISHED'}


# Add Mirror Edit
class AddMirrorEdit(bpy.types.Operator):
    bl_idname = "add.mirroredit"
    bl_label = "Add Mirror Edit"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.modifier_add(type='MIRROR')
        bpy.context.object.modifiers["Mirror"].use_clip = True
        bpy.context.object.modifiers["Mirror"].show_on_cage = True
        return {'FINISHED'}


# Apply Mirror Edit
class ApplyMirrorEdit(bpy.types.Operator):
    bl_idname = "apply.mirroredit"
    bl_label = "Apply Mirror Edit"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.modifier_apply(modifier="Mirror")
        bpy.ops.object.mode_set(mode='EDIT')
        return {'FINISHED'}


# Apply Subsurf Edit
class ApplySubsurfEdit(bpy.types.Operator):
    bl_idname = "apply.subsurfedit"
    bl_label = "Apply Subsurf Edit"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.modifier_apply(modifier="Subsurf")
        bpy.ops.object.mode_set(mode='EDIT')
        return {'FINISHED'}


# wazou Symetrize
class WazouSymetrize(bpy.types.Operator):
    bl_idname = "wazou.symetrize"
    bl_label = "Wazou Symetrize"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.mesh.select_all(action='TOGGLE')
        bpy.ops.mesh.select_all(action='TOGGLE')
        bpy.ops.mesh.symmetrize(direction='POSITIVE_X')
        bpy.ops.mesh.select_all(action='TOGGLE')
        return {'FINISHED'}


# Looptools
class VIEW3D_MT_edit_mesh_looptools(bpy.types.Menu):
    bl_idname = "loop.tools"
    bl_label = "LoopTools"

    def draw(self, context):
        layout = self.layout

        layout.operator("mesh.looptools_bridge", text="Bridge").loft = False
        layout.operator("mesh.looptools_circle")
        layout.operator("mesh.looptools_curve")
        layout.operator("mesh.looptools_flatten")
        layout.operator("mesh.looptools_gstretch")
        layout.operator("mesh.looptools_bridge", text="Loft").loft = True
        layout.operator("mesh.looptools_relax")
        layout.operator("mesh.looptools_space")


# Apply Transforms
class ApplyTransformAll(bpy.types.Operator):
    bl_idname = "apply.transformall"
    bl_label = "Apply Transform All"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        return {'FINISHED'}


# Delete modifiers
class DeleteModifiers(bpy.types.Operator):
    bl_idname = "delete.modifiers"
    bl_label = "Delete modifiers"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selection = bpy.context.selected_objects

        if not(selection):
            for obj in bpy.data.objects:
                for mod in obj.modifiers:
                    bpy.context.scene.objects.active = obj
                    bpy.ops.object.modifier_remove(modifier=mod.name)
        else:
            for obj in selection:
                for mod in obj.modifiers:
                    bpy.context.scene.objects.active = obj
                    bpy.ops.object.modifier_remove(modifier=mod.name)
        return {'FINISHED'}


# Clear All
class ClearAll(bpy.types.Operator):
    bl_idname = "clear.all"
    bl_label = "Clear All"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selection = bpy.context.selected_objects
        bpy.ops.object.location_clear()
        bpy.ops.object.rotation_clear()
        bpy.ops.object.scale_clear()
        return {'FINISHED'}


# Separate Loose Parts
class SeparateLooseParts(bpy.types.Operator):
    bl_idname = "separate.looseparts"
    bl_label = "Separate Loose Parts"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.separate(type='LOOSE')
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='TOGGLE')
        return {'FINISHED'}


# Create Hole
class CreateHole(bpy.types.Operator):
    """This Operator create a hole on a selection"""
    bl_idname = "object.createhole"
    bl_label = "Create Hole on a Selection"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):

        bpy.ops.mesh.extrude_region_move()
        bpy.ops.transform.resize(value=(0.6, 0.6, 0.6))
        bpy.ops.mesh.looptools_circle()
        bpy.ops.mesh.extrude_region_move()
        bpy.ops.transform.resize(value=(0.8, 0.8, 0.8))
        bpy.ops.mesh.delete(type='FACE')
        return {'FINISHED'}


# Symetry Lock X
class SymetryLockX(bpy.types.Operator):
    bl_idname = "object.symetrylockx"
    bl_label = "Symetry Lock X"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if bpy.context.scene.tool_settings.sculpt.use_symmetry_x is True:
            bpy.context.scene.tool_settings.sculpt.use_symmetry_x = False
        elif bpy.context.scene.tool_settings.sculpt.use_symmetry_x is False:
            bpy.context.scene.tool_settings.sculpt.use_symmetry_x = True
        return {'FINISHED'}


# Symetry Lock Y
class SymetryLockY(bpy.types.Operator):
    bl_idname = "object.symetrylocky"
    bl_label = "Symetry Lock Y"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if bpy.context.scene.tool_settings.sculpt.use_symmetry_y is True:
            bpy.context.scene.tool_settings.sculpt.use_symmetry_y = False
        elif bpy.context.scene.tool_settings.sculpt.use_symmetry_y is False:
            bpy.context.scene.tool_settings.sculpt.use_symmetry_y = True
        return {'FINISHED'}


# Symetry Lock Z
class SymetryLockZ(bpy.types.Operator):
    bl_idname = "object.symetrylockz"
    bl_label = "Symetry Lock Z"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if bpy.context.scene.tool_settings.sculpt.use_symmetry_z is True:
            bpy.context.scene.tool_settings.sculpt.use_symmetry_z = False
        elif bpy.context.scene.tool_settings.sculpt.use_symmetry_z is False:
            bpy.context.scene.tool_settings.sculpt.use_symmetry_z = True
        return {'FINISHED'}


# Dyntopo Shading
class DyntopoSmoothShading(bpy.types.Operator):
    bl_idname = "object.dtpsmoothshading"
    bl_label = "Dyntopo Smooth Shading"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if bpy.context.scene.tool_settings.sculpt.use_smooth_shading is True:
            bpy.context.scene.tool_settings.sculpt.use_smooth_shading = False
        elif bpy.context.scene.tool_settings.sculpt.use_smooth_shading is False:
            bpy.context.scene.tool_settings.sculpt.use_smooth_shading = True
        return {'FINISHED'}


# detail Variable Constant
class DetailSizevariable(bpy.types.Operator):
    bl_idname = "object.detailsizevariable"
    bl_label = "Detail Size Variable"
    bl_options = {'REGISTER', 'UNDO'}
    variable = bpy.props.FloatProperty()

    def execute(self, context):
        bpy.context.scene.tool_settings.sculpt.constant_detail = self.variable
        return {'FINISHED'}


# Detail Variable Relative
class DetailSizevariableRelative(bpy.types.Operator):
    bl_idname = "object.detailsizevariablerelative"
    bl_label = "Detail Size Variable  Relative"
    bl_options = {'REGISTER', 'UNDO'}
    variable = bpy.props.FloatProperty()

    def execute(self, context):
        bpy.context.scene.tool_settings.sculpt.detail_size = self.variable
        return {'FINISHED'}


# Detail Type
class DTPDetailType(bpy.types.Operator):
    bl_idname = "object.detailtype"
    bl_label = "Detail Type"
    bl_options = {'REGISTER', 'UNDO'}
    variable = bpy.props.StringProperty()

    def execute(self, context):
        bpy.context.scene.tool_settings.sculpt.detail_type_method = self.variable
        return {'FINISHED'}


# Detail Refine
class DTPDetailRefine(bpy.types.Operator):
    bl_idname = "object.detailrefine"
    bl_label = "Detail Refine"
    bl_options = {'REGISTER', 'UNDO'}
    variable = bpy.props.StringProperty()

    def execute(self, context):
        bpy.context.scene.tool_settings.sculpt.detail_refine_method = self.variable
        return {'FINISHED'}


# Enable Dyntopo
class EnableDyntopo(bpy.types.Operator):
    bl_idname = "enable.dyntopo"
    bl_label = "Enable Dyntopo"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.sculpt.dynamic_topology_toggle()
        bpy.context.scene.tool_settings.sculpt.detail_refine_method = 'SUBDIVIDE_COLLAPSE'
        bpy.context.scene.tool_settings.sculpt.detail_type_method = 'CONSTANT'
        bpy.context.scene.tool_settings.sculpt.use_smooth_shading = True
        return {'FINISHED'}


# Sculpt Symmetrize +X to -X
class SculptSymmetrizePlusX(bpy.types.Operator):
    bl_idname = "sculpt.symmetrizeplusx"
    bl_label = "Sculpt Symmetrize +X to -X"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.sculpt.symmetrize()
        if bpy.context.scene.tool_settings.sculpt.symmetrize_direction == 'NEGATIVE_X':
            bpy.context.scene.tool_settings.sculpt.symmetrize_direction = 'POSITIVE_X'
        return {'FINISHED'}


# Sculpt Symmetrize -X to +X
class SculptSymmetrizeMoinsX(bpy.types.Operator):
    bl_idname = "sculpt.symmetrizemoinsx"
    bl_label = "Sculpt Symmetrize - X to + X"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.sculpt.symmetrize()
        if bpy.context.scene.tool_settings.sculpt.symmetrize_direction == 'POSITIVE_X':
            bpy.context.scene.tool_settings.sculpt.symmetrize_direction = 'NEGATIVE_X'
        return {'FINISHED'}


# Sculpt Use symetry X
class SculptUseSymmetryX(bpy.types.Operator):
    bl_idname = "sculpt.sculptusesymmetryx"
    bl_label = "Sculpt Use symetry X"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if bpy.context.scene.tool_settings.sculpt.use_symmetry_x == (True):
            bpy.context.scene.tool_settings.sculpt.use_symmetry_x = False

        elif bpy.context.scene.tool_settings.sculpt.use_symmetry_x == (False):
            bpy.context.scene.tool_settings.sculpt.use_symmetry_x = True
        return {'FINISHED'}


# Sculpt Use symetry Y
class SculptUseSymmetryY(bpy.types.Operator):
    bl_idname = "sculpt.sculptusesymmetryy"
    bl_label = "Sculpt Use symetry Y"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if bpy.context.scene.tool_settings.sculpt.use_symmetry_y == (True):
            bpy.context.scene.tool_settings.sculpt.use_symmetry_y = False

        elif bpy.context.scene.tool_settings.sculpt.use_symmetry_y == (False):
            bpy.context.scene.tool_settings.sculpt.use_symmetry_y = True
        return {'FINISHED'}


# Sculpt Use symetry Z
class SculptUseSymmetryZ(bpy.types.Operator):
    bl_idname = "sculpt.sculptusesymmetryz"
    bl_label = "Sculpt Use symetry Z"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if bpy.context.scene.tool_settings.sculpt.use_symmetry_z == (True):
            bpy.context.scene.tool_settings.sculpt.use_symmetry_z = False

        elif bpy.context.scene.tool_settings.sculpt.use_symmetry_z == (False):
            bpy.context.scene.tool_settings.sculpt.use_symmetry_z = True
        return {'FINISHED'}


# Pivot to selection
class PivotToSelection(bpy.types.Operator):
    bl_idname = "object.pivot2selection"
    bl_label = "Pivot To Selection"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        saved_location = bpy.context.scene.cursor_location.copy()
        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        bpy.context.scene.cursor_location = saved_location
        return {'FINISHED'}


# Pivot to Bottom
class PivotBottom(bpy.types.Operator):
    bl_idname = "object.pivotobottom"
    bl_label = "Pivot To Bottom"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
        o = bpy.context.active_object
        init = 0
        for x in o.data.vertices:
            if init == 0:
                a = x.co.z
                init = 1
            elif x.co.z < a:
                a = x.co.z

        for x in o.data.vertices:
            x.co.z -= a

        o.location.z += a
        bpy.ops.object.mode_set(mode='EDIT')
        return {'FINISHED'}


# Space
class RetopoSpace(bpy.types.Operator):
    bl_idname = "retopo.space"
    bl_label = "Retopo Space"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.mesh.looptools_space(influence=100, input='selected', interpolation='cubic', lock_x=False, lock_y=False, lock_z=False)
        return {'FINISHED'}


# Freeze and keep pivot
class FreezeAndKeepPivot(bpy.types.Operator):
    bl_idname = "object.freezeandkeeppivot"
    bl_label = "Freeze And Keep Pivot"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Save the cursor first position
        saved_location_0 = bpy.context.scene.cursor_location.copy()
        # Move the cursor to the active origin object
        bpy.ops.view3d.snap_cursor_to_active()
        # Save the cursor position 2
        saved_location = bpy.context.scene.cursor_location.copy()
        # Apply all transforms, that move the origin of the object to 0,0,0
        bpy.ops.apply.transformall()
        # Move the cursor to the second location saved
        bpy.context.scene.cursor_location = saved_location
        # Move the origin to the cursor
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        # Move the cursor to his first location
        bpy.context.scene.cursor_location = saved_location_0
        return {'FINISHED'}


# --------------------------------------------------------------------------
# Particles
# --------------------------------------------------------------------------

# Particle Path Steps
class ParticlePathSteps(bpy.types.Operator):
    bl_idname = "object.particlepathsteps"
    bl_label = "Particle Path Steps"
    bl_options = {'REGISTER', 'UNDO'}
    variable = bpy.props.IntProperty()

    def execute(self, context):
        bpy.context.scene.tool_settings.particle_edit.draw_step = self.variable
        return {'FINISHED'}


# Particle Childrens
class ParticleChildrens(bpy.types.Operator):
    bl_idname = "object.particlechildren"
    bl_label = "Particle Childrens"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if bpy.context.scene.tool_settings.particle_edit.show_particles is True:
            bpy.context.scene.tool_settings.particle_edit.show_particles = False
            bpy.context.area.type = 'VIEW_3D'
        elif bpy.context.scene.tool_settings.particle_edit.show_particles is False:
            bpy.context.scene.tool_settings.particle_edit.show_particles = True
            bpy.context.area.type = 'VIEW_3D'
        return {'FINISHED'}


# Particle Length
class ParticleLength(bpy.types.Operator):
    bl_idname = "object.particlelength"
    bl_label = "Particle Length"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if bpy.context.scene.tool_settings.particle_edit.use_preserve_length is True:
            bpy.context.scene.tool_settings.particle_edit.use_preserve_length = False
            bpy.context.area.type = 'VIEW_3D'
        elif bpy.context.scene.tool_settings.particle_edit.use_preserve_length is False:
            bpy.context.scene.tool_settings.particle_edit.use_preserve_length = True
            bpy.context.area.type = 'VIEW_3D'
        return {'FINISHED'}


# Particle X Mirror
class ParticleXMirror(bpy.types.Operator):
    bl_idname = "object.particlexmirror"
    bl_label = "Particle X Mirror"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if bpy.context.object.data.use_mirror_x is True:
            bpy.context.object.data.use_mirror_x = False
            bpy.context.area.type = 'VIEW_3D'
        elif bpy.context.object.data.use_mirror_x is False:
            bpy.context.object.data.use_mirror_x = True
            bpy.context.area.type = 'VIEW_3D'
        return {'FINISHED'}


# Particle Root
class ParticleRoot(bpy.types.Operator):
    bl_idname = "object.particleroot"
    bl_label = "Particle Root"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if bpy.context.scene.tool_settings.particle_edit.use_preserve_root is True:
            bpy.context.scene.tool_settings.particle_edit.use_preserve_root = False
            bpy.context.area.type = 'VIEW_3D'
        elif bpy.context.scene.tool_settings.particle_edit.use_preserve_root is False:
            bpy.context.scene.tool_settings.particle_edit.use_preserve_root = True
            bpy.context.area.type = 'VIEW_3D'
        return {'FINISHED'}


# Selection Particles Mode
class SelectionParticlesMode(bpy.types.Operator):
    bl_idname = "object.spm"
    bl_label = "Selection Particles Mode"
    bl_options = {'REGISTER', 'UNDO'}
    variable = bpy.props.StringProperty()

    def execute(self, context):
        bpy.context.scene.tool_settings.particle_edit.select_mode = self.variable
        return {'FINISHED'}


# Selection Particles Brushes
class SelectionParticlesBrushes(bpy.types.Operator):
    bl_idname = "object.spb"
    bl_label = "Selection Particles Brushes"
    bl_options = {'REGISTER', 'UNDO'}
    variable = bpy.props.StringProperty()

    def execute(self, context):
        bpy.context.scene.tool_settings.particle_edit.tool = self.variable
        bpy.context.area.type = 'VIEW_3D'
        return {'FINISHED'}


# Particles Interpolate
class ParticlesInterpolate(bpy.types.Operator):
    bl_idname = "object.particleinterpolate"
    bl_label = "Particles Interpolate"
    bl_options = {'REGISTER', 'UNDO'}
    variable = bpy.props.IntProperty()

    def execute(self, context):
        if bpy.context.scene.tool_settings.particle_edit.use_default_interpolate is True:
            bpy.context.scene.tool_settings.particle_edit.use_default_interpolate = False
            bpy.context.area.type = 'VIEW_3D'
        elif bpy.context.scene.tool_settings.particle_edit.use_default_interpolate is False:
            bpy.context.scene.tool_settings.particle_edit.use_default_interpolate = True
            bpy.context.area.type = 'VIEW_3D'
        return {'FINISHED'}


# Make Object An Empty
class MakeObjectAnEmpty(bpy.types.Operator):
    bl_idname = "object.makeempty"
    bl_label = "Make Object An Empty"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if bpy.context.object.hide_render is False:
            bpy.context.object.hide_render = True
            bpy.context.object.draw_type = 'WIRE'
            bpy.context.object.cycles_visibility.camera = False
            bpy.context.object.cycles_visibility.diffuse = False
            bpy.context.object.cycles_visibility.glossy = False
            bpy.context.object.cycles_visibility.scatter = False
            bpy.context.object.cycles_visibility.transmission = False
            bpy.context.object.cycles_visibility.shadow = False
        elif bpy.context.object.hide_render is True:
            bpy.context.object.hide_render = False
            bpy.context.object.draw_type = 'SOLID'
            bpy.context.object.cycles_visibility.camera = True
            bpy.context.object.cycles_visibility.diffuse = True
            bpy.context.object.cycles_visibility.glossy = True
            bpy.context.object.cycles_visibility.scatter = True
            bpy.context.object.cycles_visibility.transmission = True
            bpy.context.object.cycles_visibility.shadow = True
        return {'FINISHED'}


# Clear Empty
class ClearEmpty(bpy.types.Operator):
    bl_idname = "object.clearempty"
    bl_label = "Clear Empty"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        C = bpy.context
        for obj in C.object.children:
            obj.select = True
            bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
            bpy.ops.object.select_all(action='TOGGLE')
        return {'FINISHED'}


# Mark Seam
class MarkSeam(bpy.types.Operator):
    bl_idname = "mark.seam"
    bl_label = "Mark Seam"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.mesh.mark_seam()
        return {'FINISHED'}


# Clear Seam
class ClearSeam(bpy.types.Operator):
    bl_idname = "clear.seam"
    bl_label = "Clear Seam"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.mesh.mark_seam(clear=True)
        return {'FINISHED'}


# Join - Separate
class Join_Separate(bpy.types.Operator):
    bl_idname = "join.separate"
    bl_label = "Join Separate"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if len(bpy.context.selected_objects) == 1:
            bpy.ops.separate.looseparts()
            bpy.context.active_object.select = True
        else:
            bpy.ops.Object.join()

        return {'FINISHED'}


# Simplify Circle
class Simplify_Circle(bpy.types.Operator):
    bl_idname = "simplify.circle"
    bl_label = "Simplify Circle"
    bl_description = ""
    bl_options = {"REGISTER", 'UNDO'}

    def execute(self, context):
        bpy.ops.mesh.select_nth()
        bpy.ops.mesh.edge_collapse()
        return {"FINISHED"}


######################
#        Pies        #
######################

# Pie Sculpt Mirror
class PieSculptMirror(Menu):
    bl_idname = "pie.sculptmirror"
    bl_label = "Pie Sculpt Mirror"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        sculpt = context.tool_settings.sculpt
        # 4 - LEFT
        pie.operator("sculpt.symmetrizemoinsx", text="-X to +X", icon='TRIA_RIGHT')
        # 6 - RIGHT
        pie.operator("sculpt.symmetrizeplusx", text="+X to -X", icon='TRIA_LEFT')
        # 2 - BOTTOM
        if bpy.context.scene.tool_settings.sculpt.use_symmetry_y == (True):
            pie.operator("sculpt.sculptusesymmetryy", text="Unlock Y", icon='LOCKED')
        else:
            pie.operator("sculpt.sculptusesymmetryy", text="Lock Y", icon='UNLOCKED')
        # 8 - TOP
        pie.operator("object.symetrylocky", text="Symmetrize Y", icon='MOD_MIRROR')
        # 7 - TOP - LEFT
        pie.operator("object.symetrylockx", text="Symmetrize X", icon='MOD_MIRROR')
        # 9 - TOP - RIGHT
        pie.operator("object.symetrylockz", text="Symmetrize Z", icon='MOD_MIRROR')
        # 1 - BOTTOM - LEFT
        if bpy.context.scene.tool_settings.sculpt.use_symmetry_x == (True):
            pie.operator("sculpt.sculptusesymmetryx", text="Unlock X", icon='LOCKED')
        else:
            pie.operator("sculpt.sculptusesymmetryx", text="Lock X", icon='UNLOCKED')
        # 3 - BOTTOM - RIGHT
        if bpy.context.scene.tool_settings.sculpt.use_symmetry_z == (True):
            pie.operator("sculpt.sculptusesymmetryz", text="Unlock Z", icon='LOCKED')
        else:
            pie.operator("sculpt.sculptusesymmetryz", text="Lock Z", icon='UNLOCKED')


# Pie Particle Brushes
class PieParticleBrushes(Menu):
    bl_idname = "pie.particleparameters"
    bl_label = "Pie Particle Parameters"

    def draw(self, context):
        layout = self.layout

        pie = layout.menu_pie()
        # 4 - LEFT
        pie.operator("object.spm", text="Path", icon='PARTICLE_PATH').variable = 'PATH'
        # 6 - RIGHT
        pie.operator("object.spm", text="Point", icon='PARTICLE_POINT').variable = 'POINT'
        # 2 - BOTTOM
        pie.operator("object.spm", text="Tip", icon='PARTICLE_TIP').variable = 'TIP'
        # 8 - TOP
        pie.operator("wm.call_menu_pie", text="Brushes", icon='BRUSH_DATA').name = "pie.particlebrushes"
        # 7 - TOP - LEFT
        pie.operator("wm.call_menu_pie", text="Options", icon='SCRIPTWIN').name = "pie.particleoptions"
        # 9 - TOP - RIGHT
        if bpy.context.scene.tool_settings.particle_edit.show_particles == (True):
            pie.operator("object.particlechildren", text="Chidren OFF", icon='HAIR')
        else:
            pie.operator("object.particlechildren", text="Chidren ON", icon='HAIR')
        # 1 - BOTTOM - LEFT
        if bpy.context.scene.tool_settings.particle_edit.use_default_interpolate == (True):
            pie.operator("object.particleinterpolate", text="Interpolate OFF", icon='HAIR')
        else:
            pie.operator("object.particleinterpolate", text="Interpolate ON", icon='HAIR')
        # 3 - BOTTOM - RIGHT
        if bpy.context.space_data.use_occlude_geometry == (True):
            pie.operator("wm.context_toggle", text="Occlude Geo ON", icon="ORTHO").data_path = "space_data.use_occlude_geometry"
        else:
            pie.operator("wm.context_toggle", text="Occlude Geo OFF", icon="ORTHO").data_path = "space_data.use_occlude_geometry"


# Pie Particle Options
class PieParticleOptions(Menu):
    bl_idname = "pie.particleoptions"
    bl_label = "Pie Particle Options"

    def draw(self, context):
        layout = self.layout

        pie = layout.menu_pie()
        # 4 - LEFT
        pie.operator("object.particlepathsteps", text="Path Steps = 6", icon='PARTICLE_POINT').variable = 6
        # 6 - RIGHT
        pie.operator("object.particlepathsteps", text="Path Steps = 2", icon='PARTICLE_POINT').variable = 2
        # 2 - BOTTOM
        pie.operator("object.particlepathsteps", text="Path Steps = 4", icon='PARTICLE_POINT').variable = 4
        # 8 - TOP
        if bpy.context.scene.tool_settings.particle_edit.use_preserve_length == (True):
            pie.operator("object.particlelength", text="Keep Lengths OFF", icon='RNDCURVE')
        else:
            pie.operator("object.particlelength", text="Keep Lengths ON", icon='RNDCURVE')
        # 7 - TOP - LEFT
        if bpy.context.object.data.use_mirror_x == (True):
            pie.operator("object.particlexmirror", text="X Mirror OFF", icon='MOD_MIRROR')
        else:
            pie.operator("object.particlexmirror", text="X Mirror ON", icon='MOD_MIRROR')
        # 9 - TOP - RIGHT
        if bpy.context.scene.tool_settings.particle_edit.use_preserve_root == (True):
            pie.operator("object.particleroot", text="Keep Root OFF", icon='LAYER_ACTIVE')
        else:
            pie.operator("object.particleroot", text="Keep Root ON", icon='LAYER_ACTIVE')
        # 1 - BOTTOM - LEFT
        pie.operator("object.particlepathsteps", text="Path Steps = 5", icon='PARTICLE_POINT').variable = 5
        # 3 - BOTTOM - RIGHT
        pie.operator("object.particlepathsteps", text="Path Steps = 3", icon='PARTICLE_POINT').variable = 3


########################################################################

########################################################################
# RMB
class View3dRightClicMenu(Menu):
    bl_idname = "pie.rightclicmenu"
    bl_label = "Right Clic Menu"

    def draw(self, context):
        layout = self.layout

        pie = layout.menu_pie()

        ################################################
        # No Objects                                   #
        ################################################
        if bpy.context.area.type == 'VIEW_3D' and not bpy.context.object:

            # 4 - LEFT
            pie.operator("wm.read_homefile", text="New", icon='NEW')
            # 6 - RIGHT
            box = pie.split().column()
            row = box.split(align=True)
            box.operator("wm.recover_last_session", text="Recover Last Session", icon='RECOVER_LAST')
            box.operator("wm.recover_auto_save", text="Recover auto Save", icon='RECOVER_AUTO')
            # 2 - BOTTOM
            box = pie.split().column()
            row = box.split(align=True)
            row.operator("mesh.primitive_cube_add", text="", icon='MESH_CUBE')
            row.operator("mesh.primitive_plane_add", text="", icon='MESH_PLANE')
            row.operator("mesh.primitive_uv_sphere_add", text="", icon='MESH_UVSPHERE')
            row.operator("mesh.primitive_cylinder_add", text="", icon='MESH_CYLINDER')
            row = box.row(align=True)
            row = box.split(align=True)
            row.operator("mesh.primitive_grid_add", text=" ", icon='MESH_GRID')
            row.operator("mesh.primitive_circle_add", text=" ", icon='MESH_CIRCLE')
            row.operator("mesh.primitive_cone_add", text=" ", icon='MESH_CONE')
            row.operator("mesh.primitive_torus_add", text=" ", icon='MESH_TORUS')
            row = box.row(align=True)
            row = box.split(align=True)
            row.operator("object.camera_add", text="", icon='OUTLINER_OB_CAMERA')
            row.operator("object.lamp_add", text="", icon='LAMP_AREA').type = 'AREA'
            row.operator("object.lamp_add", text="", icon='LAMP_SUN').type = 'SUN'
            row.operator("object.lamp_add", text="", icon='LAMP_HEMI').type = 'HEMI'
            box.menu("AddMenu", text="Objects", icon="OBJECT_DATA")
            # 8 - TOP
            pie.operator("wm.save_mainfile", text="Save", icon='FILE_TICK')
            # 7 - TOP - LEFT
            pie.operator("wm.open_mainfile", text="Open file", icon='FILE_FOLDER')
            # 9 - TOP - RIGHT
            pie.operator("wm.save_as_mainfile", text="Save As...", icon='SAVE_AS')
            # 1 - BOTTOM - LEFT
            box = pie.split().column()
            row = box.split(align=True)
            row.operator("import_scene.obj", text="Imp OBJ", icon='IMPORT')
            row.operator("export_scene.obj", text="Exp OBJ", icon='EXPORT')
            row = box.row(align=True)
            row = box.split(align=True)
            row.operator("import_scene.fbx", text="Imp FBX", icon='IMPORT')
            row.operator("export_scene.fbx", text="Exp FBX", icon='EXPORT')
            # 3 - BOTTOM - RIGHT
            box = pie.split().column()
            row = box.split(align=True)
            row.operator("wm.link", text="Link", icon='LINK_BLEND')
            row.operator("wm.append", text="Append", icon='APPEND_BLEND')

        ################################################
        # Object Mode                                  #
        ################################################
        elif bpy.context.area.type == 'VIEW_3D' and bpy.context.object.mode == 'OBJECT':
            # 4 - LEFT

            selection = bpy.context.selected_objects

            if len(bpy.context.selected_objects) == 1:
                pie.operator("join.separate", text="Separate", icon='FULLSCREEN_ENTER')

            else:
                pie.operator("join.separate", text="Join", icon='FULLSCREEN_EXIT')

            # 6 - RIGHT
            is_subsurf = False
            for mode in bpy.context.object.modifiers:
                if mode.type == 'SUBSURF':
                    is_subsurf = True
            if is_subsurf is True:
                pie.operator("remove.subsurf", text="Remove Subsurf", icon='X')
            else:
                pie.operator("object.subsurf2", text="Add Subsurf", icon='MOD_SUBSURF')

            # 2 - BOTTOM
            box = pie.split().column()
            row = box.split(align=True)
            row.operator("mesh.primitive_cube_add", text="", icon='MESH_CUBE')
            row.operator("mesh.primitive_plane_add", text="", icon='MESH_PLANE')
            row.operator("mesh.primitive_uv_sphere_add", text="", icon='MESH_UVSPHERE')
            row.operator("mesh.primitive_cylinder_add", text="", icon='MESH_CYLINDER')
            row = box.row(align=True)
            row = box.split(align=True)
            row.operator("mesh.primitive_grid_add", text=" ", icon='MESH_GRID')
            row.operator("mesh.primitive_circle_add", text=" ", icon='MESH_CIRCLE')
            row.operator("mesh.primitive_cone_add", text=" ", icon='MESH_CONE')
            row.operator("mesh.primitive_torus_add", text=" ", icon='MESH_TORUS')
            row = box.row(align=True)
            row = box.split(align=True)
            row.operator("object.camera_add", text="", icon='OUTLINER_OB_CAMERA')
            row.operator("object.lamp_add", text="", icon='LAMP_AREA').type = 'AREA'
            row.operator("object.lamp_add", text="", icon='LAMP_SUN').type = 'SUN'
            row.operator("object.lamp_add", text="", icon='LAMP_HEMI').type = 'HEMI'
            box.menu("AddMenu", text="Objects", icon="OBJECT_DATA")
            # 8 - TOP
            pie.operator("screen.redo_last", text="F6", icon='SCRIPTWIN')
            # 7 - TOP - LEFT
            box = pie.split().column()
            row = box.split(align=True)
            is_mirror = False
            for mode in bpy.context.object.modifiers:
                if mode.type == 'MIRROR':
                    is_mirror = True
            if is_mirror is True:
                row.operator("object.modifier_remove", text="Del Mirror", icon='X').modifier = "Mirror"
            else:
                row.operator("add.mirrorobject", text="Add Mirror", icon='MOD_MIRROR')

            row.operator("object.automirror", icon='MOD_MIRROR')
            row = box.row(align=True)
            row = box.split(align=True)
            row.operator("object.modifier_apply", text="Apply Mirror", icon='FILE_TICK').modifier = "Mirror"
            row = box.row(align=True)
            row.operator_menu_enum("object.modifier_add", "type")
            row.operator("delete.modifiers", text="Del Modifiers", icon='X')
            # 9 - TOP - RIGHT
            box = pie.split().column()
            row = box.row(align=True)
            row.operator("object.origin_set", text="O To Cursor", icon='CURSOR').type = 'ORIGIN_CURSOR'
            row.operator("object.origin_set", text="O To COM", icon='CLIPUV_HLT').type = 'ORIGIN_CENTER_OF_MASS'
            row = box.row(align=True)
            row.operator("object.origin_set", text="Origin To Geo", icon='ROTATE').type = 'ORIGIN_GEOMETRY'
            row.operator("object.origin_set", text="Geo To Origin", icon='BBOX').type = 'GEOMETRY_ORIGIN'
            row = box.row(align=True)
            row.operator("view3d.snap_selected_to_cursor", text="Sel to Cursor", icon='CLIPUV_HLT').use_offset = False
            row.operator("view3d.snap_cursor_to_selected", text="Cursor to Sel", icon='ROTACTIVE')
            row = box.row(align=True)
            row.operator("object.pivot2selection", text="Origin To Sel", icon='SNAP_INCREMENT')
            row.operator("object.pivotobottom", text="Origin To Bottom", icon='TRIA_DOWN')
            # 1 - BOTTOM - LEFT
            box = pie.split().column()
            row = box.row(align=True)

            row.operator("object.freezeandkeeppivot", text="Apply T Keep Origin", icon='FILE_TICK')
            row = box.row(align=True)
            row.operator("apply.transformall", text="Apply T", icon='FILE_TICK')
            row.operator("clear.all", text="Clear All", icon='MANIPUL')
            # 3 - BOTTOM - RIGHT
            box = pie.split().column()
            row = box.row(align=True)
            row.operator("object.modifier_apply", text="Apply Subsurf", icon='FILE_TICK').modifier = "Subsurf"
            row = box.row(align=True)
            if bpy.context.object.hide_render is False:
                row.operator("object.makeempty", text="Make Empty", icon='OUTLINER_OB_EMPTY')
                row.operator("object.clearempty", text="Clear Empty", icon='MESH_DATA')
            else:
                row.operator("object.makeempty", text="Make Normal", icon='MESH_CUBE')
                row.operator("object.clearempty", text="Clear Empty", icon='MESH_DATA')

        ################################################
        # Edit Mode                                    #
        ################################################
        elif bpy.context.object.mode == 'EDIT':

            # 4 - LEFT
            box = pie.split().column()
            row = box.split(align=True)
            row.operator("mesh.subdivide", text="Subdivide", icon='GRID').smoothness = 0
            row.operator("mesh.vertices_smooth", text="Smooth", icon='UV_VERTEXSEL')
            row = box.row(align=True)
            row = box.split(align=True)
            row.operator("wm.context_toggle", text="Mirror X ", icon='MOD_MIRROR').data_path = "object.data.use_mirror_x"
            row.operator("wazou.symetrize", text="Symetrize", icon='UV_EDGESEL')
            row = box.row(align=True)
            row = box.split(align=True)
            row.operator("mesh.ext_cut_faces", text="Cut Faces", icon='MOD_DECIM')
            row = box.row(align=True)
            row = box.split(align=True)
            row.operator("simplify.circle", text="Simplify Circle", icon='MESH_CIRCLE')

            # 6 - RIGHT
            is_subsurf1 = False
            for mode in bpy.context.object.modifiers:
                if mode.type == 'SUBSURF':
                    is_subsurf1 = True
            if is_subsurf1 is True:
                pie.operator("remove.subsurf", text="Remove Subsurf", icon='X')
            else:
                pie.operator("object.subsurf2", text="Add Subsurf", icon='MOD_SUBSURF')
            # 2 - BOTTOM
            box = pie.split().column()
            row = box.row(align=True)
            # Vertex
            if tuple(bpy.context.tool_settings.mesh_select_mode) == (True, False, False):
                box.label("Merge at:")
                row = box.row(align=True)
                row = box.split(align=True)
                row.operator("mesh.merge", text="First", icon='AUTOMERGE_ON').type = 'FIRST'
                row.operator("mesh.merge", text="Center", icon='AUTOMERGE_ON').type = 'CENTER'
                row.operator("mesh.merge", text="Last", icon='AUTOMERGE_ON').type = 'LAST'
            # Edges
            if tuple(bpy.context.tool_settings.mesh_select_mode) == (False, True, False):
                box.label("Merge at:")
                row = box.row(align=True)
                row = box.split(align=True)
                row.operator("mesh.merge", text="Cursor", icon='CURSOR').type = 'CURSOR'
                row.operator("mesh.merge", text="Center", icon='AUTOMERGE_ON').type = 'CENTER'
                row.operator("mesh.merge", text="Collapse", icon='AUTOMERGE_ON').type = 'COLLAPSE'
            # Faces
            if tuple(bpy.context.tool_settings.mesh_select_mode) == (False, False, True):
                box.label("Merge at:")
                row = box.row(align=True)
                row = box.split(align=True)
                row.operator("mesh.merge", text="Cursor", icon='CURSOR').type = 'CURSOR'
                row.operator("mesh.merge", text="Center", icon='AUTOMERGE_ON').type = 'CENTER'
                row.operator("mesh.merge", text="Collapse", icon='AUTOMERGE_ON').type = 'COLLAPSE'
            # 8 - TOP
            pie.operator("screen.redo_last", text="F6", icon='SCRIPTWIN')
            # 7 - TOP - LEFT
            box = pie.split().column()
            row = box.split(align=True)
            is_mirror1 = False
            for mode in bpy.context.object.modifiers:
                if mode.type == 'MIRROR':
                    is_mirror1 = True
            if is_mirror1 is True:
                row.operator("object.modifier_remove", text="Del Mirror", icon='X_VEC').modifier = "Mirror"

            else:
                row.operator("add.mirroredit", text="Add Mirror", icon='MOD_MIRROR')

            row.operator("object.automirror", icon='MOD_MIRROR')
            row = box.row(align=True)
            row = box.split(align=True)
            row.operator("apply.mirroredit", text="Apply Mirror", icon='FILE_TICK')
            row.operator("apply.subsurfedit", text="Apply Sub", icon='FILE_TICK')
            row = box.row(align=True)
            row.operator_menu_enum("object.modifier_add", "type")
            row.operator("delete.modifiers", text="Del Modifiers", icon='X')
            # 9 - TOP - RIGHT
            box = pie.split().column()
            row = box.split(percentage=0.6)
            row.operator("mesh.offset_edges", text="Offset Edges", icon='UV_EDGESEL')
            row.menu("loop.tools")
            row = box.row(align=True)
            row = box.split(align=True)
            row.operator("mesh.poke", text="Poke Faces")
            row.operator("mesh.fill_grid", text="Grid Fill")
            row = box.row(align=True)
            row = box.split(align=True)
            row.operator("mark.seam", "Mark Seam", icon='UV_EDGESEL')
            row.operator("clear.seam", "Clear Seam", icon='UV_EDGESEL')
            # 1 - BOTTOM - LEFT
            box = pie.split().column()
            row = box.split(align=True)
            row.operator("mesh.loopcut", text="Loopcut", icon='EDIT_VEC').smoothness = 1
            row.operator("mesh.inset", text="Inset  ", icon='EDIT_VEC').use_select_inset = False
            row.operator("object.createhole", text="Hole", icon='CLIPUV_DEHLT')
            row = box.row(align=True)
            row = box.split(align=True)
            row.operator("mesh.vertex_align", icon='ALIGN', text="Align")
            row.operator("retopo.space", icon='ALIGN', text="Distribute")
            row.operator("mesh.vertex_inline", icon='ALIGN', text="Ali & Dis")

            # 3 - BOTTOM - RIGHT
            box = pie.split().column()
            row = box.split(align=True)
            row.operator("mesh.flip_normals", text="Flip N", icon='FILE_REFRESH')
            row.operator("mesh.normals_make_consistent", text="consistant", icon='MATCUBE')
            row = box.row(align=True)
            row = box.split(align=True)
            row.operator("wm.context_toggle", text="Show Norms", icon='FACESEL').data_path = "object.data.show_normal_face"
            row.operator("mesh.remove_doubles", text="rem D2l", icon='X')
            row = pie.split().column()
            row = box.split(align=True)
            row.operator("mesh.separate")
            row.menu("AddMenu", text="Add Obj", icon="OBJECT_DATA")

        ################################################
        # Sculpt                                       #
        ################################################
        elif bpy.context.area.type == 'VIEW_3D' and bpy.context.object.mode == 'SCULPT':

            # ------Dyntopo

            if context.sculpt_object.use_dynamic_topology_sculpting:
                # 4 - LEFT
                pie.operator("sculpt.dynamic_topology_toggle", icon='X', text="Disable Dyntopo")
                # 6 - RIGHT
                box = pie.split().column()
                row = box.split(align=True)

                row.label(text="Curves:")

                row = box.row(align=True)
                row = box.split(align=True)
                row.operator("brush.curve_preset", icon='SMOOTHCURVE', text="").shape = 'SMOOTH'
                row.operator("brush.curve_preset", icon='SPHERECURVE', text="").shape = 'ROUND'
                row.operator("brush.curve_preset", icon='ROOTCURVE', text="").shape = 'ROOT'
                row.operator("brush.curve_preset", icon='SHARPCURVE', text="").shape = 'SHARP'
                row.operator("brush.curve_preset", icon='LINCURVE', text="").shape = 'LINE'
                row.operator("brush.curve_preset", icon='NOCURVE', text="").shape = 'MAX'

                # 2 - BOTTOM
                brush = context.tool_settings.sculpt.brush
                capabilities = brush.sculpt_capabilities
                if capabilities.has_auto_smooth:
                    col = pie.column()
                    row = col.row(align=True)

                    row.prop(brush, "auto_smooth_factor", slider=True)
                    row.prop(brush, "use_inverse_smooth_pressure", toggle=True, text="")

                    # normal_weight
                if capabilities.has_normal_weight:

                    row = col.row(align=True)
                    row.prop(brush, "normal_weight", slider=True)

                # crease_pinch_factor
                if capabilities.has_pinch_factor:

                    row = col.row(align=True)
                    row.prop(brush, "crease_pinch_factor", slider=True, text="Pinch")

                # use_original_normal and sculpt_plane
                if capabilities.has_sculpt_plane:

                    row = col.row(align=True)

                    row.prop(brush, "use_original_normal", toggle=True, icon_only=True)

                    row.prop(brush, "sculpt_plane", text="")

                if brush.sculpt_tool == 'MASK':
                    col.prop(brush, "mask_tool", text="")

                # plane_offset, use_offset_pressure, use_plane_trim, plane_trim
                if capabilities.has_plane_offset:
                    row = col.row(align=True)
                    row.prop(brush, "plane_offset", slider=True)
                    row.prop(brush, "use_offset_pressure", text="")

                    # Col.separator()

                    row = col.row()
                    row.prop(brush, "use_plane_trim", text="Trim")
                    row = col.row()
                    row.active = brush.use_plane_trim
                    row.prop(brush, "plane_trim", slider=True, text="Distance")

                # height
                if capabilities.has_height:
                    row = col.row()
                    row.prop(brush, "height", slider=True, text="Height")

                # use_frontface
                row = col.row()
                row.prop(brush, "use_frontface", text="Front Faces Only")

                # use_accumulate
                if capabilities.has_accumulate:
                    col.prop(brush, "use_accumulate")

                # 8 - TOP
                ups = context.tool_settings.unified_paint_settings
                brush = context.tool_settings.sculpt.brush

                col = pie.column(align=True)
                col.prop(ups, "size", text="Radius", slider=False)
                col.prop(brush, "strength", slider=True)

                # 7 - TOP - LEFT
                if bpy.context.tool_settings.sculpt.detail_type_method == 'CONSTANT':

                    sculpt = context.tool_settings.sculpt

                    col = pie.column(align=True)
                    col.operator("sculpt.sample_detail_size", text="Pick Detail Size", icon='EYEDROPPER')
                    col.prop(sculpt, "constant_detail")
                    col.prop(sculpt, "detail_refine_method", text="")
                    col.prop(sculpt, "detail_type_method", text="")

                elif bpy.context.tool_settings.sculpt.detail_type_method == 'RELATIVE':

                    toolsettings = context.tool_settings
                    sculpt_relative = toolsettings.sculpt
                    sculpt = context.tool_settings.sculpt

                    col = pie.column(align=True)
                    col.prop(sculpt_relative, "detail_size")
                    col.prop(sculpt, "detail_refine_method", text="")
                    col.prop(sculpt, "detail_type_method", text="")

                # 9 - TOP - RIGHT
                col = pie.column(align=True)
                col.operator("sculpt.optimize", text="Optimize")
                col.operator("sculpt.detail_flood_fill", text="Detail flood Fill")
                if bpy.context.scene.tool_settings.sculpt.use_smooth_shading is True:
                    col.operator("object.dtpsmoothshading", text="flat Shading", icon='MESH_ICOSPHERE')
                else:
                    col.operator("object.dtpsmoothshading", text="Smooth Shading", icon='SOLID')

                # 1 - BOTTOM - LEFT
                sculpt = context.tool_settings.sculpt
                box = pie.split().column()
                row = box.split(align=True)
                row.operator("wm.call_menu_pie", text="Symmetrize/Lock", icon='MOD_MIRROR').name = "pie.sculptmirror"
                row = box.row(align=True)
                row = box.split(align=True)
                row.prop(sculpt, "use_symmetry_x", text="X", toggle=True)
                row.prop(sculpt, "use_symmetry_y", text="Y", toggle=True)
                row.prop(sculpt, "use_symmetry_z", text="Z", toggle=True)
                # 3 - BOTTOM - RIGHT
                box = pie.split().column()
                row = box.split(align=True)

                row.label(text="Stroke Method:")
                row = box.row(align=True)
                row = box.split(align=True)
                row.prop(brush, "stroke_method", text="", icon='IPO_CONSTANT')

            # ------Normal Sculpt

            else:

                # 4 - LEFT
                pie.operator("enable.dyntopo", text="Enable Dyntopo", icon='LINE_DATA')
                # 6 - RIGHT
                box = pie.split().column()
                row = box.split(align=True)

                row.label(text="Curves:")

                row = box.row(align=True)
                row = box.split(align=True)
                row.operator("brush.curve_preset", icon='SMOOTHCURVE', text="").shape = 'SMOOTH'
                row.operator("brush.curve_preset", icon='SPHERECURVE', text="").shape = 'ROUND'
                row.operator("brush.curve_preset", icon='ROOTCURVE', text="").shape = 'ROOT'
                row.operator("brush.curve_preset", icon='SHARPCURVE', text="").shape = 'SHARP'
                row.operator("brush.curve_preset", icon='LINCURVE', text="").shape = 'LINE'
                row.operator("brush.curve_preset", icon='NOCURVE', text="").shape = 'MAX'

                # 2 - BOTTOM

                brush = context.tool_settings.sculpt.brush
                capabilities = brush.sculpt_capabilities
                if capabilities.has_auto_smooth:
                    col = pie.column()
                    row = col.row(align=True)

                    row.prop(brush, "auto_smooth_factor", slider=True)
                    row.prop(brush, "use_inverse_smooth_pressure", toggle=True, text="")

                    # normal_weight
                if capabilities.has_normal_weight:

                    row = col.row(align=True)
                    row.prop(brush, "normal_weight", slider=True)

                # crease_pinch_factor
                if capabilities.has_pinch_factor:

                    row = col.row(align=True)
                    row.prop(brush, "crease_pinch_factor", slider=True, text="Pinch")

                # use_original_normal and sculpt_plane
                if capabilities.has_sculpt_plane:

                    row = col.row(align=True)

                    row.prop(brush, "use_original_normal", toggle=True, icon_only=True)

                    row.prop(brush, "sculpt_plane", text="")

                # If brush.sculpt_tool == 'MASK':

                    # Row = col.row(align=True)
                    # Row.prop(brush, "mask_tool", text="")

                # plane_offset, use_offset_pressure, use_plane_trim, plane_trim
                if capabilities.has_plane_offset:
                    row = col.row(align=True)
                    row.prop(brush, "plane_offset", slider=True)
                    row.prop(brush, "use_offset_pressure", text="")

                    # Col.separator()

                    row = col.row()
                    row.prop(brush, "use_plane_trim", text="Trim")
                    row = col.row()
                    row.active = brush.use_plane_trim
                    row.prop(brush, "plane_trim", slider=True, text="Distance")

                # height
                if capabilities.has_height:
                    row = col.row()
                    row.prop(brush, "height", slider=True, text="Height")

                # use_frontface
                row = col.row()
                row.prop(brush, "use_frontface", text="Front Faces Only")

                # use_accumulate
                if capabilities.has_accumulate:
                    col.prop(brush, "use_accumulate")

                # 8 - TOP
                ups = context.tool_settings.unified_paint_settings
                brush = context.tool_settings.sculpt.brush

                col = pie.column(align=True)
                col.prop(ups, "size", text="Radius", slider=False)
                col.prop(brush, "strength", slider=True)

                # 7 - TOP - LEFT
                sculpt = context.tool_settings.sculpt
                box = pie.split().column()
                row = box.split(align=True)
                row.label(text="Symmetry:")
                row = box.row(align=True)
                row = box.split(align=True)
                row.prop(sculpt, "use_symmetry_x", text="X", toggle=True)
                row.prop(sculpt, "use_symmetry_y", text="Y", toggle=True)
                row.prop(sculpt, "use_symmetry_z", text="Z", toggle=True)

                # 9 - TOP - RIGHT
                box = pie.split().column()
                row = box.split(align=True)

                row.label(text="Stroke Method:")
                row = box.row(align=True)
                row = box.split(align=True)
                row.prop(brush, "stroke_method", text="", icon='IPO_CONSTANT')

                # 1 - BOTTOM - LEFT

                # 3 - BOTTOM - RIGHT

        ################################################
        # Particles                                    #
        ################################################
        elif bpy.context.area.type == 'VIEW_3D' and bpy.context.object.mode == 'PARTICLE_EDIT':
            # 4 - LEFT
            pie.operator("object.spb", text="Smooth", icon='BRUSH_DATA').variable = 'SMOOTH'
            # 6 - RIGHT
            pie.operator("object.spb", text="Length", icon='BRUSH_DATA').variable = 'LENGTH'
            # 2 - BOTTOM
            pie.operator("object.spb", text="Puff", icon='BRUSH_DATA').variable = 'PUFF'
            # 8 - TOP
            pie.operator("object.spb", text="Comb", icon='BRUSH_DATA').variable = 'COMB'
            # 7 - TOP - LEFT
            pie.operator("object.spb", text="Add", icon='BRUSH_DATA').variable = 'ADD'
            # 9 - TOP - RIGHT
            pie.operator("object.spb", text="Cut", icon='BRUSH_DATA').variable = 'CUT'
            # 1 - BOTTOM - LEFT
            pie.operator("object.spb", text="None", icon='BRUSH_DATA').variable = 'NONE'
            # 3 - BOTTOM - RIGHT
            pie.operator("object.spb", text="Weight", icon='BRUSH_DATA').variable = 'WEIGHT'


addon_keymaps = []


def register():
    bpy.utils.register_module(__name__)

    # Keymap Config

    wm = bpy.context.window_manager

    if wm.keyconfigs.addon:

        # Set 3d cursor with double click LMB
        km = bpy.context.window_manager.keyconfigs.addon.keymaps.new("3D View", space_type="VIEW_3D")
        kmi = km.keymap_items.new('view3d.cursor3d', 'LEFTMOUSE', 'DOUBLE_CLICK', alt=True)

        # Right Clic
        km = wm.keyconfigs.addon.keymaps.new(name='3D View Generic', space_type='VIEW_3D')
        kmi = km.keymap_items.new('wm.call_menu_pie', 'ACTIONMOUSE', 'PRESS')
        kmi.properties.name = "pie.rightclicmenu"
        kmi.active = True
        addon_keymaps.append((km, kmi))

        # ALT + Right Clic
        km = wm.keyconfigs.addon.keymaps.new(name='3D View Generic', space_type='VIEW_3D')
        kmi = km.keymap_items.new('wm.call_menu_pie', 'ACTIONMOUSE', 'PRESS', alt=True)
        kmi.properties.name = "pie.particleparameters"
        kmi.active = True
        addon_keymaps.append((km, kmi))


def unregister():
    bpy.utils.unregister_module(__name__)
    wm = bpy.context.window_manager

    if wm.keyconfigs.addon:
        for km in addon_keymaps:
            for kmi in km.keymap_items:
                km.keymap_items.remove(kmi)

            wm.keyconfigs.addon.keymaps.remove(km)

    # clear the list
    del addon_keymaps[:]


if __name__ == "__main__":
    register()

    # Bpy.ops.wm.call_menu_pie(name="View3dRightClicMenu")
