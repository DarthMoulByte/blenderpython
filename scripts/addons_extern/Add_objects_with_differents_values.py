'''
Copyright (C) 2015 Cedric Lepiller
pitiwazou@hotmail.com

Created by Cedric Lepiller

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


bl_info = {
    "name": "Add objects with differents values",
    "description": "",
    "author": "Pitiwazou, Pistiwique",
    "version": (0, 0, 1),
    "blender": (2, 76, 0),
    "location": "View3D",
    "warning": "This addon is still in development.",
    "wiki_url": "",
    "category": "Add Mesh" }
    


import bpy


########################
#      Properties      #               
########################

class WazouAddCustom_Meshes(bpy.types.AddonPreferences):
    """Creates the tools in a Panel, in the scene context of the properties editor"""
    bl_idname = __name__

    bpy.types.Scene.Enable_Tab_01 = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.Enable_Tab_02 = bpy.props.BoolProperty(default=False)
    
    def draw(self, context):
        layout = self.layout
        
        layout.prop(context.scene, "Enable_Tab_01", text="Info", icon="QUESTION")  
        if context.scene.Enable_Tab_01:
            row = layout.row()
            layout.label(text="This Addon Adds objects with differents values")
            
        layout.prop(context.scene, "Enable_Tab_02", text="URL's", icon="URL") 
        if context.scene.Enable_Tab_02:
            row = layout.row()    
            
            row.operator("wm.url_open", text="Pitiwazou.com").url = "http://www.pitiwazou.com/"
            row.operator("wm.url_open", text="Wazou's Ghitub").url = "https://github.com/pitiwazou/Scripts-Blender"
            row.operator("wm.url_open", text="BlenderLounge Forum ").url = "http://blenderlounge.fr/forum/"      


###########################
#      Enum property      #               
########################### 


###################Grid######################
#############################################

# fonction qui est lancée quand on choisi dans la liste du panel 
#et cette fonction nous permet d afficher les differentes proprietes
def Add_Grid(self, context):   
    if bpy.context.window_manager.primitive_grid_add == "0":
        x_subdivs = 0
        y_subdivs = 0   
    if bpy.context.window_manager.primitive_grid_add == "5":
        x_subdivs = 5
        y_subdivs = 5       
    if bpy.context.window_manager.primitive_grid_add == "10":
        x_subdivs = 10
        y_subdivs = 10
    elif bpy.context.window_manager.primitive_grid_add == "20":
        x_subdivs = 20
        y_subdivs = 20 
    elif bpy.context.window_manager.primitive_grid_add == "30":
        x_subdivs = 30
        y_subdivs = 30     
    bpy.ops.mesh.primitive_grid_add(x_subdivisions=x_subdivs, y_subdivisions=y_subdivs)

#enum property qui permet de creer X variantes de proprietes
bpy.types.WindowManager.primitive_grid_add = bpy.props.EnumProperty(
            items=(('0', "0", ''),
                   ('5', "5", ''),
                   ('10', "10", ''),
                   ('20', "20", ''),
                   ('30', "30", '')),
                   default='10',
                   name='',
                   update=Add_Grid)        
#pour chaque item on cree un identifiant, un nom et une icone


#################Spheres#####################
#############################################

# fonction qui est lancée quand on choisi dans la liste du panel 
#et cette fonction nous permet d afficher les differentes proprietes
def Add_Sphere(self, context):       
    if bpy.context.window_manager.primitive_sphere_add == "8":
        segments = 8
        ring = 6
    elif bpy.context.window_manager.primitive_sphere_add == "16":
        segments = 16
        ring = 8 
    elif bpy.context.window_manager.primitive_sphere_add == "24":
        segments = 24
        ring = 12  
    elif bpy.context.window_manager.primitive_sphere_add == "32":
        segments = 32
        ring = 16    
    #bien penser a ajouter le code de creation de l'objet ainsi que les valeurs qu'on veut lui ajouter
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=ring)

#enum property qui permet de creer X variantes de proprietes
bpy.types.WindowManager.primitive_sphere_add = bpy.props.EnumProperty(
            items=(('8', "8", ''),
                   ('16', "16", ''),
                   ('24', "24", ''),
                   ('32', "32", '')),
                   default='16',
                   name='',
                   update=Add_Sphere)        
#pour chaque item on cree un identifiant, un nom et une icone

################Cylindres####################
#############################################

# fonction qui est lancée quand on choisi dans la liste du panel 
#et cette fonction nous permet d afficher les differentes proprietes
def Add_Cylinders(self, context):       
    if bpy.context.window_manager.primitive_cylinder_add == "8":
        vertices = 8
    elif bpy.context.window_manager.primitive_cylinder_add == "16":
        vertices = 16
    elif bpy.context.window_manager.primitive_cylinder_add == "24":
        vertices = 24
    elif bpy.context.window_manager.primitive_cylinder_add == "32":
        vertices = 32 
    elif bpy.context.window_manager.primitive_cylinder_add == "64":
        vertices = 64     
    #bien penser a ajouter le code de creation de l'objet ainsi que les valeurs qu'on veut lui ajouter
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices)

#enum property qui permet de creer X variantes de proprietes
bpy.types.WindowManager.primitive_cylinder_add = bpy.props.EnumProperty(
            items=(('8', "8", ''),
                   ('16', "16", ''),
                   ('24', "24", ''),
                   ('32', "32", ''),
                   ('64', "64", '')),
                   default='16',
                   name='',
                   update=Add_Cylinders)        
#pour chaque item on cree un identifiant, un nom et une icone

 
       


###################
#      Panel      #               
###################       
class Custom_Objects(bpy.types.Panel):
    bl_idname = "custom_objects"
    bl_label = "Custom Objects"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Create"
    
    def draw(self, context):
        layout = self.layout
        WM = bpy.context.window_manager
        
        col = layout.column(align=True)
        row = col.row(align=True)
        row.prop(WM, "primitive_sphere_add", text="", icon='MESH_UVSPHERE')
        row.prop(WM, "primitive_grid_add", text="", icon='MESH_GRID')
        row.prop(WM, "primitive_cylinder_add", text="", icon='MESH_CYLINDER')
        


def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)
    
if __name__ == "__main__":
    register()
        
