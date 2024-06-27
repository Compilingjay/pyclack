import configparser, os

from pathlib import Path
from PySide6.QtCore import Qt


config = configparser.ConfigParser()


def init() -> None:
    """Prepare settings by making config accessible globally."""
    global config


def loadConfig(ini_file: str = "autosave.ini") -> bool:
    """
    Loads settings from the configs folder and save them to the "config"
    configparser.\n
    By default, configs are loaded from autosave.ini.
    """
    if not Path("configs").exists():
        os.makedirs("configs")
    path = Path(f"configs/{ini_file}")
    success: bool = True
    if not path.exists():
        # log str(path) does not exist
        success = False
        default_path = Path(f"configs/default.ini")
        if not default_path.exists():
            raise FileNotFoundError("default.ini config file does not exist")
    
    config.read(path)
    return success


def saveConfig(ini_file: str = "autosave.ini") -> bool:
    """
    Saves settings from configparser to configs folder.\n
    By default, configs are saved to autosave.ini.
    """
    if not Path("configs").exists():
        os.makedirs("configs")
        # log failed to save config
        return False
    path = Path(f"configs/{ini_file}")
    
    with path.open('w') as config_file:
        config.write(config_file)
    return True


def loadAndSaveSettings(ini_file: str, other_ini_file: str) -> bool:
    """
    Loads settings from an ini file in configs/ and saves it to a new file.
    Overwrites the other_ini_file if one existed previously.
    Does not modify the existing global configs for the program.
    """
    path_load = Path(f"configs/{ini_file}")
    if not path_load.exists():
        # log failed to get file to load
        return False
    
    save_config = configparser.ConfigParser()
    save_config.read(path_load)
    
    path_save = Path(f"configs/{other_ini_file}")
    with path_save.open('w') as config_file:
        save_config.write(config_file)


def isKeyInConfig(key: str, prev_key: str | None = None) -> bool:
    """
    Parse the config for non-numerical values that are identical to the key.
    Return true if identical key is found and false if not.
    True indicates that this key should not be used and the widget using this new hotkey
    should discard it and use its previous hotkey.
    """
    if key == prev_key:
        return True

    for section in config:
        for k in config[section]:
            s = None
            try:
                s = float(k)
            except:
                pass
            finally:
                if s is not None:
                    continue

            if config[section][k] == key:
                return True
    
    return False