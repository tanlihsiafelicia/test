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
	light_transform = []
	light_group 	= []

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
		light_transform.append(transform_node[0])

		# Append group nodes into light_group list
		group_node = cmds.listRelatives(transform_node, parent = True)
		light_group.append(group_node[0])
	
	# print (light_shapes) # Output: ['Lgt_Key_Shape1', 'Lgt_Fill_Shape1', 'Lgt_Rim_L_Shape1']
	# print (light_transform)
	
	# print (light_group)
	return light_shapes, light_transform, light_group # tuple output, need to tuple unpack to access list inside


def get_attr_name(light_selection_list, light_types, light_nodes):

	## light_shapes = lgt_selection()[0] # Initialise the method then tuple unpack, index [0] for light_shapes
	
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

		for lgt_shapes in light_selection_list:

			if cmds.nodeType(lgt_shapes) in light_types:
				
				attributes = cmds.listAttr(lgt_shapes)

				for attr in attributes:
					if attr in common_attributes:
						attr_name.append(f'{lgt_shapes}.{attr}')
						## attr_name = attr_name + (lgt_shapes + '.' + attr,) # only for using tuple 
				
				# pp.pprint(attr_name)
		return attr_name

	
	if light_nodes == 'transform':
		# Iterate through only if light_transform
		for lgt_select in light_selection_list:

			if cmds.listRelatives(lgt_select, shapes=True):
				
				transforms = cmds.listAttr(lgt_select)
				
				for trans in transforms:
					if trans in transform_attributes:
						trans_name.append(f'{lgt_select}.{trans}')

				# pp.pprint(trans_name)
		return trans_name

	if light_nodes == 'group':

		for lgt_select in light_selection_list:
			# Iterate through only if light_group
			if cmds.nodeType(lgt_select) == 'transform' and 'Grp' in lgt_select:

				for attr in transform_attributes:
					
					# Check if the attribute exists on the node
					if cmds.attributeQuery(attr, node=lgt_select, exists=True):

						group_name.append(f'{lgt_select}.{attr}')
						# print(f'{lgt_select}.{attr}')
				
				# pp.pprint(group_name)
			return group_name
	
	return 0


	# return attr_name, trans_name, group_name # tuple output, need to tuple unpack to access list inside


	##############################################################################################################

	# This section is only to iterate through the attributes and return the value and value Type.
	# for lgt_shapes in light_shapes:
	# 	try:
	# 		# List all visible attributes

	# 		attributes = cmds.listAttr(lgt_shapes)
	# 		# pp.pprint(attributes)

	# 		for attr in attributes:
	# 			full_attr = f'{lgt_shapes}.{attr}'

	# 			try:
	# 				# Query the value of the attribute
	# 				value = cmds.getAttr(full_attr)
	# 				value_type = type(value)

	# 				print(f'Attribute: {full_attr}, Value: {value}, Type: {value_type}')
				
	# 			except Exception as e:
	# 				print(f'Could not retrieve attribute {attr}: {str(e)}')

	# 	except Exception as e:
	# 		print(f'Could not list attributes for {lgt_shapes}: {str(e)}')

	##############################################################################################################	


def get_attr_value(attributes):

	attr_value = []
	
	# pp.pprint(attributes)
	for attr in attributes:
		# print(attr)
		value = cmds.getAttr(attr)
		attr_value.append(value)

		#############################################################################################################		
		
		# This section is only to iterate through the attr and return the value and value Type.
		
		# value_type = type(value)
		# print(f'{attr}: {value}: {value_type}')
		# print(f'{attr}: {value}')
		
		#############################################################################################################

	# print(f'{attr}:	{value}')
	# print('--------------------------------------------------')
	# pp.pprint(attr_value)
	return attr_value


def create_dict(attributes, value):

	# Empty dict
	attr_value_dict = {}

	########################################################################################	
	
	# # Check list length
	# try:
	# 	if not len(attributes) == len(value):
	# 		print('Attributes and values lengths does not match.')
	# 		print(f'Attr length: {len(attributes)}\nValue length: {len(value)}')

	# except: 
	# 	pass

	########################################################################################
	
	# print(type(attributes))
	converted_attributes = tuple(attributes)
	# print(type(converted_attributes))
	# print(type(value))

	# Creating dict with {'key_attr':'value'}
	# attr_value_dict = dict(zip(converted_attributes, value))

	for attr, val in zip(converted_attributes, value):
		attr_value_dict[attr] = val

	# pp.pprint(attr_value_dict)
	return attr_value_dict


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


def read_json():

	# Reading data from the JSON file
	with open(file_path, 'r') as file:
		loaded_data = json.load(file)
			
	# pp.pprint(loaded_data)
	return loaded_data


def set_attribute(loaded_data):

	# loaded_data = read_json()
	# # pp.pprint (loaded_data)
	

	for key, value in loaded_data.items():
		# print (key)
		# print(f"'{key}' , {value}")
			
		# Check the value type and convert appropriately
		# try: 
		# Interger
		if isinstance(value, int):
			cmds.setAttr(key, int(value))
			print('Interger value successfully imported.')

		# Float
		elif isinstance(value, float):
			cmds.setAttr(key, float(value))
			print('Float value successfully imported.')

		# Boolean
		elif isinstance(value, bool):
			cmds.setAttr(key, bool(value))
			print('Boolean value successfully imported.')

		# List
		elif isinstance(value, list):
			cmds.setAttr(key, value[0][0],value[0][1],value[0][2])
			print('i did it.')
			print(f"{key}: {value} is a list of tuples.")


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

	light_shapes, light_transform, light_group = lgt_selection(light_types)
	# print(light_shapes, light_transform, light_group)

	# attr_name, trans_name, group_name = get_attr_name(light_shapes, light_types)
	# print(attr_name)
	# for light_shape in light_shapes
	attributes_shape 		= get_attr_name(light_shapes, light_types, light_nodes='shape')
	# pp.pprint(attributes_shape)
	attributes_transform 	= get_attr_name(light_transform, light_types, light_nodes='transform')
	# pp.pprint(attributes_transform)
	attributes_group 		= get_attr_name(light_group, light_types, light_nodes='group')
	# pp.pprint(attributes_group)

	shape_value 			= get_attr_value(attributes_shape)
	transform_value 		= get_attr_value(attributes_transform)
	group_value 			= get_attr_value(attributes_group)
	# # # print(attributes_shape)
	# # # print(shape_value)


	shape_dict				= create_dict (attributes_shape, shape_value)
	transform_dict			= create_dict (attributes_transform, shape_value)
	group_dict				= create_dict (attributes_group, shape_value)
	pp.pprint(shape_dict)
	pp.pprint(transform_dict)

	# new_dict = {}

	'''
	do a for loop here, 
	compare between light_shapes and attributes_shape 
	
	a = lgt_light.color comare with b = lgt_light
	if b in a:
		True

	top_group_dict = {}
	
	for light_shape in light_shapes:
		for attr_shape in atribute_shapes:
			if light_shape in attr_shape:
				top_group_dict[light_shape] = shape_dict


	'''


	# creating_json_file		= create_json(shape_dict, transform_dict, group_dict)

# 	print('help')


########################################################################################	

# CALL YOUR FUNCTION HERE

main_export()

########################################################################################

# def main_import():
	
# 	read_json_file			= read_json()
# 	set_attribute			= set_attribute(loaded_data)