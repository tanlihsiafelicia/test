from PySide2 import QtCore, QtUiTools, QtWidgets, QtGui
from maya import OpenMayaUI as omu
from shiboken2 import wrapInstance
import maya.cmds as cmds
import mtoa.utils as mutils
import mtoa.aovs as aovs
import json
import os, sys
import re

import json
import pprint as pp 



a = cmds.xform('pSphere1', query=True, rotation=True)

a[0]

geo = 'pSphere1'

attr_name = geo + '.translateX'

b_attribute_list = cmds.listAttr(geo)

attr_list = []
value_list = []
for i_attribute in b_attribute_list:
	#print(attribute)
	if i_attribute in ['translateX', 'translateY', 'translateZ']:
		attr_list.append(i_attribute)

for j in attr_list:
	a = cmds.getAttr(geo + '.' + j)
	value_list.append(a)
	
# print(len(attr_list))

python_dict = {}
# python_dict = {'name': attr_list, 'an': {}}

another_dict = {'a': python_dict}

# print(type(python_dict))


for name, attr in zip(attr_list, value_list):
    print(name, attr)
    python_dict[name] = attr

# for i in range(0, len(attr_list)):
#     # assign each items to a temp variable
#     a = attr_list[i]
#     b = value_list[i]
    
#     # append key and value into your dict
#     #{[adding item into your keys]: adding item into the values }
#     python_dict[a] = b

print(python_dict)

# Serializing json
json_object = json.dumps(python_dict, indent=4)

# Writing to sample.json
with open("D:/Temp/sample.json", "w") as outfile:
    outfile.write(json_object)


#############


import json
import pprint as pp 

file_path = "D:/Temp/sample.json"

def import_json_data(file_path):
    # Open and read the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)

    return data

car = import_json_data(file_path)
print(type(car))

for key, val in car.items():
	print(key, val)
	cmds.setAttr('pSphere1.' + key, val)


#pp.pprint() 