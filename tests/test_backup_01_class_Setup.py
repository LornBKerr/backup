# command --> pytest --cov-report term-missing --cov=backup ../tests/

import sys
import time

import pytest

if "/home/larry/development/backup/src" not in sys.path:
    sys.path.append("/home/larry/development/backup/src")

from default_config import default_config
from lbk_library import IniFileParser
from setup_dialog import SetupDialog

config_handler = IniFileParser("backup.ini", "LBKBackup")
config_file = default_config


def test_01_setup_constr():
    """
    Test the the setup object is really a Setup class
    """
    setup = SetupDialog(config_file, config_handler)
    assert isinstance(setup, SetupDialog)


def test_02_config_settings():
    setup = SetupDialog(config_file, config_handler)
    assert isinstance(setup.config, dict)
    assert setup.config["general"]["base_dir"] == "/home"
    assert setup.config["general"]["backup_location"] == "/run/media/larry/Backup/Linux"
    assert setup.config["general"]["last_backup"] <= int(time.time() - 86400)
