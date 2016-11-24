bl_info = {
    "name": "Fracture Helpers",
    "author": "scorpion81 and Dennis Fassbaender",
    "version": (2, 00, 34),
    "blender": (2, 77, 0),
    "location": "Tool Shelf > Fracture > Fracture Helpers",
    "description": "Several fracture modifier setup helpers",
    "warning": "",
    "wiki_url": "",
    "category": "Object"}

import bpy
import math
import random
from bpy_extras import view3d_utils
from mathutils import Vector, Matrix

def setup_particles(count=100):
    ob = bpy.context.active_object
    bpy.ops.object.particle_system_add()
    #make particle system settings here....
    ob.particle_systems[0].name = "ParticleHelper"
    psys = ob.particle_systems[0].settings
    psys.count = count
    psys.frame_start = 1
    psys.frame_end = 1
    psys.lifetime = 1
    psys.factor_random = 0.0
    psys.normal_factor = 0.0
    psys.effector_weights.gravity = 0.0
    psys.draw_method = 'NONE'
    psys.use_render_emitter = False
    psys.render_type = 'NONE'
    psys.use_modifier_stack = True
    psys.emit_from = 'VOLUME'
    psys.distribution = 'RAND'
    
def raycast(context, event, ray_max=1000.0, group=None):
    """Run this function on left mouse, execute the ray cast"""
    # get the context arguments
    scene = context.scene
    region = context.region
    rv3d = context.region_data
    coord = event.mouse_region_x, event.mouse_region_y
    hit_world = None
    normal_world = None

    # get the ray from the viewport and mouse
    view_vector = view3d_utils.region_2d_to_vector_3d(region, rv3d, coord)
    ray_origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, coord)

    ray_target = ray_origin + (view_vector * ray_max)

    def visible_objects_and_duplis(group=None):
        """Loop over (object, matrix) pairs (mesh only)"""

        for obj in context.visible_objects:

            if group is not None:
                if obj.name in group.objects:
                   continue

            if obj.type == 'MESH':
                yield (obj, obj.matrix_world.copy())

            if obj.dupli_type != 'NONE':
                obj.dupli_list_create(scene)
                for dob in obj.dupli_list:
                    obj_dupli = dob.object
                    if obj_dupli.type == 'MESH':
                        yield (obj_dupli, dob.matrix.copy())

            obj.dupli_list_clear()

    def obj_ray_cast(obj, matrix):
        """Wrapper for ray casting that moves the ray into object space"""

        # get the ray relative to the object
        matrix_inv = matrix.inverted()
        ray_origin_obj = matrix_inv * ray_origin
        ray_target_obj = matrix_inv * ray_target

        # cast the ray
        result, hit, normal, face_index = obj.ray_cast(ray_origin_obj, ray_target_obj)

        if face_index != -1:
            return hit, normal, face_index
        else:
            return None, None, None

    # cast rays and find the closest object
    best_length_squared = ray_max * ray_max
    best_obj = None

    for obj, matrix in visible_objects_and_duplis(group=group):
        if obj.type == 'MESH':
            hit, normal, face_index = obj_ray_cast(obj, matrix)
            if hit is not None:
                hit_world = matrix * hit
                normal_world = matrix * normal
                scene.cursor_location = hit_world
                length_squared = (hit_world - ray_origin).length_squared
                if length_squared < best_length_squared:
                    best_length_squared = length_squared
                    best_obj = obj

    # now we have the object under the mouse cursor,
    # we could do lots of stuff but for the example just select.
    if best_obj is not None:
        best_obj.select = True
        context.scene.objects.active = best_obj

    return hit_world, normal_world

def check_fm():
    if bpy.context.active_object is None:
        return False

    for md in bpy.context.active_object.modifiers:
        if md.type == 'FRACTURE':
            return True
    return False

class MainOperationsPanel(bpy.types.Panel):
    bl_label = "Main operations" 
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Fracture"
    #bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        if not context.object:
            self.layout.label("Please select atleast one object first")
            
        else:
            layout = self.layout
            col = layout.column(align=True)
            md = find_modifier(context.object, "FRACTURE")
            if md:
                row = col.row(align=True)
                row.context_pointer_set("modifier", md)
                row.operator("object.modifier_remove", text = "Remove Fracture", icon='X')
                row.prop(md, "show_render", text="")
                row.prop(md, "show_viewport", text="")
                
                col.operator("object.fracture", icon='MOD_EXPLODE')
                col.prop(md, "auto_execute", text="Toggle Automatic Execution", icon='FILE_REFRESH')
            else:
                col.operator("object.fracture", icon='MOD_EXPLODE', text="Add Fracture")
                if not context.object.rigid_body:
                    col.operator("rigidbody.object_add", icon='MESH_ICOSPHERE',text="Add Rigidbody")
                else:
                    col.operator("rigidbody.object_remove", icon='X',text="Remove Rigidbody")
            if context.object.rigid_body:
                rb = context.object.rigid_body
                #col.prop(rb, "enabled")
                layout.prop(rb, "type")
                row = layout.row()
                row.prop(rb, "kinematic", text="Animated")
                if rb.type == "ACTIVE":
                    row.prop(rb, "use_kinematic_deactivation", text="Triggered")
                
                    row = layout.row()
                    row.prop(rb, "is_trigger")
                    row.prop(rb, "is_ghost")
                    
                    layout.prop(rb, "mass")
                

class VIEW3D_SettingsPanel(bpy.types.Panel):
    bl_label = "3D View Settings" 
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Fracture"
    #bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        if not context.object:
            self.layout.label("Please select atleast one object first")
            
        else:
            layout = self.layout
            col = layout.column(align=True)
            col.prop(context.object, "show_wire", text="Toggle Wireframe", icon ='WIRE')
            col.prop(context.space_data, "show_relationship_lines", text="Toggle Relationship Lines", icon = 'PARTICLE_TIP')
            if len(context.object.particle_systems) > 0:
                col.prop(context.object.particle_systems[0].settings, "draw_method", text="", icon = 'MOD_PARTICLES')
            
class ViewOperatorFracture(bpy.types.Operator):
    """Modal mouse based object fracture"""
    bl_idname = "view3d.mouse_based_fracture"
    bl_label = "Mouse based fracture"
    scaling = False
    hit2d = None
    size = 1.0
    act = None
    md = None
    gr = None
    msg = "Press LMB over fractured object to create helper, drag mouse to change size, release LMB to confirm, RMB or Esc ends modal operator"
    scale = Vector((1, 1, 1))

    def modal(self, context, event):
        #if event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
        #    # allow navigation
        #    return {'PASS_THROUGH'}
        if event.type == 'LEFTMOUSE':
            if event.value == 'PRESS':
                hit, normal = raycast(context, event, 1000.0, self.gr)
                if hit is not None and check_fm():
                    self.act = context.active_object
                    #self.act.select = False
                    if self.act.mouse_mode == "Radial":
                        vec = normal.normalized()
                        #if (vec != Vector((0, 0, 1))):
                        #    vec = vec.cross(Vector((0, 0, 1))
                        
                        self.scale[0] = 1 #if vec[0] == 0 else vec[0] * 0
                        self.scale[1] = 1 #if vec[1] == 0 else vec[1] * 0
                        self.scale[2] = 1 #if vec[2] == 0 else vec[2] * 0
                        
                        print(self.scale)
                        
                        #bpy.ops.mesh.primitive_uv_sphere_add(size = 0.05, location=hit, rotation=rot, \
                        #                                     segments=self.act.mouse_segments, ring_count=self.act.mouse_rings)
                        #bpy.ops.object.editmode_toggle()
                        #bpy.ops.mesh.remove_doubles()
                        #bpy.ops.object.editmode_toggle()
                        
                        #sphere wont work so try with concentric circles
                        radius = 0.15
                        bpy.ops.mesh.primitive_circle_add(radius=radius, \
                                                              vertices=self.act.mouse_segments, \
                                                              location=hit)
                        
                        bpy.ops.object.editmode_toggle()
             
                        radius += 0.1
                        for r in range(self.act.mouse_rings):
                            bpy.ops.mesh.primitive_circle_add(radius=radius, \
                                                              vertices=self.act.mouse_segments, \
                                                              location=hit)
                            ob = context.active_object
                            ob.select = True
                            radius += 0.1
                        
                        bpy.ops.object.editmode_toggle()
                        
                        z = Vector((0, 0, 1))
                        ob = context.active_object
                        angle = vec.angle(z)
                        axis = z.cross(vec)
                        mat = Matrix.Rotation(angle, 4, axis)
                        mat.translation = self.act.matrix_world.inverted() * hit
                        
                        ob.matrix_world = self.act.matrix_world * mat
                                                     
                    else:
                        if self.act.mouse_object == "Cube":
                            bpy.ops.mesh.primitive_cube_add(radius = 0.05, location=hit)
                        elif self.act.mouse_object == "Sphere":
                            bpy.ops.mesh.primitive_uv_sphere_add(size = 0.05, location=hit)
                        else:
                            if self.act.mouse_custom_object == "":
                                self.report({'WARNING'}, "Need to pick a custom object, please retry")
                                return {'CANCELLED'}
                                
                            ob = bpy.data.objects[self.act.mouse_custom_object]
                            if ob != None:
                                context.scene.objects.active = ob
                                self.act.select = False
                                ob.select = True
                                bpy.ops.object.duplicate()
                                nob = context.active_object
                                nob.location = hit
                            else:
                                self.report({'WARNING'}, "Need to pick a custom object, please retry")
                                return {'CANCELLED'}
                    self.scaling = True
                    self.hit2d = event.mouse_region_x, event.mouse_region_y
                    context.active_object.draw_type = 'WIRE'
            elif event.value == 'RELEASE':
                   
                    self.hit2d = None
                    #print(self.act, context.active_object)
                    if not self.scaling:
                        self.report({'WARNING'}, "Ambigous target object, please retry")
                        context.object.mouse_status = "Start mouse based fracture"
                        context.area.header_text_set()
                        return {'CANCELLED'}

                    self.scaling = False
                    if self.act != context.active_object and self.act is not None \
                    and context.active_object is not None:
                        if self.act.mouse_mode == "Uniform":
                            setup_particles(self.act.mouse_count)
                        self.gr.objects.link(context.active_object)
                        context.active_object.parent = self.act
                        context.active_object.location -= self.act.location
                        #put last helpers on a higher layer, in this case layer 16.
                        for x in range(0, 19):
                            if x == 15:
                                context.active_object.layers[x] = True
                            else:
                                context.active_object.layers[x] = False
                        
                        context.active_object.hide = True
                        context.scene.objects.active = self.act
                        if check_fm(): #active object changes here, so check again
                            bpy.ops.object.fracture_refresh(reset=False)
            return {'RUNNING_MODAL'}
        elif event.type == 'MOUSEMOVE':
            if not self.scaling:
                #main(context, event)
                pass
            else:
                hit2d = event.mouse_region_x, event.mouse_region_y
                size = Vector(hit2d).length - Vector(self.hit2d).length
                size *= 0.25
                if self.act.mouse_mode == "Uniform":
                    context.active_object.dimensions = (size, size, size)
                else:
                    context.active_object.dimensions = (size * self.scale[0], 
                                                        size * self.scale[1],
                                                        size * self.scale[2])
                #self.hit2d = hit2d
            return {'RUNNING_MODAL'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            context.area.header_text_set()
            context.object.mouse_status = "Start mouse based fracture"
            #delete group and group objects if desired
            if context.object.delete_helpers:
                for o in self.gr.objects:
                    self.gr.objects.unlink(o)
                    context.scene.objects.unlink(o)
                    o.user_clear()
                    bpy.data.objects.remove(o)
                bpy.data.groups.remove(self.gr)
                
            return {'CANCELLED'}

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        
        if context.active_object is None:
             self.report({'WARNING'}, "Need an Active object with Fracture Modifier!")
             return {'CANCELLED'}
            
        if context.space_data.type == 'VIEW_3D':
            self.md = None
            for md in context.active_object.modifiers:
                if md.type == 'FRACTURE':
                    self.md = md
                    break
            if self.md is not None:
                if bpy.data.groups.get("InteractiveHelpers", None) is None:
                    self.gr = bpy.data.groups.new("InteractiveHelpers")
                else:
                    self.gr = bpy.data.groups["InteractiveHelpers"]
                self.act = context.active_object
                self.md.extra_group = self.gr
                self.md.refresh = False
                if self.act.mouse_mode == "Uniform":
                    self.md.point_source = md.point_source.union({'EXTRA_PARTICLES'})
                    self.md.use_particle_birth_coordinates = True
                else:
                    self.md.point_source = md.point_source.union({'EXTRA_VERTS'})
                
                context.area.header_text_set(text=self.msg)
                context.object.mouse_status = "Mouse based fracture running"
                context.object.show_wire = True
                context.scene.layers[15] = True
                context.scene.layers[0] = True
                context.window_manager.modal_handler_add(self)
            else:
                self.report({'WARNING'}, "Active object must have a Fracture Modifier")
                return {'CANCELLED'}
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "Active space must be a View3d")
            return {'CANCELLED'}

def main(context, start=1, random=0.0):
   context.scene.layers[19] = True
   act = context.active_object
   act.select = False
   gr = None
   
   for ob in bpy.data.objects:
       try:
           ob["isCurve"] = 0
       except KeyError:
           pass

   for md in act.modifiers:
       if md.type == 'FRACTURE':
          gr = md.extra_group
          act.show_wire = True
          break
   for ob in context.selected_objects:
       if ob != act:
            ob["isCurve"] = (ob.type == 'CURVE')
            if (gr is not None) and ob.name in gr.objects:
                #already in existing group, skip  
                ob.select = False
            
   bpy.ops.view3d.snap_cursor_to_selected()
   bpy.ops.object.duplicate()
   bpy.ops.anim.keyframe_clear_v3d()   
   bpy.ops.rigidbody.objects_remove()
   
   for ob in context.selected_objects:
       if ob != act:
            context.scene.objects.active = ob
            ob.draw_type = 'BOUNDS'
            ob.hide_render = True
            ob.show_name = True
            ob.show_x_ray = True
            ob.name = ob.name.split(".")[0] + "_helper"
            ob.layers[19] = True
            for x in range(0, 19):
                ob.layers[x] = False
            
                               
   bpy.ops.object.convert(target='MESH', keep_original=False)
   
   if gr is None:
       gr = bpy.data.groups.new("Helper")
       
   if (context.scene.rigidbody_world):
        context.scene.frame_set(context.scene.rigidbody_world.point_cache.frame_start)
   else:
        context.scene.frame_set(1.0)
          
   for ob in context.selected_objects:
       if ob != act:
            print(ob, act)
            context.scene.objects.active = ob
            gr.objects.link(ob)
            
            ob.matrix_world = act.matrix_world.inverted() * ob.matrix_world
            ob.parent = act
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            bpy.ops.view3d.snap_selected_to_cursor(use_offset=True)

            ob.modifiers.new(type='PARTICLE_SYSTEM', name='ParticleHelper')
            #make particle system settings here....
            psys = ob.particle_systems[0].settings
            psys.count = 100
            psys.frame_start = start
            psys.frame_end = 1
            psys.lifetime = 1
            psys.factor_random = 1.5
            psys.normal_factor = 0.0
            psys.effector_weights.gravity = 0.0
            psys.draw_method = 'NONE'
            psys.use_render_emitter = False
            psys.render_type = 'NONE'
            psys.use_modifier_stack = True
                
            if (ob["isCurve"]):
                psys.emit_from = 'VERT'
            else:
                psys.emit_from = 'VOLUME'
                psys.distribution = 'RAND'
                
            ob.select = False
            
   context.scene.objects.active = act
   for md in act.modifiers:
       if md.type == 'FRACTURE':
           md.extra_group = gr
           md.refresh = False
           md.point_source = md.point_source.union({'EXTRA_PARTICLES'})
           md.use_particle_birth_coordinates = False
           break

   act.select = True
   bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
   act.select = False
   
   bpy.ops.object.fracture_refresh(reset=True)
   
   act = context.scene.objects.active
   use_curve = context.object.use_animation_curve
   anim_ob = context.object.animation_obj
   if (use_curve == True and anim_ob != ""):
       anim_ob = bpy.data.objects[anim_ob] 
       for ob in bpy.data.objects:
            try:
                if ((ob["isCurve"] == 1) and (ob.type == 'CURVE')):
                    print("FOUND CURVE", ob)
                    ob.select = True
                    context.scene.objects.active = ob
                    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
                    ob["isCurve"] = 0
                else:
                    ob.select = False
                    ob["isCurve"] = 0
            except KeyError:
                ob.select = False
                
       anim_ob.select = True
       bpy.ops.object.parent_set(type='PATH_CONST')
       context.scene.objects.active.select = False
       context.scene.objects.active = anim_ob
       bpy.ops.rigidbody.objects_add(type='ACTIVE')
       anim_ob.rigid_body.kinematic = True
       anim_ob.rigid_body.is_ghost = act.animation_ghost
       anim_ob.rigid_body.is_trigger = True
       anim_ob.rigid_body.use_margin = True
       anim_ob.rigid_body.collision_margin = 0.0
       bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
       
       bpy.ops.object.location_clear()
       ctx = context.copy()
       ctx["constraint"] = anim_ob.constraints["AutoPath"]
       anim_ob.constraints["AutoPath"].use_curve_follow = True
       anim_ob.constraints["AutoPath"].forward_axis = 'FORWARD_X'
       bpy.ops.constraint.followpath_path_animate(ctx, constraint="AutoPath")
       
       context.scene.objects.active = act
       act.rigid_body.enabled = True
       act.rigid_body.kinematic = True
       act.rigid_body.use_kinematic_deactivation = True
   
   context.object.animation_obj = ''
   context.object.use_animation_curve = False
   context.object.animation_ghost = False
   context.scene.update()
   
class FractureHelper(bpy.types.Operator):
    """Create helper object using an other object"""
    bl_idname = "object.fracture_helper"
    bl_label = "Generate smaller shards"
    start = bpy.props.IntProperty(name="start", default = 1)
    random = bpy.props.FloatProperty(name="random", default = 0.0)

    def execute(self, context):
        act = context.active_object is not None
        mod = False
        isNoCurve = True
        isSingle = True
        
        for md in context.active_object.modifiers:
            if md.type == 'FRACTURE':
                mod = True
                break
            
        sel = len(context.selected_objects) > 1
        for ob in context.selected_objects:
            if ob.type == 'CURVE':
                if (isNoCurve == False):
                    isSingle = False
                    break
                isNoCurve = False
        
        if not(act and sel and mod):
            self.report({'WARNING'}, "Need an active object with fracture modifier and atleast another selected object") 
            return {'CANCELLED'}
            
        if (not(isSingle) or isNoCurve) and (context.object.use_animation_curve == True) and (context.object.animation_obj == ""):
            self.report({'WARNING'}, "For animation curve please select only one curve and specify an animation object") 
            return {'CANCELLED'}
    
        main(context, self.start, self.random)
        return {'FINISHED'}
    #### Sinnvoll: Des erstellte HelperObjekt muss ans Basisobjekt geparented werden
    ####           damit es beim verschieben/rotieren mit bewegt wird!
    
    

class FracturePathPanel(bpy.types.Panel):
    bl_label = "Automations"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Fracture"
    bl_options = {'DEFAULT_CLOSED'}
  
    
    def draw(self, context):
        if not context.object:
            self.layout.label("Please select atleast one object first")
        else:
            layout = self.layout
            col = layout.column(align=True)
            row = layout.row(align=True)
            
            col.label("Path animation:", icon='PINNED')
            col.prop_search(context.object, "animation_obj", bpy.data, "objects", text="Object", icon='OBJECT_DATA')
            col.separator()
            col.prop(context.object, "use_animation_curve", text="Use As Animation Path", icon = 'ANIM')
            col.prop(context.object, "animation_ghost", text="Toggle RB Ghost", icon='GHOST_ENABLED')
            op = col.operator("object.fracture_helper", icon='MOD_PARTICLES')
            op.start = 0
            op.random = 15.0
            
            col.separator()
            col.separator()
            col.separator()
            
            col.label("Combination:", icon='PINNED')
            col.operator("object.combine_subobjects",icon='GROUP')


### Ab jetzt kommt vieles in ein Panel, finde ich besser als fuer alles ein eigenes Panel zu hab

class FractureHelperPanel(bpy.types.Panel):
    bl_label = "Generate smaller shards"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Fracture"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        if not context.object:
            self.layout.label("Please select atleast one object first")
        else:
            layout = self.layout
            col = layout.column(align=True)
            row = layout.row(align=True)
                        
            #Other objects as helpers:
            col.label(text="Smaller shards using other object:", icon='PINNED')
            #col.operator("object.fracture_helper", icon='MOD_PARTICLES')
            #col.prop(context.object, "particle_amount", text="Particle amount")
            #col.prop(context.object, "particle_random", text="Particle random")
            systems = len(context.object.particle_systems)
            col.operator("object.fracture_helper", icon='MOD_PARTICLES')
            if systems > 0:
                if systems > 1:
                    col.label(text="Only the first particle system is used as helper particle system")
                psys = context.object.particle_systems[0]
                col.prop(psys.settings, "count", text="Particle amount")
                col.prop(psys.settings, "factor_random", text="Particle random")
                
            else:
                col.label(text="Click Generate Smaller shards to make this object a helper")
        
            col.separator()
            col.separator()
            col.separator()
            
            #Mouse based helpers:
            col.label(text="Smaller shards using mouse:", icon='PINNED')
            row = col.row(align=True)
            row.prop(context.object, "mouse_mode", text="Fracture Mode", expand=True)
            if context.object.mouse_mode == "Uniform":
                row = col.row(align=True)
                row.prop(context.object, "mouse_object", text="Helper Object", expand=True)
                if (context.object.mouse_object == "Custom"):
                    col.prop_search(context.object, "mouse_custom_object", bpy.data, "objects", text="")
                col.prop(context.object, "mouse_count", text="Shard count")
            else:
                row = col.row(align=True)
                row.prop(context.object, "mouse_segments", text="Segments")
                row.prop(context.object, "mouse_rings", text="Rings")
                
            col.prop(context.object, "delete_helpers", text="Delete helpers afterwards", icon='X')
            col.operator("view3d.mouse_based_fracture", text=context.object.mouse_status, icon='RESTRICT_SELECT_OFF')
            col.separator()
            col.separator()
            col.separator()
            
            #Extract inner faces for rough edges (cluster)
            col.label(text="Rough edges:", icon='PINNED')
            col.operator("object.create_cluster_helpers", icon='FCURVE')
            col.operator("object.create_displaced_edges", icon='FCURVE')
            
            
            
class TimingPanel(bpy.types.Panel):
    bl_label = "Timing"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Fracture"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        if not context.object:
            self.layout.label("Please select atleast one object first")
        else:
            layout = self.layout
            col = layout.column(align=True)
            row = layout.row(align=True)
            
            #Time control:
            col.label(text="Delayed fracture:", icon='PINNED')
            col.prop(context.object, "is_dynamic", text="Object moves", icon='FORCE_HARMONIC')
            col.prop(context.object, "fracture_frame", text="Start fracture from frame")
            col.operator("object.fracture_frame_set", icon='PREVIEW_RANGE')

#def update_wire(self, context):
#    context.object.show_wire = context.object.use_wire

#def update_relationships(self, context):
#    for area in context.screen.areas:
#        if area.type == 'VIEW_3D':
#            for space in area.spaces:
#                if space.type == 'VIEW_3D':
#                    space.show_relationship_lines = context.object.use_relationship_lines
#                    break

#def update_visible_particles(self, context):
#    if len(context.object.particle_systems) > 0:
#        if context.object.use_visible_particles:
#            context.object.particle_systems[0].settings.draw_method = 'DOT'
#        else:
#            context.object.particle_systems[0].settings.draw_method = 'NONE'
            
#def update_autoexecute(self, context):
#    context.object.modifiers["Fracture"].auto_execute = context.object.use_autoexecute

#def update_particle_amount(self, context):
#    if len(context.object.particle_systems) > 0:
#       context.object.particle_systems[0].settings.count = context.object.particle_amount

#def update_particle_random(self, context):
#    if len(context.object.particle_systems) > 0:
#       context.object.particle_systems[0].settings.factor_random = context.object.particle_random


class FractureFrameOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.fracture_frame_set"
    bl_label = "Set start frame"
    
    def execute(self, context):
        if context.object is not None:
            mod = False
            for md in context.object.modifiers:
                if md.type == 'FRACTURE':
                    mod = True
                    break
        
            if not(mod):
                self.report({'WARNING'}, "Need an active object with fracture modifier!") 
                return {'CANCELLED'}
                
            #if FractureMod, then save preset (FrameHelperPreset) and remove mod
            ctx = context.copy()
            ctx["fracture"] = md
            bpy.ops.fracture.preset_add(ctx, name="helperpreset")
            context.object.modifiers.remove(md)
            frame_end = context.object.fracture_frame
            
            context.object.select = True
            #bpy.ops.anim.keyframe_clear_v3d()
            
            try:
                ob = context.object
                delete_keyframes(context, ob, "location", 3)
                delete_keyframes(context, ob, "rotation_euler", 3)
                delete_keyframes(context, ob, "scale", 3)
                delete_keyframes(context, ob, "rigid_body.kinematic")
            except RuntimeError: # silent fail in case of no animation is present
                pass
            
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
            
            context.object.rigid_body.kinematic = False
            if (context.object.is_dynamic):
                bpy.ops.rigidbody.bake_to_keyframes('EXEC_DEFAULT', frame_start=1, frame_end=frame_end, step=1)
                          
            context.scene.frame_set(1)
           
            bpy.ops.rigidbody.objects_add(type='ACTIVE')
            #context.object.select = False
                 
            context.object.rigid_body.kinematic = True
            context.object.keyframe_insert(data_path="rigid_body.kinematic")
            
            
            context.scene.frame_set(frame_end)
            context.object.rigid_body.kinematic = False
            context.object.keyframe_insert(data_path="rigid_body.kinematic")
            
            context.scene.frame_set(1)
            
            #re-add fracture modifier
            bpy.ops.object.modifier_add(type='FRACTURE')
            #paths = bpy.utils.preset_paths("fracture")
            filepath = bpy.utils.preset_find("helperpreset", "fracture")
            for md in context.object.modifiers:
                if md.type == 'FRACTURE':
                    break
            ctx = context.copy()
            ctx["fracture"] = md
            bpy.ops.script.execute_preset(ctx, filepath=filepath, menu_idname="FRACTURE_MT_presets")
            bpy.context.object.modifiers["Fracture"].uv_layer = "InnerUV"
            bpy.ops.object.fracture_refresh()
            
            #Move FM to top position in modifier stack
            bpy.ops.object.move_fmtotop()   
            
            return {'FINISHED'}
        else:
            self.report({'WARNING'}, "Need an active object with fracture modifier!") 
            return {'CANCELLED'}
            
class ClusterHelperOperator(bpy.types.Operator):
    """Extracts the inner faces and uses this new mesh to generate smaller shards. These will be glued used clustergroups"""
    bl_idname = "object.create_cluster_helpers"
    bl_label = "Physical rough edges"

    def make_cluster_cores(self, context, oldact, lastact):
	    # now convert to objects and create empties at the locs
        tempOb = lastact #context.active_object
        print(tempOb)
        context.scene.objects.active = oldact
        for o in bpy.data.objects:
            o.select = False

        oldact.select = True
        bpy.ops.object.rigidbody_convert_to_objects()

        gr = bpy.data.groups["OB"+oldact.name+"_conv"]
        gh = bpy.data.groups.new("ClusterHelpers")
        context.scene.layers[18] = True
        par = bpy.data.objects.new("ClusterHelperParent", None)
        par.matrix_world = oldact.matrix_world.copy()
        context.scene.objects.link(par)
        par.layers[18] = True
        par.layers[0] = False
        for go in gr.objects:
            if go == tempOb:
                continue
            ob = bpy.data.objects.new("ClusterHelper", None)
            #ob.location = go.location.copy() - par.location
            ob.matrix_world = par.matrix_world.inverted() * go.matrix_world.copy()
            ob.parent = par
            context.scene.objects.link(ob)
            ob.layers[18] = True
            ob.layers[0] = False
            
            gh.objects.link(ob)
            gr.objects.unlink(go)
            context.scene.objects.unlink(go)
            bpy.data.objects.remove(go) 

        bpy.data.groups.remove(gr)
        
        #parenten des Clusterparent an basisobjekt
        par.matrix_world = oldact.matrix_world.inverted() * par.matrix_world.copy()
        par.parent = oldact
        
        #parenten der innerfaces an basisobjekt (klappt hier nicht aus irgendeinem
        #Grund, daher spaeter)
        #tempOb.matrix_world = oldact.matrix_world.inverted() * tempOb.matrix_world.copy()
        #tempOb.parent = oldact
        
        # Extrahiertes InnerObjekt / Basisobjekt selektieren
        print(tempOb)
        tempOb.select = True
        oldact.select = True
        
        return gh
        

    def extract_inner_faces(self, context, md):
        # first separate the inner faces as new object
        # execute fracture to be sure we have shard
        bpy.ops.object.fracture_refresh();
        
        for o in bpy.data.objects:
            o.select = False
            
        active = context.active_object
        active.select = True
        oldact = active
        
        #need to dupe object for applying it
        bpy.ops.object.duplicate()
    
        #context.active_object.select = True
        #bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        # execute fracture again to be sure we have shards
        bpy.ops.object.fracture_refresh(reset=True)
        
        # apply to get real mesh and edit it
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier=md.name)
        context.active_object.data.update(True, True)
        
        #remove all other modifiers except FM
        for mod in context.active_object.modifiers:
            bpy.ops.object.modifier_remove(modifier=mod.name)
        
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT')
        
        context.tool_settings.mesh_select_mode = (False, False, True)
        #i = 0
        for p in context.active_object.data.polygons:
            if p.material_index == 0:
               #print(i, p.material_index, "SELECTED")
               p.select = True
            else:
               #print(i, p.material_index, "DESELECTED")
               p.select = False
            #i += 1

        bpy.ops.object.mode_set(mode='EDIT')
        # delete all with outer material
        bpy.ops.mesh.delete(type='FACE')
        bpy.ops.object.mode_set(mode='OBJECT')

        context.active_object.name = context.active_object.name[:-4] + "_Inner"
        bpy.ops.rigidbody.objects_remove()

        lastact = context.active_object
        context.active_object.layers[18] = True
        context.active_object.layers[0] = False
        
        print("LAST:", lastact)
        
        # Extrahiertes InnerObjekt / Basisobjekt des InnerObjekt selektieren -> Zeile 755
        # FM: ClusterGroup: ClusterHelpers einsetzen -> Zeile 841 - 848
        # FM: Falls nicht schon geschehen Constraitns aktivieren und 
        #     voreinstellen: Angle 0.4 // ClusterAngel 1.0
        # fracture_helper() ausfuehren 
        
        return oldact, lastact
        
    
    def execute(self, context):
        act = context.active_object is not None
        mod = False
        
        for md in context.active_object.modifiers:
            if md.type == 'FRACTURE':
                mod = True
                break
                
        if not(act and mod):
            self.report({'WARNING'}, "Need an active object with fracture modifier") 
            return {'CANCELLED'}
        
        oldact, lastact = self.extract_inner_faces(context, md)
        gh = self.make_cluster_cores(context, oldact, lastact)
        
        # FM: ClusterGroup: ClusterHelpers einsetzen
        md.cluster_group = gh
        # FM: Falls nicht schon geschehen Constraitns aktivieren und 
        #     voreinstellen: Angle 0.4 // ClusterAngel 1.0
        md.breaking_angle = math.radians(2.0)
        md.cluster_breaking_angle = math.radians(0.1)
        md.use_constraints = True
        context.scene.objects.active = oldact
        # fracture_helper() ausfuehren 
        bpy.ops.object.fracture_helper(start=0, random=15.0)
        
        lastact.matrix_world = oldact.matrix_world.inverted() * lastact.matrix_world.copy()
        lastact.parent = oldact

        return {'FINISHED'}

def ensure_modifier(ob, type, name):
    md = find_modifier(ob, type)
    if md is None:
        md = ob.modifiers.new(type=type, name=name)
    return md

def ensure_uv(context, ob, name):
    
    #doesnt work, sadly...
    #uv = ob.data.uv_layers.new(name="InnerUV")
    uv = None
    context.scene.objects.active = ob
    #InnerUV should be the 2nd one, 
    # maybe we want to have an outer UV too, so add anyway
    
    for u in ob.data.uv_layers:
        if u.name == name:
            uv = u
            break
        
    if uv is None:
        bpy.ops.mesh.uv_texture_add()
        uv = ob.data.uv_layers.active
        uv.name = name
    
    return uv

def ensure_texture(ob):
    name = ob.name +  "_Displacement" 
    try:
        tex = bpy.data.textures[name]
    except KeyError:
        tex = bpy.data.textures.new(type='CLOUDS', name=name)
    
    return tex

### Rough edges using displacement modifier:
class DisplacementEdgesOperator(bpy.types.Operator):
    """Setups the modifier stack for simulated (not real) rough edges"""
    bl_idname = "object.create_displaced_edges"
    bl_label = "Simulated rough edges"
    
    def execute(self, context):
        
        for ob in context.selected_objects:
            if ob.type != 'MESH':
                continue
            
            fmd = ensure_modifier(ob, 'FRACTURE', "Fracture")
            smd = ensure_modifier(ob, 'SUBSURF', "Subsurf")
            dmd = ensure_modifier(ob, 'DISPLACE', "Displace")
            emd = ensure_modifier(ob, 'EDGE_SPLIT', "EdgeSplit")
             
            bpy.ops.object.shade_smooth()
            uv = ensure_uv(context, ob, "InnerUV")
            tex = ensure_texture(ob)
             
            fmd.use_smooth = True
            fmd.uv_layer = uv.name
            fmd.autohide_dist = 0.0001
            
            smd.subdivision_type = 'SIMPLE'
            smd.levels = 2
            
            dmd.texture_coords = 'UV'
            dmd.uv_layer = uv.name
            dmd.strength = 0.5
            dmd.texture = tex
            
            emd.split_angle = math.radians(45)
            
            
            bpy.ops.object.fracture_refresh(modifier="Fracture", reset=True)

        return {'FINISHED'}

class CombineSubObjectsOperator(bpy.types.Operator):
    """Combine multiple Fractured objects into one object"""
    bl_idname = "object.combine_subobjects"
    bl_label = "Combine Sub Objects"
    
    def execute(self, context):
        #prepare objects
        context.scene.layers[17] = True
        gr = bpy.data.groups.new("CombinationGroup")
        for ob in context.selected_objects:

             gr.objects.link(ob)
             context.scene.objects.active = ob
             for md in ob.modifiers:
                if (md.type == 'FRACTURE'):
                   bpy.ops.object.fracture_refresh(reset=True)
                   
                   #stop simulation and interaction
                   ob.rigid_body.kinematic = True
                   ob.rigid_body.is_ghost = True
                   break
                elif ob.rigid_body != None:
                   #stop simulation and interaction (regular rigidbodies)
                   ob.rigid_body.kinematic = True
                   ob.rigid_body.is_ghost = True
                   
             ob.layers[17] = True
             for x in range(0, 19):
                if x != 17:
                    ob.layers[x] = False
        
        #context.scene.update()
        context.scene.layers[17] = False
        
        if len(gr.objects) == 0:
            self.report({'WARNING'}, "Found no selected object with a fracture modifier") 
            return {'CANCELLED'}
                 
        #create carrier object at 0, 0, 0 -> transformations are taken into account
        bpy.ops.mesh.primitive_cube_add()
        active = context.active_object
        active.layers[0] = True
        active.layers[17] = False
        
        bpy.ops.object.modifier_add(type='FRACTURE')
        md = active.modifiers[0]
        md.point_source = set()
        md.dm_group = gr
        bpy.ops.object.fracture_refresh(reset=True)
        
        return {'FINISHED'}

#### HIR FUER INNER VERTEX NEUE DEFINITION HINZUFUEGEN ##### -> ouch, my umlauts... lol
def find_modifier(ob, typ):
    for md in ob.modifiers:
        if md.type == typ:
            return md
    return None
    
def find_inner_uv(ob):
    for uv in ob.data.uv_textures:
        if uv.name == "InnerUV":
            return uv
    return None



class SmokeSetupOperator(bpy.types.Operator):
    """Setup smoke on inner faces"""
    bl_idname = "object.setup_smoke"
    bl_label = "Inner Smoke"
    
    def execute(self, context):
        allobs = bpy.data.objects
        flows = [] #context.selected_objects
        #flows.append(context.active_object)
        fr = context.scene.frame_current
        
        #check whether smoke is already set up, if yes.. only set keyframes
        #check for selected objects...
        for ob in context.selected_objects:
            md = find_modifier(ob, 'SMOKE')
            if md is None or (md is not None and md.smoke_type not in {'FLOW', 'DOMAIN'}):
                flows.append(ob)
            elif md.smoke_type == 'FLOW':
                set_smoke_keyframes(self, context, ob, fr)
        
        #and for active object (not really sure whether this step here is necessary,
        #shouldnt active ob be in selected objs too ?        
        if context.active_object is not None:        
            md = find_modifier(context.active_object, 'SMOKE')
            if md is None or (md is not None and md.smoke_type not in {'FLOW', 'DOMAIN'}):
                flows.append(context.active_object)
            elif md.smoke_type == 'FLOW':
                set_smoke_keyframes(self, context, context.active_object, fr)
        
        if len(flows) == 0:
            return {'FINISHED'}    
        
        #setup inner uv and FM, if not present - also remove Smoke_Collision
        for ob in flows:
            was_none = False
                      
            bpy.ops.object.modifier_remove(modifier="Smoke_Collision")
            
            md = find_modifier(ob, 'FRACTURE')
            if md is None:
                was_none = True
                md = ob.modifiers.new(name="Fracture", type='FRACTURE')
            
            uv = find_inner_uv(ob)
            if uv is None:
                uv = ob.data.uv_textures.new(name="InnerUV")
            
            #only do necessary setup here
            md.uv_layer = uv.name
            md.autohide_dist = 0.0001
            
            if was_none:    
                #some weak constraints so it doesnt fall apart to early,
                #showing the smoke
                md.use_constraints = True
                md.contact_dist = 2.0
                md.constraint_limit = 10
                md.breaking_angle = math.radians(0.5)
            
            context.scene.objects.active = ob
            bpy.ops.object.fracture_refresh(reset=True)
        
        #setup quick smoke
        bpy.ops.object.quick_smoke()
        
        #setup a blend texture (works best with inner smoke)
        tex = bpy.data.textures.new("SmokeTex", 'BLEND')
        
        #flow settings
        for ob in flows:
            md = find_modifier(ob, 'SMOKE')
            if md.smoke_type == 'FLOW':
                flow = md.flow_settings
                flow.use_texture = True
                flow.noise_texture = tex
                flow.texture_map_type = 'UV'
                flow.uv_layer = "InnerUV"
                flow.surface_distance = 0.20
                flow.density = 0.63
                flow.subframes = 2
                flow.use_initial_velocity = True
                flow.velocity_factor = 1
                flow.velocity_normal = 1
                ob.draw_type = 'TEXTURED'
                set_smoke_keyframes(self, context, ob, fr)
                
                #first two materials (should be regular and inner one)
                if context.scene.render.engine == 'BLENDER_RENDER':
                    outer = ob.material_slots[0].material
                    outer.use_transparent_shadows = True
                    inner = ob.material_slots[1].material
                    inner.use_transparent_shadows = True
                    
        #domain settings
        domainOb = context.active_object
        md = find_modifier(domainOb, 'SMOKE')
        if md.smoke_type == 'DOMAIN':
            domain = md.domain_settings
            domain.alpha = 0.097
            domain.beta = -0.147
            domain.vorticity = 1.57
            domain.use_dissolve_smoke = True
            domain.dissolve_speed = 21
            domain.use_dissolve_smoke_log = True
            domain.use_adaptive_domain = True
            domain.use_high_resolution = True
            domain.amplify = 1
            
            world = context.scene.rigidbody_world
            domain.point_cache.frame_start = world.point_cache.frame_start
            domain.point_cache.frame_end = world.point_cache.frame_end
        
        #domain render / material settings (BI)
        mat = domainOb.material_slots[0].material
        
        if context.scene.render.engine == 'BLENDER_RENDER':
            volume = mat.volume
            volume.density_scale = 3
            volume.use_light_cache = True
            volume.cache_resolution = 50
            volume.step_size = 0.03
        
        #Alle Szenenobjekte zu Collidern machen (Smoke/Particle) (inkl FM TO TOP OPERATOR)
        #bpy.ops.object.setup_collision() 
        
        #FractureModifier auf erste Position schieben
        bpy.ops.object.move_fmtotop()  
        
        #Auf Frame 1 springen
        bpy.context.scene.frame_current = 1
        
        return {'FINISHED'}



class DustSetupOperator(bpy.types.Operator):
    """Setup dust on inner faces"""
    bl_idname = "object.setup_dust"
    bl_label = "Dust"
    
    def make_dust_objects_group(self, context, ob):
        actname = bpy.context.scene.objects.active.name
        dust_count = 1
        loc = ob.location.copy()
        x = 0.0
        gr = bpy.data.groups.new(actname + "_DustObjects")
        
        context.scene.layers[17] = True
        bpy.ops.object.empty_add(type='CIRCLE', view_align=False, location=loc.to_tuple())
        bpy.context.scene.objects.active.name = actname + "_DustObjects"
        bpy.context.object.show_name = True
        bpy.context.object.show_x_ray = True
        par = bpy.context.active_object
        
        for i in range(dust_count):
            #zufaellige grösse (0 bis 1) und 
            #verschiebung um die doppelte grösse in X richtung (nur für die Optik)
            size = random.random() * 0.5 + 0.5
            x += 1.5 * size
            context.scene.layers[17] = True
            bpy.ops.mesh.primitive_ico_sphere_add(size=size, location=(loc[0] + x, loc[1], loc[2]))
            
            #for ob in bpy.context.selected_objects:
            #    ob.name = actname + "_DebrisObject"
            context.active_object.name = actname + "_DustObject"
                
            #im objektmode in gruppe einfuegen  
            #bpy.ops.object.editmode_toggle()
            gr.objects.link(context.active_object)
            
            ob = context.active_object
            #adjust transformation and parent
            ob.matrix_world = par.matrix_world.inverted() * ob.matrix_world
            ob.parent = par
            #bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)
                        
            #Layer umschalten
            context.scene.layers[0] = True
            #context.scene.layers[17] = False
            
        return gr
    
    def execute(self, context):
        selected = context.selected_objects
        allobs = bpy.data.objects
        #selected.append(context.active_object)
        act = context.active_object
        psys_name = "DUST_PSystem"
  
          
        if bpy.data.objects.get("Smoke Domain") is None:
          self.report({'WARNING'}, "Dust needs a smoke domain with the name 'Smoke Domain' !") 
          return {'CANCELLED'}
  
        #setup inner vertex group and FM, if not present
        for ob in selected:
            
            was_none = False
            vertgroup = None
            partsys = None
            gr = None
            
            md = find_modifier(ob, 'FRACTURE')
            if md is None:
                was_none = True
                md = ob.modifiers.new(name="Fracture", type='FRACTURE')

            for vg in ob.vertex_groups:
                if vg.name == "INNER_vertex":
                    vertgroup = vg
                    
            if vertgroup is None:
                vertgroup = ob.vertex_groups.new(name="INNER_vertex")
                
            md.inner_vertex_group = vertgroup.name            

            # Abfrage ob PartikelSystem "ParticleDUST" schon exestiert.
            for psystem in ob.particle_systems:
                if psystem.name == psys_name:
                    partsys = psystem
                    # Wenn ja, StartFrame syncronisieren (einlesen bzw aktualisieren).
                    # ist das setzen von Start / End frame mit "synchronisieren" gemeint ?
                    # partsys.settings.frame_start = context.object.smokedebrisdust_emission_start
                    # partsys.settings.frame_end = context.object.smokedebrisdust_emission_start + 10
                    partsys.settings.frame_start = context.scene.frame_current
                    partsys.settings.frame_end = context.scene.frame_current + 10
            
            print(partsys, len(ob.particle_systems))        
            if partsys is None:
                # Wenn nein
                # Operator arbeitet auf dem aktiven Objekt (meistens), daher setze aktuelles ob
                # als aktives objekt und stelle das alte aktive objekt hinterher wieder her
                context.scene.objects.active = ob
                bpy.ops.object.particle_system_add()
                bpy.context.object.modifiers[-1].name = "Dust_ParticleSystem"
                
                gr = self.make_dust_objects_group(context, ob)

                #finde zuletzt hinzugefuegtes partikelsystem
                #particlesystems = [md for md in context.object.modifiers if md.type == "PARTICLE_SYSTEM"]
                psys = ob.particle_systems[-1]
                
                #make particle system settings here....
                #pdata = bpy.data.particles[-1]
                pdata = psys.settings
                psys.name = psys_name;
                pdata.name = "DUST_Settings"
                pdata.count = 2500
                
                #pdata.frame_start = context.object.smokedebrisdust_emission_start
                #pdata.frame_end = context.object.smokedebrisdust_emission_start + 10
                pdata.frame_start = context.scene.frame_current
                pdata.frame_end = context.scene.frame_current + 17
                pdata.lifetime = 75
                pdata.lifetime_random = 0.60
                pdata.factor_random = 0.85
                pdata.normal_factor = 0
                pdata.tangent_phase = 0.5
                pdata.subframes = 5
                pdata.use_rotations = False
                pdata.rotation_factor_random = 0.5
                pdata.phase_factor_random = 0.5
                pdata.angular_velocity_mode = 'VELOCITY'
                pdata.angular_velocity_factor = 1
                pdata.use_dynamic_rotation = True
                pdata.particle_size = 0.008
                pdata.size_random = 0.6
                pdata.brownian_factor = 3
                pdata.use_multiply_size_mass = False
                pdata.effector_weights.gravity = 1.0
                pdata.draw_method = 'RENDER'
                pdata.use_render_emitter = True
                pdata.render_type = 'GROUP'
                pdata.use_group_pick_random = True
                pdata.dupli_group = gr
                pdata.use_modifier_stack = True
                pdata.effector_weights.gravity = 0
                psys.vertex_group_density = "INNER_vertex"
       
            #only do necessary setup here
            md.autohide_dist = 0.0001
            context.scene.objects.active = ob
            bpy.ops.object.fracture_refresh(reset=True)
            
            #erst jetzt ist definitiv ein inner material da... setze es auf allen Objekten
            #der debris group
            tmp_act = ob 
            if gr is not None:
                for obj in gr.objects:
                    context.scene.objects.active = obj
                    bpy.ops.object.material_slot_add()
                    obj.material_slots[0].material = md.inner_material
                context.scene.objects.active = tmp_act
                    
            
            #Collision auf aktuellem Objekt hinzufuegen
            #ob.modifiers.new(name="Dust_Collision", type='COLLISION')
            #ob.collision.damping_factor = 0.7
            #ob.collision.friction_factor = 0.5
            #ob.collision.friction_random = 0.5
        
        #Domain mit Force Field "Smoke Flow"
        bpy.context.scene.objects.active = bpy.data.objects["Smoke Domain"]
        bpy.ops.object.forcefield_toggle()
        bpy.context.object.field.type = 'SMOKE_FLOW'
        bpy.context.object.field.shape = 'SURFACE'
        bpy.context.object.field.source_object = bpy.data.objects["Smoke Domain"]
        bpy.context.object.field.strength = 1
        bpy.context.object.field.flow = 1
               
        #restore active object
        context.scene.objects.active = act
        
        #RB Field Weights für "Smoke Flow" auf 0 setzen!
        bpy.context.scene.rigidbody_world.effector_weights.smokeflow = 0

        #Alle Szenenobjekte zu Collidern machen (Smoke/Particle) (inkl FM TO TOP OPERATOR)
        #bpy.ops.object.setup_collision()  
        
        #FractureModifier auf erste Position schieben
        bpy.ops.object.move_fmtotop()  
        
        context.scene.frame_current = 1
        
        return {'FINISHED'} 

class DebrisSetupOperator(bpy.types.Operator):
    """Setup debris on inner faces"""
    bl_idname = "object.setup_debris"
    bl_label = "Debris"
    
    def make_debris_objects_group(self, context, ob):
        actname = bpy.context.scene.objects.active.name
        debris_count = 3
        loc = ob.location.copy()
        x = 0.0
        gr = bpy.data.groups.new(actname + "_DebrisObjects")
        
        context.scene.layers[17] = True
        bpy.ops.object.empty_add(type='CIRCLE', view_align=False, location=loc.to_tuple())
        bpy.context.scene.objects.active.name = actname + "_DebrisObjects"
        bpy.context.object.show_name = True
        bpy.context.object.show_x_ray = True
        par = bpy.context.active_object
        
        for i in range(debris_count):
            #zufaellige grösse (0 bis 1) und 
            #verschiebung um die doppelte grösse in X richtung (nur für die Optik)
            size = random.random() * 0.5 + 0.5
            x += 3 * size
            context.scene.layers[17] = True
            bpy.ops.mesh.primitive_ico_sphere_add(size=size, location=(loc[0] + x, loc[1], loc[2]), subdivisions=1)
            
            #for ob in bpy.context.selected_objects:
            #    ob.name = actname + "_DebrisObject"
            context.active_object.name = actname + "_DebrisObject"
                
            #im editmode fraktal unterteilen (2x) -> sieht (normalerweise) besser aus als 1x mit 2 cuts
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.subdivide(number_cuts=1, fractal=size*2.5, seed=random.randint(0,10))
            bpy.ops.mesh.subdivide(number_cuts=1, fractal=size*2.5, seed=random.randint(0,10))    
            #im objektmode in gruppe einfuegen  
            bpy.ops.object.editmode_toggle()
            gr.objects.link(context.active_object)
            
            ob = context.active_object
            #adjust transformation and parent
            ob.matrix_world = par.matrix_world.inverted() * ob.matrix_world
            ob.parent = par
            #bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)
                        
            #Layer umschalten
            context.scene.layers[0] = True
            #context.scene.layers[17] = False
            
        return gr
    
    def execute(self, context):
        selected = context.selected_objects
        allobs = bpy.data.objects
        #selected.append(context.active_object)
        act = context.active_object
        psys_name = "DEBRIS_PSystem"
  
        #setup inner vertex group and FM, if not present
        for ob in selected:
            
            was_none = False
            vertgroup = None
            partsys = None
            gr = None
            
            md = find_modifier(ob, 'FRACTURE')
            if md is None:
                was_none = True
                md = ob.modifiers.new(name="Fracture", type='FRACTURE')

            for vg in ob.vertex_groups:
                if vg.name == "INNER_vertex":
                    vertgroup = vg
                    
            if vertgroup is None:
                vertgroup = ob.vertex_groups.new(name="INNER_vertex")
                
            md.inner_vertex_group = vertgroup.name            

            # Abfrage ob PartikelSystem "ParticleDEBRIS" schon exestiert.
            for psystem in ob.particle_systems:
                if psystem.name == psys_name:
                    partsys = psystem
                    # Wenn ja, StartFrame syncronisieren (einlesen bzw aktualisieren).
                    # ist das setzen von Start / End frame mit "synchronisieren" gemeint ?
                    # partsys.settings.frame_start = context.object.smokedebrisdust_emission_start
                    # partsys.settings.frame_end = context.object.smokedebrisdust_emission_start + 10
                    partsys.settings.frame_start = context.scene.frame_current
                    partsys.settings.frame_end = context.scene.frame_current + 10
            
            print(partsys, len(ob.particle_systems))        
            if partsys is None:
                # Wenn nein
                # Operator arbeitet auf dem aktiven Objekt (meistens), daher setze aktuelles ob
                # als aktives objekt und stelle das alte aktive objekt hinterher wieder her
                context.scene.objects.active = ob
                bpy.ops.object.particle_system_add()
                bpy.context.object.modifiers[-1].name = "Debris_ParticleSystem"
                
                gr = self.make_debris_objects_group(context, ob)

                #finde zuletzt hinzugefuegtes partikelsystem
                #particlesystems = [md for md in context.object.modifiers if md.type == "PARTICLE_SYSTEM"]
                psys = ob.particle_systems[-1]
                
                #make particle system settings here....
                #pdata = bpy.data.particles[-1]
                pdata = psys.settings
                psys.name = psys_name;
                pdata.name = "DEBRIS_Settings"
                pdata.count = 250
                
                #pdata.frame_start = context.object.smokedebrisdust_emission_start
                #pdata.frame_end = context.object.smokedebrisdust_emission_start + 10
                pdata.frame_start = context.scene.frame_current
                pdata.frame_end = context.scene.frame_current + 10
                pdata.lifetime = context.scene.frame_end
                pdata.factor_random = 0.95
                pdata.normal_factor = 0
                pdata.tangent_phase = 0.1
                pdata.use_rotations = True
                pdata.rotation_factor_random = 0.5
                pdata.phase_factor_random = 0.5
                pdata.angular_velocity_mode = 'VELOCITY'
                pdata.angular_velocity_factor = 1
                pdata.use_dynamic_rotation = True
                pdata.particle_size = 0.135
                pdata.size_random = 0.81
                pdata.use_multiply_size_mass = True
                pdata.effector_weights.gravity = 1.0
                pdata.effector_weights.smokeflow = 0
                pdata.draw_method = 'RENDER'
                pdata.use_render_emitter = True
                pdata.render_type = 'GROUP'
                pdata.use_group_pick_random = True
                pdata.dupli_group = gr
                pdata.use_modifier_stack = True
                psys.vertex_group_density = "INNER_vertex"
       
            #only do necessary setup here
            md.autohide_dist = 0.0001
            context.scene.objects.active = ob
            bpy.ops.object.fracture_refresh(reset=True)
            
            #erst jetzt ist definitiv ein inner material da... setze es auf allen Objekten
            #der debris group
            tmp_act = ob 
            if gr is not None:
                for obj in gr.objects:
                    context.scene.objects.active = obj
                    bpy.ops.object.material_slot_add()
                    obj.material_slots[0].material = md.inner_material
                context.scene.objects.active = tmp_act
                    
            
            #Collision auf aktuellem Objekt hinzufuegen
            #ob.modifiers.new(name="Debris_Collision", type='COLLISION')
            #ob.collision.damping_factor = 0.7
            #ob.collision.friction_factor = 0.5
            #ob.collision.friction_random = 0.5
        
        #restore active object
        context.scene.objects.active = act
        
        #Alle Szenenobjekte zu Collidern machen (Smoke/Particle) (inkl FM TO TOP OPERATOR)
        #bpy.ops.object.setup_collision()  
        
        #FractureModifier auf erste Position schieben
        bpy.ops.object.move_fmtotop()  
        
        context.scene.frame_current = 1
        
        return {'FINISHED'} 
        
#FractureModifier auf erste Position schieben
class MoveFMToTopOperator(bpy.types.Operator):
    """Moves the Fracture Modifier on top position in stack"""
    bl_idname = "object.move_fmtotop"
    bl_label = "Move FM to stack s top"
    
    def execute(self, context):
        md = find_modifier(context.object, 'FRACTURE')
        #solange der Modifier nicht der erste ist, bewege hoch...
        while md != context.object.modifiers[0] and md is not None:
            bpy.ops.object.modifier_move_up(modifier="Fracture")
        return {'FINISHED'}

def delete_keyframes(context, ob, path, index=1):
    if ob.animation_data and ob.animation_data.action:
        fc = ob.animation_data.action.fcurves
        for i in range(index):
            f = fc.find(data_path=path, index=i)
            if f:
                fc.remove(f) 
    
def set_smoke_keyframes(self, context, ob, fr):
    #Vom aktellen Frame ausgehend:
    #Smoke Flow Source -> Keyframe auf Surface: 0.14
    #In der Zeitleiste 3 Frames ZURÜCK gehen, Keyframe auf Surface: 0.00
    #In der Zeitleiste 13 Frames VORWÄRTS gehen, Keyframe auf Surface: 0.00
    #ob = context.object
    md = ob.modifiers["Smoke"]
    #print(md)
    if md.type == 'SMOKE' and md.smoke_type == 'FLOW':
        # Warning, this deletes ALL keyframes on this object, no easy way to only delete all 
        # keyframes on a specific property (without memorizing the frame numbers)
        ob.select = True
        #bpy.ops.anim.keyframe_clear_v3d()
        try:
            #why on earth do we need to jump to all keyframes in this case ?! transformation
            #keyframes can be deleted in 1 go 
            delete_keyframes(context, ob, "modifiers[\"Smoke\"].flow_settings.surface_distance")
        except RuntimeError:
            pass
        
        #fr = context.scene.frame_current
        md.flow_settings.surface_distance = 0.1
        ob.keyframe_insert(data_path="modifiers[\"Smoke\"].flow_settings.surface_distance")
        
        context.scene.frame_current -= 3
        md.flow_settings.surface_distance = 0.0
        ob.keyframe_insert(data_path="modifiers[\"Smoke\"].flow_settings.surface_distance")
        
        context.scene.frame_current += 28
        ob.keyframe_insert(data_path="modifiers[\"Smoke\"].flow_settings.surface_distance")
        
        context.scene.frame_current = fr
        
                
# Per click das das aktuelle Frame als emission_start setzen
class GetFrameOperator(bpy.types.Operator):
    """Looks for the actual frame"""
    bl_idname = "object.get_frame"
    bl_label = "Start all emissions now"   
    
    
    def execute(self, context):
        ob = context.object
        psys_name = "DEBRIS_PSystem"
        try:
            psys = ob.particle_systems[psys_name]
            pdata = psys.settings
            pdata.frame_start = context.scene.frame_current
            pdata.frame_end = context.scene.frame_current + 10
        
        except KeyError:
            self.report({'WARNING'}, "No debris particle system found, skipping")
        
        try:
            fr = context.scene.frame_current    
            set_smoke_keyframes(self, context, ob, fr)
        except KeyError:
            self.report({'WARNING'}, "No smoke modifier (flow) found, skipping")
        
        #Move FM to top position in modifier stack
        bpy.ops.object.move_fmtotop()   
        
        context.scene.frame_current = 1
        
        return {'FINISHED'} 
    
# Per click allen Objekten einen Collision-Modifier hinzufuegen, falls nicht vorhanden
# Gilt fuer Collision- und SmokeModifier

### DomainObjekt muss davon ausgeschlossen werden!
### Und: Als Idee sollen Objekte die "_nsc" am Ende ihres Namen stehen haben NICHT zum SMOKE-COLLIDER
###      gemacht werden (nsc=no smoke collisions) bis irgendwann mal dieser SmokeBug von den DEVs
###      gefixt wird ;)

class CollisionSetupOperator(bpy.types.Operator):
    """Setup collision for selected objects"""
    bl_idname = "object.setup_collision"
    bl_label = "Collision on selected objects"
    
    def execute(self, context):
        selected = context.selected_objects
        allobs = bpy.data.objects
        #selected.append(context.active_object)
        act = context.active_object
               
        for act in selected:
        
           if act.type != 'MESH':
               continue
           
           md = find_modifier(act, 'COLLISION')
           md2 = find_modifier(act, 'SMOKE')
           if md2 is not None and md2.smoke_type == 'DOMAIN':
               continue
               
           if md is None:
                #was_none = True
                act.modifiers.new(name="Debris_Collision", type='COLLISION')
                act.collision.damping_factor = 0.8
                act.collision.friction_factor = 0.4
                act.collision.friction_random = 0.3   
                               
                #Ueberpruefen ob ein Smoke_Collisions vorhanden sind und ggf hinzufuegen (alle Objekte)
           #md = find_modifier(ob, 'SMOKE')
           
           #Wegen instabilitÃ¤t der SmokeSim erstmal heraus genommen 22.03.2016
           #if md2 is None:
                
                #md2 = ob.modifiers.new(name="Smoke_Collision", type='SMOKE')
           
           # nur wenn keine Domain und nicht auf _nsc endet, mache den Smokemod zu Collision 
           # (aber was ist mit existierenden Flows ? werden die ueber nsc ausgeschlossen ?
           #if md2.smoke_type not in {'DOMAIN', 'FLOW'} and not ob.name.endswith("_nsc"):     
                #md2.smoke_type = 'COLLISION'
        
        #FractureModifier auf erste Position schieben
        bpy.ops.object.move_fmtotop()            
        
        return {'FINISHED'} 
        
        

class SmokeDebrisDustSetupPanel(bpy.types.Panel):
    bl_label = "Smoke / Dust / Debris"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Fracture"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        if not context.object:
            self.layout.label("Please select atleast one object first")
        else:
            layout = self.layout
            col = layout.column(align=True)
            row = col.row(align=True)
            
            row.operator("object.setup_smoke", icon='MOD_SMOKE')
            row.operator("object.setup_dust", icon='STICKY_UVS_VERT')
            row.operator("object.setup_debris", icon='STICKY_UVS_DISABLE')
            
            col.operator("object.get_frame", icon='TIME')
            col.operator("object.setup_collision", icon='MOD_PHYSICS')
                   

class ExecuteFractureOperator(bpy.types.Operator):
    """Adds FM when needed and (re)fractures..."""
    bl_idname = "object.fracture"
    bl_label = "Execute Fracture"
    
    def execute(self, context):
        
        for ob in context.selected_objects:
            if ob.type != 'MESH':
                continue
                   
            md = find_modifier(ob, 'FRACTURE')
            if md is None:
                md = ob.modifiers.new(type='FRACTURE', name="Fracture")
           
            #Apply Scale muss interessanter Weise vorher ausgefuehrt werden?
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            context.scene.objects.active = ob
            bpy.ops.object.fracture_refresh(reset=True)
            #PhyiscsTab aktivieren ... aber WIE?
            #bpy.data.screens = 'PHYSICS'
        
        
        return {'FINISHED'} 
        


def register():
    
    bpy.utils.register_class(MainOperationsPanel)
    bpy.utils.register_class(VIEW3D_SettingsPanel)
    bpy.utils.register_class(FractureHelper)
    bpy.utils.register_class(FractureHelperPanel)
    bpy.utils.register_class(TimingPanel)
    bpy.utils.register_class(FracturePathPanel)
    bpy.utils.register_class(FractureFrameOperator)
    bpy.utils.register_class(ClusterHelperOperator)
    bpy.utils.register_class(DisplacementEdgesOperator)
    bpy.utils.register_class(CombineSubObjectsOperator)
    bpy.utils.register_class(ViewOperatorFracture)
    bpy.utils.register_class(SmokeSetupOperator)
    bpy.utils.register_class(DustSetupOperator)
    bpy.utils.register_class(DebrisSetupOperator)    
    bpy.utils.register_class(SmokeDebrisDustSetupPanel)
    bpy.utils.register_class(GetFrameOperator)
    bpy.utils.register_class(CollisionSetupOperator)
    bpy.utils.register_class(MoveFMToTopOperator)
    bpy.utils.register_class(ExecuteFractureOperator)
    
    bpy.types.Object.use_animation_curve = bpy.props.BoolProperty(name="use_animation_curve", default=False)
    bpy.types.Object.animation_obj = bpy.props.StringProperty(name="animation_obj", default = "")
    bpy.types.Object.animation_ghost = bpy.props.BoolProperty(name="animation_ghost", default = False)
    #bpy.types.Object.use_wire = bpy.props.BoolProperty(name="use_wire", default=False, update=update_wire)
    #bpy.types.Object.use_relationship_lines = bpy.props.BoolProperty(name="use_relation", default=True, update=update_relationships)
    #bpy.types.Object.use_visible_particles = bpy.props.BoolProperty(name="use_visible_particles", default=True, update=update_visible_particles)
    #bpy.types.Object.particle_amount = bpy.props.IntProperty(name="particle_amount", default=100, update=update_particle_amount)
    #bpy.types.Object.particle_random = bpy.props.FloatProperty(name="particle_random", default=1.5, update=update_particle_random)
    bpy.types.Object.fracture_frame = bpy.props.IntProperty(name="fracture_frame", default=1)
    bpy.types.Object.global_smoke_start = bpy.props.BoolProperty(name="global_smoke_start", default=False)    
    bpy.types.Object.is_dynamic = bpy.props.BoolProperty(name="is_dynamic", default=True)
    bpy.types.Object.mouse_mode = bpy.props.EnumProperty(name="mouse_mode", items=[("Uniform", "Uniform", "Uniform", 'MESH_CUBE', 0), \
                                                                                   ("Radial", "Radial", "Radial", 'MESH_UVSPHERE', 1)])
                                                                                   
    bpy.types.Object.mouse_object = bpy.props.EnumProperty(name="mouse_object", items=[("Cube", "Cube", "Cube", 'MESH_CUBE', 0), \
                                                                                         ("Sphere", "Sphere", "Sphere", 'MESH_UVSPHERE', 1), \
                                                                                         ("Custom", "Custom", "Custom", 'MESH_MONKEY', 2) ], default="Sphere")
    bpy.types.Object.mouse_custom_object = bpy.props.StringProperty(name="mouse_custom_object", default="")
    bpy.types.Object.mouse_count = bpy.props.IntProperty(name="mouse_count", default=50)
    bpy.types.Object.mouse_segments = bpy.props.IntProperty(name="mouse_segments", default=8, min=1, max=100)
    bpy.types.Object.mouse_rings = bpy.props.IntProperty(name="mouse_segments", default=8, min=1, max=100)
    bpy.types.Object.mouse_status = bpy.props.StringProperty(name="mouse_status", default="Start mouse based fracture")
    bpy.types.Object.delete_helpers = bpy.props.BoolProperty(name="delete_helpers", default=False)
    #bpy.types.Object.use_autoexecute = bpy.props.BoolProperty(name="use_autoexecute", default=False, update=update_autoexecute)
    
def unregister():
    bpy.utils.unregister_class(MainOperationsPanel)
    bpy.utils.unregister_class(VIEW3D_SettingsPanel)
    bpy.utils.unregister_class(CombineSubObjectsOperator)
    bpy.utils.unregister_class(FractureFrameOperator)
    bpy.utils.unregister_class(TimingPanel)
    bpy.utils.unregister_class(FracturePathPanel)
    bpy.utils.unregister_class(FractureHelperPanel)
    bpy.utils.unregister_class(FractureHelper)
    bpy.utils.unregister_class(ClusterHelperOperator)
    bpy.utils.unregister_class(DisplacementEdgesOperator)
    bpy.utils.unregister_class(ViewOperatorFracture)
    bpy.utils.unregister_class(SmokeSetupOperator)
    bpy.utils.unregister_class(DustSetupOperator)
    bpy.utils.unregister_class(DebrisSetupOperator)
    bpy.utils.unregister_class(SmokeDebrisDustSetupPanel)
    bpy.utils.unregister_class(GetFrameOperator)
    bpy.utils.unregister_class(CollisionSetupOperator)
    bpy.utils.unregister_class(MoveFMToTopOperator)
    bpy.utils.unregister_class(ExecuteFractureOperator)
    
       
    del bpy.types.Object.use_animation_curve
    del bpy.types.Object.animation_obj
    del bpy.types.Object.animation_ghost
    #del bpy.types.Object.use_wire
    #del bpy.types.Object.use_relationship_lines
    #del bpy.types.Object.use_visible_particles
    #del bpy.types.Object.particle_amount
    #del bpy.types.Object.particle_random
    del bpy.types.Object.fracture_frame
    del bpy.types.Object.is_dynamic
    del bpy.types.Object.mouse_object
    del bpy.types.Object.mouse_count
    del bpy.types.Object.mouse_status
    del bpy.types.Object.delete_helpers
    del bpy.types.Object.global_smoke_start


if __name__ == "__main__":
    register()
