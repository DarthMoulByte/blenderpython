
bl_info = {
    "name": "Apply Transform: Key: 'Ctrl A'",
    "description": "Apply Transform Menu",
    "author": "pitiwazou, meta-androcto",
    "version": (0, 1, 0),
    "blender": (2, 77, 0),
    "location": "Ctrl A key",
    "warning": "",
    "wiki_url": "",
    "category": "Object"
}

import bpy
from ..utils import AddonPreferences, SpaceProperty
from bpy.types import Menu, Header
from bpy.props import IntProperty, FloatProperty, BoolProperty

# Pie Apply Transforms - Ctrl + A
class PieApplyTransforms(Menu):
    bl_idname = "pie.applytranforms"
    bl_label = "Pie Apply Transforms"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        # 4 - LEFT
        pie.operator("apply.transformlocation", text="Location", icon='MAN_TRANS')
        # 6 - RIGHT
        pie.operator("apply.transformscale", text="Scale", icon='MAN_SCALE')
        # 2 - BOTTOM
        pie.operator("apply.transformrotation", text="Rotation", icon='MAN_ROT')
        # 8 - TOP
        pie.operator("apply.transformall", text="Transforms", icon='FREEZE')
        # 7 - TOP - LEFT
        pie.operator("apply.transformrotationscale", text="Rotation/Scale")
        # 9 - TOP - RIGHT
        pie.operator("clear.all", text="Clear All", icon='MANIPUL')
        # 1 - BOTTOM - LEFT
        box = pie.split().column()
        row = box.row(align=True)
        box.operator("object.visual_transform_apply", text="Visual Transforms")
        box.operator("object.duplicates_make_real", text="Make Duplicates Real")
        # 3 - BOTTOM - RIGHT
        pie.menu("clear.menu", text="Clear Transforms")

# Apply Transforms
class ApplyTransformLocation(bpy.types.Operator):
    bl_idname = "apply.transformlocation"
    bl_label = "Apply Transform Location"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)
        return {'FINISHED'}

# Apply Transforms
class ApplyTransformRotation(bpy.types.Operator):
    bl_idname = "apply.transformrotation"
    bl_label = "Apply Transform Rotation"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        return {'FINISHED'}

# Apply Transforms
class ApplyTransformScale(bpy.types.Operator):
    bl_idname = "apply.transformscale"
    bl_label = "Apply Transform Scale"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        return {'FINISHED'}

# Apply Transforms


class ApplyTransformRotationScale(bpy.types.Operator):
    bl_idname = "apply.transformrotationscale"
    bl_label = "Apply Transform Rotation Scale"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        return {'FINISHED'}

# Apply Transforms
class ApplyTransformAll(bpy.types.Operator):
    bl_idname = "apply.transformall"
    bl_label = "Apply Transform All"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        return {'FINISHED'}


# Clear Menu
class ClearMenu(bpy.types.Menu):
    bl_idname = "clear.menu"
    bl_label = "Clear Menu"

    def draw(self, context):
        layout = self.layout
        layout.operator("object.location_clear", text="Clear Location", icon='MAN_TRANS')
        layout.operator("object.rotation_clear", text="Clear Rotation", icon='MAN_ROT')
        layout.operator("object.scale_clear", text="Clear Scale", icon='MAN_SCALE')
        layout.operator("object.origin_clear", text="Clear Origin", icon='MANIPUL')

# Clear all


class ClearAll(bpy.types.Operator):
    bl_idname = "clear.all"
    bl_label = "Clear All"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.location_clear()
        bpy.ops.object.rotation_clear()
        bpy.ops.object.scale_clear()
        return {'FINISHED'}

classes = [
    PieApplyTransforms,
    ApplyTransformLocation,
    ApplyTransformRotation,
    ApplyTransformScale,
    ApplyTransformRotationScale,
    ApplyTransformAll,
    ClearMenu,
    ClearAll,
    ]

addon_keymaps = []

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    wm = bpy.context.window_manager

    if wm.keyconfigs.addon:
        # Apply Transform
        km = wm.keyconfigs.addon.keymaps.new(name='Object Mode')
        kmi = km.keymap_items.new('wm.call_menu_pie', 'A', 'PRESS', ctrl=True)
        kmi.properties.name = "pie.applytranforms"
#        kmi.active = True
        addon_keymaps.append((km, kmi))

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    wm = bpy.context.window_manager

    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps['Object Mode']
        for kmi in km.keymap_items:
            if kmi.idname == 'wm.call_menu_pie':
                if kmi.properties.name == "pie.applytranforms":
                    km.keymap_items.remove(kmi)

if __name__ == "__main__":
    register()
