from PySide2 import QtCore, QtUiTools, QtWidgets, QtGui
from maya import OpenMayaUI as omu
from shiboken2 import wrapInstance
import maya.cmds as cmds
import os, sys
import maya.mel as mel
import re  # To use regular expressions for extracting numbers

SCRIPT_FILE_PATH = 'D:/Felicia/Script_D/ui_Character_LgtRig/'
mainObject = omu.MQtUtil.mainWindow()
mayaMainWind = wrapInstance(int(mainObject), QtWidgets.QWidget)

class CharacterLightRig(QtWidgets.QWidget):    
    
    def __init__(self,parent=mayaMainWind):
        
        super(CharacterLightRig, self).__init__(parent=parent)
                   
        if(__name__ == '__main__'):
            self.ui = SCRIPT_FILE_PATH + '/ui/character_light_rig_test.ui'
        else:
            self.ui = os.path.abspath(os.path.dirname(__file__) +'/ui/character_light_rig_test.ui')
        
        self.setAcceptDrops(True)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setWindowTitle('character light rig')
        self.setFixedSize(320, 220)  # Locks the window size

        loader = QtUiTools.QUiLoader()
        ui_file = QtCore.QFile(self.ui)
        ui_file.open(QtCore.QFile.ReadOnly)
        self.theMainWidget = loader.load(ui_file)
        ui_file.close()

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(self.theMainWidget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)
        
        self.theMainWidget.Create_Key_Light_pushButton.clicked.connect(self.Create_Key_Light)
        self.theMainWidget.Create_Fill_Light_pushButton.clicked.connect(self.Create_Fill_Light)
        self.theMainWidget.Create_Rim_L_Light_pushButton.clicked.connect(self.Create_Rim_L_Light)
        self.theMainWidget.Create_Rim_R_Light_pushButton.clicked.connect(self.Create_Rim_R_Light)
        self.theMainWidget.Create_Bounce_Light_pushButton.clicked.connect(self.Create_Bounce_Light)
        self.theMainWidget.Group_All_Lights_pushButton.clicked.connect(self.Create_Group_All_Lights)

        self.light_counts = {
            "Key": 1,
            "Fill": 1,
            "Rim_L": 1,
            "Rim_R": 1,
            "Bounce": 1
        }

    def Create_Group_All_Lights(self):
        self.Create_Key_Light()
        self.Create_Fill_Light()
        self.Create_Rim_L_Light()
        self.Create_Rim_R_Light()
        self.Create_Bounce_Light()

    def Create_Key_Light(self):

        global light_counts  # Use the global dictionary for counts

        # Generate a unique light name before creating the light
        light_name = "Lgt_Key_" + str(self.light_counts["Key"]).zfill(2)
        
        # Create Keylight with the unique name
        Lgt_Key = cmds.directionalLight(name=light_name)

        # Check if light creation was successful
        if not Lgt_Key:
            raise RuntimeError("Failed to create DirectionalLight.")
        else:
            print(f"{light_name} successfully created.")

        # Group the key light and rename the group
        Key_group = cmds.group(Lgt_Key, name="Lgt_Key_Grp_" + str(self.light_counts["Key"])).zfill(2)

        # Check if group creation was successful
        if not Key_group:
            raise RuntimeError("Failed to group DirectionalLight.")

        # Set the translateZ of the light group to 50
        cmds.setAttr(Key_group + ".translateZ", 50)

        # Move the pivot of the light group to (0, 0, 0) without affecting its position
        cmds.xform(Key_group, pivots=(0, 0, 0), worldSpace=True)

        # Move the pivot of the light itself to (0, 0, 0) without affecting its position
        cmds.xform(light_name, pivots=(0, 0, 0), worldSpace=True)

        # Set the light's rotation: rotateX = -40, rotateY = -45
        cmds.setAttr(light_name + ".rotateX", -40)
        cmds.setAttr(light_name + ".rotateY", -45)
        cmds.setAttr(light_name + ".scaleZ", 50)
        cmds.setAttr(light_name + ".scaleX", 50)
        cmds.setAttr(light_name + ".scaleY", 50)

        # Increment the count for the Key prefix
        self.light_counts["Key"] += 1

    def Create_Fill_Light(self):
            global light_counts  # Use the global dictionary for counts

            # Generate a unique light name before creating the light
            light_name = "Lgt_Fill_" + str(self.light_counts["Fill"]).zfill(2)

            # Create a VRay Rectangular Light
            Lgt_Fill = cmds.shadingNode('VRayLightRectShape', asLight=True)

            # Check if light creation was successful
            if not Lgt_Fill:
                raise RuntimeError("Failed to create VRayLightRectShape.")
            else:
                print(f"{light_name} successfully created.")

            # Rename the light to the generated name
            Lgt_Fill = cmds.rename(Lgt_Fill, light_name)

            # Group the light and rename the group
            Fill_group = cmds.group(Lgt_Fill, name="Lgt_Fill_Grp_" + str(self.light_counts["Fill"]))

            # Set the translation of the light group
            cmds.setAttr(Fill_group + ".translateZ", 10)

            # Move the pivot of the light group to (0, 0, 0) without affecting its position
            cmds.xform(Fill_group, pivots=(0, 0, 0), worldSpace=True)

            # Move the pivot of the light itself to (0, 0, 0) without affecting its position
            cmds.xform(Lgt_Fill, pivots=(0, 0, 0), worldSpace=True)

            # Get the shape node(s) of the light
            light_shape = cmds.listRelatives(Lgt_Fill, shapes=True)

            # Check if light shape was found    
            if not light_shape:
                raise RuntimeError("Light shape not found.")
            
            # Move the pivot of the light shape to (0, 0, 0) without affecting its position
            cmds.xform(light_shape[0], pivots=(0, 0, 0), worldSpace=True)

            # Set the light's rotation: rotateX = -40, rotateY = 45
            cmds.setAttr(light_name + ".rotateX", -40)
            cmds.setAttr(light_name + ".rotateY", 45)
            cmds.setAttr(light_name + ".scaleZ", 50)
            cmds.setAttr(light_name + ".scaleX", 50)
            cmds.setAttr(light_name + ".scaleY", 50)

            # Increment the count for the Fill prefix
            self.light_counts["Fill"] += 1

    def Create_Rim_L_Light(self):
        global light_counts  # Use the global dictionary for counts

        # Generate a unique light name before creating the light
        light_name = "Lgt_Rim_L_" + str(self.light_counts["Rim_L"]).zfill(2)

        # Create a VRay Rectangular Light
        Lgt_Rim_L = cmds.shadingNode('VRayLightRectShape', asLight=True)

        # Check if light creation was successful
        if not Lgt_Rim_L:
            raise RuntimeError("Failed to create VRayLightRectShape.")
        else:
            print(f"{light_name} successfully created.")

        # Rename the light to the generated name
        Lgt_Rim_L = cmds.rename(Lgt_Rim_L, light_name)

        # Group the light and rename the group
        Rim_L_group = cmds.group(Lgt_Rim_L, name="Lgt_Rim_L_Grp_" + str(self.light_counts["Rim_L"]))

        # Set the translation of the light group
        cmds.setAttr(Rim_L_group + ".translateZ", 10)

        # Move the pivot of the light group to (0, 0, 0) without affecting its position
        cmds.xform(Rim_L_group, pivots=(0, 0, 0), worldSpace=True)

        # Move the pivot of the light itself to (0, 0, 0) without affecting its position
        cmds.xform(Lgt_Rim_L, pivots=(0, 0, 0), worldSpace=True)

        # Get the shape node(s) of the light
        light_shape = cmds.listRelatives(Lgt_Rim_L, shapes=True)

        # Check if light shape was found    
        if not light_shape:
            raise RuntimeError("Light shape not found.")
        
        # Move the pivot of the light shape to (0, 0, 0) without affecting its position
        cmds.xform(light_shape[0], pivots=(0, 0, 0), worldSpace=True)

        # Set the light's rotation: rotateX = -40, rotateY = 225
        cmds.setAttr(light_name + ".rotateX", -40)
        cmds.setAttr(light_name + ".rotateY", 225)
        cmds.setAttr(light_name + ".scaleZ", 50)
        cmds.setAttr(light_name + ".scaleX", 50)
        cmds.setAttr(light_name + ".scaleY", 50)

        # Increment the count for the Rim_L prefix
        self.light_counts["Rim_L"] += 1



    def Create_Rim_R_Light(self):
        global light_counts  # Use the global dictionary for counts

        # Generate a unique light name before creating the light
        light_name = "Lgt_Rim_R_" + str(self.light_counts["Rim_R"]).zfill(2)

        # Create a VRay Rectangular Light
        Lgt_Rim_R = cmds.shadingNode('VRayLightRectShape', asLight=True)

        # Check if light creation was successful
        if not Lgt_Rim_R:
            raise RuntimeError("Failed to create VRayLightRectShape.")
        else:
            print(f"{light_name} successfully created.")

        # Rename the light to the generated name
        Lgt_Rim_R = cmds.rename(Lgt_Rim_R, light_name)

        # Group the light and rename the group
        Rim_R_group = cmds.group(Lgt_Rim_R, name="Lgt_Rim_R_Grp_" + str(self.light_counts["Rim_R"]))

        # Set the translation of the light group
        cmds.setAttr(Rim_R_group + ".translateZ", 10)

        # Move the pivot of the light group to (0, 0, 0) without affecting its position
        cmds.xform(Rim_R_group, pivots=(0, 0, 0), worldSpace=True)

        # Move the pivot of the light itself to (0, 0, 0) without affecting its position
        cmds.xform(Lgt_Rim_R, pivots=(0, 0, 0), worldSpace=True)

        # Get the shape node(s) of the light
        light_shape = cmds.listRelatives(Lgt_Rim_R, shapes=True)

        # Check if light shape was found       
        if not light_shape:
            raise RuntimeError("Light shape not found.")

        # Move the pivot of the light itself to (0, 0, 0) without affecting its position
        cmds.xform(light_shape[0], pivots=(0, 0, 0), worldSpace=True)

        # Set the light's rotation: rotateX = -40, rotateY = 135
        cmds.setAttr(light_name + ".rotateX", -40)
        cmds.setAttr(light_name + ".rotateY", 135)
        cmds.setAttr(light_name + ".scaleZ", 50)
        cmds.setAttr(light_name + ".scaleX", 50)
        cmds.setAttr(light_name + ".scaleY", 50)

        # Increment the count for the Rim_R prefix
        self.light_counts["Rim_R"] += 1



    def Create_Bounce_Light(self):
        global light_counts  # Use the global dictionary for counts

        # Generate a unique light name before creating the light
        light_name = "Lgt_Bounce_" + str(self.light_counts["Bounce"]).zfill(2)

        # Create a VRay Rectangular Light
        Lgt_Bounce = cmds.shadingNode('VRayLightRectShape', asLight=True)

        # Check if light creation was successful
        if not Lgt_Bounce:
            raise RuntimeError("Failed to create VRayLightRectShape.")
        else:
            print(f"{light_name} successfully created.")

        # Rename the light to the generated name
        Lgt_Bounce = cmds.rename(Lgt_Bounce, light_name)

        # Group the light and rename the group
        Bounce_group = cmds.group(Lgt_Bounce, name="Lgt_Bounce_Grp_" + str(self.light_counts["Bounce"]))

        # Set the translation of the light group
        cmds.setAttr(Bounce_group + ".translateY", -100)
        
        # Get the shape node(s) of the light
        light_shape = cmds.listRelatives(Lgt_Bounce, shapes=True)

        # Check if light shape was found    
        if not light_shape:
            raise RuntimeError("Light shape not found.")

        # Move the pivot of the light shape to (0, 0, 0) without affecting its position
        cmds.xform(light_shape[0], pivots=(0, 0, 0), worldSpace=True)

        # Set the light's rotation: rotateX = 90, scaleXYZ = 50
        cmds.setAttr(light_name + ".rotateX", 90)
        cmds.setAttr(light_name + ".scaleZ", 50)
        cmds.setAttr(light_name + ".scaleX", 50)
        cmds.setAttr(light_name + ".scaleY", 50)

        # Increment the count for the Bounce prefix
        self.light_counts["Bounce"] += 1
    

try:
    ui.deleteLater()
except:
    pass
ui = CharacterLightRig()

#def main():
ui.show()