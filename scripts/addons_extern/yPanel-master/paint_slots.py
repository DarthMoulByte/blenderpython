import bpy, os
import tempfile
from bpy.props import *
from mathutils import *
from bpy_extras.io_utils import ImportHelper
from bpy_extras.image_utils import load_image  
from bpy.app.handlers import persistent
from .common import *

# BUG: Cannot delete mumei jacket spec node paint slot V
# BUG: Duplicate normal paint slot not copy normal map sampling V

influence_names = {
        'diffuse' : 'Diffuse Intensity',
        'color_diffuse' : 'Diffuse Color',
        'alpha' : 'Alpha',
        'translucency' : 'Translucency',

        'specular' : 'Specular Intensity',
        'color_spec' : 'Specular Color',
        'hardness' : 'Specular Hardness',

        'ambient' : 'Ambient',
        'emit' : 'Emit',
        'mirror' : 'Mirror Color',
        'raymir' : 'Ray Mirror',

        'normal' : 'Normal',
        'warp' : 'Warp',
        'displacement' : 'Displacement'
        }

influence_factor = {
        'diffuse' : 'diffuse_factor',
        'color_diffuse' : 'diffuse_color_factor',
        'alpha' : 'alpha_factor',
        'translucency' : 'translucency_factor',

        'specular' :'specular_factor',
        'color_spec' : 'specular_color_factor',
        'hardness' : 'hardness_factor',

        'ambient' : 'ambient_factor',
        'emit' : 'emit_factor',
        'mirror' : 'mirror_factor',
        'raymir' : 'raymir_factor',

        'normal' : 'normal_factor',
        'warp' : 'warp_factor',
        'displacement' : 'displacement_factor'
}

posfix_dict = {
        'diffuse' : '_DI',
        'color_diffuse' : '_D',
        'alpha' : '_A',
        'translucency' : '_T',

        'specular' : '_SI',
        'color_spec' : '_S',
        'hardness' : '_H',

        'ambient' : '_Ambient',
        'emit' : '_E',
        'mirror' : '_M',
        'raymir' : '_R',

        'normal' : '_N',
        'warp' : '_W',
        'displacement' : '_D',

        'bump' : '_B',
        }

influence_items = (
                 ('color_diffuse', 'Diffuse Color', ''),
                 ('color_spec', 'Specular Color', ''),
                 ('normal', 'Normal', ''),
                 ('bump', 'Bump', ''), ## extra!
                 ('alpha', 'Alpha', ''),
                 ('emit', 'Emit', ''),

                 ('diffuse', 'Diffuse Intensity', ''),
                 ('specular', 'Specular Intensity', ''),
                 ('hardness', 'Specular Hardness', ''),

                 ('translucency', 'Translucency', ''),
                 ('ambient', 'Ambient', ''),
                 ('mirror', 'Mirror Color', ''),
                 ('raymir', 'Ray Mirror', ''),

                 ('warp', 'Warp', ''),
                 ('displacement', 'Displacement', ''))

blend_type_items = (("MIX", "Mix", ""),
	             ("ADD", "Add", ""),
	             ("SUBTRACT", "Subtract", ""),
	             ("MULTIPLY", "Multiply", ""),
	             ("SCREEN", "Screen", ""),
	             ("OVERLAY", "Overlay", ""),
	             ("DIFFERENCE", "Difference", ""),
	             ("DIVIDE", "Divide", ""),
	             ("DARKEN", "Darken", ""),
	             ("LIGHTEN", "Lighten", ""),
	             ("HUE", "Hue", ""),
	             ("SATURATION", "Saturation", ""),
	             ("VALUE", "Value", ""),
	             ("COLOR", "Color", ""),
	             ("SOFT_LIGHT", "Soft Light", ""),
	             ("LINEAR_LIGHT", "Linear Light", ""))

class PackImage(bpy.types.Operator):
    bl_idname = "paint.yp_pack_image"
    bl_label = "Pack image into blend file"
    bl_description = "Pack image to blend file"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.object
        return obj and obj.type == 'MESH' and get_active_material()

    def execute(self, context):
        obj = context.object
        mat = get_active_material()
        img = mat.texture_paint_images[mat.paint_active_slot]

        img.pack(as_png=True)

        return{'FINISHED'}

class SaveAsImage(bpy.types.Operator):
    bl_idname = "paint.yp_save_as_texture_paint"
    bl_label = "Save As texture paint image"
    bl_description = "Save As texture paint Image"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        obj = context.object
        return obj and obj.type == 'MESH' and get_active_material()

    def execute(self, context):
        scene = context.scene
        obj = context.object
        mat = get_active_material()
        img = mat.texture_paint_images[mat.paint_active_slot]
        screen = context.screen
        area = context.area

        screen.ps_props.old_type = area.type
        scene.ps_props.screen_name = screen.name

        for i, a in enumerate(context.screen.areas):
            if a == area:
                screen.ps_props.temp_image_area_index = i
        
        old_type = area.type
        area.type = 'IMAGE_EDITOR'
        area.spaces[0].image = img
        scene.ps_props.last_image_name = img.name

        # HACK! change filepath if image is packed
        if img.packed_file:
            scene.ps_props.last_image_path = img.filepath_raw
            img.filepath_raw = '_TEMP_'

        bpy.ops.image.save_as('INVOKE_DEFAULT', relative_path=True)

        return{'FINISHED'}

class MatchTextureNameToImage(bpy.types.Operator):
    bl_idname = "paint.yp_match_texture_name_to_image_name"
    bl_label = "Match all texture name to image name"
    bl_description = "Match all texture name to image name (can be helpful for searching texture on node editor"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        sce = context.scene
        return sce.mo_props.override_mode == 'OFF'

    def execute(self, context):
        for tex in bpy.data.textures:
            if tex.type == 'IMAGE' and tex.image:
                tex.name = tex.image.name
        return {'FINISHED'}

class SaveImage(bpy.types.Operator):
    bl_idname = "paint.yp_save_texture_paint"
    bl_label = "Save texture paint image"
    bl_description = "Save texture paint image"

    @classmethod
    def poll(cls, context):
        obj = context.object
        return obj and obj.type == 'MESH' and get_active_material()

    def execute(self, context):
        obj = context.object
        mat = get_active_material()
        img = mat.texture_paint_images[mat.paint_active_slot]

        area = context.area
        old_type = area.type
        area.type = 'IMAGE_EDITOR'
        area.spaces[0].image = img
        bpy.ops.image.save()
        area.type = old_type

        return{'FINISHED'}

class ReloadImage(bpy.types.Operator):
    bl_idname = "paint.yp_reload_texture_paint"
    bl_label = "Reload texture paint image"
    bl_description = "Reload texture paint image"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.object
        return obj and obj.type == 'MESH' and get_active_material()

    def execute(self, context):
        obj = context.object
        mat = get_active_material()
        img = mat.texture_paint_images[mat.paint_active_slot]

        area = context.area
        old_type = area.type
        area.type = 'IMAGE_EDITOR'
        area.spaces[0].image = img
        bpy.ops.image.reload()
        area.type = old_type

        return {'FINISHED'}

class AddSimpleUVs(bpy.types.Operator):
    bl_idname = "mesh.yp_add_simple_uvs"
    bl_label = "Add simple UVs"
    bl_description = "Add Simple UVs"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.object
        return obj and obj.type == 'MESH' and get_active_material()

    def execute(self, context):
        obj = context.object
        mesh = obj.data
        #ps_idx = mat.paint_active_slot
        #ts_idx = mat.texture_paint_slots[ps_idx].index
        #ts = mat.texture_slots[ts_idx]

        ## Add new uv layers
        #bpy.ops.mesh.uv_texture_add()

        # Add simple uvs
        old_mode = obj.mode
        bpy.ops.object.mode_set(mode='TEXTURE_PAINT')
        bpy.ops.paint.add_simple_uvs()
        bpy.ops.object.mode_set(mode=old_mode)

        #new_uv = mesh.uv_layers.active
        #new_uv.name = 'SimpleUV'
        #ts.uv_layer = new_uv.name

        return {'FINISHED'}

class DuplicateOtherPaintSlots(bpy.types.Operator):
    bl_idname = "paint.yp_duplicate_other_material_paint_slots"
    bl_label = "Duplicate Paint Slots from other Material"
    bl_description = "Duplicate Paint Slots from other Material"
    bl_options = {'REGISTER', 'UNDO'}

    other_mat_name = StringProperty(name='Other Material Name', default='')

    @classmethod
    def poll(cls, context):
        mat = get_active_material()
        return mat

    def execute(self, context):
        #print(self.other_mat_name)
        mat = get_active_material()
        other_mat = bpy.data.materials.get(self.other_mat_name)
        if not other_mat:
            self.report({'ERROR'}, "No material named " + self.other_mat_name)
            return {'CANCELLED'}

        bpy.ops.material.yp_refresh_paint_slots(all_materials=True)

        # Get attribute list of a texture slot
        other_tslots = [ts for ts in other_mat.texture_slots 
                if ts and ts.texture and ts.texture.type == 'IMAGE' and ts.texture.image]

        if not other_tslots:
            self.report({'ERROR'}, "Material " + self.other_mat_name + " has no image textures")
            return {'CANCELLED'}

        ts_attr_list = dir(other_tslots[0])

        for ts in other_tslots:
            tex = ts.texture

            tex_found = any([slot for slot in mat.texture_slots if slot and slot.texture == tex])
            if tex_found: continue

            new_ts = mat.texture_slots.add()
            #new_ts.texture = tex

            for attr in ts_attr_list:
                if attr not in {'output_node'}:
                    try: setattr(new_ts, attr, getattr(ts, attr))
                    except: pass

        bpy.ops.material.yp_refresh_paint_slots(all_materials=True)

        return {'FINISHED'}

class DuplicateSlot(bpy.types.Operator):
    bl_idname = "paint.yp_duplicate_texture_paint_slot"
    bl_label = "Duplicate Selected Texture Paint Slot"
    bl_description = "Duplicate Selected Texture Paint Slot"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        mat = get_active_material()
        return mat and mat.texture_paint_images 

    def execute(self, context):
        obj = context.object
        mat = get_active_material()
        img = mat.texture_paint_images[mat.paint_active_slot]
        ts = mat.texture_slots[mat.texture_paint_slots[mat.paint_active_slot].index]

        new_tex = bpy.data.textures.new(img.name, 'IMAGE')
        new_tex.image = img

        new_ts = mat.texture_slots.add()
        new_ts.texture = new_tex

        ts_attr_list = dir(ts)
        tex_attr_list = dir(ts.texture)

        for attr in ts_attr_list:
            if attr not in {'output_node', 'texture'}:
                if attr == 'color':
                    value = getattr(ts, attr).copy()
                else: value = getattr(ts, attr)
                try: setattr(new_ts, attr, value)
                except: pass

        for attr in tex_attr_list:
            if attr not in {'image'}:
                value = getattr(ts.texture, attr)
                try: setattr(new_tex, attr, value)
                except: pass

        bpy.ops.material.yp_refresh_paint_slots(all_materials=False)

        return {'FINISHED'}

class RemoveSlot(bpy.types.Operator):
    """Remove selected texture paint slot"""
    bl_idname = "paint.remove_texture_paint_slot"
    bl_label = "Remove selected texture paint slot"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        mat = get_active_material()
        return mat and mat.texture_paint_images 

    def execute(self, context):
        obj = context.object
        #mat = obj.active_material
        mat = get_active_material()

        tex_id = mat.texture_paint_slots[mat.paint_active_slot].index

        mat.texture_slots.clear(tex_id)
        bpy.ops.material.yp_refresh_paint_slots(all_materials=False)

        # Remove force visible influence parameters
        reset_force_visible_influences(mat, tex_id)

        return {'FINISHED'}

class RemoveSlotWithPrompt(bpy.types.Operator):
    bl_idname = "paint.yp_remove_texture_paint_slot_with_prompt"
    bl_label = "Remove selected texture paint slot with prompt"
    bl_description = "Remove selected texture paint slot"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        mat = get_active_material()
        return mat and mat.texture_paint_images 

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        c = self.layout.column()
        c.label('Warning! You cannot undo this operation, are you sure?', icon='ERROR')

    def execute(self, context):
        mat = get_active_material()
        idx = mat.paint_active_slot
        bpy.ops.paint.remove_texture_paint_slot()
        bpy.ops.material.yp_refresh_paint_slots()
        mat.paint_active_slot = min(idx, len(mat.texture_paint_images)-1)
        return {'FINISHED'}

class OpenPaintTextureFromFile(bpy.types.Operator, ImportHelper):
    bl_idname = "paint.yp_open_paint_texture_from_file"
    bl_label = "Import Textures"
    bl_description = "Add Paint Texture From File"
    bl_options = {'REGISTER', 'UNDO'}

    # File related
    files = CollectionProperty(type=bpy.types.OperatorFileListElement, options={'HIDDEN', 'SKIP_SAVE'})
    directory = StringProperty(maxlen=1024, subtype='FILE_PATH', options={'HIDDEN', 'SKIP_SAVE'}) 

    # File browser filter
    filter_folder = BoolProperty(default=True, options={'HIDDEN', 'SKIP_SAVE'})
    filter_image = BoolProperty(default=True, options={'HIDDEN', 'SKIP_SAVE'})
    display_type = EnumProperty(
            items = (('FILE_DEFAULTDISPLAY', 'Default', ''),
                     ('FILE_SHORTDISLPAY', 'Short List', ''),
                     ('FILE_LONGDISPLAY', 'Long List', ''),
                     ('FILE_IMGDISPLAY', 'Thumbnails', '')),
            default = 'FILE_IMGDISPLAY',
            options={'HIDDEN', 'SKIP_SAVE'})

    relative = BoolProperty(name="Relative Path", default=True, description="Apply relative paths")
    new_slot = BoolProperty(default=False)

    #auto_influence = BoolProperty(default=True)
    influence = EnumProperty(
        name = 'Influence',
        items = influence_items,
        default = 'color_diffuse')

    blend_type = EnumProperty(
        name = 'Blend',
        items = blend_type_items,
        default = 'MIX')

    @classmethod
    def poll(cls, context):
        obj = context.object
        return obj and obj.type == 'MESH' and get_active_material()

    def draw(self, context):
        layout = self.layout 
        layout.prop(self, 'relative')
        if self.new_slot:
            layout.prop(self, 'influence')
            layout.prop(self, 'blend_type')

    def execute(self, context):
        obj = context.object
        mat = get_active_material()

        import_list, directory = self.generate_paths()
        if not self.new_slot:
            images = tuple(load_image(path, directory) for i, path in enumerate(import_list) if i == 0)
        else: images = tuple(load_image(path, directory) for path in import_list)

        for img in images:

            if self.relative:
                try:  # can't always find the relative path (between drive letters on windows)
                    img.filepath = bpy.path.relpath(img.filepath)
                except ValueError:
                    pass

            if not self.new_slot:
                ts = mat.texture_slots[mat.texture_paint_slots[mat.paint_active_slot].index]
                ts.texture.image = img
            else:
                tex = bpy.data.textures.new(img.name, 'IMAGE')
                tex.image = img

                ts = mat.texture_slots.add()
                ts.texture = tex
                ts.texture_coords = 'UV'
                ts.use_map_color_diffuse = False
                ts.blend_type = self.blend_type

                setattr(ts, 'use_map_'+self.influence, True)
                if self.influence == 'normal':
                    tex.use_normal_map = True

        bpy.ops.material.yp_refresh_paint_slots(all_materials=False)
        mat.paint_active_slot = [i for i, ps in enumerate(mat.texture_paint_images) if ps == img][0]

        return {'FINISHED'}

    def generate_paths(self):
        return (fn.name for fn in self.files), self.directory

class DuplicateMaterial(bpy.types.Operator):
    bl_idname = "material.yp_duplicate_to_non_node_material"
    bl_label = "Duplicate to non-node material"
    bl_description = "Duplicate material and disable use nodes on newly created material"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.object
        return (obj and 
                obj.active_material and 
                obj.active_material.use_nodes and
                obj.active_material.active_node_material)

    def execute(self, context):
        #print('Behemoth')
        obj = context.object
        mat = obj.active_material
        new_mat = None
        #node_mat = mat.active_node_material

        for node in mat.node_tree.nodes:
            if node.type == 'MATERIAL' and node.material == mat.active_node_material:
                if node.material == mat:
                    if not new_mat:
                        new_mat = mat.copy()
                        new_mat.use_nodes = False
                    node.material = new_mat
                elif node.material.use_nodes:
                    node.material.use_nodes = False

        bpy.ops.material.yp_refresh_paint_slots()

        return {'FINISHED'}

def add_new_paint_slot(mat, img, influence, override_mode, blend_type = 'MIX'):

    tex = bpy.data.textures.new(img.name, 'IMAGE')
    tex.image = img

    slot = mat.texture_slots.add()
    slot.texture = tex
    slot.texture_coords = 'UV'
    slot.use_map_color_diffuse = False
    slot.blend_type = blend_type

    if influence == 'normal':
        tex.use_normal_map = True

    if influence == 'bump':
        setattr(slot, 'use_map_normal', True)
    else: setattr(slot, 'use_map_' + influence, True)

    if override_mode == 'SPECULAR':
        mat.mo_props.originally_not_diffuse_texs += tex.name + ';'
        slot.use_map_color_spec = True

    if override_mode == 'NORMAL':
        mat.mo_props.originally_not_diffuse_texs += tex.name + ';'
        slot.use_map_normal = True
        tex.use_normal_map = True

class NewSlot(bpy.types.Operator):
    bl_idname = "paint.yp_add_slot_with_context"
    bl_label = "Add New Texture Paint Slot"
    bl_description = "Add new texture paint slot"
    bl_options = {'REGISTER', 'UNDO'}

    type = EnumProperty(
        name = 'Type',
        items = influence_items,
        default = 'color_diffuse')
    
    name = StringProperty(name='Name', default='')
    width = IntProperty(name='Width', default = 1024, min=1, max=16384)
    height = IntProperty(name='Height', default = 1024, min=1, max=16384)
    color = FloatVectorProperty(name='Color', size=4, subtype='COLOR', default=(0.0,0.0,0.0,1.0), min=0.0, max=1.0)
    alpha = BoolProperty(name='Alpha', default=True)
    hdr = BoolProperty(name='32 bit Float', default=False)

    #color_preset = EnumProperty(
    #        name = 'Color Preset',
    #        items = (('WHITE', 'White', ''),
    #                 ('BLACK', 'Black', ''),
    #                 ('TRANSPARENT', 'Transparent', ''),
    #                 ('NORMAL', 'Normal', ''),
    #                 ('CUSTOM', 'Custom Color', ''),
    #                 ),
    #        default = 'CUSTOM')

    generated_type = EnumProperty(
            name = 'Generated Type',
            items = (('BLANK', 'Blank', ''),
                     ('UV_GRID', 'UV Grid', ''),
                     ('COLOR_GRID', 'Color Grid', '')),
            default = 'BLANK')

    blend_type = EnumProperty(
        name = 'Blend',
        items = blend_type_items,
        default = 'MIX')

    @classmethod
    def poll(cls, context):
        return context.area.type =='VIEW_3D'

    def get_default_color(self, mat, channel):
        override_mode = bpy.context.scene.mo_props.override_mode

        #col = (1, 1, 1)
        #alpha = 1.0
        #col = (0.0, 0.0, 0.0)
        #alpha = 0.0

        if channel == 'normal' or override_mode in {'NORMAL', 'MATCAP'}:
            col = (0.5, 0.5, 1.0)
            alpha = 1.0
        elif channel == 'bump':
            col = (0.0, 0.0, 0.0)
            alpha = 1.0
        else:
            #col = (0.0, 0.0, 0.0)
            col = (1, 1, 1)
            alpha = 0.0
        #    base_tex_found = False
        #    for i, ts in enumerate(mat.texture_slots):
        #        if not ts: continue
        #        if not ts.texture: continue
        #        if ts.texture.type != 'IMAGE': continue
        #        if not ts.texture.image: continue
        #        if not mat.use_textures[i]: continue
        #        if ts.texture_coords != 'UV': continue
        #        if getattr(ts, 'use_map_' + channel):
        #            base_tex_found = True
        #            break
        #    if base_tex_found:
        #        col = (0, 0, 0)
        #        alpha = 0.0
        
        return (col[0], col[1], col[2], alpha)

    def invoke(self, context, event):
        obj = context.object
        mat = get_active_material()
        override_mode = context.scene.mo_props.override_mode
        
        if override_mode in {'DIFFUSE', 'DIFFUSE_SHADED', 'NORMAL', 'SPECULAR'}: 
            self.type = 'color_diffuse'
        elif override_mode in {'SPECULAR_SHADED'}: 
            self.type = 'color_spec'
        elif override_mode in {'MATCAP'}: 
            self.type = 'normal'

        #if override_mode == 'SPECULAR':
        #    posfix = posfix_dict['color_spec']
        #elif override_mode == 'NORMAL':
        #    posfix = posfix_dict['normal']
        #else: posfix = posfix_dict[self.type]
        posfix = posfix_dict[self.type]

        # Use alpha 0 if base texture already found
        self.color = self.get_default_color(mat, self.type)
        #self.color_preset = 'CUSTOM'

        self.name = mat.name + posfix

        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        row = self.layout.row()
        c = row.column()
        c.label('Name')
        c.label('Width')
        c.label('Height')
        #c.label('Color Preset')
        #c.label('Custom Color')
        c.label('Color')
        c.label('')
        c.label('Generated Type')
        c.label('')
        c.label('Blend')

        c = row.column()
        c.prop(self, 'name', text='')
        c.prop(self, 'width', text='')
        c.prop(self, 'height', text='')
        #c.prop(self, 'color_preset', expand=True)
        #c.prop(self, 'color_preset', text='')
        c.prop(self, 'color', text='')
        c.prop(self, 'alpha')
        c.prop(self, 'generated_type', text='')
        c.prop(self, 'hdr')
        c.prop(self, 'blend_type', text='')

        #row = self.layout.row()
        #c = row.column()
        #c.label('Custom Color')
        #c.label('')
        #c.label('Generated Type')
        #c.label('')
        #c.label('Blend')

        #c = row.column()
        #c.prop(self, 'color', text='')
        #c.prop(self, 'alpha')
        #c.prop(self, 'generated_type', text='')
        #c.prop(self, 'hdr')
        #c.prop(self, 'blend_type', text='')

    def execute(self, context):
        mat = get_active_material()
        override_mode = context.scene.mo_props.override_mode

        img = bpy.data.images.new(self.name, self.width, self.height, self.alpha, self.hdr)
        img.generated_type = self.generated_type

        # Set color
        #if self.color_preset == 'WHITE':
        #    img.generated_color = (1.0, 1.0, 1.0, 1.0)
        #elif self.color_preset == 'BLACK':
        #    img.generated_color = (0.0, 0.0, 0.0, 1.0)
        #elif self.color_preset == 'TRANSPARENT':
        #    img.generated_color = (0.0, 0.0, 0.0, 0.0)
        #elif self.color_preset == 'NORMAL':
        #    img.generated_color = (0.5, 0.5, 1.0, 1.0)
        #else:
        img.generated_color = self.color

        add_new_paint_slot(mat, img, self.type, override_mode, self.blend_type)

        # Refresh paint slots
        bpy.ops.material.yp_refresh_paint_slots(all_materials=False)
        # Select newly created image
        mat.paint_active_slot = [i for i, ps in enumerate(mat.texture_paint_images) if ps == img][0]

        return {'FINISHED'}

class AddSlotWithAvailableImage(bpy.types.Operator):
    bl_idname = "paint.yp_add_slot_with_available_image"
    bl_label = "Add Paint Slot with Available Image"
    bl_description = "Add new paint slot with available image"
    bl_options = {'REGISTER', 'UNDO'}

    influence = EnumProperty(
        name = 'Influence',
        items = influence_items,
        default = 'color_diffuse')

    blend_type = EnumProperty(
        name = 'Blend',
        items = blend_type_items,
        default = 'MIX')

    image_name = StringProperty(name="Image")
    image_coll = CollectionProperty(type=bpy.types.PropertyGroup)

    @classmethod
    def poll(cls, context):
        return True

    def invoke(self, context, event):
        self.image_coll.clear()
        imgs = bpy.data.images
        for img in imgs:
            self.image_coll.add().name = img.name
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        override_mode = context.scene.mo_props.override_mode
        layout = self.layout
        layout.prop_search(self, "image_name", self, "image_coll", icon='IMAGE_DATA')
        if override_mode == 'OFF':
            layout.prop(self, 'influence')
        layout.prop(self, 'blend_type')

    def execute(self, context):
        override_mode = context.scene.mo_props.override_mode
        mat = get_active_material()
        img = bpy.data.images.get(self.image_name)

        add_new_paint_slot(mat, img, self.influence, override_mode, self.blend_type)

        # Refresh paint slots
        bpy.ops.material.yp_refresh_paint_slots(all_materials=False)
        # Select newly created image
        mat.paint_active_slot = [i for i, ps in enumerate(mat.texture_paint_images) if ps == img][0]
        
        return {'FINISHED'}

class IMAGE_UL_all_images(bpy.types.UIList):
    pass
    #def draw_item(self):

def merge_texture_slot_using_render_non_mix(tslot_1, tslot_2):
    base_image = tslot_1.texture.image

    # Create temp scene
    temp_scene = bpy.data.scenes.new('_temp_scene')
    bpy.context.screen.scene = temp_scene

    # Set render setting
    temp_scene.render.resolution_percentage = 100
    temp_scene.render.resolution_x = x = base_image.size[0]
    temp_scene.render.resolution_y = y = base_image.size[1]
    temp_scene.render.alpha_mode = 'TRANSPARENT'

    # Set aspect ratio
    if y > x:
        temp_scene.render.pixel_aspect_x = y/x
    else: temp_scene.render.pixel_aspect_y = x/y

    # Add camera
    bpy.ops.object.camera_add(view_align=False, location=(0.0, 0.0, 5.0), rotation=(0.0, 0.0, 0.0))
    camera = bpy.context.object.data
    camera.type = 'ORTHO'
    camera.ortho_scale = 2.0

    # Set Plane
    bpy.ops.mesh.primitive_plane_add(radius=1, view_align=False, enter_editmode=True, location=(0, 0, 0))
    bpy.ops.uv.unwrap(method='CONFORMAL', correct_aspect=False, margin=0.0)
    bpy.ops.object.mode_set(mode='OBJECT') 
    plane = bpy.context.object.data

    # New material for plane
    temp_mat = bpy.data.materials.new('_blend_plane')
    temp_mat.use_shadeless = True
    plane.materials.append(temp_mat)

    # Use transparency
    temp_mat.use_transparency = True
    temp_mat.alpha = 0.0

    # Populate list of attributes
    attr_list = dir(tslot_1)

    for i, ts in enumerate([tslot_1, tslot_2]):
        new_ts = temp_mat.texture_slots.add()
        for attr in attr_list:
            try: 
                if attr != 'output_node' and not attr.startswith('use_map_'):
                    setattr(new_ts, attr, getattr(ts, attr))
            except: pass

        # First slot is always mix and use alpha
        if i == 0:
            new_ts.blend_type = 'MIX'
            new_ts.use_map_alpha = True
            new_ts.alpha_factor = 1.0

    # Render
    bpy.ops.render.render()

    # Create temporary image to store render result
    path = os.path.join(tempfile.gettempdir(), "_temp_image.png")
    result = bpy.data.images['Render Result']
    result.save_render(path)
    temp_img = load_image(path)

    # Copy image pixels
    pxs = list(temp_img.pixels)
    base_image.pixels = pxs

    # Delete temporary image
    temp_img.user_clear()
    bpy.data.images.remove(temp_img)
    os.remove(path)

    # Delete temp scene!
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    bpy.ops.scene.delete()

    # Delete mesh, material, & camera
    for tslot in temp_mat.texture_slots:
        if tslot: 
            tslot.texture = None
    bpy.data.meshes.remove(plane)
    bpy.data.materials.remove(temp_mat)
    camera.user_clear()
    bpy.data.cameras.remove(camera)

def merge_texture_slot_using_render(ts_list):
    base_image = ts_list[0].texture.image

    # Create temp scene
    temp_scene = bpy.data.scenes.new('_temp_scene')
    bpy.context.screen.scene = temp_scene

    # Set render setting
    temp_scene.render.resolution_percentage = 100
    temp_scene.render.resolution_x = x = base_image.size[0]
    temp_scene.render.resolution_y = y = base_image.size[1]
    temp_scene.render.alpha_mode = 'TRANSPARENT'

    # Set aspect ratio
    if y > x:
        temp_scene.render.pixel_aspect_x = y/x
    else: temp_scene.render.pixel_aspect_y = x/y

    # Add camera
    bpy.ops.object.camera_add(view_align=False, location=(0.0, 0.0, 5.0), rotation=(0.0, 0.0, 0.0))
    camera = bpy.context.object.data
    camera.type = 'ORTHO'
    camera.ortho_scale = 2.0

    # TO store temporary planes and materials
    planes = []
    mats = []

    # Populate list of attributes
    attr_list = dir(ts_list[0])

    # Create a plane for each texture slot
    for i, ts in enumerate(ts_list):

        # Set Plane
        bpy.ops.mesh.primitive_plane_add(radius=1, view_align=False, enter_editmode=True, location=(0, 0, i * 0.1))
        bpy.ops.uv.unwrap(method='CONFORMAL', correct_aspect=False, margin=0.0)
        bpy.ops.object.mode_set(mode='OBJECT') 
        plane = bpy.context.object.data
        planes.append(plane)

        # New material for plane
        temp_mat = bpy.data.materials.new('_blend_plane')
        temp_mat.use_shadeless = True
        plane.materials.append(temp_mat)
        mats.append(temp_mat)

        # Use transparency
        temp_mat.use_transparency = True
        temp_mat.alpha = 0.0

        # Set texture slot
        new_ts = temp_mat.texture_slots.add()
        for attr in attr_list:
            try: 
                if attr != 'output_node' and not attr.startswith('use_map_'):
                    setattr(new_ts, attr, getattr(ts, attr))
            except: pass

        new_ts.texture = ts.texture
        new_ts.use_map_alpha = True
        new_ts.alpha_factor = ts.diffuse_color_factor

    # Render
    bpy.ops.render.render()

    # Create temporary image to store render result
    path = os.path.join(tempfile.gettempdir(), "_temp_image.png")
    result = bpy.data.images['Render Result']
    result.save_render(path)
    temp_img = load_image(path)

    # Copy image pixels
    pxs = list(temp_img.pixels)
    base_image.pixels = pxs

    # Delete temporary image
    temp_img.user_clear()
    bpy.data.images.remove(temp_img)
    os.remove(path)

    #return

    # Delete temp scene!
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    bpy.ops.scene.delete()

    # Delete temporary stuffs
    camera.user_clear()
    bpy.data.cameras.remove(camera)

    for plane in planes:
        plane.user_clear()
        bpy.data.meshes.remove(plane)

    for mat in mats:
        for tslot in mat.texture_slots:
            if tslot: 
                tslot.texture = None
        mat.user_clear()
        bpy.data.materials.remove(mat)

def merge_texture_slot_using_bake(ts_list):
    base_image = ts_list[0].texture.image
    baked_img = base_image.copy()

    # Create temp scene
    temp_scene = bpy.data.scenes.new('_temp_scene')
    bpy.context.screen.scene = temp_scene

    # Set Plane
    bpy.ops.mesh.primitive_plane_add(radius=1, view_align=False, enter_editmode=True, location=(0, 0, 0))
    bpy.ops.uv.unwrap(method='CONFORMAL', correct_aspect=False, margin=0.0)
    #bpy.ops.uv.smart_project()
    bpy.ops.object.mode_set(mode='OBJECT') 
    plane = bpy.context.object.data
    #plane.uv_textures.active.data[0].image = base_image
    plane.uv_textures.active.data[0].image = baked_img

    # New material for plane
    temp_mat = bpy.data.materials.new('_blend_plane')
    temp_mat.use_shadeless = True
    plane.materials.append(temp_mat)

    # Populate list of attributes
    attr_list = dir(ts_list[0])

    for i, ts in enumerate(ts_list):
        new_ts = temp_mat.texture_slots.add()
        for attr in attr_list:
            try: 
                if attr != 'output_node' and not attr.startswith('use_map_'):
                    setattr(new_ts, attr, getattr(ts, attr))
            except: pass
        #if ts.use_rgb_to_intensity:
        #    ts.color = srgb_to_linear(ts.color)
    
    # Bake!
    bpy.ops.object.bake_image()

    return

    # Delete temp scene!
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    bpy.ops.scene.delete()

    # delete mesh, material, & camera
    for tslot in temp_mat.texture_slots:
        if tslot: 
            tslot.texture = None
    bpy.data.meshes.remove(plane)
    bpy.data.materials.remove(temp_mat)

    # Copy image pixels
    pxs = list(baked_img.pixels)
    base_image.pixels = pxs

    # Delete baked image
    bpy.data.images.remove(baked_img, do_unlink=True)

class MergeSlotBake(bpy.types.Operator):
    bl_idname = "paint.yp_merge_slot_bake"
    bl_label = "Merge Paint Slot"
    bl_description = "Merge paint slot"
    bl_options = {'REGISTER', 'UNDO'}

    type = EnumProperty(
        name = 'Type',
        items = (('UP', "Up", ""),
                 ('DOWN', "Down", "")),
        default = 'UP')

    @classmethod
    def poll(cls, context):
        mat = get_active_material()
        return mat and mat.texture_paint_images 

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        c = self.layout.column()
        c.label('WARNING!', icon='ERROR')
        c.label('Please save blend and images before continue')
        c.label('Because you have a chance of LOSING DATA if you UNDO')

    def execute(self, context):
        mat = get_active_material()
        ps_idx_1 = mat.paint_active_slot

        if self.type == 'UP' and ps_idx_1 < 1:
            self.report({'ERROR'}, "This slot has no upper slot")
            return {'CANCELLED'}
        if self.type == 'DOWN' and ps_idx_1 > len(mat.texture_paint_slots)-2:
            self.report({'ERROR'}, "This slot has no below slot")
            return {'CANCELLED'}

        ts_idx_1 = mat.texture_paint_slots[ps_idx_1].index
        ts_1 = mat.texture_slots[ts_idx_1]
        #tex_1 = ts_1.texture
        #img_1 = tex_1.image
        chs_1 = [key for key, value in influence_names.items() if getattr(ts_1, 'use_map_'+key)]

        if self.type == 'UP':
            ps_idx_2 = ps_idx_1 - 1
        else: ps_idx_2 = ps_idx_1 + 1

        ts_idx_2 = mat.texture_paint_slots[ps_idx_2].index
        ts_2 = mat.texture_slots[ts_idx_2]
        #tex_2 = ts_2.texture
        #img_2 = tex_2.image
        chs_2 = [key for key, value in influence_names.items() if getattr(ts_2, 'use_map_'+key)]

        if (chs_1 != chs_2 or 
            (ts_1.use_map_normal == ts_2.use_map_normal and 
             ts_1.texture.use_normal_map != ts_2.texture.use_normal_map)):
            self.report({'ERROR'}, "The slots has no matching channel/influence!")
            return {'CANCELLED'}

        #if ts_1.blend_type != ts_2.blend_type:
        #    self.report({'ERROR'}, "Cannot merge texture with different blend!")
        #    return {'CANCELLED'}

        if self.type == 'UP':
            ts_list = [ts_2, ts_1]
            delete_idx = ts_idx_1
        else: 
            ts_list = [ts_1, ts_2]
            delete_idx = ts_idx_2

        #if ts_1.use_rgb_to_intensity or ts_2.use_rgb_to_intensity:
        if ts_list[0].use_rgb_to_intensity:
            self.report({'ERROR'}, "Cannot merge to texture with RGB to intensity! Use bake diffuse/specular instead.")
            return {'CANCELLED'}

        ## MERGE PROCESS USING BAKE OR RENDER
        if ts_list[1].blend_type == 'MIX':
            merge_texture_slot_using_render(ts_list)
        else: 
            #merge_texture_slot_using_bake(ts_list)
            merge_texture_slot_using_render_non_mix(ts_list[0], ts_list[1])

        #return {'FINISHED'}

        # Delete alreade merged slot
        mat.texture_slots.clear(delete_idx)

        # Select merged paint slot
        if self.type == 'UP':
            mat.paint_active_slot = ps_idx_1-1

        bpy.ops.material.yp_refresh_paint_slots()

        return {'FINISHED'}

def bake_to_other_uv(obj, texture, source_uv_name, target_uv_name, margin):
    scene = bpy.context.scene
    mesh = obj.data

    # Duplicate object
    obj.data = obj.data.copy()
    temp_mesh = obj.data

    # Clear and create temp material for baking
    temp_mesh.materials.clear()
    temp_mat = bpy.data.materials.new('__bake_temp_')
    temp_mesh.materials.append(temp_mat)

    # Make material use alpha and shadeless
    temp_mat.use_transparency = True
    temp_mat.alpha = 0.0
    temp_mat.use_shadeless = True

    # Add texture
    #tex = ts.texture
    img = texture.image
    temp_mat.texture_slots.add()
    temp_mat.texture_slots[0].texture = texture
    temp_mat.texture_slots[0].uv_layer = source_uv_name
    temp_mat.texture_slots[0].use_map_alpha = True

    # Temp mesh target UV
    uv = temp_mesh.uv_textures.get(target_uv_name)
    uv.active_render = True
    temp_mesh.uv_textures.active = uv

    # Create target image and set uv to use this image
    target_img = img.copy()
    target_img.name = img.name + '_' + target_uv_name
    for i, data in enumerate(uv.data):
        uv.data[i].image = target_img

    # Remember!
    ori_bake_type = scene.render.bake_type
    ori_bake_margin = scene.render.bake_margin
    ori_bake_clear = scene.render.use_bake_clear

    # Bake!
    scene.render.bake_type = 'FULL'
    scene.render.use_bake_clear = True
    scene.render.bake_margin = margin
    bpy.ops.object.bake_image()

    # Revert!
    scene.render.bake_type = ori_bake_type
    scene.render.bake_margin = ori_bake_margin
    scene.render.use_bake_clear = ori_bake_clear

    # Delete temp data
    temp_mesh.materials.clear()
    bpy.data.materials.remove(temp_mat, do_unlink=True)

    # Back to original mesh
    obj.data = mesh

    # Delete temp mesh
    bpy.data.meshes.remove(temp_mesh, do_unlink=True)

    return target_img

class BakeImageToAnotherUV(bpy.types.Operator):
    bl_idname = "paint.yp_bake_image_to_another_uv"
    bl_label = "Convert image(s) to other UV"
    bl_description = "Convert image(s) to other UV"
    bl_options = {'REGISTER', 'UNDO'}

    uv_target_name = StringProperty(name="UV Target Name")
    uv_coll = CollectionProperty(type=bpy.types.PropertyGroup)
    bake_margin = IntProperty(default=5, subtype='PIXEL', name='Bake Margin')
    overwrite = BoolProperty(name='Overwrite Source Image', default=True)

    mode = EnumProperty(
        name = 'Mode',
        items = (('ACTIVE_ONLY', "Only active paint slot", ""),
                 ('ALL_MATERIAL_IMAGES', "All Material paint slots", "")),
        default = 'ACTIVE_ONLY')

    def get_active_texture_slot(self):
        mat = get_active_material()
        ps_idx = mat.paint_active_slot
        ts_idx = mat.texture_paint_slots[ps_idx].index
        ts = mat.texture_slots[ts_idx]
        return ts

    @classmethod
    def poll(cls, context):
        obj = context.object
        return obj and obj.type == 'MESH' and len(obj.data.uv_textures) > 0

    def invoke(self, context, event):
        obj = context.object
        ts = self.get_active_texture_slot()

        #if len(obj.data.uv_textures) < 2:
        #    return self.execute(context)

        if ts.uv_layer == '':
            source_uv_name = obj.data.uv_textures.active.name
        else: source_uv_name = ts.uv_layer
        
        self.uv_coll.clear()
        for uv in obj.data.uv_textures:
            self.uv_coll.add().name = uv.name
            #if uv.name != source_uv_name:
            #    self.uv_coll.add().name = uv.name
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        ts = self.get_active_texture_slot()
        row = layout.row()
        c = row.column()
        c.label('UV Target')
        c.label('Bake Margin')
        c = row.column()
        c.prop_search(self, "uv_target_name", self, "uv_coll", text='', icon='GROUP_UVS')
        c.prop(self, 'bake_margin', text='')
        c.prop(self, 'overwrite', text='Overwrite image')

    def execute(self, context):
        obj = context.object
        mesh = obj.data
        scene = context.scene
        mat = get_active_material()

        #if len(obj.data.uv_textures) < 2:
        #    self.report({'ERROR'}, "Need at least two UV Maps!")
        #    return {'CANCELLED'}

        if self.uv_target_name == '':
            self.report({'ERROR'}, "UV target cannot be empty!")
            return {'CANCELLED'}

        if self.mode == 'ACTIVE_ONLY':
            slots = [self.get_active_texture_slot()]
        elif self.mode == 'ALL_MATERIAL_IMAGES':
            slots = []
            for ps in mat.texture_paint_slots:
                slots.append(mat.texture_slots[ps.index])

        # Successful counter
        success = 0

        for ts in slots:

            # Get uv target and source
            uv_target = obj.data.uv_textures.get(self.uv_target_name)
            if ts.uv_layer == '':
                uv_source = obj.data.uv_textures.active
            else: uv_source = obj.data.uv_textures.get(ts.uv_layer)

            # Get texture and image
            tex = ts.texture
            img = tex.image

            if ts.uv_layer == '':
                self.report({'WARNING'}, "Paint Slot '" + img.name +"' UV Map is empty! So it uses the active UV Map ('" + obj.data.uv_textures.active.name + "') as source!")

            #if self.uv_target_name == uv_source.name:
            #    self.report({'ERROR'}, "Convert process of '" + img.name + "' skipped because source and target uv is same (" + uv_target.name + ")!")
            #    continue

            # Get baked image
            baked_img = bake_to_other_uv(obj, tex, uv_source.name, uv_target.name, self.bake_margin)

            # Dealing with target image
            if self.overwrite:
                # Copy image pixels
                pxs = list(baked_img.pixels)
                img.pixels = pxs

                bpy.data.images.remove(baked_img, do_unlink=True)
                # Use new uv map
                ts.uv_layer = uv_target.name
            else:
                # Cerate new texture slot if not overwriting
                new_ts = mat.texture_slots.add()
                new_tex = bpy.data.textures.new(baked_img.name, 'IMAGE')
                new_tex.image= baked_img
                new_ts.texture = new_tex
                new_ts.uv_layer = uv_target.name

                ts_attr_list = dir(ts)

                for attr in ts_attr_list:
                    if attr not in {'output_node', 'texture', 'uv_layer'}:
                        try: setattr(new_ts, attr, getattr(ts, attr))
                        except: pass

                bpy.ops.material.yp_refresh_paint_slots()

                # Disable source slot and select new paint slot
                target_ts_idx = -1
                for i, slot in enumerate(mat.texture_slots):
                    if slot == ts:
                        mat.use_textures[i] = False
                    if slot == new_ts:
                        target_ts_idx = i

                target_ps_idx = -1
                for i, ps in enumerate(mat.texture_paint_slots):
                    #print(ps.index)
                    if ps.index == target_ts_idx:
                        target_ps_idx = i

                mat.paint_active_slot = target_ps_idx

            success += 1

        if success == 0:
            return {'CANCELLED'}

        return {'FINISHED'}

# --- Force visible influence stuff

# Decode force visible influences string to dictionary
# Input:
# Format: "index/influence/influence;index/influence"
# Example: "0/color_diffuse/color_spec;1/color_diffuse"
# Output:
# Format: { index : [influence, influence], index : [influence] }
# Example: { 0 : ['color_diffuse', 'color_spec'], 1 : ['color_diffuse'] }
def decode_force_visible_influence(mat):
    prop = mat.ps_props.force_visible_influences

    force_visible_influences = {}

    if prop != '':
        segments = prop.split(';')
        for segment in segments:
            subsegments = segment.split('/')
            force_visible_influences[int(subsegments[0])] = subsegments[1:]

    return force_visible_influences

# Encode force visible influences dictionary to string
# Input:
# Format: { index : [influence, influence], index : [influence] }
# Example: { 0 : ['color_diffuse', 'color_spec'], 1 : ['color_diffuse'] }
# Output:
# Format: "index/influence/influence;index/influence"
# Example: "0/color_diffuse/color_spec;1/color_diffuse"
def encode_force_visible_influences(mat, force_visible_influences):
    encoded = ''

    for idx, influences in force_visible_influences.items():
        encoded += str(idx)
        for influence in influences:
            encoded += '/' + influence
        encoded += ';'

    # Remove last ';'
    if encoded != '':
        encoded = encoded[:-1]

    mat.ps_props.force_visible_influences = encoded

# Add data to force visible influences properties on material
def add_data_to_force_visible_influences(mat, idx, influence):
    # Get force visible influences dictionary
    force_visible_influences = decode_force_visible_influence(mat)

    # Check if hidden influence already available in dictionary
    if idx in force_visible_influences and influence in force_visible_influences[idx]:
        return

    # If index not in dictionary
    if idx not in force_visible_influences:
        force_visible_influences[idx] = []
    
    # Add influence to dictionary
    force_visible_influences[idx].append(influence)

    # Encode the dictionary again
    encode_force_visible_influences(mat, force_visible_influences)

# Remove data from force_visible_influences
def remove_data_from_force_visible_influences(mat, idx, influence):
    # Get force visible influences dictionary
    force_visible_influences = decode_force_visible_influence(mat)

    if idx not in force_visible_influences:
        return

    # Remove from dictionary
    if influence in force_visible_influences[idx]:
        force_visible_influences[idx].remove(influence)
    if force_visible_influences[idx] == []:
        del force_visible_influences[idx]

    #print(force_visible_influences)

    # Encode the dictionary again
    encode_force_visible_influences(mat, force_visible_influences)

# Toggle data on force visible influences
def toggle_data_on_force_visible_influences(mat, idx, influence):
    # Get force visible influences dictionary
    force_visible_influences = decode_force_visible_influence(mat)

    # Check if hidden influence already available in dictionary
    if idx in force_visible_influences and influence in force_visible_influences[idx]:
        remove_data_from_force_visible_influences(mat, idx, influence)
    else:
        add_data_to_force_visible_influences(mat, idx, influence)

# Check if index is available on force visible influences:
def check_available_force_visible_influences(mat, idx, influence):
    # Get force visible influences dictionary
    force_visible_influences = decode_force_visible_influence(mat)

    if idx in force_visible_influences and influence in force_visible_influences[idx]:
        return True

    return False

# Swap force visible influences by index
def swap_force_visible_influences(mat, idx_1, idx_2):
    prop = mat.ps_props

    prop.force_visible_influences = prop.force_visible_influences.replace(str(idx_1), 'temp')
    prop.force_visible_influences = prop.force_visible_influences.replace(str(idx_2), str(idx_1))
    prop.force_visible_influences = prop.force_visible_influences.replace('temp', str(idx_2))

def reset_force_visible_influences(mat, idx):
    # Get force visible influences dictionary
    force_visible_influences = decode_force_visible_influence(mat)

    # Check the index
    if idx not in force_visible_influences:
        return

    # Remove from dictionary
    del force_visible_influences[idx]

    # Encode the dictionary again
    encode_force_visible_influences(mat, force_visible_influences)

# --- End of force visible influence stuff

class ToggleForceVisibleInfluence(bpy.types.Operator):
    bl_idname = "paint.yp_toggle_force_visible_influence"
    bl_label = "Toggle Hide Influence"
    bl_description = "Toggle Hide Influence"
    bl_options = {'REGISTER', 'UNDO'}

    influence = StringProperty(default='')

    @classmethod
    def poll(cls, context):
        return True
        #mat = get_active_material()
        #return mat and mat.texture_paint_images 

    def execute(self, context):
        if self.influence not in influence_names:
            self.report({'ERROR'}, "No influence called " + self.influence)
            return {'CANCELLED'}

        mat = get_active_material()
        slot_idx = mat.texture_paint_slots[mat.paint_active_slot].index
        tslot = mat.texture_slots[slot_idx]
        tex = tslot.texture

        if self.influence == 'bump':
            influence = 'normal'
        else: influence = self.influence

        # Add data to force visible influences
        add_data_to_force_visible_influences(mat, slot_idx, influence)
        #toggle_data_on_force_visible_influences(mat, slot_idx, influence)
        #print(mat.ps_props.force_visible_influences)

        # Toggle channel
        if getattr(tslot, 'use_map_' + influence):
            setattr(tslot, 'use_map_' + influence, False)
        else: setattr(tslot, 'use_map_' + influence, True)

        return {'FINISHED'}

class RemoveInfluence(bpy.types.Operator):
    bl_idname = "texture.yp_remove_influence"
    bl_label = "Remove Influence"
    bl_description = "Remove Influence"
    bl_options = {'REGISTER', 'UNDO'}

    influence = StringProperty(default='')

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        #print(self.influence)
        if self.influence not in influence_names:
            self.report({'ERROR'}, "No influence called " + self.influence)
            return {'CANCELLED'}

        mat = get_active_material()
        slot_idx = mat.texture_paint_slots[mat.paint_active_slot].index
        tslot = mat.texture_slots[slot_idx]
        tex = tslot.texture

        if self.influence == 'bump':
            influence = 'normal'
        else: influence = self.influence

        setattr(tslot, 'use_map_' + influence, False)

        # Remove data to force visible influences
        remove_data_from_force_visible_influences(mat, slot_idx, influence)

        if self.influence == 'normal':
            tex.use_normal_map = False
            
        return{'FINISHED'}

class ToggleNormalBump(bpy.types.Operator):
    bl_idname = "texture.yp_toggle_normal_bump"
    bl_label = "Toggle Normal Bump"
    bl_description = "Toggle normal or bump for normal Influence"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        mat = get_active_material()
        tslot = mat.texture_slots[mat.texture_paint_slots[mat.paint_active_slot].index]
        tex = tslot.texture

        tex.use_normal_map = not tex.use_normal_map

        return{'FINISHED'}

class AddInfluence(bpy.types.Operator):
    bl_idname = "texture.yp_add_new_influence"
    bl_label = "Add new texture influence"
    bl_description = "Add new texture influence"
    bl_options = {'REGISTER', 'UNDO'}

    influence = EnumProperty(
        name = 'Type',
        items = influence_items,
        default = 'color_diffuse')

    @classmethod
    def poll(cls, context):
        obj = context.object
        return obj and get_active_material()

    def execute(self, context):
        mat = get_active_material()
        tslot = mat.texture_slots[mat.texture_paint_slots[mat.paint_active_slot].index]
        tex = tslot.texture

        if self.influence == 'normal':
            tex.use_normal_map = True

        if self.influence == 'bump':
            setattr(tslot, 'use_map_normal', True)
            tex.use_normal_map = False
        else: setattr(tslot, 'use_map_' + self.influence, True)

        return{'FINISHED'}

class PaintSlotMove(bpy.types.Operator):
    bl_idname = "paint.yp_slot_move"
    bl_label = "Move Texture Paint Slot"
    bl_description = "Move paint slot up and down"
    bl_options = {'REGISTER', 'UNDO'}

    type = EnumProperty(
        name = 'Type',
        items = (('UP', "Up", ""),
                 ('DOWN', "Down", "")),
        default = 'UP')

    @classmethod
    def poll(cls, context):
        mat = get_active_material()
        return mat and mat.texture_paint_images 

    def execute(self, context):

        mat = get_active_material()
        tslots = mat.texture_slots

        ps_idx_a = mat.paint_active_slot
        ts_idx_a = mat.texture_paint_slots[ps_idx_a].index
        slot_a = tslots[ts_idx_a]

        ps_idx_b = None
        #if self.type == 'UP' and ts_idx_a > 0:
        if self.type == 'UP' and ps_idx_a > 0:
            ps_idx_b = ps_idx_a-1
        #elif self.type == 'DOWN' and ts_idx_a < len(mat.texture_paint_slots)-1:
        elif self.type == 'DOWN' and ps_idx_a < len(mat.texture_paint_slots)-1:
            ps_idx_b = ps_idx_a+1
        else: return {'FINISHED'}

        ts_idx_b = mat.texture_paint_slots[ps_idx_b].index
        slot_b = tslots[ts_idx_b]
        mat.paint_active_slot = ps_idx_b

        attr_list = dir(tslots[ts_idx_a])

        data_a = {}
        for attr in attr_list:
            if attr not in {'output_node'}:
                if attr in {'color', 'offset', 'scale'}:
                    data_a[attr] = getattr(slot_a, attr).copy()
                else: data_a[attr] = getattr(slot_a, attr)

        data_b = {}
        for attr in attr_list:
            if attr not in {'output_node'}:
                if attr in {'color', 'offset', 'scale'}:
                    data_b[attr] = getattr(slot_b, attr).copy()
                else: data_b[attr] = getattr(slot_b, attr)

        for key, value in data_a.items():
            #if key == 'color':
            #    print(getattr(slot_b, key))
            try: setattr(slot_b, key, value)
            except: pass
                #print('Cannot set key', key)

        for key, value in data_b.items():
            #if key == 'color':
            #    print(getattr(slot_a, key))
            try: setattr(slot_a, key, value)
            except: pass
                #print('Cannot set key', key)
        
        # Clear some dict to prevent memory leak
        data_a.clear()
        data_b.clear()

        # Swap force visible influences
        swap_force_visible_influences(mat, ts_idx_a, ts_idx_b)

        # Refresh paint slots
        bpy.ops.material.yp_refresh_paint_slots(all_materials=False)
        # Update image editor image hack
        mat.paint_active_slot = mat.paint_active_slot

        return {'FINISHED'}

# UPDATE HANDLERS
@persistent
def set_recover_area_enable(scene):
    screen = bpy.context.screen
    ops = bpy.context.window_manager.operators

    #print(ops[-1].bl_idname)

    if (ops and 'PAINT_OT_yp_save_as_texture_paint' in ops[-1].bl_idname and
            screen.areas[0].type == 'FILE_BROWSER' and
            not screen.ps_props.recover_area):

        normal_screen = bpy.data.screens[scene.ps_props.screen_name]
        normal_screen.ps_props.recover_area = True

        print(normal_screen)

@persistent
def do_recover_area(scene):
    screen = bpy.context.screen
    ops = bpy.context.window_manager.operators

    if (ops and 'PAINT_OT_yp_save_as_texture_paint' in ops[-1].bl_idname and
        screen.areas[0].type != 'FILE_BROWSER' and
        screen.ps_props.recover_area):
        
        for i, area in enumerate(screen.areas):
            if i == screen.ps_props.temp_image_area_index:
                #img = area.spaces[0].image
                #if not img.is_dirty and img.packed_file:
                #    print('apeeel')
                #    #img.pack(as_png=True)
                #    img.unpack()
                if area.type == 'IMAGE_EDITOR':
                    area.type = screen.ps_props.old_type
                    screen.ps_props.recover_area = False
                    img = bpy.data.images.get(scene.ps_props.last_image_name)
                    if img and img.packed_file:
                        if img.filepath == '_TEMP_':
                            img.filepath_raw = scene.ps_props.last_image_path
                        else:
                            print('aaaa', img.filepath)
                            true_filepath = img.filepath
                            true_name = img.name

                            # JUST ANOTHER HACK! Blender sometimes unpack at wrong filepath
                            # Just make sure it can be tracked and then delete it
                            img.name = '_TEMP_'
                            img.unpack(method='USE_ORIGINAL')
                            fail_path = img.filepath_from_user()
                            os.remove(fail_path)

                            # Recover image
                            img.filepath = true_filepath
                            img.name = true_name
                    return

@persistent
def update_node_mat_image_texpaint(scene):
    if scene.mo_props.halt_update: return

    if not hasattr(bpy.context, 'object'):
        return

    obj = bpy.context.object
    if not obj: return

    mat = obj.active_material
    if not mat: return

    node_mat = mat.active_node_material
    if not node_mat: return

    imgs = node_mat.texture_paint_images
    if not imgs: return
    img = node_mat.texture_paint_images[node_mat.paint_active_slot]
    
    if obj.mode != 'TEXTURE_PAINT': return

    screen = bpy.context.screen
    yp_ids = [int(i[2:]) for i in screen.yp_props.uncollapsed_main_ypanel.split()]
    if not yp_ids: return

    settings = scene.tool_settings.image_paint
    if settings.mode != 'IMAGE':
        settings.mode = 'IMAGE'

    if settings.canvas != img:
        settings.canvas = img

# PROPS
class ScenePaintSlotsProps(bpy.types.PropertyGroup):
    screen_name = StringProperty(default='')
    last_image_name = StringProperty(default='')
    last_image_path = StringProperty(default='')

class ScreenPaintSlotsProps(bpy.types.PropertyGroup):
    temp_image_area_index = IntProperty(default=-1)
    old_type = StringProperty(default='')
    recover_area = BoolProperty(default=False)

class ImagePaintSlotsProps(bpy.types.PropertyGroup):
    original_packed = BoolProperty(default=False)

class MaterialPaintSlotProps(bpy.types.PropertyGroup):
    force_visible_influences = StringProperty(default='')

class TextureExtras(bpy.types.PropertyGroup):
    channel = EnumProperty(
        items = (('use_map_color_diffuse', "Diffuse Color", ""),
                 ('use_map_color_spec', "Specular Color", ""),
                 ('use_map_normal', "Normal", "")),
        default = 'use_map_color_diffuse')

# PANEL EXTRAS
def draw_viewport_shade_switcher(self, context):
    space = context.space_data
    row = self.layout.row()
    row.prop(space, 'viewport_shade', expand=True, icon_only=True)

class PaintTextureSpecialMenu(bpy.types.Menu):
    bl_idname = "MATERIAL_MT_texture_paint_specials"
    bl_label = "Texture Paint Special Menu"

    def draw(self, context):
        layout = self.layout

        obj = context.object
        mat = obj.active_material

        #layout.operator("paint.merge_slot", text="Merge Up", icon='TRIA_UP').type = 'UP'
        #layout.operator("paint.merge_slot", text="Merge Down", icon='TRIA_DOWN').type = 'DOWN'
        layout.operator("paint.yp_merge_slot_bake", text="Merge Up", icon='TRIA_UP').type = 'UP'
        #layout.operator("paint.yp_merge_slot_bake", text="Merge Down", icon='TRIA_DOWN').type = 'DOWN'
        layout.operator("paint.yp_duplicate_texture_paint_slot", text="Duplicate", icon='COPY_ID')
        layout.operator("paint.yp_bake_image_to_another_uv", text='Convert all images to another UV', icon='RENDER_STILL').mode = 'ALL_MATERIAL_IMAGES'
        if mat.use_nodes:
            node_mat = mat.active_node_material
            layout.operator("paint.yp_duplicate_other_material_paint_slots", text="Duplicate Main Material Paint Slots", icon='COPY_ID').other_mat_name = mat.name
        layout.operator("paint.yp_match_texture_name_to_image_name", icon='SYNTAX_ON')

def register():
    #bpy.types.VIEW3D_PT_view3d_shading.prepend(draw_viewport_shade_switcher)
    #bpy.types.VIEW3D_PT_slots_projectpaint.append(draw_texture_paint_slot_extras)
    #bpy.types.Texture.extras = PointerProperty(type=TextureExtras)
    # Handlers
    #bpy.app.handlers.scene_update_pre.append(match_paint_texture_slot)
    bpy.types.Screen.ps_props = PointerProperty(type=ScreenPaintSlotsProps)
    bpy.types.Scene.ps_props = PointerProperty(type=ScenePaintSlotsProps)
    bpy.types.Image.ps_props = PointerProperty(type=ImagePaintSlotsProps)
    bpy.types.Material.ps_props = PointerProperty(type=MaterialPaintSlotProps)

    bpy.app.handlers.scene_update_pre.append(set_recover_area_enable)
    bpy.app.handlers.scene_update_pre.append(do_recover_area)
    bpy.app.handlers.scene_update_pre.append(update_node_mat_image_texpaint)

def unregister():
    #bpy.types.VIEW3D_PT_view3d_shading.remove(draw_viewport_shade_switcher)
    #bpy.types.VIEW3D_PT_slots_projectpaint.remove(draw_texture_paint_slot_extras)
    # Handlers
    #bpy.app.handlers.scene_update_pre.remove(match_paint_texture_slot)
    bpy.app.handlers.scene_update_pre.remove(do_recover_area)
    bpy.app.handlers.scene_update_pre.remove(set_recover_area_enable)
    bpy.app.handlers.scene_update_pre.remove(update_node_mat_image_texpaint)
