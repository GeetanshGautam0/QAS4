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

import qa_std as STD
import qa_file_io as FileIO
from .qa_ui_def import UI_OBJECT


class _UI(UI_OBJECT):
    def __init__(self, AI: object, master: tk.Tk) -> None:
        self._master: tk.Tk = master
        self._top_level = tk.Toplevel(self._master)
        self._ai = AI

        self.screen_size = (self._master.winfo_screenwidth(), self._master.winfo_screenheight())
        ws_rat = 4/3

        self.window_size = [self.screen_size[0] // 1.5]
        self.window_size.append(self.window_size[0] // ws_rat)
        self.window_pos = [
            self.screen_size[0] // 2 - self.window_size[0] // 2,
            self.screen_size[1] // 2 - self.window_size[1] // 30 * 17
        ]

        super(_UI, self).__init__()

    def __del__(self) -> None:
        self.join(0)

    @property
    def toplevel(self) -> tk.Toplevel:
        return self._top_level

    def close(self) -> bool:
        self._master.after(0, self._master.quit)
        self._top_level.after(0, self._top_level.quit)

        self.join(0)
        return True

    def run(self) -> None:
        self.toplevel.geometry('%dx%d+%d+%d' % (
            self.window_size[0], self.window_size[1], self.window_pos[0], self.window_pos[1]
        ))

        self.toplevel.title('Quizzing Application 3 | Administrator Tools')


ModuleScript = STD.AppPolicy.PolicyManager.Module('AdminTools', 'qa_admin_tools.py')


def RunApp(AppInstance: object, master: tk.Tk) -> _UI:
    return _UI(AppInstance, master)


if __name__ == "__main__":
    ModuleScript.run_as_main()
