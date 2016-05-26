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
    "name": "TP Display Window View",
    "author": "marvin.k.breuer",
    "version": (0, 1),
    "blender": (2, 7, 7),
    "category": "Tool+"
}


import bpy
from bpy.props import IntProperty, FloatProperty, BoolProperty
from bpy.types import Operator, AddonPreferences


class TP_Display_View_Extend_Menu(bpy.types.Menu):
    bl_label = "Windows [CTRL+\]"
    bl_idname = "tp_display.view_extend_menu"

    def draw(self, context):
        layout = self.layout
        view = context.space_data
        obj = context.active_object
        toolsettings = context.tool_settings

        layout.operator("screen.region_quadview", text="Quad View", icon="SPLITSCREEN")
        layout.operator("screen.screen_full_area", text="Full Screen", icon="GO_LEFT")

        layout.separator()

        layout.menu("tp_display.view_custom_menu", text="Editor View", icon="PLUG")

        layout.separator()

        if bpy.context.area.type == 'VIEW_3D':

            layout.operator_enum("OBJECT_OT_mode_set", "mode")

            layout.separator()

            view = context.space_data
            layout.prop(context.space_data, "viewport_shade", expand=True)

            layout.separator()

        if context.scene.MenuSplitHorizontal:
            layout.operator("screen.area_split", text="Split Horizontal", icon='TRIA_DOWN').direction = "HORIZONTAL"

        if context.scene.MenuSplitVertical:
            layout.operator("screen.area_split", text="Split Vertical", icon='TRIA_RIGHT').direction = "VERTICAL"

        if context.scene.MenuJoinArea:
            layout.operator_context = "INVOKE_DEFAULT"
            layout.operator("tp_display.join_area", icon='X', text="Join Area")

        layout.separator()

        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.operator("screen.area_dupli", text="Duplicate Window", icon="SCREEN_BACK")

        layout.separator()

        layout.operator("view3d.properties", icon='MENU_PANEL')
        layout.operator("view3d.toolshelf", icon='MENU_PANEL')


class TP_Display_View_Custom_Menu(bpy.types.Menu):
    bl_label = ""
    bl_idname = "tp_display.view_custom_menu"

    def draw(self, context):
        layout = self.layout

        col = layout.column()

        if context.scene.Menu3DView:
            col.operator("object.view_menu", text="VIEW 3D", icon='VIEW3D').variable = "VIEW_3D"

        if context.scene.MenuNodeEditor:
            col.operator("object.view_menu", text="Node Editor", icon='NODETREE').variable = "NODE_EDITOR"

        if context.scene.MenuImageEditor:
            col.operator("object.view_menu", text="Image Editor", icon='IMAGE_COL').variable = "IMAGE_EDITOR"

        if context.scene.MenuOutliner:
            col.operator("object.view_menu", text="Outliner", icon='OOPS').variable = "OUTLINER"

        if context.scene.MenuProperties:
            col.operator("object.view_menu", text="Properties", icon='BUTS').variable = "PROPERTIES"

        if context.scene.MenuTextEditor:
            col.operator("object.view_menu", text="Text Editor", icon='FILE_TEXT').variable = "TEXT_EDITOR"

        if context.scene.MenuGraphEditor:
            col.operator("object.view_menu", text="Graph Editor", icon='IPO').variable = "GRAPH_EDITOR"

        if context.scene.MenuDopeSheet:
            col.operator("object.view_menu", text="Dope Sheet", icon='ACTION').variable = "DOPESHEET_EDITOR"

        if context.scene.MenuTimeline:
            col.operator("object.view_menu", text="Timeline", icon='TIME').variable = "TIMELINE"

        if context.scene.MenuNlaEditor:
            col.operator("object.view_menu", text="NLA Editor", icon='NLA').variable = "NLA_EDITOR"

        if context.scene.MenuLogicEditor:
            col.operator("object.view_menu", text="Logic Editor", icon='LOGIC').variable = "LOGIC_EDITOR"

        if context.scene.MenuSequenceEditor:
            col.operator("object.view_menu", text="Sequence Editor", icon='SEQUENCE').variable = "SEQUENCE_EDITOR"

        if context.scene.MenuMovieClip:
            col.operator("object.view_menu", text="Movie Clip Editor", icon='RENDER_ANIMATION').variable = "CLIP_EDITOR"

        if context.scene.MenuPythonConsole:
            col.operator("object.view_menu", text="Python Console", icon='CONSOLE').variable = "CONSOLE"

        if context.scene.MenuInfo:
            col.operator("object.view_menu", text="Info", icon='INFO').variable = "INFO"

        if context.scene.MenuFileBrowser:
            col.operator("object.view_menu", text="File Browser", icon='FILESEL').variable = "FILE_BROWSER"

        if context.scene.MenuUserPreferences:
            col.operator("object.view_menu", text="User Preferences", icon='PREFERENCES').variable = "USER_PREFERENCES"


bpy.utils.register_class(TP_Display_View_Custom_Menu)


class TP_Display_Preferences_Addon(AddonPreferences):
    bl_idname = __name__

    bpy.types.Scene.MenuSplitHorizontal = BoolProperty(default=True)
    bpy.types.Scene.MenuSplitVertical = BoolProperty(default=True)
    bpy.types.Scene.MenuJoinArea = BoolProperty(default=True)

    bpy.types.Scene.Menu3DView = BoolProperty(default=True)
    bpy.types.Scene.MenuNodeEditor = BoolProperty(default=True)
    bpy.types.Scene.MenuImageEditor = BoolProperty(default=True)
    bpy.types.Scene.MenuOutliner = BoolProperty(default=True)
    bpy.types.Scene.MenuProperties = BoolProperty(default=True)
    bpy.types.Scene.MenuTextEditor = BoolProperty(default=True)
    bpy.types.Scene.MenuGraphEditor = BoolProperty(default=True)
    bpy.types.Scene.MenuDopeSheet = BoolProperty(default=True)
    bpy.types.Scene.MenuTimeline = BoolProperty(default=True)
    bpy.types.Scene.MenuNlaEditor = BoolProperty(default=False)
    bpy.types.Scene.MenuLogicEditor = BoolProperty(default=False)
    bpy.types.Scene.MenuSequenceEditor = BoolProperty(default=False)
    bpy.types.Scene.MenuMovieClip = BoolProperty(default=False)
    bpy.types.Scene.MenuPythonConsole = BoolProperty(default=False)
    bpy.types.Scene.MenuInfo = BoolProperty(default=False)
    bpy.types.Scene.MenuFileBrowser = BoolProperty(default=False)
    bpy.types.Scene.MenuUserPreferences = BoolProperty(default=True)

    def draw(self, context):
        layout = self.layout

        layout.prop(context.scene, "MenuSplitHorizontal", text="Show Split Horizontal", icon='TRIA_DOWN')
        layout.prop(context.scene, "MenuSplitVertical", text="Show Split Vertical", icon='TRIA_RIGHT')
        layout.prop(context.scene, "MenuJoinArea", text="Show Join Area", icon='X')

        layout.separator()

        layout.prop(context.scene, "Menu3DView", text="Show 3D View", icon='VIEW3D')
        layout.prop(context.scene, "MenuNodeEditor", text="Show Node Editor", icon='NODETREE')
        layout.prop(context.scene, "MenuImageEditor", text="Show Image Editor", icon='IMAGE_COL')
        layout.prop(context.scene, "MenuOutliner", text="Show Outliner", icon='OOPS')
        layout.prop(context.scene, "MenuProperties", text="Show Properties", icon='BUTS')
        layout.prop(context.scene, "MenuTextEditor", text="Show Text Editor", icon='FILE_TEXT')
        layout.prop(context.scene, "MenuGraphEditor", text="Show Graph Editor", icon='IPO')
        layout.prop(context.scene, "MenuDopeSheet", text="Show Dope Sheet", icon='ACTION')
        layout.prop(context.scene, "MenuTimeline", text="Show Timeline", icon='TIME')
        layout.prop(context.scene, "MenuNlaEditor", text="Show Nla Editor", icon='NLA')
        layout.prop(context.scene, "MenuLogicEditor", text="Show Logic Editor", icon='LOGIC')
        layout.prop(context.scene, "MenuSequenceEditor", text="Show Sequence Editor", icon='SEQUENCE')
        layout.prop(context.scene, "MenuMovieClip", text="Show Movie Clip", icon='RENDER_ANIMATION')
        layout.prop(context.scene, "MenuPythonConsole", text="ShowM Python Console", icon='CONSOLE')
        layout.prop(context.scene, "MenuInfo", text="Show Info", icon='INFO')
        layout.prop(context.scene, "MenuFileBrowser", text="Show File Browser", icon='FILESEL')
        layout.prop(context.scene, "MenuUserPreferences", text="Show User Preferences", icon='PREFERENCES')

bpy.utils.register_class(TP_Display_Preferences_Addon)


class TP_Display_View_Menu(bpy.types.Operator):
    """Menu to change views"""
    bl_idname = "object.view_menu"
    bl_label = "View_Menu"
    variable = bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.context.area.type = self.variable
        return {'FINISHED'}

bpy.utils.register_class(TP_Display_View_Menu)


class TP_Display_Join_Area(bpy.types.Operator):
    """Join 2 area, clic on the second area to join"""
    bl_idname = "tp_display.join_area"
    bl_label = "Join Area"

    min_x = IntProperty()
    min_y = IntProperty()

    def modal(self, context, event):
        if event.type == 'LEFTMOUSE':
            self.max_x = event.mouse_x
            self.max_y = event.mouse_y
            bpy.ops.screen.area_join(min_x=self.min_x, min_y=self.min_y, max_x=self.max_x, max_y=self.max_y)
            bpy.ops.screen.screen_full_area()
            bpy.ops.screen.screen_full_area()
            return {'FINISHED'}
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        self.min_x = event.mouse_x
        self.min_y = event.mouse_y
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

bpy.utils.register_class(TP_Display_Join_Area)


def register():

    bpy.utils.register_class(TP_Display_View_Extend_Menu)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='Window')
        kmi = km.keymap_items.new('wm.call_menu', 'BACK_SLASH', 'PRESS', ctrl=True)
        kmi.properties.name = "tp_display.view_extend_menu"


def unregister():

    bpy.utils.unregister_class(TP_Display_View_Extend_Menu)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps['Window']
        for kmi in km.keymap_items:
            if kmi.idname == 'wm.call_menu':
                if kmi.properties.name == "":
                    km.keymap_items.remove(kmi)
                    break


if __name__ == "__main__":
    register()
    # The menu can also be called from scripts
    bpy.ops.wm.call_menu(name=TP_Display_View_Extend_Menu.bl_idname)
