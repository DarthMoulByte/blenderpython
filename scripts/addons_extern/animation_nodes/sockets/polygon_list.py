import bpy
from .. base_types.socket import AnimationNodeSocket

class PolygonListSocket(bpy.types.NodeSocket, AnimationNodeSocket):
    bl_idname = "an_PolygonListSocket"
    bl_label = "Polygon List Socket"
    dataType = "Polygon List"
    allowedInputTypes = ["Polygon List"]
    drawColor = (0.4, 0.7, 0.3, 0.5)
    storable = True
    comparable = False

    def getValueCode(self):
        return "[]"

    def getCopyExpression(self):
        return "[element.copy() for element in value]"
