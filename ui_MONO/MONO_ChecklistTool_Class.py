from comm.ui_mod.pyside_mod import *
from maya import OpenMayaUI as omu

import maya.cmds as cmds
import mtoa.utils as mutils
import mtoa.aovs as aovs
import os, sys, re, importlib, json
import pprint as pp


# SOP FOR ALL CLASS MAIN PY (UPDATED 18022025)
# # ----------------------------------------------------------------------------- #
try:
    ui.deleteLater()
except:
    pass
ui = MONO_Checklist_Tool() 


def main():
    ui.show()


# ----------------------------------------------------------------------------- #
# SOP FOR ALL SHELF COMMAND
# import MONO_Checklist_Tool 
# reload(MONO_Checklist_Tool)
# MONO_Checklist_Tool.main()