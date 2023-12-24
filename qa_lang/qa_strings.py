"""
FILE:           qa_lang/qa_strings.py
AUTHOR:         Geetansh Gautam
PROJECT:        Quizzing Application, version 4

DOC

    Defines strings that the application user interface uses..

DEFINES

    Name                    Type                            Description*
    --------------------------------------------------------------------
    SplashUI                class                           Defines strings for the splash UI (in english)
    AdminToolsUI            class                           Defines strings for the admin tools UI (in english)

    _translate_             method (str)                    Translates the provided string to the correct language, per the locale.

"""

import traceback
from googletrans import Translator
from tkinter import messagebox

from qa_std import ConsoleWriter, ErrorManager


_trans = Translator(
    service_urls=[
        'translate.google.com',
        'translate.google.ca'
    ]
)


class SplashUI:
    boot_steps = [
        'Translating Text',
        'Running Diagnostics',
        'Looking for Updates',
        'Initializing User Interface',
        'Boot Sequence Complete'
    ]

    @staticmethod
    def _set_to_en() -> None:
        SplashUI.boot_steps = ['Translating Text', 'Running Diagnostics', 'Looking for Updates', 'Initializing User Interface', 'Boot Sequence Complete']

    @staticmethod
    def _t(lang: str = 'en') -> None:
        global _trans

        if lang == 'en':
            SplashUI._set_to_en()
            return

        SplashUI.boot_steps = [_trans.translate(s, dest=lang).text for s in SplashUI.boot_steps]


class AppNames:
    AdminTools = 'Administrator Tools'
    QuizzingForm = 'Quizzing Form'
    Utilities = 'Utilities'

    @staticmethod
    def _set_to_en() -> None:
        AppNames.AdminTools = 'Administrator Tools'
        AppNames.QuizzingForm = 'Quizzing Form'
        AppNames.Utilities = 'Utilities'

    @staticmethod
    def _t(lang: str = 'en') -> None:
        global _trans

        if lang == 'en':
            AppNames._set_to_en()
            return

        AppNames.AdminTools = _trans.translate(AppNames.AdminTools, dest=lang).text
        AppNames.QuizzingForm = _trans.translate(AppNames.QuizzingForm, dest=lang).text
        AppNames.Utilities = _trans.translate(AppNames.Utilities, dest=lang).text


def translate(lang: str) -> None:
    try:

        SplashUI._t(lang)
        AppNames._t(lang)

    except Exception as E:
        ErrorManager.InvokeException(
            ErrorManager.ExceptionObject(ErrorManager.ExceptionCodes.INTERNAL_ERROR, Raise=False, fatal=False),
            Exception,
            f'Failed to translate application strings to desired LANG ({lang})\n',
            traceback.format_exc()
        )
        messagebox.showerror(
            'QA4 | LANGUAGE MANAGER',
            f'Failed to translate application strings to the desired language. Only ENGLISH is available.\n\n{E}'
        )

        SplashUI._set_to_en()
        AppNames._set_to_en()
