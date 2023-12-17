# Quizzing Application v4

Quizzing app v4 is an open source, Python-based application centered around the task of creating and hosting quizzes/trivia, with a variety of features. 

# Changelog

# Running the Application

```shell
# Run diagnostics and quit immediately
python qa_main.py start-app _RDQ

# Run Quizzing App | Admin Tools
python qa_main.py start-app admin_tools

# Run Quizzing App | Quizzing Form
python qa_main.py start-app quizzing_app

# Run Quizzing App Utilities (theme and diagnostics)
python qa_main.pt start-app util
```

## Enabling/Disabling Verbose Logging
_In `.conf\configuration.json`_:

```JSON
{
  ...
  "settings": {
    ...
    "LOG_VERB": true OR false
  }
}
```

Alternatively, _if the above is set to `true`_, VL can temporarily be disabled by adding the flag `--disable_VLE` to the command.

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
# ----------------------- Section Complete -----------------------
```

# Links
* [Developer's Website](https://geetansh.ca)
* [Bug Report Link](https://geetansh.ca/quizzing-app-v4-bug-report/)
* [Official GitHub Page](https://github.com/GeetanshGautam0/QAS4)
