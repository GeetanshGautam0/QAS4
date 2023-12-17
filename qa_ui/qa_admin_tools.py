"""
FILE:           qa_ui/qa_admin_tools.py
AUTHOR:         Geetansh Gautam
PROJECT:        Quizzing Application, version 4

DOC

    Quizzing application administrator tools UI.

DEFINES


DEPENDENCIES

    qa_std.*
    qa_file_io.
    UI_OBJECT
    tkinter

"""

import tkinter as tk
from tkinter import ttk, Tk
from typing import Optional, cast, Union, List
from enum import Enum

import qa_std as STD
from qa_std.qa_def import UpdateVariables as uV, UpdateCommand as uC
from .qa_ui_def import UI_OBJECT


_admin_tools_logger: Optional[STD.Logger] = None


class FrameID(Enum):
    (
        SELECTION_FRAME,
        CONFIGURE_FRAME,
        SCORE_MNG_FRAME
    ) = range(3)


class _UI(UI_OBJECT):
    def __init__(self, AI: object, master: tk.Tk) -> None:
        self._master: tk.Tk = master
        self._top_level = tk.Toplevel(master)

        self.toplevel.withdraw()

        self._ai = AI

        self.screen_size = (self._master.winfo_screenwidth(), self._master.winfo_screenheight())
        ws_rat = 4/3

        self.window_size = [self.screen_size[0] // 1.75]
        self.window_size.append(self.window_size[0] // ws_rat)
        self.window_pos = [
            self.screen_size[0] // 2 - self.window_size[0] // 2,
            self.screen_size[1] // 2 - self.window_size[1] // (30 / 17)
        ]

        self._theme: Optional[STD.ThemeManager.Theme] = None
        self.inputs: List[
            tk.Button, tk.Radiobutton, tk.Checkbutton, tk.Entry, tk.Text,
            ttk.Button, ttk.Radiobutton, ttk.Checkbutton, ttk.Entry,
        ] = []

        self._data = {
            FrameID.SELECTION_FRAME: {
                '_upt_req_submitted': False
            },
            FrameID.CONFIGURE_FRAME: {
                '_upt_req_submitted': False
            },
            FrameID.SCORE_MNG_FRAME: {
                '_upt_req_submitted': False
            },
        }

        # Tkinter Elements
        #       Frames
        self.selection_frame = tk.Frame(self._top_level)
        self.configure_frame = tk.Frame(self._top_level)
        self.score_mng_frame = tk.Frame(self._top_level)

        #       Selection Frame
        self.sel_frame_title = tk.Label(self.selection_frame)

        super(_UI, self).__init__()

    @property
    def toplevel(self) -> tk.Toplevel | Tk:
        return self._top_level

    def close(self) -> bool:
        self._master.after(0, self._master.destroy)
        self._top_level.after(0, self._top_level.destroy)

        return True

    @staticmethod
    def log(ldp: STD.LogDataPacket) -> None:
        global _admin_tools_logger
        _admin_tools_logger.write(ldp)

    def run(self) -> None:
        global _admin_tools_logger

        self.toplevel.geometry('%dx%d+%d+%d' % (
            self.window_size[0], self.window_size[1], self.window_pos[0], self.window_pos[1]
        ))

        self.toplevel.title('Quizzing Application 4 | Administrator Tools')
        self.toplevel.iconbitmap(STD.AppInfo.File.AdminToolsAppICO)

        # Setup padding
        self.pad_x = 20 if 20 < self.window_size[0] / 20 else 0  # PadX = 20 if 20 < 5% of the window width, else 0
        self.pad_y = 10 if 10 < self.window_size[1] / 20 else 0  # PadX = 10 if 10 < 5% of the window height, else 0

        # Set VLE_ENABLED
        self.VLE_ENABLED = not _admin_tools_logger.DISABLE_VLE

        # Create update requests
        self._crt_updt_req_frame(self._top_level)  # Create an update req for _top_level

        # Set the current frame to be the selection frame.
        self.set_frame(FrameID.SELECTION_FRAME)

        self.update_ui()

        self.toplevel.bind(
            '<Configure>',
            self._on_win_conf
        )

    def _on_win_conf(self, *_) -> None:
        ws = [
            self.toplevel.winfo_width(),
            self.toplevel.winfo_height()
        ]

        if ws != self.window_size:
            self.window_size = ws
            self.update_ui(_wraplength_events_only=True)

    # Setting up frames
    def set_frame(self, frame: FrameID):
        assert frame in (FrameID.SELECTION_FRAME, FrameID.SCORE_MNG_FRAME, FrameID.CONFIGURE_FRAME), 'Unsupported frame'

        self.disable_all_inputs()

        self.selection_frame.pack_forget()
        self.configure_frame.pack_forget()
        self.score_mng_frame.pack_forget()

        {
            FrameID.SELECTION_FRAME: self._set_frame_sel,
            FrameID.CONFIGURE_FRAME: self._set_frame_con,
            FrameID.SCORE_MNG_FRAME: self._set_frame_scr
        }[frame]()

        self.enable_all_inputs()

    #       Database Selection Frame

    def _set_frame_sel(self) -> None:
        # Configure the placement of elements
        self.selection_frame.pack(fill=tk.BOTH, expand=True)

        if not self._data[FrameID.SELECTION_FRAME]['_upt_req_submitted']:
            self._theme_frame_sel()

            # This is the first time this function has been called; place the elements in the frame.
            self.sel_frame_title.config(text='Administrator Tools')
            self.sel_frame_title.pack(fill=tk.X, expand=True, padx=self.pad_x, pady=self.pad_y)

        self._data[FrameID.SELECTION_FRAME]['_upt_req_submitted'] = True

    def _theme_frame_sel(self) -> None:
        # Submit theme update requests for the selection frame
        self._crt_updt_req_frame(self.selection_frame)
        self._crt_updt_req_label(
            self.sel_frame_title,
            fg=uV.ACCENT_COLOR,
            font_size=uV.TITLE_FONT_SIZE,
            font_face=uV.TITLE_FONT_FACE
        )

        # Misc. configuration
        self.update_requests.append(
            [
                self.sel_frame_title,
                [
                     uC.WRAP_LENGTH,
                     [
                         (
                             uC.CUSTOM,
                            lambda e, w, px: w-2*px,
                            'ELMNT', 'WND_W', 'PAD_X'
                         )
                     ],
                ]
             ]
        )

    #       Configuration Management Frame

    def _set_frame_con(self) -> None:
        self.configure_frame.pack(fill=tk.BOTH, expand=True)

        if not self._data[FrameID.CONFIGURE_FRAME]['_upt_req_submitted']:
            self._theme_frame_con()

        self._data[FrameID.CONFIGURE_FRAME]['_upt_req_submitted'] = True

    def _theme_frame_con(self) -> None:
        pass

    #       Score Management Frame

    def _set_frame_scr(self) -> None:
        self.score_mng_frame.pack(fill=tk.BOTH, expand=True)

        if not self._data[FrameID.SCORE_MNG_FRAME]['_upt_req_submitted']:
            self._theme_frame_scr()

        self._data[FrameID.SCORE_MNG_FRAME]['_upt_req_submitted'] = True

    def _theme_frame_scr(self) -> None:
        pass

    # Input management
    def enable_all_inputs(self, *exclude_inputs: Union[tk.Button | tk.Radiobutton | tk.Entry | tk.Text]) -> None:
        for inp in self.inputs:
            if inp not in exclude_inputs:
                try:
                    inp.config(state=tk.NORMAL)
                except Exception as E:
                    self.log(
                        STD.LogDataPacket('AdminToolsUI', STD.LoggingLevel.L_ERROR, f'Failed to enable input {inp}')
                    )

    def disable_all_inputs(self, *exclude_inputs: Union[tk.Button | tk.Radiobutton | tk.Entry | tk.Text]) -> None:
        for inp in self.inputs:
            if inp not in exclude_inputs:
                try:
                    inp.config(state=tk.DISABLED)
                except Exception as E:
                    self.log(
                        STD.LogDataPacket('AdminToolsUI', STD.LoggingLevel.L_ERROR, f'Failed to disable input {inp}')
                    )


ModuleScript = STD.AppPolicy.PolicyManager.Module('AdminTools', 'qa_admin_tools.py')


def RunApp(app_instance: object, master: tk.Tk, logger: STD.Logger) -> _UI:
    global _admin_tools_logger

    _admin_tools_logger = logger
    return _UI(app_instance, master)


if __name__ == "__main__":
    ModuleScript.run_as_main()
