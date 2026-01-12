# from comm.ui_mod.pyside_mod import *
from maya import OpenMayaUI as omu

import maya.cmds as cmds
import mtoa.utils as mutils
import mtoa.aovs as aovs
import os, sys, re, importlib, json
import pprint as pp


from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PySide6.QtUiTools import QUiLoader

class MainUI(QWidget):
    def __init__(self):
        super().__init__()
        loader = QUiLoader()
        self.main_widget = loader.load('main_ui.ui', self)  # Load Main UI
        self.sub_widget = loader.load('sub_ui.ui', self)    # Load Sub UI

        layout = QVBoxLayout(self)
        layout.addWidget(self.main_widget)
        layout.addWidget(self.sub_widget)

app = QApplication([])
window = MainUI()
window.show()
app.exec()
