bl_info = {
    "name": "Quick align",
    "author": "nexus-studio",
    "version": (0, 3),
    "blender": (2, 74),
    "location": "View3D / Graph Editor > alt-Q key",
    "description": "Quick alignment on axis",
    "warning": "",
    "wiki_url": "none",
    "category": "Object",
}

import bpy
from bpy.props import StringProperty, BoolProperty, EnumProperty

def align_XYZ(x, y, z, axisX, axisY, axisZ):
    if bpy.context.mode == 'OBJECT':
        bpy.context.space_data.use_pivot_point_align = True
        bpy.ops.transform.resize(value=(x, y, z), constraint_axis=(axisX, axisY, axisZ), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
        bpy.context.space_data.use_pivot_point_align = False
    else:
        bpy.ops.transform.resize(value=(x, y, z), constraint_axis=(axisX, axisY, axisZ), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

def align_graph(x, y, z, axisX, axisY, axisZ):
    bpy.ops.transform.resize(value=(x, y, z), constraint_axis=(axisX, axisY, axisZ), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

# -----------------------------------------------------------------------------
# View 3d

class VIEW3D_align_x_slots(bpy.types.Operator):
    """the alignment along the x-axis in view 3d (object or edit mode)"""
    bl_idname = "view3d.align_x_slots"
    bl_label = "Align x"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        align_XYZ(0,1,1,True,False,False)
        return {'FINISHED'}

class VIEW3D_align_y_slots(bpy.types.Operator):
    """the alignment along the y-axis in view 3d (object or edit mode)"""
    bl_idname = "view3d.align_y_slots"
    bl_label = "Align y"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        align_XYZ(1,0,1,False,True,False)
        return {'FINISHED'}

class VIEW3D_align_z_slots(bpy.types.Operator):
    """the alignment along the z-axis in view 3d (object or edit mode)"""
    bl_idname = "view3d.align_z_slots"
    bl_label = "Align z"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        align_XYZ(1,1,0,False,False,True)
        return {'FINISHED'}

# -----------------------------------------------------------------------------
# Graph
class GRAPH_align_x_slots(bpy.types.Operator):
    """the alignment along the x-axis in graph editor"""
    bl_idname = "graph.align_x_slots"
    bl_label = "Align x"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        align_graph(0,1,1,True,False,False)
        return {'FINISHED'}

class GRAPH_align_y_slots(bpy.types.Operator):
    """the alignment along the y-axis in graph editor"""
    bl_idname = "graph.align_y_slots"
    bl_label = "Align y"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        align_graph(1,0,1,False,True,False)
        return {'FINISHED'}

# -----------------------------------------------------------------------------
# menu classes

class view3d_menu(bpy.types.Menu):
    bl_label = "Quick align"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.operator("view3d.align_x_slots", text="X align", icon='COLOR_RED')
        layout.operator("view3d.align_y_slots", text="Y align", icon='COLOR_GREEN')
        layout.operator("view3d.align_z_slots", text="Z align", icon='COLOR_BLUE')

class graph_menu(bpy.types.Menu):
    bl_label = "Quick align"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.operator("graph.align_x_slots", text="X align", icon='COLOR_RED')
        layout.operator("graph.align_y_slots", text="Y align", icon='COLOR_GREEN')

addon_keymaps = []
def register():
    bpy.utils.register_module(__name__)

    kc = bpy.context.window_manager.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name="3D View", space_type="VIEW_3D")
        kmi = km.keymap_items.new('wm.call_menu', 'Q', 'PRESS', alt=True)
        kmi.properties.name = "view3d_menu"
        addon_keymaps.append(km)

        km = kc.keymaps.new(name="Graph Editor", space_type="GRAPH_EDITOR")
        kmi = km.keymap_items.new('wm.call_menu', 'Q', 'PRESS', alt=True)
        kmi.properties.name = "graph_menu"
        addon_keymaps.append(km)

def unregister():
    bpy.utils.unregister_module(__name__)

    wm = bpy.context.window_manager
    if wm.keyconfigs.addon:
        for km in addon_keymaps:
            for kmi in km.keymap_items:
                km.keymap_items.remove(kmi)
    addon_keymaps.clear()

if __name__ == "__main__":
    register()