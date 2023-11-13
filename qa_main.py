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

import random, sys, io
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
    # Add a new error hook task that removes the AppRun flag
    ErrorManager.Minf_EH_Md7182_eHookTasks.append(
        (lambda is_fatal: is_fatal, lambda: NonvolatileFlags.NVF.remove_flag('AppRun', True))
    )

    # Add a new error hook task that cancels file_io_manager's IOHistory timer
    ErrorManager.Minf_EH_Md7182_eHookTasks.append(
        (lambda is_fatal: is_fatal, file_io_manager.iohm.current_task.cancel)
    )

    # Check if the script is allowed to run as main (it has to be)
    ScriptPolicy.run_as_main()
    assert sys.excepthook == ErrorManager._O_exception_hook, 'Exception hook was not redirected.'

    # Test file IO manager
    test_file = qa_def.File('output_text.txt')
    file_io_manager.write(test_file, f'Hello, World! {random.random()}')

    theme_file = ThemeFile.ThemeFile.generate_file_data(ThemeManager.ThemeFile_s(
        qa_file_std.HeaderData(
            b'\x01\xff\x17\x12',
            b'\x00\x01', 1,
            b'\x00\x01', 1,
            qa_file_std.FileType.Theme
        ),
        'Geetansh Gautam',
        'Default',
        qa_def.File(f'.src\\.theme\\default_themes.{ThemeFile.ThemeFile.extension}'),
        [
            ThemeFile.Theme(
                'Dark Mode',
                '0xff:0x0001',
                qa_def.HexColor('#202020'),
                qa_def.HexColor('#ffffff'),
                qa_def.HexColor('#73ab84'),
                qa_def.HexColor('#ff3a20'),
                qa_def.HexColor('#efca08'),
                qa_def.HexColor('#3cc7f2'),
                qa_def.HexColor('#929292'),
                'Monserrat Semibold', 'Monserrat',
                29, 20, 14, 10,
                0, qa_def.HexColor('#000000')
            ),
            ThemeFile.Theme(
                'Light Mode',
                '0xff:0x0002',
                qa_def.HexColor('#ffffff'),
                qa_def.HexColor('#000000'),
                qa_def.HexColor('#138811'),
                qa_def.HexColor('#E01A00'),
                qa_def.HexColor('#D6A630'),
                qa_def.HexColor('#2DB2E7'),
                qa_def.HexColor('#5C5C5C'),
                'Monserrat Semibold', 'Monserrat',
                29, 20, 14, 10,
                0, qa_def.HexColor('#000000')
            )
        ],
        0, '0'
    ))

    file_io_manager.write(qa_def.File(f'.src\\.theme\\default_themes.{ThemeFile.ThemeFile.extension}'), theme_file)

    # Call _terminate_app and exit with code 0
    _terminate_app()
    sys.exit(0)
