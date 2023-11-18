"""
FILE:           qa_ui/qa_admin_tools.py
AUTHOR:         Geetansh Gautam
PROJECT:        Quizzing Application, version 4

DOC

    Quizzing application administrator tools UI.

DEFINES


DEPENDENCIES

    qa_std.*
    qa_file_io.*
    tkinter

"""

import tkinter

import qa_std as STD
import qa_file_io as FileIO


ModuleScript = STD.AppPolicy.PolicyManager.Module('AdminTools', 'qa_admin_tools.py') 


if __name__ == "__main__":
    ModuleScript.run_as_main()
