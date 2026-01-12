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
file_path = f"D:/Felicia/Script_D/ui_ImportExport/json/{file_name}"  # Combine path and file name



# class Import_Export_Light():

	# def __init__(self):
		# Initialize all objects and the light types


		# # getAttr from light translate xyz
		# self.lgt_translate_val = []
		# self.lgt_rotate_val = []
		# self.lgt_scale_val = []


# Loop through the outliner to select all the light transform and light shape
def lgt_selection(light_types):
	
	# Lists all objects in the scene
	light_shapes 	= []
	light_transforms = []
	light_groups 	= []

	# light_types = [
	# 	'aiAreaLight', 
	# 	'pointLight', 
	# 	'spotLight', 
	# 	'directionalLight', 
	# 	'areaLight', 
	# 	'ambientLight', 
	# 	'volumeLight'
	# ]

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

	
	if light_nodes == 'transform':

		if cmds.listRelatives(lgt_select, shapes=True):
			
			transforms = cmds.listAttr(lgt_select)
			
			for trans in transforms:
				if trans in transform_attributes:
					trans_name.append(f'{lgt_select}.{trans}')

		return trans_name


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

	# pp.pprint(attr_value)
	return value

def create_json(attr_value_dict):

	directory = os.path.dirname(file_path)

	# Check if the directory exist
	if not os.path.exists(directory):
		print(f"Error: Directory does not exist - {directory}")
		return False

	# Writing data to a JSON file
	with open(file_path, 'w') as outfile:
		if outfile:

			# # Combined_data need to check/ change
			# combined_date = {
			# 	'changed_attributes': changed_attributes,
			# }
			
			# Combined_data need to check/ change
			json.dump(attr_value_dict, outfile, indent=4, sort_keys=True)
			print(f'Json file created: {file_path}')
		else:
			print('File output failed.')


########################################################################################	

# extract hierarchy data into hierarchy_dict



def hierarchy_data(light_shapes):
	
	# hierarchy_dict = {}

	for shape in light_shapes:

		hierarchy_full = cmds.ls(light_shapes, long=True)
		# print(hierarchy_full)

	for hierarchy in hierarchy_full:
		
		hierarchy = hierarchy.split('|')[1:]
	
		print(hierarchy)
	
	

	
						# 	pointer_variable = hierarchy_dict

						# 	for H in hierarchy:

						# 		pointer_variable = pointer_variable.setdefault(H, {})

						# # pp.pprint(hierarchy_dict)
						# return hierarchy_dict
	# return hierarchy


########################################################################################	

def read_json():

	# Reading data from the JSON file
	with open(file_path, 'r') as file:
		loaded_data = json.load(file)
			
	# pp.pprint(loaded_data)
	return loaded_data

########################################################################################

# (done)
# create sub categort dict; hierarchy_dict, attribute_dict = combined_dict


# when in new scene

# check if obj (shape, transforms nodes exist)
# if no, then recreate
# if yes recreate hierarchy
# use for looop hierarchy_dict to iterate through which what transform node to extract and iterate through combined_dict for attribute data


# (done. NEED TO UPDATE AGAIN)
# need to update set_attribute function for additional iteration
# combined_dict = {
# 	'hierarchy_dict': hierarchy_dict,
# 	'attribute_dict': attribute_dict
# }

def check_existence(combined_dict):
	
	# for:
	# 	if cmds.objExists('surface1'):

	stack = [(combined_dict, [])]  # Stack holds (current_dict, path_to_current_dict)

	while stack:
		current, path = stack.pop()  # Get the current dictionary and its path

		for key, value in current.items():
			new_path = path + [key]  # Extend the path
			
			if isinstance(value, dict):  # If the value is a dictionary, add it to the stack
				stack.append((value, new_path))
			else:
				# Process the value (or just print it with its path)
				print(f"Path: {'.'.join(map(str, new_path))} -> Value: {value}")















########################################################################################

def set_attribute(loaded_data):

	# loaded_data = read_json()
	# # pp.pprint (loaded_data)
	

	for key, value in loaded_data.items():
		for key2, value2 in value.items():
			for key3, value3 in value2.items():
				# try:
				
				if key3 == 'parent':
					print(f'{key3}.{value3}')
					continue

				# If the value is a list
				elif isinstance(value3, list):
					cmds.setAttr(key3, value3[0][0],value3[0][1],value3[0][2])
					# print(f'{key3} value successfully imported.')

				# setAttr for value type; bool, int, float
				else:
					cmds.setAttr(key3, value3)
					# print(f'{key3} value successfully imported.')

				# except Exception as e:
				# 	print(f"Error: {e}")







			# print (key2)
		# print (key)
		# print(f"'{key}' , {value}")
		# print(value)
			
		# Check the value type and convert appropriately
		# try: 
		# # Interger
		# if isinstance(value, int):
		# 	cmds.setAttr(key, int(value))
		# 	print('Interger value successfully imported.')

		# # Float
		# elif isinstance(value, float):
		# 	cmds.setAttr(key, float(value))
		# 	print('Float value successfully imported.')

		# # Boolean
		# elif isinstance(value, bool):
		# 	cmds.setAttr(key, bool(value))
		# 	print('Boolean value successfully imported.')

		# # List
		# elif isinstance(value, list):
		# 	cmds.setAttr(key, value[0][0],value[0][1],value[0][2])
		# 	print('i did it.')
		# 	print(f"{key}: {value} is a list of tuples.")


#############################################################################################################







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

	key1_shape_dict = {}
		
	for lgt_shape in light_shapes:
		# print(lgt_shape)
		
		attribute_shape = get_attr_name(lgt_shape, light_types, light_nodes='shape')
		# print(attribute_shape)
		
		key2_shape_dict = {}
		
		for shape in attribute_shape:

			shape_value = get_attr_value(shape)

			key2_shape_dict[shape] = shape_value
		
		key1_shape_dict[lgt_shape] = key2_shape_dict

	# pp.pprint(key1_shape_dict)
	# print('------------------------------------------------------------------')


	key1_transform_dict = {}
		
	for lgt_transform in light_transforms:
		# print(lgt_transform)
		
		attribute_transform = get_attr_name(lgt_transform, light_types, light_nodes='transform')
		# print(attribute_transform)
		
		key2_transform_dict = {}
		
		for transform in attribute_transform:

			transform_value = get_attr_value(transform)

			key2_transform_dict[transform] = transform_value
		
		key1_transform_dict[lgt_transform] = key2_transform_dict

	# pp.pprint(key1_transform_dict)
	# print('------------------------------------------------------------------')

	
	key1_group_dict = {}
		
	for lgt_group in light_groups:
		# print(lgt_group)
		
		attribute_group = get_attr_name(lgt_group, light_types, light_nodes='group')
		# print(attribute_group)
		
		key2_group_dict = {}
		
		for group in attribute_group:

			group_value = get_attr_value(group)

			key2_group_dict[group] = group_value
		
		key1_group_dict[lgt_group] = key2_group_dict

	# pp.pprint(key1_group_dict)
	# print('------------------------------------------------------------------')
	
	# attribute_dict = {}

	# attribute_dict.update(key1_group_dict)
	# attribute_dict.update(key1_transform_dict)
	# attribute_dict.update(key1_shape_dict)
	# pp.pprint(attribute_dict)


	hierarchy_dict = hierarchy_data(light_shapes)
	
	# combined_dict = {
	# 	'hierarchy_dict': hierarchy_dict,
	# 	'attribute_dict': attribute_dict
	# }
	# pp.pprint(combined_dict)

	combined_dict = {}

	combined_dict.update(key1_group_dict)
	combined_dict.update(key1_transform_dict)
	combined_dict.update(key1_shape_dict)
	# pp.pprint(combined_dict)


	# creating_json = create_json(combined_dict)

	# check_existence(combined_dict)

########################################################################################	

def main_import():
	
	read_json_file = read_json()

	check_existence(combined_dict)
	
	# set_attr = set_attribute(read_json_file)


########################################################################################	

# CALL YOUR FUNCTION HERE

main_export()

# main_import()


########################################################################################

