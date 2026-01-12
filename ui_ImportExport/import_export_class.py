from PySide2 import QtCore, QtUiTools, QtWidgets, QtGui
from shiboken2 import wrapInstance
from maya import OpenMayaUI as omu
import maya.cmds as cmds
import mtoa.utils as mutils
import mtoa.aovs as aovs
import json
import os, sys
import re
import pprint as pp
import importlib # module for reload

## Import functions file here
sys.path.append('D:/Felicia/Script_D/ui_ImportExport/')
import import_export_ui_016 as IE
importlib.reload(IE) # Reload

## Import README function file here
sys.path.append('D:/Felicia/Script_D/ui_ImportExport/README/')
import helpWindow as helpp
importlib.reload(helpp) # Reload

SCRIPT_FILE_PATH = 'D:/Felicia/Script_D/ui_ImportExport/'

README_FILE_NAME = 'README_importexport.png' # File name
README_FILE_PATH = f'D:/Felicia/Script_D/ui_ImportExport/README/{README_FILE_NAME}' # Combine path and file name


mainObject = omu.MQtUtil.mainWindow()
mayaMainWind = wrapInstance(int(mainObject), QtWidgets.QWidget)

class ImportExport(QtWidgets.QWidget):    
	
	def __init__(self, parent=mayaMainWind):

		
		super(ImportExport, self).__init__(parent=parent)
				   
		if(__name__ == '__main__'):
			self.ui = SCRIPT_FILE_PATH + '/ui/ImportExport.ui'
		else:
			self.ui = os.path.abspath(os.path.dirname(__file__) + '/ui/ImportExport.ui')

		self.setAcceptDrops(True)
		self.setWindowFlags(QtCore.Qt.Window)
		self.setWindowTitle('Import Export Light Attribute')
		self.setFixedSize(595, 490)  # Locks the window size

		loader = QtUiTools.QUiLoader()
		ui_file = QtCore.QFile(self.ui)
		ui_file.open(QtCore.QFile.ReadOnly)
		self.theMainWidget = loader.load(ui_file)
		ui_file.close()
		
		main_layout = QtWidgets.QVBoxLayout()
		main_layout.addWidget(self.theMainWidget)
		main_layout.setContentsMargins(0, 0, 0, 0)
		self.setLayout(main_layout)


		# Set default settings
		self.default_file_type = '*json' # Default file type *.json
		self.theMainWidget.filetype_comboBox.setCurrentText(self.default_file_type)
		self.theMainWidget.export_radioButton.setChecked(True)  # Export is checked by default
		self.theMainWidget.import_radioButton.setChecked(False)  # Import is unchecked by default
		self.radioButton() # Run method to enable export/ disable import feature by default
		self.theMainWidget.subttitle_label.setText('Export file as') # Default label text for Export
		
		self.theMainWidget.help_toolButton.clicked.connect(self.helpButton)
		

		# Connect ui button to their handlers function
		# Export handles
		self.theMainWidget.export_radioButton.clicked.connect(self.radioButton)
		self.theMainWidget.browse_pushButton.clicked.connect(self.browse_filepath)
		self.theMainWidget.cancel_pushButton.clicked.connect(self.cancel_clicked)
		self.theMainWidget.filename_lineEdit.textChanged.connect(self.filename_lineEdit)
		self.theMainWidget.filetype_comboBox.editTextChanged.connect(self.filetype_comboBox)
		self.theMainWidget.export_pushButton.clicked.connect(self.cue_export)


		# Import handles
		self.theMainWidget.import_radioButton.clicked.connect(self.radioButton)
		self.theMainWidget.reload_pushButton.clicked.connect(self.reload_namespace)
		self.theMainWidget.namespace_listWidget.itemClicked.connect(self.selecting_namespace) # Connects item selected in listWidget
		self.theMainWidget.import_pushButton.clicked.connect(self.cue_import)

		# Initialise global variables
		self.json_file_path = None


	def helpButton(self):
		# print('Help button clicked.')
		helpp.showhelp(README_FILE_PATH)


	def radioButton(self):

		# If Export clicked
		# Enabled: file name, file type, browse, cancel, export button
		if self.theMainWidget.export_radioButton.isChecked():
			# Enable export features
			self.theMainWidget.subttitle_label.setText('Export file as')
			self.theMainWidget.export_pushButton.setEnabled(True)

			# Disable import features
			self.theMainWidget.selectnamespace_label.setEnabled(False)
			self.theMainWidget.reload_pushButton.setEnabled(False)
			self.theMainWidget.namespace_listWidget.setEnabled(False)
			self.theMainWidget.import_pushButton.setEnabled(False)

		
		# If Import clicked
		# Endable: namespace, listwidget, import button
		else:
			# Disable export features
			self.theMainWidget.subttitle_label.setText('Read json file')
			self.theMainWidget.export_pushButton.setEnabled(False)
			
			# Enable import features
			self.theMainWidget.selectnamespace_label.setEnabled(True)
			self.theMainWidget.reload_pushButton.setEnabled(True)
			self.theMainWidget.namespace_listWidget.setEnabled(True)
			self.theMainWidget.import_pushButton.setEnabled(True)


	def browse_filepath(self):
		
		# Export is checked
		if self.theMainWidget.export_radioButton.isChecked():
			file_mode = 0 # Save file mode
			caption = "Save file as"

		# Import is checked
		else:  
			file_mode = 1 # Open file mode
			caption = "Select file to open"


		# Open file dialog to select file path
		self.json_file_path = (cmds.fileDialog2(fileMode=file_mode, caption=caption, fileFilter="*.json", dialogStyle=2) or [None])[0]

		# Set the selected file path in the QLineEdit
		if self.json_file_path:
			self.theMainWidget.filename_lineEdit.setText(self.json_file_path)

	
	# Handle changes in the filename.
	def filename_lineEdit(self, text):

		if text.strip():  # Ensure text is not empty or just whitespace
			self.default_file_type = "*.json"  # Keep the default file type fixed as *.json

	
	# Handle changes in the comboBox/ dropdown box/
	def filetype_comboBox(self):
		self.default_file_type = self.theMainWidget.filetype_comboBox.currentText()
		
	
	# Cancels all action when clicked.
	def cancel_clicked(self):
		self.close()


	def get_namespace(self):

		namespace_found = cmds.ls(long=True, type='reference')

		cleaned_namespace_list = []
		
		for name in namespace_found:
			cleaned_namespace = name.split('RN')[0]
			cleaned_namespace_list.append(cleaned_namespace)
		
		# print(self.namespace_list)
		return cleaned_namespace_list
		

	def reload_namespace(self):
		
		# Retrieves all current namespaces from the outliner.
		new_namespace_list = self.get_namespace()
		
		# Clear the current namespace list and update with new data
		self.namespace_list = []

		# Check for new namespaces not already in self.namespace_list.
		for namespace in new_namespace_list:
			if namespace not in self.namespace_list:
				self.namespace_list.append(namespace)

				# if self.namespace_list == []:
				#     print('No namespace found in scene.')

		# Populate the listWidget with updated namespace list
		self.insert_namespace(self.namespace_list)


	def insert_namespace(self, namespace_list):

		# Refresh the listWidget
		self.theMainWidget.namespace_listWidget.clear()
		self.theMainWidget.namespace_listWidget.addItems(namespace_list)


	def selecting_namespace(self, item):

		self.selected_namespace = item.text()


	def cue_export(self):

		print('Running Export.')
		file_path = self.theMainWidget.filename_lineEdit.text()
		
		# Run export
		IE.main_export(file_path)

		# Information dialog
		result = cmds.confirmDialog(
			title="Information",
			message="Export completed.",
			button=["OK"],
			defaultButton="OK",
			icon="information"
			)

		
	def cue_import(self):

		namespace = ''

		print('Running Import.')
		file_path = self.theMainWidget.filename_lineEdit.text()
		
		if not file_path:
			print("Error: File path is not set. Please select a file path first.")
			return

		# Assign var to input from user
		
		try:
			namespace = self.theMainWidget.namespace_listWidget.currentItem().text()
			print('Namespace selected.')

		except AttributeError:
			namespace = ''
			print('No namespace selected.')
			
		# Run import
		IE.main_import(namespace, file_path)

		# Information dialog
		result = cmds.confirmDialog(
			title="Information",
			message="Import completed.",
			button=["OK"],
			defaultButton="OK",
			icon="information"
			)



try:
	ui.deleteLater()
except:
	pass
ui = ImportExport()
ui.show()

# def main():
	# ui.show()