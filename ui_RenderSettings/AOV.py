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


# Class instances
mainObject = omu.MQtUtil.mainWindow()
mayaMainWind = wrapInstance(int(mainObject), QtWidgets.QWidget)
aov_interface = aovs.AOVInterface()



JSON_FILE_PATH = "D:/Felicia/Script_D/ui_RenderSettings/json/Sample_AOVs.json"

# NOTES
# add check if arnold plug in is loaded
# if not pass, or load it
# or raise warning

# dictionary of aov data types : indexing
aov_data_type = {
    "int":1,
    "unit":2,
    "bool":3, 
    "float":4,
    "rgb": 5,
    "rgba":6,
    "vector":7, 
    "vector2":8,
    "pointer":9 
    }

def import_json_data(JSON_FILE_PATH):
    # Open and read the JSON file
    with open(JSON_FILE_PATH, 'r') as file:
        loaded_json_data = json.load(file)

    return loaded_json_data


json_data = import_json_data(JSON_FILE_PATH)
    # print(type(json_data))

def create_aov():
    # this is where you access the data in your nested chaos dictionary
    for key, val in json_data.items(): # accessing dict arnold : {"aov", "drivers", "filters", "outputs"}
        # print(key, val)
        for key2, val2 in val.items(): # accessing dict aov : {"N":N.binMembership}
            # pp.pprint (val2)
            if key2 == "aovs": # isolating singular key out of others. only looping within aov
                # pp.pprint(key2)
                for aov_list in val2: # accessing list
                    # pp.pprint(val2)
                    # print(val2)
                    for key3, val3 in aov_list.items(): # accessing dict {aov: aov_types} *tuple unpacking
                        aov_key_name = key3.split('_', 1)[1] # extracting aov name
                        # aov_interface.addAOV(aov_key_name)  # add aov                        
                        
                        # pp.pprint(val3)

                        # #
                        for key4, val4 in val3.items():
                            attr_name = key4.split('_',1)[1]
                            print (attr_name)
                            # pp.pprint(val4)

                            aov_name = attr_name.split('.',1)[0]
                            # pp.pprint (aov_name)

                            # if val4 == "":
                            #     # print(f"{attr_name} has no value inside.")
                            #     pass
                            # elif val4 == None:
                            #     # print(f"{attr_name} : null.")
                            #     pass

                            # elif aov_name == val4:
                            #     # print (val4)
                            #     pass

                            # else:
                            #     # cmds.setAttr(key4, val4)
                            #     pass

#TEST CALL FUNCTONS/ METHODS
import_json_data(JSON_FILE_PATH)
create_aov()






def check_aiUtility_exist(aov_uv_node):
    aov_uv_node = "aiAOV_UV"
    # Check and create "aiUtility1" node if it does not exist
    if not cmds.objExists("aiUtility1"):
        utility_node = cmds.createNode("aiUtility", name="aiUtility1")  # Create the utility node
        print(f"Created node: {utility_node}")
    else:
        utility_node = "aiUtility1"  # If it exists, set a reference to it

    # Connect "aiUtility1.outColor" to "aiAOV_UV.defaultValue"
    cmds.connectAttr(f"{utility_node}.outColor", f"{aov_uv_node}.defaultValue", force=True)
    print("Connected aiUtility1.outColor to aiAOV_UV.defaultValue.")


#TEST CALL FUNCTONS/ METHODS
import_json_data(JSON_FILE_PATH)
create_aov()
# check_aiUtility_exist(aov_uv_node)


#     # #for uv
#     # setAttr "aiUtility1.shadeMode" 2;
#     # setAttr "aiUtility1.colorMode" 5;


#     # Connect "aiUtility1.outColor" to "aiAOV_UV.defaultValue"
#     cmds.connectAttr(f"{utility_node}.outColor", f"{aov_uv_node}.defaultValue", force=True)
#     print("Connected aiUtility1.outColor to aiAOV_Uv.defaultValue.")

#                         else:
#                             cmds.setAttr(key4, val4)



#                     for key4, val4 in val3.items(): # accessing dict {.attr_name : attr_value}
#                         pp.pprint(val4)
#                         cmds.setAttr(key4, val4)
#                         # pp.pprint(key4)

