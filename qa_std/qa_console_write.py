"""
FILE:           qa_std/qa_console_write.py
AUTHOR:         Geetansh Gautam
PROJECT:        Quizzing Application, version 4

DOC

    Defines standard console write functions.
    

DEFINES

    Type            Name                Input Types                 Output Types            Alias
    ---------------------------------------------------------------------------------------------
    (dataclass)     ConsoleTheme
    (method)        SetupWinConsole     None                        None
    (method)        CheckOS             None                        qa_def.OS               std.CheckOS
    (class)         Write               None                        None                    W
    (method)        W.error             *Any, str, str              bool
    (method)        W.ok                *Any, str, str, str         bool
    (method)        W.warn              *Any, str, str              bool
    (method)        W.emphasis          *Any, str, str              bool
    (method)        W.write             *Any, str, str              bool
    (method)        stderr              *str, str, str              None
    (method)        stdout              *str, str, str              None

DEPENDENCIES

    .qa_app_pol                 [alias: AppPolicy]
    .qa_def
    .qa_dtc
    sys
    ctypes.windll               [alias: windll]
    dataclasses.dataclass

"""

import sys

from typing import Any
from . import qa_app_pol as AppPolicy, qa_def, qa_dtc
from ctypes import windll
from dataclasses import dataclass


@dataclass
class ConsoleTheme:
    BG: str = qa_def.ANSI.BG_BLACK
    FG: str = qa_def.ANSI.FG_WHITE
    ER: str = qa_def.ANSI.FG_BRIGHT_RED
    OK: str = qa_def.ANSI.FG_BRIGHT_GREEN
    WA: str = qa_def.ANSI.FG_BRIGHT_YELLOW
    HG: str = qa_def.ANSI.FG_BRIGHT_BLUE


theme = ConsoleTheme


ScriptPolicy = AppPolicy.PolicyManager.Module('ConsoleWriter', 'qa_console_write.py')


def stderr(*data: Any, delim: str = ' ', line_termination: str = '\n') -> None:
    sys.stderr.write(delim.join(data) + line_termination)


def stdout(*data: Any, delim: str = ' ', line_termination: str = '\n') -> None:
    sys.stdout.write(delim.join(data) + line_termination)


class Write:
    @staticmethod
    def error(*data: Any, delim: str = ' ', line_termination: str = '\n') -> bool:
        try:
            stderr(
                theme.ER,
                '[ERROR]    ', *[qa_dtc.convert(str, d) for d in data],
                qa_def.ANSI.RESET,
                delim=delim,
                line_termination=line_termination
            )

        except Exception as E:
            return False
        else:
            return True

    @staticmethod
    def ok(*data: Any, delim: str = ' ', line_termination: str = '\n', label: str = 'SUCCESS') -> bool:
        try:
            stdout(
                theme.OK,
                f'[{label}]  ', *[qa_dtc.convert(str, d) for d in data],
                qa_def.ANSI.RESET,
                delim=delim,
                line_termination=line_termination
            )

        except Exception as E:
            return False
        else:
            return True

    @staticmethod
    def warn(*data: Any, delim: str = ' ', line_termination: str = '\n') -> bool:
        try:
            stdout(
                theme.WA,
                '[WARNING]  ', *[qa_dtc.convert(str, d) for d in data],
                qa_def.ANSI.RESET,
                delim=delim,
                line_termination=line_termination
            )

        except Exception as E:
            return False
        else:
            return True

    @staticmethod
    def emphasis(*data: Any, delim: str = ' ', line_termination: str = '\n', label: str = 'IMPORTANT') -> bool:
        try:
            stdout(
                theme.HG,
                f'[{label}]', *[qa_dtc.convert(str, d) for d in data],
                qa_def.ANSI.RESET,
                delim=delim,
                line_termination=line_termination
            )

        except Exception as E:
            return False
        else:
            return True

    @staticmethod
    def write(*data: Any, delim: str = ' ', line_termination: str = '\n', label="GENERAL") -> bool:
        try:
            stdout(
                theme.FG,
                f'[{label}]  ', *[qa_dtc.convert(str, d) for d in data],
                qa_def.ANSI.RESET,
                delim=delim,
                line_termination=line_termination
            )

        except Exception as E:
            return False
        else:
            return True


def CheckOS() -> qa_def.OS:
    os = sys.platform
    match os:
        case 'win32':
            return qa_def.OS.WIN
        case 'darwin':
            return qa_def.OS.OSX
        case 'linux':
            return qa_def.OS.LIN
        case _:
            return qa_def.OS.OTH


def SetupWinConsole() -> None:
    kernel32 = windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)


if __name__ == "__main__":
    ScriptPolicy.run_as_main()

else:
    # Check the operating system. If it is WIN, then we need to setup the console to accept ANSI colors.
    _os = CheckOS()
    if _os == qa_def.OS.WIN:
        SetupWinConsole()

