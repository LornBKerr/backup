"""
Manage the database log of backup actions.

File:       logger.py
Author:     Lorn B Kerr
Copyright:  (c) 2022 Lorn B Kerr
License:    MIT, see file LICENSE
Version:    1.0.1
"""

import os
from typing import Any

from lbk_library import DataFile


class Logger:
    """
    Manage the database log of backup actions.

    Parameters:
        log_path (str): the path to the log database
    """

    def __init__(self, log_path: str = "") -> None:
        """
        Set the path to the log file and open the log database.

        Parameters:
            log_path (str): the path to the log file.
        """
        print("logger.init()")
        self.log_path: str = log_path
        """ The full path to the logging database """
        self.log_db: Datafile = DataFile()
        """ the log database """
        self.table = "Backup_Log"
        """ The name of the table in the database """
        self.table_def = [
            {"name": "timestamp", "type": "INTEGER"},
            {"name": "result", "type": "INTEGER"},
            {"name": "description", "type": "TEXT"},
        ]

        if log_path and os.path.isfile(log_path):
            self.log_db.sql_connect(self.log_path)
        else:
            # if database file doesn't exist, create it.
            self.create_log_database(self.log_path)

    def add_log_entry(self, entry: dict[str, Any]) -> None:
        """
        Add an entry to the log database.

        All column values must be present. No Error handling.

        Parameters:
            entry (dict[str, Any]): Contains the values to be inserted.
                "timestamp" (int): Timestamp value in seconds,
                "result" (int): result code from ResultCodes
                "description" (str) description of the action.
        """
        query = {"type": "INSERT", "table": self.table}
        sql = self.log_db.sql_query_from_array(query, entry)
        self.log_db.sql_query(sql, entry)

    def close_log(self) -> None:
        """Close connection to the log database if open."""
        if self.log_db:
            self.log_db.sql_close()

    def create_log_database(self, log_path: str) -> DataFile:
        """
        Create a new Log Database.

        The database has one table with 3 fields:
            timestamp (int): When the logged event happened
            result (int): the result of the event by one of the result codes
                found in the file 'result_codes.py',
            description (str): What was the event

        If no path to the new Log Database is given, a "FileNotFoundError"
        is raised.

        Parameters:
            log_path (str): path to the new Log Database.

        Returns:
            the new database reference

        Raises:
            FileNotFoundError
        """
        if not log_path:
            raise FileNotFoundError("Log Database path cannot be empty.")

        self.log_path = log_path
        self.log_db.sql_connect(log_path)
        self.log_db.sql_query("DROP TABLE IF EXISTS " + self.table)
        create_table = "CREATE TABLE IF NOT EXISTS " + self.table + " ("
        for row_def in self.table_def:
            create_table += row_def["name"] + " " + row_def["type"] + " NOT NULL, "
        create_table = create_table[:-2]
        create_table += ")"
        self.log_db.sql_query(create_table, [])
        return self.log_db
