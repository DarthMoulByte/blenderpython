import bpy
from ... base_types.node import AnimationNode
from . spline_evaluation_base import SplineEvaluationBase

class GetSplineLengthNode(bpy.types.Node, AnimationNode, SplineEvaluationBase):
    bl_idname = "an_GetSplineLengthNode"
    bl_label = "Get Spline Length"

    def create(self):
        self.inputs.new("an_SplineSocket", "Spline", "spline").defaultDrawType = "PROPERTY_ONLY"
        socket = self.inputs.new("an_FloatSocket", "Start", "start")
        socket.minValue = 0
        socket = self.inputs.new("an_FloatSocket", "End", "end")
        socket.minValue = 0
        socket.value = 1.0
        self.outputs.new("an_FloatSocket", "Length", "length")

    def draw(self, layout):
        layout.prop(self, "parameterType", text = "")

    def drawAdvanced(self, layout):
        col = layout.column()
        col.active = self.parameterType == "UNIFORM"
        col.prop(self, "resolution")

    def execute(self, spline, start, end):
        spline.update()
        if spline.isEvaluable:
            if start == 0 and end == 1:
                # to get a more exact result on polysplines currently
                return spline.getLength(self.resolution)

            if self.parameterType == "UNIFORM":
                spline.ensureUniformConverter(self.resolution)
                start = spline.toUniformParameter(start)
                end = spline.toUniformParameter(end)
            return spline.getPartialLength(self.resolution, start, end)
        return 0.0
