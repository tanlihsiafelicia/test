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


# # extract hierarchy data into list
# def hierarchy_data(light_shapes):
	
# 	long_name_list = []
	
# 	hierarchy_full = cmds.ls(light_shapes, long=True)
# 	# print(hierarchy_full)

# 	for hierarchy in hierarchy_full:
		
# 		hierarchy = hierarchy.split('|')[1:]
	
# 		# print(hierarchy)
# 		long_name_list.append(hierarchy)

# 	# print(long_name_list)
# 	return long_name_list


#############################################################################################################

def read_json():

	# Reading data from the JSON file
	with open(file_path, 'r') as file:
		loaded_data = json.load(file)
			
	# pp.pprint(loaded_data)
	return loaded_data


def create_light(combined_dict):

	# node_shape = None
	# node_name = None
	# node_type = None
	# node_parent = None

	# Light creation
	for key, value in combined_dict['attribute_dict'].items():
		
		# Check scene for existing lights
		if cmds.objExists(key):
			# print(f'{key} exists in scene.')
			continue
		else:
			# print(f'{key} DOES NOT exists in scene.')


			# Get value of keys nodetype
			node_type = value.get('nodetype')

			# Create empty group transform node
			if 'transform' in node_type:
				created_grp_node = cmds.group(empty=True, name=key)

			# Create light shape node
			else: 
				created_shape_node = cmds.createNode(node_type, name=key)


	# Group parenting
	for key, value in combined_dict['attribute_dict'].items():

		# Get value of keys for parent
		node_parent = value.get('parent')

		# Get value of keys nodetype
		node_type = value.get('nodetype')

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
					lgt_transform = cmds.listRelatives(key, parent=True) # Assigns new var to lgt transform to be deleted later
					cmds.parent(key, node_parent, relative=True, shape=True) # Parents shape to transform & group node
					cmds.delete(lgt_transform[0]) # Delete unused lgt transform node
			# print('Objects successfully already parented.')
		
		# If object already parented
		else:
			print(f'{key} already parented.')
	
	print('Light successfully created.')



def set_pivot(combined_dict):

	# Directly accessing 'attribute_dict'
	for key, value in combined_dict['attribute_dict'].items():
		for key2, value2 in value.items():
			if key2 == 'pivot_data':
				# Get pivot data for object space
				pivot_rotate = value2.get('pivot_rotate')		
				pivot_scale = value2.get('pivot_scale')
				# print(f'{key}.pivot_world.{pivot_world}')

	
				# Set pivot rotate
				set_pivot_rotate = cmds.xform(key, objectSpace=True, rotatePivot=pivot_rotate)

				# Set pivot scale
				set_pivot_scale = cmds.xform(key, objectSpace=True, scalePivot=pivot_scale)

			# else:
			#     print(f"No pivot data found for {key}.")

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

			# If the value is a list (.color)
			elif isinstance(value2, list):
				cmds.setAttr(key2, value2[0][0],value2[0][1],value2[0][2])
				# print(f'{key2} value successfully imported.')

			# setAttr for value type; bool, int, float
			else:
				# print('here')
				cmds.setAttr(key2, value2)
				# print(f'{key2} value successfully imported.')

	# Iteration to connect HDR file
	for key, value in loaded_data['attribute_dict'].items():
		for key2, value2 in value.items():

			# If 'file_attached' is true, connect file 
			if key2 == 'file_attached' and isinstance(value2, str):

				hdr_file_path = value2
				
				# Create file node
				file_node = cmds.shadingNode('file', asTexture=True)
				# print(f'file_node: {file_node}')

				# if cmds.objExists(file_node):
				# 	print(f'file_node: {file_node}')

				# Set the HDR file path on the file node
				cmds.setAttr(f"{file_node}.fileTextureName", hdr_file_path, type="string")

				# Connect the file node's outColor to the DomeLight's color attribute
				if cmds.connectAttr(f"{file_node}.outColor", f"{key}.color", force=True):
					print ("HDR file connected to Dome Light.")

				else:
					print("No HDR file selected.")

	print('Attributes successfully imported.')



#############################################################################################################

def main_export():

	light_types = [
		'aiAreaLight',
		'aiSkyDomeLight',
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
		parent_object = cmds.listRelatives(lgt_shape, parent=True) or []

		# if parent_object is None:
		# 	parent_object = parent_object
		# else:
		# 	parent_object = parent_object[0]

		# Get the node type
		node_types = cmds.nodeType(lgt_shape)

		# Get the file path from the file node
		connections = cmds.listConnections(f"{lgt_shape}.color", type="file")
		
		if connections:
			file_node = connections[0]
			file_attached = cmds.getAttr(f"{file_node}.fileTextureName")
		else:
			file_attached = None

		key2_shape_dict = {}
		# Get attribute values
		for shape in attribute_shape:
			shape_value = get_attr_value(shape)
			key2_shape_dict[shape] = shape_value

		# key2_shape_dict['name'] 		= lgt_shape # insert node name data
		key2_shape_dict['child_shape']	= False # insert if node has a shape node child
		key2_shape_dict['parent']		= parent_object # insert parent of node data
		key2_shape_dict['nodetype']		= node_types # insert node type data
		key2_shape_dict['file_attached']= file_attached # insert file data if any
		key1_shape_dict[lgt_shape]		= key2_shape_dict

	# pp.pprint(key1_shape_dict)
	# print('------------------------------------------------------------------')


	key1_transform_dict = {}
	# Getting transform nodes attributes name and value
	for lgt_transform in light_transforms:
	
		attribute_transform = get_attr_name(lgt_transform, light_types, light_nodes='transform')
		parent_object = cmds.listRelatives(lgt_transform, parent=True) or []

		# if parent_object is None:
		# 	parent_object = parent_object
		# else:
		# 	parent_object = parent_object[0]

		# Get the node type
		node_types = cmds.nodeType(lgt_transform)
		
		# Get the object space pivot rotate
		pivot_rotate = cmds.xform(lgt_transform, query=True, objectSpace=True, rotatePivot=True)

		# Get the object space pivot scale
		pivot_scale = cmds.xform(lgt_transform, query=True, objectSpace=True, scalePivot=True)

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
		
		# key2_transform_dict.update({'pivot_world': pivot_world})
		# key2_transform_dict.update({'pivot_object': pivot_object})
		
		# key2_transform_dict['name'] 		= lgt_transform # insert node name data
		key2_transform_dict['child_shape'] 	= True # insert if node has a shape node child
		key2_transform_dict['parent'] 		= parent_object # insert parent of node data
		key2_transform_dict['nodetype'] 	= node_types # insert node type data
		key2_transform_dict['pivot_data'] 	= pivot_data # insert pivot object and world data
		key1_transform_dict[lgt_transform] 	= key2_transform_dict

	# pp.pprint(key1_transform_dict)
	# print('------------------------------------------------------------------')

	
	key1_group_dict = {}
	# Getting group transform nodes attributes name and value
	for lgt_group in light_groups:
		attribute_group = get_attr_name(lgt_group, light_types, light_nodes='group')
		parent_object = cmds.listRelatives(lgt_group, parent=True) or []
		
		# if parent_object is None:
		# 	parent_object = parent_object
		# else:
		# 	parent_object = parent_object[0]

		# Get the node type
		node_types = cmds.nodeType(lgt_group)
		
		# Get the object space pivot rotate
		pivot_rotate = cmds.xform(lgt_group, query=True, objectSpace=True, rotatePivot=True)

		# Get the object space pivot scale
		pivot_scale = cmds.xform(lgt_group, query=True, objectSpace=True, scalePivot=True)

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
		
		
		# key2_group_dict['name'] 		= lgt_group # insert node name data
		key2_group_dict['child_shape'] 	= False # insert if node has a shape node child
		key2_group_dict['parent'] 		= parent_object # insert parent of node data
		key2_group_dict['nodetype'] 	= node_types # insert node type data
		key2_group_dict['pivot_data'] 	= pivot_data # insert pivot object and world data
		key1_group_dict[lgt_group] 		= key2_group_dict

	# pp.pprint(key1_group_dict)
	# print('------------------------------------------------------------------')
	

	attribute_dict = {}

	# Combining all the dicts together
	attribute_dict.update(key1_group_dict)
	attribute_dict.update(key1_transform_dict)
	attribute_dict.update(key1_shape_dict)

	# Getting each shape's hierarchy 
	# long_name_list = hierarchy_data(light_shapes)
	
	# combined_dict = {
	# 	'long_name_list': long_name_list,
	# 	'attribute_dict': attribute_dict
	# }

	combined_dict = {
		'attribute_dict': attribute_dict
	}
	
	creating_json = create_json(combined_dict)

	

########################################################################################	

def main_import():
	
	read_json_file = read_json()
	
	create_light(read_json_file)

	set_pivot(read_json_file)

	set_attr = set_attribute(read_json_file)


########################################################################################	

# CALL YOUR FUNCTION HERE

# main_export()

main_import()


########################################################################################

