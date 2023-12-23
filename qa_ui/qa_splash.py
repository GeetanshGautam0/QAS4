"""
FILE:           qa_ui/qa_splash.py
AUTHOR:         Geetansh Gautam
PROJECT:        Quizzing Application, version 4

DOC

    Splash UI.

DEFINES


DEPENDENCIES

    Quizzing Application Standard Library
        * ThemeManager
        * LocaleManager
        * AppInfo
        * AppPolicy
        * Logger
        * Logging Level
        * LogDataPacket (LDP)
        * qa_def

    Quizzing Application User Interface Library
        * UI_OBJECT

    tkinter
    typing

"""

import tkinter as tk, sys
from tkinter import ttk
from typing import Optional, Callable, List, Any, cast

from qa_std import (
    AppInfo,
    AppPolicy,
    Logger, LogDataPacket
)
from qa_std.qa_def import UpdateVariables as uV, Color, clamp
from .qa_ui_def import UI_OBJECT

_splash_logger: Optional[Logger] = None
ScriptPolicy = AppPolicy.PolicyManager.Module('qa_splash.py', 'Splash Screen UI')


class SplashUI(UI_OBJECT):
    def __init__(self, app_instance: object, master: tk.Tk, termination_function: Callable[[], None], steps: List[str]) -> None:
        self._ai = app_instance
        self._master = master
        self._tf = termination_function
        self._s = steps
        self._progress_tracker = 0

        self._tl = tk.Toplevel(master)

        ws_ratio = 1/2

        self.screen_size = (self._master.winfo_screenwidth(), self._master.winfo_screenheight())
        self.window_size = [int(0.4 * self.screen_size[0]), ]
        self.window_size = (self.window_size[0], int(self.window_size[0] * ws_ratio))  # type: ignore
        self.screen_size = (
            self.screen_size[0] // 2 - self.window_size[0] // 2,
            self.screen_size[1] // 2 - self.window_size[1] // 2
        )

        self.style = ttk.Style(self._tl)
        self.style.theme_use('default')

        # Elements
        self.f1, self.f2 = tk.Frame(self._tl), tk.Frame(self._tl)
        self.sf1 = tk.Label(self.f1)

        self.close_button = ttk.Button(self.f1)

        self.app_name_lbl = tk.Label(self.f2)
        self.info_lbl = tk.Label(self.f2)
        self.pb_var = tk.DoubleVar(self.f2, 0)

        self.progress_bar = ttk.Progressbar(
            self.f2, variable=self.pb_var, length=100, mode='determinate', orient=tk.HORIZONTAL
        )

        self._v73 = False
        self._g = None

        # Initialize the parent class (which calls run and defines several UI functions)
        super(SplashUI, self).__init__()

    @property
    def toplevel(self) -> tk.Tk | tk.Toplevel:
        return self._tl

    def close(self) -> bool:
        self._tf()  # Call the termination routine

        self._master.after(0, self._master.quit)

        try:
            sys.exit(0)
        except Exception as _:
            pass

        return True

    @property
    def complete_boot(self) -> bool:
        return len(self._s) == self._progress_tracker

    @property
    def grad(self) -> List[str]:
        if self._v73:
            return cast(List[str], self._g)

        else:
            self.load_theme()
            self._g = Color.fade(self._theme.background.color, self._theme.accent.color)  # type: ignore
            self._v73 = True

            return cast(List[str], self._g)

    @staticmethod
    def log(ldp: LogDataPacket) -> None:
        global _splash_logger
        if isinstance(_splash_logger, Logger):
            _splash_logger.write(ldp)

    def _update_ui_plugin(self, *_: Any, **__: Any) -> None:
        self.style.configure(
            "Horizontal.TProgressbar",
            foreground=self.grad[0],
            background=self.grad[0],
            troughcolor=self._theme.background.color,  # type: ignore
            borderwidth=0,
            thickness=2
        )

        self.style.configure(
            'TButton',
            background=self._theme.background.color,  # type: ignore
            foreground=self._theme.accent.color,  # type: ignore
            font=(self._theme.font_face, self._theme.font_size_normal),  # type: ignore
            focuscolor=self._theme.accent.color,  # type: ignore
            bordercolor=self._theme.border_color.color,  # type: ignore
            borderwidth=self._theme.border_radius,  # type: ignore
            highlightcolor=self._theme.border_color.color,  # type: ignore
            highlightthickness=self._theme.border_radius  # type: ignore
        )

        self.style.map(
            'TButton',
            background=[('active', self._theme.accent.color), ('disabled', self._theme.background.color), ('readonly', self._theme.grey.color)],  # type: ignore
            foreground=[('active', self._theme.background.color), ('disabled', self._theme.grey.color), ('readonly', self._theme.background.color)]  # type: ignore
        )

        self.style.configure(
            'Large.TButton',
            background=self._theme.background.color,  # type: ignore
            foreground=self._theme.accent.color,  # type: ignore
            font=(self._theme.font_face, self._theme.font_size_large),  # type: ignore
            focuscolor=self._theme.accent.color,  # type: ignore
            bordercolor=self._theme.border_color.color,  # type: ignore
            borderwidth=self._theme.border_radius,  # type: ignore
            highlightcolor=self._theme.border_color.color,  # type: ignore
            highlightthickness=self._theme.border_radius  # type: ignore
        )

        self.style.map(
            'Large.TButton',
            background=[('active', self._theme.accent.color), ('disabled', self._theme.background.color), ('readonly', self._theme.grey.color)],  # type: ignore
            foreground=[('active', self._theme.background.color), ('disabled', self._theme.grey.color), ('readonly', self._theme.background.color)]  # type: ignore
        )

        self._t_upd()

    def run(self) -> None:
        global _splash_logger

        # Have to set these values here since they are declared as None in the parent class,
        #   which is called at the end of the __init__ function and immediately calls this
        #   function.
        self.pad_x = 20 if 20 < self.window_size[0] // 20 else 0
        self.pad_y = 10 if 10 < self.window_size[1] // 20 else 0

        self.VLE_ENABLED = not cast(Logger, _splash_logger).DISABLE_VLE

        # Configure the window frame

        self._tl.geometry(
            '%sx%s+%s+%s' %
            (self.window_size[0], self.window_size[1], self.screen_size[0], self.screen_size[1])
        )
        self._tl.wm_protocol('WM_DELETE_WINDOW', self.close)
        self._tl.title('Quizzing Application v4')

        self._tl.update()

        # Configure elements

        self.sf1.config(text='Quizzing Application 4', anchor=tk.W, justify=tk.LEFT)
        self.close_button.config(text='\u00d7', command=self.close, style='Large.TButton', width=2)
        self.progress_bar.configure(style='Horizontal.TProgressbar')

        self.app_name_lbl.config(text='', anchor=tk.W, justify=tk.LEFT)
        self.info_lbl.config(anchor=tk.W, justify=tk.LEFT, text=self._s[0])

        # Place elements

        self.sf1.pack(fill=tk.X, expand=True, side=tk.LEFT)
        self.close_button.pack(fill=tk.NONE, expand=False)

        self.f2.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, pady=(0, self.pad_y))
        self.f1.pack(fill=tk.X, expand=False, padx=self.pad_x, pady=self.pad_y)

        self.app_name_lbl.pack(fill=tk.BOTH, expand=True, padx=self.pad_x * 2, pady=self.pad_y//2)
        self.progress_bar.pack(fill=tk.X, expand=False, pady=self.pad_y//2)
        self.info_lbl.pack(fill=tk.X, expand=False, padx=self.pad_x * 2, pady=self.pad_y//2)

        # Create update requests
        self._crt_updt_req_frame(self._tl)
        self._crt_updt_req_frame(self.f1)
        self._crt_updt_req_label(self.sf1, fg=uV.ACCENT_COLOR)

        self._crt_updt_req_frame(self.f2)
        self._crt_updt_req_label(self.app_name_lbl, fg=uV.ACCENT_COLOR, font_face=uV.TITLE_FONT_FACE, font_size=uV.TITLE_FONT_SIZE)
        self._crt_updt_req_label(self.info_lbl, fg=uV.FOREGROUND, font_size=uV.SMALL_FONT_SIZE)

        self.update_ui()

        # Tick and show
        self._t_upd()

        self._tl.wm_deiconify()
        self._tl.focus_get()
        self._tl.overrideredirect(True)
        self._tl.wm_attributes('-topmost', True)

    def set_app_name(self, app_name: str) -> None:
        self.app_name_lbl.config(text=app_name)
        self._t_upd()

    def increment_progress(self, resolution: int = 50) -> None:
        if self._progress_tracker >= len(self._s):
            return

        self._progress_tracker += 1
        info = self._s[self._progress_tracker - 1]

        if AppInfo.ConfigurationFile.config.BT in (AppInfo.BuildType.BETA, AppInfo.BuildType.ALPHA):
            info += f"\n{AppInfo.ConfigurationFile.config.BT.name} {AppInfo.ConfigurationFile.config.BI} ({AppInfo.ConfigurationFile.config.AVS})"

        self._t_upd()

        p = int(self._progress_tracker / len(self._s) * 100)
        p = p if p <= 100 else 100

        g = self.grad
        l = len(g)

        for pi in range(
            int(self.pb_var.get()) * resolution,
            p * resolution
        ):
            if pi >= (100 * resolution):
                break

            self.pb_var.set(pi/resolution)

            col = g[cast(int, clamp(0, int(pi/resolution/100 * l), l - 1))]

            self.style.configure("Horizontal.TProgressbar", foreground=col, background=col)
            self.app_name_lbl.config(fg=col)

            self._t_upd()

        self.info_lbl.config(text=info)

    def _t_upd(self) -> None:
        self._tl.update()
        self._master.update()

        self.progress_bar.update()


def CreateSplashScreen(
        app_instance: object,
        master: tk.Tk,
        logger_instance: Logger,
        termination_function: Callable[[], None],
        boot_steps: List[str]
) -> SplashUI:
    global _splash_logger

    _splash_logger = logger_instance
    return SplashUI(app_instance, master, termination_function, boot_steps)


if __name__ == "__main__":
    ScriptPolicy.run_as_main()
