import tkinter as tk
from threading import Thread
from overloading import overload


class UI_OBJECT(Thread):
    def __init__(self) -> None:
        super(UI_OBJECT, self).__init__()
        self.start()

    @property
    def toplevel(self) -> tk.Toplevel:
        raise Exception('Property behaviour not yet defined.')

    @property
    def ready_to_close(self) -> bool:
        return True

    def close(self) -> bool:
        raise Exception('Function behaviour not yet defined.')
