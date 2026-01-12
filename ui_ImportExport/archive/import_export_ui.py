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


JSON_FILE_PATH = 'D:/Felicia/Script_D/ui_ImportExport/json/'




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
			'''
			# check this loop
			'''
			# print (lgt_shapes)

			# List all visible attributes
			attributes = cmds.listAttr(lgt_shapes)
			# pp.pprint(attributes)

			for attr in attributes:
				try:
					# Construct the attribute name
					self.object_attribute = f"{lgt_shapes}.{attr}"
					# print(object_attribute)
					
					# Get the default value of the attribute
					default_value = cmds.attributeQuery(attr, node=lgt_shapes, listDefault=True)
					# print(f"{attr}.{default_value}")

					# Skip attributes without default values
					if not default_value:
						continue

					# Get the current value of the attribute
					current_value = cmds.getAttr(self.object_attribute)
					# print(f"{lgt_shapes}.{attr}.{current_value[0]}")

					# Compare and collect if different
					if current_value != default_value:
						self.changed_attributes[self.object_attribute] = current_value[0]
						# print(f'{self.object_attribute}.{current_value[0]}')

				except:
					pass # Handle attributes that may not support querying default values

		pp.pprint(self.changed_attributes)
		# print(json.dumps(changed_attributes, indent=2))
		return self.changed_attributes
		
	def write_json(self):

		# Save to JSON file
		with open(file_path, "w") as file:
        	# json.dump(self.changed_attributes, file, indent=4, sort_keys=True)
			print(json.dump(self.changed_attributes, file, indent=4, sort_keys=True))

write_json(light_name, file_path)

ui = Import_Export_Light()


ui.lgt_selection()
ui.get_attributes()


# select_light = ui.lgt_selection()
# print(select_light[0]) # light_shapes
# print(select_light[1]) # light_transform
# print(select_light[2]) # light_group

# ui.lgt_translate(select_light)
# ui.lgt_rotate()
# ui.lgt_scale()



# def main():
	# ui.show()

