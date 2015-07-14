# 「3Dビュー」エリア > 「プロパティ」パネル > 「ビュー」パネル

import bpy

################
# オペレーター #
################

class SaveView(bpy.types.Operator):
	bl_idname = "view3d.save_view"
	bl_label = "Save view"
	bl_description = "Save the current 3D view perspective"
	bl_options = {'REGISTER', 'UNDO'}
	
	save_name = bpy.props.StringProperty(name="The name", default="View saved games")
	
	def execute(self, context):
		data = ""
		for line in context.user_preferences.addons["Addon Factory"].preferences.view_savedata.split('|'):
			if (line == ""):
				continue
			try:
				save_name = line.split(':')[0]
			except ValueError:
				context.user_preferences.addons["Addon Factory"].preferences.view_savedata = ""
				self.report(type={'ERROR'}, message="Failed to load of the SaveGame resets")
				return {'CANCELLED'}
			if (str(self.save_name) == save_name):
				continue
			data = data + line + '|'
		text = data + str(self.save_name) + ':'
		co = context.region_data.view_location
		text = text + str(co[0]) + ',' + str(co[1]) + ',' + str(co[2]) + ':'
		ro = context.region_data.view_rotation
		text = text + str(ro[0]) + ',' + str(ro[1]) + ',' + str(ro[2]) + ',' + str(ro[3]) + ':'
		text = text + str(context.region_data.view_distance) + ':'
		text = text + context.region_data.view_perspective
		context.user_preferences.addons["Addon Factory"].preferences.view_savedata = text
		for area in context.screen.areas:
			area.tag_redraw()
		return {'FINISHED'}
	def invoke(self, context, event):
		return context.window_manager.invoke_props_dialog(self)

class LoadView(bpy.types.Operator):
	bl_idname = "view3d.load_view"
	bl_label = "Point of load"
	bl_description = "Load the current 3D view perspective"
	bl_options = {'REGISTER', 'UNDO'}
	
	index = bpy.props.StringProperty(name="View saved names", default="View saved games")
	
	def execute(self, context):
		for line in context.user_preferences.addons["Addon Factory"].preferences.view_savedata.split('|'):
			if (line == ""):
				continue
			try:
				index, loc, rot, distance, view_perspective = line.split(':')
			except ValueError:
				context.user_preferences.addons["Addon Factory"].preferences.view_savedata = ""
				self.report(type={'ERROR'}, message="Failed to load of the SaveGame resets")
				return {'CANCELLED'}
			if (str(self.index) == index):
				for i, v in enumerate(loc.split(',')):
					context.region_data.view_location[i] = float(v)
				for i, v in enumerate(rot.split(',')):
					context.region_data.view_rotation[i] = float(v)
				context.region_data.view_distance = float(distance)
				context.region_data.view_perspective = view_perspective
				self.report(type={'INFO'}, message=str(self.index))
				break
		else:
			self.report(type={'WARNING'}, message="Saved game does not exist")
		return {'FINISHED'}

class DeleteViewSavedata(bpy.types.Operator):
	bl_idname = "view3d.delete_view_savedata"
	bl_label = "View save to discard"
	bl_description = "Removes all viewpoints save data"
	bl_options = {'REGISTER', 'UNDO'}
	
	@classmethod
	def poll(cls, context):
		if (context.user_preferences.addons["Addon Factory"].preferences.view_savedata == ""):
			return False
		return True
	def execute(self, context):
		context.user_preferences.addons["Addon Factory"].preferences.view_savedata = ""
		return {'FINISHED'}

################
# メニュー追加 #
################

# メニューのオン/オフの判定
def IsMenuEnable(self_id):
	for id in bpy.context.user_preferences.addons["Addon Factory"].preferences.disabled_menu.split(','):
		if (id == self_id):
			return False
	else:
		return True

# メニューを登録する関数
def menu(self, context):
	if (IsMenuEnable(__name__.split('.')[-1])):
		self.layout.prop(context.user_preferences.view, 'use_zoom_to_mouse')
		self.layout.prop(context.user_preferences.view, 'use_rotate_around_active')
		self.layout.prop(context.scene, 'sync_mode')
		box = self.layout.box()
		col = box.column(align=True)
		col.operator(SaveView.bl_idname, icon="PLUGIN")
		if (context.user_preferences.addons["Addon Factory"].preferences.view_savedata != ""):
			col.operator(DeleteViewSavedata.bl_idname, icon="PLUGIN")
		if (context.user_preferences.addons["Addon Factory"].preferences.view_savedata):
			col = box.column(align=True)
			col.label(text="View save to load", icon='PLUGIN')
			for line in context.user_preferences.addons["Addon Factory"].preferences.view_savedata.split('|'):
				if (line == ""):
					continue
				try:
					index = line.split(':')[0]
				except ValueError:
					pass
				col.operator(LoadView.bl_idname, text=index, icon="PLUGIN").index = index
	if (context.user_preferences.addons["Addon Factory"].preferences.use_disabled_menu):
		self.layout.operator('wm.toggle_menu_enable', icon='VISIBLE_IPO_ON').id = __name__.split('.')[-1]