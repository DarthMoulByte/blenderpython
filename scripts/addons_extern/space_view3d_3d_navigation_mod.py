# 3D NAVIGATION TOOLBAR v1.2 - 3Dview Addon - Blender 2.5x
#
# THIS SCRIPT IS LICENSED UNDER GPL,
# please read the license block.
#
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
    "name": "3D Navigation_mod",
    "author": "Demohero, uriel, meta-androcto",
    "version": (1, 2),
    "blender": (2, 71, 0),
    "location": "View3D > Tool Shelf > 3D Navigation Tab",
    "description": "Navigate the Camera & 3D View from the Toolshelf",
    "warning": "",
    "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.6/Py/"
                "Scripts/3D_interaction/3D_Navigation",
    "category": "3D View",
}

# import the basic library
import bpy

class OrbitUpView(bpy.types.Operator):
	bl_idname = 'opr.orbit_up_view'
	bl_label = 'Orbit Up View'
	bl_description = 'Orbit the view towards'
	
	def execute(self, context):
		bpy.ops.view3d.view_orbit(type = 'ORBITUP')
		return {'FINISHED'}
		
class OrbitLeftView(bpy.types.Operator):
	bl_idname = 'opr.orbit_left_view'
	bl_label = 'Orbit Left View'
	bl_description = 'Orbit the view around to the Right'
	
	def execute(self, context):
		bpy.ops.view3d.view_orbit(type = 'ORBITLEFT')
		return {'FINISHED'}
		
class OrbitRightView(bpy.types.Operator):
	bl_idname = 'opr.orbit_right_view'
	bl_label = 'Orbit Right View'
	bl_description = 'Orbit the view around to the Left'
	
	def execute(self, context):
		bpy.ops.view3d.view_orbit(type = 'ORBITRIGHT')
		return {'FINISHED'}
		
class OrbitDownView(bpy.types.Operator):
	bl_idname = 'opr.orbit_down_view'
	bl_label = 'Orbit Down View'
	bl_description = 'Orbit the view away'
	
	def execute(self, context):
		bpy.ops.view3d.view_orbit(type = 'ORBITDOWN')
		return {'FINISHED'}
		
class PanUpView(bpy.types.Operator):
	bl_idname = 'opr.pan_up_view'
	bl_label = 'Pan Up View'
	bl_description = 'Pan the view Down'
	
	def execute(self, context):
		bpy.ops.view3d.view_pan(type = 'PANUP')
		return {'FINISHED'}
		
class PanLeftView(bpy.types.Operator):
	bl_idname = 'opr.pan_left_view'
	bl_label = 'Pan Right View'
	bl_description = 'Pan the view to your Right'
	
	def execute(self, context):
		bpy.ops.view3d.view_pan(type = 'PANLEFT')
		return {'FINISHED'}
		
class PanRightView(bpy.types.Operator):
	bl_idname = 'opr.pan_right_view'
	bl_label = 'Pan Left View'
	bl_description = 'Pan the view to your Left'
	
	def execute(self, context):
		bpy.ops.view3d.view_pan(type = 'PANRIGHT')
		return {'FINISHED'}
		
class PanDownView(bpy.types.Operator):
	bl_idname = 'opr.pan_down_view'
	bl_label = 'Pan Down View'
	bl_description = 'Pan the view up'
	
	def execute(self, context):
		bpy.ops.view3d.view_pan(type = 'PANDOWN')
		return {'FINISHED'}
		
class ZoomInView(bpy.types.Operator):
	bl_idname = 'opr.zoom_in_view'
	bl_label = 'Zoom In View'
	bl_description = 'Zoom in in the view'
	
	def execute(self, context):
		bpy.ops.view3d.zoom(delta = 1)
		return {'FINISHED'}
		
class ZoomOutView(bpy.types.Operator):
	bl_idname = 'opr.zoom_out_view'
	bl_label = 'Zoom Out View'
	bl_description = 'Zoom out in the view'
	
	def execute(self, context):
		bpy.ops.view3d.zoom(delta = -1)
		return {'FINISHED'}
		
class RollLeftView(bpy.types.Operator):
	bl_idname = 'opr.roll_left_view'
	bl_label = 'Roll Left View'
	bl_description = 'Roll the view left'
	
	def execute(self, context):
		bpy.ops.view3d.view_roll(angle = -0.261799)
		return {'FINISHED'}
		
class RollRightView(bpy.types.Operator):
	bl_idname = 'opr.roll_right_view'
	bl_label = 'Roll Right View'
	bl_description = 'Roll the view right'
	
	def execute(self, context):
		bpy.ops.view3d.view_roll(angle = 0.261799)
		return {'FINISHED'}
		
class LeftViewpoint(bpy.types.Operator):
	bl_idname = 'opr.left_viewpoint'
	bl_label = 'Left Viewpoint'
	bl_description = 'View from the Left'
	
	def execute(self, context):
		bpy.ops.view3d.viewnumpad(type = 'LEFT')
		return {'FINISHED'}
		
class RightViewpoint(bpy.types.Operator):
	bl_idname = 'opr.right_viewpoint'
	bl_label = 'Right Viewpoint'
	bl_description = 'View from the Right'
	
	def execute(self, context):
		bpy.ops.view3d.viewnumpad(type = 'RIGHT')
		return {'FINISHED'}
		
class FrontViewpoint(bpy.types.Operator):
	bl_idname = 'opr.front_viewpoint'
	bl_label = 'Front Viewpoint'
	bl_description = 'View from the Front'
	
	def execute(self, context):
		bpy.ops.view3d.viewnumpad(type = 'FRONT')
		return {'FINISHED'}
		
class BackViewpoint(bpy.types.Operator):
	bl_idname = 'opr.back_viewpoint'
	bl_label = 'Back Viewpoint'
	bl_description = 'View from the Back'
	
	def execute(self, context):
		bpy.ops.view3d.viewnumpad(type = 'BACK')
		return {'FINISHED'}
		
class TopViewpoint(bpy.types.Operator):
	bl_idname = 'opr.top_viewpoint'
	bl_label = 'Top Viewpoint'
	bl_description = 'View from the Top'
	
	def execute(self, context):
		bpy.ops.view3d.viewnumpad(type = 'TOP')
		return {'FINISHED'}
		
class BottomViewpoint(bpy.types.Operator):
	bl_idname = 'opr.bottom_viewpoint'
	bl_label = 'Bottom Viewpoint'
	bl_description = 'View from the Bottom'
	
	def execute(self, context):
		bpy.ops.view3d.viewnumpad(type = 'BOTTOM')
		return {'FINISHED'}
		
class ShowHideObject(bpy.types.Operator):
	bl_idname = 'opr.show_hide_object'
	bl_label = 'Show/Hide Object'
	bl_description = 'Show/hide selected objects'
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		if context.object == None:
			self.report({'ERROR'}, 'Cannot perform this operation on NoneType objects')
			return {'CANCELLED'}
			
		if context.object.mode != 'OBJECT':
			self.report({'ERROR'}, 'This operation can be performed only in object mode')
			return {'CANCELLED'}
			
		for i in bpy.data.objects:
			if i.select:
				if i.hide:
					i.hide = False
					i.hide_select = False
					i.hide_render = False
				else:
					i.hide = True
					i.select = False
					
					if i.type not in ['CAMERA', 'LAMP']:
						i.hide_render = True
		return {'FINISHED'}

# main class of this toolbar
class VIEW3D_PT_3dnavigationPanel(bpy.types.Panel):
    bl_category = "Navigation"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_label = "3D Nav"

    def draw(self, context):
        layout = self.layout
        view = context.space_data

# Triple boutons
        col = layout.column(align=True)
        col.operator("view3d.localview", text="View Global/Local")
        col.operator("view3d.view_persportho", text="View Persp/Ortho")
        col.operator("view3d.viewnumpad", text="View Camera", icon='CAMERA_DATA').type='CAMERA'

# group of 6 buttons
        col = layout.column(align=True)
        col.label(text="Align view from:")
        row = col.row()
        row.operator("view3d.viewnumpad", text="Front").type='FRONT'
        row.operator("view3d.viewnumpad", text="Back").type='BACK'
        row = col.row()
        row.operator("view3d.viewnumpad", text="Left").type='LEFT'
        row.operator("view3d.viewnumpad", text="Right").type='RIGHT'
        row = col.row()
        row.operator("view3d.viewnumpad", text="Top").type='TOP'
        row.operator("view3d.viewnumpad", text="Bottom").type='BOTTOM'

# group of 2 buttons
        col = layout.column(align=True)
        col.label(text="View to Object:")
        col.prop(view, "lock_object", text="")
        col.operator("view3d.view_selected", text="View to Selected")

        col = layout.column(align=True)
        col.label(text="Cursor:")

        row = col.row()
        row.operator("view3d.snap_cursor_to_center", text="Center")
        row.operator("view3d.view_center_cursor", text="View")

        col.operator("view3d.snap_cursor_to_selected", text="Cursor to Selected")

class VIEW3D_PT_pan_navigation(bpy.types.Panel):
	bl_idname = 'pan.navigation'
	bl_label = 'Pan Orbit Zoom Roll'
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_category = 'Navigation'
	bl_options = {'DEFAULT_CLOSED'}
	
	def draw(self, context):
		layout = self.layout

		row = layout.row()
		box = row.box()
		box.label(text = 'Pan:')
		rowr = box.row()
		rowr.operator('opr.pan_up_view', text = '', icon = 'TRIA_DOWN')
		rowr.operator('opr.pan_down_view', text = '', icon = 'TRIA_UP')

		rowr = box.row()
		rowr.operator('opr.pan_right_view',	text = '', icon = 'BACK')	
		rowr.operator('opr.pan_left_view',	text = '', icon = 'FORWARD')

		rowr = box.row()

		box = row.box()
		box.label(text = 'Orbit:')
		rowr = box.row()
		rowr.operator('opr.orbit_up_view', text = '', icon = 'TRIA_DOWN')
		rowr.operator('opr.orbit_down_view', text = '', icon = 'TRIA_UP')
		rowr = box.row()
		rowr.operator('opr.orbit_right_view',	text = '', icon = 'BACK')
		rowr.operator('opr.orbit_left_view',	text = '', icon = 'FORWARD')		

		rowr = box.row()
		row = layout.row()
		
		box = row.box()
		box.label(text = 'Zoom:')
		rowr = box.row()
		rowrowr = rowr.row(align = True)
		rowrowr.operator('opr.zoom_in_view',	text = '', icon = 'ZOOMIN')
		rowrowr.operator('opr.zoom_out_view',	text = '', icon = 'ZOOMOUT')
		
		box = row.box()
		box.label(text = 'Roll:')
		rowr = box.row()
		rowrowr = rowr.row(align = True)
		rowrowr.operator('opr.roll_left_view',	text = '', icon = 'LOOP_BACK')
		rowrowr.operator('opr.roll_right_view',	text = '', icon = 'LOOP_FORWARDS')

# register the class
def register():
    bpy.utils.register_module(__name__)

    pass

def unregister():
    bpy.utils.unregister_module(__name__)

    pass

if __name__ == "__main__":
    register()
