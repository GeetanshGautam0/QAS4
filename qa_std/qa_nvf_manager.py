"""
FILE:           qa_std/qa_nvf_manager.py
AUTHOR:         Geetansh Gautam
PROJECT:        Quizzing Application, version 4

DOC

    Quizzing application non-volatile flag manager

DEFINES

    Type                Name                    [Inputs]                        [Output]                    [alias]
    ---------------------------------------------------------------------------------------------------------------

DEPENDENCIES

    os   (path.isfile)
    zlib (crc32)
    qa_app_info

"""

import zlib, os
from . import qa_app_info


class NVF:
    extension = 'qNVF'

    @staticmethod
    def create_flag(flag_name: str) -> int:
        if not os.path.isdir(f'{qa_app_info.Storage.NonvolatileFlagDir}'):
            os.makedirs(f'{qa_app_info.Storage.NonvolatileFlagDir}')

        file = f'{qa_app_info.Storage.NonvolatileFlagDir}\\{flag_name}.{NVF.extension}'

        if os.path.exists(file):
            with open(file, 'r') as f_in:
                r = f_in.read()
                count = int(r.split('-')[0].strip())
                f_in.close()

            count += 1

        else:
            count = 1

        out_str_raw = f'{count}{flag_name}'
        out_str = f'{count}-{zlib.crc32(out_str_raw.encode())}'

        with open(file, 'w') as f_out:
            f_out.write(out_str)
            f_out.close()

        return count

    @staticmethod
    def check_flag(flag_name: str) -> int:
        file = f'{qa_app_info.Storage.NonvolatileFlagDir}\\{flag_name}.{NVF.extension}'
        if not os.path.isfile(file):
            return 0

        else:
            with open(file, 'r') as f_in:
                r = f_in.read()
                c = int(r.split('-')[0])
                f_in.close()

            return c

    @staticmethod
    def remove_flag(flag_name: str, remove_all: bool = True) -> int:
        file = f'{qa_app_info.Storage.NonvolatileFlagDir}\\{flag_name}.{NVF.extension}'

        n = NVF.check_flag(flag_name)
        if not n:
            return 0

        if remove_all:
            os.remove(file)
            return 0

        out_str_raw = f'{n - 1}{flag_name}'
        out_str = f'{n - 1}-{zlib.crc32(out_str_raw.encode())}'

        with open(file, 'w') as f_out:
            f_out.write(out_str)
            f_out.close()

        assert NVF.check_flag(flag_name) == (n - 1)

        return n - 1
