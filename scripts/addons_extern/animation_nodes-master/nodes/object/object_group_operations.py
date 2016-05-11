import bpy
from ... base_types.node import AnimationNode

class ObjectGroupOperationsNode(bpy.types.Node, AnimationNode):
    bl_idname = "an_ObjectGroupOperationsNode"
    bl_label = "Object Group Operations"

    def create(self):
        self.inputs.new("an_ObjectGroupSocket", "Group", "group").defaultDrawType = "PROPERTY_ONLY"
        self.inputs.new("an_ObjectSocket", "Object", "object").defaultDrawType = "PROPERTY_ONLY"
        self.inputs.new("an_BooleanSocket", "Linked", "linked")
        self.outputs.new("an_ObjectGroupSocket", "Group", "group")

    def execute(self, group, object, linked):
        if group is None: return group
        if object is None: return group

        if object.name in group.objects:
            if not linked: group.objects.unlink(object)
        else:
            if linked: group.objects.link(object)

        return group
