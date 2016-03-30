import bpy
from bpy.props import *
from ... events import propertyChanged
from ... base_types.node import AnimationNode
from ... algorithms.mesh_generation.from_splines import revolveProfileAroundAxis

projectionTypeItems = [
    ("PARAMETER", "Same Parameter", ""),
    ("PROJECT", "Project", "") ]

class RevolveSplineNode(bpy.types.Node, AnimationNode):
    bl_idname = "an_RevolveSplineNode"
    bl_label = "Revolve Spline"

    projectionType = EnumProperty(name = "Projection Type", default = "PROJECT", items = projectionTypeItems, update = propertyChanged)

    def create(self):
        self.inputs.new("an_SplineSocket", "Axis", "axis")
        self.inputs.new("an_SplineSocket", "Profile", "profile")
        socket = self.inputs.new("an_IntegerSocket", "Spline Samples", "splineSamples")
        socket.minValue = 2
        socket.value = 16
        socket = self.inputs.new("an_IntegerSocket", "Surface Samples", "surfaceSamples")
        socket.minValue = 3
        socket.value = 16
        self.outputs.new("an_VectorListSocket", "Vertices", "vertices")
        self.outputs.new("an_PolygonIndicesListSocket", "Polygons", "polygons")
        self.width += 20

    def draw(self, layout):
        layout.prop(self, "projectionType", text = "")

    def execute(self, axis, profile, splineSamples, surfaceSamples):
        def canExecute():
            if not axis.isEvaluable: return False
            if not profile.isEvaluable: return False
            if splineSamples < 2: return False
            if surfaceSamples < 3: return False
            return True

        axis.update()
        profile.update()

        if canExecute():
            vertices, polygons = revolveProfileAroundAxis(axis, profile, splineSamples, surfaceSamples, self.projectionType)
            return vertices, polygons
        else: return [], []
