import bpy
import random
from bpy.props import *
from ... events import propertyChanged, executionCodeChanged
from ... base_types.node import AnimationNode
from ... algorithms.random import getUniformRandom

class RandomNumberNode(bpy.types.Node, AnimationNode):
    bl_idname = "an_RandomNumberNode"
    bl_label = "Random Number"

    def socketUsageChanged(self, context):
        self.inputs["Min"].hide = not self.useMinValue
        self.inputs["Max"].hide = not self.useMaxValue
        executionCodeChanged()

    nodeSeed = IntProperty(update = propertyChanged)

    useNodeSeed = BoolProperty(name = "Use Node Seed",
        description = "Turning this off gives a speedup",
        default = True, update = executionCodeChanged)

    checkSeed = BoolProperty(name = "Check Seed",
        description = "Can be turned of when using small seeds ( < 20.000.000 )",
        default = True, update = executionCodeChanged)

    useMinValue = BoolProperty(name = "Use Min Value",
        description = "When turned off 0 will be used as min value",
        default = True, update = socketUsageChanged)

    useMaxValue = BoolProperty(name = "Use Max Value",
        description = "When turned off 1 will be used as max value",
        default = True, update = socketUsageChanged)

    def create(self):
        self.inputs.new("an_IntegerSocket", "Seed", "seed")
        self.inputs.new("an_FloatSocket", "Min", "minValue").value = 0.0
        self.inputs.new("an_FloatSocket", "Max", "maxValue").value = 1.0
        self.outputs.new("an_FloatSocket", "Number", "number")
        self.randomizeNodeSeed()

    def draw(self, layout):
        if self.useNodeSeed:
            layout.prop(self, "nodeSeed", text = "Node Seed")

    def drawAdvanced(self, layout):
        layout.prop(self, "useNodeSeed")
        layout.prop(self, "checkSeed")

        col = layout.column(align = True)
        col.prop(self, "useMaxValue")
        subcol = col.column()
        subcol.active = self.useMaxValue
        subcol.prop(self, "useMinValue")

    def getExecutionCode(self):
        if self.useNodeSeed and self.checkSeed: seedCode = "(seed + self.nodeSeed * 1034) % len(random_number_cache)"
        elif self.useNodeSeed and not self.checkSeed: seedCode = "seed + self.nodeSeed * 1034"
        elif not self.useNodeSeed and self.checkSeed: seedCode = "seed % len(random_number_cache)"
        elif not self.useNodeSeed and not self.checkSeed: seedCode = "seed"

        if self.useMinValue and self.useMaxValue: changeCode = " * (maxValue - minValue) + minValue"
        elif not self.useMinValue and self.useMaxValue: changeCode = " * maxValue"
        else: changeCode = ""

        return "number = random_number_cache[{}]{}".format(seedCode, changeCode)

    def duplicate(self, sourceNode):
        self.randomizeNodeSeed()

    def randomizeNodeSeed(self):
        self.nodeSeed = int(random.random() * 100)
