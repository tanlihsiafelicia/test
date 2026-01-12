from PySide2 import QtCore, QtUiTools, QtWidgets, QtGui
from maya import OpenMayaUI as omu
from shiboken2 import wrapInstance
import maya.cmds as cmds
import mtoa.utils as mutils
import mtoa.aovs as aovs
import json
import os, sys
import re
import pprint as pp


## Get input from main import_export_class
# file_name = 'Lgt_Export_Attr.json'  # File name
# file_path = f'D:/Felicia/Script_D/ui_ImportExport/json/{file_name}'  # Combine path and file name

## File path for animExport
animExport_file_name = 'Anim_Export.anim'  # File name
animExport_file_path = f'D:/Felicia/Script_D/ui_ImportExport/json/{animExport_file_name}'  # Combine path and file name

node_types = [
		'nurbsCurve', 
		'aiAreaLight',
		'aiSkyDomeLight',
		'pointLight', 
		'spotLight', 
		'directionalLight', 
		'areaLight', 
		'ambientLight', 
		'volumeLight', 
	]

	
# Loop through the outliner to select all the light transform and light shape
def lgt_selection(node_types):
	
	# Lists all objects in the scene
	shape_nodes		= []
	transform_nodes	= []
	group_nodes		= []
	curve_nodes		= []
	
	# Filter all CURVE shape nodes in outliner and append to curve_nodes list
	for obj in cmds.ls(type=node_types[0]):
		curve_nodes.append(obj)
	
	# Loop through all LIGHT shape nodes in outliner
	for obj in cmds.ls(type=node_types[1:]):

		# Append it into shape_nodes list
		shape_nodes.append(obj)
	
	for obj in cmds.ls(type=node_types):
		# print(obj)
		# Append TRANSFORM nodes into transform_nodes list
		transform_node = cmds.listRelatives(obj, parent=True, fullPath=True)
		# print(transform_node)
		if transform_node:
			split_transform_node = transform_node[0].split('|')
			# print(split_transform_node)

			for i in range(1, len(split_transform_node)):
				transform_nodes.append(split_transform_node[i])

		# Append GROUP nodes into group_nodes list
		group_node = cmds.listRelatives(transform_node, parent=True, fullPath=True)
		# print(group_node)
		if group_node:
			split_group_node = group_node[0].split('|')

			for i in range(1, len(split_group_node)):
				group_nodes.append(split_group_node[i])
		
		# Condition to continue append top level group node
		# else:
		# 	group_nodes.extend(transform_node)
	
	# pp.pprint(transform_nodes)
	# pp.pprint(group_nodes)
	return curve_nodes, shape_nodes, transform_nodes, group_nodes # tuple output, need to tuple unpack to access list inside


def get_attr_name(node_select, node_types, node_filter):

	# Define the most commonly used attributes
	common_attributes = [
		'aiCamera',
		'aiCastShadows',
		'aiColorTemperature',
		'aiDiffuse',
		'aiCastVolumetricShadows',
		'aiIndirect',
		'normalize',
		'aiSamples',
		'aiSpecular',
		'aiSss',
		'aiTransmission',
		'aiUseColorTemperature',
		'aiVolume',
		'aiVolumeSamples',
		'color',
		'exposure',
		'intensity',
		'aiSpread',
		'aiSpread',
		'aiRoundness',
		'aiSoftEdge',
		'aiShadowDensity',
		'aiShadowColor',
		'format',
		'portalMode',
		'aiAovIndirect',
		'emitDiffuse',
		'emitSpecular',
		'aiExposure',
		'aiAngle',
		'aiNormalize'
		]

	nurbs_attributes = [
		'aiRenderCurve',
		'aiCurveWidth',
		'aiSampleRate',
		'aiCurveShader'
		'primaryVisibility',
		'castsShadows',
		'aiExportRefPoints',
		'aiOpaque',
		'aiMatte',
		'primaryVisibility',
		'castsShadows',
		'aiVisibleInDiffuseReflection',
		'aiVisibleInSpecularReflection',
		'aiVisibleInDiffuseTransmission',
		'aiVisibleInSpecularTransmission',
		'aiVisibleInVolume',
		'aiSelfShadows',
		'aiMode'
		]

	curve_attr_name = []
	shape_attr_name = []
	trans_attr_name = []
	group_attr_name = []

	# Iterate through only if curve_nodes
	if node_filter == 'curve':
		if cmds.nodeType(node_select) in node_types: # Filter nurbsCurve nodeType
			# Get all attributes
			attributes = cmds.listAttr(node_select)

			# Filter selected attributes 
			for attr in attributes:
				if attr in nurbs_attributes:
					curve_attr_name.append(f'{node_select}.{attr}')
		

			# Get custom attribute
			custom_attributes = cmds.listAttr(node_select, userDefined=True)
			if custom_attributes:
				for attr in custom_attributes:
					curve_attr_name.append(f'{node_select}.{attr}')
				# print(curve_attr_name)

		# pp.pprint(curve_attr_name)
		return curve_attr_name
		

	# Iterate through only if shape_nodes
	if node_filter == 'shape':
		# #if cmds.nodeType(node_select) in node_types: # Filter light nodeType
		# print(node_select)
			
		# Get all attributes
		attributes = cmds.listAttr(node_select)

		# Filter selected attributes 
		for attr in attributes:
			if attr in common_attributes:
				shape_attr_name.append(f'{node_select}.{attr}')

		# pp.pprint(shape_attr_name)
		return shape_attr_name


	# Iterate through only if transform_nodes
	if node_filter == 'transform':
		
		# if cmds.nodeType(node_select) in node_types: # Filter _ nodeType
			# print(f'{node_select}')

		transforms_attr = cmds.listAttr(node_select, keyable=True)
		# print(f'{node_select}.{transforms_attr}')
		
		for attr in transforms_attr:
			trans_attr_name.append(f'{node_select}.{attr}')

		return trans_attr_name
	

	# Iterate through only if group_nodes
	if node_filter == 'group':
		group_attr = cmds.listAttr(node_select, keyable=True)
	
		for attr in group_attr:
			group_attr_name.append(f'{node_select}.{attr}')
		
		# pp.pprint(group_attr_name)
		return group_attr_name
	
	return 0


def get_attr_value(attributes):

	# attr_value = []
	value = cmds.getAttr(attributes)

	return value


# Get curve attribute and custom attribute (if any)
def get_curve_data(curve_node):

	curve_data = {}

	curve_spans	 = cmds.getAttr(f'{curve_node}.spans')
	curve_form 	 = cmds.getAttr(f'{curve_node}.form')
	curve_degree = cmds.getAttr(f'{curve_node}.degree')

	curve_data[(f'{curve_node}.spans')] = curve_spans
	curve_data[(f'{curve_node}.form')] 	= curve_form
	curve_data[(f'{curve_node}.degree')]= curve_degree

	# Gets world space positions
	worldspace_positions = []
	for i in range(curve_spans + curve_degree):
		worldspace = cmds.pointPosition(f'{curve_node}.cv[{i}]')
		worldspace = tuple(worldspace) # Converts list to tuple
		worldspace_positions.append(worldspace) # Append/ combine into worldspace_positions list
	
	curve_data[(f'{curve_node}.cv')] = worldspace_positions

	# pp.pprint(curve_data)
	return curve_data


# Get custom attribute settings data
def get_custom_attr_setting(curve_node):
	
	# Check userDefined custom attributes
	custom_attr = cmds.listAttr(curve_node, userDefined=True)

	custom_setting_dict = {}
	if custom_attr:
		for attr in custom_attr:
			# Check custom attribute type (float: interger: boolean: enum)
			custom_attr_type = cmds.attributeQuery(attr, node=curve_node, attributeType= True)

			curve_value_float_list 	= []
			curve_value_int_list 	= []
			curve_value_enum_list	= []
			curve_value_bool_list	= []
			combined_list 			= []

			# Store custom attribute setting values
			if custom_attr_type == 'double': # float
				
				# Get min, max, default value and convert to integer
				min_val = cmds.attributeQuery(attr, node=curve_node, min=True)
				max_val = cmds.attributeQuery(attr, node=curve_node, max=True)
				def_val = cmds.attributeQuery(attr, node=curve_node, ld=True)

				# Append curve attr value (min, max, default value)
				curve_value_float_list.append(min_val[0]) # Append min value
				curve_value_float_list.append(max_val[0]) # Append max value
				curve_value_float_list.append(def_val[0]) # Append default value
				
				# Create dict for custom attributes settings
				combined_list.append(custom_attr_type)
				combined_list.append(curve_value_float_list)
				custom_setting_dict[f'{curve_node}.{attr}'] = combined_list
				

			if custom_attr_type == 'long': # integer
				
				# Get min, max, default value and convert to integer
				min_val = int(cmds.attributeQuery(attr, node=curve_node, min=True)[0])
				max_val = int(cmds.attributeQuery(attr, node=curve_node, max=True)[0])
				def_val = int(cmds.attributeQuery(attr, node=curve_node, ld=True)[0])

				# Append curve attr value (min, max, default value)
				curve_value_int_list.append(min_val)
				curve_value_int_list.append(max_val)
				curve_value_int_list.append(def_val)
				
				# Create dict for custom attributes settings
				combined_list.append(custom_attr_type)
				combined_list.append(curve_value_int_list)
				custom_setting_dict[f'{curve_node}.{attr}'] = combined_list


			if custom_attr_type == 'enum': # enum

				# Get enum names
				enum_names = cmds.attributeQuery(attr, node=curve_node, listEnum= True)
				curve_value_enum_list = enum_names[0].split(':')

				# Create dict for custom attributes settings
				combined_list.append(custom_attr_type)
				combined_list.append(curve_value_enum_list)
				custom_setting_dict[f'{curve_node}.{attr}'] = combined_list

			
			if custom_attr_type == 'bool': # boolean

				# Create dict for custom attributes settings
				combined_list.append(custom_attr_type)
				combined_list.append(curve_value_bool_list)
				custom_setting_dict[f'{curve_node}.{attr}'] = combined_list

	# pp.pprint(custom_setting_dict)
	return custom_setting_dict


# Filters out curve's transform node and check if there are keyframes
def check_keyframe(crv_node):

	curve_transform = cmds.listRelatives(crv_node, parent=True)[0] # Get curve transform node from curve shapes
	curve_trans_attr = cmds.listAttr(curve_transform, keyable=True) # Get attributes of curve transform node

	for attr in curve_trans_attr:
		# Checks which keyframe has keys
		keyed_frames = cmds.keyframe(f'{curve_transform}.{attr}', query=True, timeChange=True)
		# print(f'{curve_transform}.{attr}:{keyed_frames}')
	
		if keyed_frames:
			return curve_transform

# Filters out selection of worldnode with light shapes within group
def select_worldnode():

	clear_selection = cmds.select(clear= True)
	selection = cmds.ls(transforms= True)

	final_selection = []
	selection_list = []
	temp_list = []

	for s in selection:
		no_parent = cmds.listRelatives(s, parent= True)
		if no_parent == None:
			selection_list.append(s)

	# Selecting camera shape and transform node
	unused_nodes = []
	cam_shape = cmds.ls(cameras= True)
	cam_transform = cmds.listRelatives(cam_shape, parent=True)

	unused_nodes.extend(cam_shape)
	unused_nodes.extend(cam_transform)

	# Remove camera shape and transform node from main selection
	for node in unused_nodes:
		if node in selection_list:
			selection_list.remove(node)

	for s in selection_list:
		descendent_list = cmds.listRelatives(s, allDescendents= True)
		for d in descendent_list:
			nodetype = cmds.nodeType(d)
			if nodetype in node_types[1:]:
				if s not in final_selection:
					final_selection.append(s)
	
	# print(final_selection)
	return final_selection
				

# Execute animExport of nodes with keyframes
def export_animExport():

	# Query the start and end frames from the Maya scene
	start_frame = cmds.playbackOptions(query=True, min=True)  # Get the start frame
	end_frame = cmds.playbackOptions(query=True, max=True)   # Get the end frame
	print(f'Start Frame: {start_frame}\nEnd Frame: {end_frame}')

	# Define export options in a dictionary for clarity
	options_dict = {
		'precision': 8,
		'intValue': 17,
		'nodeNames': 1,
		'verboseUnits': 0,
		'whichRange': 1,
		'range': f'{start_frame}:{end_frame}',
		'options': 'keys',
		'hierarchy': 'below',
		'controlPoints': 0,
		'shapes': 1,
		'helpPictures': 0,
		'useChannelBox': 0,
		'copyKeyCmd': (
			'-animation objects '
			'-option keys '
			'-hierarchy below '
			'-controlPoints 0 '
			'-shape 1'
		)
	}

	# Convert dictionary to a formatted options string
	options_str = ';'.join(f'{key}={value}' for key, value in options_dict.items())

	plugin_name = 'animImportExport'

	# Check animExport plug in is loaded
	is_loaded = cmds.pluginInfo(plugin_name, query= True, loaded= True)

	if not is_loaded:
		try:
			cmds.loadPlugin(plugin_name)
			print(f"The plugin '{plugin_name}' has been loaded.")
		except Exception as e:
			print(f"Failed to load the plugin '{plugin_name}': {str(e)}")

	# Check animExport plug in is auto-loaded
	is_auto_loaded = cmds.pluginInfo(plugin_name, query=True, autoload=True)

	if not is_auto_loaded:
		cmds.pluginInfo(plugin_name, edit=True, autoload=True)
		print(f"The plugin '{plugin_name}' has been set to auto-load.")
	
	# Clear and reselect top parent node before export
	cmds.select(cl=True)
	cmds.select(select_worldnode())
	

	# AnimExport
	cmds.file(
		animExport_file_path,
		force=True,					# Overwrite existing file if needed
		options=options_str,		# Apply export options
		type='animExport',			# Set file type
		preserveReferences= True,	# Maintain external references
		exportSelected=True
	)
	

	# print(f'Animation exported from frame {start_frame} to {end_frame} to {file_path}.')
	print(f'Animation exported: {animExport_file_path}')


def remove_namespace(combined_dict):

	cleaned_dict = {}
	cleaned_dict_main = {}

	for key, value in combined_dict['attribute_dict'].items():

		new_value2 = {}

		# Remove namespace for attr name
		for key2, value2 in value.items():
		
			# Remove namespace in 'parent' value
			if key2 == 'parent':
				cleaned_key2 = [s.split(":")[-1] for s in value2]
				value2 = cleaned_key2

			# Remove namespace from keys
			cleaned_key2 = key2.split(':')[-1]
			new_value2[cleaned_key2] = value2

		# Remove namespace for key name
		cleaned_key = key.split(':')[-1]
		cleaned_dict[cleaned_key] = new_value2
		cleaned_dict_main['attribute_dict'] = cleaned_dict
	
	combined_dict = cleaned_dict_main
	
	return combined_dict


def create_json(attr_value_dict, file_path):

	directory = os.path.dirname(file_path)

	# Check if the directory exist
	if not os.path.exists(directory):
		print(f'Error: Directory does not exist - {directory}')
		return False

	# Writing data to a JSON file
	with open(file_path, 'w') as outfile:
		if outfile:
			# Combined_data need to check/ change
			json.dump(attr_value_dict, outfile, indent=4, sort_keys=False)
			print(f'Json file created: {file_path}')
		else:
			print('File output failed.')


########################################################################################

def read_json(file_path):

	# Reading data from the JSON file
	with open(file_path, 'r') as file:
		loaded_data = json.load(file)
			
	# pp.pprint(loaded_data)
	print('json file loaded.')
	return loaded_data


def namespace_input():

	# user_input_switch = False

	# First dialog: Ask a yes/no question
	result_yes_no = cmds.confirmDialog(
	title='Namespace Options',
	message="Do you want to include a namespace?",
	button=["Yes", "No"],
	defaultButton='Yes',
	cancelButton='No',
	dismissString='No'
	)

	# Check if the user pressed OK
	if result_yes_no == 'Yes':
		
		# Prompt the user for input
		result = cmds.promptDialog(
		title='Namespace Options',
		message='Use selected namespace as parent and add new namespace string:',
		button=['OK', 'Cancel'],
		defaultButton='OK',
		cancelButton='Cancel',
		dismissString='Cancel'
		)

		# Check if the user pressed OK
		if result == 'OK':
			user_input = cmds.promptDialog(query=True, text=True)
			user_input_switch = user_input
			# print("Namespace input:", user_input)
		else:
			# print("No namespace entered.")
			pass

	else:
		user_input_switch = False
		# print("Namespace inclusion not selected.")

	# print(f'Include namespace: {user_input_switch}')
	# print(user_input_switch)
	return user_input_switch


# Recreate new dict with namespace added
def adding_namespace(user_input, combined_dict):

	namespaced_dict = {}
	namespaced_key = {}
	temp_dict = {}

	for key, value in combined_dict['attribute_dict'].items():

		namespaced_key2 = {} # Initialise empty dict so it will reset at every for loop (so to not take in everything)
		key_wth_namespace = f'{user_input}:{key}'
		new_key = key.replace(key, key_wth_namespace)
		
		for key2, value2 in value.items():
		
			# Re-add keys without namespace into dict
			if key2 == 'child_shape':
				namespaced_key2[key2] = value2
				
			# Add namespace for 'parent' value
			elif key2 == 'parent':
				if value2 == []:
					namespaced_value2 = []
				else:
					namespaced_value2 = [user_input + ':' + value2[0]]
				value2 = namespaced_value2
				namespaced_key2[key2] = value2
				
			elif key2 == 'nodetype':
				namespaced_key2[key2] = value2

			elif key2 == 'pivot_data':
				namespaced_key2[key2] = value2

			elif key2 == 'file_attached':
				namespaced_key2[key2] = value2
			
			elif key2 == 'curve_data':
				namespaced_key2[key2] = value2

			elif key2 == 'custom_setting':
				namespaced_key2[key2] = value2

			else:
				key2_wth_namespace = f'{user_input}:{key2}' # Add back namespace
				namespaced_key2[key2_wth_namespace] = value2 # Compilation into dict at key2 

		# Compilation into dict at key1
		temp_dict[key_wth_namespace] = namespaced_key2
		namespaced_key.update(temp_dict)

	namespaced_dict['attribute_dict'] = namespaced_key

	return namespaced_dict


def create_light(loaded_data):

	# Shape node creation
	for key, value in loaded_data['attribute_dict'].items():
		
		# Check scene for existing lights
		if cmds.objExists(key):
			continue

		else:
			# print(f'{key} DOES NOT exists in scene.')
			# Get value of keys nodetype
			nodetype = value.get('nodetype')
			childshape = value.get('child_shape')

			# Create shape node first
			if nodetype != 'transform':
				created_shape_node = cmds.createNode(nodetype, name=key)
			
	# Transform node creation
	for key, value in loaded_data['attribute_dict'].items():
		
		# Check scene for existing lights
		if cmds.objExists(key):
			continue

		else:
			# print(f'{key} DOES NOT exists in scene.')
			# Get value of keys nodetype
			nodetype = value.get('nodetype')
			childshape = value.get('child_shape')

			# Create shape node first
			if nodetype == 'transform':
				created_shape_node = cmds.createNode(nodetype, name=key)

	# Group parenting
	for key, value in loaded_data['attribute_dict'].items():

		node_parent = value.get('parent') # Get value of keys for parent
		nodetype = value.get('nodetype') # Get value of keys nodetype
		currently_parented = cmds.listRelatives(key, parent=True) # Check if key item has parent

		# Check if object is correctly parented:
		if currently_parented != node_parent:
			# Selects light transform only
			if node_parent: # Condition to continue through if parent value is None/null
				if cmds.objectType(key)=='transform': # Checks for transform node on created group node
					# Parents transform nodes to group
					cmds.parent(key, node_parent)
				else:
					# Parents shape node to parented transform node
					trans_node = cmds.listRelatives(key, parent=True) # Assigns new var to lgt transform to be deleted later
					cmds.parent(key, node_parent, relative=True, shape=True) # Parents shape to transform & group node
					cmds.delete(trans_node[0]) # Delete unused lgt transform node
			# print('Objects successfully already parented.')
	
	print('Light successfully recreated.')


def create_curve(loaded_data):

	# Creating curve node
	for key, value in loaded_data['attribute_dict'].items():

		# Check scene for existing curve
		if not cmds.objExists(key):

			# Filter iteration only within curve_data
			if 'curve_data' in value:
				curve_data = value['curve_data']
				
				for key2, value2 in curve_data.items():
				# Reassign value for easy value2 access
					spans 		= curve_data[f'{key}.spans']
					form 		= curve_data[f'{key}.form']
					degree 		= curve_data[f'{key}.degree']
					cv 			= curve_data[f'{key}.cv']
					# custom_attr = curve_data[f'{key}.custom_attr']

				# Recreate the curve
				curve_created = cmds.curve(point=cv, degree=degree)

				# Get the curve shape node
				shape_curve = cmds.listRelatives(curve_created,shapes= True)[0]
				
				# Get parent of curve shape
				parent_name = value['parent'][0]
	
				# Handle curve form
				if form == 1:  # Closed
					cmds.closeCurve(curve_created, preserveShape=False)

				elif form == 2:  # Periodic
					cmds.closeCurve(curve_created, preserveShape=False, replaceOriginal=True)

				elif form == 0:  # Open
					continue

				# Rename curve
				cmds.rename(shape_curve,key)
				cmds.rename(curve_created, parent_name)
				
				# Validate spans
				actual_spans = cmds.getAttr(f"{cmds.listRelatives(parent_name, shapes=True)[0]}.spans")
				# If spans does not match, proceed to rebuild curve
				if actual_spans != spans:
					print(f'Warning: Expected spans ({spans}) do not match recreated spans ({actual_spans}).\nProceed to rebuild Curve {key}.')

					# Clear selection before rebuilding curve
					cmds.select(cl=1)

					# Rebuild curve
					rebuilt_curve = cmds.rebuildCurve(key , s=spans, d=degree,)

					# Set CV positions
					for index, value in enumerate(cv):
						cmds.xform(f'{key}.cv[{index}]', translation=value, worldSpace=True)
					print(f'{key} Curve successfully rebuilt.')

		# else:
		# 	print(f'{key} curve already exists in scene.')
	print('Curves successfully recreated.')


def create_custom_attr(loaded_data):
	
	for key, value in loaded_data['attribute_dict'].items():
		custom_setting = value.get('custom_setting')

		attr_type	= []
		attr_value	= []

		# print(f'{key}.{custom_setting}')

		# if custom_setting == {}:
		# 	continue

		for node_attr, value in custom_setting.items():
			node, attr_name = node_attr.split('.') # Split the node name and attr name
			attr_type = value[0]
			attr_value = value[1]

			# Check if the attribute exists
			if not cmds.attributeQuery(attr_name, node= node, exists= True):
				
				# print(f'{node_attr} does not exist, proceed to create.')

				if attr_type == 'double': # float
					created_cusAttr = cmds.addAttr(node, longName= attr_name, attributeType= attr_type, keyable= True, min=attr_value[0] , max=attr_value[1] , dv=attr_value[2])
					# print(f'{attr_name} done added.')

				elif attr_type == 'long': # integer
					created_cusAttr = cmds.addAttr(node, longName= attr_name, attributeType= attr_type, keyable= True, min=attr_value[0] , max=attr_value[1] , dv=attr_value[2])
					# print(f'{attr_name} done added.')

				elif attr_type == 'bool': # boolean
					created_cusAttr = cmds.addAttr(node, longName= attr_name, attributeType= attr_type, keyable= True)
					# print(f'{attr_name} done added.')

				elif attr_type == 'enum': # enum
					enum_names = [':'.join(attr_value)]
					created_cusAttr = cmds.addAttr(node, longName= attr_name, attributeType= attr_type, keyable= True, enumName= enum_names[0])
					# print(f'{attr_name} done added.')

			# else:
			# 	print(f'{node_attr} already exist in scene.')
		
	print('Custom attribute successfully recreated.')


def set_pivot(loaded_data):

	# Directly accessing 'attribute_dict'
	for key, value in loaded_data['attribute_dict'].items():
		for key2, value2 in value.items():
			if key2 == 'pivot_data':
				# Get pivot data for object space
				pivot_rotate = value2.get('pivot_rotate')		
				pivot_scale = value2.get('pivot_scale')

				# Set pivot rotate
				set_pivot_rotate = cmds.xform(key, objectSpace=True, rotatePivot=pivot_rotate)

				# Set pivot scale
				set_pivot_scale = cmds.xform(key, objectSpace=True, scalePivot=pivot_scale)

			# else:
			#     print(f'No pivot data found for {key}.')

	print ('Pivot successfully imported.')


def set_attribute(loaded_data):

	# Directly accessing 'attribute_dict'
	for key, value in loaded_data['attribute_dict'].items():
		for key2, value2 in value.items():
				
			# Exclude 'child_shape' data from setAttr
			if key2 == 'child_shape':
				continue

			# Exclude 'parent' data from setAttr
			elif key2 == 'parent':
				continue

			# Exclude 'nodetype' data from setAttr
			elif key2 == 'nodetype':
				continue

			# Exclude 'pivot_data' data from setAttr
			elif key2 == 'pivot_data':
				continue

			# Exclude 'pivot_data' data from setAttr
			elif key2 == 'file_attached':
				continue

			# Exclude 'curve_data' data from setAttr
			elif key2 == 'curve_data':
				continue

			# Exclude 'custom_setting' data from setAttr
			elif key2 == 'custom_setting':
				continue

			# If the value is a list (.color)
			elif isinstance(value2, list):
				continue
				# cmds.setAttr(key2, value2[0][0],value2[0][1],value2[0][2])
				# print(f'{key2} value successfully imported.')

			# setAttr for value type; bool, int, float
			else:
				cmds.setAttr(key2, value2)
				# print(f'{key2} value successfully imported.')


	# Iteration to connect HDR file
	
	for key, value in loaded_data['attribute_dict'].items():
		for key2, value2 in value.items():

			# If 'file_attached' is true, connect file 
			if key2 == 'file_attached' and isinstance(value2, str):

				hdr_file_path = value2

				# Check if the attribute is connected
				connections = cmds.listConnections(key, plugs=True, destination=False)

				if connections:
					# print(f"The attribute '{key}' is connected to: {connections}")
					continue

				else:
					# Create file node
					file_node = cmds.shadingNode('file', asTexture=True)

					# if cmds.objExists(file_node):
					# 	print(f'file_node: {file_node}')
					
					# Set the HDR file path on the file node
					cmds.setAttr(f'{file_node}.fileTextureName', hdr_file_path, type='string')

					# Connect the file node's outColor to the DomeLight's color attribute
					if cmds.connectAttr(f'{file_node}.outColor', f'{key}.color', force=True):
						print ('HDR file connected to Dome Light.')

					else:
						print('No HDR file selected.')

	print('Attributes successfully imported.')


# Execute import animExport file
def import_animExport(animExport_file_path):

	# Clear and reselect top parent node before import
	cmds.select(cl=True)
	cmds.select(select_worldnode())

	cmds.file(animExport_file_path, i= True, force=True, type='animExport', options='v=0;')
	print('Animation succuessfully imported.')


########################################################################################

def main_export(file_path, node_types=node_types ):

	curve_nodes, shape_nodes, transform_nodes, group_nodes = lgt_selection(node_types) 
	# print(f'curve_nodes = {curve_nodes}')
	# print(f'shape_nodes = {shape_nodes}')
	# print(f'transform_nodes = {transform_nodes}')
	# print(f'group_nodes = {group_nodes}')

	# # key1 = object name
	# # value1/ key2 = attr name
	# # value2 = attr value

	key1_curve_dict = {}
	keyframe_item_list = []
	
	# Getting CURVE shape nodes attributes name and value
	for crv_node in curve_nodes:

		# Get attribute name of curve/ ctrl shape and transform node (in channel box)
		attribute_curve = get_attr_name(crv_node, node_types, node_filter='curve')
		
		# Get the parent of each node
		parent_object = cmds.listRelatives(crv_node, parent=True) or []
		
		# Get the node type
		node_types = cmds.nodeType(crv_node)

		# Check if node has a transform or other node type. transform node = False, shape node = True 
		child_shape = False
		child_node = cmds.listRelatives(crv_node, children=True)
		if child_node != None:
			for child in child_node:
				node = cmds.objectType(child)
				if node == 'transform':
					child_shape = False
				else:
					child_shape = True
		# else:
		# 	print(f'{crv_node}: child_node: {child_node}')
		
		key2_curve_dict = {}
		# Get attribute values
	
		for curve in attribute_curve:
			curve_value = get_attr_value(curve)
			key2_curve_dict[curve] = curve_value
			
		# Get curve attribute and custom attribute (if any)
		curve_data = get_curve_data(crv_node)
		
		# Get custom attribute settings data
			# check if need to put if condition if there are no custom attr
		custom_setting = get_custom_attr_setting(crv_node)
		
		key2_curve_dict['child_shape']	= child_shape 		# if node has a shape node child
		key2_curve_dict['parent']		= parent_object		# parent of node data
		key2_curve_dict['nodetype']		= node_types 		# node type data
		key2_curve_dict['curve_data']	= curve_data 		# curve data
		key2_curve_dict['custom_setting']= custom_setting 	# curve data
		key1_curve_dict[crv_node]		= key2_curve_dict
		
		# Filters out curve's transform node and check if there are keyframes
		checking_keyframe = check_keyframe(crv_node)

		if checking_keyframe:
			keyframe_item_list.append(checking_keyframe)
			# print(keyframe_item_list)

			# Item selection before export
			cmds.select(keyframe_item_list)

	if keyframe_item_list != []:
		# Run animExport        
		# final_select = select_worldnode()
		export_animExport()
		
			
	else:
		print('No animation to export.')

		
	# pp.pprint(key1_curve_dict)
	# print('------------------------------------------------------------------')

	key1_shape_dict = {}
	# Getting LIGHT shape nodes attributes name and value
	for shp_node in shape_nodes:
		
		attribute_shape = get_attr_name(shp_node, node_types, node_filter='shape')

		# Get the parent of each node
		parent_object = cmds.listRelatives(shp_node, parent=True) or []
		
		# Get the node type
		node_types = cmds.nodeType(shp_node)

		# Check if node has a transform or other node type. transform node = False, shape node = True 
		child_shape = False
		child_node = cmds.listRelatives(shp_node, children=True)
		if child_node != None:
			# print(f'{shp_node}: child_node: {child_node}')
			for child in child_node:
				node = cmds.objectType(child)
				if node == 'transform':
					child_shape = False
				else:
					child_shape = True
		# else:
		# 	print(f'{shp_node}: child_node: {child_node}')




		# Get the file path from the file node
		connections = cmds.listConnections(f'{shp_node}.color', type='file')
		
		if connections:
			file_node = connections[0]
			file_attached = cmds.getAttr(f'{file_node}.fileTextureName')
		else:
			file_attached = None

		key2_shape_dict = {}
		# Get attribute values
		for shape in attribute_shape:

			# Get custom attribute settings data
				# check if need to put if condition if there are no custom attr
			custom_setting = get_custom_attr_setting(shp_node)

			shape_value = get_attr_value(shape)
			key2_shape_dict[shape] = shape_value
		
		key2_shape_dict['child_shape']	= child_shape		# if node has a shape node child
		key2_shape_dict['parent']		= parent_object		# parent of node data
		key2_shape_dict['nodetype']		= node_types 		# node type data
		key2_shape_dict['file_attached']= file_attached 	# file data if any
		key2_shape_dict['custom_setting']= custom_setting 	# curve data
		key1_shape_dict[shp_node]		= key2_shape_dict

	# pp.pprint(key1_shape_dict)
	# print('------------------------------------------------------------------')


	key1_transform_dict = {}
	# Getting TRASNFORM nodes attributes name and value
	for trans_node in transform_nodes:
		
		attribute_transform = get_attr_name(trans_node, node_types, node_filter='transform')
	
		# Get the parent of each node
		parent_object = cmds.listRelatives(trans_node, parent=True) or []
		
		# Get the node type
		node_types = cmds.nodeType(trans_node)

		# Check if node has a transform or other node type. transform node = False, shape node = True 
		child_shape = False
		child_node = cmds.listRelatives(trans_node, children=True)
		if child_node != None:
			for child in child_node:
				node = cmds.objectType(child)
				if node == 'transform':
					child_shape = False
				else:
					child_shape = True

		# else:
		# 	print(f'{trans_node}: child_node: {child_node}')
		
		# Get the object space pivot rotate
		pivot_rotate = cmds.xform(trans_node, query=True, objectSpace=True, rotatePivot=True)

		# Get the object space pivot scale
		pivot_scale = cmds.xform(trans_node, query=True, objectSpace=True, scalePivot=True)

		# Store the data in a dictionary
		pivot_data = {
			'pivot_rotate': pivot_rotate,
			'pivot_scale': pivot_scale
		}

		key2_transform_dict = {}
		# Get attribute and translation values
		for transform in attribute_transform:
			# print(transform)

			# Get custom attribute settings data
				# check if need to put if condition if there are no custom attr
			custom_setting = get_custom_attr_setting(trans_node)

			transform_value = get_attr_value(transform)
			key2_transform_dict[transform] = transform_value

		key2_transform_dict['child_shape'] 	= child_shape 		# if node has a shape node child
		key2_transform_dict['parent'] 		= parent_object		# parent of node data
		key2_transform_dict['nodetype'] 	= node_types 		# node type data
		key2_transform_dict['pivot_data'] 	= pivot_data 		# pivot object and world data
		key2_transform_dict['custom_setting']= custom_setting 	# curve data
		key1_transform_dict[trans_node] 	= key2_transform_dict

	# pp.pprint(key1_transform_dict)
	# print('------------------------------------------------------------------')

	
	key1_group_dict = {}
	# # Getting GROUP transform nodes attributes name and value
	for grp_node in group_nodes:
		attribute_group = get_attr_name(grp_node, node_types, node_filter='group')
		
		# Get the parent of each node
		parent_object = cmds.listRelatives(grp_node, parent=True) or []
		
		# Get the node type
		node_types = cmds.nodeType(grp_node)

		
		# # Check if node has a transform or other node type. transform node = False, shape node = True 
		child_shape = False
		child_node = cmds.listRelatives(grp_node, children=True)
		if child_node != None:
			for child in child_node:
				node = cmds.objectType(child)
				if node == 'transform':
					child_shape = False
				else:
					child_shape = True
		# else:
		# 	print(f'{grp_node}: child_node: {child_node}')

		# Get the object space pivot rotate
		pivot_rotate = cmds.xform(grp_node, query=True, objectSpace=True, rotatePivot=True)

		# Get the object space pivot scale
		pivot_scale = cmds.xform(grp_node, query=True, objectSpace=True, scalePivot=True)

		# Store the data in a dictionary
		pivot_data = {
			'pivot_rotate': pivot_rotate,
			'pivot_scale': pivot_scale
		}

		key2_group_dict = {}
		# Get attribute and translation values
		for group in attribute_group:

			# Get custom attribute settings data
				# check if need to put if condition if there are no custom attr
			custom_setting = get_custom_attr_setting(grp_node)

			group_value = get_attr_value(group)
			key2_group_dict[group] = group_value
		
		key2_group_dict['child_shape'] 	= child_shape		# if node has a shape node child
		key2_group_dict['parent'] 		= parent_object 	# parent of node data
		key2_group_dict['nodetype'] 	= node_types 		# node type data
		key2_group_dict['pivot_data'] 	= pivot_data 		# pivot object and world data
		key2_group_dict['custom_setting']= custom_setting 	# curve data
		key1_group_dict[grp_node] 		= key2_group_dict

	# pp.pprint(key1_group_dict)
	# print('------------------------------------------------------------------')

	# # Remarks
	# # key1 = oject name
	# # value1/ key2 = attr name
	# # value2 = attr value

	attribute_dict = {}

	# Combining all the dicts together
	attribute_dict.update(key1_group_dict)
	attribute_dict.update(key1_transform_dict)
	attribute_dict.update(key1_shape_dict)
	attribute_dict.update(key1_curve_dict)

	combined_dict = {
		'attribute_dict': attribute_dict
	}

	# # Create json file (wth namespace)
	# creating_json = create_json(combined_dict)

	# Remove namespace and update combined_dict
	removing_namespace = remove_namespace(combined_dict)

	# Create json file (w/out namespace)
	creating_json = create_json(removing_namespace, file_path)

	

########################################################################################

def main_import(namespace, file_path):

	read_json_file = read_json(file_path)
	
	insert_namespace = namespace

	# Add namespace into new dict 
	added_namespace = adding_namespace(insert_namespace, read_json_file)


	# If NO namespace selected:
	# 	Iterate through json file to compare and check for light existence in scene:
	# 		If light does NOT EXIST:
	# 			Recreate light
		
	# 	Iterate again to reconfirm light existence:
	# 		If light EXIST:
	# 			Set attribute and import animation

	# Else if GOT namespace selected:
	# 	Iterate through json file to compare and check for light existence in scene:
	# 		If light EXIST:
	# 			Set attribute and import animation
	# 		If light does NOT EXIST:
	# 			No nothing


	# Clear all selection
	cmds.select(cl=True)

	if insert_namespace == '': # WITHOUT namespace
		print('WITHOUT namespace')
		# Iterate and check for light existence in scene, if none, recreate light (WITHOUT namespace)
		for key, value in read_json_file['attribute_dict'].items():
			lgtrig_exist = cmds.objExists(key) # Checks scene and compare with json (NO namespace)

			if not lgtrig_exist: # If light rig NOT EXIST in scene
				print(f'{key}: light NOTTTTTTTTTTTTTTT EXIST, WITHOUT namespace')
				creating_create_light	= create_light(read_json_file)
				creating_create_curve	= create_curve(read_json_file)
				creating_custom_attr	= create_custom_attr(read_json_file)
				setting_pivot			= set_pivot(read_json_file)

		# # 2nd Iteration after all lights exist, set attribute & import animation
		for key, value in read_json_file['attribute_dict'].items():
			if lgtrig_exist: # If light rig NOW EXIST in scene
				print('########################################################################################')
				print('light EXIST with namespace')
				seting_attr 			= set_attribute(read_json_file)
				import_anim 			= import_animExport(animExport_file_path)

	else: # WITH namespace
		print('WITH namespace')
		# Iterate and check for light existence in scene, if none, recreate light (WITH namespace)
		for key, value in added_namespace['attribute_dict'].items():
			namespace_lgtrig_exist = cmds.objExists(key) # Checks scene and compare with json (WITH namespace)

			if namespace_lgtrig_exist: # If namespace light rig NOT EXIST in scene
				print('light EXIST with namespace')
				set_attr 		= set_attribute(added_namespace)
				import_anim 	= import_animExport(animExport_file_path)
			
			else:
				print(f'{key} does not exist in scene.')

########################################################################################
	# else: # WITH namespace
	# 	print('WITH namespace')
	# 	# Iterate and check for light existence in scene, if none, recreate light (WITH namespace)
	# 	for key, value in added_namespace['attribute_dict'].items():
	# 		namespace_lgtrig_exist = cmds.objExists(key) # Checks scene and compare with json (WITH namespace)

	# 		if not namespace_lgtrig_exist: # If namespace light rig NOT EXIST in scene
	# 			print('light NOT EXIST with namespace')
	# 			creating_create_light	= create_light(added_namespace)
	# 			creating_create_curve	= create_curve(added_namespace)
	# 			creating_custom_attr	= create_custom_attr(added_namespace)
	# 			setting_pivot			= set_pivot(added_namespace)
		
	# 	# 2nd Iteration after all lights exist, set attribute & import animation
	# 	for key, value in added_namespace['attribute_dict'].items():
	# 		if namespace_lgtrig_exist: # If namespace light rig NOW EXIST in scene
	# 			print('light EXIST with namespace')
	# 			set_attr 		= set_attribute(added_namespace)
	# 			import_anim 	= import_animExport(animExport_file_path)
########################################################################################
			
				



	# for key, value in added_namespace['attribute_dict'].items():
	# 	namespace_lgtrig_exist = cmds.objExists(key)

	# if lgtrig_exist: # If light rig EXIST, WITHOUT namespace
	# 	# print('LIGHT RIG EXIST')

	# 	if insert_namespace == '': # WITHOUT namespace
	# 		# print('NO NAMESPACE')
	# 		set_attr 		= set_attribute(read_json_file)
	# 		import_anim 	= import_animExport(animExport_file_path)

	# 	elif namespace_lgtrig_exist: # If light rig EXIST, WITH namespace
	# 		# print('GOT NAMESPACE')
	# 		set_attr 		= set_attribute(added_namespace)
	# 		import_anim 	= import_animExport(animExport_file_path)

	# else: # If light rig NOT EXIST
	# 	# print('LIGHT RIG NOTTTTTTTTTTTTTTTTTTTTTT EXIST')
	# 	creating_create_light	= create_light(read_json_file)
	# 	creating_create_curve	= create_curve(read_json_file)
	# 	creating_custom_attr	= create_custom_attr(read_json_file)
	# 	setting_pivot			= set_pivot(read_json_file)
	# 	seting_attr 			= set_attribute(read_json_file)
	# 	import_anim 			= import_animExport(animExport_file_path)





########################################################################################

# CALL YOUR FUNCTION HERE

# main_export(file_path)

# main_import(namespace, file_path)

########################################################################################


# TEST MODE
print('########################################################################################')
# namespace = ''
# file_name = 'TEST_2.json'  # File name
# file_path = f'D:/Felicia/Script_D/ui_ImportExport/json/{file_name}'  # Combine path and file name


# main_export(file_path, node_types)
# main_import(namespace, file_path)


	
########################################################################################

