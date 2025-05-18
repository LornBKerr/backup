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
import time

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

import pytest
from build_filesystem import build_config_file, filesystem, get_test_config
from external_storage import ExternalStorage
from lbk_library import IniFileParser
from main import Backup
from result_codes import ResultCodes
from setup_window import SetupWindow

# from setup_window import SetupWindow

config_dirname = ".config/lbk_software"


def test_04_01_constructor(filesystem):
    """
    Test the the object is really a Backup class
    """
    # set filesystem
    source, dest = filesystem
    config_dir = source / config_dirname
    backup = Backup([], config_dir)
    assert isinstance(backup, Backup)


def test_04_02_config_file(filesystem):
    source, dest = filesystem
    config_dir = source / config_dirname
    backup = Backup([], config_dir)
    os.remove(config_dir / "backup" / "backup.ini")
    config_file = backup.get_config_file()
    assert len(config_file) == 0
    assert config_file == {}

    build_config_file(source, dest)
    config_file = backup.get_config_file()
    assert isinstance(config_file["general"]["last_backup"], int)
    assert isinstance(config_file["general"]["base_dir"], str)
    assert isinstance(config_file["dir_exclude"]["specific_dirs"], list)
    assert isinstance(config_file["file_exclude"]["backup_files"], bool)
    assert not config_file["file_exclude"]["backup_files"]

    # change config file to include a populated list and a true value
    config_file["dir_exclude"]["specific_dirs"] = ["venv", ".venv"]
    config_file["dir_exclude"]["cloud_storage"] = True
    backup.config_handler.write_config(config_file)
    config_file = backup.get_config_file()
    assert isinstance(config_file["dir_exclude"]["cloud_storage"], bool)
    assert config_file["dir_exclude"]["cloud_storage"]
    assert isinstance(config_file["dir_exclude"]["specific_dirs"], list)
    assert len(config_file["dir_exclude"]["specific_dirs"]) == 2


def test_04_03_required_actions(filesystem):
    """
    Test the backup.set_required_actions() method

    Walk throgh the various allowed actions.
    """
    # set filesystem
    source, dest = filesystem
    config_dir = source / config_dirname

    # Do empty action list
    action_list = []
    backup = Backup(action_list, config_dir)
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
        "-t",
        "-v",
        "--version",
    ]
    # multiple actions
    actions = backup.set_required_actions(action_list)
    assert not actions["backup"]
    assert actions["setup"]
    assert actions["verbose"]
    assert actions["version"]


def test_04_04_no_config_file(filesystem, capsys):
    """
    Test the action when no config file is present.

    Should raise the SystemExit exception with error code 3.
    """
    source, dest = filesystem
    config_dir = source / config_dirname
    os.remove(config_dir / "backup" / "backup.ini")

    action_list = []

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        backup = Backup(action_list, config_dir)
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == ResultCodes.NO_CONFIG_FILE
    # end test_Backup_05()


def test_04_05_external_storage(filesystem):
    """
    Test the call to ExternalStorage.

    We don't want to do a backup here, just check the the right object is
    called. The ExternalStorage file is tested in
    'test_backup_03_class_Backup.py'. Set the source and destination
    directories to empty strings which will disable actual backups.
    """
    source, dest = filesystem
    config_dir = source / config_dirname
    config_handler = IniFileParser(
        "backup.ini", "backup", source / ".config/lbk_software"
    )
    config_file = config_handler.read_config()
    config_file["general"]["base_dir"] = ""
    config_file["general"]["backup_dir"] = ""
    config_file["general"]["external_storage"] = True
    config_handler.write_config(config_file)

    action_list = ["-b"]
    backup = Backup(action_list, config_dir)
    assert isinstance(backup.external_storage, ExternalStorage)


def test_04_setup_window(filesystem):
    source, dest = filesystem
    config_dir = source / config_dirname
    backup = Backup(["--setup"], config_dir)
    config_file = backup.get_config_file()
    print("setup:", config_file)
    if sys.platform.startswith("linux"):
        assert config_file["general"]["backup_dir"] == "/run/media/larry/Backup/Linux"
    elif sys.platform.startswith("win"):
        assert config_file["general"]["backup_dir"] == "E:\\Windows11"
