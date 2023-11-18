"""
FILE:           qa_std/qa_def.py
AUTHOR:         Geetansh Gautam
PROJECT:        Quizzing Application, version 4

DOC

    Quizzing Application Definitions

    * Defines custom classes, structs, and enums that are to be used throughout the application.
    * Script-specific classes, structs, and enums many be defined within their respective scripts.

DEFINES

    (enum)                  OS
    (enum)                  ExcepionCodes
    (class)                 HexColor
    (class)                 File
    (class)     -           ANSI
    (Exception)             NotYetImplemented

DEPENDENCIES

    typing.**               Union, Tuple
    enum.Enum               [alias: Enum]
    re

"""

from typing import Tuple, Union
import re
from enum import Enum


class OS(Enum):
    WIN = 0
    OSX = 1
    LIN = 2
    OTH = 3


class ExceptionCodes(Enum):
    (
        BASE_EXCEPTION,
        ARGUMENT_TYPE_ERROR,
        CONFIG_ERROR,
        FILE_NOT_FOUND_ERROR,
        FILE_RELATED_ERROR,
        ATTRIBUTE_ERROR,
        VALUE_ERROR,
        INTERNAL_ERROR,
        ARITHMETIC_ERROR, ZERO_DIVISION_ERROR
    ) = range(10)


class HexColor:
    def __init__(self, color: str):
        self.color = color.upper()
        assert self.check(), 'Color provided does not match expected pattern (1)'

    def check(self) -> Union[str, None]:
        res = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', self.color)
        return str(res) if res is not None else None


class File:
    def __init__(self, file_path: str):
        assert isinstance(file_path, str)

        self.file_path = file_path.strip().replace('/', '\\')
        self.path, self.file_name = File.split_file_path(self.file_path)

    @staticmethod
    def split_file_path(file_path: str) -> Tuple[str, str]:
        assert isinstance(file_path, str)

        tokens = file_path.replace("\\", '/').split('/')
        return "\\".join(i for i in tokens[:-1:]), tokens[-1]


class NotYetImplemented(Exception):
    def __init__(self, feature: str) -> None:
        self.f = feature
        
    def __str__(self) -> str:
        return f'Feature {self.f} has not yet been implemented.'


class ANSI:
    """
    (class)     -           ANSI

    Defines colors in terms of their ANSI color codes; used for console logging.

    Defined colors and formatting codes:
        Foreground:
            FG_BLACK
            FG_RED
            FG_GREEN
            FG_YELLOW
            FG_BLUE
            FG_MAGENTA
            FG_CYAN
            FG_WHITE
            FG_BRIGHT_RED
            FG_BRIGHT_GREEN
            FG_BRIGHT_YELLOW
            FG_BRIGHT_BLUE
            FG_BRIGHT_MAGENTA
            FG_BRIGHT_CYAN
            FG_BRIGHT_WHITE

        Background:
            BG_BLACK
            BG_RED
            BG_GREEN
            BG_YELLOW
            BG_BLUE
            BG_MAGENTA
            BG_CYAN
            BG_WHITE
            BG_BRIGHT_RED
            BG_BRIGHT_GREEN
            BG_BRIGHT_YELLOW
            BG_BRIGHT_BLUE
            BG_BRIGHT_MAGENTA
            BG_BRIGHT_CYAN
            BG_BRIGHT_WHITE

        Formatting:
            BOLD
            UNDERLINE
            REVERSED
            RESET
    """

    FG_BLACK = "\x1b[30m"
    FG_RED = '\x1b[31m'
    FG_GREEN = '\x1b[32m'
    FG_YELLOW = '\x1b[33m'
    FG_BLUE = '\x1b[34m'
    FG_MAGENTA = '\x1b[35m'
    FG_CYAN = '\x1b[36m'
    FG_WHITE = '\x1b[37m'

    FG_BRIGHT_RED = '\x1b[31;1m'
    FG_BRIGHT_GREEN = '\x1b[32;1m'
    FG_BRIGHT_YELLOW = '\x1b[33;1m'
    FG_BRIGHT_BLUE = '\x1b[34;1m'
    FG_BRIGHT_MAGENTA = '\x1b[35;1m'
    FG_BRIGHT_CYAN = '\x1b[36;1m'
    FG_BRIGHT_WHITE = '\x1b[37;1m'

    BG_BLACK = "\x1b[40m"
    BG_RED = '\x1b[41m'
    BG_GREEN = '\x1b[42m'
    BG_YELLOW = '\x1b[43m'
    BG_BLUE = '\x1b[44m'
    BG_MAGENTA = '\x1b[45m'
    BG_CYAN = '\x1b[46m'
    BG_WHITE = '\x1b[47m'

    BG_BRIGHT_RED = '\x1b[41;1m'
    BG_BRIGHT_GREEN = '\x1b[42;1m'
    BG_BRIGHT_YELLOW = '\x1b[43;1m'
    BG_BRIGHT_BLUE = '\x1b[44;1m'
    BG_BRIGHT_MAGENTA = '\x1b[45;1m'
    BG_BRIGHT_CYAN = '\x1b[46;1m'
    BG_BRIGHT_WHITE = '\x1b[47;1m'

    BOLD = '\x1b[1m'
    UNDERLINE = '\x1b[4m'
    REVERSED = '\x1b[7m'
    RESET = '\x1b[0m'
