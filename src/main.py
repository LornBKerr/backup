"""
Backup the selected file system.

Backup a set of files to the external backup storage.

File:       main.py
Author:     Lorn B Kerr
Copyright:  (c) 2022, 2023 Lorn B Kerr
License:    MIT, see file LICENSE
Version:    1.1.0
"""

import datetime
import os
import re
import sys
import time
from typing import Any

from PySide6.QtCore import QSettings

from default_config import default_config
from external_storage import ExternalStorage
from logger import Logger
from result_codes import ResultCodes
from setup_window import SetupWindow


class Backup:
    """
    This executes the backup process.

    Part 1: backup to external storage.
    Backup any new and changed files in the global home directory to the
    backup directory on an external disk drive. A new file is one that
    has been added or renamed since the last backup. A changed file is
    one whose modification time stamp is greater than the backed up
    file time stamp.

    Any new directories are created in the backup store and changed
    files are copied to the store.
    """

    def __init__(self, action_list: list[str] = []) -> None:
        """
        Initialize and run the backup program based on the action list.

        Parameters:
            action_list (list[str]):  the set of requested actions.
               Actions defined (all optional) are:
                --setup
                    Run the setup portion to configure the program
                -b, --backup
                    Run the backup portion (default if no other option
                    is included, required if other options are used.
                -v, --verbose
                    Show the steps being accomplished.
                --version
                    Show the version of the program.

        Errors:
            Exits  with error code 3 and with an error message if no
            configuration file is present and the program is executed
            without the '--setup' action flag.
        """
        self.actions: dict[str, bool]
        """ The set of requested actions """
        self.config = QSettings("Unnamed Branch", "Backup")
        """The configuration setup."""
        self.external_storage: ExternalStorage
        """ Handle the backup to the external storage drive """
        self.logger: Logger
        """ The results log database driver """

        start_time = time.time()  # Get the starting timestamp

        # set configuration
        if not len(self.config.allKeys()):
            self.initialize_config_file()

        self.actions = self.set_required_actions(action_list)
        print(self.actions)

        if not self.config and not self.actions["setup"]:
            print(
                "\n\tERROR! No Configuration File:",
                "\n\tCannot run the backup program until setup is completed",
                "\n\tPlease use 'backup --setup'\n",
            )
            sys.exit(ResultCodes.NO_CONFIG_FILE)  # Error 3: No Config File, Run Setup.

        # Update the config file if required
        if self.actions["setup"]:
            self.do_setup(action_list)
            self.config = self.get_config_file()

        # Setup logging
        # put the logger file in the same directory as the config file
        log_db_path = os.path.join(
            os.path.dirname(self.config_handler.config_path()),
            self.config["general"]["log_file"],
        )
        self.logger = Logger(log_db_path)

        self.logger.add_log_entry(
            {
                "timestamp": int(start_time),
                "result": ResultCodes.SUCCESS,
                "description": "Backup Started "
                + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time)),
            }
        )

        if self.actions["verbose"]:
            print(
                "started:",
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time)),
            )

        if self.actions["backup"]:
            if self.config["general"]["external_storage"]:
                self.external_storage = ExternalStorage(
                    self.config, self.logger, self.actions
                )

        # update the config file 'last backup' time
        self.config["general"]["last_backup"] = int(start_time)
        self.config_handler.write_config(self.config)

        end_time = time.time()  # Get the ending timestamp
        elapsed = int(end_time - start_time)  # how long did backup take.
        self.logger.add_log_entry(
            {
                "timestamp": int(end_time),
                "result": ResultCodes.SUCCESS,
                "description": "Backup Finished "
                + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time)),
            }
        )
        self.logger.add_log_entry(
            {
                "timestamp": int(end_time),
                "result": ResultCodes.SUCCESS,
                "description": "Elapsed time: "
                + str(datetime.timedelta(seconds=elapsed)),
            }
        )

        self.logger.close_log()

        if self.actions["verbose"]:
            print(
                "ended:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_time))
            )
            print("Elapsed time: " + str(datetime.timedelta(seconds=elapsed)))
        # end __init__()

    def set_required_actions(self, args: list[str]) -> list[bool]:
        """
        Set the required actions from the command line arguments.

        If no arguments are supplied, then set for backup only.

        Parameters:
            args (list[str]): the set of requested actions

        Returns:
            (list[bool]) the requested actions
        """
        # initialize requested actions
        actions = {
            "backup": False,  # Do backup?
            "setup": False,  # Do the setup?
            "verbose": False,  # show progress on terminal
            "version": False,  # show program version and exit
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
                elif action == "--setup":
                    actions["setup"] = True
                elif action == "-v" or action == "--verbose":
                    actions["verbose"] = True
                elif action == "--version":
                    actions["version"] = True

        return actions

    def initialize_config_file(self) -> None:
        """
        If there is no stored QSettings entries, then this supplies a
        default set of values. The default values are found in the
        file 'backup/src/default_config.py'.
        """
        for heading in default_config:
            self.config.beginGroup(heading)
            for key in default_config[heading]:
                self.config.setValue(key, default_config[heading][key])
            self.config.endGroup()

    def do_setup(self, args) -> int:
        """
        Set up initial configuration file.

        Temporary fix while waiting for GUI to be developed and released.
        """
        setup_window = SetupWindow(self.config_handler, self.actions)
