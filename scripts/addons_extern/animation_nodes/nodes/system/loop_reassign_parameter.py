import bpy
from bpy.props import *
from ... base_types.node import AnimationNode
from ... tree_info import getNodeByIdentifier, keepNodeLinks

class ReassignLoopParameterNode(bpy.types.Node, AnimationNode):
    bl_idname = "an_ReassignLoopParameterNode"
    bl_label = "Reassign Loop Parameter"
    onlySearchTags = True

    def identifierChanged(self, context):
        socket = self.linkedParameterSocket
        if socket:
            self.parameterIdName = self.linkedParameterSocket.bl_idname
            self.generateSocket()

    loopInputIdentifier = StringProperty(update = identifierChanged)
    parameterIdentifier = StringProperty(update = identifierChanged)
    parameterIdName = StringProperty()

    def create(self):
        self.width = 180

    def draw(self, layout):
        socket = self.linkedParameterSocket
        if socket:
            layout.label("{} > {}".format(repr(socket.node.subprogramName), socket.text), icon = "GROUP_VERTEX")
        else:
            layout.label("Target does not exist", icon = "ERROR")

    def edit(self):
        network = self.network
        if network.type != "Invalid": return
        if network.loopInAmount != 1: return
        loopInput = network.loopInputNode
        if self.loopInputIdentifier == loopInput.identifier: return
        self.loopInputIdentifier = loopInput.identifier

    @keepNodeLinks
    def generateSocket(self):
        self.inputs.clear()
        socket = self.inputs.new(self.parameterIdName, "New Value", "newValue")
        socket.defaultDrawType = "TEXT_ONLY"

    @property
    def linkedParameterSocket(self):
        try:
            inputNode = self.loopInputNode
            return inputNode.outputsByIdentifier[self.parameterIdentifier]
        except: pass

    @property
    def loopInputNode(self):
        try: return getNodeByIdentifier(self.loopInputIdentifier)
        except: return None
