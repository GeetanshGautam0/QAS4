"""
FILE:           qa_std/qa_theme.py
AUTHOR:         Geetansh Gautam
PROJECT:        Quizzing Application, version 4

DOC

    Quizzing Application Theme Management

DEFINES

    (class)     dataclass       ConsoleTheme

DEPENDENCIES

    dataclasses.dataclass   [alias: dataclass]
    qa_def
    qa_app_pol              [alias: AppPolicy]

"""

from dataclasses import dataclass
from . import qa_def
from . import qa_app_pol as AppPolicy


@dataclass
class ConsoleTheme:
    BG: str = qa_def.ANSI.BG_BLACK
    FG: str = qa_def.ANSI.FG_WHITE
    ER: str = qa_def.ANSI.FG_BRIGHT_RED
    OK: str = qa_def.ANSI.FG_BRIGHT_GREEN
    WA: str = qa_def.ANSI.FG_BRIGHT_YELLOW
    HG: str = qa_def.ANSI.FG_BRIGHT_BLUE


ScriptPolicy = AppPolicy.PolicyManager.Module('ThemeManager', 'qa_theme.py')


if __name__ == "__main__":
    ScriptPolicy.run_as_main()