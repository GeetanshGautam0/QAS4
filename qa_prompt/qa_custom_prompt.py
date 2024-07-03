"""
FILE:           qa_custom_prompt.py
AUTHOR:         Geetansh Gautam
PROJECT:        Quizzing Application, version 4

DOC

    Quizzing application custom prompts

DEFINES

    Type                        Name                                Description
    ----------------------------------------------------------------------------
    Enum                        PromptType
    Struct                      Prompt                              Prompt Object
         PromptType                 TYPE
         String                     TITLE
         String                     BODY_TEXT
         SharedMemoryDict           SMD_OBJECT                      A shared memory dictionary object
         [(String, String), ...]    BUTTONS                         List of buttons (DISPLAY, RESPONSE)
    class                       StandardResponses                   A list of standardized responses

DEPENDENCIES

    * tkinter
    * typing
        - List
        - Tuple
        - Optional
    * overloading
        - overload
    * shared_memory_dict
    * enum
    * QA ThemeManager
        - ThemeInfo
        - Theme

"""

import tkinter as tk
from shared_memory_dict import SharedMemoryDict
from dataclasses import dataclass
from overloading import overload
from enum import Enum
from typing import (
    List, Tuple,
    Optional
)

from qa_std.qa_app_pol import PolicyManager


ScriptPolicy = PolicyManager.Module('CustomPrompts', 'qa_custom_prompt.py')


class PromptType(Enum):
    (
        MSG_ERR,  # Error Message
        MSG_WAR,  # Warning Message
        MSG_SUC,  # Success Message
        MSG_INF,  # Info Message
        INP_BTN  # Button Input
    ) = range(5)


class _LoggingLevel(Enum):
    (
        _ERR,
        _WAR,
        _SUC,
        _GEN
    ) = range(4)


class StandardResponses:
    CANCEL = '_cancel'
    OK = '_ok'
    ACCEPT = '_accept'
    REJECT = '_reject'
    EXIT = '_exit'

    UPDATE_STABLE_STREAM = '_stab_stream'
    UPDATE_BETA_STREAM = '_beta_stream'
    UPDATE_ALPHA_STREAM = '_alph_stream'


@dataclass
class Theme:
    BG: str
    FG: str
    RD: str
    YE: str
    GR: str
    AC: str
    FF: str
    FS_M: int
    FS_L: int
    FS_S: int
    FS_T: int


_theme_def_light = Theme(
    BG='#FFFFFF',
    FG='#000000',
    RD='#E01A00',
    YE='#D6A630',
    GR='#138811',
    AC='#2DB2E7',
    FF='Montserrat Black',
    FS_T=29,
    FS_L=20,
    FS_M=14,
    FS_S=10
)


@dataclass
class Prompt:
    TYPE: PromptType
    TITLE: str
    BODY_TEXT: str
    SMD_OBJECT: SharedMemoryDict
    BUTTONS: List[Tuple[str, str]]

    _LONG_MODE: bool = False

    def __init__(
            self,
            prt: PromptType,
            ttl: str,
            bdy: str,
            smd: SharedMemoryDict,
            btn: Optional[List[Tuple[str, str]]]
    ) -> None:
        self.TYPE = prt
        self.TITLE = ttl.strip()
        self.BODY_TEXT = bdy.strip()
        self.SMD_OBJECT = smd

        self._LONG_MODE = len(self.BODY_TEXT) >= 100  # Enabled long mode if  body text is longer than 100 characters

        if btn is None:
            self.BUTTONS = [
                ('OKAY', StandardResponses.OK),
                ('CANCEL', StandardResponses.CANCEL)
            ]

        else:
            assert isinstance(btn, list)
            assert len(btn)

            _b: List[Tuple[str, str]] = []

            for e in btn:
                assert isinstance(e, tuple)
                assert len(e) == 2
                assert isinstance(e[0], str) and isinstance(e[1], str)
                assert len(e[0].strip()) and len(e[1].strip())

                _b = [*_b, (e[0].strip(), e[1].strip())]

            self.BUTTONS = _b

    @overload(__init__)  # type: ignore
    def __init__(
            self,
            prompt_type: PromptType,
            title: str,
            body_text: str,
            smd: SharedMemoryDict
    ) -> None:
        ...

    @overload(__init__)  # type: ignore
    def __init__(
            self,
            prompt_type: PromptType,
            title: str,
            body_text: str,
            smd: SharedMemoryDict,
            buttons: List[Tuple[str, str]]
    ) -> None:
        ...


class _PROMPT:
    def __init__(
            self,
            prompt: Prompt,
            master: Optional[tk.Tk] = None
    ) -> None:
        self.tp_lvl = tk.Toplevel(master=master)  # type: ignore
        self.theme: Optional[Theme] = None

    def log(self, ll: _LoggingLevel, data: str) -> None:
        pass


if __name__ == "__main__":
    ScriptPolicy.run_as_main()
