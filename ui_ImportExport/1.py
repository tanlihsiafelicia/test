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
file_name = 'Lgt_Export_Attr.json'  # File name
file_path = f'D:/Felicia/Script_D/ui_ImportExport/json/{file_name}'  # Combine path and file name

## File path for animExport
animExport_file_name = 'Anim_Export.anim'  # File name
animExport_file_path = f'D:/Felicia/Script_D/ui_ImportExport/json/{animExport_file_name}'  # Combine path and file name


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


# Execute animExport of nodes with keyframes
def export_animExport():

	# Query the start and end frames from the Maya scene
	start_frame = cmds.playbackOptions(query=True, min=True)  # Get the start frame
	end_frame = cmds.playbackOptions(query=True, max=True)   # Get the end frame
	print(f'Start Frame: {start_frame}\nEnd Frame: {end_frame}')

	cmds.file(animExport_file_path, force=True, options=f'v=0;range={start_frame}:{end_frame}', type='animExport', exportSelected=True)
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


def main_export():
	

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
		child_node = cmds.listRelatives(crv_node, children=True)
		if child_node == None:
			continue
		node = cmds.objectType(child_node)
		if node == 'transform':
			child_shape = False
			print(f'{node}|{child_node}: False')
		else:
			child_shape = True
			print(f'{node}|{child_node}: True')

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
		
		key2_curve_dict['child_shape']	= child_shape		# if node has a shape node child
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
		export_animExport()
			
	else:
		print('No animation to export.')

		
	# pp.pprint(key1_curve_dict)
	# print('------------------------------------------------------------------')

	key1_shape_dict = {}
	# Getting LIGHT shape nodes attributes name and value
	for shp_node in shape_nodes:
		# print(shp_node)
		
		attribute_shape = get_attr_name(shp_node, node_types, node_filter='shape')

		# Get the parent of each node
		parent_object = cmds.listRelatives(shp_node, parent=True) or []
		
		# Get the node type
		node_types = cmds.nodeType(shp_node)
		
		# Check if node has a transform or other node type. transform node = False, shape node = True 
		child_node = cmds.listRelatives(shp_node, children=True)
		# print(f'child_node: {child_node}')
		if child_node == None:
			continue
		node = cmds.objectType(child_node)
		if node == 'transform':
			child_shape = False
			# print(f'{node}|{child_node}: False')
		else:
			child_shape = True
			# print(f'{node}|{child_node}: True')

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
		child_node = cmds.listRelatives(trans_node, children=True)
		if child_node == None:
			continue
		node = cmds.objectType(child_node)
		if node == 'transform':
			child_shape = False
			# print(f'{node}|{child_node}: False')
		else:
			child_shape = True
			# print(f'{node}|{child_node}: True')

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

		key2_transform_dict['child_shape'] 	= child_shape		# if node has a shape node child
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

		# Check if node has a transform or other node type. transform node = False, shape node = True 
		child_node = cmds.listRelatives(grp_node, children=True)
		if child_node == None:
			continue
		node = cmds.objectType(child_node)
		if node == 'transform':
			child_shape = False
			# print(f'{node}|{child_node}: False')
		else:
			child_shape = True
			# print(f'{node}|{child_node}: True')
		
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
		key2_group_dict['parent'] 		= parent_object		# parent of node data
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


main_export()