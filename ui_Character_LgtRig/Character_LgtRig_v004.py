# author_name
# put some signature and brief descrption of the script
# how to call the script

# go throught code, add # comment on func wherever is needed for easy future understanding!!!!!


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
        self.theMainWidget.Create_Light_pushButton.clicked.connect(self.create_light_by_type)

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
            # Uncheck all individual checkboxes when "Select All" is unchecked
            self.theMainWidget.Key_Light_checkBox.blockSignals(True)
            self.theMainWidget.Fill_Light_checkBox.blockSignals(True)
            self.theMainWidget.Rim_L_Light_checkBox.blockSignals(True)
            self.theMainWidget.Rim_R_Light_checkBox.blockSignals(True)
            self.theMainWidget.Dome_Light_checkBox.blockSignals(True)

            # uncheck all checkboxes
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

    #  & HDR for Dome light
    def create_light(self, light_type):
        # Check the existing lights of the given type and find the highest number
        max_light_number = self.check_existing_light_number(light_type)
        new_light_number = max_light_number + 1

        # Format the new light group and light with zfill(2)
        self.light_group = f"{light_type}_Grp_{str(new_light_number).zfill(2)}"
        self.light_name = f"{light_type}_{str(new_light_number).zfill(2)}"

        # print(light_type)
        if light_type == "Lgt_Key":
            light = cmds.directionalLight(name=self.light_name)
            
        elif light_type == "Lgt_Dome":

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
                light = mutils.createLocator("aiSkyDomeLight", asLight=True)
                light = cmds.rename(light[1],self.light_name)
                
                # User wants to select an HDR file
                hdr_file_path = (cmds.fileDialog2(fileFilter="Maya Files (*.png *.exr *.hdr)", dialogStyle=2, fileMode=1) or [None])[0]
                
                if hdr_file_path:
                    print(f"Selected HDR file: {hdr_file_path[0]}")
                    
                    # Create file node
                    file_node = cmds.shadingNode('file', asTexture=True)
                    
                    # Set the HDR file path on the file node
                    cmds.setAttr(f"{file_node}.fileTextureName", hdr_file_path, type="string")
                    self.dome_shape = cmds.listRelatives(light,shapes=True)[0]

                    # Connect the file node's outColor to the aiSkyDomeLight's color attribute
                    cmds.connectAttr(f"{file_node}.outColor", f"{self.dome_shape}.color", force=True)
                    print ("HDR file connected to Dome Light.")

                else:
                    print("No HDR file selected.")

            if user_choice == "No":
                light = mutils.createLocator("aiSkyDomeLight", asLight=True)
                light = cmds.rename(light[1],self.light_name)

        else:
            light = mutils.createLocator("aiAreaLight", asLight=True)
            light = cmds.rename(light[1],self.light_name)

        self.light_object = light

        # Group the light
        self.light_group = cmds.group(light, name=self.light_group)
        if not self.light_group:
            raise RuntimeError(f"Failed to group {light_type} light.") # print message if failed

        # Set Rotate & Scale attr for all light types
        if light_type == "Lgt_Key":
            self.light_attr_by_type(self.light_name, (0, 0, 15), (-40, -45, 0), (50, 50, 50))

        elif light_type == "Lgt_Fill":
            self.light_attr_by_type(self.light_name, (0, 0, 5), (-40, 45, 0), (50, 50, 50))
        
        elif light_type == "Lgt_Rim_L":
            self.light_attr_by_type(self.light_name, (0, 0, 5), (-40, 225, 0), (50, 50, 50))
            
        elif light_type == "Lgt_Rim_R":
            self.light_attr_by_type(self.light_name, (0, 0, 5), (-40, 135, 0), (50, 50, 50))

        # Success message
        print(f"{self.light_name} successfully created and grouped as {self.light_group}.")
        # Update the global light count for the light type

        self.light_counts[light_type] += 1

    # Setting translate, rotate & scale attributes base on light type
    def light_attr_by_type(self, light_type, trans=(0,0,0), rot=(0,0,0), scl=(1,1,1)):
        cmds.setAttr(f"{light_type}.translate", trans[0], trans[1], trans[2])
        cmds.xform(light_type, pivots=(0, 0, 0), worldSpace=True)
        cmds.setAttr(f"{light_type}.rotate", rot[0], rot[1], rot[2])
        cmds.setAttr(f"{light_type}.scale", scl[0], scl[1], scl[2])
        
    # Creating light based on which checkBox is selected
    def create_light_by_type(self):
        # Flag to track if "Select All" was selected
        select_all = self.theMainWidget.Select_All_checkBox.isChecked()
    
        if select_all:
            print("Creating all lights.")
            for light_type in ["Lgt_Key","Lgt_Fill", "Lgt_Rim_L", "Lgt_Rim_R","Lgt_Dome"]:
                self.create_light(light_type) # Create all other Lights

        # For other lights, use `create_arnold_light_by_type`
        else:
            # Check and create lights individually
            if self.theMainWidget.Key_Light_checkBox.isChecked():
                self.create_light("Lgt_Key")  # Create Key Light

            if self.theMainWidget.Fill_Light_checkBox.isChecked():
                self.create_light("Lgt_Fill") # Create Fill Light

            if self.theMainWidget.Rim_L_Light_checkBox.isChecked():
                self.create_light("Lgt_Rim_L")  # Create Lgt_Rim_L Light

            if self.theMainWidget.Rim_R_Light_checkBox.isChecked():
                self.create_light("Lgt_Rim_R")  # Create Lgt_Rim_R Light

            if self.theMainWidget.Dome_Light_checkBox.isChecked():
                self.create_light("Lgt_Dome")

try:
    ui.deleteLater()
except:
    pass
ui = CharacterLightRig()
ui.show()

# def main():
    # ui.show()
