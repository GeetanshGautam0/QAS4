"""
FILE:           qa_std/qa_main.py
AUTHOR:         Geetansh Gautam
PROJECT:        Quizzing Application, version 4

DOC

    Quizzing application initializer script.

DEFINES


DEPENDENCIES

    sys
    typing.**
    threading.Thread
    qa_std
    enum.Enum

"""

import random, sys
from typing import Any
from qa_std import *
from enum import Enum
from qa_file_io import *


ScriptPolicy = AppPolicy.PolicyManager.Module('AppInitializer', 'qa_main.py')


class AppID(Enum):
    QuizzingForm = 0
    AdminTools = 1
    Utilities = 2


class AppManager:
    def __init__(self, app_id: AppID, *args: Any, **kwargs: Any) -> None:
        """
        AppManager

        Wrapper for launching and configuring applications.

        Errors Raised:

            __init__    ->      0x0001:0x0000 ==> 0x0001: 0xFFFF

        :raises AssertionError: 0x0001:0x0000 Invalid application ID

        :param app_id: ID of application to be launched (AppID)
        :param args:   Additional arguments (Any)
        :param kwargs: Keyword arguments (Any)
        :return: None
        """

        self.app_id = app_id
        self._ar, self._kw = args, kwargs

        assert app_id in AppID.__members__.values(), '0x0001:0x0000'

        self.run()

    def run(self) -> None:
        pass

    def __del__(self) -> None:
        sys.excepthook = sys.__excepthook__
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__


if __name__ == "__main__":
    NonvolatileFlags.NVF.create_flag('AppRun')

    ErrorManager.RedirectExceptionHandler()
    ScriptPolicy.run_as_main()

    test_file = qa_def.File('output_text.txt')
    fio = qa_file_std.FileIO()

    fio.write(test_file, f'Hello, World! {random.random()}')

    NonvolatileFlags.NVF.remove_flag('AppRun', True)
    try:
        qa_file_std.IOHistoryManager.current_task.cancel()

    except Exception as E:
        ConsoleWriter.Write.error(f'IOHistManager.CT.CANCEL:', str(E))

