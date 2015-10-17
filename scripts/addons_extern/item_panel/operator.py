
# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by the Free
#  Software Foundation; either version 2 of the License, or (at your option)
#  any later version.
#
#  This program is distributed in the hope that it will be useful, but WITHOUT
#  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#  FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#  more details.
#
#  You should have received a copy of the GNU General Public License along with
#  this program; if not, write to the Free Software Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# imports
import bpy
from bpy.types import Operator
from bpy.props import BoolProperty
from . import function

###############
## OPERATORS ##
###############

# batch
class batch:
  '''
  Contains Classes:
    auto
    name (Operator)
    copy (Operator)
    reset (Operator)
  '''

  # auto
  class auto:
    '''
      Constains Classes;
        name (Operator)
        objects (Operator)
        constraints (Operator)
        modifiers (Operator)
        objectData (Operator)
    '''

    # main
    class name(Operator):
      '''
        Automatically name datablocks based on type.
      '''
      bl_idname = 'view3d.batch_auto_name'
      bl_label = 'Auto Name'
      bl_description = 'Automatically name datablocks based on type.'
      bl_options = {'REGISTER', 'UNDO'}

      # poll
      @classmethod
      def poll(cls, context):
        '''
          Space data type must be in 3D view.
        '''
        return context.space_data.type in 'VIEW_3D'

      # draw
      def draw(self, context):
        '''
          Draw the operator panel/menu.
        '''

        # layout
        layout = self.layout

        # option
        option = context.screen.batchAutoNameSettings

        # batch type
        layout.prop(option, 'batchType', expand=True)

        # column
        column = layout.column(align=True)

        # type row
        split = column.split(align=True)
        split.prop(option, 'objects', text='', icon='OBJECT_DATA')
        split.prop(option, 'constraints', text='', icon='CONSTRAINT')
        split.prop(option, 'modifiers', text='', icon='MODIFIER')
        split.prop(option, 'objectData', text='', icon='MESH_DATA')
        split.prop(option, 'boneConstraints', text='', icon='CONSTRAINT_BONE')

        # type filters
        column = layout.column()
        column.prop(option, 'objectType', text='')
        column.prop(option, 'constraintType', text='')
        column.prop(option, 'modifierType', text='')

        # settings
        column = layout.column()
        column.label(text='Name Settings:')
        split = column.split(align=True)
        split.operator('view3d.batch_auto_name_object_names', text='Objects')
        split.operator('view3d.batch_auto_name_constraint_names', text='Constraints')
        split.operator('view3d.batch_auto_name_modifier_names', text='Modifiers')
        split.operator('view3d.batch_auto_name_object_data_names', text='Object Data')

      # execute
      def execute(self, context):
        '''
          Execute the operator.
        '''

        # auto
        function.batch.auto.main(context)
        return {'FINISHED'}

      # invoke
      def invoke(self, context, event):
        '''
          Invoke the operator panel/menu, control its width.
        '''
        context.window_manager.invoke_props_dialog(self, width=300)
        return {'RUNNING_MODAL'}

    # objects
    class objects(Operator):
      '''
        Invoke the auto name object names dialogue.
      '''
      bl_idname = 'view3d.batch_auto_name_object_names'
      bl_label = 'Object Names'
      bl_description = 'Change the names used for objects.'
      bl_options = {'REGISTER', 'UNDO'}

      # poll
      @classmethod
      def poll(cls, context):
        '''
          Space data type must be in 3D view.
        '''
        return context.space_data.type in 'VIEW_3D'

      # draw
      def draw(self, context):
        '''
          Draw the operator panel/menu.
        '''

        # layout
        layout = self.layout

        # option
        option = context.scene.batchAutoNameObjectNames

        # input fields

        # mesh
        column = layout.column()
        row = column.row()
        row.label(icon='OUTLINER_OB_MESH')
        row.prop(option, 'mesh', text='')

        # curve
        column = layout.column()
        row = column.row()
        row.label(icon='OUTLINER_OB_CURVE')
        row.prop(option, 'curve', text='')

        # surface
        column = layout.column()
        row = column.row()
        row.label(icon='OUTLINER_OB_SURFACE')
        row.prop(option, 'surface', text='')

        # meta
        column = layout.column()
        row = column.row()
        row.label(icon='OUTLINER_OB_META')
        row.prop(option, 'meta', text='')

        # font
        column = layout.column()
        row = column.row()
        row.label(icon='OUTLINER_OB_FONT')
        row.prop(option, 'font', text='')

        # armature
        column = layout.column()
        row = column.row()
        row.label(icon='OUTLINER_OB_ARMATURE')
        row.prop(option, 'armature', text='')

        # lattice
        column = layout.column()
        row = column.row()
        row.label(icon='OUTLINER_OB_LATTICE')
        row.prop(option, 'lattice', text='')

        # empty
        column = layout.column()
        row = column.row()
        row.label(icon='OUTLINER_OB_EMPTY')
        row.prop(option, 'empty', text='')

        # speaker
        column = layout.column()
        row = column.row()
        row.label(icon='OUTLINER_OB_SPEAKER')
        row.prop(option, 'speaker', text='')

        # camera
        column = layout.column()
        row = column.row()
        row.label(icon='OUTLINER_OB_CAMERA')
        row.prop(option, 'camera', text='')

        # lamp
        column = layout.column()
        row = column.row()
        row.label(icon='OUTLINER_OB_LAMP')
        row.prop(option, 'lamp', text='')

      # execute
      def execute(self, context):
        '''
          Execute the operator.
        '''
        # do nothing
        return {'FINISHED'}

      # invoke
      def invoke(self, context, event):
        '''
          Invoke the operator panel/menu, control its width.
        '''
        context.window_manager.invoke_props_dialog(self, width=150)
        return {'RUNNING_MODAL'}

    # constraints
    class constraints(Operator):
      '''
        Invoke the auto name constraint names dialogue.
      '''
      bl_idname = 'view3d.batch_auto_name_constraint_names'
      bl_label = 'Constraint Names'
      bl_description = 'Change the names used for constraints.'
      bl_options = {'REGISTER', 'UNDO'}

      # poll
      @classmethod
      def poll(cls, context):
        '''
          Space data type must be in 3D view.
        '''
        return context.space_data.type in 'VIEW_3D'

      # draw
      def draw(self, context):
        '''
          Draw the operator panel/menu.
        '''

        # layout
        layout = self.layout

        # option
        option = context.scene.batchAutoNameConstraintNames

        # input fields
        split = layout.split()

        # motion tracking
        column = split.column()
        column.label(text='Motion Tracking')

        # camera solver
        row = column.row()
        row.label(icon='CONSTRAINT_DATA')
        row.prop(option, 'cameraSolver', text='')

        # follow track
        row = column.row()
        row.label(icon='CONSTRAINT_DATA')
        row.prop(option, 'followTrack', text='')

        # object solver
        row = column.row()
        row.label(icon='CONSTRAINT_DATA')
        row.prop(option, 'objectSolver', text='')

        # transform
        column = split.column()
        column.label(text='Transform')

        # copy location
        row = column.row()
        row.label(icon='CONSTRAINT_DATA')
        row.prop(option, 'copyLocation', text='')

        # copy rotation
        row = column.row()
        row.label(icon='CONSTRAINT_DATA')
        row.prop(option, 'copyRotation', text='')

        # copy scale
        row = column.row()
        row.label(icon='CONSTRAINT_DATA')
        row.prop(option, 'copyScale', text='')

        # copy transforms
        row = column.row()
        row.label(icon='CONSTRAINT_DATA')
        row.prop(option, 'copyTransforms', text='')

        # limit distance
        row = column.row()
        row.label(icon='CONSTRAINT_DATA')
        row.prop(option, 'limitDistance', text='')

        # limit location
        row = column.row()
        row.label(icon='CONSTRAINT_DATA')
        row.prop(option, 'limitLocation', text='')

        # limit rotation
        row = column.row()
        row.label(icon='CONSTRAINT_DATA')
        row.prop(option, 'limitRotation', text='')

        # limit scale
        row = column.row()
        row.label(icon='CONSTRAINT_DATA')
        row.prop(option, 'limitScale', text='')

        # maintain volume
        row = column.row()
        row.label(icon='CONSTRAINT_DATA')
        row.prop(option, 'maintainVolume', text='')

        # transform
        row = column.row()
        row.label(icon='CONSTRAINT_DATA')
        row.prop(option, 'transform', text='')

        # tracking
        column = split.column()
        column.label(text='Tracking')

        # clamp to
        row = column.row()
        row.label(icon='CONSTRAINT_DATA')
        row.prop(option, 'clampTo', text='')

        # damped track
        row = column.row()
        row.label(icon='CONSTRAINT_DATA')
        row.prop(option, 'dampedTrack', text='')

        # inverse kinematics
        row = column.row()
        row.label(icon='CONSTRAINT_DATA')
        row.prop(option, 'inverseKinematics', text='')

        # locked track
        row = column.row()
        row.label(icon='CONSTRAINT_DATA')
        row.prop(option, 'lockedTrack', text='')

        # spline inverse kinematics
        row = column.row()
        row.label(icon='CONSTRAINT_DATA')
        row.prop(option, 'splineInverseKinematics', text='')

        # stretch to
        row = column.row()
        row.label(icon='CONSTRAINT_DATA')
        row.prop(option, 'stretchTo', text='')

        # track to
        row = column.row()
        row.label(icon='CONSTRAINT_DATA')
        row.prop(option, 'trackTo', text='')

        # relationship
        column = split.column()
        column.label(text='Relationship')

        # action
        row = column.row()
        row.label(icon='CONSTRAINT_DATA')
        row.prop(option, 'action', text='')

        # child of
        row = column.row()
        row.label(icon='CONSTRAINT_DATA')
        row.prop(option, 'childOf', text='')

        # floor
        row = column.row()
        row.label(icon='CONSTRAINT_DATA')
        row.prop(option, 'floor', text='')

        # follow path
        row = column.row()
        row.label(icon='CONSTRAINT_DATA')
        row.prop(option, 'followPath', text='')

        # pivot
        row = column.row()
        row.label(icon='CONSTRAINT_DATA')
        row.prop(option, 'pivot', text='')

        # rigid body joint
        row = column.row()
        row.label(icon='CONSTRAINT_DATA')
        row.prop(option, 'rigidBodyJoint', text='')

        # shrinkwrap
        row = column.row()
        row.label(icon='CONSTRAINT_DATA')
        row.prop(option, 'shrinkwrap', text='')

      # execute
      def execute(self, context):
        '''
          Execute the operator.
        '''
        # do nothing
        return {'FINISHED'}

      # invoke
      def invoke(self, context, event):
        '''
          Invoke the operator panel/menu, control its width.
        '''
        context.window_manager.invoke_props_dialog(self, width=600)
        return {'RUNNING_MODAL'}

    # modifiers
    class modifiers(Operator):
      '''
        Invoke the auto name modifier names dialogue.
      '''
      bl_idname = 'view3d.batch_auto_name_modifier_names'
      bl_label = 'Modifier Names'
      bl_description = 'Change the names used for modifiers.'
      bl_options = {'REGISTER', 'UNDO'}

      # poll
      @classmethod
      def poll(cls, context):
        '''
          Space data type must be in 3D view.
        '''
        return context.space_data.type in 'VIEW_3D'

      # draw
      def draw(self, context):
        '''
          Draw the operator panel/menu.
        '''

        # layout
        layout = self.layout

        # option
        option = context.scene.batchAutoNameModifierNames

        # input fields
        split = layout.split()

        # modify
        column = split.column()
        column.label(text='Modify')

        # data transfer
        row = column.row()
        row.label(icon='MOD_DATA_TRANSFER')
        row.prop(option, 'dataTransfer', text='')

        # mesh cache
        row = column.row()
        row.label(icon='MOD_MESHDEFORM')
        row.prop(option, 'meshCache', text='')

        # normal edit
        row = column.row()
        row.label(icon='MOD_NORMALEDIT')
        row.prop(option, 'normalEdit', text='')

        # uv project
        row = column.row()
        row.label(icon='MOD_UVPROJECT')
        row.prop(option, 'uvProject', text='')

        # uv warp
        row = column.row()
        row.label(icon='MOD_UVPROJECT')
        row.prop(option, 'uvWarp', text='')

        # vertex weight edit
        row = column.row()
        row.label(icon='MOD_VERTEX_WEIGHT')
        row.prop(option, 'vertexWeightEdit', text='')

        # vertex weight mix
        row = column.row()
        row.label(icon='MOD_VERTEX_WEIGHT')
        row.prop(option, 'vertexWeightMix', text='')

        # vertex weight proximity
        row = column.row()
        row.label(icon='MOD_VERTEX_WEIGHT')
        row.prop(option, 'vertexWeightProximity', text='')

        # generate
        column = split.column()
        column.label(text='Generate')

        # array
        row = column.row()
        row.label(icon='MOD_ARRAY')
        row.prop(option, 'array', text='')

        # bevel
        row = column.row()
        row.label(icon='MOD_BEVEL')
        row.prop(option, 'bevel', text='')

        # boolean
        row = column.row()
        row.label(icon='MOD_BOOLEAN')
        row.prop(option, 'boolean', text='')

        # build
        row = column.row()
        row.label(icon='MOD_BUILD')
        row.prop(option, 'build', text='')

        # decimate
        row = column.row()
        row.label(icon='MOD_DECIM')
        row.prop(option, 'decimate', text='')

        # edge split
        row = column.row()
        row.label(icon='MOD_EDGESPLIT')
        row.prop(option, 'edgeSplit', text='')

        # mask
        row = column.row()
        row.label(icon='MOD_MASK')
        row.prop(option, 'mask', text='')

        # mirror
        row = column.row()
        row.label(icon='MOD_MIRROR')
        row.prop(option, 'mirror', text='')

        # multiresolution
        row = column.row()
        row.label(icon='MOD_MULTIRES')
        row.prop(option, 'multiresolution', text='')

        # remesh
        row = column.row()
        row.label(icon='MOD_REMESH')
        row.prop(option, 'remesh', text='')

        # screw
        row = column.row()
        row.label(icon='MOD_SCREW')
        row.prop(option, 'screw', text='')

        # skin
        row = column.row()
        row.label(icon='MOD_SKIN')
        row.prop(option, 'skin', text='')

        # solidify
        row = column.row()
        row.label(icon='MOD_SOLIDIFY')
        row.prop(option, 'solidify', text='')

        # subdivision surface
        row = column.row()
        row.label(icon='MOD_SUBSURF')
        row.prop(option, 'subdivisionSurface', text='')

        # triangulate
        row = column.row()
        row.label(icon='MOD_TRIANGULATE')
        row.prop(option, 'triangulate', text='')

        # wireframe
        row = column.row()
        row.label(icon='MOD_WIREFRAME')
        row.prop(option, 'wireframe', text='')

        # deform
        column = split.column()
        column.label(text='Deform')

        # armature
        row = column.row()
        row.label(icon='MOD_ARMATURE')
        row.prop(option, 'armature', text='')

        # cast
        row = column.row()
        row.label(icon='MOD_CAST')
        row.prop(option, 'cast', text='')

        # corrective smooth
        row = column.row()
        row.label(icon='MOD_SMOOTH')
        row.prop(option, 'correctiveSmooth', text='')

        # curve
        row = column.row()
        row.label(icon='MOD_CURVE')
        row.prop(option, 'curve', text='')

        # displace
        row = column.row()
        row.label(icon='MOD_DISPLACE')
        row.prop(option, 'displace', text='')

        # hook
        row = column.row()
        row.label(icon='HOOK')
        row.prop(option, 'hook', text='')

        # laplacian smooth
        row = column.row()
        row.label(icon='MOD_SMOOTH')
        row.prop(option, 'laplacianSmooth', text='')

        # laplacian deform
        row = column.row()
        row.label(icon='MOD_MESHDEFORM')
        row.prop(option, 'laplacianDeform', text='')

        # lattice
        row = column.row()
        row.label(icon='MOD_LATTICE')
        row.prop(option, 'lattice', text='')

        # mesh deform
        row = column.row()
        row.label(icon='MOD_MESHDEFORM')
        row.prop(option, 'meshDeform', text='')

        # shrinkwrap
        row = column.row()
        row.label(icon='MOD_SHRINKWRAP')
        row.prop(option, 'shrinkwrap', text='')

        # simple deform
        row = column.row()
        row.label(icon='MOD_SIMPLEDEFORM')
        row.prop(option, 'simpleDeform', text='')

        # smooth
        row = column.row()
        row.label(icon='MOD_SMOOTH')
        row.prop(option, 'smooth', text='')

        # warp
        row = column.row()
        row.label(icon='MOD_WARP')
        row.prop(option, 'warp', text='')

        # wave
        row = column.row()
        row.label(icon='MOD_WAVE')
        row.prop(option, 'wave', text='')

        # simulate
        column = split.column()
        column.label(text='Simulate')

        # cloth
        row = column.row()
        row.label(icon='MOD_CLOTH')
        row.prop(option, 'cloth', text='')

        # collision
        row = column.row()
        row.label(icon='MOD_PHYSICS')
        row.prop(option, 'collision', text='')

        # dynamic paint
        row = column.row()
        row.label(icon='MOD_DYNAMICPAINT')
        row.prop(option, 'dynamicPaint', text='')

        # explode
        row = column.row()
        row.label(icon='MOD_EXPLODE')
        row.prop(option, 'explode', text='')

        # fluid simulation
        row = column.row()
        row.label(icon='MOD_FLUIDSIM')
        row.prop(option, 'fluidSimulation', text='')

        # ocean
        row = column.row()
        row.label(icon='MOD_OCEAN')
        row.prop(option, 'ocean', text='')

        # particle instance
        row = column.row()
        row.label(icon='MOD_PARTICLES')
        row.prop(option, 'particleInstance', text='')

        # particle system
        row = column.row()
        row.label(icon='MOD_PARTICLES')
        row.prop(option, 'particleSystem', text='')

        # smoke
        row = column.row()
        row.label(icon='MOD_SMOKE')
        row.prop(option, 'smoke', text='')

        # soft body
        row = column.row()
        row.label(icon='MOD_SOFT')
        row.prop(option, 'softBody', text='')

      # execute
      def execute(self, context):
        '''
          Execute the operator.
        '''
        # do nothing
        return {'FINISHED'}

      # invoke
      def invoke(self, context, event):
        '''
          Invoke the operator panel/menu, control its width.
        '''
        context.window_manager.invoke_props_dialog(self, width=600)
        return {'RUNNING_MODAL'}

    # objects
    class objectData(Operator):
      '''
        Invoke the auto name object data names dialogue.
      '''
      bl_idname = 'view3d.batch_auto_name_object_data_names'
      bl_label = 'Object Data Names'
      bl_description = 'Change the names used for objects data.'
      bl_options = {'REGISTER', 'UNDO'}

      # poll
      @classmethod
      def poll(cls, context):
        '''
          Space data type must be in 3D view.
        '''
        return context.space_data.type in 'VIEW_3D'

      # draw
      def draw(self, context):
        '''
          Draw the operator panel/menu.
        '''

        # layout
        layout = self.layout

        # option
        option = context.scene.batchAutoNameObjectDataNames

        # input fields

        # mesh
        column = layout.column()
        row = column.row()
        row.label(icon='MESH_DATA')
        row.prop(option, 'mesh', text='')

        # curve
        column = layout.column()
        row = column.row()
        row.label(icon='CURVE_DATA')
        row.prop(option, 'curve', text='')

        # surface
        column = layout.column()
        row = column.row()
        row.label(icon='SURFACE_DATA')
        row.prop(option, 'surface', text='')

        # meta
        column = layout.column()
        row = column.row()
        row.label(icon='META_DATA')
        row.prop(option, 'meta', text='')

        # font
        column = layout.column()
        row = column.row()
        row.label(icon='FONT_DATA')
        row.prop(option, 'font', text='')

        # armature
        column = layout.column()
        row = column.row()
        row.label(icon='ARMATURE_DATA')
        row.prop(option, 'armature', text='')

        # lattice
        column = layout.column()
        row = column.row()
        row.label(icon='LATTICE_DATA')
        row.prop(option, 'lattice', text='')

        # speaker
        column = layout.column()
        row = column.row()
        row.label(icon='SPEAKER')
        row.prop(option, 'speaker', text='')

        # camera
        column = layout.column()
        row = column.row()
        row.label(icon='CAMERA_DATA')
        row.prop(option, 'camera', text='')

        # lamp
        column = layout.column()
        row = column.row()
        row.label(icon='LAMP_DATA')
        row.prop(option, 'lamp', text='')

      # execute
      def execute(self, context):
        '''
          Execute the operator.
        '''
        # do nothing
        return {'FINISHED'}

      # invoke
      def invoke(self, context, event):
        '''
          Invoke the operator panel/menu, control its width.
        '''
        context.window_manager.invoke_props_dialog(self, width=150)
        return {'RUNNING_MODAL'}

  # name
  class name(Operator):
    '''
      Batch name datablocks.
    '''
    bl_idname = 'wm.batch_name'
    bl_label = 'Batch Name'
    bl_description = 'Batch name datablocks.'
    bl_options = {'REGISTER', 'UNDO'}

    # draw
    def draw(self, context):
      '''
        Operator body.
      '''

      # layout
      layout = self.layout

      # option
      option = context.screen.batchNameSettings

      # batch type
      layout.prop(option, 'batchType', expand=True)

      # column
      column = layout.column(align=True)

      # object datablocks

      # row 1
      row = column.row(align=True)
      row.scale_x = 5 # hack: forces buttons to line up correctly
      row.prop(option, 'objects', text='', icon='OBJECT_DATA')
      row.prop(option, 'groups', text='', icon='GROUP')
      row.prop(option, 'actions', text='', icon='ACTION')
      row.prop(option, 'greasePencil', text='', icon='GREASEPENCIL')
      row.prop(option, 'constraints', text='', icon='CONSTRAINT')
      row.prop(option, 'modifiers', text='', icon='MODIFIER')
      row.prop(option, 'objectData', text='', icon='MESH_DATA')
      row.prop(option, 'boneGroups', text='', icon='GROUP_BONE')
      row.prop(option, 'bones', text='', icon='BONE_DATA')
      row.prop(option, 'boneConstraints', text='', icon='CONSTRAINT_BONE')

      # row 2
      row = column.row(align=True)
      row.scale_x = 5 # hack: forces buttons to line up correctly
      row.prop(option, 'vertexGroups', text='', icon='GROUP_VERTEX')
      row.prop(option, 'shapekeys', text='', icon='SHAPEKEY_DATA')
      row.prop(option, 'uvs', text='', icon='GROUP_UVS')
      row.prop(option, 'vertexColors', text='', icon='GROUP_VCOL')
      row.prop(option, 'materials', text='', icon='MATERIAL')
      row.prop(option, 'textures', text='', icon='TEXTURE')
      row.prop(option, 'particleSystems', text='', icon='PARTICLES')
      row.prop(option, 'particleSettings', text='', icon='MOD_PARTICLES')

      # type filters
      column = layout.column()
      column.prop(option, 'objectType', text='')
      column.prop(option, 'constraintType', text='')
      column.prop(option, 'modifierType', text='')

      # global datablocks

      # column
      column = layout.column(align=True)

      # row 1
      row = column.row(align=True)
      row.scale_x = 5 # hack: forces buttons to line up correctly
      row.prop(option, 'scenes', text='', icon='SCENE_DATA')
      row.prop(option, 'renderLayers', text='', icon='RENDERLAYERS')
      row.prop(option, 'worlds', text='', icon='WORLD')
      row.prop(option, 'libraries', text='', icon='LIBRARY_DATA_DIRECT')
      row.prop(option, 'images', text='', icon='IMAGE_DATA')
      row.prop(option, 'masks', text='', icon='MOD_MASK')
      row.prop(option, 'sequences', text='', icon='SEQUENCE')
      row.prop(option, 'movieClips', text='', icon='CLIP')
      row.prop(option, 'sounds', text='', icon='SOUND')

      # row 2
      row = column.row(align=True)
      row.scale_x = 5 # hack: forces buttons to line up correctly
      row.prop(option, 'screens', text='', icon='SPLITSCREEN')
      row.prop(option, 'keyingSets', text='', icon='KEYINGSET')
      row.prop(option, 'palettes', text='', icon='COLOR')
      row.prop(option, 'brushes', text='', icon='BRUSH_DATA')
      row.prop(option, 'linestyles', text='', icon='LINE_DATA')
      row.prop(option, 'nodes', text='', icon='NODE_SEL')
      row.prop(option, 'nodeLabels', text='', icon='NODE')
      row.prop(option, 'nodeGroups', text='', icon='NODETREE')
      row.prop(option, 'texts', text='', icon='TEXT')

      # row
      row = column.row()
      row.separator()

      # input fields

      # custom name
      column.prop(option, 'customName')
      column.separator()

      # find
      row = column.row(align=True)
      row.prop(option, 'find', icon='VIEWZOOM')

      # regex
      row.prop(option, 'regex', text='', icon='SCRIPT')
      column.separator()

      # replace
      column.prop(option, 'replace', icon='FILE_REFRESH')
      column.separator()

      # prefix
      column.prop(option, 'prefix', icon='LOOP_BACK')
      column.separator()

      # suffix
      column.prop(option, 'suffix', icon='LOOP_FORWARDS')
      column.separator()
      row = column.row()

      # trim start
      row.label(text='Trim Start:')
      row.prop(option, 'trimStart', text='')
      column.separator()
      row = column.row()

      # trim end
      row.label(text='Trim End:')
      row.prop(option, 'trimEnd', text='')

    # execute
    def execute(self, context):
      '''
        Execute the operator.
      '''

      # name
      function.batch.main(context)
      return {'FINISHED'}

    # invoke
    def invoke(self, context, event):
      '''
        Invoke the operator panel/menu, control its width.
      '''
      context.window_manager.invoke_props_dialog(self, width=300)
      return {'RUNNING_MODAL'}

  # batch copy
  class copy(Operator):
    '''
      Transfer names from some types of datablocks to others.
    '''
    bl_idname = 'view3d.batch_copy'
    bl_label = 'Batch Name Copy'
    bl_description = 'Copy names from some types of datablocks to others.'
    bl_options = {'REGISTER', 'UNDO'}

    # poll
    @classmethod
    def poll(cls, context):
      '''
        Space data type must be in 3D view.
      '''
      return context.space_data.type in 'VIEW_3D'

    # draw
    def draw(self, context):
      '''
        Draw the operator panel/menu.
      '''

      # layout
      layout = self.layout

      # option
      option = context.screen.batchCopySettings

      # batch type
      layout.prop(option, 'batchType', expand=True)

      # column
      column = layout.column(align=True)

      # source
      column.label(text='Copy:', icon='COPYDOWN')
      column = layout.column(align=True)
      column.prop(option, 'source', expand=True)
      column = layout.column(align=True)

      # targets
      column.label(text='Paste:', icon='PASTEDOWN')
      column = layout.column(align=True)
      split = column.split(align=True)
      split.prop(option, 'objects', text='', icon='OBJECT_DATA')
      split.prop(option, 'objectData', text='', icon='MESH_DATA')
      split.prop(option, 'materials', text='', icon='MATERIAL')
      split.prop(option, 'textures', text='', icon='TEXTURE')
      split.prop(option, 'particleSystems', text='', icon='PARTICLES')
      split.prop(option, 'particleSettings', text='', icon='MOD_PARTICLES')

      # use active object
      column = layout.column()
      column.prop(option, 'useActiveObject')

    # execute
    def execute(self, context):
      '''
        Execute the operator.
      '''

      # copy
      function.batch.copy(context)
      return {'FINISHED'}

    # invoke
    def invoke(self, context, event):
      '''
        Invoke the operator panel/menu, control its width.
      '''
      context.window_manager.invoke_props_dialog(self, width=150)
      return {'RUNNING_MODAL'}

  # reset
  class resetSettings(Operator):
    '''
      Reset batch operator properties.
    '''
    bl_idname = 'view3d.batch_reset_settings'
    bl_label = 'Reset Settings'
    bl_description = 'Reset batch operator options to their default values.'
    bl_options = {'REGISTER', 'UNDO'}

    # auto
    auto = BoolProperty(
      name = 'Batch Auto Name',
      description = 'Reset the option values for batch auto name.',
      default = True
    )

    # names
    names = BoolProperty(
      name = 'Batch Auto Name → Name Settings',
      description = 'Reset the option values for batch auto name → name settings.',
      default = False
    )

    # name
    name = BoolProperty(
      name = 'Batch Name',
      description = 'Reset the option values for batch name.',
      default = True
    )

    # copy
    copy = BoolProperty(
      name = 'Batch Copy Name',
      description = 'Reset the option values for batch copy name.',
      default = True
    )

    # poll
    @classmethod
    def poll(cls, context):
      '''
        Space data type must be in 3D view.
      '''
      return context.space_data.type in 'VIEW_3D'

    # draw
    def draw(self, context):
      '''
        Draw the operator panel/menu.
      '''

      # layout
      layout = self.layout

      # column
      column = layout.column()

      # options
      column.prop(self, 'auto')
      column.prop(self, 'names')
      column.prop(self, 'name')
      column.prop(self, 'copy')

    # execute
    def execute(self, context):
      '''
        Execute the operator.
      '''

      # reset
      function.batch.resetSettings(context, self.auto, self.names, self.name, self.copy)
      return {'FINISHED'}

  # transfer
  class transferSettings(Operator):
    '''
      Transfer batch operator property values.
    '''
    bl_idname = 'view3d.batch_transfer_settings'
    bl_label = 'Transfer Settings'
    bl_description = 'Transfer current batch operator option values to other screens and scenes.'
    bl_options = {'REGISTER', 'UNDO'}

    # auto
    auto = BoolProperty(
      name = 'Batch Auto Name',
      description = 'Transfer the option values for batch auto name.',
      default = True
    )

    # names
    names = BoolProperty(
      name = 'Batch Auto Name → Name Settings',
      description = 'Transfer the option values for batch auto name → name settings.',
      default = True
    )

    # name
    name = BoolProperty(
      name = 'Batch Name',
      description = 'Transfer the option values for batch name.',
      default = True
    )

    # copy
    copy = BoolProperty(
      name = 'Batch Copy Name',
      description = 'Transfer the option values for batch copy name.',
      default = True
    )

    # poll
    @classmethod
    def poll(cls, context):
      '''
        Space data type must be in 3D view.
      '''
      return context.space_data.type in 'VIEW_3D'

    # draw
    def draw(self, context):
      '''
        Draw the operator panel/menu.
      '''

      # layout
      layout = self.layout

      # column
      column = layout.column()

      # options
      column.prop(self, 'auto')
      column.prop(self, 'names')
      column.prop(self, 'name')
      column.prop(self, 'copy')

    # execute
    def execute(self, context):
      '''
        Execute the operator.
      '''

      # reset
      function.batch.transferSettings(context, self.auto, self.names, self.name, self.copy)
      return {'FINISHED'}
