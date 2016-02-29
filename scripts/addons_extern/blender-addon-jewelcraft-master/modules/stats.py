import bpy
from os import path
from math import pi
from .. import (
	var,
	localization,
)
from . import (
	utility,
	volume,
	report,
)


def weight_display():
	context = bpy.context
	prefs = context.user_preferences.addons[var.addon_id].preferences
	props = context.scene.jewelcraft
	l = localization.locale[prefs.lang]
	m = props.weighting_metals
	vol = volume.calculate(context.active_object)
	mm3 = ' ' + l['mm3']
	g = ' ' + l['g']

	if m == 'VOL':
		report.data = str(round(vol, 4)) + mm3

	elif m == 'CUSTOM':
		dens = props.weighting_custom / 1000 # cm→mm
		report.data = str(round(vol * dens, 2)) + g

	else:
		mdens = var.metal_density[m] / 1000 # cm→mm
		report.data = str(round(vol * mdens, 2)) + g






def stats_get():
	sce = bpy.context.scene
	obs = sce.objects
	props = sce.jewelcraft
	stats = {}

	stats['METALS'] = []
	append = stats['METALS'].append
	if props.export_m_24kt        : append('24KT')
	if props.export_m_22kt        : append('22KT')
	if props.export_m_18kt_white  : append('18KT_WHITE')
	if props.export_m_14kt_white  : append('14KT_WHITE')
	if props.export_m_18kt_yellow : append('18KT_YELLOW')
	if props.export_m_14kt_yellow : append('14KT_YELLOW')
	if props.export_m_sterling    : append('STERLING')
	if props.export_m_palladium   : append('PALLADIUM')
	if props.export_m_platinum    : append('PLATINUM')
	if props.export_m_custom      : append('CUSTOM')

	if (props.export_size and obs.get(props.export_size)):
		stats['SIZE'] = str(round(obs[props.export_size].dimensions[0], 2))

	if (props.export_shank and obs.get(props.export_shank)):
		stats['SHANK'] = stats_shank(obs[props.export_shank])

	if (props.export_dim and obs.get(props.export_dim)):
		stats['DIM'] = [str(round(obs[props.export_dim].dimensions[0], 1)),
		                str(round(obs[props.export_dim].dimensions[1], 1)),
		                str(round(obs[props.export_dim].dimensions[2], 1))]

	if (props.export_weight and obs.get(props.export_weight)):
		stats['WEIGHT'] = volume.calculate(obs[props.export_weight])

	stats['GEMS'] = stats_gems()

	return stats






def template():
	stats = stats_get()
	l = export_locale()
	t = ''
	mm = ' ' + l['mm']

	if 'SIZE' in stats:
		t += '{}\n    {}\n\n'.format(l['t_size'], stats['SIZE']+mm)

	if 'SHANK' in stats:
		t += '{}\n    {}\n\n'.format(l['t_width'], stats['SHANK'][0]+mm)
		t += '{}\n    {}\n\n'.format(l['t_thickness'], stats['SHANK'][1]+mm)

	if 'DIM' in stats:
		dim = stats['DIM']
		t += '{}\n    {} × {} × {}\n\n'.format(l['t_dim'], dim[0], dim[1], dim[2]+mm)

	if ('WEIGHT' in stats and stats['METALS']):
		t += l['t_weight'] + '\n    '
		for metal in stats['METALS']:
			t += format_weight(stats['WEIGHT'], metal, l) + '\n    '
		t += '\n'

	if stats['GEMS']:
		col_len = [len(l['type']), len(l['cut']), len(l['size']), len(l['qty'])]
		rows = []
		append = rows.append
		for tpe in sorted(stats['GEMS']):
			for cut in sorted(stats['GEMS'][tpe]):
				for size in sorted(stats['GEMS'][tpe][cut]):
					row = format_gems(tpe, cut, size, stats['GEMS'][tpe][cut][size], l)
					append(row)
					for i in range(len(col_len)):
						if len(row[i]) > col_len[i]:
							col_len[i] = len(row[i])

		table_columns = '{{:{}}} | {{:{}}} | {{:{}}} | {{}}\n    '.format(str(col_len[0]), str(col_len[1]), str(col_len[2]))
		underline_len = col_len[0] + col_len[1] + col_len[2] + col_len[3] + 10

		t += l['t_settings'] + '\n    '
		t += table_columns.format(l['type'], l['cut'], l['size'], l['qty'])
		t += '—' * underline_len + '\n    '
		for gem in rows:
			t += table_columns.format(gem[0], gem[1], gem[2], gem[3])

	return t






def export():
	filepath = bpy.data.filepath

	if filepath:
		stats = template()
		filename = bpy.path.display_name_from_filepath(filepath)
		save_path = path.join(path.dirname(filepath), filename + '_stats.txt')

		f = open(save_path, 'w', encoding='utf-8')
		f.write(stats)
		f.close()

	else:
		prefs = bpy.context.user_preferences.addons[var.addon_id].preferences
		l = localization.locale[prefs.lang]
		return utility.show_error_message(l['error_file'])






#############################################################################
# Stats utility #############################################################
#############################################################################


def stats_shank(ob):
	mos = []
	for mo in ob.modifiers:
		if mo.type == 'CURVE':
			mos.append(mo.name)

	if mos:
		mo = ob.modifiers[mos[-1]]
		save_state = mo.show_viewport
		mo.show_viewport = False
		bpy.context.scene.update()
		stats = [str(round(ob.dimensions[1], 1)),
		         str(round(ob.dimensions[2], 1))]
		mo.show_viewport = save_state
	else:
		stats = [str(round(ob.dimensions[1], 1)),
		         str(round(ob.dimensions[2], 1))]

	return stats


def stats_gems():
	stats = {}

	for ob in bpy.context.scene.objects:

		if (ob.type == 'MESH' and ob.data.get('gem')):

			tpe = ob.data['gem']['TYPE']
			cut = ob.data['gem']['CUT']

			if (ob.parent and ob.parent.dupli_type == 'FACES'):
				count = polycount(ob.parent)
			elif (ob.parent and ob.parent.dupli_type == 'NONE'):
				count = 0
			else:
				count = 1

			if cut in ['ROUND', 'SQUARE']:
				length = round( (ob.dimensions[0] + ob.dimensions[1]) / 2, 2)
				depth = round(ob.dimensions[2], 2)
				if length.is_integer(): length = int(length)
				if depth.is_integer():  depth  = int(depth)
				size = (length, depth)
			else:
				length = round(ob.dimensions[1], 2)
				width = round(ob.dimensions[0], 2)
				depth = round(ob.dimensions[2], 2)
				if length.is_integer(): length = int(length)
				if width.is_integer():  width  = int(width)
				if depth.is_integer():  depth  = int(depth)
				size = (length, width, depth)

			if (stats.get(tpe) and stats[tpe].get(cut) and stats[tpe][cut].get(size)):
				stats[tpe][cut][size] = stats[tpe][cut][size] + count
			elif (stats.get(tpe) and stats[tpe].get(cut)):
				stats[tpe][cut][size] = count
			elif stats.get(tpe):
				stats[tpe][cut] = {size : count}
			else:
				stats[tpe] = {cut : {size : count}}

	return stats


def polycount(obj):
	bm = volume.bmesh_copy_from_object(obj, triangulate=False, apply_modifiers=True)
	polycount = len(bm.faces)
	bm.free()
	return polycount






#############################################################################
# Template utility ##########################################################
#############################################################################


def export_locale():
	context = bpy.context
	prefs = context.user_preferences.addons[var.addon_id].preferences
	props = context.scene.jewelcraft

	if props.export_lang == 'AUTO':
		l = prefs.lang
	else:
		l = props.export_lang

	return localization.locale[l]


def format_weight(vol, metal, l):
	props = bpy.context.scene.jewelcraft

	if metal == 'CUSTOM':
		dens = props.export_m_custom_density / 1000 # cm→mm
		mat = props.export_m_custom_name
	else:
		dens = var.metal_density[metal] / 1000 # cm→mm
		mat = l[metal.lower()]

	return '{} {} ({})'.format(str(round(vol*dens, 2)), l['g'], mat)


def format_gems(tpe, cut, size, qty, l):
	props = bpy.context.scene.jewelcraft
	mm = ' ' + l['mm']
	ct = ' ' + l['ct']
	itms = ' ' + l['items']

	if len(size) == 2:
		crt = ct_calc(tpe, cut, l=size[0], h=size[1])
		Size = '{} ({})'.format(str(size[0])+mm, str(crt)+ct)

	else:
		crt = ct_calc(tpe, cut, l=size[0], w=size[1], h=size[2])
		Size = '{} × {} ({})'.format(str(size[0]), str(size[1])+mm, str(crt)+ct)

	qty_ct = qty * crt

	Qty = '{} ({})'.format(str(qty)+itms, str(qty_ct)+ct)
	Type = l[tpe.lower()]
	Cut = l[cut.lower()]

	return (Type, Cut, Size, Qty)


def ct_calc(tpe, cut, l=None, w=None, h=None):
	props = bpy.context.scene.jewelcraft
	dens = var.stone_density[tpe] / 1000 # cm→mm
	corr = var.gem_volume_correction[cut]
	mul = 5 # g→ct

	if cut == 'ROUND':
		vol = (pi * ((l/2)**2) * h/3) * corr

	elif cut in ['OVAL', 'PEARL', 'MARQUISE']:
		vol = (pi * (l/2) * (w/2) * h/3) * corr

	elif cut in ['SQUARE', 'BAGUETTE', 'EMERALD', 'ASSCHER', 'PRINCESS', 'CUSHION']:
		vol = (l*w*h / 3) * corr

	elif cut in ['TRILLION']:
		vol = (l*w*h / 6) * corr

	ct = vol * dens * mul

	return round(ct, 3)
