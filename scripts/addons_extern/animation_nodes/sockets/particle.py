import bpy
from .. base_types.socket import AnimationNodeSocket

class ParticleSocket(bpy.types.NodeSocket, AnimationNodeSocket):
    bl_idname = "an_ParticleSocket"
    bl_label = "Particle Socket"
    dataType = "Particle"
    allowedInputTypes = ["Particle"]
    drawColor = (0.5, 0.3, 0.1, 1)
    storable = False
    hashable = True

    def getValueCode(self):
        return "None"
