"""
File Backup

Backup the selected file system to the backup storage and to cloud storage.

Part 1: backup to external storage
Backup any new and changed files in the global home directory to the backup
directory on an external disk drive. A new file is one that has been added or
renamed since the last backup. A changed file is one whose modification
time stamp is greater than the backed up file time stamp.

Any new directories are created in the backup store and changed files
are copied to the store.

Part 2 - Not yet implemented
After the external storage is updated, backup to cloud storage using
the 'restic' program.

 File:       backup.py
 Author:     Lorn B Kerr
 Copyright:  (c) 2022 Lorn B Kerr
 License:    see file LICENSE
 """


import datetime
import re
import sys
import time
from typing import Any

from external_storage import ExternalStorage
from lbk_library import Dbal, IniFileParser
from logger import Logger
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
                    (Partially Implemented) Run the setup portion to configure the
                    program
                -b, --backup
                    Run the backup portion (default if no other option is
                    included, required if backup is desired after setup is
                    requested.
                -r, --restore
                    (Not Implemented) Restore the previously saved cloud backup
                -t, --test
                    (Not Implemented) Run the backup portion showing what would
                    be accomplished without actually saving anything.
                -v, --verbose
                    Show the steps being accomplished.

              config_dir: (string) override the default system config path,
                    default is empty string to use the default system location.
        Errors:
            Exits  with error code 3 and with an error message if no
            configuration file is present and the program is executed without
            the '-s' or '--setup' action flag.
        """
        self.actions: dict[str, bool]
        """ The set of requested actions """
        self.config: dict[str, Any] = {}
        """ The configuration File (dict)"""
        self.config_handler: IniFileParser
        """ Config file reader/writer """
        self.external_storage: ExternalStorage = None
        """ Handle the backup to the external storage drive """
        self.logger: Logger
        """ The results database log driver """
        self.setup_dialog: SetupDialog = None
        """ The Setup Dialog class """

        # initialize
        start_time = time.time()  # Get the starting timestamp
        self.config_handler = IniFileParser("backup.ini", "LBKBackup", config_dir)
        # put the logger file in the same directory as the config file
        self.logger = Logger(self.config_handler.config_path())

        self.actions = self.set_required_actions(action_list)

        if self.actions["verbose"]:
            print(
                "started:", time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(start_time))
            )


        if self.actions["setup"]:
            self.setup_dialog = SetupDialog(self.config, self.config_handler)
        self.config = self.get_config_file()
        if not self.config and not self.actions["setup"]:
            print(
                "\n\tERROR! No Configuration File:",
                "\n\tCannot run the backup program",
                "\n\tPlease use 'backup -s' or 'backup --setup'\n",
            )
            sys.exit(3)  # Error 3: No Config File, Run Setup.

        if self.actions["backup"]:
            if self.config["general"]["external_storage"]:
                self.external_storage = ExternalStorage(self.config, self.actions)

        # update the config file 'last backup' time
        self.config["general"]["last_backup"] = int(start_time)
        self.config_handler.write_config(self.config)

        end_time = time.time()  # Get the ending timestamp
        elapsed = int(end_time - start_time)  # how long did backup take.
        if self.actions["verbose"]:
            print("ended:", time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(end_time)))
            print("Elapsed time:", datetime.timedelta(seconds=elapsed))
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
                elif action == "-v" or action == "--verbose":
                    actions["verbose"] = True

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
