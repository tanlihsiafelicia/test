import maya.cmds as cmds
import mtoa.utils as mutils
import mtoa.aovs as aovs
import json
import os, sys
import re
import pprint as pp

file_name = 'TEST_2.json'  # File name
file_path = f'D:/Felicia/Script_D/ui_ImportExport/json/{file_name}'  # Combine path and file name

def read_json(file_path):

	# Reading data from the JSON file
	with open(file_path, 'r') as file:
		loaded_data = json.load(file)
			
	# pp.pprint(loaded_data)
	print('json file loaded.')
	return loaded_data


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


def main_import(namespace, file_path):

	read_json_file = read_json(file_path)
	
	insert_namespace = namespace

	# Add namespace into new dict 
	added_namespace = adding_namespace(insert_namespace, read_json_file)

	# Clear all selection
	cmds.select(cl=True)

	if insert_namespace == '': # WITHOUT namespace
		print('WITHOUT namespace')
		for key, value in read_json_file['attribute_dict'].items():
			lgtrig_exist = cmds.objExists(key) # Checks scene and compare with json (for no namespace)

			if lgtrig_exist: # If light rig EXIST
				print(f'{key}: light EXIST, WITHOUT namespace')
				# set_attr 		= set_attribute(read_json_file)
				# import_anim 	= import_animExport(animExport_file_path)

			else: # If light rig NOT EXIST
				print(f'{key}: light NOTTTTTTTTTTTTTTT EXIST, WITHOUT namespace')
				# creating_create_light	= create_light(read_json_file)
				# creating_create_curve	= create_curve(read_json_file)
				# creating_custom_attr	= create_custom_attr(read_json_file)
				# setting_pivot			= set_pivot(read_json_file)
				# seting_attr 			= set_attribute(read_json_file)
				# import_anim 			= import_animExport(animExport_file_path)

	else: # WITH namespace
		print('WITH namespace')
		for key, value in added_namespace['attribute_dict'].items():
			namespace_lgtrig_exist = cmds.objExists(key)

			if namespace_lgtrig_exist: # Lights alr exist in scene
				print('light EXIST with namespace')
				set_attr 		= set_attribute(added_namespace)
				import_anim 	= import_animExport(animExport_file_path)
			
			else: # Lights alr exist in scene
				print('light NOT EXIST with namespace')
				creating_create_light	= create_light(added_namespace)
				creating_create_curve	= create_curve(added_namespace)
				creating_custom_attr	= create_custom_attr(added_namespace)
				setting_pivot			= set_pivot(added_namespace)
				seting_attr 			= set_attribute(added_namespace)
				import_anim 			= import_animExport(animExport_file_path)


########################################################################################

print('########################################################################################')

namespace = ''
main_import(namespace, file_path)