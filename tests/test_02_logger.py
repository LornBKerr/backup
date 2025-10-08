"""
Test the Logger class functionality.

File:       test_02_logger.py
Author:     Lorn B Kerr
Copyright:  (c) 2022 - 2025 Lorn B Kerr
License:    MIT, see file LICENSE
Version:    1.0.1
"""

import os
import sys

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

import pytest
from build_filesystem import filesystem
from lbk_library import DataFile

from logger import Logger
from result_codes import ResultCodes


def test_02_01_init_(filesystem):
    """
    Testing Backup.Logger.__init__()

    Test the the object is really a Logger class
    """
    source, dest = filesystem
    path = dest / "test_log.db"  # temp location
    logger = Logger(path)
    assert isinstance(logger, Logger)
    logger.log_db.sql_close()


def test_02_02_create_log_database_bad_path(filesystem):
    """
    Testing Backup.Logger.create_log_database()

    Call with empty path. Should raise a FileNotFound exception.
    """
    source, dest = filesystem
    db_path = dest / "test_log.db"

    with pytest.raises(FileNotFoundError) as pytest_wrapped_exception:
        logger = Logger()        
        logger.create_log_database("")
    assert pytest_wrapped_exception.type == FileNotFoundError
    assert str(pytest_wrapped_exception.value) == "Log Database path cannot be empty."


def test_02_03_create_log_database(filesystem):
    """
    Call with a temp file name. Check for table presence. Check for
    empty table. Check for columns in table.
    """
    source, dest = filesystem
    path = dest / "test_log.db"

    # does path to db exist
    path = dest / "test_log.db"
    logger = Logger(path)
    assert os.path.exists(path)
    assert logger.log_path == path
    assert isinstance(logger.log_db, DataFile)
    assert logger.log_db.sql_is_connected()

    # check table exists
    sql = (
        "SELECT count(*) FROM sqlite_master WHERE type='table'"
        + " AND name='"
        + logger.table
        + "'"
    )
    result = logger.log_db.sql_query(sql, {})
    assert logger.log_db.sql_fetchrow(result)["count(*)"] == 1
    # check column names and types
    sql = "PRAGMA table_info(" + logger.table + ")"
    result = logger.log_db.sql_query(sql, {})
    table_desc = logger.log_db.sql_fetchrowset(result)
    assert len(table_desc) == len(logger.table_def)
    for row in logger.table_def:
        db_row = next(
            (table_row for table_row in table_desc if table_row["name"] == row["name"]),
            None,
        )
        assert db_row["name"] == row["name"]
        assert db_row["type"] == row["type"]
    logger.log_db.sql_close()
    
    # now open an existing dtafile.
    logger = Logger(path)
    assert logger.log_db.sql_is_connected()
    logger.log_db.sql_close()
    

def test_02_04_close_log(filesystem):
    """
    Testing Backup.Logger.close_log()

    The database should be closed after the call
    """
    source, dest = filesystem
    path = dest / "test_log.db"  # temp location
    logger = Logger(path)
    assert logger.log_db
    assert logger.log_db.sql_is_connected()
    logger.close_log()
    assert not logger.log_db.sql_is_connected()


def test_02_05_add_log_entry(filesystem):
    """
    Test Backup.dd_log_entry()

    Generate a valid log entry, write to database, cheek the resulting
    row
    """
    source, dest = filesystem
    path = dest / "test_log.db"
    logger = Logger(path)
    assert logger.log_db.sql_is_connected()
    time = 1000000
    result_code = ResultCodes.NO_CONFIG_FILE
    description = "Test"
    entry = {"timestamp": time, "result": result_code, "description": description}
    logger.add_log_entry(entry)
    logger.close_log()

    # test results
    logger.log_db = DataFile()
    logger.log_db.sql_connect(path)
    sql = "SELECT * FROM " + logger.table
    result = logger.log_db.sql_query(sql, {})
    data = logger.log_db.sql_fetchrow(result)
    assert data["timestamp"] == time
    assert data["result"] == result_code
    assert data["description"] == description
    logger.close_log()

