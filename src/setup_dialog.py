"""
Initialize the configuration settings for the Backup program.

For now, just uses the default configuration settings. Eventually this
will be a nice gui dialog to set and change all the configuration
options.

File:       setup.py
Author:     Lorn B Kerr
Copyright:  (c) 2022 Lorn B Kerr
License:    see License.txt
"""

import os
import sys
import time

from default_config import default_config


class SetupDialog:
    """
    Setup the configuration file for the backup.
    """

    def __init__(self, config, config_handler) -> None:
        """
        Initialize the Setup dialog.

        Initially just reads the default configuration settings. The
        (platform dependent) backup file location is set. Then the
        config.ini file is saved to the config directory location.

        Eventually this will be a nice GUI to allow changing the settings.

        Parameters:
            config: (dict) the current configuration settings, may be empty
            config_handler (IniFileParser) read and write the configuration
                settings
        """
        # initial settings while developing, to be replaced with GUI
        self.config = default_config
        self.config["general"]["base_dir"] = os.path.expanduser("~")
        if sys.platform.startswith("linux"):
            self.config["general"]["backup_location"] = "/run/media/larry/Backup/Linux"
        elif sys.platform.startswith("win"):
            self.config["general"]["backup_location"] = "E:\\Windows11"
        self.config["general"]["last_backup"] = 0
        config_handler.write_config(self.config)
        # end __init()


# end class SetupDialog
