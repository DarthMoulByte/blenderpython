
bl_info = {
    "name": "View Numpad: Key: 'Q' ",
    "description": "View Numpad Menu",
    "author": "pitiwazou, meta-androcto",
    "version": (0, 1, 0),
    "blender": (2, 77, 0),
    "location": "Q key",
    "warning": "",
    "wiki_url": "",
    "category": "3D View"
}

import bpy
from ..utils import AddonPreferences, SpaceProperty
from bpy.types import Menu, Header
from bpy.props import IntProperty, FloatProperty, BoolProperty

# Persp/Ortho
class PerspOrthoView(bpy.types.Operator):
    bl_idname = "persp.orthoview"
    bl_label = "Persp/Ortho"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.view3d.view_persportho()
        return {'FINISHED'}

# Lock Camera Transforms
class LockCameraTransforms(bpy.types.Operator):
    bl_idname = "object.lockcameratransforms"
    bl_label = "Lock Camera Transforms"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if bpy.context.object.lock_rotation[0] == False:
            bpy.context.object.lock_rotation[0] = True
            bpy.context.object.lock_rotation[1] = True
            bpy.context.object.lock_rotation[2] = True
            bpy.context.object.lock_location[0] = True
            bpy.context.object.lock_location[1] = True
            bpy.context.object.lock_location[2] = True
            bpy.context.object.lock_scale[0] = True
            bpy.context.object.lock_scale[1] = True
            bpy.context.object.lock_scale[2] = True

        elif bpy.context.object.lock_rotation[0] == True:
            bpy.context.object.lock_rotation[0] = False
            bpy.context.object.lock_rotation[1] = False
            bpy.context.object.lock_rotation[2] = False
            bpy.context.object.lock_location[0] = False
            bpy.context.object.lock_location[1] = False
            bpy.context.object.lock_location[2] = False
            bpy.context.object.lock_scale[0] = False
            bpy.context.object.lock_scale[1] = False
            bpy.context.object.lock_scale[2] = False
        return {'FINISHED'}

# Active Camera
bpy.types.Scene.cameratoto = bpy.props.StringProperty(default="")

# Pie View All Sel Glob Etc - Q
class PieViewallSelGlobEtc(Menu):
    bl_idname = "pie.vieallselglobetc"
    bl_label = "Pie View All Sel Glob..."

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        # 4 - LEFT
        pie.operator("view3d.view_all", text="View All").center = True
        # 6 - RIGHT
        pie.operator("view3d.view_selected", text="View Selected")
        # 2 - BOTTOM
        pie.operator("persp.orthoview", text="Persp/Ortho", icon='RESTRICT_VIEW_OFF')
        # 8 - TOP
        pie.operator("view3d.localview", text="Local/Global")
        # 7 - TOP - LEFT
        pie.operator("screen.region_quadview", text="Toggle Quad View", icon='SPLITSCREEN')
        # 1 - BOTTOM - LEFT
        pie.operator("screen.screen_full_area", text="Full Screen", icon='FULLSCREEN_ENTER')
        # 9 - TOP - RIGHT
        # 3 - BOTTOM - RIGHT

# Pie views numpad - Q
class PieViewNumpad(Menu):
    bl_idname = "pie.viewnumpad"
    bl_label = "Pie Views Ortho"

    def draw(self, context):
        layout = self.layout
        ob = bpy.context.object
        obj = context.object
        pie = layout.menu_pie()
        scene = context.scene
        rd = scene.render

        # 4 - LEFT
        pie.operator("view3d.viewnumpad", text="Left", icon='TRIA_LEFT').type = 'LEFT'
        # 6 - RIGHT
        pie.operator("view3d.viewnumpad", text="Right", icon='TRIA_RIGHT').type = 'RIGHT'
        # 2 - BOTTOM
        pie.operator("view3d.viewnumpad", text="Bottom", icon='TRIA_DOWN').type = 'BOTTOM'
        # 8 - TOP
        pie.operator("view3d.viewnumpad", text="Top", icon='TRIA_UP').type = 'TOP'
        # 7 - TOP - LEFT
        pie.operator("view3d.viewnumpad", text="Front").type = 'FRONT'
        # 9 - TOP - RIGHT
        pie.operator("view3d.viewnumpad", text="Back").type = 'BACK'
        # 1 - BOTTOM - LEFT
        box = pie.split().column()
        row = box.row(align=True)
        if context.space_data.lock_camera == False:
            row.operator("wm.context_toggle", text="Lock Cam to View", icon='UNLOCKED').data_path = "space_data.lock_camera"
        elif context.space_data.lock_camera == True:
            row.operator("wm.context_toggle", text="Lock Cam to View", icon='LOCKED').data_path = "space_data.lock_camera"

        row = box.row(align=True)
        row.operator("view3d.viewnumpad", text="View Cam", icon='VISIBLE_IPO_ON').type = 'CAMERA'
        row.operator("view3d.camera_to_view", text="Cam to view", icon='MAN_TRANS')

        if ob.lock_rotation[0] == False:
            row = box.row(align=True)
            row.operator("object.lockcameratransforms", text="Lock Transforms", icon='LOCKED')

        elif ob.lock_rotation[0] == True:
            row = box.row(align=True)
            row.operator("object.lockcameratransforms", text="UnLock Transforms", icon='UNLOCKED')
        row = box.row(align=True)
        row.prop(rd, "use_border", text="Border")
        # 3 - BOTTOM - RIGHT
        pie.operator("wm.call_menu_pie", text="View All/Sel/Glob...", icon='BBOX').name = "pie.vieallselglobetc"

classes = [
    PieViewNumpad,
    LockCameraTransforms,
    PieViewallSelGlobEtc,
    PerspOrthoView,
    ]

addon_keymaps = []

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    wm = bpy.context.window_manager

    if wm.keyconfigs.addon:
        # Views numpad
        km = wm.keyconfigs.addon.keymaps.new(name='3D View Generic', space_type='VIEW_3D')
        kmi = km.keymap_items.new('wm.call_menu_pie', 'Q', 'PRESS')
        kmi.properties.name = "pie.viewnumpad"
#        kmi.active = True
        addon_keymaps.append((km, kmi))


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    wm = bpy.context.window_manager

    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps['3D View Generic']
        for kmi in km.keymap_items:
            if kmi.idname == 'wm.call_menu_pie':
                if kmi.properties.name == "pie.viewnumpad":
                    km.keymap_items.remove(kmi)

if __name__ == "__main__":
    register()
