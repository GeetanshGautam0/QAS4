# Quizzing Application v4

Quizzing app v4 is an open source, Python-based application centered around the task of creating and hosting quizzes/trivia, with a variety of features. 

![Automated Tests](https://github.com/GeetanshGautam0/QAS4/actions/workflows/tests.yml/badge.svg)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)

# Changelog

# Running the Application

```shell
# Run diagnostics and quit immediately
python qa_main.py start-app _RDQ --lapp

# Run Quizzing App | Admin Tools
python qa_main.py start-app admin_tools --lapp

# Run Quizzing App | Quizzing Form
python qa_main.py start-app quizzing_app --lapp

# Run Quizzing App Utilities (theme and diagnostics)
python qa_main.pt start-app util --lapp
```

The `--lapp` flag must be added to enable the app to boot. This is done to avoid a bug in
the test and diagnostics system.

## Enabling/Disabling Verbose Logging
_In `.conf\configuration.json`_:

```JSON
{
  "settings": {
    "LOG_VERB": true
  }
}
```

or,

```JSON
{
  "settings": {
    "LOG_VERB": false
  }
}
```

_If the above is set to `true`_, VL can **_temporarily_** be disabled by adding the flag `--disable_VLE` to the command.

```shell
python qa_main.py [COMMAND] --disable_VLE
```


---
__NOTE__: Window resize events cause `update_ui` to be called. If verbose logging is enabled, this can lead to the 
application lagging as the window is resized.

It is highly recommended to explicitly add this flag unless you're debugging the application.

## Other App Settings (Only Configurable in Development)
```python
# qa_std/qa_app_pol.py

# ----------------------- File IO Settings -----------------------
# POLICY_MAX_IO_EVENTS_PER_MINUTE
#   Specifies the maximum number of IO events that can be allowed in any given one-minute period
#   Failure to comply with this policy should result in the invocation of a IOError exception
#
# Default: 1000
#
POLICY_MAX_IO_EVENTS_PER_MINUTE = 15_000
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
POLICY_MAX_WHILE_LOOP_RETRIES = 100_000
#
# POLICY_FO_GEN_THEME_FILE_VERSION
#   Specifies the version of theme files that is to be generated
#
# Default: 1
#
POLICY_FO_GEN_THEME_FILE_VERSION = 1
#
#
# POLICY_CWRT_ENABLE_STDOUT
#   Specifies whether the ConsoleWriter.STDOUT function is allowed to print messages to console.
#
#   NOTE: IF SET TO FALSE, LOG MESSAGES WILL NOT APPEAR IN CONSOLE BUT WILL STILL BE SAVED TO THE LOG FILE.
#
# Default: True
POLICY_CWRT_ENABLE_STDOUT = True
# ----------------------- Section Complete -----------------------
```

# Links
* [Developer's Website](https://geetansh.ca)
* [Bug Report Link](https://geetansh.ca/quizzing-app-v4-bug-report/)
* [Official GitHub Page](https://github.com/GeetanshGautam0/QAS4)
