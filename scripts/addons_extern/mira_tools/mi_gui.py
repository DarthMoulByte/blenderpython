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

import bpy


class MI_ExtrudePanel(bpy.types.Panel):
    bl_label = "Modify"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_context = "mesh_edit"
    bl_category = 'Mira'

    def draw(self, context):
        layout = self.layout
        extrude_settings = context.scene.mi_extrude_settings

        layout.operator("mira.draw_extrude", text="Draw Extrude")

        layout.prop(extrude_settings, "extrude_mode", text='Mode')

        layout.prop(extrude_settings, "extrude_step_type", text='Step')
        if extrude_settings.extrude_step_type == 'Asolute':
            layout.prop(extrude_settings, "absolute_extrude_step", text='')
        else:
            layout.prop(extrude_settings, "relative_extrude_step", text='')

        if extrude_settings.extrude_mode == 'Screen':
            layout.prop(extrude_settings, "do_symmetry", text='Symmetry')
            if extrude_settings.do_symmetry:
                layout.prop(extrude_settings, "symmetry_axys", text='Axys')


class MI_DeformPanel(bpy.types.Panel):
    bl_label = "Deform"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_context = "mesh_edit"
    bl_category = 'Mira'

    def draw(self, context):
        cur_stretch_settings = context.scene.mi_cur_stretch_settings
        lin_def_settings = context.scene.mi_ldeformer_settings
        curguide_settings = context.scene.mi_curguide_settings

        layout = self.layout
        layout.operator("mira.noise", text="Noise")
        # layout.label(text="Deformer:")
        layout.operator("mira.deformer", text="Deformer")

        layout.separator()
        layout.operator("mira.linear_deformer", text="LinearDeformer")
        layout.prop(lin_def_settings, "manual_update", text='ManualUpdate')

        layout.separator()
        layout.label(text="CurveStretch:")
        layout.operator("mira.curve_stretch", text="CurveStretch")
        layout.prop(cur_stretch_settings, "points_number", text='PointsNumber')
        layout.prop(cur_stretch_settings, "spread_mode", text='Spread')

        layout.separator()
        layout.label(text="CurveGuide:")
        layout.operator("mira.curve_guide", text="CurveGuide")
        layout.prop(curguide_settings, "points_number", text='PointsNumber')
        layout.prop(curguide_settings, "deform_type", text='DeformType')


class MI_CurveSettingsPanel(bpy.types.Panel):
    bl_label = "CurveSettings"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_context = "mesh_edit"
    bl_category = 'Mira'


    def draw(self, context):
        layout = self.layout
        curve_settings = context.scene.mi_curve_settings

        layout.prop(curve_settings, "surface_snap", text='SurfaceSnapping')
        layout.prop(curve_settings, "curve_resolution", text='Resolution')
        layout.prop(curve_settings, "draw_handlers", text='Handlers')
        layout.operator("mira.curve_test", text="Curve Test")