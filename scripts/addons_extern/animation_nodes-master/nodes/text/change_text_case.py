import bpy
from bpy.props import *
from ... events import executionCodeChanged
from ... base_types.node import AnimationNode

caseTypeItems= [("UPPER", "To Upper Case", ""),
                ("LOWER", "To Lower Case", ""),
                ("CAPITALIZE", "Capitalize Phrase", "") ]

caseTypeCode = { item[0] : item[0].lower() for item in caseTypeItems }

class ChangeTextCaseNode(bpy.types.Node, AnimationNode):
    bl_idname = "an_ChangeTextCaseNode"
    bl_label = "Change Text Case"

    def caseTypeChanges(self, context):
        executionCodeChanged()

    caseType = EnumProperty(
        name = "Case Type", default = "CAPITALIZE",
        items = caseTypeItems, update = caseTypeChanges)

    def create(self):
        self.inputs.new("an_StringSocket", "Text", "inText")
        self.outputs.new("an_StringSocket", "Text", "outText")

    def draw(self, layout):
        layout.prop(self, "caseType", text = "")

    def getExecutionCode(self):
        return "outText = inText.{}()".format(caseTypeCode[self.caseType])
