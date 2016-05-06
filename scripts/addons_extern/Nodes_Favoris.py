# ##### BEGIN GPL LICENSE BLOCK ###############################################
#                                                                             #
#  This program is free software; you can redistribute it and/or              #
#  modify it under the terms of the GNU General Public License                #
#  as published by the Free Software Foundation; either version 2             #
#  of the License, or (at your option) any later version.                     #
#                                                                             #
#  This program is distributed in the hope that it will be useful,            #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of             #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the              #
#  GNU General Public License for more details.                               #
#                                                                             #
#  You should have received a copy of the GNU General Public License          #
#  along with this program; if not, write to the Free Software Foundation,    #
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.         #
#                                                                             #
# ##### END GPL LICENSE BLOCK #################################################


bl_info = {
    "name": "Nodes Favoris",
    "description": "",
    "author": "Cédric Lepiller",
    "version": (0, 0, 2),
    "blender": (2, 76, 0),
    "location": "NODE_EDITOR",
    "warning": "",
    "wiki_url": "",
    "category": "Node"}

import bpy

bpy.types.Scene.fav_input = bpy.props.BoolProperty(default=True)
bpy.types.Scene.fav_shaders = bpy.props.BoolProperty(default=True)
bpy.types.Scene.fav_Textures = bpy.props.BoolProperty(default=True)
bpy.types.Scene.fav_Color = bpy.props.BoolProperty(default=True)
bpy.types.Scene.fav_vector = bpy.props.BoolProperty(default=True)
bpy.types.Scene.fav_converter = bpy.props.BoolProperty(default=True)
bpy.types.Scene.fav_layout = bpy.props.BoolProperty(default=True)
bpy.types.Scene.fav_script = bpy.props.BoolProperty(default=True)
bpy.types.Scene.fav_output = bpy.props.BoolProperty(default=True)

############### Prefs ########################

# Class Prefs


class NodesFavorisPrefs(bpy.types.AddonPreferences):
    """Creates the tools in a Panel, in the scene context of the properties editor"""
    bl_idname = __name__

    bpy.types.Scene.Enable_Tab_01 = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.Enable_Tab_02 = bpy.props.BoolProperty(default=False)

    def draw(self, context):
        layout = self.layout

        layout.prop(context.scene, "Enable_Tab_01", text="Info", icon="QUESTION")
        if context.scene.Enable_Tab_01:
            row = layout.row()
            layout.label(text="This Addon add a Tab in the Node Editor to select nodes.")

        layout.prop(context.scene, "Enable_Tab_02", text="URL's", icon="URL")
        if context.scene.Enable_Tab_02:
            row = layout.row()
            row.operator("wm.url_open", text="Pitiwazou.com").url = "http://www.pitiwazou.com/"
            row.operator("wm.url_open", text="Wazou's Ghitub").url = "https://github.com/pitiwazou/Scripts-Blender"
            row.operator("wm.url_open", text="BlenderLounge Forum ").url = "http://blenderlounge.fr/forum/"


class NodesFavoris(bpy.types.Panel):
    bl_idname = "nodes_favoris"
    bl_label = "Favoris"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "TOOLS"
    bl_category = "Favoris"

    def draw(self, context):
        layout = self.layout

        # Input
        if context.scene.fav_input == False:
            row = layout.row(align=True)
            row.prop(context.scene, "fav_input", text="Input", icon='ZOOMOUT')
            row.label("", icon='NODETREE')

            layout.operator("node.add_node", text="Texture Coordinate").type = "ShaderNodeTexCoord"
            layout.operator("node.add_node", text="Mapping").type = "ShaderNodeMapping"
            layout.operator("node.add_node", text="Attribute").type = "ShaderNodeAttribute"
            layout.operator("node.add_node", text="Light Path").type = "ShaderNodeLightPath"
            layout.operator("node.add_node", text="Fresnel").type = "ShaderNodeFresnel"
            layout.operator("node.add_node", text="Layer Weight").type = "ShaderNodeLayerWeight"
            layout.operator("node.add_node", text="RGB").type = "ShaderNodeRGB"
            layout.operator("node.add_node", text="Value").type = "ShaderNodeValue"
            layout.operator("node.add_node", text="Tangent").type = "ShaderNodeTangent"
            layout.operator("node.add_node", text="Geometry").type = "ShaderNodeNewGeometry"
            layout.operator("node.add_node", text="Wireframe").type = "ShaderNodeWireframe"
            layout.operator("node.add_node", text="Object Info").type = "ShaderNodeObjectInfo"
            layout.operator("node.add_node", text="Hair Info").type = "ShaderNodeHairInfo"
            layout.operator("node.add_node", text="Particle Info").type = "ShaderNodeParticleInfo"
            layout.operator("node.add_node", text="Camera Data").type = "ShaderNodeCameraData"
            layout.operator("node.add_node", text="UV Map").type = "ShaderNodeUVMap"
        else:
            row = layout.row(align=True)
            row.prop(context.scene, "fav_input", text="Input", icon='ZOOMIN')
            row.label("", icon='NODETREE')

            row = layout.row(align=True)
            row.operator("node.add_node", text="Text Co").type = "ShaderNodeTexCoord"
            row.operator("node.add_node", text="Mapping").type = "ShaderNodeMapping"
            row = layout.row(align=True)
            row.operator("node.add_node", text="Fresnel").type = "ShaderNodeFresnel"
            row.operator("node.add_node", text="Layer Weight").type = "ShaderNodeLayerWeight"
            layout.operator("node.add_node", text="RGB").type = "ShaderNodeRGB"

        # Shaders
        if context.scene.fav_shaders == False:
            row = layout.row(align=True)
            row.prop(context.scene, "fav_shaders", text="Shaders", icon='ZOOMOUT')
            row.label("", icon='MATERIAL')

            layout.operator("node.add_node", text="Mix shader").type = "ShaderNodeMixShader"
            layout.operator("node.add_node", text="Add Shader").type = "ShaderNodeAddShader"
            layout.operator("node.add_node", text="Diffuse").type = "ShaderNodeBsdfDiffuse"
            layout.operator("node.add_node", text="Glossy").type = "ShaderNodeBsdfGlossy"
            layout.operator("node.add_node", text="Transparent").type = "ShaderNodeBsdfTransparent"
            layout.operator("node.add_node", text="Refraction").type = "ShaderNodeBsdfRefraction"
            layout.operator("node.add_node", text="Glass").type = "ShaderNodeBsdfGlass"
            layout.operator("node.add_node", text="Translucent").type = "ShaderNodeBsdfTranslucent"
            layout.operator("node.add_node", text="Anisotropic").type = "ShaderNodeBsdfAnisotropic"
            layout.operator("node.add_node", text="Velvet").type = "ShaderNodeBsdfVelvet"
            layout.operator("node.add_node", text="Toon").type = "ShaderNodeBsdfToon"
            layout.operator("node.add_node", text="SSS").type = "ShaderNodeSubsurfaceScattering"
            layout.operator("node.add_node", text="Emission").type = "ShaderNodeEmission"
            layout.operator("node.add_node", text="Hair").type = "ShaderNodeBsdfHair"
            layout.operator("node.add_node", text="Ambient Occlusion").type = "ShaderNodeAmbientOcclusion"
            layout.operator("node.add_node", text="Holdout").type = "ShaderNodeHoldout"
            layout.operator("node.add_node", text="VolumeAbsorption").type = "ShaderNodeVolumeAbsorption"
            layout.operator("node.add_node", text="Volume Scatter").type = "ShaderNodeVolumeScatter"

        else:
            row = layout.row(align=True)
            row.prop(context.scene, "fav_shaders", text="Shaders", icon='ZOOMIN')
            row.label("", icon='MATERIAL')

            layout.operator("node.add_node", text="Mix shader").type = "ShaderNodeMixShader"
            row = layout.row(align=True)
            row.operator("node.add_node", text="Diffuse").type = "ShaderNodeBsdfDiffuse"
            row.operator("node.add_node", text="Glossy").type = "ShaderNodeBsdfGlossy"
            row = layout.row(align=True)
            row.operator("node.add_node", text="Transparent").type = "ShaderNodeBsdfTransparent"
            row.operator("node.add_node", text="Glass").type = "ShaderNodeBsdfGlass"
            row = layout.row(align=True)
            row.operator("node.add_node", text="Translucent").type = "ShaderNodeBsdfTranslucent"
            row.operator("node.add_node", text="SSS").type = "ShaderNodeSubsurfaceScattering"
            row = layout.row(align=True)
            row.operator("node.add_node", text="Velvet").type = "ShaderNodeBsdfVelvet"
            row.operator("node.add_node", text="Emission").type = "ShaderNodeEmission"

        # Textures
        if context.scene.fav_Textures == False:
            row = layout.row(align=True)
            row.prop(context.scene, "fav_Textures", text="Textures", icon='ZOOMOUT')
            row.label("", icon='TEXTURE')

            layout.operator("node.nw_add_multiple_images", text="Multiple Images")
            layout.operator("node.nw_add_sequence", text="Image Sequence")
            layout.separator()
            layout.operator("node.add_node", text="Image Texture").type = "ShaderNodeTexImage"
            layout.operator("node.add_node", text="Environment").type = "ShaderNodeTexEnvironment"
            layout.operator("node.add_node", text="Sky").type = "ShaderNodeTexSky"
            layout.operator("node.add_node", text="Noise").type = "ShaderNodeTexNoise"
            layout.operator("node.add_node", text="Wave").type = "ShaderNodeTexWave"
            layout.operator("node.add_node", text="Voronoi").type = "ShaderNodeTexVoronoi"
            layout.operator("node.add_node", text="Musgrave").type = "ShaderNodeTexMusgrave"
            layout.operator("node.add_node", text="Gradient").type = "ShaderNodeTexGradient"
            layout.operator("node.add_node", text="Gradient").type = "ShaderNodeTexGradient"
            layout.operator("node.add_node", text="Magic").type = "ShaderNodeTexMagic"
            layout.operator("node.add_node", text="Checker").type = "ShaderNodeTexChecker"
            layout.operator("node.add_node", text="Brick").type = "ShaderNodeTexBrick"
            layout.operator("node.add_node", text="Point Density").type = "ShaderNodeTexPointDensity"
        else:
            row = layout.row(align=True)
            row.prop(context.scene, "fav_Textures", text="Textures", icon='ZOOMIN')
            row.label("", icon='TEXTURE')

            layout.operator("node.add_node", text="Image Texture").type = "ShaderNodeTexImage"
            row = layout.row(align=True)
            row.operator("node.add_node", text="Noise").type = "ShaderNodeTexNoise"
            row.operator("node.add_node", text="Voronoi").type = "ShaderNodeTexVoronoi"
            row = layout.row(align=True)
            row.operator("node.add_node", text="Musgrave").type = "ShaderNodeTexMusgrave"
            row.operator("node.add_node", text="Gradient").type = "ShaderNodeTexGradient"
            row = layout.row(align=True)
            row.operator("node.add_node", text="Magic").type = "ShaderNodeTexMagic"
            row.operator("node.add_node", text="Checker").type = "ShaderNodeTexChecker"
            row = layout.row(align=True)
            row.operator("node.add_node", text="Brick").type = "ShaderNodeTexBrick"
            row.operator("node.add_node", text="Wave").type = "ShaderNodeTexWave"

        # Color
        row = layout.row(align=True)
        if context.scene.fav_Color == False:
            row.prop(context.scene, "fav_Color", text="Color", icon='ZOOMOUT')
            row.label("", icon='COLOR_RED')

            layout.operator("node.add_node", text="Mix RGB").type = "ShaderNodeMixRGB"
            layout.operator("node.add_node", text="RGB Curves").type = "ShaderNodeRGBCurve"
            layout.operator("node.add_node", text="Invert").type = "ShaderNodeInvert"
            layout.operator("node.add_node", text="Light Falloff").type = "ShaderNodeLightFalloff"
            layout.operator("node.add_node", text="Hue/Saturation").type = "ShaderNodeHueSaturation"
            layout.operator("node.add_node", text="Gamma").type = "ShaderNodeGamma"
            layout.operator("node.add_node", text="Bright Contrast").type = "ShaderNodeBrightContrast"

        else:
            row = layout.row(align=True)
            row.prop(context.scene, "fav_Color", text="Color", icon='ZOOMIN')
            row.label("", icon='COLOR_RED')

            row = layout.row(align=True)
            row.operator("node.add_node", text="Mix RGB").type = "ShaderNodeMixRGB"
            row.operator("node.add_node", text="RGB Curves").type = "ShaderNodeRGBCurve"
            row = layout.row(align=True)
            row.operator("node.add_node", text="Invert").type = "ShaderNodeInvert"
            row.operator("node.add_node", text="Light Falloff").type = "ShaderNodeLightFalloff"
            row = layout.row(align=True)
            row.operator("node.add_node", text="Hue/Sat").type = "ShaderNodeHueSaturation"
            row.operator("node.add_node", text="Gamma").type = "ShaderNodeGamma"
            layout.operator("node.add_node", text="Bright Contrast").type = "ShaderNodeBrightContrast"

        # Vector
        if context.scene.fav_vector == False:
            row = layout.row(align=True)
            row.prop(context.scene, "fav_vector", text="Vector", icon='ZOOMOUT')
            row.label("", icon='RNDCURVE')

            layout.operator("node.add_node", text="Bump").type = "ShaderNodeBump"
            layout.operator("node.add_node", text="NormalMap").type = "ShaderNodeNormalMap"
            layout.operator("node.add_node", text="Normal").type = "ShaderNodeNormal"
            layout.operator("node.add_node", text="Vector Curves").type = "ShaderNodeVectorCurve"
            layout.operator("node.add_node", text="Vector Transform").type = "ShaderNodeVectorTransform"
        else:
            row = layout.row(align=True)
            row.prop(context.scene, "fav_vector", text="Vector", icon='ZOOMIN')
            row.label("", icon='RNDCURVE')

            layout.operator("node.add_node", text="Bump").type = "ShaderNodeBump"
            layout.operator("node.add_node", text="NormalMap").type = "ShaderNodeNormalMap"

        # Converter
        if context.scene.fav_converter == False:
            row = layout.row(align=True)
            row.prop(context.scene, "fav_converter", text="Converter", icon='ZOOMOUT')
            row.label("", icon='RNA')

            layout.operator("node.add_node", text="Math").type = "ShaderNodeMath"
            layout.operator("node.add_node", text="Color Ramp").type = "ShaderNodeValToRGB"
            layout.operator("node.add_node", text="RGB To BW").type = "ShaderNodeRGBToBW"
            layout.operator("node.add_node", text="Vector Math").type = "ShaderNodeVectorMath"
            layout.operator("node.add_node", text="Separate RGB").type = "ShaderNodeSeparateRGB"
            layout.operator("node.add_node", text="Combine RGB").type = "ShaderNodeCombineRGB"
            layout.operator("node.add_node", text="Separate XYZ").type = "ShaderNodeSeparateXYZ"
            layout.operator("node.add_node", text="Combine XYZ").type = "ShaderNodeCombineXYZ"
            layout.operator("node.add_node", text="Separate HSV").type = "ShaderNodeSeparateHSV"
            layout.operator("node.add_node", text="Combine HSV").type = "ShaderNodeCombineHSV"
            layout.operator("node.add_node", text="Wavelength").type = "ShaderNodeWavelength"
            layout.operator("node.add_node", text="Blackbody").type = "ShaderNodeBlackbody"

        else:
            row = layout.row(align=True)
            row.prop(context.scene, "fav_converter", text="Converter", icon='ZOOMIN')
            row.label("", icon='RNA')

            row = layout.row(align=True)
            row.operator("node.add_node", text="Math").type = "ShaderNodeMath"
            row.operator("node.add_node", text="Color Ramp").type = "ShaderNodeValToRGB"
            row = layout.row(align=True)
            row.operator("node.add_node", text="RGB To BW").type = "ShaderNodeRGBToBW"
            row.operator("node.add_node", text="Separate RGB").type = "ShaderNodeSeparateRGB"

        # Layout
        if context.scene.fav_layout == False:
            row = layout.row(align=True)
            row.prop(context.scene, "fav_layout", text="Layout", icon='ZOOMOUT')
            row.label("", icon='SPLITSCREEN')

            layout.operator("node.add_node", text="Frame").type = "NodeFrame"
            layout.operator("node.add_node", text="Reroute").type = "NodeReroute"

        else:
            row = layout.row(align=True)
            row.prop(context.scene, "fav_layout", text="Layout", icon='ZOOMIN')
            row.label("", icon='SPLITSCREEN')

        # Script
        if context.scene.fav_script == False:
            row = layout.row(align=True)
            row.prop(context.scene, "fav_script", text="Script", icon='ZOOMOUT')
            row.label("", icon='TEXT')

            layout.operator("node.add_node", text="Script").type = "ShaderNodeScript"

        else:
            row = layout.row(align=True)
            row.prop(context.scene, "fav_script", text="Script", icon='ZOOMIN')
            row.label("", icon='TEXT')

        # Output
        if context.scene.fav_output == False:
            row = layout.row(align=True)
            row.prop(context.scene, "fav_output", text="Output", icon='ZOOMOUT')
            row.label("", icon='NODETREE')

            layout.operator("node.add_node", text="Material Output").type = "ShaderNodeOutputMaterial"
            layout.operator("node.add_node", text="Lamp Output").type = "ShaderNodeOutputLamp"

        else:
            row = layout.row(align=True)
            row.prop(context.scene, "fav_output", text="Output", icon='ZOOMIN')
            row.label("", icon='NODETREE')


def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
