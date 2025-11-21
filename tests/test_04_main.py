"""
Test the Backup class functionality.

File:       test_02_logger.py
Author:     Lorn B Kerr
Copyright:  (c) 2022 - 2025 Lorn B Kerr
License:    MIT, see file LICENSE
Version:    1.0.1
"""

import os
import sys
#import time

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

#import pytest
from build_filesystem import build_config_file, filesystem
#from external_storage import ExternalStorage
from lbk_library.gui import Settings
from main import Backup
#from result_codes import ResultCodes
#from setup import Setup

config_name = "BackupTest"

# build_empty_config; config file exists but has no entries.

def test_04_01_constructor(filesystem):
    """
    Test the the object is really a Backup class
    """
    # set filesystem
    source, dest = filesystem
    config = build_config_file(source, dest, config_name)
    backup = Backup([], config_name)
    assert isinstance(backup, Backup)


def test_04_02_config_file(filesystem):
    config_name = "BackupTest"
    source, dest = filesystem
    config = build_config_file(source, dest, config_name)

    backup = Backup([], config_name)
    assert len(backup.config.allKeys()) != 0
    print(backup.config.allKeys())
    assert isinstance(backup.config.value("last_backup"), int)
    assert isinstance(backup.config.value("start_dir"), str)
    assert isinstance(backup.config.read_list("exclude_specific_dirs"), list)
    assert isinstance(backup.config.value("exclude_backup_files"), bool)
    assert not backup.config.value("exclude_backup_files")

    # change config file to include a populated list and a true value
    backup.config.write_list("exclude_specific_dirs", ["venv", "bin"])
    backup.config.set_bool_value("exclude_download_dir", False)
    backup.config.sync()
    assert not backup.config.bool_value("exclude_download_dir")  
    assert isinstance(backup.config.read_list("exclude_specific_dirs"), list)
    assert len(backup.config.read_list("exclude_specific_dirs")) == 2


def test_04_03_required_actions(filesystem):
    """
    Test the backup.set_required_actions() method

    Walk throgh the various allowed actions.
    """
    # set filesystem
    source, dest = filesystem
    config_file = source / config_name

    # Do empty action list
    action_list = []
    backup = Backup(action_list, config_name)
    # actions should have backup set to True and everything else set to False
    actions = backup.set_required_actions(action_list)
    assert actions["backup"]
    assert not actions["setup"]
    assert not actions["verbose"]

    # Do action list for backup only
    action_list = [
        "-b",
    ]
    # actions should have backup set to True and everything else set to False
    actions = backup.set_required_actions(action_list)
    assert actions["backup"]
    assert not actions["setup"]
    assert not actions["verbose"]

    # do action list with setup only; all except setup should be False.
    action_list = [
        "--setup",
    ]
    # actions should have everything set to False
    actions = backup.set_required_actions(action_list)
    assert not actions["backup"]
    assert actions["setup"]
    assert not actions["verbose"]

    # do action list with multiple settings;
    action_list = [
        "--setup",
        "--restore",
        "-v",
        "--version",
    ]
    # multiple actions
    actions = backup.set_required_actions(action_list)
    assert not actions["backup"]
    assert actions["setup"]
    assert actions["verbose"]
    assert actions["version"]
    
    
    # do action list with combined settings;
    action_list = ["-bsv", "--version"]
    # multiple actions
    actions = backup.set_required_actions(action_list)
    assert actions["backup"]
    assert actions["setup"]
    assert actions["verbose"]
    assert actions["version"]


