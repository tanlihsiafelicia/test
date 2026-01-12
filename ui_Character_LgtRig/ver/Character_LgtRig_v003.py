from PySide2 import QtCore, QtUiTools, QtWidgets, QtGui
from maya import OpenMayaUI as omu
from shiboken2 import wrapInstance
import maya.cmds as cmds
import mtoa.utils as mutils
import maya.mel as mel
import os, sys
import re  # To use regular expressions for extracting numbers

SCRIPT_FILE_PATH = 'D:/Felicia/Script_D/ui_Character_LgtRig/'
mainObject = omu.MQtUtil.mainWindow()
mayaMainWind = wrapInstance(int(mainObject), QtWidgets.QWidget)

class CharacterLightRig(QtWidgets.QWidget):    
    
    def __init__(self, parent=mayaMainWind):
        
        super(CharacterLightRig, self).__init__(parent=parent)
                   
        if(__name__ == '__main__'):
            self.ui = SCRIPT_FILE_PATH + '/ui/Character_LgtRig_v002.ui'
        else:
            self.ui = os.path.abspath(os.path.dirname(__file__) + '/ui/Character_LgtRig_v002.ui')

        self.setAcceptDrops(True)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setWindowTitle('character light rig')
        self.setFixedSize(280, 230)  # Locks the window size


        loader = QtUiTools.QUiLoader()
        ui_file = QtCore.QFile(self.ui)
        ui_file.open(QtCore.QFile.ReadOnly)
        self.theMainWidget = loader.load(ui_file)
        ui_file.close()

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(self.theMainWidget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)
        
        # Connect the checkbox and button to their handlers
        self.theMainWidget.Key_Light_checkBox.stateChanged.connect(self.handle_individual_light)
        self.theMainWidget.Fill_Light_checkBox.stateChanged.connect(self.handle_individual_light)
        self.theMainWidget.Rim_L_Light_checkBox.stateChanged.connect(self.handle_individual_light)
        self.theMainWidget.Rim_R_Light_checkBox.stateChanged.connect(self.handle_individual_light)
        self.theMainWidget.Dome_Light_checkBox.stateChanged.connect(self.handle_individual_light)

        self.theMainWidget.Select_All_checkBox.stateChanged.connect(self.handle_select_all)
        self.theMainWidget.Create_Light_pushButton.clicked.connect(self.create_light)

        
        # # Initial value for the selection
        # self.key_light_selected = False
        # self.fill_light_selected = False
        # self.rim_l_light_selected = False
        # self.rim_r_light_selected = False
        # self.dome_light_selected = False
        # self.select_all_selected = False

        self.light_counts = {
            "Lgt_Key": 0,
            "Lgt_Fill": 0,
            "Lgt_Rim_L": 0,
            "Lgt_Rim_R": 0,
            "Lgt_Bounce": 0,
            "Lgt_Dome" : 0
        }
    
    # Global function to check the highest existing light number for multiple light types
    def check_existing_light_number(self, light_type):

        # List all lights and groups in the scene
        all_lights = cmds.ls(type='light')  
        all_groups = cmds.ls(type='transform')
        max_number = 0

        # Find the highest number for lights and groups of the given type
        for light in all_lights:
            if light_type in light:
                try:
                    number = int(light.split("_")[-1])  # Extract the number from the name
                    max_number = max(max_number, number)
                except ValueError:
                    continue
        
        for group in all_groups:
            if f"{light_type}_Grp" in group:
                try:
                    number = int(group.split("_")[-1])  # Extract the number from the group
                    max_number = max(max_number, number)
                except ValueError:
                    continue

        return max_number

    # Function to handle individual checkbox state changes
    def handle_individual_light(self):
        # Check if any individual checkbox is unchecked
        if not all([
            self.theMainWidget.Key_Light_checkBox.isChecked(),
            self.theMainWidget.Fill_Light_checkBox.isChecked(),
            self.theMainWidget.Rim_L_Light_checkBox.isChecked(),
            self.theMainWidget.Rim_R_Light_checkBox.isChecked(),
            self.theMainWidget.Dome_Light_checkBox.isChecked()
        ]):
            # Uncheck "Select All" if any checkbox is unchecked
            # Temporarily block signals to prevent recursive calls
            self.theMainWidget.Select_All_checkBox.blockSignals(True)
            self.theMainWidget.Select_All_checkBox.setCheckState(QtCore.Qt.Unchecked)
            self.theMainWidget.Select_All_checkBox.blockSignals(False)

            
        else:
            # Check "Select All" if all checkboxes are checked
            self.theMainWidget.Select_All_checkBox.blockSignals(True)
            self.theMainWidget.Select_All_checkBox.setCheckState(QtCore.Qt.Checked)
            self.theMainWidget.Select_All_checkBox.blockSignals(False)

            
    def handle_select_all(self, state):
        if state == QtCore.Qt.Checked:
            print('All lights checkbox selected!')

            # Check all individual checkboxes when "Select All" is checked
            # Temporarily block signals to prevent triggering individual handlers
            self.theMainWidget.Key_Light_checkBox.blockSignals(True)
            self.theMainWidget.Fill_Light_checkBox.blockSignals(True)
            self.theMainWidget.Rim_L_Light_checkBox.blockSignals(True)
            self.theMainWidget.Rim_R_Light_checkBox.blockSignals(True)
            self.theMainWidget.Dome_Light_checkBox.blockSignals(True)

            # Check all checkboxes
            self.theMainWidget.Key_Light_checkBox.setCheckState(QtCore.Qt.Checked)
            self.theMainWidget.Fill_Light_checkBox.setCheckState(QtCore.Qt.Checked)
            self.theMainWidget.Rim_L_Light_checkBox.setCheckState(QtCore.Qt.Checked)
            self.theMainWidget.Rim_R_Light_checkBox.setCheckState(QtCore.Qt.Checked)
            self.theMainWidget.Dome_Light_checkBox.setCheckState(QtCore.Qt.Checked)

            # Re-enable signals after setting states
            self.theMainWidget.Key_Light_checkBox.blockSignals(False)
            self.theMainWidget.Fill_Light_checkBox.blockSignals(False)
            self.theMainWidget.Rim_L_Light_checkBox.blockSignals(False)
            self.theMainWidget.Rim_R_Light_checkBox.blockSignals(False)
            self.theMainWidget.Dome_Light_checkBox.blockSignals(False)

        else:
            print('All lights checkbox deselected!')

            # Uncheck all individual checkboxes when "Select All" is unchecked
            self.theMainWidget.Key_Light_checkBox.blockSignals(True)
            self.theMainWidget.Fill_Light_checkBox.blockSignals(True)
            self.theMainWidget.Rim_L_Light_checkBox.blockSignals(True)
            self.theMainWidget.Rim_R_Light_checkBox.blockSignals(True)
            self.theMainWidget.Dome_Light_checkBox.blockSignals(True)

            self.theMainWidget.Key_Light_checkBox.setCheckState(QtCore.Qt.Unchecked)
            self.theMainWidget.Fill_Light_checkBox.setCheckState(QtCore.Qt.Unchecked)
            self.theMainWidget.Rim_L_Light_checkBox.setCheckState(QtCore.Qt.Unchecked)
            self.theMainWidget.Rim_R_Light_checkBox.setCheckState(QtCore.Qt.Unchecked)
            self.theMainWidget.Dome_Light_checkBox.setCheckState(QtCore.Qt.Unchecked)

            # Re-enable signals after setting states
            self.theMainWidget.Key_Light_checkBox.blockSignals(False)
            self.theMainWidget.Fill_Light_checkBox.blockSignals(False)
            self.theMainWidget.Rim_L_Light_checkBox.blockSignals(False)
            self.theMainWidget.Rim_R_Light_checkBox.blockSignals(False)
            self.theMainWidget.Dome_Light_checkBox.blockSignals(False)

    def create_key_light(self, light_type):

        # Check the existing lights of the given type and find the highest number
        max_light_number = self.check_existing_light_number(light_type)
        new_light_number = max_light_number + 1

        # Format the new light group and light with zfill(2)
        light_group = f"{light_type}_Grp_{str(new_light_number).zfill(2)}"
        light_name = f"{light_type}_{str(new_light_number).zfill(2)}"

        # Create Maya Directional Light for Key Light
        light = cmds.directionalLight(name=light_name)
        if not light:
            raise RuntimeError(f"Failed to create {light_type} light.")
        # else:
        #     print("Creating Directional light.")

        # Group the light
        light_group = cmds.group(light, name=light_group)
        if not light_group:
            raise RuntimeError(f"Failed to group {light_type} light.")
            
        # Set specific rotation based on the light type
        # Attributes for Lgt_Key
        cmds.setAttr(f"{light_name}.translateZ", 50)

        # Common pivot settings for all light types
        cmds.xform(light_group, pivots=(0, 0, 0), worldSpace=True)
        cmds.xform(light_name, pivots=(0, 0, 0), worldSpace=True)

        # Common scale settings for all light types
        cmds.setAttr(f"{light_name}.scaleX", 50)
        cmds.setAttr(f"{light_name}.scaleY", 50)
        cmds.setAttr(f"{light_name}.scaleZ", 50)

        # Set specific rotation based on the light type
        # Attributes for Lgt_Key
        cmds.setAttr(f"{light_name}.rotateX", -40)
        cmds.setAttr(f"{light_name}.rotateY", -45)

        # Set specific exposure based on the light type
        # Attributes for Lgt_Key
        cmds.setAttr(f"{light_name}.aiExposure", 1)

        # Success message
        print(f"{light_name} successfully created and grouped as {light_group}.")
        # Update the global light count for the light type

        self.light_counts[light_type] += 1

    def create_arnold_light_by_type(self, light_type):

            # Check the existing lights of the given type and find the highest number
            max_light_number = self.check_existing_light_number(light_type)
            new_light_number = max_light_number + 1

            # Create Arnold Area Light for all other lights
            light = mutils.createLocator("aiAreaLight", asLight=True)
                
            # Check if light creation was successful
            if not light:
                raise RuntimeError("Failed to create ", light, " light.")
            # else:
            #     print(f"{light} light successfully created.")

            # Extract the transform node from the tuple (first element)
            light_transform = light[1]

            # Format the new light group and light with zfill(2)
            light_group = f"{light_type}_Grp_{str(new_light_number).zfill(2)}"
            light_name = f"{light_type}_{str(new_light_number).zfill(2)}"

            # Group the light and rename the group
            light_group = cmds.group(light, name = light_group)
            if not light_group:
                raise RuntimeError(f"Failed to group {light_type} light.")

            # Rename the light 
            light_name = cmds.rename(light_transform, light_name)
                
            # # Set specific translateZ value based on light type
            # if light_type == "Lgt_Bounce":
            #     cmds.setAttr(f"{light_name}.translateZ", 0)
            # else:
            # Common scale settings for all light types
            cmds.setAttr(f"{light_name}.translateZ", 10)  # Default value for other lights

            # Common pivot settings for all light types
            cmds.xform(light_group, pivots=(0, 0, 0), worldSpace=True)
            cmds.xform(light_name, pivots=(0, 0, 0), worldSpace=True)

            # Common scale settings for all light types
            cmds.setAttr(f"{light_name}.scaleX", 50)
            cmds.setAttr(f"{light_name}.scaleY", 50)
            cmds.setAttr(f"{light_name}.scaleZ", 50)

            if light_type == "Lgt_Fill":
                # Attributes for Lgt_Fill
                cmds.setAttr(f"{light_name}.rotateX", -40)
                cmds.setAttr(f"{light_name}.rotateY", 45)

            elif light_type == "Lgt_Rim_L":
                # Attributes for Lgt_Rim_L
                cmds.setAttr(f"{light_name}.rotateX", -40)
                cmds.setAttr(f"{light_name}.rotateY", 225)

            elif light_type == "Lgt_Rim_R":
                # Attributes for Lgt_Rim_R
                cmds.setAttr(f"{light_name}.rotateX", -40)
                cmds.setAttr(f"{light_name}.rotateY", 135)

            # elif light_type == "Lgt_Bounce":
            #     # Attributes for Lgt_Bounce
            #     cmds.setAttr(f"{light_name}.translateY", -50)
            #     cmds.setAttr(f"{light_name}.rotateX", 90)
                
            # Success message
            print(f"{light_name} successfully created and grouped as {light_group}.")
            # Update the global light count for the light type

            self.light_counts[light_type] += 1
            
    def create_aiSkyDome_light(self, light_type):

        # Check the existing lights of the given type and find the highest number
        max_light_number = self.check_existing_light_number(light_type)
        new_light_number = max_light_number + 1

        # Create the aiSkyDomeLight transform node
        light = mutils.createLocator("aiSkyDomeLight", asLight=True)
            
        # Check if light creation was successful
        if not light:
            raise RuntimeError("Failed to create ", light, " light.")
        # else:
        #     print(f"{light} light successfully created.")

        # Extract the transform node and shape node
        light_transform_node = light[1]  # Extract the transform node (second value in the tuple)
        self.light_shape = cmds.listRelatives(light_transform_node, shapes=True)[0]  # Get the shape node

        # Format the new light group and light with zfill(2)
        light_group = f"{light_type}_Grp_{str(new_light_number).zfill(2)}"
        light_transform = f"{light_type}_{str(new_light_number).zfill(2)}"
        self.light_shape = f"{light_type}_Shape{str(new_light_number)}"

        # Group the light and rename the group
        light_group = cmds.group(light, name = light_group)
        if not light_group:
            raise RuntimeError(f"Failed to group {light_type} light.")

        # Rename the transform node
        light_name = cmds.rename(light_transform_node, light_transform)

        print("Creating_Dome_light.")

    def create_light(self):
        # Flag to track if "Select All" was selected
        select_all = self.theMainWidget.Select_All_checkBox.isChecked()
    
        if select_all:
            print("Creating all lights.")
            self.create_key_light("Lgt_Key") # Create Key Light

            for light_type in ["Lgt_Fill", "Lgt_Rim_L", "Lgt_Rim_R"]:
                self.create_arnold_light_by_type(light_type) # Create all other Lights

            # self.create_aiSkyDome_light("Lgt_Dome") # Create dome Lights

        # For other lights, use `create_arnold_light_by_type`
        else:
            # Check and create lights individually
            if self.theMainWidget.Key_Light_checkBox.isChecked():
                self.create_key_light("Lgt_Key")  # Create Key Light
                print("Creating_key_light.") 

            if self.theMainWidget.Fill_Light_checkBox.isChecked():
                print("Creating_Fill_light.")
                self.create_arnold_light_by_type("Lgt_Fill")  # Create Fill Light

            if self.theMainWidget.Rim_L_Light_checkBox.isChecked():
                print("Creating_Rim_L_light.")
                self.create_arnold_light_by_type("Lgt_Rim_L")  # Create Lgt_Rim_L Light

            if self.theMainWidget.Rim_R_Light_checkBox.isChecked():
                print("Creating_Rim_R_light.")
                self.create_arnold_light_by_type("Lgt_Rim_R")  # Create Lgt_Rim_R Light

            # if self.theMainWidget.Dome_Light_checkBox.isChecked():
            #     print("Creating_Dome_light.")
            #     self.create_aiSkyDome_light("Lgt_Dome")  # Create Dome Light
            
            # if self.theMainWidget.Bounce_Light_checkBox.isChecked():
            #     print("Creating_Bounce_light.")
            #     self.create_arnold_light_by_type("Lgt_Bounce")  # Create Bounce Light
        
        if self.theMainWidget.Dome_Light_checkBox.isChecked():
            # Prompt the user to decide whether to select an HDR file


            user_choice = cmds.confirmDialog(
                title="HDR Selection",
                message="Do you want to select a HDR file for the dome light?",
                button=["Yes", "No"],
                defaultButton="Yes",
                cancelButton="No",
                dismissString="Cancel"
            )

            if user_choice == "Yes":

                # Create the Dome Light
                self.create_aiSkyDome_light("Lgt_Dome")
                
                # User wants to select an HDR file
                hdr_file_path = (cmds.fileDialog2(fileFilter="Maya Files (*.png *.exr *.hdr)", dialogStyle=2, fileMode=1) or [None])[0]
                
                if hdr_file_path:
                    print(f"Selected HDR file: {hdr_file_path[0]}")
                    
                    file_node = cmds.shadingNode('file', asTexture=True)
                    # Set the HDR file path on the file node
                    cmds.setAttr(f"{file_node}.fileTextureName", hdr_file_path, type="string")

                    # Connect the file node's outColor to the aiSkyDomeLight's color attribute
                    cmds.connectAttr(f"{file_node}.outColor", f"{self.light_shape}.color", force=True)
                    print ("HDR file connected to Dome Light.")



                else:
                    print("No HDR file selected.")
                    # self.warning_window()  # Show warning if needed

            if user_choice == "No":
                self.create_aiSkyDome_light("Lgt_Dome")  # Create Dome Light
                print("Skipping HDR file selection.")

try:
    ui.deleteLater()
except:
    pass
ui = CharacterLightRig()
ui.show()

# def main():
    # ui.show()
