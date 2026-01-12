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



class Import_Export_Light():

	def __init__(self):
		# Initialize all objects and the light types

		# Lists all objects in the scene


		self.light_shapes = []
		self.light_transform = []
		self.light_group = []

		self.light_types = [
			'aiAreaLight', 
			'pointLight', 
			'spotLight', 
			'directionalLight', 
			'areaLight', 
			'ambientLight', 
			'volumeLight'
		]

		self.all_objects = cmds.ls(type=self.light_types)

		self.changed_attributes = {}
		self.changed_transform_attributes = {}
		



		# # getAttr from light translate xyz
		# self.lgt_translate_val = []
		# self.lgt_rotate_val = []
		# self.lgt_scale_val = []


	# Loop through the outliner to select all the light transform and light shape
	def lgt_selection(self):

		# Loop through all obj in outliner
		for obj in self.all_objects:
			node_type = cmds.nodeType(obj) # Get the node type of the object

			# Check if node matches light_types and append it into light_shapes list
			if node_type in self.light_types:
				self.light_shapes.append(obj)
				
				# Append transform nodes into light_transform list
				transform_node = cmds.listRelatives(obj, parent = True)
				self.light_transform.append(transform_node[0])

				# Append group nodes into light_group list
				group_node = cmds.listRelatives(transform_node, parent = True)
				self.light_group.append(group_node[0])
		
		# print (self.light_shapes) # output: ['Lgt_Key_Shape1', 'Lgt_Fill_Shape1', 'Lgt_Rim_L_Shape1']
		# print (self.light_transform)
		# print (self.light_group)
		# return self.light_shapes, self.light_transform, self.light_group # tuple output, need to tuple unpack to access list inside


	def get_attributes(self):

		for lgt_shapes in self.light_shapes:
			
			##############################################################################################################

			# this section is only to iterate through the attributes and return the value and value Type.
			# try:
				# List all visible attributes
			attributes = cmds.listAttr(lgt_shapes)
			pp.pprint(attributes)

			# 	for attr in attributes:
			# 		full_attr = f"{lgt_shapes}.{attr}"

			# 		try:
			# 			# Query the value of the attribute
			# 			value = cmds.getAttr(full_attr)
			# 			value_type = type(value)

			# 			print(f"Attribute: {full_attr}, Value: {value}, Type: {value_type}")
					
			# 		except Exception as e:
			# 			print(f"Could not retrieve attribute {attr}: {str(e)}")

			# except Exception as e:
			# 	print(f"Could not list attributes for {lgt_shapes}: {str(e)}")

			##############################################################################################################	



















					# 			if cmds.attributeQuery(attr, node=lgt_shapes, message=True):
					# print(f'{lgt_shapes}.{attr} is a message and has no data value.')

					# # Retrieve the attribute value
					# value = cmds.getAttr(f"{lgt_shapes}.{attr}")
					# value_type = type(value)
					# print(f"Attribute: {lgt_shapes}.{attr}, Value: {value}, Type: {value_type}")


				# for attr in attributes:

				# Skips compound
				# if '.' in attr:
				# 	# print(f'{lgt_shapes}.{attr}')
				# 	continue

				# if cmds.attributeQuery(attr, node=lgt_shapes, message=True):
				# 	# print(f'{lgt_shapes}.{attr} is a message and has no data value.')
				# 	continue

				# Could not retrieve attribute message: Message attributes have no data values.
			

				# if not cmds.attributeQuery(attr, node=lgt_shapes, connectable=True):
				# 	print(f'{lgt_shapes}.{attr} is a non-connectable attribute.')


					# try:
					# 	# Check if the attribute exists on the object

					# 	if cmds.attributeQuery(attr, node=lgt_shapes, message=True):
					# 		print(f'{lgt_shapes}.{attr} is a message and has no data value.')

					# 	if cmds.attributeQuery(attr, node=lgt_shapes, exists=True):
					# 		# Retrieve the attribute value
					# 		value = cmds.getAttr(f"{lgt_shapes}.{attr}")
					# 		value_type = type(value)
					# 		print(f"Attribute: {lgt_shapes}.{attr}, Value: {value}, Type: {value_type}")
					# 	else:
					# 		print(f"Could not retrieve attribute {attr}: Attribute does not exist on {lgt_shapes}.")
					# except RuntimeError as e:
					# 	print(f"Could not retrieve attribute {attr}: {str(e)}")
					# except TypeError as e:
					# 	print(f"Could not retrieve attribute {attr}: {str(e)}")


		# for lgt_shapes in self.light_shapes: 

		# # 	# List all visible attributes
		# 	attributes = cmds.listAttr(lgt_shapes)
		# 	# split_text = attributes.split(',')
		# 	# print(f'{lgt_shapes}.{attributes}')
		# 	# pp.pprint(attributes)
			
		# 	for attr in cmds.listAttr(lgt_shapes):

		# 		# Skips compound
		# 		if '.' in attr:
		# 			# print(f'{lgt_shapes}.{attr}')
		# 			continue

		# 		if cmds.attributeQuery(attr, node=lgt_shapes, message=True):
		# 			# print(f'{lgt_shapes}.{attr} is a message and has no data value.')
		# 			continue


		# 		if not cmds.attributeQuery(attr, node=lgt_shapes, connectable=True):
		# 			# print(f'{lgt_shapes}.{attr} is a non-connectable attribute.')
		# 			continue
		# 			# binMembership
		# 			# isHierarchicalConnection
		# 			# rmbCommand
		# 			# underWorldObject

				


# search for
# not hidden and keyable

# query for name clash
# cmds.ls(long=True)

		# pp.pprint(self.changed_attributes)
		# print(json.dumps(changed_attributes, indent=2))
		# return self.changed_attributes


	# def get_transform_attributes(self):

	# 	for lgt_transform in self.light_transform:
			
	# 		# print (lgt_transform)

	# 		# Get attr value for transform nodes
	# 		transform_attributes = cmds.listAttr(lgt_transform)
	# 		# pp.pprint(transform_attributes)

	# 		for transform in transform_attributes:
	# 			# pp.pprint(transform)

	# 			try:
	# 				# Construct the attribute name
	# 				object_attribute = f"{lgt_transform}.{attr}"
	# 				# print(object_attribute)
					
	# 				# Get the default value of the attribute
	# 				default_transform_value = cmds.attributeQuery(attr, node=lgt_transform, listDefault=True)
	# 				# print(f"{transform}.{default_transform_value}")

	# 				# Skip attributes without default values
	# 				if not default_transform_value:
	# 					continue

	# 				# Get the current value of the attribute
	# 				current_value = cmds.getAttr(object_attribute)
	# 				# print(f"{lgt_transform}.{transform}.{current_value[0]}")

	# 				# Compare and collect if different
	# 				if current_value != default_transform_value:
	# 					self.changed_attributes[object_attribute] = current_value[0]
	# 					# print(f'{self.object_attribute}.{current_value[0]}')

	# 			except:
	# 				pass # Handle attributes that may not support querying default values

	# 	# pp.pprint(self.changed_attributes)
	# 	# print(json.dumps(self.changed_attributes, indent=2))
	# 	return self.changed_transform_attributes
		

	def create_json(self):

		self.directory = os.path.dirname(file_path)

		# Check if the directory exist
		if not os.path.exists(self.directory):
			print(f"Error: Directory does not exist - {self.directory}")
			return False

		# Writing data to a JSON file
		with open(file_path, 'w') as outfile:
			if outfile:

				combined_date = {
					'changed_attributes':self.changed_attributes,
					# 'changed_transform_attributes': self.changed_transform_attributes
				}
				
				json.dump(self.combined_date, outfile, indent=4, sort_keys=True)
				print(f'Json file created: {file_path}')
			else:
				print('File output failed.')


	def read_json(self):

		# Reading data from the JSON file
		with open(file_path, 'r') as file:
			loaded_data = json.load(file)
				
		# pp.pprint(loaded_data)
		return loaded_data


	def set_attribute(self):

		self.attribute_type = {
			'double3': 3,
			'double2': 2,
		}

		json_data = self.read_json()

		for key, value in json_data.items():
			aov_key_name = key.split('.',1)[0] # shape_name
			# print(aov_key_name)
			
			aov_attr_name = key.split('.',1)[1] # attr_name
			# print(aov_attr_name)

			for key2, value2 in self.attribute_type.items():
				if len(value) == value2:
						attr_type = key2
						# break
						cmds.setAttr(key, *value, type = attr_type)
						print(f'{key}.{value} imported.')


				# try:
				# 	if len(value) == value2:
				# 		attr_type = key2
				# 		# break
				# 		cmds.setAttr(key, *value, type = attr_type)
				# 		print(f'{key}.{value} imported.')
				
				# except:
				# 	raise ValueError(f"Invalid attribute type or value length for {key}.'{attr_type}': {value}")
				
				# print('Attributes successfully imported.')
				

			# else:
			# 	print('Action failed.')




ui = Import_Export_Light()


ui.lgt_selection()
ui.get_attributes()
# ui.get_transform_attributes()
# ui.create_json()
# ui.read_json()
# ui.set_attribute()


# select_light = ui.lgt_selection()
# print(select_light[0]) # light_shapes
# print(select_light[1]) # light_transform
# print(select_light[2]) # light_group

# ui.lgt_translate(select_light)
# ui.lgt_rotate()
# ui.lgt_scale()



# def main():
	# ui.show()

