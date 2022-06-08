"""
Define the default configuration for the Backup Program on Linux.

File:       default_config.py
Author:     Lorn B Kerr
Copyright:  (c) 2022 Lorn B Kerr
License:    see License.txt
"""

import os

# import platform
import sys

default_config = {
    # General conditions that apply in all cases
    "general": {
        # Time stamp of the last backup. Default of '0' means never.
        "last_backup": 0,
        # What is the base directory to start scanning for changed
        # files. By default, it is the 'users' dir, '/home/' on linux
        # or 'C:\Users' on Windows.
        "base_dir": "",
        # Where is the external storage? For a usb drive, Fedora Linux is
        # '/run/media/*backup_directory*', Windows will be a drive letter,
        # generally 'E:' or greater.
        "backup_location": "",
        # Do we want to backup to external storage, True if so, False if not
        "external_storage": False,
        # Do we want to backup to cloud storage, True if so, False if not,
        # Specific config options for cloud storage are in the
        # 'cloud_backup_options' section below
        "cloud_storage": False,
        # The backup program configuration subdirectory in the system config dir
        "config_dir": "LBKBackup",
        # the config file name
        "config_file": "backup.ini",
        # The backup log file name
        "log_file": "backup_log.db",
    },
    # What directories and files do we want to exclude from the backup?
    # In general operation, areas like the various cache and trash
    # directories are volatile and probably don't need backup. Other
    # specific directories can also be specified.
    "dir_exclude": {
        # set of directories to exclude
        # cache directories generally have the form '*/*cache*/'
        "cache_dir": True,
        # trash bins have the form '*/*trash*/
        "trash_dir": True,
        # download directories are usually transient; download
        # something and then put it where it belongs, so no backup
        # needed.
        "download_dir": True,
        # Don't save the Windows 'System Volume Information'.
        # Restoring this MAY lead to interesting and unnerving
        # results with Windows.
        "sysVolInfo_dir": True,
        # Specific directories can be noted for exclusion as desired.
        "specific_dirs": [
            "venv",
        ],
    },
    # What specific files do we want to exclude from backup.
    "file_exclude": {
        # Don't need standard backup files generated by various
        # programs with signatures like '*~' and '*.bak'
        "backup_files": True,
        # Some programs use a single file for for the 'cache' rather
        # than a directory. Exclude these files if True
        "cache_files": True,
        # Specific files can be noted for exclusion as desired.
        "specific_files": [],
    },
    # What directories do we want to include in the backup that
    # would otherwise be excluded?  Specific directories should be
    # specified.
    "dir_include": {
        # set of directories to include.
        "specific_dirs": [],
    },
    # Specific files can be noted for inclusion as desired.
    "file_include": {
        "specific_files": [],
    },
    # Cloud backup options TBD
    "cloud_backup_options": {},
}

# #######
# Standard Locations From Qt5.15 documentation
# Data Location
#   macOS:  "~/Library/Application Support/<APPNAME>",
#           "/Library/Application Support/<APPNAME>".
#           "<APPDIR>/../Resources"
#   Windows:"C:/Users/<USER>/AppData/Local/<APPNAME>",
#           "C:/ProgramData/<APPNAME>",
#           "<APPDIR>",
#           "<APPDIR>/data",
#           "<APPDIR>/data/<APPNAME>"
#   Linux:  "~/.local/share/<APPNAME>",
#           "/usr/local/share/<APPNAME>",
#           "/usr/share/<APPNAME>"
#
#
# In the table above, <APPNAME> is usually the organization name, the
# application name, or both, or a unique name generated at packaging.
# Similarly, <APPROOT> is the location where this application is installed
# (often a sandbox). <APPDIR> is the directory containing the application
# executable.
# The first path is the writable path (unless noted). Other, additional paths,
# if any, represent non-writable locations.