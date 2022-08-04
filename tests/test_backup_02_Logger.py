# command --> pytest --cov-report term-missing --cov=backup ./tests/
#   run from parent directory for 'src' and 'tests'.

import os
import sys

# import time

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

import pytest
from lbk_library import Dbal  # IniFileParser

from build_filesystem import (
#    add_files,
#    additional_files,
#    directories,
    filesystem,
#    get_test_config,
#    load_directory_set,
)
from logger import Logger
from result_codes import ResultCodes


def test_Logger_01(filesystem):
    """
    Testing Backup.Logger.__init__()

    Test the the object is really a Logger class
    """
    source, dest = filesystem
    path = dest / "./test_log.db"  # temp location
    logger = Logger(path)
    assert isinstance(logger, Logger)
    # end test_Logger_01()


def test_Logger_02(filesystem):
    """
    Testing Backup.Logger.close_log()

    The database should be closed after the call
    """
    source, dest = filesystem
    path = dest / "./test_log.db"  # temp location
    logger = Logger(path)
    assert logger.log_db
    assert logger.log_db.sql_is_connected()
    logger.close_log()
    assert not logger.log_db.sql_is_connected()
    # end test_Logger_02()


def test_Logger_03(filesystem):
    """
    Testing Backup.Logger.create_log_database()

    Call with empty path. Should raise a FileNotFound exception.
    """
    source, dest = filesystem
    path = dest / "./test_log.db"
    logger = Logger(path)

    with pytest.raises(FileNotFoundError) as pytest_wrapped_e:
        logger.create_log_database("")
    assert pytest_wrapped_e.type == FileNotFoundError
    assert str(pytest_wrapped_e.value) == "Log Database path cannot be empty."
    # end test_Logger_03()


def test_Logger_04(filesystem):
    """
    Testing Backup.Logger.create_log_database()

    Call with a temp file name. Check for table presence. Check for
    empty table. Check for columns in table.
    """
    source, dest = filesystem
    path = dest / "./test_log.db"
    logger = Logger(path)

    # does path to db exist
    path = dest / "./test_log.db"
    logger.create_log_database(path)
    assert os.path.exists(path)
    assert logger.log_path == path

    # does table exist
    dbref = Dbal()
    dbref.sql_connect(path)
    # check table exists
    sql = (
        "SELECT count(*) FROM sqlite_master WHERE type='table'"
        + " AND name='"
        + logger.table
        + "'"
    )
    result = dbref.sql_query(sql, {})
    assert dbref.sql_fetchrow(result)["count(*)"] == 1

    # check column names and types
    sql = "PRAGMA table_info(" + logger.table + ")"
    result = dbref.sql_query(sql, {})
    table_desc = dbref.sql_fetchrowset(result)
    assert len(table_desc) == len(logger.table_def)
    for row in logger.table_def:
        print(row)
        db_row = next(
            (table_row for table_row in table_desc if table_row["name"] == row["name"]),
            None,
        )
        print(db_row)
        assert db_row["name"] == row["name"]
        assert db_row["type"] == row["type"]

    logger.close_log()
    # end test_Logger_04()


def test_logger_05(filesystem):
    """
    Test Backup.dd_log_entry()

    Generate a valid log entry, write to database, cheek the resulting
    row
    """
    source, dest = filesystem
    path = dest / "./test_log.db"
    logger = Logger(path)
    assert logger.log_db.sql_is_connected()
    time = 1000000
    result_code = ResultCodes.NO_CONFIG_FILE
    description = "Test"
    entry = {"timestamp": time, "result": result_code, "description": description}
    logger.add_log_entry(entry)
    # test results
    dbref = Dbal()
    dbref.sql_connect(path)
    sql = "SELECT * FROM " + logger.table
    result = dbref.sql_query(sql, {})
    data = dbref.sql_fetchrow(result)
    assert data["timestamp"] == time
    assert data["result"] == result_code
    assert data["description"] == description
    logger.close_log()
    # end test_logger_05()


# end test_backup_02_logger.py
