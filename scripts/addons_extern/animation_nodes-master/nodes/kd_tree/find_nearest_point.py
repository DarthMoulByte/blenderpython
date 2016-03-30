import bpy
from mathutils import Vector
from ... base_types.node import AnimationNode

class FindNearestPointInKDTreeNode(bpy.types.Node, AnimationNode):
    bl_idname = "an_FindNearestPointInKDTreeNode"
    bl_label = "Find Nearest Point"

    def create(self):
        self.inputs.new("an_KDTreeSocket", "KDTree", "kdTree")
        self.inputs.new("an_VectorSocket", "Vector", "searchVector").defaultDrawType = "PROPERTY_ONLY"
        self.outputs.new("an_VectorSocket", "Vector", "nearestVector")
        self.outputs.new("an_FloatSocket", "Distance", "distance")
        self.outputs.new("an_IntegerSocket", "Index", "index")

    def getExecutionCode(self):
        yield "nearestVector, index, distance = kdTree.find(searchVector)"
        yield "if nearestVector is None:"
        yield "    nearestVector, index, distance = mathutils.Vector((0, 0, 0)), 0.0, -1"

    def getUsedModules(self):
        return ["mathutils"]
