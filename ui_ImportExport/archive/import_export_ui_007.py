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


file_name = 'Lgt_Export_Attr.json'  # File name
file_path = f'D:/Felicia/Script_D/ui_ImportExport/json/{file_name}'  # Combine path and file name



# Loop through the outliner to select all the light transform and light shape
def lgt_selection(light_types):
	
	# Lists all objects in the scene
	light_shapes 	= []
	light_transforms = []
	light_groups 	= []

	# Loop through all obj in outliner
	for obj in cmds.ls(type=light_types):

		# Append it into light_shapes list
		light_shapes.append(obj)
		
		# Append transform nodes into light_transform list
		transform_node = cmds.listRelatives(obj, parent = True)
		# print(transform_node)
		light_transforms.append(transform_node[0])

		# Append group nodes into light_group list
		group_node = cmds.listRelatives(transform_node, parent = True, fullPath=True)

		split_group_node = group_node[0].split('|')
		# print(split_group_node)

		for i in range(1, len(split_group_node)):
			light_groups.append(split_group_node[i])
	
	return light_shapes, light_transforms, light_groups # tuple output, need to tuple unpack to access list inside


def get_attr_name(lgt_select, light_types, light_nodes):

	# Define the most commonly used attributes
	common_attributes = [
		'aiCamera',					# Controls light contribution to camera rays
		'aiCastShadows',			# Enables or disables shadow casting
		'aiColorTemperature',		# Adjusts the light's color temperature
		'aiDiffuse',				# Controls light contribution to diffuse surfaces
		'aiCastVolumetricShadows',	# Toggles casting shadows in volumes
		'aiIndirect',				# Adjusts indirect light contribution
		'normalize',				# Normalizes light intensity regardless of size
		'aiSamples',				# Sets the number of samples for light quality
		'aiSpecular',				# Controls light contribution to specular reflections
		'aiSss',					# Controls light interaction with subsurface scattering
		'aiTransmission',			# Adjusts light contribution to transmissive materials
		'aiUseColorTemperature',	# Toggles color temperature usage
		'aiVolume',					# Controls light contribution to volumes
		'aiVolumeSamples',			# Sets the number of volume sampling rays
		'color',					# Defines the light's emitted color
		'exposure',					# Adjusts the brightness using an exponential scale
		'intensity',				# Sets the light's base brightness level
		]

	transform_attributes = [
		'translateX',
		'translateY',
		'translateZ',
		'rotateX',
		'rotateY',
		'rotateZ',
		'scaleX',
		'scaleY',
		'scaleZ',
		'visibility'
	]

	attr_name 	= []
	trans_name 	= []
	group_name 	= []
	
	# Iterate through only if light_shapes
	if light_nodes == 'shape':
		if cmds.nodeType(lgt_select) in light_types:
			
			attributes = cmds.listAttr(lgt_select)

			for attr in attributes:
				if attr in common_attributes:
					attr_name.append(f'{lgt_select}.{attr}')
					## attr_name = attr_name + (lgt_select + '.' + attr,) # only for using tuple 
			
		return attr_name

	# Iterate through only if light_transforms
	if light_nodes == 'transform':
		if cmds.listRelatives(lgt_select, shapes=True):
			
			transforms = cmds.listAttr(lgt_select)
			
			for trans in transforms:
				if trans in transform_attributes:
					trans_name.append(f'{lgt_select}.{trans}')

		return trans_name

	# Iterate through only if light_groups
	if light_nodes == 'group':
		if cmds.listRelatives(lgt_select, children=True):

			if not cmds.listRelatives(lgt_select, shapes=True):
				# print(f'group =  {lgt_select}')

				for attr in transform_attributes:
					
					# Check if the attribute exists on the node
					if cmds.attributeQuery(attr, node=lgt_select, exists=True):

						group_name.append(f'{lgt_select}.{attr}')
						# print(f'{lgt_select}.{attr}')
			
		return group_name
	
	return 0

def get_attr_value(attributes):

	attr_value = []
	value = cmds.getAttr(attributes)

	return value

def create_json(attr_value_dict):

	directory = os.path.dirname(file_path)

	# Check if the directory exist
	if not os.path.exists(directory):
		print(f'Error: Directory does not exist - {directory}')
		return False

	# Writing data to a JSON file
	with open(file_path, 'w') as outfile:
		if outfile:
			# Combined_data need to check/ change
			json.dump(attr_value_dict, outfile, indent=4, sort_keys=True)
			print(f'Json file created: {file_path}')
		else:
			print('File output failed.')


# extract hierarchy data into list
def hierarchy_data(light_shapes):
	
	long_name_list = []
	
	hierarchy_full = cmds.ls(light_shapes, long=True)
	# print(hierarchy_full)

	for hierarchy in hierarchy_full:
		
		hierarchy = hierarchy.split('|')[1:]
	
		# print(hierarchy)
		long_name_list.append(hierarchy)

	# print(long_name_list)
	return long_name_list


#############################################################################################################

def read_json():

	# Reading data from the JSON file
	with open(file_path, 'r') as file:
		loaded_data = json.load(file)
			
	# pp.pprint(loaded_data)
	return loaded_data


def create_group_hierarchy(combined_dict):

	# Traversing long_name_list
	for sub in combined_dict['long_name_list']:
		sub.reverse()
		# print(sub)
		
		# Reset the parent_group variable for each sublist
		parent_group = None
		created_group = {}
		
		for item in sub:

			# Skip items that contain 'Light'
			if 'Light' in item:
				continue

			# Check if the group already exists
			if item in created_group:

				# Update the parent group if the group already exists
				parent_group = created_group[item]
				continue

			# Check if the group exist
			if cmds.objExists(item):

				# If exist, check the parent of the group and parent it
				parent_item = cmds.listRelatives(parent_group, parent=True)

				if not parent_item:
					if parent_group == None:
						continue
					cmds.parent(parent_group,item)

			else:
				# Create a new group under the current parent group
				if parent_group:
					new_group = cmds.group(parent_group, empty=False, name=item)
				else:
					new_group = cmds.group(empty=True, name=item)
				
				# Track the created group in the dictionary
				created_group[item] = new_group
			
				# Rename the current variable so the next loop does not override it
				parent_group = new_group

	grouped_hierarchy = parent_group

	return grouped_hierarchy


def create_light(combined_dict):

	# node_shape = None
	# node_name = None
	# node_type = None
	# node_parent = None

	for key, value in combined_dict['attribute_dict'].items():
			for key2, value2 in value.items():
				
				
				# Extract and assign variable to the keys
				if key2 == 'child_shape':
					node_shape = value[key2]
					# print(f'{key2}.{node_shape}')

				if key2 == 'name':
					node_name = value[key2]
					# print(node_name)

				if key2 == 'nodetype':
					node_type = value[key2]
					# print(node_type)
					
					# Create light shape node
					if 'transform' not in node_type:
						created_shape_node = cmds.createNode(node_type, name=node_name)
					
					# Create empty group transform node
					if 'transform' in node_type and not node_shape:
						created_grp_node = cmds.group(empty=True, name=node_name)



	for key, value in combined_dict['attribute_dict'].items():
			for key2, value2 in value.items():

				if key2 == 'parent':
					node_parent = value[key2]

					if not node_parent == None: # Condition to continue through if parent value is None/null
						if cmds.objectType(key)=='transform': # Checks for transform node on created group node
							cmds.parent(key, node_parent)
					# print(node_parent)
				



	# for key, value in combined_dict['attribute_dict'].items():
	# 		parent_switch= True
	# 		node_parent = []
	# 		for key2, value2 in value.items():

	# 			if key2 == 'parent':
	# 				node_parent = value[key2]
	# 				# print(node_parent)
				
	# 			if key2 == 'nodetype':
	# 				node_type = value[key2]
	# 				# print(node_type)
	# 				if not node_type == 'transform':
	# 					parent_switch =False

					
	# 				# cmds.parent(key, node_parent)
	# 				# # Parent the node
	# 				# 	# print(f'created_node.{created_node}')
	# 				# 	# print(f'node_name.{node_name}')

	# 		if parent_switch:
	# 			if node_parent == None:
	# 				continue
	# 			cmds.parent(key, node_parent)
					

def set_attribute(loaded_data):

	# Directly accessing 'attribute_dict'
	for key, value in loaded_data['attribute_dict'].items():
		for key2, value2 in value.items():
				
				# Exclude 'child_shape' data from setAttr
				if key2 == 'child_shape':
					continue

				# Exclude'name' data from setAttr
				elif key2 == 'name':
					continue
				
				# Exclude'nodetype' data from setAttr
				elif key2 == 'nodetype':
					continue

				# Exclude'parent' data from setAttr
				elif key2 == 'parent':
					continue

				# If the value is a list
				elif isinstance(value2, list):
					cmds.setAttr(key2, value2[0][0],value2[0][1],value2[0][2])
					# print(f'{key2} value successfully imported.')

				# setAttr for value type; bool, int, float
				else:
					cmds.setAttr(key2, value2)
					# print(f'{key2} value successfully imported.')

	print('Attributes successfully imported.')



#############################################################################################################

def main_export():

	light_types = [
		'aiAreaLight', 
		'pointLight', 
		'spotLight', 
		'directionalLight', 
		'areaLight', 
		'ambientLight', 
		'volumeLight'
	]

	light_shapes, light_transforms, light_groups = lgt_selection(light_types)
	# print(light_shapes, light_transforms, light_groups)
	# print(f'light_shapes = {light_shapes}')
	# print(f'light_transforms = {light_transforms}')
	# print(f'light_groups = {light_groups}')

	key1_shape_dict = {}
	# Getting shape nodes attributes name and value
	for lgt_shape in light_shapes:

		attribute_shape = get_attr_name(lgt_shape, light_types, light_nodes='shape')

		# Get the parent of each node
		parent_object = cmds.listRelatives(lgt_shape, parent=True)

		if parent_object is None:
			parent_object = parent_object
		else:
			parent_object = parent_object[0]


		# Get the node type
		node_types = cmds.nodeType(lgt_shape)

		key2_shape_dict = {}
		
		for shape in attribute_shape:
			shape_value = get_attr_value(shape)
			key2_shape_dict[shape] = shape_value

		key2_shape_dict['parent'] 	= parent_object # insert parent of node data
		key2_shape_dict['nodetype'] = node_types # insert node type data
		key2_shape_dict['name'] 	= lgt_shape # insert node name data
		key2_shape_dict['child_shape'] = False # insert if node has a shape node child
		key1_shape_dict[lgt_shape] 	= key2_shape_dict

	# pp.pprint(key1_shape_dict)
	# print('------------------------------------------------------------------')


	key1_transform_dict = {}
	# Getting transform nodes attributes name and value
	for lgt_transform in light_transforms:
	
		attribute_transform = get_attr_name(lgt_transform, light_types, light_nodes='transform')
		parent_object = cmds.listRelatives(lgt_transform, parent=True)

		if parent_object is None:
			parent_object = parent_object
		else:
			parent_object = parent_object[0]

		# Get the node type
		node_types = cmds.nodeType(lgt_transform)

		# child_shape = cmds.listRelatives(lgt_transform, children=True)
		
		key2_transform_dict = {}
		
		for transform in attribute_transform:
			transform_value = get_attr_value(transform)
			key2_transform_dict[transform] = transform_value
		
		key2_transform_dict['parent'] 		= parent_object # insert parent of node data
		key2_transform_dict['nodetype'] 	= node_types # insert node type data
		key2_transform_dict['name'] 		= lgt_transform # insert node name data
		key2_transform_dict['child_shape'] 	= True # insert if node has a shape node child
		key1_transform_dict[lgt_transform] 	= key2_transform_dict

	# pp.pprint(key1_transform_dict)
	# print('------------------------------------------------------------------')

	
	key1_group_dict = {}
	# Getting group transform nodes attributes name and value
	for lgt_group in light_groups:
		attribute_group = get_attr_name(lgt_group, light_types, light_nodes='group')
		parent_object = cmds.listRelatives(lgt_group, parent=True)
		
		if parent_object is None:
			parent_object = parent_object
		else:
			parent_object = parent_object[0]

		# Get the node type
		node_types = cmds.nodeType(lgt_transform)
		
		key2_group_dict = {}
		
		for group in attribute_group:
			group_value = get_attr_value(group)
			key2_group_dict[group] = group_value
		
		
		key2_group_dict['parent'] 	= parent_object # insert parent of node data
		key2_group_dict['nodetype'] = node_types # insert node type data
		key2_group_dict['name'] 	= lgt_group # insert node name data
		key2_group_dict['child_shape'] = False # insert if node has a shape node child
		key1_group_dict[lgt_group] 	= key2_group_dict

	# pp.pprint(key1_group_dict)
	# print('------------------------------------------------------------------')
	

	attribute_dict = {}

	# Combining all the dicts together
	attribute_dict.update(key1_group_dict)
	attribute_dict.update(key1_transform_dict)
	attribute_dict.update(key1_shape_dict)

	# Getting each shape's hierarchy 
	long_name_list = hierarchy_data(light_shapes)
	
	combined_dict = {
		'long_name_list': long_name_list,
		'attribute_dict': attribute_dict
	}

	# creating_json = create_json(combined_dict)

	

########################################################################################	

def main_import():
	
	read_json_file = read_json()
	
	create_light(read_json_file)

	set_attr = set_attribute(read_json_file)


########################################################################################	

# CALL YOUR FUNCTION HERE

# main_export()

main_import()


########################################################################################

