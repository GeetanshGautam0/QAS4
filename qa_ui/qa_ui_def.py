import tkinter as tk
from threading import Thread
from typing import List, Tuple, Any, cast, Optional

from qa_std.qa_def import (
    UpdateCommand as UC,
    UpdateVariables as UV,
    HexColor
)
from qa_std import LogDataPacket, LoggingLevel, ThemeManager, AppInfo


class UI_OBJECT(Thread):
    def __init__(self) -> None:
        super(UI_OBJECT, self).__init__()

        self.update_requests: List[List[tk.Widget, Tuple[UC, List[Any, ...]]]] = []
        self.post_update_req: List[List[tk.Widget, Tuple[UC, List[Any, ...]]]] = []

        self._theme: Optional[ThemeManager.Theme] = None

        self.pad_x: Optional[int] = None
        self.pad_y: Optional[int] = None

        self.start()

    @property
    def toplevel(self) -> tk.Toplevel:
        raise NotImplementedError('Property _toplevel_ not yet defined.')

    @property
    def ready_to_close(self) -> bool:
        return True

    def close(self) -> bool:
        raise NotImplementedError('App termination behaviour not yet defined.')

    def load_theme(self) -> None:
        ThemeManager.ThemeInfo.load_all_data()
        self._theme = ThemeManager.ThemeInfo.preferred_theme

    @staticmethod
    def log(_: LogDataPacket) -> None:
        return  # Add a log command here once the logger instance is available

    def apply_update_reqs(self, reqs: List[Any]) -> None:
        for entry in reqs:
            _el, *requests = entry
            element = cast(tk.Label | tk.Widget, _el)

            for request in requests:
                command, _a = request
                args = []

                for arg in _a:

                    if arg in UV.__members__.values():
                        arg = {
                            UV.BACKGROUND: self._theme.background,
                            UV.FOREGROUND: self._theme.foreground,
                            UV.BORDER_COLOR: self._theme.border_color,
                            UV.BORDER_WIDTH: self._theme.border_radius,
                            UV.ACCENT_COLOR: self._theme.accent,
                            UV.ERROR_COLOR: self._theme.error,
                            UV.WARNING_COLOR: self._theme.warning,
                            UV.GRAY_COLOR: self._theme.grey,
                            UV.OK_COLOR: self._theme.successful,
                            UV.FONT_FACE: self._theme.font_face,
                            UV.TITLE_FONT_FACE: self._theme.title_font_face,
                            UV.TITLE_FONT_SIZE: self._theme.font_size_title,
                            UV.LARGE_FONT_SIZE: self._theme.font_size_large,
                            UV.NORML_FONT_SIZE: self._theme.font_size_normal,
                            UV.SMALL_FONT_SIZE: self._theme.font_size_small,
                        }[arg]

                    elif isinstance(arg, (list, tuple)):
                        if len(arg) > 1:
                            if arg[0] == UC.CUSTOM:  # Run a custom command
                                arg.pop(0)
                                if len(arg) == 1:
                                    arg = arg[0]()
                                else:
                                    arg = arg[0](arg[1::])

                    else:
                        arg = {
                            'PAD_X': self.pad_x,
                            'PAD_Y': self.pad_y,
                            'SCR_W': self.toplevel.winfo_screenwidth(),
                            'SCR_H': self.toplevel.winfo_screenheight(),
                            'WND_W': self.toplevel.winfo_width(),
                            'WND_H': self.toplevel.winfo_height()
                        }.get(arg, arg)

                    args.append(arg)

                try:
                    assert isinstance(command, UC), 'Invalid command.'
                    assert isinstance(args, list), 'Invalid arguments.'

                    match command:
                        case UC.BACKGROUND:
                            assert len(args) == 1
                            assert isinstance(args[0], HexColor)
                            element.config(background=args[0].color)

                        case UC.FOREGROUND:
                            assert len(args) == 1
                            assert isinstance(args[0], HexColor)
                            element.config(foreground=args[0].color)

                        case UC.FONT:
                            assert len(args) == 2  # Only support family and size
                            assert isinstance(args[0], str) & isinstance(args[1], int)

                            element.config(font=(*args,))

                        case UC.CUSTOM:
                            assert len(args) >= 1

                            if len(args) == 1:
                                args[0]()
                            else:
                                args[0](*args[1::])

                        case UC.BORDER_COLOR:
                            assert len(args) == 1
                            assert isinstance(args[0], HexColor)

                            element.config(
                                highlightcolor=args[0].color,
                                highlightbackground=args[0].color
                            )

                        case UC.BORDER_WIDTH:
                            assert len(args) == 1
                            assert isinstance(args[0], (float, int))

                            element.config(
                                highlightthickness=args[0],
                                borderwidth=args[0],
                                bd=args[0],
                            )

                        case _:
                            raise NotImplementedError('Update command.')

                except Exception as E:
                    self.log(LogDataPacket(
                        'UIObject',
                        LoggingLevel.L_ERROR,
                        f'Failed to apply command {command} to {element}: {E}'
                    ))

                else:
                    if AppInfo.ConfigurationFile.config.VLE:  # Verbose logging enabled
                        self.log(LogDataPacket(
                            'UIObject',
                            LoggingLevel.L_GENERAL,
                            f'[VERBOSE LOGGING ENABLED] Applied command {command} to {element}'
                        ))

    def _update_ui_plugin(self, *_, **_0) -> None:
        return  # Add your own code here.

    def update_ui(self) -> None:
        self.load_theme()
        self.apply_update_reqs(self.update_requests)

        # Extra computation goes here, if needed.
        self._update_ui_plugin()

        self.apply_update_reqs(self.post_update_req)
