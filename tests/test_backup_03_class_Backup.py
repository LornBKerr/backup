# command --> pytest --cov-report term-missing --cov=backup ./tests/
#   run from parent directory for 'src' and 'tests'.

import os
import sys
import time

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)
#
# import pytest

from backup import Backup
from build_filesystem import (  # add_files,; additional_files,; directories,; get_test_config,; load_directory_set,
    filesystem,
)

# from lbk_library import IniFileParser


def test_Backup_01(filesystem):
    """
    Test the the object object is really a Backup class
    """
    # set filesystem
    source, dest = filesystem
    config_dir = source / ".config"
    backup = Backup([], config_dir)
    assert isinstance(backup, Backup)
    # end test_Backup_01()


def test_Backup_02(filesystem):
    """
    Test the backup.set_required_actions() method

    Walk throgh the various allowed actions.
    """
    # set filesystem
    source, dest = filesystem
    config_dir = source / ".config"

    # Do empty action list
    action_list = []
    backup = Backup(action_list, config_dir)
    # actions should have backup set to True and everything else set to False
    actions = backup.set_required_actions(action_list)
    assert actions['backup']
    assert not actions['setup']
    assert not actions['restore']
    assert not actions['test']
    assert not actions['verbose']
    
    # Do action list for backup only
    action_list = ['-b',]
    backup = Backup(action_list, config_dir)
    # actions should have backup set to True and everything else set to False
    actions = backup.set_required_actions(action_list)
    assert actions['backup']
    assert not actions['setup']
    assert not actions['restore']
    assert not actions['test']
    assert not actions['verbose']

    # do action list with setup only; not defined yet so all should be False.
    action_list = ['-s',]
    backup = Backup(action_list, config_dir)
    # actions should have everything set to False
    actions = backup.set_required_actions(action_list)
    assert not actions['backup']
    assert not actions['setup']
    assert not actions['restore']
    assert not actions['test']
    assert not actions['verbose']
    # end test_Backup_02()

def test_Backup_03(filesystem):
    """
    Testing the get_config_file() method
    
    The method retrieves the config file, then converts the strings in the
    stored file to the needed types such as integers, booleans and lists.
    """
    # set filesystem
    source, dest = filesystem
    config_dir = source / ".config"
    action_list = []
    backup = Backup(action_list, config_dir)
    config_file = backup.get_config_file()
    assert isinstance(config_file['general']['last_backup'], int)
    assert isinstance(config_file['general']['base_dir'], str)
    assert isinstance(config_file['dir_exclude']['specific_dirs'], list)
    assert isinstance(config_file['file_exclude']['backup_files'], bool)
    assert not config_file['file_exclude']['backup_files']
    
    # change config file to include a populated list and a true value
    config_file['dir_exclude']['specific_dirs'] = ['venv', '.venv']
    config_file['dir_exclude']['cloud_storage'] = True
    backup.config_handler.write_config(config_file)
    config_file = backup.get_config_file()
    assert isinstance(config_file['dir_exclude']['cloud_storage'], bool)
    assert config_file['dir_exclude']['cloud_storage']
    assert isinstance(config_file['dir_exclude']['specific_dirs'], list)
    assert len(config_file['dir_exclude']['specific_dirs']) == 2

    




