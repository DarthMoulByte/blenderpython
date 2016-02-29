bl_info = {
	"name": "JewelCraft",
	"author": "Mikhail Rachinskiy (jewelcourses.com)",
	"version": (1,3),
	"blender": (2,7,5),
	"location": "3D View → Tool Shelf",
	"description": "JewelCraft—add-on for jewelry design that provides tools for asset management, jeweling and statistics gathering to easily get all valuable information about your jewelry product such as: gemstone settings, product dimensions and weight in different metals.",
	"wiki_url": "https://github.com/mrachinskiy/blender-addon-jewelcraft",
	"tracker_url": "https://github.com/mrachinskiy/blender-addon-jewelcraft/issues",
	"category": "Add Mesh"}

if "bpy" in locals():
	import importlib
	importlib.reload(var)
	importlib.reload(localization)
	importlib.reload(operators)
	importlib.reload(ui)
	importlib.reload(modules.icons)
	importlib.reload(modules.assets)
	importlib.reload(modules.stats)
	importlib.reload(modules.props_utility)
else:
	import bpy
	from bpy.props import (
		EnumProperty,
		BoolProperty,
		FloatProperty,
		StringProperty,
		PointerProperty,
	)
	from bpy.types import (
		PropertyGroup,
		AddonPreferences,
	)
	from . import (
		var,
		operators,
		ui,
	)
	from .modules import props_utility
	from .modules.icons import preview_collections




class JewelCraftPreferences(AddonPreferences):

	bl_idname = var.addon_id

	lang = EnumProperty(
		name="UI language",
		items=(
			('RU', "Russian (Русский)", ""),
			('EN', "English (English)", ""),
		),
		default="EN",
		description="Add-on UI language")


	def draw(self, context):
		layout = self.layout
		split = layout.split(percentage=.4)
		split.prop(self, 'lang')




class JewelCraftProperties(PropertyGroup):

	import_gem_type = EnumProperty(name="Type", items=props_utility.gem_type)
	import_gem_cut = EnumProperty(name="Cut", items=props_utility.gem_cut)
	import_gem_size = FloatProperty(name="Size", description="Set gemstone size", default=1.0, min=0.1, step=10, precision=2)


	weighting_metals = EnumProperty(name="Metals" , items=props_utility.weighting_metals)
	weighting_custom = FloatProperty(description="Custom density (g/cm³)", default=1.0, min=0.01, step=1, precision=2)


	export_options = BoolProperty()

	export_size = StringProperty(description="Object for size reference")
	export_shank = StringProperty(description="Object for shank width and height reference")
	export_dim = StringProperty(description="Object for dimensions reference")
	export_weight = StringProperty(description="Object for weight reference")

	export_metals           = BoolProperty()
	export_m_24kt           = BoolProperty()
	export_m_22kt           = BoolProperty()
	export_m_18kt_white     = BoolProperty(default=True)
	export_m_14kt_white     = BoolProperty(default=True)
	export_m_18kt_yellow    = BoolProperty()
	export_m_14kt_yellow    = BoolProperty()
	export_m_sterling       = BoolProperty()
	export_m_palladium      = BoolProperty()
	export_m_platinum       = BoolProperty()
	export_m_custom         = BoolProperty()
	export_m_custom_name    = StringProperty(description="Material name")
	export_m_custom_density = FloatProperty(description="Custom density (g/cm³)", default=1.0, min=0.01, step=1, precision=2)

	export_lang = EnumProperty(
		name="Export stats language",
		items=(
			('RU',   "Russian (Русский)", ""),
			('EN',   "English (English)", ""),
			('AUTO', "Auto", "Inherit locale from add-on preferences"),
		),
		default="AUTO",
		description="Statistics language")




classes = (
	ui.JewelCraftImportPanel,
	ui.JewelCraftWeightingPanel,
	ui.JewelCraftExportPanel,

	operators.IMPORT_GEM,
	operators.IMPORT_TYPE,
	operators.IMPORT_CUT,
	operators.IMPORT_PRONGS,
	operators.IMPORT_SINGLE_PRONG,
	operators.IMPORT_CUTTER,
	operators.IMPORT_CUTTER_SEAT_ONLY,
	operators.IMPORT_IMITATION_3_PRONG,
	operators.MAKE_DUPLIFACE,
	operators.WEIGHT_DISPLAY,

	operators.EXPORT_PICK_SIZE,
	operators.EXPORT_PICK_SHANK,
	operators.EXPORT_PICK_DIM,
	operators.EXPORT_PICK_WEIGHT,
	operators.EXPORT_STATS,

	JewelCraftPreferences,
	JewelCraftProperties,
)




def register():
	for cls in classes:
		bpy.utils.register_class(cls)

	bpy.types.Scene.jewelcraft = PointerProperty(type=JewelCraftProperties)


def unregister():
	pcoll_remove = bpy.utils.previews.remove
	for pcoll in preview_collections.values():
		pcoll_remove(pcoll)
	preview_collections.clear()

	for cls in classes:
		bpy.utils.unregister_class(cls)

	del bpy.types.Scene.jewelcraft


if __name__ == "__main__":
	register()
