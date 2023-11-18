"""
FILE:           qa_std/qa_logger.py
AUTHOR:         Geetansh Gautam
PROJECT:        Quizzing Application, version 4

DOC

    Quizzing Application Logger

    Is an addon for ConsoleWriter that allows for saving logs to files. 
    Invokes the console writer as appropriate.

DEFINES

    Type                        Name                    [Inputs]                    [Outputs]                   [alias]
    -------------------------------------------------------------------------------------------------------------------
    Enum                        LoggingLevel                                                                    LL
    dataclass                   LogDataPacket                                                                   LDP

DEPENDENCIES

    ConsoleWriter
    AppPolicy
    AppInfo
    enum.Enum
    dataclasses.dataclass
    threading.Thread
    os
    qa_file_io 
    .qa_def
    .qa_dtc
    typing

LOGGING LEVELS
    L_ERROR 
    L_WARNING
    L_GENERAL
    L_SUCCESS
    L_EMPHASIS

"""

from distutils.log import Log
import qa_file_io as FileIO
from . import qa_app_pol as AppPolicy
from . import qa_app_info as AppInfo
from . import qa_console_write as ConsoleWriter
from . import qa_def
from . import qa_dtc

import os, datetime
from typing import Callable, Any
from enum import Enum
from dataclasses import dataclass
from threading import Thread


class LoggingLevel(Enum):
    (
        L_ERROR,
        L_WARNING,
        L_GENERAL,
        L_EMPHASIS,
        L_SUCCESS
    ) = range(5)


@dataclass
class LogDataPacket:
    script: str
    logging_level: LoggingLevel
    data: Any


class Logger(Thread):
    def __init__(self) -> None:
        self.thread = Thread
        self.thread.__init__(self, name="LoggerThread")
        
        # Define the following symbols but do not initialize them. 
        self._lfile: qa_def.File
        self._stime: datetime.datetime
        self._ready = False
        
        # The function to write to the file
        self.write_to_file: Callable[..., Any]
        
        self._on_init()
        
    def _on_init(self) -> None:
        # Make sure that the logger dir is available
        if not os.path.isdir(AppInfo.Storage.LoggerDir):
            os.makedirs(AppInfo.Storage.LoggerDir)
        
        self._stime = datetime.datetime.now()
        self._lfile = qa_def.File(f'{AppInfo.Storage.LoggerDir}\\QuizzingAppLog {self._stime.strftime("%b %d %Y - %H %M %S")}.qLog')
        
        FileIO.file_io_manager.write(
            self._lfile, 
            f'This log was generated {self._stime.strftime("on %b %d %Y at %H:%M:%S")}',
            secure_mode=False
        )
        
        self.write_to_file = lambda data_to_write: \
            FileIO.file_io_manager.write(
                self._lfile,
                data_to_write,
                secure_mode=False,
                append_mode=True,
                offload_to_new_thread=False,
                append_delim='\n'
            )
        
        self._ready = True
        
        self._dump_logger_info_()
        
    def _dump_logger_info_(self) -> None:
        self.write(LogDataPacket('Logger', LoggingLevel.L_GENERAL,  'New logger instance created.'))
        self.write(LogDataPacket('Logger', LoggingLevel.L_GENERAL,  f'    * Log file: {self._lfile.file_name}'))
        self.write(LogDataPacket('Logger', LoggingLevel.L_GENERAL,  f'    THE FOLLOWING LOGGING LEVELS ARE AVAILABLE:'))
        self.write(LogDataPacket('Logger', LoggingLevel.L_ERROR,    f'      Error logging available.'))
        self.write(LogDataPacket('Logger', LoggingLevel.L_WARNING,  f'      Warning logging available.'))
        self.write(LogDataPacket('Logger', LoggingLevel.L_SUCCESS,  f'      Success message logging available.'))
        self.write(LogDataPacket('Logger', LoggingLevel.L_EMPHASIS, f'      Important message logging available.'))
        self.write(LogDataPacket('Logger', LoggingLevel.L_GENERAL,  f'      General message logging available.'))
        
        self.add_empty_line()
    
    def add_empty_line(self) -> None:
        ConsoleWriter.stdout('\n')
        self.write_to_file('\n')
    
    def write(self, ldp: LogDataPacket) -> None:
        assert self._ready
        assert isinstance(ldp.script, str)
        
        # Convert the script name to bytes; make sure to use the same CFA as the file IO manager
        script_b = qa_dtc.convert(bytes, ldp.script, cfa=FileIO.file_io_manager.cfa)
        
        # Convert the data to bytes; make sure to use the same CFA as the file IO manager
        data_b = qa_dtc.convert(bytes, ldp.data, cfa=FileIO.file_io_manager.cfa)
        
        # Convert the logging level to bytes; make sure to use the same CFA as the file IO manager
        
        # Add a label. Then, theme the message and store it to a log file.
        match ldp.logging_level:
            case LoggingLevel.L_ERROR:
                ANSI_CODES = [qa_def.ANSI.FG_BRIGHT_RED, qa_def.ANSI.BOLD, qa_def.ANSI.RESET, True]
            
            case LoggingLevel.L_EMPHASIS:
                ANSI_CODES = [qa_def.ANSI.FG_BRIGHT_CYAN, qa_def.ANSI.BOLD, qa_def.ANSI.RESET, False]
            
            case LoggingLevel.L_GENERAL:
                ANSI_CODES = [qa_def.ANSI.RESET, qa_def.ANSI.BOLD, qa_def.ANSI.RESET, False]
            
            case LoggingLevel.L_SUCCESS:
                ANSI_CODES = [qa_def.ANSI.FG_BRIGHT_GREEN, qa_def.ANSI.BOLD, qa_def.ANSI.RESET, True]
            
            case LoggingLevel.L_WARNING:
                ANSI_CODES = [qa_def.ANSI.FG_BRIGHT_YELLOW, qa_def.ANSI.BOLD, qa_def.ANSI.RESET, True]
            
            case _:
                raise Exception('Unexpected logging level')
            
        logging_name_b = qa_dtc.convert(
            bytes,
            {
                LoggingLevel.L_ERROR:       'ERROR',
                LoggingLevel.L_WARNING:     'WARNING',
                LoggingLevel.L_GENERAL:     'GENERAL',
                LoggingLevel.L_SUCCESS:     'SUCCESS',
                LoggingLevel.L_EMPHASIS:    'IMPORTANT',
            }[ldp.logging_level],
            cfa=FileIO.file_io_manager.cfa
        )
        
        if (12 - len(logging_name_b)) > 0:
            spaces_b = qa_dtc.convert(bytes, ' ', cfa=FileIO.file_io_manager.cfa) * (12 - len(logging_name_b))
        else:
            spaces_b = qa_dtc.convert(bytes, '', cfa=FileIO.file_io_manager.cfa)
        
        # Get the current time and store it as bytes
        time_b = qa_dtc.convert(bytes, datetime.datetime.now().strftime("ON %b %d %Y AT %H:%M:%S"), cfa=FileIO.file_io_manager.cfa)

        # Append the bytes to form the final bytearray.
        # Pass a version of the bytes (without the logging level) to the ConsoleWriter (to an appropriate function) 
        
        data = b'[%b %b] ' % (script_b, time_b)
        
        if (50 - len(data)) > 0:
            data += qa_dtc.convert(bytes, ' ', cfa=FileIO.file_io_manager.cfa) * (50 - len(data))
        
        data = b'%b %b' % (data, data_b)
        
        {
            LoggingLevel.L_ERROR:       ConsoleWriter.Write.error,
            LoggingLevel.L_WARNING:     ConsoleWriter.Write.warn,
            LoggingLevel.L_GENERAL:     ConsoleWriter.Write.write,
            LoggingLevel.L_SUCCESS:     ConsoleWriter.Write.ok,
            LoggingLevel.L_EMPHASIS:    ConsoleWriter.Write.emphasis,
        }[ldp.logging_level]('[LOGGED]', data)
        
        ANSI_CODES_b = [qa_dtc.convert(bytes, ac, cfa=FileIO.file_io_manager.cfa) for ac in ANSI_CODES[:3]]
        prepend_b = b'[%b%b%b%b]%b' % (ANSI_CODES_b[1], ANSI_CODES_b[0], logging_name_b, ANSI_CODES_b[2], spaces_b)
        
        output_b = b'%b%b %b%b' % (
            prepend_b, 
            ANSI_CODES_b[0] if ANSI_CODES[-1] else ANSI_CODES_b[2],
            data,
            ANSI_CODES_b[-1]
        )
        
        self.write_to_file(output_b)
        
    def __del__(self) -> None:
        try:
            self.thread.join(self, 0)
        except Exception as E:
            pass
    

ModulePolicy = AppPolicy.PolicyManager.Module('Logger', 'qa_logger.py')


if __name__ == "__main__":
    ModulePolicy.run_as_main()

