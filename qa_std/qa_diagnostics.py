"""
FILE:           qa_std/qa_diagnostics.py
AUTHOR:         Geetansh Gautam
PROJECT:        Quizzing Application, version 4

DOC

    Quizzing application diagnostics.
    * Used by unit testing 
    * Used by APP:DIAGNOSTICS_AND_MAINTENANCE_UTILITY

DEFINES


DEPENDENCIES

    AppPolicy

"""

from . import locale as M_locale
from . import qa_def as M_qa_def
from . import qa_dtc as M_qa_dtc
from . import qa_app_info as M_qa_app_info

from . import qa_logger as Logger
from . import qa_app_pol as AppPolicy

from typing import Callable, Any, Type


_global_logger: Logger.Logger
ModulePolicy = AppPolicy.PolicyManager.Module('Diagnostics', 'qa_diagnostics.py')


def _raises(
        exception: Type[BaseException],
        function: Callable[[Any], Any],
        *args: Any,
        **kwargs: Any
) -> None:
    try:
        function(*args, **kwargs)
    except exception as _:
        pass
    except:
        raise Exception
    else:
        raise Exception



class ModDiagnostics:
    # 0xF001:0xXXXX

    # Locale module (diagnostic code: 0xF001:0x0000)
    @staticmethod
    def locale() -> bool:
        global _global_logger
        diagnostic_code = '0xF001:0x0000'

        try:
            M_locale.get_locale()

        except Exception as E:
            _global_logger.write(
                Logger.LogDataPacket(
                    'Diagnostics', Logger.LoggingLevel.L_ERROR,
                    f'DIAG <{diagnostic_code}> "A.CONF:LOCALE" FAILED: {E}'
                )
            )
            return False

        else:
            _global_logger.write(
                Logger.LogDataPacket(
                    'Diagnostics', Logger.LoggingLevel.L_SUCCESS,
                    f'DIAG <{diagnostic_code}> "A.CONF:LOCALE" PASS'
                )
            )
            return True

    # QA DEF module
    #   HexColor            diagnostic code: 0xF001:0x0001
    #   ConvertColor        diagnostic code: 0xF001:0x0002
    #   File                diagnostic code: 0xF001:0x0003
    @staticmethod
    def qa_def() -> bool:
        global _global_logger

        # HexColor
        hc_diagnostic_code = '0xF001:0x0001'

        try:
            M_qa_def.HexColor('#ffffff')                                # Should not raise an error
            M_qa_def.HexColor('#fff')                                   # Should not raise an error
            _raises(AssertionError, M_qa_def.HexColor, 'ffffff')  # Should raise an AssertionError
            _raises(AssertionError, M_qa_def.HexColor, '#ffff')   # Should raise an AssertionError
            _raises(AssertionError, M_qa_def.HexColor, '#ffffgg') # Should raise an AssertionError

        except Exception as E:
            _global_logger.write(
                Logger.LogDataPacket(
                    'Diagnostics', Logger.LoggingLevel.L_ERROR,
                    f'DIAG <{hc_diagnostic_code}> "QA_DEF:HEX_COLOR" FAILED: {E}'
                )
            )
            return False
        else:
            _global_logger.write(
                Logger.LogDataPacket(
                    'Diagnostics', Logger.LoggingLevel.L_SUCCESS,
                    f'DIAG <{hc_diagnostic_code}> "QA_DEF:HEX_COLOR" PASS'
                )
            )

        # Convert Color
        cc_diagnostic_code = '0xF001:0x0002'

        try:
            hex_color = M_qa_def.HexColor('#1f1f1f')
            c_rgb = M_qa_def.ConvertColor.HexToRGB(hex_color.color)
            c_hex = M_qa_def.ConvertColor.RGBToHex(c_rgb)

            assert c_hex.upper() == hex_color.color, 'Hex --> RGB --> Hex'

        except Exception as E:
            _global_logger.write(
                Logger.LogDataPacket(
                    'Diagnostics', Logger.LoggingLevel.L_ERROR,
                    f'DIAG <{cc_diagnostic_code}> "QA_DEF:COLOR_CONV" FAILED: {E}'
                )
            )
            return False
        else:
            _global_logger.write(
                Logger.LogDataPacket(
                    'Diagnostics', Logger.LoggingLevel.L_SUCCESS,
                    f'DIAG <{cc_diagnostic_code}> "QA_DEF:COLOR_CONV" PASS'
                )
            )

        # File
        f_diagnostic_code = '0xF001:0x0003'

        try:
            file = M_qa_def.File('.\\src/test.txt')

            assert file.file_path == '.\\src\\test.txt', 'File.file_path'
            assert file.path == '.\\src', 'File.path'
            assert file.file_name == 'test.txt', 'File.file_name'

            _raises(AssertionError, M_qa_def.File, 123)

        except Exception as E:
            _global_logger.write(
                Logger.LogDataPacket(
                    'Diagnostics', Logger.LoggingLevel.L_ERROR,
                    f'DIAG <{f_diagnostic_code}> "QA_DEF:FILE" FAILED: {E}'
                )
            )
            return False
        else:
            _global_logger.write(
                Logger.LogDataPacket(
                    'Diagnostics', Logger.LoggingLevel.L_SUCCESS,
                    f'DIAG <{f_diagnostic_code}> "QA_DEF:FILE" PASS'
                )
            )

        return True

    # ----
    # QA_DTC Test data
    _qa_dtc_test_str = '`1234567890-=~!@#$%^&*()_+QWERTYUIOP{}|qwertyuiop[]asdfghjkl;ASDFGHJKL:"zxcvbnm,./ZXCVBNM<>?'
    _qa_dtc_test_bytes = b'`1234567890-=~!@#$%^&*()_+QWERTYUIOP{}|qwertyuiop[]asdfghjkl;ASDFGHJKL:"zxcvbnm,./ZXCVBNM<>?'
    _qa_dtc_test_int = 234782384723
    _qa_dtc_test_float = 123123.123124
    _qa_dtc_test_tuple = (
        'Hello, World!',
        [_qa_dtc_test_bytes],
        {_qa_dtc_test_str},
        (_qa_dtc_test_float, _qa_dtc_test_int),
        {_qa_dtc_test_int: _qa_dtc_test_float, complex(12, 56): True}
    )
    _qa_dtc_test_list = [*_qa_dtc_test_tuple]
    _qa_dtc_test_set = {15, 1293, 1831, 12930}
    _qa_dtc_test_complex = complex(12, 56)
    _qa_dtc_test_bool = True
    _qa_dtc_test_dict = {'Hello, World!': _qa_dtc_test_list}

    _qa_dtc_test_cfa = M_qa_dtc.CFA(';', '-', ':', False)

    @staticmethod
    def _qa_dtc_sr1_(
            diagnostic_code: str,
            expected: Any,
            actual: Any,
            conversion: str
    ) -> bool:
        try:
            assert expected == actual, conversion

        except Exception as E:
            _global_logger.write(
                Logger.LogDataPacket(
                    'Diagnostics', Logger.LoggingLevel.L_ERROR,
                    f'DIAG <{diagnostic_code}> "{conversion}" FAILED: {E}'
                )
            )
            return False
        else:
            _global_logger.write(
                Logger.LogDataPacket(
                    'Diagnostics', Logger.LoggingLevel.L_SUCCESS,
                    f'DIAG <{diagnostic_code}> "{conversion}" PASS'
                )
            )

        return True

    # QA DTC Module (--> BYTES)
    #   STR     --> BYTES                       0xF001:0x0004
    #   INT     --> BYTES                       0xF001:0x0005
    #   FLOAT   --> BYTES                       0xF001:0x0006
    #   LIST    --> BYTES                       0xF001:0x0007
    #   TUPLE   --> BYTES                       0xF001:0x0008
    #   COMPLEX --> BYTES                       0xF001:0x0009
    #   BOOL    --> BYTES                       0xF001:0x000A
    #   SET     --> BYTES                       0xF001:0x000B
    #   DICT    --> BYTES                       0xF001:0x000C
    @staticmethod
    def _qa_dtc_to_bytes() -> bool:
        from_str = M_qa_dtc.convert(bytes, ModDiagnostics._qa_dtc_test_str, cfa=ModDiagnostics._qa_dtc_test_cfa)
        from_int = M_qa_dtc.convert(bytes, ModDiagnostics._qa_dtc_test_int, cfa=ModDiagnostics._qa_dtc_test_cfa)
        from_float = M_qa_dtc.convert(bytes, ModDiagnostics._qa_dtc_test_float, cfa=ModDiagnostics._qa_dtc_test_cfa)
        from_list = M_qa_dtc.convert(bytes, ModDiagnostics._qa_dtc_test_list, cfa=ModDiagnostics._qa_dtc_test_cfa)
        from_tuple = M_qa_dtc.convert(bytes, ModDiagnostics._qa_dtc_test_tuple, cfa=ModDiagnostics._qa_dtc_test_cfa)
        from_complex = M_qa_dtc.convert(bytes, ModDiagnostics._qa_dtc_test_complex, cfa=ModDiagnostics._qa_dtc_test_cfa)
        from_bool = M_qa_dtc.convert(bytes, ModDiagnostics._qa_dtc_test_bool, cfa=ModDiagnostics._qa_dtc_test_cfa)
        from_set = M_qa_dtc.convert(bytes, ModDiagnostics._qa_dtc_test_set, cfa=ModDiagnostics._qa_dtc_test_cfa)
        from_dict = M_qa_dtc.convert(bytes, ModDiagnostics._qa_dtc_test_dict, cfa=ModDiagnostics._qa_dtc_test_cfa)

        exp_str = b'`1234567890-=~!@#$%^&*()_+QWERTYUIOP{}|qwertyuiop[]asdfghjkl;ASDFGHJKL:"zxcvbnm,./ZXCVBNM<>?'
        exp_int = b'234782384723'
        exp_float = b'123123.123124'
        exp_list = b'[Hello, World!;[`1234567890-=~!@#$%^&*()_+QWERTYUIOP{}|qwertyuiop[]asdfghjkl;ASDFGHJKL:"zxcvbnm,./ZXCVBNM<>?];{`1234567890-=~!@#$%^&*()_+QWERTYUIOP{}|qwertyuiop[]asdfghjkl;ASDFGHJKL:"zxcvbnm,./ZXCVBNM<>?};(123123.123124;234782384723);{234782384723-123123.123124:(12.0+56.0j)-True}]'
        exp_tuple = b'(Hello, World!;[`1234567890-=~!@#$%^&*()_+QWERTYUIOP{}|qwertyuiop[]asdfghjkl;ASDFGHJKL:"zxcvbnm,./ZXCVBNM<>?];{`1234567890-=~!@#$%^&*()_+QWERTYUIOP{}|qwertyuiop[]asdfghjkl;ASDFGHJKL:"zxcvbnm,./ZXCVBNM<>?};(123123.123124;234782384723);{234782384723-123123.123124:(12.0+56.0j)-True})'
        exp_complex = b'(12.0+56.0j)'
        exp_bool = b'True'
        exp_set = b'{12930;15;1293;1831}'
        exp_dict = b'{Hello, World!-[Hello, World!;[`1234567890-=~!@#$%^&*()_+QWERTYUIOP{}|qwertyuiop[]asdfghjkl;ASDFGHJKL:"zxcvbnm,./ZXCVBNM<>?];{`1234567890-=~!@#$%^&*()_+QWERTYUIOP{}|qwertyuiop[]asdfghjkl;ASDFGHJKL:"zxcvbnm,./ZXCVBNM<>?};(123123.123124;234782384723);{234782384723-123123.123124:(12.0+56.0j)-True}]}'

        return (
            ModDiagnostics._qa_dtc_sr1_('0xF001:0x0004', exp_str, from_str,     'str --> bytes') &
            ModDiagnostics._qa_dtc_sr1_('0xF001:0x0005', exp_int, from_int,     'int --> bytes') &
            ModDiagnostics._qa_dtc_sr1_('0xF001:0x0006', exp_float, from_float, 'float --> bytes') &
            ModDiagnostics._qa_dtc_sr1_('0xF001:0x0007', exp_list, from_list,   'list --> bytes') &
            ModDiagnostics._qa_dtc_sr1_('0xF001:0x0008', exp_tuple, from_tuple, 'tuple --> bytes') &
            ModDiagnostics._qa_dtc_sr1_('0xF001:0x0009', exp_complex, from_complex, 'complex --> bytes') &
            ModDiagnostics._qa_dtc_sr1_('0xF001:0x000A', exp_bool, from_bool, 'bool --> bytes') &
            ModDiagnostics._qa_dtc_sr1_('0xF001:0x000B', exp_set, from_set, 'set --> bytes') &
            ModDiagnostics._qa_dtc_sr1_('0xF001:0x000C', exp_dict, from_dict, 'dict --> bytes')
        )

    @staticmethod
    def qa_dtc() -> bool:
        return ModDiagnostics._qa_dtc_to_bytes()

    # Test 0xF001:0x000D
    #       Check if all source files are present

    @staticmethod
    def check_source_files() -> bool:
        global _global_logger

        if M_qa_app_info.File._check_files():
            _global_logger.write(
                Logger.LogDataPacket(
                    'Diagnostics',
                    Logger.LoggingLevel.L_SUCCESS,
                    'DIAG <0xF001:0x000D> "A.FILE:SRC_FILES" PASS'
                )
            )
            return True

        _global_logger.write(
            Logger.LogDataPacket(
                'Diagnostics',
                Logger.LoggingLevel.L_ERROR,
                'DIAG <0xF001:0x000D> "A.FILE:SRC_FILES" FAIL'
            )
        )
        return False


class GeneralDiagnostics:
    pass


class AppDiagnostics:
    pass


if __name__ == "__main__":
    ModulePolicy.run_as_main()
