import bpy
from .. base_types.socket import AnimationNodeSocket

class MatrixListSocket(bpy.types.NodeSocket, AnimationNodeSocket):
    bl_idname = "an_MatrixListSocket"
    bl_label = "Matrix List Socket"
    dataType = "Matrix List"
    allowedInputTypes = ["Matrix List"]
    drawColor = (1, 0.56, 0.3, 0.5)
    storable = True
    hashable = False

    def getValueCode(self):
        return "[]"

    def getCopyExpression(self):
        return "[element.copy() for element in value]"
