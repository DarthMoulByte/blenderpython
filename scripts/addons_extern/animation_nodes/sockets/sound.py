import bpy
from bpy.props import *
from .. events import propertyChanged
from .. utils.enum_items import enumItemsFromDicts
from .. base_types.socket import AnimationNodeSocket
from .. nodes.sound.sound_from_sequences import SingleSoundEvaluator, EqualizerSoundEvaluator

soundTypeItems = [
    ("SINGLE", "Single", "Only one strength per frame per sequence", "NONE", 0),
    ("EQUALIZER", "Equalizer", "Multiple strengths for different frequencies", "NONE", 1)]

@enumItemsFromDicts
def getBakeDataItems(self, context):
    items = []
    sequences = getattr(self.nodeTree.scene.sequence_editor, "sequences", [])
    for sequenceIndex, sequence in enumerate(sequences):
        if sequence.type != "SOUND": continue
        sound = sequence.sound

        for bakeIndex, data in enumerate(sound.singleData):
            items.append({
                "id" : data.identifier,
                "value" : "SINGLE_{}_{}".format(sequenceIndex, bakeIndex),
                "name" : "#{} - {} - Single".format(bakeIndex, sequence.name),
                "description" : "Low: {}  High: {}  Attack: {:.3f}  Release: {:.3f}".format(data.low, data.high, data.attack, data.release) })

        for bakeIndex, data in enumerate(sound.equalizerData):
            items.append({
                "id" : data.identifier,
                "value" : "EQUALIZER_{}_{}".format(sequenceIndex, bakeIndex),
                "name" : "#{} - {} - Equalizer".format(bakeIndex, sequence.name),
                "description" : "Attack: {:.3f}  Release: {:.3f}".format(data.attack, data.release) })
    return items

class SoundSocket(bpy.types.NodeSocket, AnimationNodeSocket):
    bl_idname = "an_SoundSocket"
    bl_label = "Sound Socket"
    dataType = "Sound"
    allowedInputTypes = ["Sound"]
    drawColor = (0.9, 0.7, 0.4, 1)
    storable = False
    hashable = False

    bakeData = EnumProperty(name = "Bake Data", items = getBakeDataItems)

    def drawProperty(self, layout, text):
        layout.prop(self, "bakeData", text = text)

    def getValue(self):
        try:
            # update the property in the ui
            self.bakeData = self.bakeData

            soundType, sequenceIndex, bakeIndex = self.bakeData.split("_")
            sequence = self.nodeTree.scene.sequence_editor.sequences[int(sequenceIndex)]
            evaluatorClass = SingleSoundEvaluator if soundType == "SINGLE" else EqualizerSoundEvaluator
            return evaluatorClass([sequence], int(bakeIndex))
        except:
            return None

    def setProperty(self, data):
        self.bakeData, self.type = data

    def getProperty(self):
        return self.bakeData, self.type
