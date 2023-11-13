"""
FILE:           qa_std/qa_theme.py
AUTHOR:         Geetansh Gautam
PROJECT:        Quizzing Application, version 4

DOC

    Quizzing Application Theme Management

DEFINES

    (class)     dataclass       Theme

DEPENDENCIES

    qa_app_pol                              [alias: AppPolicy]
    qa_file_io.qa_theme_file.Theme

"""

from . import qa_app_pol as AppPolicy
from qa_file_io.qa_theme_file import Theme, ThemeFile_s


ScriptPolicy = AppPolicy.PolicyManager.Module('ThemeManager', 'qa_theme.py')


if __name__ == "__main__":
    ScriptPolicy.run_as_main()
