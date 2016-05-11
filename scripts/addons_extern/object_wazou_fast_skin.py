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
    "name": "Fast Skin",
    "author": "Cédric Lepiller",
    "version": (0, 0, 2),
    "blender": (2, 74, 0),
    "description": "Create a fast Skin model",
    "category": "Object",}
 
import bpy
import bmesh
from bpy.types import Menu
from bpy.props import IntProperty, FloatProperty, BoolProperty
 
bpy.types.Scene.Skin_Mirror = bpy.props.BoolProperty(default=True)
bpy.types.Scene.Skin_Skin = bpy.props.BoolProperty(default=False)
bpy.types.Scene.Skin_Subdivs = bpy.props.BoolProperty(default=True)
bpy.types.Scene.Skin_Shading = bpy.props.BoolProperty(default=True)
 
########################
#      Properties      #               
########################
 
def update_panel(self, context):
    try:
        bpy.utils.unregister_class(Fast_Skin)
    except:
        pass
    Fast_Skin.bl_category = context.user_preferences.addons[__name__].preferences.category
    bpy.utils.register_class(Fast_Skin)
 
 
class Wazou_fast_skin(bpy.types.AddonPreferences):
    """Creates mesh with skin Modifier in One clic"""
    bl_idname = __name__
 
 
    bpy.types.Scene.Enable_Tab_FK_01 = bpy.props.BoolProperty(default=False)
 
    category = bpy.props.StringProperty(
            name="Category",
            description="Choose a name for the category of the panel",
            default="Fast Skin",
            update=update_panel,
            )
 
 
    def draw(self, context):
        layout = self.layout
 
        layout.prop(self, "category")
 
        layout.prop(context.scene, "Enable_Tab_FK_01", text="URL's", icon="URL") 
        if context.scene.Enable_Tab_FK_01:
            row = layout.row()    
 
            row.operator("wm.url_open", text="Pitiwazou.com").url = "http://www.pitiwazou.com/"
            row.operator("wm.url_open", text="Wazou's Ghitub").url = "https://github.com/pitiwazou/Scripts-Blender"
            row.operator("wm.url_open", text="BlenderLounge Forum ").url = "http://blenderlounge.fr/forum/" 
 
 
 
#######################
#       Classes       #               
#######################
#Align to X
class Create_Skin(bpy.types.Operator):  
    bl_idname = "object.createskin"  
    bl_label = "Create Skin"  
    bl_options = {'REGISTER', 'UNDO'}
 
    def execute(self, context):
        #Creata plane and enter in edit mode
        bpy.ops.mesh.primitive_cube_add(radius=1, view_align=False, enter_editmode=True, location=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
 
        #Align to X
        bpy.ops.object.align2x()
 
        #remove doubles
        bpy.ops.mesh.remove_doubles()
 
        #Go in Object mode
        bpy.ops.object.editmode_toggle()
 
        #Add Mirror
        bpy.ops.object.modifier_add(type='MIRROR')
 
        #Cage On/Off
        bpy.ops.object.mirrorcageonoff()
 
 
        #Add Skin modifier
        bpy.ops.object.modifier_add(type='SKIN')
 
        #Smooth Shading
        bpy.context.object.modifiers["Skin"].use_smooth_shade = True
 
        #Clippin Mirror
        bpy.context.object.modifiers["Mirror"].use_clip = True
 
        # Add Subdiv
        bpy.ops.object.modifier_add(type='SUBSURF')
 
        #Subdiv Ite 3
        bpy.context.object.modifiers["Subsurf"].levels = 3
 
        #Enter in edit mode
        bpy.ops.object.editmode_toggle()
 
 
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                area.spaces.active.use_occlude_geometry ^= True
                break # stop after the first 3D View
        return {'FINISHED'}   
 
 
#Align to X
class AlignToX(bpy.types.Operator):  
    bl_idname = "object.align2x"  
    bl_label = "Align To X"  
    bl_options = {'REGISTER', 'UNDO'}
 
    def execute(self, context):
        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
 
        for vert in bpy.context.object.data.vertices:
            if vert.select: 
                vert.co[0] = 0
                vert.co[1] = 0
        bpy.ops.object.editmode_toggle() 
        return {'FINISHED'}  
 
#Add Mirror Object
class AddMirrorObject(bpy.types.Operator):  
    bl_idname = "add.mirrorobject"  
    bl_label = "Add Mirror Object"  
    bl_options = {'REGISTER', 'UNDO'}
 
    def execute(self, context):
        if bpy.context.object.mode == "OBJECT":
            bpy.ops.object.modifier_add(type='MIRROR')
            bpy.context.object.modifiers["Mirror"].use_clip = True
            bpy.context.object.modifiers["Mirror"].show_on_cage = True
 
        elif bpy.context.object.mode == "EDIT":
            bpy.ops.object.modifier_add(type='MIRROR')
            bpy.context.object.modifiers["Mirror"].use_clip = True
            bpy.context.object.modifiers["Mirror"].show_on_cage = True
            bpy.context.object.modifiers["Mirror"].show_in_editmode = True
 
        return {'FINISHED'}  
 
#Apply Mirror
class ApplyMirror(bpy.types.Operator):  
    bl_idname = "apply.mirror"  
    bl_label = "Apply Mirror"  
    bl_options = {'REGISTER', 'UNDO'}
 
    def execute(self, context):
        if bpy.context.object.mode == "OBJECT":
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Mirror")
 
 
        elif bpy.context.object.mode == "EDIT":
            bpy.ops.object.mode_set(mode = 'OBJECT')
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Mirror")
            bpy.ops.object.mode_set(mode = 'EDIT')
 
        return {'FINISHED'}   
 
#Subsurf 2
class SubSurf2(bpy.types.Operator):  
    bl_idname = "object.subsurf2"  
    bl_label = "SubSurf 2"  
    bl_options = {'REGISTER', 'UNDO'}
 
    def execute(self, context):
        if bpy.context.object.mode == "OBJECT":
            bpy.ops.object.subdivision_set(level=2)
            bpy.context.object.modifiers["Subsurf"].show_only_control_edges = True
 
        if bpy.context.object.mode == "EDIT":
            bpy.ops.object.subdivision_set(level=2)
            bpy.context.object.modifiers["Subsurf"].show_on_cage = True
            bpy.context.object.modifiers["Subsurf"].show_only_control_edges = True
            bpy.ops.object.mode_set(mode = 'EDIT')
        return {'FINISHED'}   
 
#Remove Subsurf
class RemoveSubSurf2(bpy.types.Operator):  
    bl_idname = "object.removesubsurf2"  
    bl_label = "Remove SubSurf"  
    bl_options = {'REGISTER', 'UNDO'}
 
    def execute(self, context):
        if bpy.context.object.mode == "OBJECT":
            bpy.ops.object.modifier_remove(modifier="Subsurf")
 
        if bpy.context.object.mode == "EDIT":
            bpy.ops.object.mode_set(mode = 'OBJECT')
            bpy.ops.object.modifier_remove(modifier="Subsurf")
            bpy.ops.object.mode_set(mode = 'EDIT')
        return {'FINISHED'}
 
#Apply Subsurf
class ApplySubSurf(bpy.types.Operator):  
    bl_idname = "object.applysubsurf"  
    bl_label = "Apply subsurf"  
    bl_options = {'REGISTER', 'UNDO'}
 
    def execute(self, context):
        if bpy.context.object.mode == "OBJECT":
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Subsurf")
 
        if bpy.context.object.mode == "EDIT":
            bpy.ops.object.mode_set(mode = 'OBJECT')
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Subsurf")
            bpy.ops.object.mode_set(mode = 'EDIT')
        return {'FINISHED'}   
 
#Sursurf On/Off
class SursurfOnOff(bpy.types.Operator):
    bl_idname = "object.subsurfonoff"
    bl_label = "Sursurf On/Off"
    bl_options = {'REGISTER', 'UNDO'}
 
    def execute(self, context):
        layout = self.layout 
 
        bpy.context.object.modifiers["Subsurf"].show_viewport = not bpy.context.object.modifiers["Subsurf"].show_viewport
        return {'FINISHED'} 
 
#Sursurf Edit On/Off
class SursurfEditOnOff(bpy.types.Operator):
    bl_idname = "object.subsurfeditonoff"
    bl_label = "Sursurf Edit On/Off"
    bl_options = {'REGISTER', 'UNDO'}
 
    def execute(self, context):
        layout = self.layout 
 
        bpy.context.object.modifiers["Subsurf"].show_in_editmode = not bpy.context.object.modifiers["Subsurf"].show_in_editmode
        return {'FINISHED'}  
 
#Sursurf Cage On/Off
class SursurfCageOnOff(bpy.types.Operator):
    bl_idname = "object.subsurfcageonoff"
    bl_label = "Sursurf Cage On/Off"
    bl_options = {'REGISTER', 'UNDO'}
 
    def execute(self, context):
        layout = self.layout 
 
        bpy.context.object.modifiers["Subsurf"].show_on_cage = not bpy.context.object.modifiers["Subsurf"].show_on_cage
        return {'FINISHED'}  
 
 
#Sursurf Optimal Display
class SursurfOptimalDisplay(bpy.types.Operator):
    bl_idname = "object.subsurfoptimaldisplay"
    bl_label = "Sursurf Optimal Display"
    bl_options = {'REGISTER', 'UNDO'}
 
    def execute(self, context):
        layout = self.layout 
 
        bpy.context.object.modifiers["Subsurf"].show_only_control_edges = not bpy.context.object.modifiers["Subsurf"].show_only_control_edges
        return {'FINISHED'}  
 
#######Mirror###########
 
#Mirror On/Off
class MirrorOnOff(bpy.types.Operator):
    bl_idname = "object.mirroronoff"
    bl_label = "Mirror On/Off"
    bl_options = {'REGISTER', 'UNDO'}
 
    def execute(self, context):
        layout = self.layout 
 
        bpy.context.object.modifiers["Mirror"].show_viewport = not bpy.context.object.modifiers["Mirror"].show_viewport
        return {'FINISHED'} 
 
#Mirror Cage On/Off
class MirrorCageOnOff(bpy.types.Operator):
    bl_idname = "object.mirrorcageonoff"
    bl_label = "Mirror Cage On/Off"
    bl_options = {'REGISTER', 'UNDO'}
 
    def execute(self, context):
        layout = self.layout 
 
        bpy.context.object.modifiers["Mirror"].show_on_cage = not bpy.context.object.modifiers["Mirror"].show_on_cage
        return {'FINISHED'}  
 
#Mirror Clipping
class MirrorClipping(bpy.types.Operator):
    bl_idname = "object.mirrorclipping"
    bl_label = "Mirror Clipping"
    bl_options = {'REGISTER', 'UNDO'}
 
    def execute(self, context):
        layout = self.layout 
 
        bpy.context.object.modifiers["Mirror"].use_clip = not bpy.context.object.modifiers["Mirror"].use_clip
        return {'FINISHED'} 
 
#Add Mirror Object
class AddMirrorObject(bpy.types.Operator):  
    bl_idname = "add.mirrorobject"  
    bl_label = "Add Mirror Object"  
    bl_options = {'REGISTER', 'UNDO'}
 
    def execute(self, context):
        if bpy.context.object.mode == "OBJECT":
            bpy.ops.object.modifier_add(type='MIRROR')
            bpy.context.object.modifiers["Mirror"].use_clip = True
            bpy.context.object.modifiers["Mirror"].show_on_cage = True
            bpy.ops.object.modifier_move_up(modifier="Mirror")
            bpy.ops.object.modifier_move_up(modifier="Mirror")
            bpy.ops.object.modifier_move_up(modifier="Mirror")
 
 
        elif bpy.context.object.mode == "EDIT":
            bpy.ops.object.modifier_add(type='MIRROR')
            bpy.context.object.modifiers["Mirror"].use_clip = True
            bpy.context.object.modifiers["Mirror"].show_on_cage = True
            bpy.context.object.modifiers["Mirror"].show_in_editmode = True
            bpy.ops.object.modifier_move_up(modifier="Mirror")
            bpy.ops.object.modifier_move_up(modifier="Mirror")
            bpy.ops.object.modifier_move_up(modifier="Mirror")
 
        return {'FINISHED'}  
 
#Apply Mirror
class ApplyMirror(bpy.types.Operator):  
    bl_idname = "apply.mirror"  
    bl_label = "Apply Mirror"  
    bl_options = {'REGISTER', 'UNDO'}
 
    def execute(self, context):
        if bpy.context.object.mode == "OBJECT":
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Mirror")
 
 
        elif bpy.context.object.mode == "EDIT":
            bpy.ops.object.mode_set(mode = 'OBJECT')
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Mirror")
            bpy.ops.object.mode_set(mode = 'EDIT')
 
        return {'FINISHED'}   
 
#######Subsurf###########
 
#Subsurf 
class SubSurf2(bpy.types.Operator):  
    bl_idname = "object.subsurf2"  
    bl_label = "SubSurf 2"  
    bl_options = {'REGISTER', 'UNDO'}
 
    def execute(self, context):
        if bpy.context.object.mode == "OBJECT":
            bpy.ops.object.subdivision_set(level=2)
            bpy.context.object.modifiers["Subsurf"].show_only_control_edges = True
 
        if bpy.context.object.mode == "EDIT":
            bpy.ops.object.subdivision_set(level=2)
            bpy.context.object.modifiers["Subsurf"].show_on_cage = True
            bpy.context.object.modifiers["Subsurf"].show_only_control_edges = True
            bpy.ops.object.mode_set(mode = 'EDIT')
        return {'FINISHED'}   
 
#Remove Subsurf
class RemoveSubSurf2(bpy.types.Operator):  
    bl_idname = "object.removesubsurf2"  
    bl_label = "Remove SubSurf"  
    bl_options = {'REGISTER', 'UNDO'}
 
    def execute(self, context):
        if bpy.context.object.mode == "OBJECT":
            bpy.ops.object.modifier_remove(modifier="Subsurf")
 
        if bpy.context.object.mode == "EDIT":
            bpy.ops.object.mode_set(mode = 'OBJECT')
            bpy.ops.object.modifier_remove(modifier="Subsurf")
            bpy.ops.object.mode_set(mode = 'EDIT')
        return {'FINISHED'}
 
#Apply Subsurf
class ApplySubSurf(bpy.types.Operator):  
    bl_idname = "object.applysubsurf"  
    bl_label = "Apply subsurf"  
    bl_options = {'REGISTER', 'UNDO'}
 
    def execute(self, context):
        if bpy.context.object.mode == "OBJECT":
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Subsurf")
 
        if bpy.context.object.mode == "EDIT":
            bpy.ops.object.mode_set(mode = 'OBJECT')
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Subsurf")
            bpy.ops.object.mode_set(mode = 'EDIT')
        return {'FINISHED'}   
 
#Sursurf On/Off
class SursurfOnOff(bpy.types.Operator):
    bl_idname = "object.subsurfonoff"
    bl_label = "Sursurf On/Off"
    bl_options = {'REGISTER', 'UNDO'}
 
    def execute(self, context):
        layout = self.layout 
 
        bpy.context.object.modifiers["Subsurf"].show_viewport = not bpy.context.object.modifiers["Subsurf"].show_viewport
        return {'FINISHED'} 
 
#Sursurf Edit On/Off
class SursurfEditOnOff(bpy.types.Operator):
    bl_idname = "object.subsurfeditonoff"
    bl_label = "Sursurf Edit On/Off"
    bl_options = {'REGISTER', 'UNDO'}
 
    def execute(self, context):
        layout = self.layout 
 
        bpy.context.object.modifiers["Subsurf"].show_in_editmode = not bpy.context.object.modifiers["Subsurf"].show_in_editmode
        return {'FINISHED'}  
 
 
#Apply Skin
class ApplySubSurf(bpy.types.Operator):  
    bl_idname = "object.applyskin"  
    bl_label = "Apply Skin"  
    bl_options = {'REGISTER', 'UNDO'}
 
    def execute(self, context):
        if bpy.context.object.mode == "OBJECT":
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Mirror")
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Skin")
 
        if bpy.context.object.mode == "EDIT":
            bpy.ops.object.mode_set(mode = 'OBJECT')
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Mirror")
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Skin")
            bpy.ops.object.mode_set(mode = 'EDIT')
        return {'FINISHED'}         
#################
#Panel          #
#################     
class Fast_Skin(bpy.types.Panel):
    bl_idname = "view3D.fast_Skin"
    bl_label = "Fast skin"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Tools"
 
    def draw(self, context):
        layout = self.layout
 
 
 
 
        if bpy.context.area.type == 'VIEW_3D' and not bpy.context.object:
 
            layout.operator("object.createskin", text='Create Skin', icon='POSE_HLT')
 
        elif bpy.context.area.type == 'VIEW_3D' and bpy.context.object.mode == 'OBJECT':
            layout.operator("object.createskin", text='Create Skin', icon='POSE_HLT')
 
 
        elif bpy.context.object.mode == 'EDIT':  
            if context.scene.Skin_Skin==False:
                layout.prop(context.scene, "Skin_Skin", text="Skin Properties", icon='TRIA_DOWN')     
                layout.operator("object.skin_root_mark", text='Mark Root', icon='META_EMPTY')
 
                row = layout.row(align=True) 
                row.operator("object.skin_loose_mark_clear", text='Mark Loose').action='MARK'
                row.operator("object.skin_loose_mark_clear", text='Clear Loose').action='CLEAR'
                row = layout.row() 
                row.operator("object.skin_radii_equalize", text="Equalize Radii")
                row = layout.row() 
                row.operator("object.applyskin", text="Apply skin/Mirror", icon='FILE_TICK')
 
            else:
                layout.prop(context.scene, "Skin_Skin", text="Skin Properties", icon='TRIA_RIGHT')
 
            #box.operator("object.skin_radii_equalize", text='Equalize Radii')
 
            if context.scene.Skin_Subdivs==False:
                layout.prop(context.scene, "Skin_Subdivs", text="Subdivs Properties", icon='TRIA_DOWN')   
 
                #Subsurf
                box = layout.box()
                row = box.row(align=True)
                is_subsurf = False
                for mode in bpy.context.object.modifiers :
                    if mode.type == 'SUBSURF' :
                        is_subsurf = True
                if is_subsurf == True :
                    row.operator("object.removesubsurf2", text="Del Subsurf", icon='X')
 
                else :
                    row.operator("object.subsurf2", text="Add Subsurf", icon='MOD_SUBSURF')
 
                row.operator("object.applysubsurf", text="Apply Subsurf", icon='FILE_TICK')
 
 
                #On/Off, Edit
                row = box.row(align=True)
                for mode in bpy.context.object.modifiers :
                    if mode.type == 'SUBSURF' :
                        is_subsurf = True
                if is_subsurf == True :
 
                    #View On/Off
                    if bpy.context.object.modifiers["Subsurf"].show_viewport == (True) :
                        row.operator("object.subsurfonoff", text="View",icon='RESTRICT_VIEW_OFF')
                    else:
                        row.operator("object.subsurfonoff", text="View",icon='VISIBLE_IPO_OFF')   
                    #Edit On/Off
                    if bpy.context.object.modifiers["Subsurf"].show_in_editmode == (True) :
                        row.operator("object.subsurfeditonoff", text="Edit",icon='EDITMODE_HLT')
                    else:
                        row.operator("object.subsurfeditonoff", text="Edit",icon='SNAP_VERTEX') 
 
                row = box.row()
                row.label('Subdivisions :')    
                row = box.row(align=True) 
                row.operator("object.subdivision_set", text='0').level=0
                row.operator("object.subdivision_set", text='1').level=1
                row.operator("object.subdivision_set", text='2').level=2
                row.operator("object.subdivision_set", text='3').level=3
                row.operator("object.subdivision_set", text='4').level=4
 
 
            else:
                layout.prop(context.scene, "Skin_Subdivs", text="Subdivs Properties", icon='TRIA_RIGHT')
 
            #Mirror
            if context.scene.Skin_Mirror==False:
                layout.prop(context.scene, "Skin_Mirror", text="Mirror Properties", icon='TRIA_DOWN') 
 
                box = layout.box()
                row = box.row()
                is_mirror = False
                for mode in bpy.context.object.modifiers :
                    if mode.type == 'MIRROR' :
                        is_mirror = True
                if is_mirror == True :
                    row.operator("object.modifier_remove", text="Del Mirror", icon='X').modifier="Mirror"
                else:
                    row.operator("add.mirrorobject", icon = 'MOD_MIRROR', text="Add Mirror")
 
                #On/Off, Edit, Cage
                row = box.row(align=True)
                for mode in bpy.context.object.modifiers :
                    if mode.type == 'MIRROR' :
                        is_mirror = True
                if is_mirror == True :
 
                    #View On/Off
                    if bpy.context.object.modifiers["Mirror"].show_viewport == (True) :
                        row.operator("object.mirroronoff", text="View",icon='RESTRICT_VIEW_OFF')
                    else:
                        row.operator("object.mirroronoff", text="View",icon='VISIBLE_IPO_OFF')  
                    #Cage On/Off
                    if bpy.context.object.modifiers["Mirror"].show_on_cage == (True) :
                        row.operator("object.mirrorcageonoff", text="Cage",icon='OUTLINER_OB_MESH')
                    else:
                        row.operator("object.mirrorcageonoff", text="Cage",icon='OUTLINER_DATA_MESH') 
                    #Clipping
                    if bpy.context.object.modifiers["Mirror"].use_clip == (True) :
                        row.operator("object.mirrorclipping", text="Clipping",icon='UV_EDGESEL')
                    else:
                        row.operator("object.mirrorclipping", text="Clipping",icon='SNAP_EDGE') 
 
                row = box.row()
                row.operator("apply.mirror", text="Apply Mirror", icon='FILE_TICK')             
 
            else:
                layout.prop(context.scene, "Skin_Mirror", text="Mirror Properties", icon='TRIA_RIGHT')
 
 
            #Mirror
            if context.scene.Skin_Shading==False:
                layout.prop(context.scene, "Skin_Shading", text="Shading Properties", icon='TRIA_DOWN')
                box = layout.box()
                row = box.row() 
                row.prop(context.space_data, "use_occlude_geometry")
            else:
                layout.prop(context.scene, "Skin_Shading", text="Shading Properties", icon='TRIA_RIGHT')
 
            layout.label('Info :')
            layout.label('Skin Radius = CTRL + A, plus X or Y  :')
            layout.label('Add point on X = CTRL + RMB :')
 
 
def register():
    bpy.utils.register_module(__name__)
    update_panel(None, bpy.context)
 
def unregister():
    bpy.utils.unregister_module(__name__)
 
if __name__ == "__main__":
    register()    
