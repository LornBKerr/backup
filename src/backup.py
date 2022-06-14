"""
File Backup

Backup the '/home' filesystem to the backup storage and to cloud storage.

Part 1: backup to external storage
Backup any new and changed files in the global home directory to the backup
directory on an external disk drive. A new file is one that has been added or
renamed since the last backup. A changed file is one whose modification
timestamp is greater than the stored last backup timestamp.

Any new directories are created in the backup store and changed files
are copied to the store.

Part 2
After the external storage is updated, backup to cloud storage using
the 'restic' program.

 File:       backup.py
 Author:     Lorn B Kerr
 Copyright:  (c) 2022 Lorn B Kerr
 License:    see License.txt
 """

import re
import sys
import time  # datetime,
from typing import Any

from lbk_library import IniFileParser

from external_storage import ExternalStorage
from setup_dialog import SetupDialog


class Backup:
    """
    This executes the backup program.
    """

    def __init__(self, action_list: list[str] = [], config_dir: str = "") -> None:
        """
        Initialize and run the backup program based on the action list.

        Parameters:
            action_list: (list[string]) the set of requested actions.
                Actions defined (all optional) are:
                -s, --setup
                    (Not Implemented) Run the setup portion to configure the
                    program
                -b, --backup
                    Run the backup portion (default if setup is not requested,
                    required if backup is desired after setup is requested.
                -r, --restore
                    (Not Implemented) Restore the previously saved cloud backup
                -t, --test
                    (Not Implemented) Run the backup portion showing what would
                    be accomplished without actually saving anything.
                -v, --verbose
                    (Not Implemented) Show the steps being accomplished

              config_dir: (string) override the default system config path,
                    default is empty string to use the default system location.
        """
        self.actions: dict[str, bool]
        """ The set of requested actions """
        self.config: dict = {}
        """ The configuration File (dict)"""
        self.config_handler: IniFileParser
        """ Config file reader/writer """

        start_time = time.time()  # Get the starting timestamp
        self.actions = self.set_required_actions(action_list)
        self.config_handler = IniFileParser("backup.ini", "LBKBackup", config_dir)

        if self.actions["setup"]:
            SetupDialog(self.config, self.config_handler)
        self.config = self.get_config_file()

        if not self.config and not self.actions["setup"]:
            print(
                "\n\tERROR! No Configuration File:",
                "\n\tCannot run the backup program",
                "\n\tPlease use 'backup -s' or 'backup --setup'\n",
            )
            exit()

        if self.actions["backup"]:
          if self.config["general"]["external_storage"]:
                ExternalStorage(self.config)

           # update the conf file last backup time
        self.config["general"]["last_backup"] = int(start_time)
        self.config_handler.write_config(self.config)
        # end __init__()

    def set_required_actions(self, args: list[str]) -> list[bool]:
        """
        Set the required actions from the command line arguments.

        If no arguments are supplied, then set for backup only.

        Parameters:
            args: (list[string]) the set of requested actions

        Returns:
            (list[bool]) the rquested actions
        """
        # initialize requested actions
        actions = {
            "backup": False,  # Do backup?
            "setup": False,  # Do the setup?
            "restore": False,  # do restore?
            "test": False,  # do test actions?
            "verbose": False,  # show progress on terminal
            "config_loc": False,  # no config file specified
        }

        # set required actions
        if len(args) == 0:
            # no requested actions, set to backup only (normal condition)
            actions["backup"] = True
        else:
            # some set of arguments are requested
            for action in args:
                if action == "-b" or action == "--backup":
                    actions["backup"] = True
                elif action == "-s" or action == "--setup":
                    actions["setup"] = True
#                elif action == "-r" or action == "--restore":
#                    actions["restore"] = True
#                elif action == "-t" or action == "--test":
#                    actions["test"] = True
#                elif action == "-v" or action == "--verbose":
#                    actions["verbose"] = True
        return actions

    # end set_required_actions()

    def get_config_file(self) -> dict[str, Any]:
        """
        Read the config file.

        The raw config file values are all strings. Before returning the
        config file, convert the boolean, integer and list string values
        to actual boolean, integer and list entities.

        Returns:
            (dict[str, Any]) the set of configuration values.
        """
        config = self.config_handler.read_config()
        for section in config:
            for option in config[section]:
                # handle booleans
                if config[section][option] in ["True", "true"]:
                    config[section][option] = True
                elif config[section][option] in ["False", "false"]:
                    config[section][option] = False
                    # handle integers
                elif re.match(r"\d+", config[section][option]):
                    config[section][option] = int(config[section][option])
                    # handle lists
                elif re.match(r"\[.*\]", config[section][option]):
                    dir_list = config[section][option][1:-1]
                    if len(dir_list) == 0:  # empty list
                        config[section][option] = []
                    else:
                        dir_list = dir_list.replace("'", "")
                        dir_list = dir_list.replace(" ", "")
                        config[section][option] = dir_list.split(",")
        return config
        # end get_config_file()
# end Class Backup


if __name__ == "__main__":
    # get the command line arguments
    args = sys.argv
    args.pop(0)  # discard the program name

    # Run the program
    #    app = QApplication(sys.argv)  # used for the setup GUI
    Backup(args)
# end file backup.py
