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
    "name": "Render Border",
    "description": "Render Border",
    "author": "Christian Brinkmann, David Wiesner",
    "version": (0, 0, 2),
    "blender": (2, 75, 0),
    "tracker_url": "https://github.com/p2or/blender-renderborder",
    "location": "Camera > Properties > Data > Render Border",
    "category": "Render"
}

import bpy

def round_pixels(pixel_float):
    return round(pixel_float, 2)

def calc_normalized(pixels_int, pixel_max):
    return pixels_int / pixel_max

def calc_pixels(normalized_float, pixel_max):
    return normalized_float * pixel_max

def calc_width(res_x, min_x, max_x):
    return res_x * max_x - res_x * min_x

def calc_height(res_y, min_y, max_y):
    return res_y * max_y - res_y * min_y  

def calc_centerX(res_x, min_x, width):
    return res_x * min_x + width / 2

def calc_centerY(res_y, min_y, height):
    return res_y * min_y + height / 2

# ------------------------------------------------------------------------
# properties
# ------------------------------------------------------------------------
class RenderBorder(bpy.types.PropertyGroup):
    
    # static member
    _rd = None
    _resX = _resY = _minX = _maxX = _minY = _maxY = 0 
    _width = _height = _centerX = _centerY = 0
                       
    def set_centerX(self, value):
        diffX = calc_normalized((value - self._centerX), self._resX)
        self._rd.border_min_x += diffX
        self._rd.border_max_x += diffX
        RenderBorder._minX = calc_pixels(self._rd.border_min_x, self._resX)
        RenderBorder._maxX = calc_pixels(self._rd.border_max_x, self._resX)
        RenderBorder._width = calc_width(self._resX, self._rd.border_min_x, self._rd.border_max_x)
        RenderBorder._centerX = value
    
    def set_centerY(self, value):
        diffY = calc_normalized((value - self._centerY), self._resY)
        self._rd.border_min_y += diffY
        self._rd.border_max_y += diffY
        RenderBorder._minY = calc_pixels(self._rd.border_min_y, self._resY)
        RenderBorder._maxY = calc_pixels(self._rd.border_max_y, self._resY)
        RenderBorder._height = calc_height(self._resY, self._rd.border_min_y, self._rd.border_max_y)
        RenderBorder._centerY = value
    
    def set_minX(self, value):
        self._rd.border_min_x = calc_normalized(value, self._resX)
        RenderBorder._minX = round_pixels(calc_pixels(self._rd.border_min_x, self._resX))
        RenderBorder._width = calc_width(self._resX, self._rd.border_min_x, self._rd.border_max_x)
        RenderBorder._centerX = calc_centerX(self._resX, self._rd.border_min_x, self._width)
    
    def set_maxX(self, value):
        self._rd.border_max_x = calc_normalized(value, self._resX)
        RenderBorder._maxX = round_pixels(calc_pixels(self._rd.border_max_x, self._resX))
        RenderBorder._width = calc_width(self._resX, self._rd.border_min_x, self._rd.border_max_x)
        RenderBorder._centerX = calc_centerX(self._resX, self._rd.border_min_x, self._width)

    def set_minY(self, value):
        self._rd.border_min_y = calc_normalized(value, self._resY)
        RenderBorder._minY = round_pixels(calc_pixels(self._rd.border_min_y, self._resY))
        RenderBorder._height = calc_height(self._resY, self._rd.border_min_y, self._rd.border_max_y)
        RenderBorder._centerY = calc_centerY(self._resY, self._rd.border_min_y, self._height)
        
    def set_maxY(self, value):
        self._rd.border_max_y = calc_normalized(value, self._resY)
        RenderBorder._maxY = round_pixels(calc_pixels(self._rd.border_max_y, self._resY))
        RenderBorder._height = calc_height(self._resY, self._rd.border_min_y, self._rd.border_max_y)
        RenderBorder._centerY = calc_centerY(self._resY, self._rd.border_min_y, self._height)
    
    def set_useBorder(self, value):
        self._rd.use_border = value
           
    def get_centerX(self):
        return RenderBorder._centerX
    
    def get_centerY(self):
        return RenderBorder._centerY
        
    def get_minX(self):
        return RenderBorder._minX
    
    def get_maxX(self):
        return RenderBorder._maxX
    
    def get_minY(self):
        return RenderBorder._minY
    
    def get_maxY(self):
        return RenderBorder._maxY

    def get_width(self):
        return abs(round_pixels(RenderBorder._width))
    
    def get_height(self):
        return abs(round_pixels(RenderBorder._height))
        
    def get_useBorder(self):
        bpy.ops.renderborder.init_renderborder()
        bpy.ops.renderborder.update_renderborder()
        return self._rd.use_border

    center_x = bpy.props.IntProperty(
        name = "Center X",
        description =   ("Horizontal center of the render border box"),
        min = 0, default = 0, get=get_centerX, set=set_centerX )
    
    center_y = bpy.props.IntProperty(
        name = "Center Y",
        description =   ("Vertical center of the render border box"),
        min = 0, default = 0, get=get_centerY, set=set_centerY )

    width = bpy.props.IntProperty(
        name = "Width",
        description =   ("Width of render border box"),
        min = 0, default = 0, get=get_width)

    height = bpy.props.IntProperty(
        name = "Height",
        description =   ("Height of render border box"),
        min = 0, default = 0, get=get_height)
                   
    min_x = bpy.props.IntProperty(
        description =   ("Pixel distance between the left edge "
                        "of the camera border and the left "
                        "side of the render border box"),
        name = "Min X", min = 0, default = 0, get=get_minX, set=set_minX )
    
    max_x = bpy.props.IntProperty(
        description =   ("Pixel distance between the right edge "
                        "of the camera border and the right "
                        "side of the render border box"),
        name = "Max X",min = 0, default = 0, get=get_maxX, set=set_maxX )
        
    min_y = bpy.props.IntProperty(
        description =   ("Pixel distance between the bottom edge "
                        "of the camera border and the bottom "
                        "edge of the render border box"),
        name = "Min Y", min = 0, default = 0, get=get_minY, set=set_minY )
   
    max_y = bpy.props.IntProperty(
        description =   ("Pixel distance between the top edge "
                        "of the camera border and the top "
                        "edge of the render border box"),
        name = "Max Y", min = 0, default = 0, get=get_maxY, set=set_maxY )
    
    use_rborder = bpy.props.BoolProperty(
        name = "Use render border", description = "Use render border", 
        get=get_useBorder, set=set_useBorder)

# ------------------------------------------------------------------------
# operators
# ------------------------------------------------------------------------
# http://wiki.blender.org/index.php/Extensions:2.6/Py/API_Changes
class InitRenderBorder(bpy.types.Operator):
    bl_idname = "renderborder.init_renderborder"
    bl_label = "Init Render Border"
    bl_options = {'INTERNAL'}
 
    @classmethod
    def poll(cls, context):
        return context.active_object is not None
 
    def execute(self, context):
        scn = context.scene
        #if RenderBorder._rd == None:
        RenderBorder._rd = scn.render
        RenderBorder._resX = scn.render.resolution_x
        RenderBorder._resY = scn.render.resolution_y
        return {'FINISHED'}

class UpdateRenderBorder(bpy.types.Operator):
    bl_idname = "renderborder.update_renderborder"
    bl_label = "Update Render Border"
    bl_description = "Adapt size of viewport values"
    bl_options = {'INTERNAL'}
    
    def execute(self, context):
        scn = context.scene
        rbx = scn.renderborder
        rbx.min_x = round_pixels(calc_pixels(scn.render.border_min_x, scn.render.resolution_x))
        rbx.min_y = round_pixels(calc_pixels(scn.render.border_min_y, scn.render.resolution_y))
        rbx.max_x = round_pixels(calc_pixels(scn.render.border_max_x, scn.render.resolution_x))
        rbx.max_y = round_pixels(calc_pixels(scn.render.border_max_y, scn.render.resolution_y))
        return {'FINISHED'}
      
class ResetRenderBorder(bpy.types.Operator):
    bl_idname = "renderborder.reset_renderborder"
    bl_label = "Reset Render Border"
    bl_description = "Fit render border to the current camera resolution"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        scn = context.scene
        rbx = scn.renderborder
        rbx.min_x = 0
        rbx.min_y = 0
        rbx.max_x = scn.render.resolution_x
        rbx.max_y = scn.render.resolution_y
        self.report({'INFO'}, "Render Border adapted")
        return {'FINISHED'}
    
# ------------------------------------------------------------------------
# panel
# ------------------------------------------------------------------------

class RenderBorderPanel(bpy.types.Panel):
    bl_label = "Render Border"
    bl_idname = "DATA_PT_camera.renderborder"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"
    
    @classmethod
    def poll(cls, context):
        return context.active_object.type == "CAMERA"
    
    def draw_header(self, context):
        scn = context.scene
        rbx = scn.renderborder
        self.layout.prop(rbx, "use_rborder", text="")
    
    def draw(self, context):
        scn = context.scene
        rbx = scn.renderborder
        layout = self.layout
      
        row = layout.row()
        col = layout.column(align=True)
        rowsub = col.row(align=True)
        rowsub.prop(rbx, "min_x", text="X")
        rowsub.prop(rbx, "max_x", text="R")
        rowsub = col.row(align=True)
        rowsub.prop(rbx, "min_y", text="Y")
        rowsub.prop(rbx, "max_y", text="T")
        col.prop(rbx, "center_x")
        col.prop(rbx, "center_y")
        col.operator("renderborder.reset_renderborder", text="Reset Render Border")
        row = layout.row()
        col = layout.column(align=True)
        rowsub = col.row(align=True)
        rowsub = row.split(align=True, percentage=0.3)
        rowsub.prop(scn.render, "use_crop_to_border", text="Crop Image")
        rowsub.alignment = 'RIGHT'
        rowsub.label('Width: {}px Height: {}px'.format(str(rbx.width), str(rbx.height)))

        
# ------------------------------------------------------------------------
# registration
# ------------------------------------------------------------------------

def register():
    bpy.utils.register_module(__name__)
    bpy.types.Scene.renderborder = bpy.props.PointerProperty(type=RenderBorder)

def unregister():
    bpy.utils.unregister_module(__name__)
    del bpy.types.Scene.renderborder

if __name__ == "__main__":
    register()
