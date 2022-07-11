# command --> pytest --cov-report term-missing --cov=backup ./tests/
#   run from parent directory for 'src' and 'tests'.

import os
import sys
#import time

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from build_filesystem import (
#    add_files,
#    additional_files,
#    directories,
#    filesystem,
    get_test_config,
#    load_directory_set,
)
from logger import Logger

# from lbk_library import IniFileParser


def test_Logger_01():
    """
    Testing Backup.Logger.__init__()

    Test the the object is really a Logger class
    """
    test_config = get_test_config()
    path = ''
    logger = Logger(path)
    assert isinstance(logger, Logger)
    # end test_ExternalStorage_01()



