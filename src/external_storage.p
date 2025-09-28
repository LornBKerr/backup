#"""
#Backup a directory structure to an external drive.
#
#File:       external_storage.py
#Author:     Lorn B Kerr
#Copyright:  (c) 2022 Lorn B Kerr
#License:    MIT, see file LICENSE
#Version:    1.1.0
#"""
#
#import os
#import shutil
#import sys
#import time
#from copy import deepcopy
#from typing import Any
#
#from logger import Logger
#from result_codes import ResultCodes
#
#file_name = "external_storage.py"
#file_version = "1.1.0"
#changes = {
#    "1.0.0": "Initial release",
#    "1.1.0": "Removed unused cloud options and config values;"
#    + "Removed unnecessary section headers to make a single level dict;"
#    + "Corrected 'base_dir' to 'start_dir'.",
#}
#
#
#class ExternalStorage:
#    """
#    Backup a directory structure to an external drive.
#
#    Parameters:
#        config (dict[str, Any]): the config file; the criteria for
#                the backup.
#        actions (dict[str, bool]): The required actions to take.
#    """
#
#    def __init__(
#        self, config: dict[str, Any], logger: Logger, actions: dict[str, bool] = None
#    ) -> None:
#        """
#        Backup all fresh files to the external drive.
#
#        Fresh files are those files that added or have changed since the
#        last backup and are not otherwise excluded from backup.
#        """
#        self.actions: dict[str, bool] = actions
#        """ The list of actions directed """
#        self.config: dict[str, Any] = config
#        """ The configuration controlling the backup """
#        self.directories_checked: int = 0
#        """ The count of all directories traversed. """
#        self.directories_backed_up: int = 0
#        """ The count of the new directories backed up """
#        self.files_files_checked: int = 0
#        """ The count of files checked for potential backup. """
#        self.files_backed_up: int = 0
#        """ The count of the fresh files actually backed up """
#        self.logger: Logger = logger
#        """ The result logger for the database. """
#
#        if (
#            self.config["start_dir"] == ""
#            and self.config["backup_location"] == ""
#        ):
#            self.logger.add_log_entry(
#                {
#                    "timestamp": int(time.time()),
#                    "result": ResultCodes.NO_SOURCE_OR_DESTINATION,
#                    "description": (
#                        " Need to specify both the source"
#                        " and destination directories. "
#                    ),
#                }
#            )
##        else:
##            self.backup()
##
##        self.logger.add_log_entry(
##            {
##                "timestamp": int(time.time()),
##                "result": ResultCodes.SUCCESS,
##                "description": str(self.directories_checked) + " directories checked.",
##            }
##        )
##        self.logger.add_log_entry(
##            {
##                "timestamp": int(time.time()),
##                "result": ResultCodes.SUCCESS,
##                "description": str(self.directories_backed_up)
##                + " directories backed up to external storage.",
##            }
##        )
##        self.logger.add_log_entry(
##            {
##                "timestamp": int(time.time()),
##                "result": ResultCodes.SUCCESS,
##                "description": str(self.files_files_checked) + " files checked.",
##            }
##        )
##        self.logger.add_log_entry(
##            {
##                "timestamp": int(time.time()),
##                "result": ResultCodes.SUCCESS,
##                "description": str(self.files_backed_up)
##                + " files backed up to external storage.",
##            }
##        )
##
##        if self.actions["verbose"]:
##            print(self.directories_checked, "directories checked.")
##            print(
##                self.directories_backed_up, "directories backed up to external storage."
##            )
##            print(self.files_files_checked, "files checked.")
##            print(self.files_backed_up, "files backed up to external storage.")
##
##    def backup(self) -> None:
##        """
##        Scan and backup the directories.
##
##        Copy changed/new, not excluded files to external storage. Then
##        check for any specifically included directories and files.
##
##        As the directories are scanned, the destination is checked to
##        ensure the destination is present prior to tring to copy a
##        new or changed file to the destination.
##        """
##        source = self.config["start_dir"]
##        source_len = len(str(source)) + 1
##        destination = self.config["backup_location"]
##
##        # make sure the base destination directory exists
##        try:
##            if not os.path.isdir(destination):
##                os.makedirs(destination)
##        except Exception as exc:
##            self.logger.add_log_entry(
##                {
##                    "timestamp": int(time.time()),
##                    "result": ResultCodes.NO_EXTERNAL_STORAGE,
##                    "description": " Could not access the Extrernal Storage Drive ",
##                }
##            )
##
##            sys.exit(ResultCodes.NO_EXTERNAL_STORAGE)
##
##            # walk the base directory and all subdirectories.
##        for current_dir, subdirs, fileset in os.walk(source):
##            self.directories_checked += 1
##            if self.actions["verbose"]:
##                if self.directories_checked % 1000 == 0:
##                    print(self.directories_checked, "directories processsed")
##            # if directory not excluded, check the directory's file_set
##            is_dir_excluded = [
##                ele for ele in self.dir_exclude_list if ele in current_dir
##            ]
##            is_dir_included = [
##                ele for ele in self.dir_include_list if ele in current_dir
##            ]
##            if not bool(is_dir_excluded) or bool(is_dir_included):
##                self.directories_backed_up += 1
##                # make sure the current destination directory exists
##                destination_dir = os.path.join(destination, current_dir[source_len:])
##                if not os.path.isdir(destination_dir):
##                    os.mkdir(destination_dir)
##                self.process_dir_files(current_dir, destination_dir, fileset)
##
##    def process_dir_files(
##        self, current_dir: str, destination_dir: str, fileset: list[str]
##    ) -> None:
##        """
##        Step through the the current directory.
##
##        Backup the new/changed files that are not otherwise excluded.
##
##        Parameters:
##            current_dir: (str) the directory being read
##            destination_dir: (str) the backup destination for the
##                new/changed file .
##            fileset: (list[str]) the set of files to backup.
##        """
##        for filename in fileset:
##            self.files_files_checked += 1
##            if not (
##                filename.endswith(tuple(self.file_exclude_list))
##                or bool([ele for ele in self.file_exclude_list if (ele in filename)])
##            ):
##                self.process_file(current_dir, destination_dir, filename)
##
##    def process_file(
##        self, current_dir: str, destination_dir: str, filename: str
##    ) -> None:
##        """
##        Backup the current file if necessary.
##
##        If the file has been modified since the last backup, copy it to
##        the external storage directory. If the file is a link and is
##        broken, skip the link.
##
##        Parameters:
##            current_dir: (str) the directory being read
##            destination_dir: (str) the backupdestination for the
##                new/changed file .
##            filename: (str) the file to backup.
##        """
##        current_path = os.path.join(current_dir, filename)
##        destination_path = os.path.join(destination_dir, filename)
##
##        # check for broken symlink os.path.islink(path)
##        # if broken, skip link and return
##        if os.path.islink(current_path) and not os.path.isfile(current_path):
##            return  # skip broken links
##
##            # if file is newer than backup file, back it up
##        if (
##            not os.path.exists(destination_path)
##            or int(os.stat(current_path).st_mtime)
##            > self.config["general"]["last_backup"]
##            or int(os.stat(current_path).st_mtime)
##            > int(os.stat(destination_path).st_mtime)
##        ):
##            try:
##                shutil.copy2(current_path, destination_path, follow_symlinks=False)
##                shutil.copystat(current_path, destination_path, follow_symlinks=False)
##                self.files_backed_up += 1
##                if self.actions["verbose"]:
##                    print("file:", destination_path)
##            except Exception as exc:
##                self.logger.add_log_entry(
##                    {
##                        "timestamp": int(time.time()),
##                        "result": ResultCodes.FILE_NOT_COPIED,
##                        "description": "Backup of file " + current_path + " failed.",
##                    }
##                )
##                if self.actions["verbose"]:
##                    print("Backup of file", current_path, "failed.")
##
##    @property
##    def dir_exclude_list(self) -> list[str]:
##        """
##        Builds the list of excluded directories from the config settings.
##
##        Returns:
##            (list[str]) the set of excluded directories.
##        """
##        exclusion_list = deepcopy(self.config["dir_exclude"]["specific_dirs"])
##        if self.config["dir_exclude"]["cache_dir"]:
##            exclusion_list.append("cache")
##            exclusion_list.append("Cache")
##        if self.config["dir_exclude"]["trash_dir"]:
##            exclusion_list.append("trash")  # linux
##            exclusion_list.append("Trash")
##            exclusion_list.append("$RECYCLE.BIN")  # windows
##        if self.config["dir_exclude"]["download_dir"]:
##            exclusion_list.append("Downloads")  # Linux
##
##            # Don't save the Windows 'System Volume Information'.
##            # Restoring this MAY lead to interesting and unnerving
##            # results with Windows.
##        if self.config["dir_exclude"]["sysvolinfo_dir"]:
##            exclusion_list.append("System Volume Information")
##
##        return exclusion_list
##        # end set_set_dir_exclude_list()
##
##    @property
##    def dir_include_list(self) -> list[str]:
##        """
##        Builds the list of specifically included directories.
##
##        Returns:
##            (list[str]) the set of included directories.
##        """
##        inclusion_list = deepcopy(self.config["dir_include"]["specific_dirs"])
##        return inclusion_list
##        # end set_dir_include_list()
##
##    @property
##    def file_exclude_list(self) -> list[str]:
##        """
##        Builds the list of excluded files.
##
##        Returns:
##            (list[str]) the set of excluded directories.
##        """
##        # What specific files do we want to exclude from backup.
##        exclusion_list = deepcopy(self.config["file_exclude"]["specific_files"])
##        if self.config["file_exclude"]["backup_files"]:
##            exclusion_list.append("~")
##            exclusion_list.append(".bak")
##        if self.config["file_exclude"]["cache_files"]:
##            exclusion_list.append("cache")
##            exclusion_list.append("Cache")
##        return exclusion_list
##        # end set_file_exclude_list()
##
##    @property
##    def file_include_list(self) -> list[str]:
##        """
##        Builds the list of included files.
##
##        Returns:
##            (list[str]) the set of included directories.
##        """
##        # What specific files do we want to include in the backup.
##        inclusion_list = deepcopy(self.config["file_include"]["specific_files"])
##        return inclusion_list
##        # end set_file_include_list()
