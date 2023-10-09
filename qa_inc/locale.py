"""
FILE:           qa_inc/locale.py
AUTHOR:         Geetansh Gautam
PROJECT:        Quizzing Application, version 4

DOC

    Locale information

DEFINES

    (class)     enum                            LOCALE
    (enum)      LOCALE                          ENG_US              English (U.S.)  "en-US"
    (class)     dataclass                       Locale
                Locale                          locale              Locale requested by applications settings.
                                                                    DO NOT access locale directly. Use get_locale.
                dict[LOCALE, class]             LOCALE_MAP
    (method)    Locale                          get_locale          Loads and returns `locale`. NEVER access `locale`
                                                                    directly.
                bool                            locale_loaded

DEPENDENCIES

    typing.*
    json
    os
    enum.Enum                   [alias: Enum]

RAISES

    FileNotFoundError
                                .conf/configuration.json
                                locale *

    AssertionError
        from get_locale         0x00----
                                0x000001                DATA STRUCTURE
                                0x000002                DATA STRUCTURE
                                0x000003                DATA STRUCTURE
                                0x000004                DATA STRUCTURE
                                0x000005                DATA INTEGRITY


"""

import json, os
from typing import *
from dataclasses import dataclass
from enum import Enum


class LOCALE(Enum):
    ENG_US = 0


@dataclass
class Locale:
    lang: Optional[str] = None
    region: Optional[str] = None
    encoding: Optional[str] = None


class EnglishUS(Locale):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        Locale.__init__(self)

        self.lang = 'en'
        self.region = 'US'
        self.encoding = 'utf-8'

    def __format__(self, spec: str) -> str:
        match spec:
            case 'lang':
                return self.lang
            case 'region':
                return self.region
            case 'encoding':
                return self.encoding
            case _:
                return self.__str__()


LOCALE_MAP: Dict[int, Any] = {
    LOCALE.ENG_US.value: EnglishUS
}

locale: Locale
locale_loaded = False


def get_locale() -> Locale:
    global locale, locale_loaded, LOCALE_MAP

    # If already loaded, return locale info
    if locale_loaded:
        return locale

    # Open the config file
    if not os.path.isfile('.conf/configuration.json'):
        raise FileNotFoundError('.conf/configuration.json')

    with open('.conf/configuration.json', 'r') as configuration:
        config_raw = configuration.read()
        configuration.close()

    # Look for locale information. If it doesn't exist, default to en-US
    app_locale = json.loads(config_raw).get('settings', {}).get('locale', [0, 'en-US'])

    # Make sure that the data is structured correctly
    assert isinstance(app_locale, list),    '0x000001'
    assert len(app_locale) == 2,            '0x000002'
    assert isinstance(app_locale[0], int),  '0x000003'
    assert isinstance(app_locale[1], str),  '0x000004'

    # Look for the class that matches with the locale
    if app_locale[0] not in LOCALE_MAP.keys():
        raise FileNotFoundError(f'locale {app_locale[1]}')

    # Generate the locale information
    locale = cast(Locale, LOCALE_MAP[app_locale[0]]())

    # Check to make sure that this is the right locale
    locale_name = f'{locale.lang}-{locale.region}'
    assert locale_name == app_locale[1],    '0x000005'

    # All is well; set locale_loaded to true and then return the locale information
    locale_loaded = True
    return locale
