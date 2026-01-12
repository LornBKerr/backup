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
import re
import time

from external_storage import ExternalStorage
from lbk_library.gui import Settings
from logger import Logger

from PySide6.QtWidgets import QApplication
from result_codes import ResultCodes
from setup import Setup

file_name = "main.py"
file_version = "1.1.0"
changes = {
    "1.0.0": "Initial release",
    "1.0.1": "Changed library 'PyQt5' to 'PySide6' and code cleanup",
    "1.1.0": "Changed from ini file to lbkLibrary/Settings",
}


class Backup:
    """
    This executes the backup process.

    Backup any new and changed files in the global home directory to the
    backup directory on an external disk drive. A new file is one that
    has been added or renamed since the last backup. A changed file is
    one whose modification time stamp is greater than the backed up
    file time stamp.

    Any new directories are created in the backup store and changed
    files are copied to the store.
    """

    def __init__(
        self, action_list: list[str] = [], config_name: str = "Backup.conf"
    ) -> None:
        """
        Initialize and run the backup program based on the action list.

        Parameters:
            action_list (list[str]):  the set of requested actions.
               Actions defined (all optional) are:
                -s, --setup
                    Run the setup portion to configure the program
                -b, --backup
                    Run the backup portion (default if no other option
                    is included, required if other options are used.
                -v, --verbose
                    Show the steps being accomplished.
                --version
                    Show the version of the program.
            config_name (str) -: The name of the system configuration file,
                 defaults to 'Backup'.
        """
        self.actions: dict[str, bool] = self.set_required_actions(action_list)
        """The set requested actions from the action list."""
        self.config = Settings("UnnamedBranch", config_name)
        """The configuration setup."""

        self.external_storage: ExternalStorage
        """Handle the backup to the external storage drive."""
        self.logger: Logger
        """The results log driver."""

        start_time = time.time()  # Get the starting timestamp
        print("start time", start_time)
        print("actions:", self.actions)

        # If there is no configuration set or configuration is requested,
        # initialize the configuration and reload config.
        if not len(self.config.allKeys()) or self.actions["setup"]:
            self.do_setup()
            self.config = Settings("UnnamedBranch", config_name)

        # Start logging
        self.logger = Logger(
            self.config.value("log_path"), self.config.value("log_name")
        )
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
            self.external_storage = ExternalStorage(
                self.config, self.logger, self.actions
            )

        # update the config file 'last backup' time
        self.config.setValue("last_backup", int(start_time))

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
        self.logger.close_log()

    def set_required_actions(self, args: list[str]) -> dict[str, bool]:
        """
        Set the required actions from the command line arguments.

        Valid arguments are in the group
            -b, --backup, -s, --setup, -v, --verbose, --version
        The single letter arguments can be combined into a group
        (i.e.: -bv will be decoded as --backup -- verbose).

        If no arguments are supplied, then set for backup only.

        Parameters:
            args (list[str]): the set of requested actions

        Returns:
            (dict[str, bool]) the requested actions
        """
        # initialize requested actions
        actions = {
            "backup": False,  # Do backup?
            "setup": False,  # Do the setup?
            "verbose": False,  # show progress on terminal
            "version": False,  # show program version and exit
        }

        # validate/simplify grouped single letter actions
        for i in range(len(args)):
            if re.match(r"-[A-Za-z]{2,}", args[i]):
                new_args = list(args[i])
                for j in range(1, len(new_args)):
                    args.append("-" + new_args[j])
                args.remove(args[i])

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
                elif action == "-v" or action == "--verbose":
                    actions["verbose"] = True
                elif action == "--version":
                    actions["version"] = True
        return actions

    def do_setup(self) -> int:
        """
        Set up initial configuration file.

        Open the setup window to set all the configuration values.
        """
        self.app = QApplication.instance()
        if self.app is None:
            self.app = QApplication(sys.argv)
        self.main_window = Setup(self.config)
        return_value = self.app.exec()
        self.app.shutdown()  # Undocumented workaround to destroy the app
        # https://bugreports.qt.io/browse/PYSIDE-1190
        return return_value
