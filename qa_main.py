"""
FILE:           qa_std/qa_main.py
AUTHOR:         Geetansh Gautam
PROJECT:        Quizzing Application, version 4

DOC

    Quizzing application initializer script.

DEFINES


DEPENDENCIES

    tkinter
    sys
    typing.**
    threading.Thread
    qa_std
    enum.Enum

"""

import sys, click
import tkinter as tk

from tkinter import messagebox
from typing import cast, Any, Dict, Callable, Optional, Type
from enum import Enum
from time import sleep

import qa_std.qa_diagnostics as Diagnostics
from qa_std import (
    AppPolicy, NonvolatileFlags, ConsoleWriter,
    Logger, LoggingLevel, LogDataPacket,
    qa_def, ErrorManager, ThemeManager
)
from qa_file_io import file_io_manager
from qa_ui import RunAdminTools, CreateSplashScreen
from qa_ui.qa_ui_def import UI_OBJECT

ScriptPolicy = AppPolicy.PolicyManager.Module('AppInitializer', 'qa_main.py')


class AppID(Enum):
    QuizzingForm = 0
    AdminTools = 1
    Utilities = 2


class AppManager:
    RunAppFunctions: Dict[AppID, Callable[[object, tk.Tk, Logger], UI_OBJECT]] = {
        AppID.AdminTools: RunAdminTools
    }

    def __init__(self, app_id: AppID, *args: Any, **kwargs: Any) -> None:
        """
        AppManager

        Wrapper for launching and configuring applications.

        Errors Raised:

            __init__    ->      0x0001:0x0000 ==> 0x0001:0x0000

        :raises AssertionError: 0x0001:0x0000 Invalid application ID

        :param app_id: ID of application to be launched (AppID)
        :param args:   Additional arguments (Any)
        :param kwargs: Keyword arguments (Any)
        :return: None
        """

        self.app_id = app_id
        self._ar, self._kw = args, kwargs
        self._tk_master: Optional[tk.Tk] = None
        self._tu_id = None

        self._ui: Optional[UI_OBJECT] = None
        self._quit_signals = 0
        self._task_2739: Optional[str] = None

        self.boot_steps = [
            'Running Diagnostics',
            'Initializing User Interface',
            'Boot Sequence Complete'
        ]

        assert app_id in AppID.__members__.values(), '0x0001:0x0000'

        self.run()

    def _on_app_close(self) -> None:
        assert isinstance(self._ui, UI_OBJECT)
        self._quit_signals += 1

        def _reset_quit_signal(cls: AppManager) -> None:
            cls._quit_signals = 0

            AppLogger.write(LogDataPacket(
                'AppInstanceManager - AIM',
                LoggingLevel.L_EMPHASIS,
                'The quit signal counter has been reset to zero.'
            ))

        try:    cast(tk.Tk, self._tk_master).after_cancel(cast(str, self._task_2739))
        except: pass

        self._task_2739 = self._tk_master.after(15_000, _reset_quit_signal, self)  # type: ignore

        # Ask the app if it is good to close
        if self._ui.ready_to_close:
            AppLogger.write(LogDataPacket(
                'AppInstanceManager - AIM',
                LoggingLevel.L_EMPHASIS,
                'Sending the app termination signal.'
            ))

            # Send the closure signal
            self._ui.close()
            _terminate_app_()

            sys.exit(0)

        elif self._quit_signals >= 3:
            AppLogger.write(LogDataPacket(
                'AppInstanceManager - AIM',
                LoggingLevel.L_ERROR,
                'FORCE QUIT COMMAND RECEIVED.'
            ))

            messagebox.showerror('Quizzing App | App Instance Manager', 'FORCE QUIT command received.')
            self._ui.close()
            cast(tk.Tk, self._tk_master).destroy()
            _terminate_app_()

            sys.exit(0)

        else:
            AppLogger.write(LogDataPacket(
                'AppInstanceManager - AIM',
                LoggingLevel.L_ERROR,
                'App not ready to close. QUIT 3 times in 15 seconds to FORCE QUIT.'
            ))

    def temp_update(self) -> None:
        cast(tk.Tk, self._tk_master).update()  # type: ignore
        cast(tk.Tk | tk.Toplevel, self.splash_screen.toplevel).update()  # type: ignore

        self._tu_id = self.splash_screen.toplevel.after(100, self.temp_update)  # type: ignore

    def run(self) -> None:
        global AppLogger

        if isinstance(self._ui, UI_OBJECT):
            return

        self._tk_master = tk.Tk()
        self._tk_master.withdraw()

        self._tk_master.title('QA4 | App Instance Manager (AIM)')

        self.splash_screen = CreateSplashScreen(self, self._tk_master, AppLogger, _terminate_app_, self.boot_steps)
        self.temp_update()

        self.splash_screen.set_app_name(
            {
                AppID.AdminTools: 'Administrator Tools',
                AppID.Utilities: 'Utilities',
                AppID.QuizzingForm: 'Quizzing Form'
            }[self.app_id]
        )

        # Run diagnostics

        self.splash_screen.increment_progress()

        _run_essential_diagnostics_()

        # Launch the app UI.

        self.splash_screen.increment_progress()

        self._ui = AppManager.RunAppFunctions[self.app_id](self, self._tk_master, AppLogger)

        # Boot sequence complete

        self.splash_screen.increment_progress()

        assert self.splash_screen.complete_boot

        self.splash_screen.toplevel.after_cancel(cast(str, self._tu_id))
        self.splash_screen.toplevel.destroy()

        self._tk_master.protocol('WM_DELETE_WINDOW', self._on_app_close)
        self._ui.toplevel.protocol('WM_DELETE_WINDOW', self._on_app_close)

        self._ui.toplevel.wm_deiconify()
        self._ui.toplevel.overrideredirect(False)
        self._ui.toplevel.focus_get()

        self._ui.toplevel.mainloop()

    def __del__(self) -> None:
        sys.excepthook = sys.__excepthook__
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__


_ActiveApp: AppManager


def _terminate_app_(**kwargs: Any) -> None:
    """

    :keyword redirect_exception_hook: Redirect the exception hook to sys.__excepthook__

    :param kwargs: Keyword arguments
    :return: None
    """

    # Remove the AppRun flag, if it exists
    NonvolatileFlags.NVF.remove_flag('AppRun', True)

    try:
        file_io_manager.iohm.current_task.cancel()
    except Exception as E:
        ConsoleWriter.Write.error(f'IOHistManager.CT.CANCEL:', str(E))

    if kwargs.get('redirect_exception_hook', False):
        sys.excepthook = sys.__excepthook__


def _check_for_tickets_() -> None:
    global AppLogger
    
    AppLogger.write(LogDataPacket('AppInitializer', LoggingLevel.L_GENERAL, 'Looking for maintainance tickets.'))
    
    flags = NonvolatileFlags.NVF.yield_all_flags()
    for flag in flags:
        match flag:
            case 'TCKT_APP_UPDT':
                # Ask the user whether to update the app or not.
                raise qa_def.NotYetImplemented('Update ticket system')

            case 'TCKT_APP_REQ_UPDT':
                # Update mandatory.
                AppLogger.write(LogDataPacket('AppInitializer', LoggingLevel.L_WARNING, 'APP UPDATE MANDATED.'))
                raise qa_def.NotYetImplemented('Update ticket system')
            
            case _:
                pass


@click.group()
def CommandLineInterface() -> None:
    pass


StartAppIDs = ['quizzing_app', 'admin_tools', 'util']


def raise_error_routine(exception: Type[BaseException], *error_args: Any, quit_app: bool = True) -> None:
    global _ActiveApp

    if quit_app and '_ActiveApp' in dir():
        assert isinstance(_ActiveApp, AppManager)

        if isinstance(_ActiveApp._tk_master, tk.Tk):
            _ActiveApp._ui.close()  # type: ignore
            _ActiveApp._tk_master.destroy()  # type: ignore

    _terminate_app_(redirect_exception_hook=False)

    raise exception(*error_args)


@CommandLineInterface.command()
@click.argument('app_name')
@click.option('--lapp', is_flag=True)
@click.option('--disable_VLE', is_flag=True)
def start_app(**kwargs: Optional[None]) -> None:
    global StartAppIDs, AppLogger

    assert kwargs.get('lapp') == True, 'Add the --lapp flag to enable the app to boot.'

    app: Optional[AppID] = None
    app_name = kwargs.pop('app_name')

    match app_name:
        case 'quizzing_app':
            app = AppID.QuizzingForm

        case 'admin_tools':
            app = AppID.AdminTools

        case 'util':
            app = AppID.Utilities

        case '_RDQ':
            _run_essential_diagnostics_()
            sys.stdout.write('General app diagnostics complete. Run util to run all diagnostics.\n')

            # Terminate app
            _terminate_app_()
            sys.exit(0)

        case _:
            raise_error_routine(Exception, 'Invalid/Unexpected app ID.')

    AppLogger.DISABLE_VLE = cast(bool, kwargs.get('disable_vle', False))

    assert isinstance(app, AppID)
    _ActiveApp = AppManager(app, **kwargs)


def _run_essential_diagnostics_() -> None:
    """
    RUN ESSENTIAL DIAGNOSTICS

    Essential diagnostics include:
    * F001:0000 (AC.locale)
    * F001:0001 (AC.ConvertColor)
    * F001:0002 (AC.File)
    * F001:0004 (AC.DTC)
    * F001:0005 (AC.DTC)
    * F001:0006 (AC.DTC)
    * F001:0007 (AC.DTC)
    * F001:0008 (AC.DTC)
    * F001:0009 (AC.DTC)
    * F001:000A (AC.DTC)
    * F001:000B (AC.DTC)
    * F001:000C (AC.DTC)
    * F001:000D (AC.DTC)
    * F001:000E (AC.DTC)
    * F001:000F (AC.DTC)
    * F001:0010 (AC.DTC)
    * F001:0011 (AC.DTC)
    * F001:0012 (AC.DTC)
    * F001:0013 (AC.DTC)
    * F001:0014 (AC.DTC)
    * F001:0015 (AC.DTC)
    * F001:0016 (AC.DTC)
    * F001:0017 (AC.DTC)
    * F001:0018 (AC.DTC)
    * F001:0019 (AC.DTC)
    * F001:001A (AC.DTC)
    * F001:001B (AC.DTC)
    * F001:001C (AC.DTC)
    * F001:001D (AC.DTC)
    * F001:001E (AC.DTC)
    * F001:001F (AC.DTC)
    * F001:0020 (AC.DTC)
    * F001:0021 (AC.DTC)
    * F001:0022 (AC.DTC)
    * F001:0023 (AC.DTC)
    * F001:0024 (AC.DTC)
    * F001:0025 (AC.DTC)
    * F001:0026 (AC.DTC)
    * F001:0027 (AC.DTC)
    * F001:0028 (AC.File.SOURCE_FILES)

    :return: None
    """

    AppLogger.add_empty_line()
    AppLogger.write(LogDataPacket('AppInitializer', LoggingLevel.L_EMPHASIS, 'Running essential diagnostics.'))

    assert Diagnostics.ModDiagnostics.locale(), 'Diagnostic failed.'
    assert Diagnostics.ModDiagnostics.qa_def(), 'Diagnostic failed.'
    assert Diagnostics.ModDiagnostics.qa_dtc(), 'Diagnostic failed.'
    assert Diagnostics.ModDiagnostics.check_source_files(), 'Diagnostic failed.'


if __name__ == "__main__":
    if '--lapp' in sys.argv:
        NonvolatileFlags.NVF.create_flag('AppRun')
        ErrorManager.RedirectExceptionHandler()

        AppLogger = Logger()
        ErrorManager._global_logger = AppLogger
        ThemeManager._global_logger = AppLogger
        Diagnostics._global_logger = AppLogger

        # Add a new error hook task that removes the AppRun flag (contingent on whether the error is fatal)
        ErrorManager.Minf_EH_Md7182_eHookTasks.append(
            (lambda is_fatal: is_fatal, lambda: NonvolatileFlags.NVF.remove_flag('AppRun', True))  # type: ignore
        )
        # Add a new error hook task that cancels file_io_manager's IOHistory timer
        #   (contingent on whether the error is fatal)
        ErrorManager.Minf_EH_Md7182_eHookTasks.append(
            (lambda is_fatal: is_fatal, file_io_manager.iohm.current_task.cancel)  # type: ignore
        )

        ErrorManager.Minf_EH_Md7182_eHookTasks.append(
            (lambda is_fatal: is_fatal, lambda: AppLogger.thread.join(AppLogger, 0))  # type: ignore
        )

        # Check if the script is allowed to run as main (it has to be)
        ScriptPolicy.run_as_main()
        # assert sys.excepthook == ErrorManager._O_exception_hook, 'Exception hook was not redirected.'

        # --------------------------------------------------------------------------------------------

        # Check for tickets
        _check_for_tickets_()

        # Load the theme data
        ThemeManager._global_logger = AppLogger

        # Run the command line interface --> Run the app.
        CommandLineInterface()

        # --------------------------------------------------------------------------------------------

        # Call _terminate_app_ and exit with code 0
        _terminate_app_(redirect_exception_hook=True)
        sys.exit(0)

    else:
        sys.stdout.write('[WARN] --lapp flag not found; app boot disabled')
