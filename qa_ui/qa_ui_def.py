import tkinter as tk, traceback
from threading import Thread
from typing import (
    List, Tuple, SupportsIndex, Set,
    Optional, Any,
    cast,
)

from qa_std.qa_def import (
    UpdateCommand as UC, UpdateVariables as UV
)
from qa_std import (
    LogDataPacket, LoggingLevel,
    ThemeManager,
    AppInfo
)


class UI_OBJECT:
    def __init__(self) -> None:
        super(UI_OBJECT, self).__init__()

        self.VLE_ENABLED = True
        self.update_requests: List[List[tk.Widget, Tuple[UC, List[Any, ...]]]] = []
        self.post_update_req: List[List[tk.Widget, Tuple[UC, List[Any, ...]]]] = []

        self._theme: Optional[ThemeManager.Theme] = None

        self.pad_x: Optional[int] = None
        self.pad_y: Optional[int] = None

        self.run()

    def run(self) -> None:
        raise NotImplementedError

    @property
    def toplevel(self) -> tk.Toplevel | tk.Tk:
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
        return  # Add a log command here in the subclass when the logger instance is available

    def _ureq_manage_args(self, element: tk.Widget, args: List[Any] | Tuple[Any] | Set[Any] | SupportsIndex) -> List[Any]:
        output = []

        for arg in args:

            if arg in UV.__members__.values():
                arg = {
                    UV.BACKGROUND: self._theme.background.color,
                    UV.FOREGROUND: self._theme.foreground.color,
                    UV.BORDER_COLOR: self._theme.border_color.color,
                    UV.BORDER_WIDTH: self._theme.border_radius,
                    UV.ACCENT_COLOR: self._theme.accent.color,
                    UV.ERROR_COLOR: self._theme.error.color,
                    UV.WARNING_COLOR: self._theme.warning.color,
                    UV.GRAY_COLOR: self._theme.grey.color,
                    UV.OK_COLOR: self._theme.successful.color,
                    UV.FONT_FACE: self._theme.font_face,
                    UV.TITLE_FONT_FACE: self._theme.title_font_face,
                    UV.TITLE_FONT_SIZE: self._theme.font_size_title,
                    UV.LARGE_FONT_SIZE: self._theme.font_size_large,
                    UV.NORML_FONT_SIZE: self._theme.font_size_normal,
                    UV.SMALL_FONT_SIZE: self._theme.font_size_small,
                }[arg]

            elif isinstance(arg, (list, tuple, set)):
                arg = [*arg]  # Convert to a list to allow for the 'pop' function to be called.

                if len(arg) > 1:
                    if arg[0] == UC.CUSTOM:  # Run a custom command
                        arg.pop(0)
                        if len(arg) == 1:
                            arg = arg[0]()
                        else:
                            cargs = self._ureq_manage_args(element, arg[1::])
                            arg = arg[0](*cargs)

            else:
                arg = {
                    'PAD_X': self.pad_x,
                    'PAD_Y': self.pad_y,
                    'ELMNT': element,
                }.get(arg, arg)

                try:
                    narg = {
                        'SCR_W': self.toplevel.winfo_screenwidth(),
                        'SCR_H': self.toplevel.winfo_screenheight(),
                        'WND_W': self.toplevel.winfo_width(),
                        'WND_H': self.toplevel.winfo_height(),
                    }.get(arg, arg)

                except NotImplementedError:
                    pass

                else:
                    arg = narg
                    del narg

            output.append(arg)

        return output

    def apply_update_reqs(self, reqs: List[Any]) -> None:
        self.toplevel.update()

        for entry in reqs:
            _el, *requests = entry
            element = cast(tk.Label | tk.Widget, _el)

            for request in requests:
                command, _a = request
                args = self._ureq_manage_args(element, _a)

                try:
                    assert isinstance(command, UC), 'Invalid command.'
                    assert isinstance(args, list), 'Invalid arguments.'

                    match command:
                        case UC.BACKGROUND:
                            assert len(args) == 1
                            element.config(background=args[0])

                        case UC.FOREGROUND:
                            assert len(args) == 1
                            element.config(foreground=args[0])

                        case UC.FONT:
                            assert len(args) == 2  # Only support family and size
                            assert isinstance(args[0], str) & isinstance(args[1], int)

                            element.config(font=(*args,))

                        case UC.CUSTOM:
                            assert len(args) >= 1

                            if len(args) == 1:
                                args[0]()
                            else:
                                cargs = self._ureq_manage_args(element, args[1::])
                                args[0](*cargs)

                        case UC.BORDER_COLOR:
                            assert len(args) == 1

                            element.config(
                                highlightcolor=args[0],
                                highlightbackground=args[0]
                            )

                        case UC.BORDER_WIDTH:
                            assert len(args) == 1
                            assert isinstance(args[0], (float, int))

                            element.config(
                                highlightthickness=args[0],
                                borderwidth=args[0],
                                bd=args[0],
                            )

                        case UC.ACTIVE_BACKGROUND:
                            assert len(args) == 1

                            element.config(activebackground=args[0])

                        case UC.ACTIVE_FOREGROUND:
                            assert len(args) == 1

                            element.config(activeforeground=args[0])

                        case UC.WRAP_LENGTH:
                            assert len(args) == 1
                            assert isinstance(args[0], (float, int))

                            element.config(wraplength=args[0])

                        case _:
                            raise NotImplementedError('Update command.')

                except Exception as E:
                    if AppInfo.ConfigurationFile.config.VLE & self.VLE_ENABLED:  # Verbose logging enabled
                        self.log(LogDataPacket(
                            'UIObject',
                            LoggingLevel.L_ERROR,
                            f'[VERBOSE LOGGING ENABLED] Failed to apply command {command} to {element}: {traceback.format_exc()}.'
                        ))

                    else:
                        self.log(LogDataPacket(
                            'UIObject',
                            LoggingLevel.L_ERROR,
                            f'Failed to apply command {command} to {element}: {E}.'
                        ))

                else:
                    if AppInfo.ConfigurationFile.config.VLE & self.VLE_ENABLED:  # Verbose logging enabled
                        self.log(LogDataPacket(
                            'UIObject',
                            LoggingLevel.L_GENERAL,
                            f'[VERBOSE LOGGING ENABLED] Applied command {command} to {element}'
                        ))

    def _update_ui_plugin(self, *_, **__) -> None:
        return  # Add your own code here.

    def update_ui(self) -> None:
        self.load_theme()
        self.apply_update_reqs(self.update_requests)

        # Extra computation goes here, if needed.
        self._update_ui_plugin()

        self.apply_update_reqs(self.post_update_req)

        # Functions to create update requests
        # The syntax for adding an update request:
        #
        #       [... [ELEMENT, [COMMAND, [ARGS]], ...]]

    def _crt_updt_req_frame(
            self,
            frame: tk.Tk | tk.Toplevel | tk.Frame
    ) -> None:
        self.update_requests.append(
            [
                cast(tk.Widget, frame),
                [UC.BACKGROUND, [UV.BACKGROUND]]
            ]
        )

    def _crt_updt_req_label(
            self,
            label: tk.Label | tk.LabelFrame,
            bg: str | UV = UV.BACKGROUND,
            fg: str | UV = UV.FOREGROUND,
            font_size: int | UV = UV.NORML_FONT_SIZE,
            font_face: str | UV = UV.FONT_FACE,
    ) -> None:
        self.update_requests.append(
            [
                label,
                [UC.BACKGROUND, [bg]],
                [UC.FOREGROUND, [fg]],
                [UC.FONT, (font_face, font_size)],
            ]
        )
