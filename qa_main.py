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

import sys
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


def _terminate_app() -> None:
    # Remove the AppRun flag, if it exists
    NonvolatileFlags.NVF.remove_flag('AppRun', True)

    try:
        file_io_manager.iohm.current_task.cancel()
    except Exception as E:
        ConsoleWriter.Write.error(f'IOHistManager.CT.CANCEL:', str(E))

    sys.excepthook = sys.__excepthook__


if __name__ == "__main__":
    NonvolatileFlags.NVF.create_flag('AppRun')
    ErrorManager.RedirectExceptionHandler()
    
    AppLogger = Logger()
    ErrorManager._global_logger = AppLogger
    ThemeManager._global_logger = AppLogger
    
    # Add a new error hook task that removes the AppRun flag (contingent on whether the error is fatal)
    ErrorManager.Minf_EH_Md7182_eHookTasks.append(
        (lambda is_fatal: is_fatal, lambda: NonvolatileFlags.NVF.remove_flag('AppRun', True))
    )

    # Add a new error hook task that cancels file_io_manager's IOHistory timer (contingent on whether the error is fatal)
    ErrorManager.Minf_EH_Md7182_eHookTasks.append(
        (lambda is_fatal: is_fatal, file_io_manager.iohm.current_task.cancel)
    )

    # Check if the script is allowed to run as main (it has to be)
    ScriptPolicy.run_as_main()
    assert sys.excepthook == ErrorManager._O_exception_hook, 'Exception hook was not redirected.'

    # --------------------------------------------------------------------------------------------
    
    
    
    AppLogger.write(
        LogDataPacket(
            'AppInitializer', 
            LoggingLevel.L_EMPHASIS, 
            f'Generated log file {AppLogger._lfile.file_name}'
        )
    )
    
    ThemeManager.T_Config._get_pref_theme_()
    
    # --------------------------------------------------------------------------------------------

    # Call _terminate_app and exit with code 0
    _terminate_app()
    sys.exit(0)
