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
		if cmds.nodeType(node_select) in node_types: # Filter _ nodeType
			transforms_attr = cmds.listAttr(node_select, keyable=True)
			
			for attr in transforms_attr:
				trans_attr_name.append(f'{node_select}.{attr}')

		# pp.pprint(trans_attr_name)
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


def get_curve_data(curve_node):

	curve_data = {}

	curve_spans	 = cmds.getAttr(f'{curve_node}.spans')
	curve_form 	 = cmds.getAttr(f'{curve_node}.form')
	curve_degree = cmds.getAttr(f'{curve_node}.degree')

	curve_data[(f'{curve_node}.spans')] = curve_spans
	curve_data[(f'{curve_node}.form')] 	= curve_form
	curve_data[(f'{curve_node}.degree')]= curve_degree

	# Check for custom attribute
	custom_attr = cmds.listAttr(curve_node, userDefined=True)
	
	# If there is a custom attribute, get attribute value
	if custom_attr:
		customAttr_dict = {}
		for attr in custom_attr:
			curve_value = cmds.getAttr(f'{curve_node}.{attr}') 
			
			# Create nested dict for custom attributes
			customAttr_dict[(f'{curve_node}.{attr}')] = curve_value
			curve_data[(f'{curve_node}.custom_attr')] = customAttr_dict

	# Gets world space positions
	worldspace_positions = []
	for i in range(curve_spans + curve_degree):
		worldspace = cmds.pointPosition(f'{curve_node}.cv[{i}]')
		worldspace = tuple(worldspace) # Converts list to tuple
		worldspace_positions.append(worldspace) # Append/ combine into worldspace_positions list
	
	curve_data[(f'{curve_node}.cv')] = worldspace_positions

	# pp.pprint(curve_data)
	return curve_data


# Filters out curve's transform node and check if there are keyframes
def check_keyframe(crv_node):

	curve_transform = cmds.listRelatives(crv_node, parent=True)[0] # Get curve transform node from curve shapes
	curve_trans_attr = cmds.listAttr(curve_transform, keyable=True) # Get attributes of curve transform node

	for attr in curve_trans_attr:
	
		# Checks which keyframe has keys
		keyed_frames = cmds.keyframe(f'{curve_transform}.{attr}', query=True, timeChange=True)
		
		if keyed_frames:
			return curve_transform
		# else:
		# 	print('no animation found.')

	
		# # Check for keyframe value
		# keyframe_value = cmds.keyframe(f'{curve_transform}.{attr}', query=True, valueChange=True)
		# if keyframe_value:
		# 	# print(f'{curve_transform}.{attr}: {keyframe_value}')
		# 	# return keyframe_value
	
	# return 0


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

def read_json(file_path):

	# Reading data from the JSON file
	with open(file_path, 'r') as file:
		loaded_data = json.load(file)
			
	# pp.pprint(loaded_data)
	print('json file loaded')
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
				
			elif key2 == 'nodetype':
				namespaced_key2[key2] = value2
				
			# Add namespace for 'parent' value
			elif key2 == 'parent':
				if value2 == []:
					namespaced_value2 = []
				else:
					namespaced_value2 = [user_input + ':' + value2[0]]
				value2 = namespaced_value2
				namespaced_key2[key2] = value2

			elif key2 == 'pivot_data':
				namespaced_key2[key2] = value2

			elif key2 == 'file_attached':
				namespaced_key2[key2] = value2
			
			elif key2 == 'curve_data':
				namespaced_key2[key2] = value2

			else:
				key2_wth_namespace = f'{user_input}:{key2}' # Add back namespace
				namespaced_key2[key2_wth_namespace] = value2 # Compilation into dict at key2 

		# Compilation into dict at key1
		temp_dict[key_wth_namespace] = namespaced_key2
		namespaced_key.update(temp_dict)

	namespaced_dict['attribute_dict'] = namespaced_key

	return namespaced_dict


def create_light(namespaced_dict):

	# Light creation
	for key, value in namespaced_dict['attribute_dict'].items():
		
		# Check scene for existing lights
		if cmds.objExists(key):
			# print(f'{key} exists in scene.')
			continue
		else:
			# print(f'{key} DOES NOT exists in scene.')

			# Get value of keys nodetype
			nodetype = value.get('nodetype')

			# Create empty group transform node
			if 'transform' in nodetype:
				created_grp_node = cmds.group(empty=True, name=key)

			# Create light shape node
			else: 
				created_shape_node = cmds.createNode(nodetype, name=key)


	# Group parenting
	for key, value in namespaced_dict['attribute_dict'].items():

		# Get value of keys for parent
		node_parent = value.get('parent')

		# Get value of keys nodetype
		nodetype = value.get('nodetype')

		# # Check if key item has parent
		currently_parented = cmds.listRelatives(key, parent=True)
		# print(f'{key}.{currently_parented}')

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
		
		# If object already parented
		# else:
		# 	print(f'{key} already parented.')
	
	print('Light successfully created.')


def create_curve(namespaced_dict):

	# Creating curve node
	for key, value in namespaced_dict['attribute_dict'].items():

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
					custom_attr = curve_data[f'{key}.custom_attr']

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
			# print(key2)
				
			# Exclude 'child_shape' data from setAttr
			if key2 == 'child_shape':
				continue

			# Exclude 'nodetype' data from setAttr
			elif key2 == 'nodetype':
				continue

			# Exclude 'parent' data from setAttr
			elif key2 == 'parent':
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

	cmds.file(animExport_file_path, i= True, force=True, type='animExport', options='v=0;')
	print('Animation succuessfully imported.')

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
		# print(f'{crv_node}.{node_types}')
		
		key2_curve_dict = {}
		# Get attribute values
	
		for curve in attribute_curve:
			curve_value = get_attr_value(curve)
			key2_curve_dict[curve] = curve_value
			
		# Get curve attribute and custom attribute (if any)
		curve_data = get_curve_data(crv_node)
		
		key2_curve_dict['child_shape']	= False 		# if node has a shape node child
		key2_curve_dict['parent']		= parent_object # parent of node data
		key2_curve_dict['nodetype']	= node_types 	# node type data
		key2_curve_dict['curve_data']	= curve_data 	# curve data
		key1_curve_dict[crv_node]		= key2_curve_dict
		
		# Filters out curve's transform node and check if there are keyframes
		checking_keyframe = check_keyframe(crv_node)

		if check_keyframe == True:	
			# Item selection before export
			cmds.select(keyframe_item_list)

			# Run animExport
			export_animExport()
			
		else:
			print('No animation to export.')

		# Append items with keyframe to keyframe_item_list
		keyframe_item_list.append(checking_keyframe)
		
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
		# print(f'{shp_node}.{node_types}')

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
			shape_value = get_attr_value(shape)
			key2_shape_dict[shape] = shape_value
		
		key2_shape_dict['child_shape']	= False 		# if node has a shape node child
		key2_shape_dict['parent']		= parent_object # parent of node data
		key2_shape_dict['nodetype']	= node_types 	# node type data
		key2_shape_dict['file_attached']= file_attached # file data if any
		key1_shape_dict[shp_node]		= key2_shape_dict

	# pp.pprint(key1_shape_dict)
	# print('------------------------------------------------------------------')


	key1_transform_dict = {}
	# Getting TRASNFORM nodes attributes name and value
	for trans_node in transform_nodes:
		# print(trans_node)

		attribute_transform = get_attr_name(trans_node, node_types, node_filter='transform')
		# pp.pprint(attribute_transform)
		# Get the parent of each node
		parent_object = cmds.listRelatives(trans_node, parent=True) or []
		
		# Get the node type
		node_types = cmds.nodeType(trans_node)
		
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

			transform_value = get_attr_value(transform)
			key2_transform_dict[transform] = transform_value

		key2_transform_dict['child_shape'] 	= True 			# if node has a shape node child
		key2_transform_dict['parent'] 		= parent_object # parent of node data
		key2_transform_dict['nodetype'] 	= node_types 	# node type data
		key2_transform_dict['pivot_data'] 	= pivot_data 	# pivot object and world data
		key1_transform_dict[trans_node] 	= key2_transform_dict

	# pp.pprint(key1_transform_dict)
	# print('------------------------------------------------------------------')

	
	key1_group_dict = {}
	# # Getting GROUP transform nodes attributes name and value
	for grp_node in group_nodes:
		# print(grp_node)
		attribute_group = get_attr_name(grp_node, node_types, node_filter='group')
		
		# Get the parent of each node
		parent_object = cmds.listRelatives(grp_node, parent=True) or []
		
		# Get the node type
		node_types = cmds.nodeType(grp_node)
		
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
			group_value = get_attr_value(group)
			key2_group_dict[group] = group_value
		
		key2_group_dict['child_shape'] 	= False 		# if node has a shape node child
		key2_group_dict['parent'] 		= parent_object # parent of node data
		key2_group_dict['nodetype'] 	= node_types 	# node type data
		key2_group_dict['pivot_data'] 	= pivot_data 	# pivot object and world data
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

def main_import():
	
	read_json_file = read_json(file_path)
	
	# insert_namespace = namespace_input()
	
	insert_namespace = namespace

	# If scene has NO namespace/ NO scene referenced. Create light and setAttr.
	if insert_namespace == False:
			
		read_json_file = read_json(file_path)
		
		create_light(read_json_file)

		create_curve(read_json_file)
		
		set_pivot(read_json_file)
		
		set_attr = set_attribute(read_json_file)
	
		import_anim = import_animExport(animExport_file_path)
	
	# If scene has namespace/ has scene referenced. Only setAttr.
	else:
		added_namespace = adding_namespace(insert_namespace, read_json_file)

		set_attr = set_attribute(added_namespace)



########################################################################################	

# CALL YOUR FUNCTION HERE

# main_export(file_path)

# main_import(namespace, file_path)

################################################


# TEST MODE
print('########################################################################################')
main_export()

# namespace = 'Sample_LgtRig:'
# main_import(namespace)

### for loop to addAttr for multiple custom_attr
### check why aiarea lights but name under curve





	
########################################################################################

