"""
Edit the configuration file for the backup program.

This configuration file provides the criteria for what is saved to the
backup file. The criteria are set as categories of files such as 'cache'
files and 'trash' files along with other settings.

The first time the program is run, a set of default settings are loaded
into the dialog. These can be accepted or modified as desired.then saved
to be used for future runs.

File:       setup.py
Author:     Lorn B Kerr
Copyright:  (c) 2022, 2023 Lorn B Kerr
License:    MIT see file LICENSE
Version:    1.0.0
"""

import os
import sys
from typing import Any

from default_config import default_config
from lbk_library import IniFileParser


class Setup:
    """Setup the configuration file for the backup."""

    def __init__(
        self, config_handler: IniFileParser, config: dict[Any, Any] = {}
    ) -> None:
        """
        Initialize the Setup dialog.

        Initially just reads the default configuration settings. The
        (platform dependent) backup file location is set. Then the
        config.ini file is saved to the config directory location.

        Eventually this will be a nice GUI to allow changing the
        settings.

        Parameters:
            config_handler (IniFileParser) read and write the
                configuration settings.
            config: (dict) the current configuration settings, may be
                empty. NOT USED currently.
        """
        # initial settings while developing, to be replaced with GUI
        self.config = default_config

        self.config["general"]["base_dir"] = os.path.expanduser("~")
        if sys.platform.startswith("linux"):
            self.config["general"]["backup_dir"] = "/run/media/larry/Backup/Linux"
        elif sys.platform.startswith("win"):
            self.config["general"]["backup_dir"] = "E:\\Windows11"
        self.config["general"]["last_backup"] = 0
        self.config["general"]["external_storage"] = True
        config_handler.write_config(self.config)
