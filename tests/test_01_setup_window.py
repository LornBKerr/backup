# command --> pytest --cov-report term-missing --cov=backup ../tests/

import os
import sys
import time

import pytest

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from default_config import default_config
from lbk_library import IniFileParser
from setup_window import SetupWindow

config_handler = IniFileParser("backup.ini", "backup")
config_file = default_config


def test_01_01_SetupWindow():
    setup = SetupWindow(config_handler)
    assert isinstance(setup, SetupWindow)


def test_01_02_SetupWindow():
    """
    Testing the basic configuration settings from SetupDialog.

    This is a placeholder until the actual dialog is written.
    """
    setup = SetupWindow(config_handler)
    assert isinstance(setup.config, dict)
    assert setup.config["general"]["base_dir"] == os.path.expanduser("~")
    if sys.platform.startswith("linux"):
        assert setup.config["general"]["backup_dir"] == "/run/media/larry/Backup/Linux"
    elif sys.platform.startswith("win"):
        assert setup.config["general"]["backup_dir"] == "E:\\Windows11"
    assert setup.config["general"]["last_backup"] <= int(time.time() - 86400)
