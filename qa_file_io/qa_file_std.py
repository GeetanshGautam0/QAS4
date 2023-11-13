"""
FILE:           qa_file_io/qa_file_std.py
AUTHOR:         Geetansh Gautam
PROJECT:        Quizzing Application, version 4

DOC

    Quizzing Application Standard File IO Functions

DEFINES

    Type            Name                    [Inputs]                    [Outputs]                   [aliases]
    ---------------------------------------------------------------------------------------------------------
    Enum            FileType
    Enum            OperationType                                                                   op
    (class)         IOHistory                                                                       IOH
    UNINIT IOH      IOHistoryManager        None                        None
    (class)         FileIO                  *, **                       None                        FIO
    (method)        FIO.write               File, Any, bool, bool       bool                        SW

UNINIT: Uninitiated object.

DEPENDENCIES

    os
    qa_std.qa_nvf_manager
    qa_std.qa_def
    qa_std.qa_dtc
    qa_std.locale
    qa_std.qa_app_info
    qa_std.qa_app_pol
    threading.Timer
    threading.Thread
    enum.Enum
    cryptography.fernet.Fernet
    gzip
    shutil
    zlib

Relevant App Policies
    * POLICY_MAX_IO_EVENTS_PER_MINUTE
    * POLICY_FIO_SW_COMPRESS_SRC_FILE

"""

import os, random, gzip, hashlib, zlib, shutil
from dataclasses import dataclass
from enum import Enum
from threading import Timer, Thread
from typing import Any, List, Tuple, Dict
from qa_std import qa_def, qa_dtc, qa_app_info, qa_app_pol, locale, qa_console_write, qa_nvf_manager
from cryptography.fernet import Fernet


class FileType(Enum):
    SecureWriteBackup = 0
    QuizFile = 1
    AdminFile = 2
    Theme = 3


class BadFileFormat(Exception):
    def __init__(self, file_format: str, error: str) -> None:
        assert file_format in FileType._member_names_, 'Invalid file_format.'
        self.ff = file_format
        self.e = error

    def __str__(self) -> str:
        return f'Improper file format for "{self.ff}". {self.e}'


@dataclass
class HeaderSection:
    SectionName: str

    # SectionStart and SectionLength are both both indices.
    SectionStart: int
    SectionLength: int


class Header:
    MAGIC_BYTES = HeaderSection('MAGIC_BYTES', 0, 4)
    VERSION = HeaderSection('VERSION', 4, 2)

    HEADER_VERSION = HeaderSection('HEADER_VERSION', 6, 2)

    # Used by external functions
    byteorder = 'big'
    items = [MAGIC_BYTES, VERSION, HEADER_VERSION]


@dataclass
class HeaderData:
    MAGIC_BYTES: bytes

    # Version information
    VERSION_BYTES: bytes
    VERSION_INT: int

    # Header version information
    HEADER_VERSION_BYTES: bytes
    HEADER_VERSION_INT: int

    # File Type information
    DETECTED_FILE_TYPE: FileType


@dataclass
class HeaderVersionOne(HeaderData):
    pass


# Each file type, except for SecureWriteBackup files, must have one of the following bytes in their header, which
#   is used to identify the file type.

MagicBytes = {
    b'\x01\xff\x17\x10': FileType.QuizFile,
    b'\x01\xff\x17\x11': FileType.AdminFile,
    b'\x01\xff\x17\x12': FileType.Theme
}


MPV_FIO_923983nfu_MBR = {v: k for k, v in MagicBytes.items()}


def GetMagicBytes(file_type: FileType) -> bytes:
    global MPV_FIO_923983nfu_MBR
    return MPV_FIO_923983nfu_MBR.get(file_type)


class OperationType(Enum):
    READ = 0
    WRITE = 1


class IOHistory:
    def __init__(self) -> None:
        self.after = lambda t, f: Timer(t, f)
        self._buffer: List[Tuple[OperationType, int]] = []
        self.current_task = self.after(10, self._clear_buffer)
        self.current_task.start()

    def _clear_buffer(self) -> None:
        if not qa_nvf_manager.NVF.check_flag('AppRun'):
            raise Exception('App not running.')

        self._buffer = []
        self.current_task = self.after(10, self._clear_buffer)
        self.current_task.start()

    def add_event(self, op_type: OperationType) -> None:
        self._buffer.append(
            (op_type, len(self._buffer) * random.randint(1001, 9999))
        )

        if len(self._buffer) > qa_app_pol.POLICY_MAX_IO_EVENTS_PER_MINUTE / 6:
            raise IOError(f'Too many IO events in one minute (> {qa_app_pol.POLICY_MAX_IO_EVENTS_PER_MINUTE})')

    def __del__(self) -> None:
        self.current_task.cancel()


class FileIO:
    MPV_FIO_710Nd_enK: Dict[FileType, bytes] = {
        FileType.SecureWriteBackup: b'TniX7J7DK67d4kkNl-6NAz4oFX9gOdGZ502N5-LoNMs='
    }

    def __init__(self, IOHistoryManager: IOHistory, *args: Any, **kwargs: Any) -> None:
        """
        FileIO

        Contains functions for:
            1) Writing to files

        Automatically takes care of encryption and decryption.

        :param IOHistoryManager:
        :param args: Misc. args
        :param kwargs: Misc. keyword args
        """

        self.locale: locale.Locale = locale.get_locale()
        self._ar, self._kw = args, kwargs

        self.cfa = qa_dtc.CFA() if not isinstance(self._kw.get('cfa'), qa_dtc.CFA) else self._kw.get('cfa')
        self.iohm = IOHistoryManager

    @staticmethod
    def _write_bytes_to_file_(file: qa_def.File, data: bytes) -> None:
        if len(file.path):
            if not os.path.isdir(file.path):
                os.makedirs(file.path)

        with open(file.file_path, 'wb') as output_file:
            output_file.write(data)
            output_file.close()

    def _create_file_backup_(self, file: qa_def.File, current_bytes: bytes) -> Tuple[qa_def.File, bool]:
        # Take a backup of the file, store it in the appdata folder
        i = 1

        # This loop is compliant with the MAX_WHILE_LOOP_RETRIES policy.
        #   Use i as a counter for how many attempts have been made at file name generation.
        while i < qa_app_pol.POLICY_MAX_WHILE_LOOP_RETRIES:
            # Base file name
            backup_file_name = f'{file.file_name}-{hashlib.md5(current_bytes).hexdigest()}'
            # Salt: random number. Add: extension
            backup_file_name += f'-{str(random.random()).split(".")[-1]}.qSWBackup'
            # Add: directory absolute path.
            backup_file_name = f'{qa_app_info.Storage.SecureWriteBackupDir}\\{backup_file_name}'

            if not os.path.exists(backup_file_name):
                break

            i += 1

        else:
            raise Exception(f'File name generation took too many attempts ({i}).')

        # Encrypt current_bytes using SecureWriteBackup encryption key.
        current_enc_bytes = Fernet(self.MPV_FIO_710Nd_enK[FileType.SecureWriteBackup]).encrypt(current_bytes)

        # Store the backup_file_name as a File object for ease of use (splits dir and file names with regex).
        backup_file = qa_def.File(backup_file_name)

        if not os.path.isdir(backup_file.path):
            # If the destination directory tree does not exist, create it before creating the backup file.
            os.makedirs(backup_file.path)

        # Store the data as encrypted bytes.
        with open(backup_file.file_path, 'wb') as f_out:
            # Optionally: compress the data too
            if qa_app_pol.POLICY_FIO_SW_COMPRESS_SRC_FILE:
                f_out.write(gzip.compress(current_enc_bytes, qa_app_pol.POLICY_SW_GZIP_COMPRESSION_LEVEL))

            else:
                f_out.write(current_enc_bytes)

            f_out.close()

        return backup_file, os.path.isfile(backup_file.file_path)

    @staticmethod
    def _restore_from_backup_(output_file: qa_def.File, backup_file: qa_def.File, crc32: int) -> None:
        # Make sure that the backup file exists, and it is in the right directory
        assert (backup_file.path == qa_app_info.Storage.SecureWriteBackupDir) & os.path.isfile(backup_file.file_path), \
            'Invalid backup file (ERROR 1)'

        qa_console_write.Write.ok('File format accepted.')

        # Copy backup file to output_dir
        shutil.copyfile(backup_file.file_path, f'{output_file.file_path}.swb')

        qa_console_write.Write.ok('Backup file copied to output dir.')

        with open(f'{output_file.file_path}.swb', 'rb') as f_in:
            raw0: bytes = f_in.read()

            if qa_app_pol.POLICY_FIO_SW_COMPRESS_SRC_FILE:
                raw: bytes = gzip.decompress(raw0)

            else:
                raw = raw0

            f_in.close()

        # Read in the bytes, decrypt the bytes.
        d_bytes = Fernet(FileIO.MPV_FIO_710Nd_enK[FileType.SecureWriteBackup]).decrypt(raw)

        qa_console_write.Write.ok('Decrypted backup.')

        # Compute the CRC
        d_crc = zlib.crc32(d_bytes)

        qa_console_write.Write.write(f'CRC32 of original bytes: {crc32}. CRC32 of recovered bytes: {d_crc}')
        if d_crc - crc32:
            qa_console_write.Write.warn(
                'CRC32 checksum of recovered data does not match the original data.',
                'Data was potentially lost.'
            )

        else:
            qa_console_write.Write.ok('Backup validated with CRC32.')

        with open(output_file.file_path, 'wb') as f_out:
            f_out.write(d_bytes)
            f_out.close()

        qa_console_write.Write.write('Wrote backup to file.')

        with open(output_file.file_path, 'rb') as f_in:
            n_hash = hashlib.md5(f_in.read()).hexdigest()
            if n_hash in backup_file.file_name:
                qa_console_write.Write.ok(f'Backup restoration validated ({n_hash}).')
            else:
                qa_console_write.Write.warn(n_hash)

    def write(
            self,
            file: qa_def.File,
            data: Any,
            secure_mode: bool = True,
            append_mode: bool = False,
            offload_to_new_thread: bool = False,
            append_delim: str = '\n'
    ) -> bool:

        """
        FileIO.write
        Aliases:
            * SecureWrite
            * SW

        :param file:            qa_def.File object for output file
        :param data:            Data to write (any type that can be converted to bytes via qa_std.qa_dtc)
        :param secure_mode:     Should secure mode be used (default = True; highly recommended)
        :param append_mode:     Should the data be appended to the file?
        :param offload_to_new_thread: Should the write operation be offloaded to a new thread?
        :param append_delim:    Delimiter used to separated current and new bytes, if append_mode is enabled.
        :raises AssertionError:
        :return:                Success status as a boolean (unless offloaded to a new thread)
        """

        if offload_to_new_thread:
            Thread(target=lambda: self.write(file, data, secure_mode, append_mode, False)).start()
            return True

        # Add a write event to the IO history
        self.iohm.add_event(OperationType.WRITE)

        # Convert data to bytes (taking the locale into account).
        new_bytes = qa_dtc.convert(bytes, data, cfa=self.cfa)

        if os.path.isfile(file.file_path):
            # Read in the current bytes in the file, if it exists (soft handling)
            with open(file.file_path, 'rb') as f_in:
                current_bytes = f_in.read()
                f_in.close()

        else:
            current_bytes = qa_dtc.convert(bytes, '', cfa=self.cfa)

        # Generate a checksum of the current data using the zlib.crc32 command
        cb_crc32, cb_l = zlib.crc32(current_bytes), len(current_bytes)

        if secure_mode and cb_l:
            # If secure_mode is enabled, and there is data in the file, make a backup of the file and store it
            # to the user data directory (AppData in WIN).
            backup_file, backup_made = self._create_file_backup_(file, current_bytes)
            assert backup_made, '[SECURE WRITE] Failed to create file backup'

        if append_mode:
            delim_bytes = qa_dtc.convert(bytes, append_delim, cfa=self.cfa)
            new_bytes = (current_bytes + delim_bytes + new_bytes)

        # Release the memory occupied by the following variable(s).
        del current_bytes

        try:
            # Write the new data to the file.
            FileIO._write_bytes_to_file_(file, new_bytes)

        except PermissionError as PE:
            # If the write fails due to a permission error, then there is noting the app can do to rectify that at this
            #   stage. Furthermore, a restoration attempt is not necessary as any existing data would not have been
            #   overwritten in the first place.
            qa_console_write.Write.error('Failed to write data to output file due to insufficient permission(s).')
            raise PE

        except Exception as E:
            # Log the error in the console as an error (logger not setup as of now).
            # TODO: replace with a log command once logger is implemented.

            qa_console_write.Write.error('Failed to write data to output file: ', str(E))

            if secure_mode and cb_l:
                # If the write process fails, re-create the file using the backup.
                qa_console_write.Write.emphasis('Trying to restore your data using a backup. DO NOT QUIT THE APP.')

                try:
                    FileIO._restore_from_backup_(file, backup_file, cb_crc32)

                except NameError:
                    raise Exception('[FATAL] Did not find backup file object.')

            raise IOError('Failed to write bytes to file.')

        return True
