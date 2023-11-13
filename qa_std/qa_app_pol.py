"""
FILE:           qa_std/qa_app_pol.py
AUTHOR:         Geetansh Gautam
PROJECT:        Quizzing Application, version 4

DOC

    Quizzing application policy definition.

DEFINES

    Type            Name                            Input                   Output          Alias
    ---------------------------------------------------------------------------------------------
    (class)         FailureToComplyWithPolicy*      (float, str, str)       None
    (class)         PolicyManager                                                           PM
    (class)         PM.Module                       (str, str)              None            MOD
    (method)        MOD.run_as_main                 None                    None

*ExceptionClass

DEPENDENCIES

"""


class FailureToComplyWithPolicy(Exception):
    def __init__(self, policy_id: float, policy_name: str, error_str: str) -> None:
        self.pol_id, self.pol_name, self.error = policy_id, policy_name, error_str

    def __str__(self) -> str:
        return f'Script failed to comply with the application policy. PID: {self.pol_id}. PNAME: {self.pol_name}\n' + \
                f'Error description: {self.error}'


# ----------------------- File IO Settings -----------------------
# POLICY_MAX_IO_EVENTS_PER_MINUTE
#   Specifies the maximum number of IO events that can be allowed in any given one-minute period
#   Failure to comply with this policy should result in the invocation of a IOError exception
#
# Default: 1000
#
POLICY_MAX_IO_EVENTS_PER_MINUTE = 1000
#
# POLICY_FIO_SW_COMPRESS_SRC_FILE
#   Specifies whether the secure write function should compress source files (if secure write mode is enabled)
#
# Default: True (compress source files)
#
POLICY_FIO_SW_COMPRESS_SRC_FILE = True
#
# POLICY_SW_GZIP_COMPRESSION_LEVEL
#   Specifies the level of compression performed by GZIP.COMPRESS and/or ZLIB.COMPRESS in SW functions.
#
# Default: 7
#
POLICY_SW_GZIP_COMPRESSION_LEVEL = 7

# ----------------------- Section Complete -----------------------

# ----------------------- Global Settings ------------------------
# POLICY_MAX_WHILE_LOOP_RETRIES
#   Specifies the maximum number of times that a loop can be run (specifically a while loop).
#
# Default: 10_000
#
POLICY_MAX_WHILE_LOOP_RETRIES = 10_000
#
# POLICY_FO_GEN_THEME_FILE_VERSION
#   Specifies the version of theme files that is to be generated
#
# Default: 1
#
POLICY_FO_GEN_THEME_FILE_VERSION = 1
#
# ----------------------- Section Complete -----------------------


class PolicyManager:
    class Module:
        def __init__(self, module_name: str, module_script_name: str) -> None:
            self.mn, self.msn = module_name, module_script_name
            self._pol_root_n = 1
            self._pol_id_map = {
                'MRAMS': 0
            }

        def run_as_main(self) -> None:
            policy_name = 'MRAMS'
            policy_exclusions = ['qa_main.py']
            policy_id = self._pol_id_map[policy_name] / (10 * (len(self._pol_id_map) // 10 + 1)) + self._pol_root_n

            if self.msn not in policy_exclusions:
                raise FailureToComplyWithPolicy(
                    policy_id,
                    policy_name,
                    f'The module "{self.mn}" cannot be run as a standalone script.'
                )

