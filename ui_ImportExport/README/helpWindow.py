# from PySide2 import QtCore, QtUiTools, QtWidgets, QtGui
# from maya import OpenMayaUI as omu
# from shiboken2 import wrapInstance
# import maya.cmds as cmds
# import mtoa.utils as mutils
# import mtoa.aovs as aovs
# import json
import os, sys
import re
import pprint as pp
import importlib # module for reload
import subprocess, platform


def showhelp(README_FILE_PATH):
    
    if not os.path.isfile(README_FILE_PATH):
        print(f'Error: The file "{README_FILE_PATH}" does not exist.')
        return

    try:
        if platform.system() == 'Windows':
            os.startfile(README_FILE_PATH)  # Windows-specific

        elif platform.system() == 'Darwin':  # macOS
            subprocess.run(['open', README_FILE_PATH], check=True)

        else:  # Linux and others
            subprocess.run(['xdg-open', README_FILE_PATH], check=True)

    except Exception as e:
        print(f'An error occurred while trying to open the PDF: {e}')



########################################################################################

# CALL YOUR FUNCTION HERE
# send_help = showhelp(README_FILE_PATH)