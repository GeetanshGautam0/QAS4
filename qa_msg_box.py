"""
FILE:           qa_std/qa_error_manager.py
AUTHOR:         Geetansh Gautam
PROJECT:        Quizzing Application, version 4

DOC

    Quizzing application error manager.

DEFINES

    Type            Name                Input Types              Output Type             Alias
    ---------------------------------------------------------------------------------------


DEPENDENCIES

    tkinter
        messagebox
    enum
    dataclasses
    typing

"""

from tkinter import messagebox
from enum import Enum
from dataclasses import dataclass
from typing import Callable, Tuple, Any


class MessageBoxType(Enum):
    TKINTER = 0
    CUSTOM = 1


class MessageType(Enum):
    ERROR = 0
    WARNING = 1
    SUCCESS = 2
    INFO = 3


@dataclass
class Message:
    msg_t: MessageType
    title: str
    text: str


def show_message(message: Message) -> MessageBoxType:
    fn = ()

    match message.msg_t:

        case MessageType.ERROR:
            fn = (_CMB.error, messagebox.showerror)  # type: ignore

        case MessageType.WARNING:
            fn = (_CMB.warn, messagebox.showwarning)  # type: ignore

        case MessageType.SUCCESS:
            fn = (_CMB.success, messagebox.showinfo)  # type: ignore

        case _:
            fn = (_CMB.info, messagebox.showinfo)  # type: ignore

    try:
        fn[0](message)  # type: ignore
        return MessageBoxType.CUSTOM

    except Exception as _:
        fn[1](message.title, message.text)  # type: ignore
        return MessageBoxType.TKINTER


class _CMB:
    @staticmethod
    def error(*_: Any) -> None:
        raise NotImplementedError

    @staticmethod
    def warn(*_: Any) -> None:
        raise NotImplementedError

    @staticmethod
    def success(*_: Any) -> None:
        raise NotImplementedError

    @staticmethod
    def info(*_: Any) -> None:
        raise NotImplementedError

