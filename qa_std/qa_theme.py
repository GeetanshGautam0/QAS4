"""
FILE:           qa_std/qa_theme.py
AUTHOR:         Geetansh Gautam
PROJECT:        Quizzing Application, version 4

DOC

    Quizzing Application Theme Management

DEFINES

    (class)     dataclass       Theme

DEPENDENCIES

    qa_app_pol                              [alias: AppPolicy]
    qa_file_io.qa_theme_file.Theme

"""

import os, json
from typing import Tuple, List, Any, cast

from . import qa_def
from . import qa_app_pol as AppPolicy
from . import qa_app_info as AppInfo
from . import qa_logger as Logger

from qa_file_io.qa_theme_file import Theme, ThemeFile_s, ThemeFile
from qa_file_io import file_io_manager as FileIOManager


ScriptPolicy = AppPolicy.PolicyManager.Module('ThemeManager', 'qa_theme.py')
_default_theme_code = '5a95015ab1713b6a18ebb1750d04434730358774015'[:32]
_global_logger: Logger.Logger


class T_Config:
    @staticmethod
    def _reset_pref_file_() -> Theme:
        default_theme_file = T_DefaultTheme._load_default_theme_file_()
        default_themes = {theme.theme_code[:32]: (theme.theme_name, theme) for theme in T_DefaultTheme._load_default_themes_()[0]}
        
        if _default_theme_code not in default_themes:
            
            raise Exception(
                f'Did not find theme {_default_theme_code} in:\n\t* %s' % (
                    '\n\t* '.join([f'{v[0]}: {k}' for k, v in default_themes.items()])
                )
            )
            
        T_Config._set_pref_theme_(default_theme_file, default_themes[_default_theme_code][1])
        return default_themes[_default_theme_code][1]
    
    @staticmethod
    def _get_pref_theme_() -> Theme:
        global _default_theme_code, _global_logger
        
        'Returns: path to theme file, theme collection name, theme name, theme code'
        
        if not os.path.isfile(AppInfo.Storage.ThemeConfigurationFile):
            return T_Config._reset_pref_file_()  # Resets the theme file and returns the defualt theme.
        
        # If the file does exist
        with open(AppInfo.Storage.ThemeConfigurationFile) as f_in:
            r = f_in.read()
            f_in.close()
        
        try:
            j = json.loads(r)
            
            collection = j['tcl']
            file = qa_def.File(j['t.f'])
            code = j['t.c'][:32]
            name = j['t.n']
            
            assert os.path.isfile(file.file_path), 'Theme file not available.'
            loaded_file = ThemeFile.read_file(file)
            
            assert loaded_file.collection_name == collection, 'Theme collection not available.'
            
            for theme in loaded_file.themes:
                                
                if (theme.theme_name == name) and (theme.theme_code[:32] == code):
                    _global_logger.write(Logger.LogDataPacket(
                        'ThemeManager',
                        Logger.LoggingLevel.L_SUCCESS,
                        'Found preferred theme.'
                    ))
                                        
                    return theme
                
            raise Exception('Did not found theme')
            
        except Exception as E:
            _global_logger.write(Logger.LogDataPacket(
                'ThemeManager',
                Logger.LoggingLevel.L_ERROR,
                f'The theme configuration was corrupted and needed to be reset; restored theme preferrence to Default: Light Mode.\nException: {E}'
            ))
            
            return T_Config._reset_pref_file_()
    
    @staticmethod
    def _set_pref_theme_(theme_file: ThemeFile_s, theme: Theme) -> None:
        if not os.path.isdir(AppInfo.Storage.AppSettingsDir):
            os.makedirs(AppInfo.Storage.AppSettingsDir)
        
        assert os.path.isfile(theme_file.file.file_path)
        
        dtw = {
            't.f': theme_file.file.file_path,
            't.n': theme.theme_name,
            't.c': theme.theme_code,
            'tcl': theme_file.collection_name
        }
        
        FileIOManager.write(
            qa_def.File(AppInfo.Storage.ThemeConfigurationFile),
            json.dumps(dtw, indent=4),
            secure_mode=True,
            append_mode=False,
            offload_to_new_thread=False
        )


class T_DefaultTheme:
    @staticmethod
    def _load_default_themes_() -> Tuple[List[Theme], Any]:
        theme_file = T_DefaultTheme._load_default_theme_file_()
        return theme_file.themes, (
            theme_file.header, 
            theme_file.collection_name, 
            theme_file.file, 
            theme_file.author
        )
    
    @staticmethod
    def _load_default_theme_file_() -> ThemeFile_s:
        return ThemeFile.read_file(qa_def.File(AppInfo.Storage.DefaultThemeFile))


class ThemeInfo:
    default_themes: List[Theme]
    preferred_theme: Theme
    
    @staticmethod
    def load_all_data() -> None:       
        ThemeInfo.default_themes = T_DefaultTheme._load_default_themes_()[0]
        ThemeInfo.preferred_theme = T_Config._get_pref_theme_()


if __name__ == "__main__":
    ScriptPolicy.run_as_main()
