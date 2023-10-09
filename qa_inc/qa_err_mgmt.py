"""
FILE:           qa_inc/qa_err_mgmt.py
AUTHOR:         Geetansh Gautam
PROJECT:        Quizzing Application, version 4

DOC

    Quizzing application error management.

DEFINES

    (class)     enum            ErrorType
    (class)     dataclass       ErrorStruct
    (method)    None            ErrorStruct.setup()

DEPENDENCIES

    sys
    traceback
    dataclasses.dataclass   [alias: dataclass]
    enum.Enum               [alias: Enum]
    typing.Any              [alias: Any]
    typing.cast             [alias: cast]

"""

import sys, traceback
from dataclasses import dataclass
from enum import Enum
from typing import cast, Any


class ErrorType(Enum):
    """
    ErrorType (Enum).
    Defines various error types used by the error management system.

    Defined error types:
        * UnspecifiedError  (0)  *def   The default error code. No information specified.
        * SystemErrorA      (1)         For errors that are caused by a quizzing application script
        * SystemErrorB      (2)         For errors that are caused by a user interaction with a quizzing app script
        * SystemErrorP      (3)         For errors that are caused by a non-qa-script-related error.
                                            (usually the result of an error raised by a non-qa import).
        * FileIOError       (4)         For errors raised during any file IO operations
                                            (not covered by System Errors A, B, and P).
    """

    UnspecifiedError = 0
    SystemErrorA = 1
    SystemErrorB = 2
    SystemErrorP = 3
    FileIOError = 4


@dataclass
class ErrorStruct:
    """
    ErrorStruct (Data Class)
    Struct used by all functions in the quizzing app error management system chain.

    Revision A1:
        (ErrorType)     :argument type:         The type of error
        (Any)           :argument data:         The information about the error.
        (bool)          :argument fatal:        Is the error fatal? default = False

        THE FOLLOWING VARIABLES ARE NOT INPUTS. ANY DATA STORED IN THEM WILL BE OVER-WRITTEN
        (str)           string                          The information about the error, as a string.

    """

    # Rev. A1 arguments start here
    type: ErrorType
    data: Any
    fatal: bool = False

    # Rev. A1 auto-gen variables
    string: str = cast(str, None)

    def setup(self) -> None:
        print(self.type)
