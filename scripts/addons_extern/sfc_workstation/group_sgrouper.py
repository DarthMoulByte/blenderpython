# ***** BEGIN GPL LICENSE BLOCK *****
#
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ***** END GPL LICENCE BLOCK *****



bl_info = {
    "name": "Super Grouper",
    "author": "Paul Geraskin",
    "version": (0, 1, 0),
    "blender": (2, 73, 0),
    "location": "Toolshelf > Relations Tab",
    "warning": "",
    "description": "Super Grouper",
    "wiki_url": "",
    "category": "Retopology"}




import bpy
import random
import string

from bpy.props import *
from bpy.types import Operator, AddonPreferences
from bpy.types import Menu, Panel, UIList, PropertyGroup
from bpy.props import StringProperty, BoolProperty, IntProperty, CollectionProperty, BoolVectorProperty, PointerProperty
from bpy.app.handlers import persistent


NUM_LAYERS = 20
SCENE_SGR = '#SGR'
UNIQUE_ID_NAME = 'sg_belong_id'


class SG_Group(PropertyGroup):
    use_toggle = BoolProperty(name="", default=True)
    # is_wire = BoolProperty(name="", default=False)
    is_locked = BoolProperty(name="", default=False)
    is_selected = BoolProperty(name="", default=False)
                               # this is just a temporary value as a user can
                               # select/deselect
    unique_id = StringProperty(default="")

    wire_color = FloatVectorProperty(
        name="wire",
        subtype='COLOR',
        default=(0.2, 0.2, 0.2),
        min=0.0, max=1.0,
        description="wire color of the group"
    )


class SG_Object_Id(PropertyGroup):
    unique_id_object = StringProperty(default="")


class SG_Other_Settings(PropertyGroup):
    select_all_layers = BoolProperty(name="SelectVisibleLayers", default=True)
    unlock_obj = BoolProperty(name="UnlockObj", default=False)
    unhide_obj = BoolProperty(name="UnhideObj", default=True)




def draw_sgrouper(self, context):
    layout = self.layout

    scene = context.scene

    if context.scene.name.endswith(SCENE_SGR) is False:
        sg_settings = scene.sg_settings

        row = layout.row(align=True)
        row.operator(
            "super_grouper.super_group_add", icon='ZOOMIN', text="")
        row.operator(
            "super_grouper.super_group_remove", icon='ZOOMOUT', text="")

        op = row.operator(
            "super_grouper.super_group_move", icon='TRIA_UP', text="")
        op.do_move = 'UP'

        op = row.operator(
            "super_grouper.super_group_move", icon='TRIA_DOWN', text="")
        op.do_move = 'DOWN'

        row = layout.row(align=True)
        op = row.operator(
            "super_grouper.change_selected_objects", text="", emboss=False, icon='BBOX')
        op.sg_objects_changer = 'BOUND_SHADE'

        op = row.operator(
            "super_grouper.change_selected_objects", text="", emboss=False, icon='WIRE')
        op.sg_objects_changer = 'WIRE_SHADE'

        op = row.operator(
            "super_grouper.change_selected_objects", text="", emboss=False, icon='MATERIAL')
        op.sg_objects_changer = 'MATERIAL_SHADE'

        op = row.operator(
            "super_grouper.change_selected_objects", text="", emboss=False, icon='RETOPO')
        op.sg_objects_changer = 'SHOW_WIRE'

        op = row.operator(
            "super_grouper.change_selected_objects", text="", emboss=False, icon='SOLID')
        op.sg_objects_changer = 'HIDE_WIRE'

        row = layout.row(align=True)
        if scene.super_groups and scene.super_groups[scene.super_groups_index].use_toggle:
            # op = row.operator(
                #"super_grouper.change_grouped_objects", text="", emboss=False, icon='UNLOCKED')
            # op.sg_group_changer = 'UNLOCKED'

            op = row.operator(
                "super_grouper.change_grouped_objects", text="", emboss=False, icon='COLOR_GREEN')
            op.sg_group_changer = 'COLOR_WIRE'

            op = row.operator(
                "super_grouper.change_grouped_objects", text="", emboss=False, icon='COLOR_RED')
            op.sg_group_changer = 'DEFAULT_COLOR_WIRE'

        if scene.super_groups:
            row.prop(
                scene.super_groups[scene.super_groups_index], "wire_color", text='')

        row = layout.row()
        row.template_list(
            "SG_named_super_groups", "", scene, "super_groups", scene, "super_groups_index")

        row = layout.row()
        row.operator("super_grouper.add_to_group", text="Add")
        row.operator(
            "super_grouper.super_remove_from_group", text="Remove")
        row.operator("super_grouper.clean_object_ids", text="Clean")
        # layout.separator()
        layout.label(text="Selection Settings:")
        row = layout.row(align=True)
        row.prop(sg_settings, "select_all_layers", text='L')
        row.prop(sg_settings, "unlock_obj", text='L')
        row.prop(sg_settings, "unhide_obj", text='H')
        row = layout.row(align=True)


class SG_named_super_groups(UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        super_group = item

        # check for lock camera and layer is active
        # view_3d = context.area.spaces.active  # Ensured it is a 'VIEW_3D' in panel's poll(), weak... :/
        # use_spacecheck = False if view_3d.lock_camera_and_layers else True

        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.prop(super_group, "name", text="", emboss=False)

            # select operator
            # icon = 'LOCKED'
            # op = layout.operator("super_grouper.toggle_select", text="", emboss=False, icon=icon)
            # op.group_idx = index

            # select operator
            icon = 'RESTRICT_SELECT_OFF' if super_group.use_toggle else 'RESTRICT_SELECT_ON'
            op = layout.operator(
                "super_grouper.toggle_select", text="", emboss=False, icon=icon)
            op.group_idx = index

            # lock operator
            icon = 'LOCKED' if super_group.is_locked else 'UNLOCKED'
            op = layout.operator(
                "super_grouper.change_grouped_objects", text="", emboss=False, icon=icon)
            op.sg_group_changer = 'LOCKING'
            op.group_idx = index

            # view operator
            icon = 'RESTRICT_VIEW_OFF' if super_group.use_toggle else 'RESTRICT_VIEW_ON'
            op = layout.operator(
                "super_grouper.toggle_visibility", text="", emboss=False, icon=icon)
            op.group_idx = index

        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'


bpy.utils.register_class(SG_named_super_groups)

def generate_id():
    # Generate unique id
    other_ids = []
    for scene in bpy.data.scenes:
        if scene != bpy.context.scene and scene.name.endswith(SCENE_SGR) is False:
            for s_group in scene.super_groups:
                other_ids.append(s_group.unique_id)

    while True:
        uni_numb = None
        uniq_id_temp = ''.join(random.choice(string.ascii_uppercase + string.digits)
                               for _ in range(10))
        if uniq_id_temp not in other_ids:
            uni_numb = uniq_id_temp
            break

    other_ids = None  # clean
    return uni_numb


class SG_super_group_add(bpy.types.Operator):

    """Add and select a new layer group"""
    bl_idname = "super_grouper.super_group_add"
    bl_label = "Add Super Group"
    bl_options = {'REGISTER', 'UNDO'}

    # layers = BoolVectorProperty(name="Layers", default=([False] *
    # NUM_LAYERS), size=NUM_LAYERS)

    @classmethod
    def poll(cls, context):
        return bool(context.scene)

    def execute(self, context):
        scene = context.scene

        check_same_ids()  # check scene ids

        super_groups = scene.super_groups
        # layers = self.layers

        # get all ids
        all_ids = []
        for s_group in super_groups:
            if s_group.unique_id not in all_ids:
                all_ids.append(s_group.unique_id)

        # remove s_groups
        for obj in context.selected_objects:
            for s_group in super_groups:
                SG_del_properties_from_obj(UNIQUE_ID_NAME, all_ids, obj, True)

        # generate new id
        uni_numb = generate_id()
        all_ids = None

        group_idx = len(super_groups)
        new_s_group = super_groups.add()
        new_s_group.name = "SG.%.3d" % group_idx
        new_s_group.unique_id = uni_numb
        # new_s_group.wire_color = (random.uniform(0.0 , 1.0),
        # random.uniform(0.0 , 1.0), random.uniform(0.0 , 1.0))
        scene.super_groups_index = group_idx

        # add the unique id of selected objects
        for obj in context.selected_objects:
            SG_add_property_to_obj(new_s_group.unique_id, obj)

        return {'FINISHED'}

bpy.utils.register_class(SG_super_group_add)



class SG_super_group_remove(bpy.types.Operator):

    """Remove selected layer group"""
    bl_idname = "super_grouper.super_group_remove"
    bl_label = "Remove Super Group"
    bl_options = {'REGISTER', 'UNDO'}

    # group_idx = bpy.props.IntProperty()

    @classmethod
    def poll(cls, context):
        return bool(context.scene)

    def execute(self, context):
        scene = context.scene

        # if a scene contains goups
        if scene.super_groups:
            check_same_ids()  # check scene ids

            s_group_id = scene.super_groups[scene.super_groups_index].unique_id

            # get all ids
            s_groups = []
            for s_group in scene.super_groups:
                s_groups.append(s_group.unique_id)

            # clear context scene
            for obj in scene.objects:
                SG_del_properties_from_obj(
                    UNIQUE_ID_NAME, [s_group_id], obj, True)

            # clear SGR scene
            sgr_scene_name = scene.name + SCENE_SGR
            if sgr_scene_name in bpy.data.scenes:
                sgr_scene = bpy.data.scenes[scene.name + SCENE_SGR]
                for obj in sgr_scene.objects:
                    SGR_switch_object(obj, sgr_scene, scene, s_group_id)
                    SG_del_properties_from_obj(
                        UNIQUE_ID_NAME, [s_group_id], obj, True)

                # remove group_scene if it's empty
                if len(sgr_scene.objects) == 0:
                    bpy.data.scenes.remove(sgr_scene)

            # finally remove s_group
            scene.super_groups.remove(scene.super_groups_index)
            if scene.super_groups_index > len(scene.super_groups) - 1:
                scene.super_groups_index = len(scene.super_groups) - 1

        return {'FINISHED'}

bpy.utils.register_class(SG_super_group_remove)



class SG_super_group_move(bpy.types.Operator):

    """Remove selected layer group"""
    bl_idname = "super_grouper.super_group_move"
    bl_label = "Move Super Group"
    bl_options = {'REGISTER', 'UNDO'}

    do_move = EnumProperty(
        items=(('UP', 'UP', ''),
               ('DOWN', 'DOWN', '')
               ),
        default = 'UP'
    )

    @classmethod
    def poll(cls, context):
        return bool(context.scene)

    def execute(self, context):
        scene = context.scene

        # if a scene contains goups
        if scene.super_groups and len(scene.super_groups) > 1:
            s_group_id = scene.super_groups[scene.super_groups_index].unique_id
            if scene.super_groups:
                move_id = None
                if self.do_move == 'UP' and scene.super_groups_index > 0:
                    move_id = scene.super_groups_index - 1
                    scene.super_groups.move(scene.super_groups_index, move_id)
                elif self.do_move == 'DOWN' and scene.super_groups_index < len(scene.super_groups) - 1:
                    move_id = scene.super_groups_index + 1
                    scene.super_groups.move(scene.super_groups_index, move_id)

                if move_id is not None:
                    scene.super_groups_index = move_id

        return {'FINISHED'}

bpy.utils.register_class(SG_super_group_move)




class SG_clean_object_ids(bpy.types.Operator):

    """Remove selected layer group"""
    bl_idname = "super_grouper.clean_object_ids"
    bl_label = "Clean Objects IDs if the objects were imported from other blend files"
    bl_options = {'REGISTER', 'UNDO'}

    # group_idx = bpy.props.IntProperty()

    @classmethod
    def poll(cls, context):
        return bool(context.scene)

    def execute(self, context):
        check_same_ids()  # check scene ids

        scenes_ids = []
        for scene in bpy.data.scenes:
            if scene.super_groups:
                for s_group in scene.super_groups:
                    if s_group.unique_id not in scenes_ids:
                        scenes_ids.append(s_group.unique_id)

        for obj in bpy.data.objects:
            SG_del_properties_from_obj(UNIQUE_ID_NAME, scenes_ids, obj, False)

        scenes_ids = None  # clean

        return {'FINISHED'}

bpy.utils.register_class(SG_clean_object_ids)


def SGR_get_group_scene(context):
    group_scene_name = context.scene.name + SCENE_SGR

    if group_scene_name in bpy.data.scenes:
        return bpy.data.scenes[group_scene_name]

    return None


def SG_create_group_scene(context):
    group_scene_name = context.scene.name + SCENE_SGR

    if context.scene.name.endswith(SCENE_SGR) is False:
        if group_scene_name in bpy.data.scenes:
            return bpy.data.scenes[group_scene_name]
        else:
            return bpy.data.scenes.new(group_scene_name)

    return None


def SG_select_objects(scene, ids):
    temp_scene_layers = list(scene.layers[:])  # copy layers of the scene
    for obj in scene.objects:
        if obj.sg_belong_id:
            for prop in obj.sg_belong_id:
                if prop.unique_id_object in ids:
                    for i in range(20):
                        if obj.layers[i] is True:
                            if scene.layers[i] is True or scene.sg_settings.select_all_layers:
                                # unlock
                                if scene.sg_settings.unlock_obj:
                                    obj.hide_select = False
                                # unhide
                                if scene.sg_settings.unhide_obj:
                                    obj.hide = False

                                # select
                                obj.select = True

                                # break if we need to select only visible
                                # layers
                                if scene.sg_settings.select_all_layers is False:
                                    break
                                else:
                                    temp_scene_layers[i] = obj.layers[i]

    # set layers switching to a scene
    if scene.sg_settings.select_all_layers:
        scene.layers = temp_scene_layers


class SG_toggle_select(bpy.types.Operator):

    """Toggle Select"""
    bl_idname = "super_grouper.toggle_select"
    bl_label = "Toggle Select"
    bl_description = "Toggle Select"
    bl_options = {'REGISTER', 'UNDO'}

    group_idx = IntProperty()

    def execute(self, context):
        scene = context.scene
        if self.group_idx < len(scene.super_groups):
            # check_same_ids()  # check scene ids

            s_group = scene.super_groups[self.group_idx]

            if s_group.use_toggle is True:
                SG_select_objects(scene, [s_group.unique_id])
                if scene.sg_settings.unlock_obj:
                    s_group.is_locked = False

        return {'FINISHED'}

bpy.utils.register_class(SG_toggle_select)




class SG_toggle_visibility(bpy.types.Operator):

    """Toggle Visibility"""
    bl_idname = "super_grouper.toggle_visibility"
    bl_label = "Toggle Visibility"
    bl_description = "Toggle Visibility"
    bl_options = {'REGISTER', 'UNDO'}

    group_idx = IntProperty()

    def execute(self, context):
        scene = context.scene
        if self.group_idx < len(scene.super_groups):
            # check_same_ids()  # check scene ids

            current_s_group = scene.super_groups[self.group_idx]

            # Try to get or create new GroupScene
            group_scene = SGR_get_group_scene(context)
            if group_scene is None and current_s_group.use_toggle is True:
                group_scene = SG_create_group_scene(context)

            # if GroupScene exists now we can switch objects
            if group_scene is not None:
                if current_s_group.use_toggle is True:
                    for obj in scene.objects:
                        SGR_switch_object(
                            obj, scene, group_scene, current_s_group.unique_id)
                else:
                    for obj in group_scene.objects:
                        SGR_switch_object(
                            obj, group_scene, scene, current_s_group.unique_id)
                    if len(group_scene.objects) == 0:
                        bpy.data.scenes.remove(group_scene)

            current_s_group.use_toggle = not current_s_group.use_toggle  # switch visibility

        return {'FINISHED'}

bpy.utils.register_class(SG_toggle_visibility)


def SGR_switch_object(obj, scene_source, scene_terget, s_group_id):
    do_switch = False
    if obj.sg_belong_id:
        for prop in obj.sg_belong_id:
            if prop.unique_id_object == s_group_id:
                do_switch = True
                break

        if do_switch is True:
            layers = obj.layers[:]  # copy layers
            obj.select = False

            # if object is not already linked
            if obj.name not in scene_terget.objects:
                obj2 = scene_terget.objects.link(obj)
                obj2.layers = layers  # paste layers

            scene_source.objects.unlink(obj)
            layers = None  # clean


def sg_is_object_in_s_groups(groups_prop_values, obj):
    is_in_group = False
    for prop in obj.sg_belong_id:
        if prop.unique_id_object in groups_prop_values:
            is_in_group = True
            break

    if is_in_group:
        return True
    else:
        return False


class SG_change_grouped_objects(bpy.types.Operator):
    bl_idname = "super_grouper.change_grouped_objects"
    bl_label = "Change Grouped"
    bl_description = "change object and grouped display"
    bl_options = {'REGISTER', 'UNDO'}

    sg_group_changer = EnumProperty(
        items=(('COLOR_WIRE', 'COLOR_WIRE', ''),
               ('DEFAULT_COLOR_WIRE', 'DEFAULT_COLOR_WIRE', ''),
               ('LOCKING', 'LOCKING', '')
               ),
        default = 'DEFAULT_COLOR_WIRE'
    )

    list_objects = ['LOCKING']

    group_idx = IntProperty()

    def execute(self, context):
        scene_parse = context.scene
        if scene_parse.super_groups:
            # check_same_ids()  # check scene ids

            s_group = None
            if self.sg_group_changer not in self.list_objects:
                s_group = scene_parse.super_groups[
                    scene_parse.super_groups_index]
            else:
                if self.group_idx < len(scene_parse.super_groups):
                    s_group = scene_parse.super_groups[self.group_idx]

            # if s_group.use_toggle is False:
            #     scene_parse = SGR_get_group_scene(context)
            if s_group is not None and s_group.use_toggle is True:
                for obj in scene_parse.objects:
                    if sg_is_object_in_s_groups([s_group.unique_id], obj):
                        if self.sg_group_changer == 'COLOR_WIRE':
                            r = s_group.wire_color[0]
                            g = s_group.wire_color[1]
                            b = s_group.wire_color[2]
                            obj.color = (r, g, b, 1)
                            obj.show_wire_color = True
                        elif self.sg_group_changer == 'DEFAULT_COLOR_WIRE':
                            obj.show_wire_color = False
                        elif self.sg_group_changer == 'LOCKING':
                            if s_group.is_locked is False:
                                obj.hide_select = True
                                obj.select = False
                            else:
                                obj.hide_select = False

                # switch locking for the group
                if self.sg_group_changer == 'LOCKING':
                    if s_group.is_locked is False:
                        s_group.is_locked = True
                    else:
                        s_group.is_locked = False

        return {'FINISHED'}

bpy.utils.register_class(SG_change_grouped_objects)


class SG_change_selected_objects(bpy.types.Operator):
    bl_idname = "super_grouper.change_selected_objects"
    bl_label = "Change Selected"
    bl_description = "change object and grouped display"
    bl_options = {'REGISTER', 'UNDO'}

    sg_objects_changer = EnumProperty(
        items=(('BOUND_SHADE', 'BOUND_SHADE', ''),
               ('WIRE_SHADE', 'WIRE_SHADE', ''),
               ('MATERIAL_SHADE', 'MATERIAL_SHADE', ''),
               ('SHOW_WIRE', 'SHOW_WIRE', ''),
               ('HIDE_WIRE', 'HIDE_WIRE', '')
               ),
        default = 'MATERIAL_SHADE'
    )
    sg_do_with_groups = [
        'COLOR_WIRE', 'DEFAULT_COLOR_WIRE', 'LOCKED', 'UNLOCKED']

    def execute(self, context):
        for obj in context.selected_objects:
            if self.sg_objects_changer == 'BOUND_SHADE':
                obj.draw_type = 'BOUNDS'
            elif self.sg_objects_changer == 'WIRE_SHADE':
                obj.draw_type = 'WIRE'
            elif self.sg_objects_changer == 'MATERIAL_SHADE':
                obj.draw_type = 'TEXTURED'
            elif self.sg_objects_changer == 'SHOW_WIRE':
                obj.show_wire = True
            elif self.sg_objects_changer == 'HIDE_WIRE':
                obj.show_wire = False

        return {'FINISHED'}

bpy.utils.register_class(SG_change_selected_objects)


class SG_add_to_group(bpy.types.Operator):
    bl_idname = "super_grouper.add_to_group"
    bl_label = "Add"
    bl_description = "Add To Super Group"
    bl_options = {'REGISTER', 'UNDO'}

    # group_idx = bpy.props.IntProperty()

    def execute(self, context):
        scene = context.scene

        if scene.super_groups:
            check_same_ids()  # check ids

            # remove s_groups
            ids = []
            for s_group in scene.super_groups:
                ids.append(s_group.unique_id)
            for obj in context.selected_objects:
                for s_group in scene.super_groups:
                    SG_del_properties_from_obj(UNIQUE_ID_NAME, ids, obj, True)
            ids = None

            s_group = scene.super_groups[scene.super_groups_index]
            for obj in context.selected_objects:
                # add the unique id of selected group
                SG_add_property_to_obj(s_group.unique_id, obj)

                # switch locking for obj
                if s_group.is_locked is True:
                    obj.hide_select = True
                    obj.select = False
                else:
                    obj.hide_select = False

                # check if the group is hidden
                if s_group.use_toggle is False:
                    # Try to get or create new GroupScene
                    group_scene = SGR_get_group_scene(context)
                    if group_scene is None:
                        group_scene = SG_create_group_scene(context)

                    # Unlink object
                    if group_scene is not None:
                        group_scene.objects.link(obj)
                        context.scene.objects.unlink(obj)

        return {'FINISHED'}

bpy.utils.register_class(SG_add_to_group)




class SG_remove_from_group(bpy.types.Operator):
    bl_idname = "super_grouper.super_remove_from_group"
    bl_label = "Add"
    bl_description = "Remove from Super Group"
    bl_options = {'REGISTER', 'UNDO'}

    # group_idx = bpy.props.IntProperty()

    def execute(self, context):
        scene = context.scene

        if scene.super_groups:
            check_same_ids()  # check ids

            # get all ids
            s_groups = []
            for s_group in scene.super_groups:
                s_groups.append(s_group.unique_id)

            # remove s_groups
            for obj in context.selected_objects:
                SG_del_properties_from_obj(UNIQUE_ID_NAME, s_groups, obj, True)
            s_groups = None  # clear

        return {'FINISHED'}

bpy.utils.register_class(SG_remove_from_group)



def SG_add_property_to_obj(prop_name, obj):
    props = obj.sg_belong_id

    has_value = False
    if props:
        for prop in props:
            if prop.unique_id_object == prop_name:
                has_value = True
                break

    # add the value if it does not exist
    if has_value == False:
        added_prop = props.add()
        added_prop.unique_id_object = prop_name


def SG_del_properties_from_obj(prop_name, s_groups_ids, obj, delete_in_s_groups=True):
    props = obj.sg_belong_id

    if len(props.values()) > 0:

        # remove item
        prop_len = len(props)
        index_prop = 0
        for i in range(prop_len):
            prop_obj = props[index_prop]
            is_removed = False
            if prop_obj.unique_id_object in s_groups_ids and delete_in_s_groups == True:
                props.remove(index_prop)
                is_removed = True
            elif prop_obj.unique_id_object not in s_groups_ids and delete_in_s_groups == False:
                props.remove(index_prop)
                is_removed = True

            if is_removed is False:
                index_prop += 1

        if len(props.values()) == 0:
            del bpy.data.objects[obj.name][prop_name]


def check_same_ids():
    scenes = bpy.data.scenes
    current_scene = bpy.context.scene

    check_scenes = []
    for scene in scenes:
        if scene.name.endswith(SCENE_SGR) is False and scene != current_scene:
            check_scenes.append(scene)

    if check_scenes:
        other_ids = []
        for scene in check_scenes:
            for s_group in scene.super_groups:
                if s_group.unique_id not in other_ids:
                    other_ids.append(s_group.unique_id)

        all_obj_list = None

        if other_ids:
            for i in range(len(current_scene.super_groups)):
                current_s_group = current_scene.super_groups[i]
                current_id = current_s_group.unique_id
                if current_id in other_ids:
                    new_id = generate_id()

                    if all_obj_list is None:
                        all_obj_list = []
                        all_obj_list += current_scene.objects
                        group_scene = SGR_get_group_scene(bpy.context)
                        if group_scene is not None:
                            all_obj_list += group_scene.objects

                    for obj in all_obj_list:
                        has_id = False
                        for prop in obj.sg_belong_id:
                            if prop.unique_id_object == current_s_group.unique_id:
                                has_id = True
                                break
                        if has_id == True:
                            SG_add_property_to_obj(new_id, obj)

                    # set new id
                    current_s_group.unique_id = new_id

    # clean
    check_scenes = None
    all_obj_list = None
    other_ids = None




def register():


    bpy.utils.register_module(__name__)

    bpy.types.Scene.super_groups = CollectionProperty(type=SG_Group)
    bpy.types.Object.sg_belong_id = CollectionProperty(type=SG_Object_Id)
    bpy.types.Scene.sg_settings = PointerProperty(type=SG_Other_Settings)

    # Unused, but this is needed for the TemplateList to work...
    bpy.types.Scene.super_groups_index = IntProperty(default=-1)


def unregister():
    #import bpy

    del bpy.types.Scene.super_groups
    del bpy.types.Object.sg_belong_id
    del bpy.types.Scene.sg_settings

    del bpy.types.Scene.super_groups_index

    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
    
