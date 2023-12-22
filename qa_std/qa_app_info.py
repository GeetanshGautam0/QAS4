"""
FILE:           qa_std/qa_app_info.py
AUTHOR:         Geetansh Gautam
PROJECT:        Quizzing Application, version 4

DOC

    Quizzing Application App Info

DEFINES

    Type                        Name                    [Inputs]                    [Outputs]                   [alias]
    -------------------------------------------------------------------------------------------------------------------
    Enum                            BuildType
    Dataclass                       Configuration
    (class)                         ConfigurationFile                                                           CF
    (method)                        CF.load_file

RAISES

    Error Type                  Error Code              Error Description
    -------------------------------------------------------------------------------------------------------------------
    AssertionError              0x100F:0x0000           Source files (Files) not present.

DEPENDENCIES

    josn
    os
    appdires
    typing
    enum.Enum
    dataclasses.dataclass

"""

import json, os, appdirs
from typing import cast, Tuple
from enum import Enum
from dataclasses import dataclass


class Storage:
    AppDataDir = appdirs.user_data_dir(
        'Quizzing Application',
        'Geetansh Gautam',
        '4.1',
        True
    ).replace('/', '\\')
    SourceDirectory = '.src'

    QAConfigFileExtension = 'qconfig'

    SecureWriteBackupDir = f'{AppDataDir}\\.swb'
    AppSettingsDir = f'{AppDataDir}\\.asd'
    ThemeInstallDir = f'{AppDataDir}\\.tid'
    NonvolatileFlagDir = f'{AppDataDir}\\.nvf'
    LoggerDir = f'{AppDataDir}\\.log'
    
    ThemeDefaultDir = f'{SourceDirectory}\\.theme'
    ConfigurationDefaultDir = f'{SourceDirectory}\\.conf'

    ThemeConfigurationFile = f'{AppSettingsDir}\\qt.{QAConfigFileExtension}'
    QuizConfigurationFile = f'{AppSettingsDir}\\qz.{QAConfigFileExtension}'

    DefaultThemeFile = f'{ThemeDefaultDir}\\default_themes.qTheme'


class BuildType(Enum):
    ALPHA = 0
    BETA = 1
    STABLE = 2


@dataclass
class Configuration:
    AVS: str                            # App version string
    BT: BuildType                       # Build Type
    BI: str                             # Build ID

    locale: Tuple[str, str]             # Locale information
    VLE: bool                           # Verbose logging enabled

    _ver: int = 1


class ConfigurationFile:
    """

    DEFINES:
    * loc       STRING          Configuration file path (relative to working directory)

    :raise AssertionError:      0x0000:0x0001       Configuration file not found (fatal)
    :raise AssertionError:      0x0000:0x0002       Configuration File Format/Data Error 1 (AVS)
    :raise AssertionError:      0x0000:0x0003       Configuration File Format/Data Error 2 (BT)
    :raise AssertionError:      0x0000:0x0004       Configuration File Format/Data Error 3 (BI)
    :raise AssertionError:      0x0000:0x0005       Configuration File Format/Data Error 4 (locale)
    :raise AssertionError:      0x0000:0x0006       Configuration File Format/Data Error 5 (VLE)

    """

    loc: str = '.conf/configuration.json'
    config: Configuration

    @staticmethod
    def load_file() -> None:
        assert os.path.isfile(ConfigurationFile.loc), '0x0000:0x0001'
        with open(ConfigurationFile.loc, 'r') as configuration_file:
            raw = configuration_file.read()
            configuration_file.close()

        configuration_json = json.loads(raw)
        del raw

        ConfigurationFile.config = Configuration(
            configuration_json['build']['AVS'],
            {0: BuildType.ALPHA, 1: BuildType.BETA, 2: BuildType.STABLE}[configuration_json['build']['BT']],
            configuration_json['build']['BI'],
            cast(Tuple[str, str], (*configuration_json['settings']['locale'], )),
            configuration_json['settings']['LOG_VERB']
        )

        assert isinstance(ConfigurationFile.config.AVS, str),           '0x0000:0x0002'
        assert isinstance(ConfigurationFile.config.BT, BuildType),      '0x0000:0x0003'
        assert isinstance(ConfigurationFile.config.BI, str),            '0x0000:0x0004'
        assert isinstance(ConfigurationFile.config.locale, tuple),      '0x0000:0x0005'
        assert isinstance(ConfigurationFile.config.VLE, bool),          '0x0000:0x0006'


ConfigurationFile.load_file()


class File:
    AdminToolsAppICO = f'{Storage.SourceDirectory}\\.ico\\.app_ico\\admn_t.ico'
    QuizzingToolAppICO = f'{Storage.SourceDirectory}\\.ico\\.app_ico\\qz_t.ico'
    UtilitiesAppICO = f'{Storage.SourceDirectory}\\.ico\\.app_ico\\util.ico'
    SetupAppICO = f'{Storage.SourceDirectory}\\.ico\\.app_ico\\setup.ico'
    UpdaterAppICO = f'{Storage.SourceDirectory}\\.ico\\.app_ico\\updater.ico'

    AdminToolsFileICO = f'{Storage.SourceDirectory}\\.ico\\.app_ico\\admn_file.ico'
    LogFileICO = f'{Storage.SourceDirectory}\\.ico\\.app_ico\\log.ico'
    BackupFileICO = f'{Storage.SourceDirectory}\\.ico\\.app_ico\\backup_file.ico'
    QuizFileICO = f'{Storage.SourceDirectory}\\.ico\\.app_ico\\qz_file.ico'
    ScoreFileICO = f'{Storage.SourceDirectory}\\.ico\\.app_ico\\scr_file.ico'

    @staticmethod
    def _check_files() -> bool:
        o = True
        for f in (
            File.AdminToolsFileICO,
            File.QuizzingToolAppICO,
            File.UtilitiesAppICO,
            File.SetupAppICO,
            File.UpdaterAppICO,
            File.AdminToolsAppICO,
            File.LogFileICO,
            File.BackupFileICO,
            File.QuizFileICO,
            File.ScoreFileICO
        ):
            o &= os.path.exists(f)

        return o


assert File._check_files(), '0x100F:0x0000 - Source files not present.'

