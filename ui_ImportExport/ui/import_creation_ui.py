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



def read_json():

	# Reading data from the JSON file
	with open(file_path, 'r') as file:
		loaded_data = json.load(file)

	pp.pprint(loaded_data)
	return loaded_data


def set_attribute(loaded_data):

	for key, value in loaded_data.items():
		
		for key2, value2 in value.items():
			# try:
			# List
			if isinstance(value2, list):
				cmds.setAttr(key2, value2[0][0],value2[0][1],value2[0][2])
				# print(f'{key2} value successfully imported.')

			else:
				cmds.setAttr(key2, value2)
				# print(f'{key2} value successfully imported.')

			# except Exception as e:
			# 	print(f"Error: {e}")

	print('------------------------------------------------------------------')	
	print('Import successful.')




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


########################################################################################	

def main_import():
	
	read_json_file = read_json()

	# set_attr = set_attribute(read_json_file)


########################################################################################	

# CALL YOUR FUNCTION HERE


main_import()


########################################################################################
