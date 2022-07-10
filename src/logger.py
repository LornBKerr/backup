"""
Manage the database log of backup actions.

File:       logger.py
Author:     Lorn B Kerr
Copyright:  (c) 2022 Lorn B Kerr
License:    see LICENSE file
"""

from lbk_library import Dbal, IniFileParser


class Logger:
    """
    Manage the database log of backup actions.
    """
    def __init__(self, log_path:str = "") -> None:
        self.log_path = log_path
        print(self.log_path)
        
