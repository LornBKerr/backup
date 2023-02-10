"""
Initialize the configuration settings for the Backup program.

For now, it just uses the default configuration settings plus setting the
source and destination directories.

Eventually this will be a nice gui dialog to set and change all the
configuration options.

File:       setup.py
Author:     Lorn B Kerr
Copyright:  (c) 2022, 2023 Lorn B Kerr
License:    MIT, see LICENSE file
"""

import os
import sys
import time
from typing import Any

from default_config import default_config
from lbk_library import IniFileParser


class SetupWindow:
    """
    Setup the configuration file for the backup.
    """

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
        config_handler.write_config(self.config)
